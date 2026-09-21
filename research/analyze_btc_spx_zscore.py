# -*- coding: utf-8 -*-
"""
Backtest BTC/SPX (dan BTC/XAU) Ratio Z-Score sebagai sinyal (2026-09-21).

Pemakaian: python research/analyze_btc_spx_zscore.py [spx|xau|ndx]   (default spx)
XAU = emas, dari Yahoo GC=F (futures bulan terdekat, pendekatan harga spot). NDX = Nasdaq 100 (^NDX).

Setelan (pilihan praktis yang disepakati):
  - rasio = log(BTC / S&P 500)
  - Z = (rasio - SMA_w) / STD_w, rata-rata & SD dari jendela yang sama
  - S&P akhir pekan / libur = harga penutupan terakhir (ffill)
  - BTC dari data_master_all_metrics.csv (ChartInspect), S&P dari Yahoo (^GSPC)
  - tanpa penghalusan tambahan
Jendela diuji: 365, 730, 1460 hari.

Sinyal = episode. Sisi beli: Z turun menembus ambang (mis. -2). Episode dianggap
selesai saat Z kembali ke atas 0; baru setelah itu sinyal berikutnya boleh
muncul. Sisi jual (peringatan): cermin, Z naik menembus ambang positif.

Untuk tiap sinyal diukur dari harga BTC hari sinyal:
  - return 90 / 180 / 365 hari ke depan
  - penurunan terdalam (max drawdown) dalam 180 hari ke depan  -> risiko leverage
  - kenaikan tertinggi dalam 180 hari ke depan (untuk sisi jual: risiko keluar terlalu cepat)
Pembanding (baseline) = return rata-rata semua hari di periode yang sama.

Periode uji dibuat sama untuk semua jendela: mulai hari pertama Z jendela 4 tahun
terdefinisi, supaya perbandingan adil.
"""
import json
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "research" / "findings"
BENCHES = {"spx": ("%5EGSPC", "S&P 500"), "xau": ("GC%3DF", "Emas (XAU)"), "ndx": ("%5ENDX", "Nasdaq 100")}
BENCH = sys.argv[1] if len(sys.argv) > 1 else "spx"
SYMBOL, BENCH_NAME = BENCHES[BENCH]
BENCH_CSV = OUT / f"_{BENCH}_yahoo.csv"
WINDOWS = [365, 730, 1460]
BUY_TH = [-1.0, -1.5, -2.0, -2.5]
SELL_TH = [1.5, 2.0, 2.5]
HORIZONS = [90, 180, 365]
DIV_TH = [-1.5, -2.0, -2.5]  # syarat low pertama
DIV_PIVOT = [14, 30, 60]  # lebar pivot low (hari)


def load_bench():
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}"
           "?period1=1262304000&period2=4102444800&interval=1d")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        d = json.load(urllib.request.urlopen(req, timeout=30))["chart"]["result"][0]
        s = pd.Series(d["indicators"]["quote"][0]["close"],
                      index=pd.to_datetime(d["timestamp"], unit="s").normalize(), name="bench").dropna()
        s.rename_axis("date").to_csv(BENCH_CSV)
    except Exception as e:  # offline: pakai salinan terakhir
        print(f"Yahoo gagal ({e}), pakai {BENCH_CSV.name}")
    return pd.read_csv(BENCH_CSV, parse_dates=["date"]).set_index("date").bench


btc = pd.read_csv(ROOT / "data_master_all_metrics.csv", usecols=["date", "btc_price"],
                  parse_dates=["date"]).set_index("date").btc_price
bench = load_bench()
df = pd.concat([btc, bench], axis=1).loc[bench.index[0]:]
df["bench"] = df.bench.ffill()
df = df.dropna()
ratio = np.log(df.btc_price / df.bench)
for w in WINDOWS:
    df[f"z{w}"] = (ratio - ratio.rolling(w).mean()) / ratio.rolling(w).std()

