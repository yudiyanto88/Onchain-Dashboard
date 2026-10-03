"""
framework_v2.py — zona 2 dimensi + status pasar Decision Framework v2 (§0–1) + gate/veto K2.

Logika sinyal DISALIN dari research/framework_review_2026-07/backtest/btlib.py (mesin
backtest v2) supaya alert harian == backtest. Cek paritas: alerts/test_framework_v2.py.
Butuh histori PENUH (SMA180, lock alarm bear, puncak siklus) — jangan dipanggil pada tail.
"""
import numpy as np
import pandas as pd

MIN_STREAK_DAYS = 7      # sinyal A: minimal hari di Z5 sebelum cross-down
PEAK_CONFIRM_DAYS = 14   # sinyal B: gap turun ≥14 hari setelah puncak
PAIR_WINDOW = 90         # 2 dari 4 sinyal dalam 90 hari
RESET_STREAK_Z5 = 7      # ≥7 hari di Z5 = lock alarm lepas
MVRV_HOLD_DAYS = 7
Z5_QUAL_DAYS = 120
SIGNALS = ["sig_A", "sig_B", "sig_C", "sig_D"]


def _streak(mask: pd.Series) -> pd.Series:
    """Panjang run True yang sedang berjalan (0 kalau False)."""
    mask = mask.fillna(False).astype(bool)
    return mask.astype(int).groupby((~mask).cumsum()).cumsum()


def _signals(df: pd.DataFrame) -> None:
    n = len(df)
    dts = df["date"].values
    above = (df["btc_price"] > df["aviv_upper_px"]).values
    strk = _streak(pd.Series(above)).values
    df["streak_above"] = strk

    # A: AVIV Upper cross-down setelah ≥7 hari di Z5
    sig_a = np.zeros(n, dtype=bool)
    sig_a[1:] = (~above[1:]) & (strk[:-1] >= MIN_STREAK_DAYS)

    # B: gap SMA90(STH-SOPR) − SMA60-dari-SMA90 memuncak (>0) lalu 14 hari di bawah puncak
    ma90 = df["sth_sopr"].rolling(90, min_periods=90).mean()
    g = (ma90 - ma90.rolling(60, min_periods=60).mean()).values
    sig_b = np.zeros(n, dtype=bool)
    for i in range(1, n - PEAK_CONFIRM_DAYS):
        if np.isnan(g[i]) or g[i] <= 0 or g[i] <= g[i - 1]:
            continue
        if np.all(g[i + 1:i + 1 + PEAK_CONFIRM_DAYS] < g[i]):
            sig_b[i + PEAK_CONFIRM_DAYS] = True

    # C: MVRV Momentum bearish cross, bertahan ≥7 hari
    m1 = df["mvrv_ratio"].rolling(30, min_periods=30).mean()
    m2 = m1.rolling(30, min_periods=30).mean()
    ok = (m1.notna() & m2.notna()).values
    below = ((m1 < m2) & ok).values
    sig_c = np.zeros(n, dtype=bool)
    for i in range(1, n - MVRV_HOLD_DAYS + 1):
        if ok[i] and ok[i - 1] and below[i] and not below[i - 1] \
                and np.all(below[i:i + MVRV_HOLD_DAYS]):
            sig_c[i + MVRV_HOLD_DAYS - 1] = True

    # D: MVRV < SMA180 hari ke-7, dan kunjungan Z5 terakhir ≤120 hari
    sma180 = df["mvrv_ratio"].rolling(180, min_periods=180).mean()
    run = _streak(df["mvrv_ratio"] < sma180).values
    last_z5 = pd.Series(np.where(above, dts, np.datetime64("NaT"))).ffill().values
    since_z5 = (dts - last_z5) / np.timedelta64(1, "D")   # NaN kalau belum pernah Z5
    sig_d = (run == MVRV_HOLD_DAYS) & (since_z5 <= Z5_QUAL_DAYS)

    df["sig_A"], df["sig_B"], df["sig_C"], df["sig_D"] = sig_a, sig_b, sig_c, sig_d


def _fast_confirms(df: pd.DataFrame) -> tuple[list[int], np.ndarray]:
    """Index hari alarm bear CEPAT bunyi: ≥2 tipe sinyal berbeda dalam 90 hari;
    setelah bunyi, terkunci sampai harga ≥7 hari di Z5 (sinyal selama terkunci tidak
    dihitung). Return (index bunyi, mask hari terkunci)."""
    dates = df["date"]
    strk = df["streak_above"].values
    evs = [(dates[i], t, i) for i in range(len(df)) for t in SIGNALS if df[t].values[i]]
    confirms, lock = [], -1
    locked = np.zeros(len(df), dtype=bool)
    for k, (d, _, idx) in enumerate(evs):
        if idx <= lock:
            continue
        types = set()
        for pd_, pt, pidx in reversed(evs[:k + 1]):
            if (d - pd_).days > PAIR_WINDOW:
                break
            if pidx > lock:
                types.add(pt)
        if len(types) >= 2:
            confirms.append(idx)
            after = np.nonzero(strk[idx + 1:] >= RESET_STREAK_Z5)[0]
            lock = idx + 1 + after[0] if len(after) else len(df)
            locked[idx + 1:lock + 1] = True
    return confirms, locked


