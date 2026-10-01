"""Langkah 0: audit akses + ketersediaan data Kalshi KXFEDDECISION dan Binance BTCUSDT.

Hanya baca data publik. Tanpa kunci API. Bisa dijalankan ulang: market yang candle-nya
sudah tersimpan di data/raw/kalshi_candles_1m/ dilewati.

Keluaran:
  data/raw/access_check.json
  data/raw/kalshi_events.csv, kalshi_markets.csv   (daftar yang ditemukan lewat API)
  data/raw/kalshi_candles_1m/{ticker}.parquet      (candle 1 menit, jendela 28 hari)
  data/raw/kalshi_candles_1d/{ticker}.parquet      (candle harian, seluruh umur market)
  data/processed/audit_markets.csv, audit_events.csv
"""
import datetime as dt
import json
import re
import sys
import time
import zipfile
import io

import pandas as pd
import requests

from common import KALSHI, PROC, RAW, SERIES, WINDOW_DAYS, Kalshi

UTC = dt.timezone.utc
NOW = dt.datetime.now(UTC)
CHUNK_DAYS = 3  # 3 hari x 1440 = 4320 < batas 5000 candle per permintaan
D1 = RAW / "kalshi_candles_1d"
M1 = RAW / "kalshi_candles_1m"
for p in (D1, M1, RAW / "binance"):
    p.mkdir(parents=True, exist_ok=True)


def ts(x: dt.datetime) -> int:
    return int(x.timestamp())


