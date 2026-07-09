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

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
LOG_DIR = REPO_ROOT / "alerts" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

LOOKBACK = 120             # baris history yang diload (≥104 utk K1 gap MA90-MA60 + declining 14d)
PULLBACK_WINDOW = 14       # hari untuk deteksi pullback 5%
ZONE_CONVERGENCE_PCT = 0.02  # threshold Z2 convergence (2%)

# --- Posisi user saat ini — update manual kalau posisi berubah ---
K3_ACTIVE = True           # short K3 lagi jalan; set False kalau sudah ditutup
K3_SHORT_ENTRY_PRICE = 79000  # harga entry short (Oktober 2025)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _load_tail(path: Path, n: int, date_col: str = "date") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=[date_col])
    return df.sort_values(date_col).tail(n).reset_index(drop=True)


def load_data() -> pd.DataFrame:
    price    = _load_tail(REPO_ROOT / "data_price_level.csv", LOOKBACK)
    mvrv     = _load_tail(REPO_ROOT / "data_mvrv.csv", LOOKBACK)[
                   ["date", "sth_mvrv", "lth_mvrv"]]
    supply   = _load_tail(REPO_ROOT / "data_supply.csv", LOOKBACK)[
                   ["date", "percent_btc_in_profit", "pct_sth_in_profit", "pct_lth_in_profit"]]
    momentum = _load_tail(REPO_ROOT / "data_momentum.csv", LOOKBACK)[
                   ["date", "asopr", "lth_sopr", "sth_sopr"]]

    df = price.merge(mvrv, on="date", how="left")
    df = df.merge(supply, on="date", how="left")
    df = df.merge(momentum, on="date", how="left")

    # AVIV ratio & bands per tanggal. NOTE: ChartInspect's own price_at_aviv_mean /
    # price_at_aviv_plus_1_sigma columns use active_realized_price as base, yang salah
    # (base yang benar = btc_price / aviv_ratio) — lihat fix di app.py load_data_aviv().
    # Di sini kita hitung sendiri dari kolom mentah, bukan ambil kolom turunan ChartInspect.
    aviv = _load_tail(REPO_ROOT / "data_aviv.csv", LOOKBACK)[
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

    return df


# ---------------------------------------------------------------------------
# Zone classifier
# ---------------------------------------------------------------------------

def classify_zone(row: pd.Series) -> str:
    price    = row["btc_price"]
    sth_rp   = row["sth_cost_basis"]
    lth_rp   = row["lth_cost_basis"]
    rp       = row["realized_price"]
    av_mean  = row["aviv_mean_px"]
    av_upper = row["aviv_upper_px"]

    three_rp = [sth_rp, lth_rp, rp]
    spread   = (max(three_rp) - min(three_rp)) / min(three_rp) if min(three_rp) > 0 else 1

    if spread < ZONE_CONVERGENCE_PCT:
        return "Z2"
    if price >= av_upper:
        return "Z5"
    if price >= av_mean:
        return "Z4"
    if price >= rp:
        return "Z3"
    if price >= sth_rp:
        return "Z1b" if sth_rp < lth_rp else "Z3"
    return "Z1"


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
    """STH RP, RP, LTH RP konvergen < 2% — Z2 terbentuk, K5 mulai."""
    row = df.iloc[-1]
    sth_rp = row["sth_cost_basis"]
    rp     = row["realized_price"]
    lth_rp = row["lth_cost_basis"]
    three  = [sth_rp, rp, lth_rp]
    spread = (max(three) - min(three)) / min(three) if min(three) > 0 else 1
    if spread < ZONE_CONVERGENCE_PCT:
        return Condition("RP_CROSS_Z2", True,
                         f"STH RP/RP/LTH RP konvergen — spread {spread*100:.1f}% < 2% "
                         f"(STH ${sth_rp:,.0f} | RP ${rp:,.0f} | LTH ${lth_rp:,.0f}) — K5 dimulai")
    return Condition("RP_CROSS_Z2", False, "")


def check_pullback_5pct(df: pd.DataFrame) -> Condition:
    """Pullback ≥5% dari high 14 hari — entry window K5."""
    if len(df) < 2:
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
    "Z1":  "harga di bawah STH RP, bear bottom terdalam",
    "Z1b": "harga antara STH RP dan RP",
    "Z2":  "STH RP≈RP≈LTH RP, konvergen",
    "Z3":  "harga antara RP dan AVIV Mean",
    "Z4":  "harga antara AVIV Mean–AVIV Upper",
    "Z5":  "puncak siklus, di atas AVIV Upper",
}

