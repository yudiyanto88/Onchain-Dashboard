"""
alert_check.py — Conditional daily BTC on-chain alert
Kirim Telegram HANYA kalau ada kondisi framework yang trigger.

Requires env vars (GitHub Secrets):
  TELEGRAM_BOT_TOKEN  — bot token dari @BotFather
  TELEGRAM_CHAT_ID    — chat_id tujuan (personal atau group)
"""

import os
import sys
import json
import requests
import pandas as pd
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import framework_v2

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
LOG_DIR = REPO_ROOT / "alerts" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

LOOKBACK = 120             # baris history untuk checker & blok K (≥104 utk K1 gap MA90-MA60 + declining 14d)
PULLBACK_WINDOW = 14       # hari untuk deteksi pullback 5%

# --- Posisi user saat ini — update manual kalau posisi berubah ---
K3_ACTIVE = True           # short K3 lagi jalan; set False kalau sudah ditutup
K3_SHORT_ENTRY_PRICE = 79000  # harga entry short (Oktober 2025)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _load(path: Path, date_col: str = "date") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=[date_col])
    return df.sort_values(date_col).reset_index(drop=True)


def load_data() -> pd.DataFrame:
    """Histori PENUH + kolom v2 (zona, status pasar, gate/veto). Status pasar v2
    butuh histori panjang (SMA180, lock alarm bear) — main() yang memotong ke LOOKBACK."""
    price    = _load(REPO_ROOT / "data_price_level.csv")
    mvrv     = _load(REPO_ROOT / "data_mvrv.csv")[
                   ["date", "mvrv_ratio", "sth_mvrv", "lth_mvrv"]]
    supply   = _load(REPO_ROOT / "data_supply.csv")[
                   ["date", "percent_btc_in_profit", "pct_sth_in_profit", "pct_lth_in_profit"]]
    momentum = _load(REPO_ROOT / "data_momentum.csv")[
                   ["date", "asopr", "lth_sopr", "sth_sopr"]]

    df = price.merge(mvrv, on="date", how="left")
    df = df.merge(supply, on="date", how="left")
    df = df.merge(momentum, on="date", how="left")

    # AVIV ratio & bands per tanggal. NOTE: ChartInspect's own price_at_aviv_mean /
    # price_at_aviv_plus_1_sigma columns use active_realized_price as base, yang salah
    # (base yang benar = btc_price / aviv_ratio) — lihat fix di archive/app_v1.py load_data_aviv() dan dashboard/data.py.
    # Di sini kita hitung sendiri dari kolom mentah, bukan ambil kolom turunan ChartInspect.
    aviv = _load(REPO_ROOT / "data_aviv.csv")[
               ["date", "aviv_ratio", "aviv_mean", "aviv_upper_1sd"]]
    df = df.merge(aviv, on="date", how="left")

    # F&G — hanya nilai terbaru
    fg = pd.read_csv(REPO_ROOT / "data_fg.csv", parse_dates=["date"])
    fg_value = float(fg.sort_values("date").iloc[-1]["Fear & Greed"])

    # Derived columns
    df["cvdd_ratio"]    = df["btc_price"] / df["cvdd"]
    aviv_base = df["btc_price"] / df["aviv_ratio"]
    # AVIV Mean price = base × mean_ratio
    df["aviv_mean_px"]  = aviv_base * df["aviv_mean"]
    # AVIV Upper = +0.5 SD ≈ midpoint antara mean dan +1 SD
    df["aviv_upper_px"] = aviv_base * (
        df["aviv_mean"] + (df["aviv_upper_1sd"] - df["aviv_mean"]) / 2
    )
    df["fg"] = fg_value

    return framework_v2.compute(df)


# ---------------------------------------------------------------------------
# Zone classifier
# ---------------------------------------------------------------------------

def classify_zone(row: pd.Series) -> str:
    """Zona v2 (struktur × posisi harga) — dihitung framework_v2.compute()."""
    return row["zone"]


# ---------------------------------------------------------------------------
# Condition result
# ---------------------------------------------------------------------------

@dataclass
class Condition:
    name: str
    fired: bool
    detail: str


# ---------------------------------------------------------------------------
# Condition checkers
# Semua terima df (20 rows), return Condition(name, fired, detail)
# ---------------------------------------------------------------------------

def check_zone_change(df: pd.DataFrame) -> Condition:
    if len(df) < 2:
        return Condition("ZONE_CHANGE", False, "")
    z_today = classify_zone(df.iloc[-1])
    z_yesterday = classify_zone(df.iloc[-2])
    if z_today != z_yesterday:
        return Condition("ZONE_CHANGE", True, f"{z_yesterday} → {z_today}")
    return Condition("ZONE_CHANGE", False, "")


def check_aviv_cross_up(df: pd.DataFrame) -> Condition:
    """Cross naik AVIV Upper: hari ini di atas, 3 hari sebelumnya semua di bawah."""
    if len(df) < 4:
        return Condition("AVIV_CROSS_UP", False, "")
    today = df.iloc[-1]
    prev3 = df.iloc[-4:-1]
    if (today["btc_price"] > today["aviv_upper_px"] and
            (prev3["btc_price"] <= prev3["aviv_upper_px"]).all()):
        return Condition("AVIV_CROSS_UP", True,
                         f"Harga ${today['btc_price']:,.0f} menembus AVIV Upper "
                         f"${today['aviv_upper_px']:,.0f} (K1 atau K2 radar)")
    return Condition("AVIV_CROSS_UP", False, "")


