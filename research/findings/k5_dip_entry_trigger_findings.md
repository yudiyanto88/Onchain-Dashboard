# K5 Dip-Entry Trigger Validation — Findings

Script: `analyze_k5_dip_entry_trigger.py`. Data per 2026-07-05 snapshot.

## Zona window yang dipakai
- Z2 start = STH RP cross up RP, Price < AVIV Mean
- Z3 end = price sustained ≥3 hari di atas AVIV Upper (0.5σ, dihitung dari `price_at_aviv_mean` + 0.5×(`price_at_aviv_plus_1_sigma` − `price_at_aviv_mean`), konsisten dengan `analyze_k3_exit_a.py`)

| Episode | Z2 start | Z3 end | Durasi |
|---|---|---|---|
| 2018-2019 recovery | 2019-05-07 | 2019-07-08 | 63 hari |
| 2022-2023 recovery | 2023-03-01 | 2024-02-27 | 364 hari |

(Catatan: batas Z3-end sedikit berbeda dari `verify_z3_definition.py`/`z3.md` versi lama karena data on-chain sudah di-refresh berkali-kali sejak analisis itu — tidak mengubah kesimpulan di bawah.)

## Base case: STH in Loss ≥ 50%, SOPR konfirmasi ≤ 0.98

**2018-2019: 0/6 pullback trigger fire.** STH in Loss max yang tercapai hanya 40.5% (pullback #4, 2019-06-09) — STH cohort tidak pernah mayoritas underwater selama window Z2/Z3 di cycle ini. Recovery 2019 terlalu cepat (V-shape) untuk kondisi ini pernah terpenuhi.

**2022-2023: 2 sinyal bersih dari 13 pullback.**

| Pullback | STH Loss max | SOPR min saat konfirmasi | Entry | Recover ke entry | Gain 30d | Gain 60d | Gain 90d | Regresi Z1? |
|---|---|---|---|---|---|---|---|---|
| Mar 2023 (trigger 03-09, confirm 03-09) | 51.4% | 0.953 | $20,376 | 2 hari | +37.2% | +36.1% | +30.6% | Tidak |
| Aug 2023 (trigger 08-04, confirm 08-17) | 97.8% | 0.965 | $26,668 | 12 hari | -0.3% | +6.9% | +42.1% | Tidak |

2 pullback lain trigger STH≤50% tapi SOPR **tidak pernah** konfirmasi ≤0.98 dalam window pullback itu:
- Mei-Jun 2023: trigger di $27,737 (STH loss 76.3%), harga masih turun lagi -9.3% ke $25,173 sebelum akhirnya rally besar → filter kombinasi menghindarkan entry prematur, tapi juga jadi *missed opportunity* kalau dilihat dari hasil akhir.
- Jan 2024: trigger di $41,803 (STH loss 60.6%), harga turun lagi -5.4% ke $39,564 lalu rally pasca-ETF.

**False signal check:**
- 4a (STH≤50% confirmed entry lalu regresi ke Z1): 0/2 — bersih.
- 4b (SOPR≤0.98 fire di luar konteks pullback, saat harga naik): 2 kejadian satu-hari (2023-03-30, 2023-07-06) — kalau SOPR dipakai sendirian tanpa syarat STH≤50%+pullback, ini jadi false signal. Kombinasi 2 kondisi berhasil menyaring keduanya.

## Sensitivity grid (STH Loss 40/50/60% × SOPR 0.95/0.98/1.00)

- **2019**: hampir semua kombinasi 0 confirm, kecuali SOPR≤1.00 (trivial — hampir selalu benar, bukan konfirmasi berarti).
- **2023**: SOPR≤0.98 & STH≥50% = kombinasi paling bersih (2/4 confirm, 0 false regress, avg gain30d +18.5%). SOPR≤1.00 hampir tidak menyaring apapun (confirm≈trigger count). SOPR≤0.95 terlalu ketat — sering 0 confirm atau confirm tunggal dengan hasil noisy (sampel kecil, -11% avg pada 40%/0.95).

## Kesimpulan

Kombinasi STH in Loss ≥50% + min(aSOPR,STH-SOPR) ≤0.98 **valid mengarah ke entry yang profitable di cycle 2022-2023** (2/2 confirmed entries positif di 90 hari, 0 regresi ke Z1, dan berhasil menyaring 2 false SOPR spike). Tapi **sama sekali tidak fire di cycle 2018-2019** — sinyal ini kondisional pada tipe recovery (butuh STH cohort benar-benar mayoritas underwater saat pullback, terjadi di recovery yang choppy/panjang seperti 2023, bukan di V-shape cepat seperti 2019).

Sample size sangat tipis — **n=2 confirmed signal** di seluruh histori data yang tersedia. Tidak cukup untuk high-confidence standalone gate. Sesuai Hard Constraint #3 (multi-indicator confirmation, bukan single signal) — perlakukan ini sebagai satu kandidat trigger dalam N-of-M framework (BB1/PD1), bukan syarat tunggal untuk deploy loan.