# Batas atas tiap zona + zona tujuan kalau tembus ke atas. Z2/Z5 ditangani
# terpisah (Z2 = state konvergen tanpa batas harga tunggal, Z5 = sudah puncak).
ZONE_UPPER_BOUND = {
    "Z1":  ("STH RP", "sth_cost_basis", "Z1b"),
    "Z1b": ("RP", "realized_price", "Z2"),
    "Z3":  ("AVIV Mean", "aviv_mean_px", "Z4"),
    "Z4":  ("AVIV Upper", "aviv_upper_px", "Z5"),
}



def zone_numeric_desc(row: pd.Series, zone: str) -> str:
    """Deskripsi zona SAAT INI dengan angka $ asli (bukan label generik)."""
    sth_rp, rp = row["sth_cost_basis"], row["realized_price"]
    aviv_mean, aviv_upper = row["aviv_mean_px"], row["aviv_upper_px"]
    if zone == "Z1":
        return f"harga di bawah STH RP ${sth_rp:,.0f}, bear bottom terdalam"
    if zone == "Z1b":
        return f"harga antara STH RP ${sth_rp:,.0f} – RP ${rp:,.0f}"
    if zone == "Z2":
        return "STH RP≈RP≈LTH RP, konvergen"
    if zone == "Z3":
        return f"harga antara RP ${rp:,.0f} – AVIV Mean ${aviv_mean:,.0f}"
    if zone == "Z4":
        return f"harga antara AVIV Mean ${aviv_mean:,.0f} – AVIV Upper ${aviv_upper:,.0f}"
    if zone == "Z5":
        return f"harga di atas AVIV Upper ${aviv_upper:,.0f}, puncak siklus"
    return ""


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
    elif zone == "Z2":
        lines.append("⬆️ Zona transisi (konvergen) — tunggu breakout arah Z3")

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

    # Kondisi 3: K4 mulai aktif (zona Z1 hari ini)
    cond3 = classify_zone(today) == "Z1"
    mark3 = "✅" if cond3 else "❌"
    lines.append(
        f"{mark3} K4 mulai aktif, masuk Z1 ({ZONE_DESC_SHORT['Z1']}) "
        f"→ tutup short, pindah ke akumulasi"
    )

    # K4 watch — 4 kondisi framework (scorecard dipakai bareng build_k4_block)
    k4_score, k4_lines, _ = _k4_scorecard(df)
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


def build_k4_block(df: pd.DataFrame) -> list[str]:
    """K4 — Akumulasi agresif bear bottom (Z1/Z1b). Standalone (dipakai saat
    K3 sudah ditutup). Skor 0-4 → agresivitas DCA per framework."""
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
    lines.append(f"→ {dca}")
    if extreme:
        lines.append("‼️ Price/CVDD ≤ 1.0 (langka, <2 hari/10thn) → boleh deploy 50% sisa cash pool hari ini")
    return lines