def check_aviv_cross_down(df: pd.DataFrame) -> Condition:
    """Cross turun AVIV Upper: kemarin di atas, hari ini di bawah."""
    if len(df) < 2:
        return Condition("AVIV_CROSS_DOWN", False, "")
    today = df.iloc[-1]
    yesterday = df.iloc[-2]
    if (today["btc_price"] <= today["aviv_upper_px"] and
            yesterday["btc_price"] > yesterday["aviv_upper_px"]):
        return Condition("AVIV_CROSS_DOWN", True,
                         f"Harga turun ke ${today['btc_price']:,.0f}, "
                         f"di bawah AVIV Upper ${today['aviv_upper_px']:,.0f} — K1 trigger zone")
    return Condition("AVIV_CROSS_DOWN", False, "")


def check_sth_rp_cross_up(df: pd.DataFrame) -> Condition:
    """Harga cross naik STH RP — Signal D K4, masuk Z1b."""
    if len(df) < 2:
        return Condition("STH_RP_CROSS_UP", False, "")
    today = df.iloc[-1]
    yesterday = df.iloc[-2]
    if (today["btc_price"] > today["sth_cost_basis"] and
            yesterday["btc_price"] <= yesterday["sth_cost_basis"]):
        return Condition("STH_RP_CROSS_UP", True,
                         f"Harga ${today['btc_price']:,.0f} menembus STH RP "
                         f"${today['sth_cost_basis']:,.0f} ke atas — Signal D K4")
    return Condition("STH_RP_CROSS_UP", False, "")


def check_sth_rp_cross_down(df: pd.DataFrame) -> Condition:
    """Harga cross turun STH RP — masuk Z1."""
    if len(df) < 2:
        return Condition("STH_RP_CROSS_DOWN", False, "")
    today = df.iloc[-1]
    yesterday = df.iloc[-2]
    if (today["btc_price"] < today["sth_cost_basis"] and
            yesterday["btc_price"] >= yesterday["sth_cost_basis"]):
        return Condition("STH_RP_CROSS_DOWN", True,
                         f"Harga ${today['btc_price']:,.0f} jatuh di bawah STH RP "
                         f"${today['sth_cost_basis']:,.0f}")
    return Condition("STH_RP_CROSS_DOWN", False, "")


def check_rp_cross_z2(df: pd.DataFrame) -> Condition:
    """STH RP cross naik melewati RP — status bear dibuka, K5 mulai (v2 §0)."""
    if len(df) < 2:
        return Condition("STH_RP_CROSS_RP", False, "")
    today, yesterday = df.iloc[-1], df.iloc[-2]
    if (today["sth_cost_basis"] > today["realized_price"] and
            yesterday["sth_cost_basis"] <= yesterday["realized_price"]):
        return Condition("STH_RP_CROSS_RP", True,
                         f"STH RP ${today['sth_cost_basis']:,.0f} naik memotong RP "
                         f"${today['realized_price']:,.0f} — status bear dibuka, K5 mulai")
    return Condition("STH_RP_CROSS_RP", False, "")


def check_bear_alarm(df: pd.DataFrame) -> Condition:
    """Alarm bear cepat (v2 §0): bunyi, dibuka lagi, atau ada sinyal pool baru hari ini."""
    today = df.iloc[-1]
    if today["fast_confirm"]:
        return Condition("BEAR_ALARM", True,
                         "Alarm bear CEPAT bunyi (2 dari 4 sinyal dalam 90 hari) — "
                         "aturan beli K2/K5 berhenti")
    if len(df) >= 2 and df.iloc[-2]["bear_active"] and not today["bear_active"]:
        return Condition("BEAR_ALARM", True, "Status bear DIBUKA — alarm cepat lepas")
    new = [BEAR_SIGNAL_NAMES[c] for c in framework_v2.SIGNALS if today[c]]
    if new and not today["alarm_locked"]:
        return Condition("BEAR_ALARM", True, "Sinyal bear baru hari ini: " + "; ".join(new))
    return Condition("BEAR_ALARM", False, "")


def check_pullback_5pct(df: pd.DataFrame) -> Condition:
    """Pullback ≥5% dari high 14 hari — entry window K5 (hanya saat K5 berlaku:
    sejak STH RP cross RP, status bukan bear)."""
    if len(df) < 2 or not df.iloc[-1]["k5_window"] or df.iloc[-1]["bear_active"]:
        return Condition("PULLBACK_5PCT", False, "")
    window = df.tail(PULLBACK_WINDOW)
    high_14d = window["btc_price"].max()
    today_price = df.iloc[-1]["btc_price"]
    pct_drop = (high_14d - today_price) / high_14d
    if pct_drop >= 0.05:
        return Condition("PULLBACK_5PCT", True,
                         f"Turun {pct_drop*100:.1f}% dari high 14D "
                         f"${high_14d:,.0f} → ${today_price:,.0f} — cek kondisi K5")
    return Condition("PULLBACK_5PCT", False, "")


def check_cvdd_approaching(df: pd.DataFrame) -> Condition:
    """Price/CVDD < 1.10 — mendekati batas historis ekstrem, K4 radar."""
    row = df.iloc[-1]
    ratio = row["cvdd_ratio"]
    if ratio < 1.10:
        return Condition("CVDD_APPROACHING", True,
                         f"Price/CVDD = {ratio:.3f} (< 1.10) — "
                         f"harga ${row['btc_price']:,.0f} mendekati CVDD ${row['cvdd']:,.0f}")
    return Condition("CVDD_APPROACHING", False, "")


def check_supply_profit_drop(df: pd.DataFrame) -> Condition:
    """Supply in Profit tadi > 90% dan sekarang turun — K1 signal 5."""
    if len(df) < 2:
        return Condition("SUPPLY_PROFIT_DROP", False, "")
    yesterday_pct = float(df.iloc[-2]["percent_btc_in_profit"])
    today_pct     = float(df.iloc[-1]["percent_btc_in_profit"])
    if yesterday_pct > 90 and today_pct < yesterday_pct:
        return Condition("SUPPLY_PROFIT_DROP", True,
                         f"Supply Profit turun {yesterday_pct:.1f}% → {today_pct:.1f}% "
                         f"(was > 90%) — K1 signal 5")
    return Condition("SUPPLY_PROFIT_DROP", False, "")