def parse_iso(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


# ---------------------------------------------------------------- akses
def access_check() -> dict:
    out = {"checked_at_utc": NOW.isoformat()}
    tests = {
        "kalshi_series": f"{KALSHI}/series/{SERIES}",
        "binance_vision_monthly": "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1m/BTCUSDT-1m-2025-01.zip",
        "binance_rest_api": "https://api.binance.com/api/v3/ping",
    }
    for name, url in tests.items():
        try:
            r = requests.head(url, timeout=30, allow_redirects=True) if "vision" in url else requests.get(url, timeout=30)
            out[name] = {"status": r.status_code, "ok": r.status_code == 200}
        except Exception as e:  # noqa: BLE001
            out[name] = {"status": None, "ok": False, "error": str(e)[:200]}
    return out


def binance_check() -> dict:
    """Ketersediaan file bulanan + satuan timestamp (ms vs us) di beberapa periode."""
    base = "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1m"
    months = pd.period_range("2023-03", "2026-09", freq="M")
    avail = {}
    for m in months:
        r = requests.head(f"{base}/BTCUSDT-1m-{m}.zip", timeout=30)
        avail[str(m)] = r.status_code
    units = {}
    for m in ("2023-04", "2024-12", "2025-01", "2026-08"):
        if avail.get(m) != 200:
            continue
        f = RAW / "binance" / f"BTCUSDT-1m-{m}.zip"
        if not f.exists():
            f.write_bytes(requests.get(f"{base}/BTCUSDT-1m-{m}.zip", timeout=120).content)
        with zipfile.ZipFile(f) as z:
            with z.open(z.namelist()[0]) as fh:
                first = fh.readline().decode().strip().split(",")
        v = int(first[0])
        units[m] = {"first_open_time": v, "digits": len(str(v)), "unit": "us" if len(str(v)) >= 16 else "ms"}
    return {"monthly_http_status": avail, "timestamp_units": units}


# ---------------------------------------------------------------- Kalshi: event + market
def list_events(k: Kalshi) -> pd.DataFrame:
    rows, cur = [], ""
    while True:
        d = k.get("/events", {"series_ticker": SERIES, "limit": 200, "cursor": cur})
        rows += d["events"]
        cur = d.get("cursor", "")
        if not cur:
            break
    df = pd.DataFrame(rows)[["event_ticker", "series_ticker", "strike_date", "title", "sub_title"]]
    df["strike_dt"] = pd.to_datetime(df["strike_date"], utc=True)
    return df.sort_values("strike_dt").reset_index(drop=True)


def list_markets(k: Kalshi, event_ticker: str) -> list[dict]:
    """Gabungkan /historical/markets dan /markets (live). Tandai sumber, itu menentukan endpoint candle."""
    found = {}
    for src, path in (("historical", "/historical/markets"), ("live", "/markets")):
        cur = ""
        while True:
            d = k.get(path, {"event_ticker": event_ticker, "limit": 200, "cursor": cur})
            for m in d["markets"]:
                m["source"] = src
                found.setdefault(m["ticker"], m)
            cur = d.get("cursor", "")
            if not cur:
                break
    return list(found.values())


def parse_strike(cs: dict | None) -> tuple[str, str, bool]:
    """custom_strike -> (arah, angka, terbuka). Contoh {'Hike': '>25'} -> ('Hike','25',True)."""
    if not cs:
        return "", "", False
    (direction, val), = cs.items()
    val = str(val)
    open_ended = ">" in val
    num = re.sub(r"[^0-9.]", "", val)
    return direction, num, open_ended


# ---------------------------------------------------------------- Kalshi: candle
def candle_rows(cs: list[dict]) -> pd.DataFrame:
    """Endpoint historical memakai nama field polos (volume, close); endpoint live memakai
    sufiks (volume_fp, close_dollars). Terima keduanya."""

    def f(x):
        try:
            return float(x) if x not in (None, "") else None
        except (TypeError, ValueError):
            return None

    def g(d, key, suffixes=("", "_dollars", "_fp")):
        for sfx in suffixes:
            if d.get(key + sfx) not in (None, ""):
                return f(d.get(key + sfx))
        return None

    rows = []
    for c in cs:
        p, b, a = c.get("price", {}) or {}, c.get("yes_bid", {}) or {}, c.get("yes_ask", {}) or {}
        rows.append({
            "end_ts": c["end_period_ts"],
            "volume": g(c, "volume") or 0.0,
            "open_interest": g(c, "open_interest"),
            "p_open": g(p, "open"), "p_high": g(p, "high"), "p_low": g(p, "low"),
            "p_close": g(p, "close"), "p_mean": g(p, "mean"), "p_prev": g(p, "previous"),
            "bid_open": g(b, "open"), "bid_close": g(b, "close"),
            "ask_open": g(a, "open"), "ask_close": g(a, "close"),
        })
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df = df.drop_duplicates("end_ts").sort_values("end_ts").reset_index(drop=True)
    # candle 1m dengan end_ts=T mencakup [T-60, T): kunci menit = awal periode
    df["minute_start"] = pd.to_datetime(df["end_ts"] - 60, unit="s", utc=True)
    return df


def candle_path(m: dict) -> str:
    if m["source"] == "historical":
        return f"/historical/markets/{m['ticker']}/candlesticks"
    return f"/series/{SERIES}/markets/{m['ticker']}/candlesticks"


def fetch_candles(k: Kalshi, m: dict, start: dt.datetime, end: dt.datetime, period: int, chunk_days: int) -> pd.DataFrame:
    parts, cur = [], start
    while cur < end:
        nxt = min(cur + dt.timedelta(days=chunk_days), end)
        d = k.get(candle_path(m), {"start_ts": ts(cur), "end_ts": ts(nxt), "period_interval": period})
        if d.get("candlesticks"):
            parts.append(candle_rows(d["candlesticks"]))
        cur = nxt
    if not parts:
        return pd.DataFrame()
    return pd.concat(parts).drop_duplicates("end_ts").sort_values("end_ts").reset_index(drop=True)


# ---------------------------------------------------------------- main
def main():
    k = Kalshi()
    access = access_check()
    print("akses:", json.dumps(access))

    events = list_events(k)
    done = events[events["strike_dt"] < NOW].copy()
    print(f"event total {len(events)}, sudah lewat tanggal rapat: {len(done)}")

    mrows = []
    for _, e in done.iterrows():
        for m in list_markets(k, e["event_ticker"]):
            d, n, op = parse_strike(m.get("custom_strike"))
            mrows.append({
                "event_ticker": e["event_ticker"], "ticker": m["ticker"], "source": m["source"],
                "status": m["status"], "result": m.get("result"), "direction": d, "strike_num": n,
                "open_ended": op, "open_time": m["open_time"], "close_time": m["close_time"],
                "volume_total": float(m.get("volume_fp") or 0), "expiration_value": m.get("expiration_value"),
                "strike_date": e["strike_date"],
            })
    markets = pd.DataFrame(mrows)
    events.drop(columns="strike_dt").to_csv(RAW / "kalshi_events.csv", index=False)
    markets.to_csv(RAW / "kalshi_markets.csv", index=False)
    print(f"market ditemukan: {len(markets)} di {markets.event_ticker.nunique()} event")
    print(markets.groupby("event_ticker").size().to_string())

    # candle harian (umur penuh) + candle 1 menit (jendela 28 hari)
    arows = []
    t0 = time.time()
    for i, m in enumerate(markets.itertuples(), 1):
        mm = {"ticker": m.ticker, "source": m.source}
        strike = parse_iso(m.strike_date)
        close = parse_iso(m.close_time)
        opent = parse_iso(m.open_time)
        w_start = strike - dt.timedelta(days=WINDOW_DAYS)
        w_end = min(close, strike)

        fd = D1 / f"{m.ticker}.parquet"
        if fd.exists():
            d1 = pd.read_parquet(fd)
        else:
            d1 = fetch_candles(k, mm, opent, close + dt.timedelta(minutes=1), 1440, 1000)
            d1.to_parquet(fd)
        f1 = M1 / f"{m.ticker}.parquet"
        if f1.exists():
            c1 = pd.read_parquet(f1)
        else:
            c1 = fetch_candles(k, mm, max(w_start, opent), w_end, 1, CHUNK_DAYS)
            c1.to_parquet(f1)

        win_minutes = int((w_end - w_start).total_seconds() // 60)
        traded = c1[c1["volume"] > 0] if len(c1) else c1
        both = traded[traded["bid_close"].notna() & traded["ask_close"].notna()] if len(traded) else traded
        arows.append({
            "event_ticker": m.event_ticker, "ticker": m.ticker, "source": m.source,
            "direction": m.direction, "strike_num": m.strike_num, "open_ended": m.open_ended,
            "result": m.result, "volume_total_contracts": m.volume_total,
            "first_candle_any": d1["minute_start"].min() if len(d1) else pd.NaT,
            "first_candle_traded": d1.loc[d1["volume"] > 0, "minute_start"].min() if len(d1) else pd.NaT,
            "window_minutes": win_minutes,
            "candles_returned": len(c1),
            "candles_vol_gt0": len(traded),
            "candles_empty": win_minutes - len(traded),
            "pct_traded": 100 * len(traded) / win_minutes if win_minutes else float("nan"),
            "traded_with_bid_and_ask": len(both),
            "volume_in_window": float(c1["volume"].sum()) if len(c1) else 0.0,
        })
        if i % 10 == 0:
            print(f"[{i}/{len(markets)}] {time.time()-t0:.0f}s  calls={k.n_calls} 429={k.n_429}", flush=True)

    am = pd.DataFrame(arows)
    am.to_csv(PROC / "audit_markets.csv", index=False)

    # agregasi per event: menit di mana MINIMAL SATU market ada transaksi
    erows = []
    for _, e in done.iterrows():
        tick = markets.loc[markets.event_ticker == e["event_ticker"], "ticker"].tolist()
        strike = e["strike_dt"].to_pydatetime()
        w_end_all = strike
        mins, per_week = set(), {}
        for t in tick:
            c = pd.read_parquet(M1 / f"{t}.parquet")
            if len(c):
                mins |= set(c.loc[c["volume"] > 0, "end_ts"])
        win = WINDOW_DAYS * 1440
        s_end = ts(strike)
        wk = [0, 0, 0, 0]
        for t_ in mins:
            idx = min(int((s_end - t_) // (7 * 86400)), 3)
            if 0 <= (s_end - t_) <= WINDOW_DAYS * 86400:
                wk[idx] += 1
        sub = am[am.event_ticker == e["event_ticker"]]
        erows.append({
            "event_ticker": e["event_ticker"], "meeting_utc": e["strike_date"],
            "n_markets": len(sub),
            "first_candle_traded_min": sub["first_candle_traded"].min(),
            "first_candle_any_min": sub["first_candle_any"].min(),
            "window_minutes": win,
            "minutes_any_trade": len(mins),
            "pct_any_trade": 100 * len(mins) / win,
            "pct_last7d": 100 * wk[0] / (7 * 1440),
            "pct_d8_14": 100 * wk[1] / (7 * 1440),
            "pct_d15_21": 100 * wk[2] / (7 * 1440),
            "pct_d22_28": 100 * wk[3] / (7 * 1440),
            "median_market_pct_traded": sub["pct_traded"].median(),
            "max_market_pct_traded": sub["pct_traded"].max(),
            "volume_in_window": sub["volume_in_window"].sum(),
            "min_bid_ask_share": (sub["traded_with_bid_and_ask"].sum() / max(sub["candles_vol_gt0"].sum(), 1)),
        })
    ae = pd.DataFrame(erows)
    ae.to_csv(PROC / "audit_events.csv", index=False)

    out = {"access": access, "binance": binance_check(), "api_calls": k.n_calls, "http_429": k.n_429}
    (RAW / "access_check.json").write_text(json.dumps(out, indent=2, default=str))
    print("selesai. panggilan API:", k.n_calls, " 429:", k.n_429)


if __name__ == "__main__":
    sys.exit(main())