def build_k5_block(df: pd.DataFrame) -> list[str]:
    """K5 — Deploy loan di awal bull (Z2/Z3).
    Masuk hanya setelah pullback ≥5% dari high lokal, lalu tentukan besar deploy
    dari F&G dan STH Loss / SOPR. LTV cap 52% (hard limit, tidak digeser sinyal)."""
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
        f"→ {deploy}. LTV cap 52%.",
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
    """K2 — Masuk di bull dip (Z4/Z3, turun dari zona atas). 5 kondisi →
    confidence Low/Medium/High/VeryHigh. Kondisi #5 (bounce AVIV Mean) hanya
    bisa terkonfirmasi setelah bounce, jadi ditandai terpisah."""
    today = df.iloc[-1]
    price = today["btc_price"]

    # C1: STH-MVRV<0.95 & rasio LTH/STH-MVRV naik dalam 14 hari
    sth_mvrv = today["sth_mvrv"]
    ratio_now = today["lth_mvrv"] / sth_mvrv if sth_mvrv > 0 else 0.0
    idx14 = -15 if len(df) >= 15 else 0
    base_sth = df["sth_mvrv"].iloc[idx14]
    ratio_14 = df["lth_mvrv"].iloc[idx14] / base_sth if base_sth > 0 else ratio_now
    c1 = sth_mvrv < 0.95 and ratio_now > ratio_14

    # C2: STH-SOPR<0.97 belum >14 hari & aSOPR masih >0.95
    below_streak = 0
    for v in df["sth_sopr"].iloc[::-1]:
        if v < 0.97:
            below_streak += 1
        else:
            break
    c2 = today["sth_sopr"] < 0.97 and below_streak <= 14 and today["asopr"] > 0.95

    # C3: Supply Profit >60% & STH profit turun
    sthp = today["pct_sth_in_profit"]
    sthp_prev = df["pct_sth_in_profit"].iloc[-2] if len(df) >= 2 else sthp
    c3 = today["percent_btc_in_profit"] > 60 and sthp < sthp_prev

    # C4: LTH profit stabil — tidak turun >2 poin dari rata-rata 30 hari
    lthp = today["pct_lth_in_profit"]
    lthp_ma30 = df["pct_lth_in_profit"].tail(30).mean()
    c4 = lthp >= lthp_ma30 - 2

    # C5: close < AVIV Mean lalu close balik ke atas pada/atau sebelum hari ke-4
    c5 = False
    below = today["btc_price"] < today["aviv_mean_px"]
    if not below:  # sudah balik ke atas, cek berapa lama tadi di bawah
        days_below = 0
        for i in range(len(df) - 2, -1, -1):
            if df["btc_price"].iloc[i] < df["aviv_mean_px"].iloc[i]:
                days_below += 1
            else:
                break
        c5 = 1 <= days_below <= 4

    base_conf = sum([c1, c2, c3, c4])   # C5 dihitung terpisah (post-bounce)
    total = base_conf + (1 if c5 else 0)
    level = ("Very High" if total >= 5 else "High" if total == 4
             else "Medium" if total == 3 else "Low")

    lines = [f"*🟢 K2 — Bull Dip Entry* (confidence {level}, {total}/5)"]
    lines += [
        f"{'✅' if c1 else '❌'} STH-MVRV {sth_mvrv:.2f} <0.95 & rasio LTH/STH naik 14d",
        f"{'✅' if c2 else '❌'} STH-SOPR {today['sth_sopr']:.2f} <0.97 ({below_streak}d ≤14) & aSOPR {today['asopr']:.2f} >0.95",
        f"{'✅' if c3 else '❌'} Supply Profit {today['percent_btc_in_profit']:.1f}% >60% & STH profit turun",
        f"{'✅' if c4 else '❌'} LTH profit {lthp:.1f}% stabil (≥ MA30 {lthp_ma30:.1f}% −2)",
        f"{'✅' if c5 else '⏳'} Close balik di atas AVIV Mean ≤ hari ke-4 (hanya pasti setelah bounce)",
    ]
    if level == "Low":
        lines.append("→ Low — belum ada aksi. Cash habis dulu sebelum loan; ikuti tabel deploy K2. LTV cap 52%.")
    else:
        lines.append(f"→ {level} — deploy cash 100% dulu, loan sesuai price action (tabel K2). LTV cap 52%.")
    return lines


# Registry builder per K-node + peta zona → K-node yang aktif.
# Dispatch otomatis: kalau zona berubah, section K ikut berubah tanpa edit build_message.
# (K1/K2/K4 belum di-dispatch di sini — K4 masih lewat blok K3/K4 live-position.)
KNODE_BUILDERS = {
    "K1": build_k1_block,
    "K2": build_k2_block,
    "K4": build_k4_block,
    "K5": build_k5_block,
    "K6": build_k6_block,
}

# K6 berlaku di Z2/Z3 (per seksi K6 doc: selesai saat masuk Z4). Z4 = K2 (dip dari
# Z5). Z5 = K1 (kurangi puncak) + K2 (transisi turun). Z1/Z1b pakai K4 standalone
# HANYA saat K3 sudah ditutup — kalau K3_ACTIVE, jalur K3/K4 live-position yang dipakai.
ZONE_KNODE_MAP = {
    "Z1":  ["K4"],
    "Z1b": ["K4"],
    "Z2":  ["K5", "K6"],
    "Z3":  ["K5", "K6"],
    "Z4":  ["K2"],
    "Z5":  ["K1", "K2"],
}


def build_message(row: pd.Series, triggered: list[Condition], df: pd.DataFrame) -> str:
    zone     = classify_zone(row)
    date_str = row["date"].strftime("%d %b %Y")

    header = f"🔔 *BTC ALERT — {date_str}*" if triggered else f"📊 *BTC Status — {date_str}*"
    lines = [
        header,
        f"${row['btc_price']:,.0f} | Zona {zone} ({zone_numeric_desc(row, zone)})",
    ]

    lines += [""]
    lines += build_zone_block(row, zone)

    if K3_ACTIVE:
        # Posisi short live: tampilkan jalur exit K3 + progres akumulasi K4.
        # Selama K3 aktif, node zona early-bull (K5/K6) belum berlaku (framework).
        lines += [""]
        lines += build_k3_k4_block(df)
    else:
        # Dispatch otomatis berdasarkan zona sekarang.
        for knode in ZONE_KNODE_MAP.get(zone, []):
            builder = KNODE_BUILDERS.get(knode)
            if builder:
                lines += [""]
                lines += builder(df)

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
        df = load_data()
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
    sent = send_telegram(message)

    save_log(today, triggered, sent)

    if not sent:
        sys.exit(1)


if __name__ == "__main__":
    main()