def check_sth_mvrv_low(df: pd.DataFrame) -> Condition:
    """STH-MVRV < 1.05 saat harga masih di atas STH RP — K1 signal 3."""
    row = df.iloc[-1]
    if row["sth_mvrv"] < 1.05 and row["btc_price"] > row["sth_cost_basis"]:
        return Condition("STH_MVRV_LOW", True,
                         f"STH-MVRV = {row['sth_mvrv']:.3f} (< 1.05) "
                         f"saat harga masih di atas STH RP — K1 signal 3")
    return Condition("STH_MVRV_LOW", False, "")


def check_cvdd_touch(df: pd.DataFrame) -> Condition:
    """Price/CVDD ≤ 1.0 — event langka sekali, K4 flag ekstrem."""
    row = df.iloc[-1]
    ratio = row["cvdd_ratio"]
    if ratio <= 1.0:
        return Condition("CVDD_TOUCH", True,
                         f"‼️ Price/CVDD = {ratio:.4f} ≤ 1.0 — "
                         f"EXTREMELY RARE (< 2 hari dalam 10 tahun data) — K4 deploy 50% cash")
    return Condition("CVDD_TOUCH", False, "")


ALL_CHECKERS = [
    check_zone_change,
    check_aviv_cross_up,
    check_aviv_cross_down,
    check_sth_rp_cross_up,
    check_sth_rp_cross_down,
    check_rp_cross_z2,
    check_bear_alarm,
    check_pullback_5pct,
    check_cvdd_approaching,
    check_supply_profit_drop,
    check_sth_mvrv_low,
    check_cvdd_touch,
]


# ---------------------------------------------------------------------------
# Message builder
# ---------------------------------------------------------------------------

# Deskripsi singkat tiap zona (dipakai berulang di berbagai tempat pesan,
# supaya Z[x] apapun yang disebut selalu ada penjelasannya).
ZONE_DESC_SHORT = {
    "ZC":  "capitulation, harga di bawah RP",
    "ZD":  "dip dalam, harga antara RP dan STH RP",
    "Z1":  "struktur terbalik, harga di bawah STH RP, bear bottom",
    "Z1b": "struktur terbalik, harga antara STH RP dan RP",
    "Z2":  "STH RP≈RP≈LTH RP, konvergen",
    "Z2t": "transisi, struktur terbalik tapi harga di atas RP",
    "Z3":  "harga antara STH RP dan AVIV Mean",
    "Z4":  "harga antara AVIV Mean–AVIV Upper",
    "Z5":  "puncak siklus, di atas AVIV Upper",
}

# Batas atas tiap zona + zona tujuan kalau tembus ke atas. Z2/Z2t/Z5 ditangani
# terpisah (Z2 = state konvergen tanpa batas harga tunggal, Z5 = sudah puncak).
ZONE_UPPER_BOUND = {
    "ZC":  ("RP", "realized_price", "ZD"),
    "ZD":  ("STH RP", "sth_cost_basis", "Z3"),
    "Z1":  ("STH RP", "sth_cost_basis", "Z1b"),
    "Z1b": ("RP", "realized_price", "Z2t"),
    "Z3":  ("AVIV Mean", "aviv_mean_px", "Z4"),
    "Z4":  ("AVIV Upper", "aviv_upper_px", "Z5"),
}

# 4 sinyal pool alarm bear cepat (v2 §0)
BEAR_SIGNAL_NAMES = {
    "sig_A": "harga turun dari Z5 menembus AVIV Upper",
    "sig_B": "gap MA90−MA60 STH-SOPR memuncak lalu turun ≥14 hari",
    "sig_C": "MVRV Momentum bearish cross ≥7 hari",
    "sig_D": "MVRV Ratio di bawah SMA180 ≥7 hari (Z5 ≤120 hari lalu)",
}


def zone_numeric_desc(row: pd.Series, zone: str) -> str:
    """Deskripsi zona SAAT INI dengan angka $ asli (bukan label generik)."""
    sth_rp, rp = row["sth_cost_basis"], row["realized_price"]
    aviv_mean, aviv_upper = row["aviv_mean_px"], row["aviv_upper_px"]
    if zone == "ZC":
        return f"capitulation, harga di bawah RP ${rp:,.0f}"
    if zone == "ZD":
        return f"dip dalam, harga antara RP ${rp:,.0f} – STH RP ${sth_rp:,.0f}"
    if zone == "Z1":
        return f"harga di bawah STH RP ${sth_rp:,.0f}, bear bottom"
    if zone == "Z1b":
        return f"harga antara STH RP ${sth_rp:,.0f} – RP ${rp:,.0f}"
    if zone in ("Z2", "Z2t"):
        return ZONE_DESC_SHORT[zone]
    if zone == "Z3":
        return f"harga antara STH RP ${sth_rp:,.0f} – AVIV Mean ${aviv_mean:,.0f}"
    if zone == "Z4":
        return f"harga antara AVIV Mean ${aviv_mean:,.0f} – AVIV Upper ${aviv_upper:,.0f}"
    if zone == "Z5":
        return f"harga di atas AVIV Upper ${aviv_upper:,.0f}, puncak siklus"
    return ""


