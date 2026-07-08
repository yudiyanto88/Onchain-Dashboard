# Jarak (Stretch) Harga dari STH RP selama Z2+Z3 — Cycle 2019 & 2023

Script: `analyze_price_stretch_sth_rp.py`. Dikerjakan 2026-07-05.

**Definisi:**
- Z2 mulai: STH RP cross ke atas RP (Realized Price)
- Z3 berakhir: Price cross ke atas AVIV Upper (0.5σ), bertahan ≥3 hari
- Stretch = (Price − STH_RP) / STH_RP × 100%
- Window detection direplikasi persis dari metodologi
  [[project_k5_dip_entry_trigger]] (`analyze_k5_dip_entry_trigger.py`)

## Window ditemukan

- **2019 CYCLE:** Z2 start 2019-05-07 → Z3 end 2019-07-08 (63 hari)
- **2023 CYCLE:** Z2 start 2023-03-01 → Z3 end 2024-02-27 (364 hari)

(Sama persis dengan window K5 dip-entry trigger sebelumnya — konsisten.)

## 1. Distribusi stretch harian

| Cycle | Min | P25 | Median | Mean | P75 | P90 | Max |
|---|---|---|---|---|---|---|---|
| 2019 (63 hari) | 23.4% | 37.2% | 42.2% | 43.0% | 50.9% | 56.2% | 73.9% |
| 2023 (364 hari) | -10.2% | 2.6% | 10.9% | 11.3% | 20.1% | 26.7% | 35.9% |
| **Gabungan (427 hari)** | -10.2% | 3.5% | 15.7% | 16.0% | 24.9% | 37.9% | 73.9% |

**Observasi kunci:** Stretch 2019 jauh lebih tinggi di semua persentil — bahkan
minimum-nya (23.4%) di atas median 2023 (10.9%). Ini konsisten dengan
[[project_k5_dip_entry_trigger]]: 2019 adalah recovery V-shape cepat, harga
meninggalkan STH RP jauh di belakang sebelum STH cohort sempat mayoritas rugi.
2023 lebih choppy — stretch sering tipis bahkan sempat negatif (-10.2%, price
sempat balik di bawah STH RP meski masih dalam window Z2/Z3 broadly defined).

## 2. Stretch threshold vs koreksi ≥5% dalam 14 hari

| Cycle | Stretch ≥20% | Stretch ≥30% | Stretch ≥40% |
|---|---|---|---|
| 2019 | 27/63 hari (43%) | 27/53 hari (51%) | 24/38 hari (**63%**) |
| 2023 | 26/94 hari (28%) | 10/23 hari (43%) | 0 hari (tidak pernah tembus 40%) |
| **Gabungan** | 53/157 hari (34%) | 37/76 hari (49%) | 24/38 hari (63%) |

**Observasi kunci:** Hubungan monotonik yang jelas — makin tinggi stretch,
makin tinggi probabilitas koreksi ≥5% dalam 14 hari (2019: 43%→51%→63%; 2023:
28%→43%). Ini **jauh lebih bersih** dibanding hit rate aSOPR/STH-SOPR
Bollinger Band di Z3 yang cuma ~20-36% flat tanpa gradasi
([[project_asopr_bb_z3]]). Stretch dari STH RP tampak jadi indikator yang
lebih informatif untuk risiko koreksi jangka pendek.

## 3. Rata-rata stretch tertinggi (di local peak) sebelum tiap koreksi ≥5%

**2019 (6 koreksi):** rata-rata stretch di peak = **+62.1%**
- Semua 6 koreksi terjadi setelah stretch >50% (range +54.5% s/d +73.9%)

**2023 (13 koreksi):** rata-rata stretch di peak = **+24.8%**
- Range lebih lebar: +12.1% (Juli 2023, 3 koreksi berturutan dari peak yang
  sama) s/d +32.0% (April 2023, 4 koreksi)

**Gabungan (n=19):** rata-rata = **+36.6%**, median = **+32.0%**

**Observasi:** Threshold stretch yang memicu koreksi jauh berbeda antar cycle
— 2019 butuh stretch >50% dulu sebelum koreksi berarti terjadi, sementara di
2023 koreksi ≥5% sudah bisa muncul dari stretch serendah +12%. Ini menguatkan
kesimpulan bahwa **threshold stretch absolut TIDAK universal antar cycle** —
2019 adalah rally jauh lebih parah/cepat, jadi "peregangan" yang dianggap
ekstrem juga jauh lebih tinggi.

## Kesimpulan

1. Stretch dari STH RP adalah indikator yang **lebih diskriminatif** dibanding
   Bollinger Band SOPR — ada gradasi jelas: makin tinggi stretch, makin besar
   peluang koreksi ≥5% (34%→49%→63% gabungan kedua cycle).
2. **Threshold absolut tidak konsisten antar cycle** — 2019 butuh stretch jauh
   lebih tinggi (rata-rata peak +62%) dibanding 2023 (+25%) sebelum koreksi
   terjadi. Kalau mau dipakai sebagai trigger, pertimbangkan threshold
   relatif (mis. percentile historis cycle berjalan) bukan angka absolut
   tetap.
3. Stretch ≥40% adalah level dengan hit rate tertinggi (63%) di data yang
   tersedia, tapi n masih kecil (38 hari, hanya muncul di 2019) — 2023 bahkan
   tidak pernah mencapai level ini di window Z2/Z3, jadi generalisasinya
   terbatas ke rally jenis 2019.
4. Sesuai Hard Constraint #3, meskipun sinyal ini lebih bersih dari BB SOPR,
   tetap perlu dikombinasikan dengan indikator lain (bukan gate standalone)
   mengingat sample cuma 2 cycle.