def compute(df: pd.DataFrame) -> pd.DataFrame:
    """Tambah kolom v2 ke histori penuh. Kolom masuk: date, btc_price, sth_cost_basis,
    realized_price, lth_cost_basis, aviv_mean_px, aviv_upper_px, mvrv_ratio, sth_mvrv,
    sth_sopr, asopr, percent_btc_in_profit, pct_lth_in_profit."""
    df = df.dropna(subset=["btc_price", "sth_cost_basis", "realized_price", "lth_cost_basis",
                           "aviv_mean_px", "aviv_upper_px"])
    df = df[df["btc_price"] > 1].sort_values("date").reset_index(drop=True)
    n = len(df)
    P, S, R, L = df["btc_price"], df["sth_cost_basis"], df["realized_price"], df["lth_cost_basis"]
    M, U = df["aviv_mean_px"], df["aviv_upper_px"]
    _signals(df)

    # ---- Zona 2 dimensi (§1) ----
    conv = ((S - R).abs() / R < 0.02) & ((R - L).abs() / R < 0.02)
    df["struct"] = np.where(conv, "C", np.where(S > R, "N", "T"))
    df["zone"] = np.select(
        [P >= U,
         conv & (P >= M), conv,
         (S > R) & (P < R), (S > R) & (P < S), (S > R) & (P < M), S > R,
         P < S, P < R],
        ["Z5", "Z4", "Z2", "ZC", "ZD", "Z3", "Z4", "Z1", "Z1b"],
        default="Z2t")

    # ---- Status pasar: alarm bear cepat, terkunci sampai unlock (§0) ----
    confirms, df["alarm_locked"] = _fast_confirms(df)
    df["fast_confirm"] = False
    df.loc[confirms, "fast_confirm"] = True
    s, r, strk = S.values, R.values, df["streak_above"].values
    bear = np.zeros(n, dtype=bool)
    since = np.full(n, np.datetime64("NaT"), dtype="datetime64[ns]")
    for ci in confirms:
        end, inverted = n - 1, False
        for j in range(ci + 1, n):
            inverted = inverted or s[j] < r[j]
            # unlock: STH RP cross naik RP setelah sempat terbalik;
            # kalau tidak pernah terbalik: harga ≥7 hari di Z5
            if (inverted and s[j] > r[j] and s[j - 1] <= r[j - 1]) or \
                    (not inverted and strk[j] >= RESET_STREAK_Z5):
                end = j
                break
        new = ~bear[ci:end + 1]
        since[ci:end + 1][new] = df["date"].values[ci]
        bear[ci:end + 1] = True
    df["bear_active"] = bear
    df["bear_since"] = since

    # ---- K2: gate, veto, penghenti, cross MVRV Momentum ----
    b97 = df["sth_sopr"] < 0.97
    df["G1"] = (df["sth_mvrv"] >= 0.80) & (df["sth_mvrv"] < 0.97)
    df["G2"] = b97 & (_streak(b97) <= 14) & (df["asopr"] > 0.95)
    df["V1"] = df["percent_btc_in_profit"] <= 60
    df["V2"] = df["pct_lth_in_profit"] < df["pct_lth_in_profit"].shift(1).rolling(30).mean() - 2
    below180 = df["mvrv_ratio"] < df["mvrv_ratio"].rolling(180).mean()
    z5_recent = (P >= U).rolling(Z5_QUAL_DAYS, min_periods=1).max().astype(bool)
    df["stopper"] = (_streak(below180) >= 7) & z5_recent
    ma30 = df["mvrv_ratio"].rolling(30).mean()
    up = (ma30 > ma30.rolling(30).mean()).values
    bull = np.zeros(n, dtype=bool)
    for i in range(1, n - 7):
        if up[i] and not up[i - 1] and up[i:i + 7].all():
            bull[i + 7] = True
    df["bull_cross"] = bull
    df["last_bear_cross"] = df["date"].where(df["sig_C"]).ffill()
    df["last_bull_cross"] = df["date"].where(df["bull_cross"]).ffill()

    # ---- K5 window: STH RP cross naik RP .. harga ≥ AVIV Upper 3 hari (§K5) ----
    cross_up = ((S > R) & (S.shift(1) <= R.shift(1))).values
    at_upper = _streak(P >= U).values
    k5, on = np.zeros(n, dtype=bool), False
    for i in range(n):
        on = (on or cross_up[i]) and at_upper[i] < 3
        k5[i] = on
    df["k5_window"] = k5

    # ---- Lantai waktu K4: ≥9 bulan sejak puncak siklus DAN close < RP ----
    peak_idx = pd.Series(np.where(P == P.cummax(), np.arange(n), np.nan)).ffill()
    df["months_since_peak"] = ((np.arange(n) - peak_idx) / 30.0).values
    df["tf_on"] = (df["months_since_peak"] >= 9) & (P < R)
    return df