def build_status_block(df: pd.DataFrame) -> list[str]:
    """Status pasar v2 §0 — menentukan aturan mana yang hidup."""
    today = df.iloc[-1]
    if today["bear_active"]:
        inverted = today["sth_cost_basis"] < today["realized_price"]
        unlock = ("STH RP naik memotong RP" if inverted else
                  "STH RP naik memotong RP setelah sempat terbalik (sekarang belum terbalik), "
                  "atau harga ≥7 hari di Z5")
        return [
            f"*🧭 Status Pasar: BEAR* (alarm cepat bunyi {today['bear_since']:%d %b %Y})",
            "Aturan beli K2/K5 berhenti.",
            f"Dibuka lagi kalau: {unlock}",
        ]
    if today["alarm_locked"]:
        return ["*🧭 Status Pasar: BULL* (status bear sudah dibuka)",
                "Alarm bear cepat belum bisa bunyi lagi sampai harga ≥7 hari di Z5."]
    recent = df[(df["date"] >= today["date"] - pd.Timedelta(days=framework_v2.PAIR_WINDOW))
                & ~df["alarm_locked"]]
    fired = [(c, recent.loc[recent[c], "date"].iloc[-1]) for c in framework_v2.SIGNALS if recent[c].any()]
    lines = [f"*🧭 Status Pasar: BULL* (alarm bear cepat {len(fired)}/4 sinyal dalam 90 hari, bunyi kalau 2)"]
    lines += [f"⚠️ {BEAR_SIGNAL_NAMES[c]} ({d:%d %b})" for c, d in fired]
    return lines


def build_zone_block(row: pd.Series, zone: str) -> list[str]:
    price = row["btc_price"]
    lines = ["*📍 Zona*"]

    if zone in ZONE_UPPER_BOUND:
        label, col, target = ZONE_UPPER_BOUND[zone]
        level = row[col]
        pct = (level / price - 1) * 100
        lines.append(f"⬆️ {label} {pct:+.1f}% → {target} ({ZONE_DESC_SHORT[target]})")
    elif zone == "Z5":
        lines.append("⬆️ Sudah di puncak zona — tidak ada batas atas")
    elif zone in ("Z2", "Z2t"):
        lines.append("⬆️ Zona transisi — tunggu breakout arah Z3")

    cvdd = row["cvdd"]
    cvdd_ratio = price / cvdd
    cvdd_pct = (cvdd / price - 1) * 100
    lines.append(f"⬇️ CVDD {cvdd_pct:+.1f}% (Price/CVDD {cvdd_ratio:.2f})")

    return lines


def build_k3_k4_block(df: pd.DataFrame) -> list[str]:
    """Status posisi short K3 user + progres menuju trigger K4.
    Asumsi K3_ACTIVE (bukan auto-detect dari histori) — update manual di
    config kalau posisi berubah."""
    today = df.iloc[-1]
    price = today["btc_price"]
    pnl_pct = (K3_SHORT_ENTRY_PRICE - price) / K3_SHORT_ENTRY_PRICE * 100

    lines = [
        f"*📉 K3 — Short/Hedge* (AKTIF, entry ${K3_SHORT_ENTRY_PRICE:,.0f}, {pnl_pct:+.1f}%)",
        "Exit kalau salah satu ini kejadian:",
    ]

    # Kondisi 1: 4 hari berturutan close > AVIV Mean, tapi harga masih < STH RP
    last4 = df.tail(4)
    above_mean_streak = len(last4) >= 4 and (last4["btc_price"] > last4["aviv_mean_px"]).all()
    below_sth = price < today["sth_cost_basis"]
    cond1 = above_mean_streak and below_sth
    mark1 = "✅" if cond1 else "❌"
    lines.append(
        f"{mark1} Harga 4 hari beruntun di atas AVIV Mean, tapi masih di bawah "
        f"STH RP (${today['sth_cost_basis']:,.0f}) → kurangi sizing short"
    )

    # Kondisi 2: harga balik ke Z5 dan bertahan ≥3 hari
    last3 = df.tail(3)
    zones3 = last3.apply(classify_zone, axis=1)
    cond2 = len(last3) >= 3 and (zones3 == "Z5").all()
    mark2 = "✅" if cond2 else "❌"
    lines.append(
        f"{mark2} Harga balik ke Z5 ({ZONE_DESC_SHORT['Z5']}) & bertahan 3 hari "
        f"→ tutup short penuh (bacaan K3 salah)"
    )

    # Kondisi 3: K4 mulai aktif — Z1/Z1b, atau K4-tanpa-Z1 (ZC + ≥3/4 + alarm bear cepat)
    k4_score, k4_lines, _ = _k4_scorecard(df)
    cond3 = _k4_active(today, k4_score)
    mark3 = "✅" if cond3 else "❌"
    lines.append(
        f"{mark3} K4 mulai aktif (masuk Z1, atau di ZC dengan K4 ≥3/4 + alarm bear cepat) "
        f"→ tutup short, pindah ke akumulasi"
    )

    # Kondisi 4: lantai waktu — ≥9 bulan sejak puncak siklus DAN close < RP
    mark4 = "✅" if today["tf_on"] else "❌"
    lines.append(
        f"{mark4} Lantai waktu: {today['months_since_peak']:.1f} bulan sejak puncak (target ≥9) "
        f"& harga di bawah RP (${today['realized_price']:,.0f}) → kurangi short bertahap, lalu DCA 5%/bulan"
    )

    # K4 watch — 4 kondisi framework (scorecard dipakai bareng build_k4_block)
    lines += ["", f"*🎯 K4 — Akumulasi Bear Bottom* ({k4_score}/4 kondisi)"]
    lines += k4_lines
    return lines


