# aSOPR Crossover — Trigger Candidates

---

## Metodologi Backtest

- **Data:** `data_momentum_events.csv` — kolom `date`, `btc_price`, `asopr`
- **Periode:** 2013–2025 (data historis lengkap)
- **Major events:** 11 bottoms, 10 peaks (algorithmic detection: window=90d, min drawdown=28%, min runup=65%, merge=60d)
- **Lead time:** hari antara crossover dan major event — makin besar = makin awal
- **Precision:** % crossover yang diikuti major event dalam 120 hari
- **False+/yr:** rata-rata false positive per tahun (crossover tanpa major event dalam 120 hari)

---

## Top 3 Pairs

### UP Crossover — Accumulate / Buy

| Pair | Avg Lead | Med Lead | Hit Rate @60d | Detection | Precision | False+/yr |
|------|----------|----------|--------------|-----------|-----------|-----------|
| **EMA90/SMA80** | 62d | 47d | 71% | 11/11 | 29.8% | 2.5 |
| **EMA55/SMA35** | 64d | 65d | 62% | 11/11 | 27.3% | 3.7 |
| **EMA60/SMA30** | 42d | 25d | 63% | 11/11 | 31.7% | 3.2 |

### DOWN Crossover — Distribute / Sell

| Pair | Avg Lead | Med Lead | Hit Rate @60d | Detection | Precision | False+/yr |
|------|----------|----------|--------------|-----------|-----------|-----------|
| **EMA90/SMA80** | 60d | 50d | 67% | 9/10 | 22.4% | 2.9 |
| **EMA60/SMA30** | 45d | 23d | 61% | 9/10 | 25.9% | 3.1 |
| **EMA55/SMA35** | 37d | 41d | 58% | 9/10 | 23.8% | 3.7 |

---

## Karakteristik Tiap Pair

### EMA90/SMA80 — Cycle-Level Signal
- MA paling lambat → filter noise otomatis
- Lead time hampir sama untuk UP (62d) dan DOWN (60d) → simetris
- False positive paling sedikit (~2.5–2.9/yr)
- Validated secara eksternal oleh Alphactal (SOPR Trend Signal chart)
- **Cocok sebagai:** sinyal awal yang "berat" — perlu konfirmasi dari metrik lain untuk aksi

### EMA55/SMA35 — Best Early Warning untuk Bottom
- Avg lead UP terpanjang (64d) — fires paling awal untuk cycle bottom
- Untuk DOWN lead lebih pendek (37d) → lebih dekat ke actual peak
- Artinya: untuk strategi S1/S2, EMA55/SMA35 DOWN bisa dijadikan Stage 2 (aksi agresif)
- **Cocok sebagai:** BB1 early trigger + S2 late/aggressive trigger

### EMA60/SMA30 — Best Precision
- Precision terbaik untuk keduanya: 31.7% UP, 25.9% DOWN
- Lead time UP = 42d (lebih dekat ke bottom) → konfirmasi setelah EMA90/EMA55 sudah fired
- **Cocok sebagai:** konfirmasi sekunder — kalau EMA90 sudah fire dan EMA60 ikut fire, confidence naik

---

## Threshold Filter yang Disarankan

Signal crossover hanya dihitung valid jika level EMA memenuhi kondisi:

| Direction | Threshold | Logic |
|-----------|-----------|-------|
| UP (buy) | EMA ≤ 0.99–1.00 | aSOPR ditekan — holder jual rugi/impas |
| DOWN (sell) | EMA ≥ 1.01–1.015 | aSOPR elevated — holder jual untung berlebihan |

> EMA90/SMA80: gunakan 1.015 / 0.99 (strict)  
> EMA55/SMA35 & EMA60/SMA30: bisa pakai 1.01 / 1.00 (sedikit lebih longgar)

---

## Sequential Firing — Behavior di Cycle Events

Untuk bottom :
```
EMA55/SMA35 UP  → avg ~64d sebelum bottom  (earliest)
EMA90/SMA80 UP  → avg ~62d sebelum bottom  (hampir bersamaan dengan EMA55)
EMA60/SMA30 UP  → avg ~42d sebelum bottom  (konfirmasi, lebih dekat ke event)
```

Untuk peak :
```
EMA90/SMA80 DOWN → avg ~60d sebelum peak   (earliest warning)
EMA60/SMA30 DOWN → avg ~45d sebelum peak   (mid timing)
EMA55/SMA35 DOWN → avg ~37d sebelum peak   (Stage 2 — closest to peak)
```

Ketika 2–3 pair fire dalam window 60–90 hari → multiple trigger count naik 

