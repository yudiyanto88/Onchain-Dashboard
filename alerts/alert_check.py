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

LOOKBACK = 20              # baris history yang diload
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
                   ["date", "percent_btc_in_profit", "pct_sth_in_profit"]]
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

ZONE_LABELS = {
    "Z1":  "Price < STH RP — bear bottom terdalam",
    "Z1b": "STH RP ≤ Price < RP",
    "Z2":  "STH RP ≈ RP ≈ LTH RP — konvergen",
    "Z3":  "RP ≤ Price < AVIV Mean",
    "Z4":  "AVIV Mean ≤ Price < AVIV Upper",
    "Z5":  "Price ≥ AVIV Upper — puncak siklus",
}

# Batas atas tiap zona + zona tujuan kalau tembus ke atas. Z2/Z5 ditangani
# terpisah (Z2 = state konvergen tanpa batas harga tunggal, Z5 = sudah puncak).
ZONE_UPPER_BOUND = {
    "Z1":  ("STH RP", "sth_cost_basis", "Z1b"),
    "Z1b": ("RP", "realized_price", "Z2"),
    "Z3":  ("AVIV Mean", "aviv_mean_px", "Z4"),
    "Z4":  ("AVIV Upper", "aviv_upper_px", "Z5"),
}


def build_zone_block(row: pd.Series, zone: str) -> list[str]:
    price = row["btc_price"]
    lines = [f"📍 Zona {zone}: {ZONE_LABELS.get(zone, '')}"]

    if zone in ZONE_UPPER_BOUND:
        label, col, target = ZONE_UPPER_BOUND[zone]
        level = row[col]
        pct = (level / price - 1) * 100
        lines.append(f"⬆️ Ke atas: {label} ${level:,.0f} ({pct:+.1f}%) → masuk {target}")
    elif zone == "Z5":
        lines.append("⬆️ Sudah di puncak zona — tidak ada batas atas")
    elif zone == "Z2":
        lines.append("⬆️ Zona transisi (konvergen) — tunggu breakout arah Z3")

    cvdd = row["cvdd"]
    cvdd_ratio = price / cvdd
    cvdd_pct = (cvdd / price - 1) * 100
    lines.append(f"⬇️ Ke bawah: CVDD ${cvdd:,.0f} ({cvdd_pct:+.1f}%) | Price/CVDD {cvdd_ratio:.2f} (K4 flag ≤1.10)")

    return lines


def build_k3_k4_block(df: pd.DataFrame) -> list[str]:
    """Status posisi short K3 user + progres menuju trigger K4.
    Asumsi K3_ACTIVE (bukan auto-detect dari histori) — update manual di
    config kalau posisi berubah."""
    today = df.iloc[-1]
    price = today["btc_price"]
    pnl_pct = (K3_SHORT_ENTRY_PRICE - price) / K3_SHORT_ENTRY_PRICE * 100

    lines = [
        f"🎯 *K3 — Short aktif* (entry ~${K3_SHORT_ENTRY_PRICE:,.0f})",
        f"Unrealized: {pnl_pct:+.1f}%",
        "",
        "*Exit check K3:*",
    ]

    # Kondisi 1: 4 hari berturutan close > AVIV Mean, tapi harga masih < STH RP
    last4 = df.tail(4)
    above_mean_streak = len(last4) >= 4 and (last4["btc_price"] > last4["aviv_mean_px"]).all()
    below_sth = price < today["sth_cost_basis"]
    cond1 = above_mean_streak and below_sth
    lines.append(f"• 4hr close > AVIV Mean, masih < STH RP: {'✅ kurangi ukuran short' if cond1 else 'belum'}")

    # Kondisi 2: harga balik ke Z5 dan bertahan ≥3 hari
    last3 = df.tail(3)
    zones3 = last3.apply(classify_zone, axis=1)
    cond2 = len(last3) >= 3 and (zones3 == "Z5").all()
    lines.append(f"• Balik ke Z5 (≥3 hari): {'✅ tutup short penuh' if cond2 else 'belum'}")

    # Kondisi 3: K4 mulai aktif (zona Z1 hari ini)
    cond3 = classify_zone(today) == "Z1"
    lines.append(f"• K4 mulai aktif (Z1): {'✅ tutup short, alih ke akumulasi' if cond3 else 'belum'}")

    # K4 watch — 4 kondisi framework
    lth_mvrv = today["lth_mvrv"]
    c1 = lth_mvrv < 1.0

    asopr_7d = df.tail(7)["asopr"]
    asopr_streak_ok = len(asopr_7d) >= 7 and (asopr_7d < 0.93).all()
    lth_sopr_ok = today["lth_sopr"] < 0.50
    c2 = asopr_streak_ok and lth_sopr_ok

    c3 = today["percent_btc_in_profit"] < 50 and today["pct_sth_in_profit"] < 10

    c4 = (price / today["cvdd"]) < 1.10

    k4_score = sum([c1, c2, c3, c4])
    lines += [
        "",
        f"*K4 watch ({k4_score}/4 kondisi):*",
        f"• LTH-MVRV < 1.0: {'✅' if c1 else '—'} ({lth_mvrv:.2f})",
        f"• aSOPR<0.93×7hr & LTH-SOPR<0.50: {'✅' if c2 else '—'} (LTH-SOPR {today['lth_sopr']:.2f})",
        f"• Supply Profit<50% & STH<10%: {'✅' if c3 else '—'} ({today['percent_btc_in_profit']:.1f}% / {today['pct_sth_in_profit']:.1f}%)",
        f"• Price/CVDD < 1.10: {'✅' if c4 else '—'} ({price / today['cvdd']:.2f})",
    ]
    return lines


def build_message(row: pd.Series, triggered: list[Condition], df: pd.DataFrame) -> str:
    zone     = classify_zone(row)
    date_str = str(row["date"])[:10]

    if triggered:
        lines = [
            f"🔔 *BTC ALERT — {date_str}*",
            f"Harga: *${row['btc_price']:,.0f}* | Zona: *{zone}*",
        ]
    else:
        lines = [
            f"📊 BTC Status — {date_str}",
            f"Harga: *${row['btc_price']:,.0f}* | Zona: *{zone}*",
        ]

    lines.append("")
    lines += build_zone_block(row, zone)

    if K3_ACTIVE:
        lines.append("")
        lines += build_k3_k4_block(df)

    if triggered:
        lines += ["", "*KONDISI AKTIF:*"]
        for c in triggered:
            lines.append(f"• *{c.name}*: {c.detail}")
    else:
        lines += ["", "Tidak ada kondisi khusus hari ini — cuma update rutin."]

    lines += [
        "",
        "📊 *KEY LEVELS:*",
        f"STH RP     : ${row['sth_cost_basis']:,.0f}",
        f"RP         : ${row['realized_price']:,.0f}",
        f"AVIV Mean  : ${row['aviv_mean_px']:,.0f}",
        f"AVIV Upper : ${row['aviv_upper_px']:,.0f}",
        f"CVDD       : ${row['cvdd']:,.0f}",
    ]
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
    log_path = LOG_DIR / f"alert_{date_str.replace('-', '')}.json"
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


if __name__ == "__main__":
    main()