def _k4_scorecard(df: pd.DataFrame) -> tuple[int, list[str], bool]:
    """4 kondisi K4 (agresivitas DCA). Return (score, display_lines, extreme_flag).
    extreme_flag = Price/CVDD ≤ 1.0 (event langka → deploy 50% sekaligus)."""
    today = df.iloc[-1]
    price = today["btc_price"]

    lth_mvrv = today["lth_mvrv"]
    c1 = lth_mvrv < 1.0

    asopr_streak = 0
    for v in df["asopr"].iloc[::-1]:
        if v < 0.93:
            asopr_streak += 1
        else:
            break
    lth_sopr = today["lth_sopr"]
    c2 = asopr_streak >= 7 and lth_sopr < 0.50

    supply_profit, sth_profit = today["percent_btc_in_profit"], today["pct_sth_in_profit"]
    c3 = supply_profit < 50 and sth_profit < 10

    cvdd_ratio_now = price / today["cvdd"]
    c4 = cvdd_ratio_now < 1.10

    lines = [
        f"{'✅' if c1 else '❌'} LTH-MVRV {lth_mvrv:.2f} (target <1.0)",
        f"{'✅' if c2 else '❌'} aSOPR streak {asopr_streak} hari (target ≥7 hari) & LTH-SOPR {lth_sopr:.2f} (target <0.50)",
        f"{'✅' if c3 else '❌'} Supply Profit {supply_profit:.1f}% / STH {sth_profit:.1f}% (target <50% / <10%)",
        f"{'✅' if c4 else '❌'} Price/CVDD {cvdd_ratio_now:.2f} (target <1.10)",
    ]
    return sum([c1, c2, c3, c4]), lines, cvdd_ratio_now <= 1.0


def _k4_active(today: pd.Series, score: int) -> bool:
    """K4 aktif? Jalur utama (Z1/Z1b) atau K4-tanpa-Z1 (ZC + count ≥3 + alarm bear cepat)."""
    zone = today["zone"]
    return zone in ("Z1", "Z1b") or (zone == "ZC" and score >= 3 and bool(today["bear_active"]))


def build_k4_block(df: pd.DataFrame) -> list[str]:
    """K4 — Akumulasi bear bottom (Z1/Z1b/ZC). Standalone (dipakai saat K3 sudah
    ditutup). Skor 0-4 → agresivitas DCA; v2 menambah K4-tanpa-Z1 dan lantai waktu."""
    today = df.iloc[-1]
    zone = today["zone"]
    score, cond_lines, extreme = _k4_scorecard(df)
    dca = {
        0: "Belum beli — pantau saja",
        1: "Belum beli — pantau saja",
        2: "DCA ringan: 15%/bln dari cash pool + income langsung masuk",
        3: "DCA agresif: 25%/bln dari cash pool + income langsung masuk",
        4: "DCA maksimal: 35%/bln dari cash pool + income langsung masuk",
    }[score]
    lines = [f"*🎯 K4 — Akumulasi Bear Bottom* ({score}/4 kondisi)"]
    lines += cond_lines

    # Signal D: harga > STH RP ≥3 hari → K4 & lantai waktu selesai
    above_sth = 0
    for p, s in zip(df["btc_price"].iloc[::-1], df["sth_cost_basis"].iloc[::-1]):
        if p > s:
            above_sth += 1
        else:
            break
    if above_sth >= 3:
        lines.append(f"→ Signal D nyala (harga di atas STH RP {above_sth} hari) — K4 selesai, stop DCA")
    elif _k4_active(today, score):
        jalur = "K4-tanpa-Z1 aktif (≥3/4 + alarm bear cepat)" if zone == "ZC" else "Jalur utama"
        lines.append(f"→ {jalur}: {dca}")
    elif today["tf_on"]:
        lines.append(
            f"→ Lantai waktu aktif ({today['months_since_peak']:.1f} bulan sejak puncak & harga di bawah RP): "
            f"DCA 5% cash pool/bulan. Spot only — tidak menyentuh loan/LTV")
    else:
        lines.append(
            f"→ TUNGGU, jangan deploy. K4-tanpa-Z1 butuh ≥3/4 + alarm bear cepat; "
            f"lantai waktu butuh ≥9 bulan sejak puncak (sekarang {today['months_since_peak']:.1f})")
    if extreme:
        lines.append("‼️ Price/CVDD ≤ 1.0 (langka, <2 hari/10thn) → boleh deploy 50% sisa cash pool hari ini")
    return lines


def build_k5_block(df: pd.DataFrame) -> list[str]:
    """K5 — Deploy loan di awal bull (Z2/Z3).
    Masuk hanya setelah pullback ≥5% dari high lokal, lalu tentukan besar deploy
    dari F&G dan STH Loss / SOPR. LTV cap 45% (v2 — agresivitas = kecepatan deploy)."""
    today = df.iloc[-1]
    price = today["btc_price"]

    window   = df.tail(PULLBACK_WINDOW)
    high_loc = window["btc_price"].max()
    pullback = (high_loc - price) / high_loc * 100 if high_loc > 0 else 0.0

    fg          = today["fg"]
    sth_loss    = 100 - today["pct_sth_in_profit"]
    sopr_min    = min(today["asopr"], today["sth_sopr"])

    has_pullback = pullback >= 5
    c_fg         = fg < 50
    c_loss_sopr  = sth_loss >= 50 or sopr_min <= 0.98

    # Ladder deploy sesuai tabel framework (semua mensyaratkan pullback ≥5% dulu)
    if not has_pullback:
        deploy = "Belum masuk — tunggu pullback ≥5% dari high lokal"
    elif c_fg and c_loss_sopr:
        deploy = "Deploy 100% kapasitas sisa"
    elif c_loss_sopr:
        deploy = "Deploy 70–80% kapasitas sisa"
    elif c_fg:
        deploy = "Deploy 50–60% kapasitas sisa"
    else:
        deploy = "Pullback cukup, tapi F&G/SOPR belum — tunggu konfirmasi"

    return [
        "*🏗️ K5 — Deploy Loan Awal Bull*",
        f"{'✅' if has_pullback else '❌'} Pullback {PULLBACK_WINDOW}D {pullback:.1f}% "
        f"(high ${high_loc:,.0f} → ${price:,.0f}, target ≥5%)",
        f"{'✅' if c_fg else '❌'} F&G {fg:.0f} (target <50)",
        f"{'✅' if c_loss_sopr else '❌'} STH Loss {sth_loss:.1f}% (≥50%) "
        f"atau min(aSOPR,STH-SOPR) {sopr_min:.2f} (≤0.98)",
        f"→ {deploy}. LTV cap 45%.",
    ]