price = df.btc_price
fwd = {h: price.shift(-h) / price - 1 for h in HORIZONS}
# min/max harga dalam 180 hari ke depan (tidak termasuk hari ini)
fut_min = price[::-1].rolling(180, min_periods=1).min()[::-1].shift(-1)
fut_max = price[::-1].rolling(180, min_periods=1).max()[::-1].shift(-1)
mdd180 = fut_min / price - 1
mup180 = fut_max / price - 1

start = df[f"z{max(WINDOWS)}"].first_valid_index()
test = df.loc[start:]
base = {h: fwd[h].loc[start:].dropna() for h in HORIZONS}


def episodes(z, th):
    """Hari pertama Z menembus ambang; re-arm setelah Z kembali melewati 0."""
    below = th < 0
    armed, out = True, []
    for t, v in z.dropna().items():
        if armed and (v <= th if below else v >= th):
            out.append(t)
            armed = False
        elif not armed and (v > 0 if below else v < 0):
            armed = True
    return out


def divergences(z, th, n):
    """Bullish divergence di dalam satu episode Z negatif.

    Pivot low Z = titik terendah dalam +-n hari (baru diketahui n hari kemudian).
    Low pertama harus <= th. Low berikutnya: Z lebih tinggi (higher low) tapi harga
    BTC lebih rendah (lower low) -> sinyal, tanggal = pivot kedua + n hari (tanpa
    melihat masa depan). Satu sinyal per episode; episode reset saat Z > 0.
    """
    v = z.to_numpy()
    idx = z.index
    px = price.reindex(idx).to_numpy()
    out, anchor, fired, last = [], None, False, 0
    for i in range(n, len(v) - n):
        if np.isnan(v[i - n:i + n + 1]).any() or v[i] != v[i - n:i + n + 1].min():
            continue
        if (v[last:i] > 0).any():  # sempat balik ke atas 0 -> episode baru
            anchor, fired = None, False
        last = i
        if anchor is None:
            if v[i] <= th:
                anchor = i
        elif v[i] > v[anchor] and px[i] < px[anchor]:
            if not fired:
                out.append((idx[i + n], idx[anchor], idx[i]))
                fired = True
        elif v[i] < v[anchor]:
            anchor = i
    return out


def stats(ev):
    r = {"n": len(ev)}
    for h in HORIZONS:
        x = fwd[h].reindex(ev).dropna()
        r[f"n_{h}d"] = len(x)
        r[f"median_{h}d"] = x.median()
        r[f"hit_{h}d"] = (x > 0).mean() if len(x) else np.nan  # % sinyal yang harganya naik
    r["median_mdd180"] = mdd180.reindex(ev).median()
    r["worst_mdd180"] = mdd180.reindex(ev).min()
    r["median_mup180"] = mup180.reindex(ev).median()
    return r


def detail(t, extra):
    return {**extra, "date": t.date(), "btc_price": round(price[t]),
            **{f"ret_{h}d": round(fwd[h][t], 3) if pd.notna(fwd[h][t]) else None for h in HORIZONS},
            "mdd_180d": round(mdd180[t], 3), "mup_180d": round(mup180[t], 3)}


rows, details = [], []
for w in WINDOWS:
    z = test[f"z{w}"]
    for th in BUY_TH + SELL_TH:
        ev = episodes(z, th)
        rows.append({"window": w, "threshold": th, "side": "beli" if th < 0 else "jual", **stats(ev)})
        details += [detail(t, {"window": w, "threshold": th, "z": round(z[t], 2)}) for t in ev]

# bullish divergence: pivot dicari di seluruh data, sinyal dihitung mulai periode uji
div_rows, div_details = [], []
for w in WINDOWS:
    for n in DIV_PIVOT:
        for th in DIV_TH:
            sig = [x for x in divergences(df[f"z{w}"], th, n) if x[0] >= start]
            ev = [x[0] for x in sig]
            div_rows.append({"window": w, "pivot_n": n, "first_low": th, **stats(ev)})
            div_details += [detail(t, {"window": w, "pivot_n": n, "first_low": th, "low1": a.date(),
                                       "z_low1": round(df[f"z{w}"][a], 2), "px_low1": round(price[a]),
                                       "low2": b.date(), "z_low2": round(df[f"z{w}"][b], 2),
                                       "px_low2": round(price[b])}) for t, a, b in sig]