def _find_local_highs(prices: list[float], w: int = 5) -> list[int]:
    """Index harga yang lebih tinggi dari w hari sebelum DAN w hari sesudah.
    Butuh w hari data setelahnya, jadi local high baru terkonfirmasi H+w."""
    highs = []
    for i in range(w, len(prices) - w):
        before = max(prices[i - w:i])
        after  = max(prices[i + 1:i + w + 1])
        if prices[i] > before and prices[i] > after:
            highs.append(i)
    return highs


def build_k6_block(df: pd.DataFrame) -> list[str]:
    """K6 — Kurangi loan tiap local high baru (Z2/Z3).
    Local high = harga > 5 hari sebelum & sesudah → baru terkonfirmasi H+5.
    Aksi: bayar loan sampai LTV turun 10 poin (butuh LTV live user — belum di-state)."""
    prices = df["btc_price"].tolist()
    highs  = _find_local_highs(prices, w=5)

    lines = ["*📉 K6 — Kurangi Loan di Local High*"]

    if not highs:
        lines.append("❌ Belum ada local high baru terkonfirmasi (butuh 5 hari data sesudah)")
        return lines

    last_idx  = highs[-1]
    last_high = prices[last_idx]
    days_ago  = len(prices) - 1 - last_idx  # ==5: high 5 hari lalu, baru terkonfirmasi HARI INI
    prev_high = prices[highs[-2]] if len(highs) >= 2 else None

    # Trigger K6 = local high baru DAN lebih tinggi dari sebelumnya.
    # "baru" = baru terkonfirmasi hari ini (days_ago==5). Local high lama yang sudah
    # terkonfirmasi berhari-hari lalu berarti aksinya seharusnya sudah diambil — jangan
    # ulang sinyal basi tiap hari.
    just_confirmed = days_ago == 5
    is_higher      = prev_high is None or last_high > prev_high

    if just_confirmed and is_higher:
        cmp = "(higher high)" if prev_high else "(local high pertama di window)"
        lines.append(
            f"✅ Local high baru ${last_high:,.0f} baru terkonfirmasi hari ini {cmp} "
            f"→ bayar loan sampai LTV turun 10 poin"
        )
    elif not just_confirmed:
        lines.append(
            f"❌ Belum ada local high baru — terakhir ${last_high:,.0f} (terkonfirmasi {days_ago - 5}h lalu)"
        )
    else:  # just_confirmed but not higher
        lines.append(
            f"❌ Local high baru ${last_high:,.0f} tidak lebih tinggi dari sebelumnya "
            f"${prev_high:,.0f} — bukan trigger"
        )
    return lines


def _sth_sopr_ma_gap(df: pd.DataFrame) -> pd.Series:
    """Gap MA60 − MA90 dari STH-SOPR. Butuh ≥90 baris; NaN sebelum itu."""
    s = df["sth_sopr"]
    return s.rolling(60).mean() - s.rolling(90).mean()


def _gap_peaked_declining(gap: pd.Series, n: int = 14):
    """True kalau gap sudah turun berturut-turut ≥n hari (memuncak lalu menurun).
    Return (declining, last_value_or_None)."""
    g = gap.dropna()
    if len(g) < n + 1:
        return False, None
    recent = g.iloc[-(n + 1):]
    declining = all(recent.iloc[i] < recent.iloc[i - 1] for i in range(1, len(recent)))
    return declining, float(g.iloc[-1])


def _new_high_peaks(df: pd.DataFrame, w: int = 5) -> list[int]:
    """Index local high (w hari) yang SEKALIGUS new high di window ini —
    kandidat 'ATH baru' untuk cek diminishing MVRV/aSOPR."""
    prices = df["btc_price"].tolist()
    peaks, run = [], -1.0
    for i in _find_local_highs(prices, w):
        if prices[i] > run:
            run = prices[i]
            peaks.append(i)
    return peaks


def _diminishing_at_peaks(df: pd.DataFrame, metric: str, w: int = 5):
    """Cek metric (MVRV/aSOPR) di ATH-baru terakhir < ATH-baru sebelumnya.
    Return (fired_or_None, detail). None = belum cukup ATH di window."""
    peaks = _new_high_peaks(df, w)
    if len(peaks) < 2:
        return None, f"belum cukup ATH baru di window {len(df)}d"
    last, prev = peaks[-1], peaks[-2]
    m_last, m_prev = df[metric].iloc[last], df[metric].iloc[prev]
    return (m_last < m_prev), f"{m_last:.2f} vs ATH sebelumnya {m_prev:.2f}"


def build_k1_block(df: pd.DataFrame) -> list[str]:
    """K1 — Kurangi posisi di puncak siklus (Z5). OR-gate trigger:
    AVIV Upper cross-down ATAU gap MA90-MA60 STH-SOPR turun ≥14 hari."""
    today = df.iloc[-1]
    price = today["btc_price"]

    # Relevansi: K1 baru relevan kalau harga sudah bertahan di Z5 ≥14 hari.
    # (approx: Z5 beruntun terakhir dalam window — bukan kumulatif sepanjang siklus.)
    z5_streak = 0
    for i in range(len(df) - 1, -1, -1):
        if classify_zone(df.iloc[i]) == "Z5":
            z5_streak += 1
        else:
            break
    relevant = z5_streak >= 14

    # 5 sinyal peringatan
    mvrv_dim, mvrv_det   = _diminishing_at_peaks(df, "sth_mvrv")
    asopr_dim, asopr_det = _diminishing_at_peaks(df, "asopr")
    s3 = price > today["sth_cost_basis"] and today["sth_mvrv"] < 1.10
    gap = _sth_sopr_ma_gap(df)
    gap_declining, gap_val = _gap_peaked_declining(gap, n=14)
    prof = today["percent_btc_in_profit"]
    prof_prev = df["percent_btc_in_profit"].iloc[-2] if len(df) >= 2 else prof
    s5 = prof > 90 and prof < prof_prev

    def mark(v):  # None = data belum cukup
        return "⚠️" if v is None else ("✅" if v else "❌")

    rel_note = f"Z5 beruntun {z5_streak}d — " + ("relevan" if relevant else "perlu ≥14d, belum relevan")
    lines = [f"*🔺 K1 — Kurangi Posisi di Puncak Siklus* ({rel_note})", "5 sinyal peringatan:"]
    lines += [
        f"{mark(mvrv_dim)} MVRV turun tiap ATH baru ({mvrv_det})",
        f"{mark(asopr_dim)} aSOPR turun tiap ATH baru ({asopr_det})",
        f"{mark(s3)} Harga > STH RP tapi STH-MVRV {today['sth_mvrv']:.2f} mendekati 1.0 (<1.10)",
        f"{mark(gap_declining)} Gap MA90-MA60 STH-SOPR turun ≥14 hari"
        + (f" (gap {gap_val:+.3f})" if gap_val is not None else " (butuh ≥90 hari data)"),
        f"{mark(s5)} Supply Profit >90% & mulai turun ({prof:.1f}%)",
    ]

    # Trigger eksekusi — OR gate
    prev = df.iloc[-2] if len(df) >= 2 else today
    aviv_cross_down = price <= today["aviv_upper_px"] and prev["btc_price"] > prev["aviv_upper_px"]
    trigger = aviv_cross_down or gap_declining
    lines.append("")
    if trigger and relevant:
        why = "AVIV Upper cross-down" if aviv_cross_down else "gap MA90-MA60 turun ≥14 hari"
        lines.append(f"🔴 TRIGGER ({why}) → lunasi SEMUA loan + jual 20–30% BTC ke USDT")
    elif trigger and not relevant:
        why = "AVIV Upper cross-down" if aviv_cross_down else "gap MA90-MA60 turun ≥14 hari"
        lines.append(f"🟡 OR-gate nyala ({why}) tapi K1 belum relevan (Z5 <14 hari) — pantau, jangan eksekusi dulu")
    else:
        lines.append("→ Belum trigger. Pantau OR-gate: AVIV Upper cross-down ATAU gap MA90-MA60 turun ≥14 hari")
    return lines


def build_k2_block(df: pd.DataFrame) -> list[str]:
    """K2 — Masuk di bull dip (ZD/Z3/Z4, status bull). v2: GATE → VETO → MASUK
    (bukan hitungan 5 kondisi lagi). Funding rate (pengubah ukuran) belum dimuat di sini."""
    today = df.iloc[-1]

    stk97 = 0
    for v in df["sth_sopr"].iloc[::-1]:
        if v < 0.97:
            stk97 += 1
        else:
            break
    lthp = today["pct_lth_in_profit"]
    lthp_ma30 = df["pct_lth_in_profit"].shift(1).tail(30).mean()

    def gate(v):
        return "✅" if v else "❌"

    def veto(v):
        return "🚫" if v else "✅"

    def tgl(d):
        return f"{d:%d %b %Y}" if pd.notna(d) else "belum ada"

    bear_x, bull_x = today["last_bear_cross"], today["last_bull_cross"]
    lines = [
        "*🟢 K2 — Bull Dip Entry* (gate → veto → masuk)",
        f"MVRV Momentum: bearish cross terakhir {tgl(bear_x)} · bullish cross terakhir {tgl(bull_x)}",
        "Gate (dua-duanya harus ✅):",
        f"{gate(today['G1'])} STH-MVRV {today['sth_mvrv']:.2f} di band 0.80–0.97",
        f"{gate(today['G2'])} STH-SOPR {today['sth_sopr']:.2f} <0.97 belum >14 hari ({stk97}h) "
        f"& aSOPR {today['asopr']:.2f} >0.95",
        "Veto (satu 🚫 = jangan masuk):",
        f"{veto(today['V1'])} Supply in Profit {today['percent_btc_in_profit']:.1f}% (veto kalau ≤60%)",
        f"{veto(today['V2'])} LTH profit {lthp:.1f}% vs rata-rata 30 hari {lthp_ma30:.1f}% (veto kalau turun >2 poin)",
        f"{veto(today['stopper'])} Penghenti: MVRV di bawah SMA180 ≥7 hari & Z5 ≤120 hari lalu",
    ]

    gates = bool(today["G1"]) and bool(today["G2"])
    vetoed = bool(today["V1"]) or bool(today["V2"]) or bool(today["stopper"])
    if vetoed:
        lines.append("→ Veto nyala — jangan masuk, apapun kata gate.")
    elif not gates:
        lines.append("→ Gate belum terbuka — loan belum boleh masuk. Cash bertahap boleh sejak bearish cross "
                     "(25–30% cash K2 per pembelian, jarak ~2 minggu atau tiap turun ~7%).")
    else:
        lines.append("→ Gate terbuka, veto bersih — loan boleh masuk. LTV cap 45%.")
        if pd.notna(bull_x) and (pd.isna(bear_x) or bull_x > bear_x):
            lines.append("→ Bullish cross terkonfirmasi — top-up boleh, LTV gabungan maksimal 48%.")
    if today["fg"] < 30:
        lines.append(f"F&G {today['fg']:.0f} <30 = kelas dip dalam, BUKAN lampu hijau — periksa gate & veto lebih ketat.")
    return lines


# Registry builder per K-node + peta zona → K-node yang aktif.
# Dispatch otomatis: kalau zona/status berubah, section K ikut berubah tanpa edit build_message.
KNODE_BUILDERS = {
    "K1": build_k1_block,
    "K2": build_k2_block,
    "K4": build_k4_block,
    "K5": build_k5_block,
    "K6": build_k6_block,
}