res = pd.DataFrame(rows)
det = pd.DataFrame(details)
res.to_csv(OUT / f"_btc_{BENCH}_zscore_summary.csv", index=False)
det.to_csv(OUT / f"_btc_{BENCH}_zscore_signals.csv", index=False)
dres = pd.DataFrame(div_rows)
ddet = pd.DataFrame(div_details)
dres.to_csv(OUT / f"_btc_{BENCH}_zscore_divergence_summary.csv", index=False)
ddet.to_csv(OUT / f"_btc_{BENCH}_zscore_divergence_signals.csv", index=False)

pd.set_option("display.width", 250, "display.max_columns", 30, "display.float_format", "{:.2f}".format)
print(f"Periode uji: {start.date()} s/d {test.index[-1].date()}")
print("Baseline semua hari: " + ", ".join(
    f"{h}d median {base[h].median():+.2f}, naik {(base[h] > 0).mean():.0%}" for h in HORIZONS))
print("Baseline MDD180 median", round(mdd180.loc[start:].median(), 3))
print(res.to_string(index=False))
print("\nZ terakhir:", {w: round(df[f'z{w}'].iloc[-1], 2) for w in WINDOWS})
print("\nSinyal detail:")
print(det.to_string(index=False))
print("\nBullish divergence:")
print(dres.to_string(index=False))
print(ddet.to_string(index=False))


def plot():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    names = {365: "1 tahun", 730: "2 tahun", 1460: "4 tahun"}
    fig, axes = plt.subplots(3, 1, figsize=(16, 18), facecolor="#0b0b0d")
    for ax, w in zip(axes, WINDOWS):
        z = df[f"z{w}"].loc["2013-06":].dropna()
        p = df.loc[z.index]
        ax.set_facecolor("#0b0b0d")
        ax.fill_between(z.index, 0, z, where=z >= 0, color="#e84545", lw=0)
        ax.fill_between(z.index, 0, z, where=z < 0, color="#2ecc71", lw=0)
        for y, c in [(2.5, "#e84545"), (-2.5, "#2ecc71"), (-2, "#2ecc71"), (0, "#888")]:
            ax.axhline(y, color=c, ls=":", lw=1)
        ax.set_ylim(-4, 5.5)
        ax.tick_params(colors="#ccc")
        ax.grid(color="#222", lw=0.5)
        ax.set_ylabel("Z-Score", color="#ccc")
        a2 = ax.twinx()
        a2.plot(p.index, p.btc_price, color="white", lw=1.2)
        a2.set_yscale("log")
        a2.tick_params(colors="#ccc")
        ev = episodes(df[f"z{w}"].loc[start:], -2.0)
        a2.scatter(ev, p.btc_price.reindex(ev), s=140, color="#facc15", edgecolor="black", zorder=5)
        for t in ev:
            a2.annotate(t.strftime("%b %Y"), (t, p.btc_price[t]), xytext=(0, -22), textcoords="offset points",
                        color="#facc15", ha="center", fontsize=10)
        a3 = ax.twinx()
        a3.plot(p.index, p.bench, color="#3b82f6", lw=1.2)
        a3.set_yscale("log")
        a3.axis("off")
        ax.set_title(f"BTC/{BENCH.upper()} Ratio Z-Score — jendela {names[w]}  |  sekarang {z.iloc[-1]:+.2f}"
                     f"  |  sinyal beli Z ≤ −2: {len(ev)}×", color="white", fontsize=15, weight="bold")
        for s in [*ax.spines.values(), *a2.spines.values()]:
            s.set_color("#333")
    fig.text(0.5, 0.003, f"Putih = harga BTC  ·  Biru = {BENCH_NAME}  ·  Merah = BTC lebih kuat  ·  Hijau = BTC lebih lemah"
             f"  ·  Titik kuning = sinyal beli Z ≤ −2 (dihitung mulai {start.year})", color="#ccc", ha="center", fontsize=12)
    fig.tight_layout(rect=(0, 0.015, 1, 1))
    fig.savefig(ROOT / "research" / f"btc_{BENCH}_zscore_3_jendela.png", dpi=85, facecolor=fig.get_facecolor())