def knodes_for(today: pd.Series) -> tuple[list[str], str]:
    """K-node aktif per tabel zona v2 §1 (zona × status pasar). Return (daftar K, catatan
    tunggu). Dipakai HANYA saat K3 sudah ditutup — kalau K3_ACTIVE, jalur K3/K4 yang dipakai."""
    zone = today["zone"]
    if zone == "Z5":
        return ["K1"], ""
    if zone in ("Z1", "Z1b", "ZC"):
        return ["K4"], ""
    if zone in ("Z2", "Z2t"):
        return ["K5", "K6"], ""
    # ZD / Z3 / Z4: aturan beli hanya hidup di status bull
    if today["bear_active"]:
        return [], "⏸️ *TUNGGU* — alarm bear cepat bunyi, aturan beli K2/K5 tidak berlaku di zona ini."
    if zone == "ZD":
        return ["K2"], ""
    if today["k5_window"]:   # naik dari bawah (sejak STH RP cross RP, belum tembus AVIV Upper 3 hari)
        return (["K5", "K6"] if zone == "Z3" else ["K6", "K2"]), ""
    return ["K2"], ""        # dip dari atas


def build_message(row: pd.Series, triggered: list[Condition], df: pd.DataFrame) -> str:
    zone     = classify_zone(row)
    date_str = row["date"].strftime("%d %b %Y")

    header = f"🔔 *BTC ALERT — {date_str}*" if triggered else f"📊 *BTC Status — {date_str}*"
    lines = [
        header,
        f"${row['btc_price']:,.0f} | Zona {zone} ({zone_numeric_desc(row, zone)})",
    ]

    lines += [""]
    lines += build_status_block(df)

    lines += [""]
    lines += build_zone_block(row, zone)

    if K3_ACTIVE:
        # Posisi short live: tampilkan jalur exit K3 + progres akumulasi K4.
        # Selama K3 aktif, node zona early-bull (K5/K6) belum berlaku (framework).
        lines += [""]
        lines += build_k3_k4_block(df)
    else:
        # Dispatch otomatis berdasarkan zona × status pasar.
        knodes, wait_note = knodes_for(row)
        if wait_note:
            lines += ["", wait_note]
        for knode in knodes:
            lines += [""]
            lines += KNODE_BUILDERS[knode](df)

    lines += ["", "*⚡ Kondisi Trigger*"]
    if triggered:
        for c in triggered:
            lines.append(f"• *{c.name}*: {c.detail}")
    else:
        lines.append("Tidak ada kondisi trigger khusus hari ini.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Telegram sender
# ---------------------------------------------------------------------------

def send_telegram(message: str) -> bool:
    if not BOT_TOKEN or not CHAT_ID:
        print("[WARN] TELEGRAM_BOT_TOKEN atau TELEGRAM_CHAT_ID tidak di-set — skip kirim.")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        print(f"[OK] Telegram terkirim (msg_id={r.json()['result']['message_id']})")
        return True
    except requests.RequestException as e:
        print(f"[ERROR] Gagal kirim Telegram: {e}")
        return False


# ---------------------------------------------------------------------------
# Log saver
# ---------------------------------------------------------------------------

def save_log(row: pd.Series, triggered: list[Condition], sent: bool) -> None:
    date_str = str(row["date"])[:10]
    log_path = LOG_DIR / f"alert_{date_str}.json"
    entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "data_date": date_str,
        "zone": classify_zone(row),
        "bear_active": bool(row["bear_active"]),
        "telegram_sent": sent,
        "triggered_count": len(triggered),
        "triggered_conditions": [{"name": c.name, "detail": c.detail} for c in triggered],
        "snapshot": {
            "price":             round(float(row["btc_price"]), 2),
            "sth_rp":            round(float(row["sth_cost_basis"]), 2),
            "rp":                round(float(row["realized_price"]), 2),
            "lth_rp":            round(float(row["lth_cost_basis"]), 2),
            "cvdd":              round(float(row["cvdd"]), 2),
            "cvdd_ratio":        round(float(row["cvdd_ratio"]), 4),
            "aviv_mean_px":      round(float(row["aviv_mean_px"]), 2),
            "aviv_upper_px":     round(float(row["aviv_upper_px"]), 2),
            "sth_mvrv":          round(float(row["sth_mvrv"]), 4),
            "supply_in_profit":  round(float(row["percent_btc_in_profit"]), 2),
            "fg":                int(row["fg"]),
        },
    }
    with open(log_path, "w") as f:
        json.dump(entry, f, indent=2)
    print(f"[OK] Log disimpan: alerts/logs/{log_path.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== BTC Alert Check ===")

    try:
        df = load_data().tail(LOOKBACK).reset_index(drop=True)
    except Exception as e:
        print(f"[ERROR] Gagal load data: {e}")
        sys.exit(1)

    today = df.iloc[-1]
    zone  = classify_zone(today)
    print(f"Date : {str(today['date'])[:10]}")
    print(f"Price: ${today['btc_price']:,.0f} | Zone: {zone}")
    print(f"STH RP: ${today['sth_cost_basis']:,.0f} | RP: ${today['realized_price']:,.0f} | "
          f"AVIV Mean: ${today['aviv_mean_px']:,.0f} | AVIV Upper: ${today['aviv_upper_px']:,.0f}")
    print()

    results   = [checker(df) for checker in ALL_CHECKERS]
    triggered = [c for c in results if c.fired]

    print(f"Conditions checked : {len(results)}")
    print(f"Conditions triggered: {len(triggered)}")
    for c in triggered:
        print(f"  ✓ {c.name}: {c.detail}")

    message = build_message(today, triggered, df)
    print("\n--- Preview Pesan ---")
    print(message)
    print("---------------------\n")
    if "--dry-run" in sys.argv:   # uji lokal: tidak kirim Telegram, tidak tulis log
        return
    sent = send_telegram(message)

    save_log(today, triggered, sent)

    if not sent:
        sys.exit(1)


if __name__ == "__main__":
    main()