def plot_divergence():
    """Chart jendela 1 & 2 tahun dengan sinyal bullish divergence (pivot 30, low pertama <= -2)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 1, figsize=(16, 12), facecolor="#0b0b0d")
    for ax, w, label in zip(axes, [365, 730], ["1 tahun", "2 tahun"]):
        z = df[f"z{w}"].loc["2013-06":].dropna()
        p = df.loc[z.index]
        ax.set_facecolor("#0b0b0d")
        ax.fill_between(z.index, 0, z, where=z >= 0, color="#e84545", lw=0, alpha=.55)
        ax.fill_between(z.index, 0, z, where=z < 0, color="#2ecc71", lw=0, alpha=.55)
        for y, c in [(-2, "#2ecc71"), (0, "#888")]:
            ax.axhline(y, color=c, ls=":", lw=1)
        ax.set_ylim(-4.5, 5)
        ax.tick_params(colors="#ccc")
        ax.grid(color="#222", lw=.5)
        ax.set_ylabel("Z-Score", color="#ccc")
        a2 = ax.twinx()
        a2.plot(p.index, p.btc_price, color="white", lw=1.1)
        a2.set_yscale("log")
        a2.tick_params(colors="#ccc")
        for t in episodes(df[f"z{w}"].loc[start:], -2.0):
            a2.scatter(t, p.btc_price[t], s=90, color="#9ca3af", edgecolor="black", zorder=5)
        sig = [x for x in divergences(df[f"z{w}"], -2.0, 30) if x[0] >= start]
        for t, lo1, lo2 in sig:
            ax.plot([lo1, lo2], [z[lo1], z[lo2]], color="#facc15", lw=2.5)
            a2.plot([lo1, lo2], [p.btc_price[lo1], p.btc_price[lo2]], color="#facc15", lw=2.5, ls="--")
            a2.scatter(t, p.btc_price[t], s=220, marker="*", color="#facc15", edgecolor="black", zorder=6)
            a2.annotate(t.strftime("%b %Y"), (t, p.btc_price[t]), xytext=(0, 16), textcoords="offset points",
                        color="#facc15", ha="center", fontsize=11, weight="bold")
        ax.set_title(f"BTC/{BENCH.upper()} Z-Score {label} + bullish divergence  |  sinyal divergence: {len(sig)}×"
                     f"  |  titik abu = sinyal Z ≤ −2 biasa", color="white", fontsize=14, weight="bold")
        for s_ in [*ax.spines.values(), *a2.spines.values()]:
            s_.set_color("#333")
    fig.text(0.5, 0.004, "Bintang kuning = sinyal divergence  ·  garis kuning bawah = Z low lebih tinggi  ·  putus-putus = "
             "harga BTC low lebih rendah  ·  pivot 30 hari, low pertama Z ≤ −2", color="#ccc", ha="center", fontsize=12)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(ROOT / "research" / f"btc_{BENCH}_zscore_divergence.png", dpi=85, facecolor=fig.get_facecolor())


plot()
plot_divergence()

if __name__ == "__main__":
    # self-check logika episode: re-arm hanya setelah lewat 0
    zz = pd.Series([0.5, -2.1, -2.5, -1.0, -2.2, 0.1, -2.3],
                   index=pd.date_range("2020-01-01", periods=7))
    assert episodes(zz, -2.0) == [zz.index[1], zz.index[6]]
    assert episodes(-zz, 2.0) == [zz.index[1], zz.index[6]]
