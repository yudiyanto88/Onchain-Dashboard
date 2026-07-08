# Test 3 Kondisi (Threshold K2) sebagai Trigger Tambahan Bull Dip Z4

Script: `analyze_bull_dip_z4_k2_trigger.py`. Dikerjakan 2026-07-05.

**Konteks:** Lanjutan dari [[project_bull_dip_z4_conditions]] — kali ini
threshold disesuaikan ke konteks Z4/Z5 (bukan threshold K5 yang dirancang
untuk Z2/Z3 bear recovery):
- F&G ≤ 35 (vs ≤50 sebelumnya)
- STH Loss ≥ 70% (vs ≥60% sebelumnya)
- min(aSOPR, STH-SOPR) ≤ 0.98 (sama)

Window: 14 episode bull dip ke Z4 yang sama (7 di 2019-2020, 7 di 2023-2024).

## Tabel per episode

| Period | Start-End | Days | Drop% | F&G≤35 | STH Loss≥70% | SOPR≤0.98 | N/3 | Resolusi |
|---|---|---|---|---|---|---|---|---|
| 2019-20 | 06-27→06-27 | 1 | -12.8% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2019-20 | 06-30→07-02 | 3 | -11.6% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2019-20 | 07-04→07-07 | 4 | -8.2% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2019-20 | 07-11→07-13 | 3 | -6.1% | **YA** | TIDAK | TIDAK | 1 | **BREAKDOWN** |
| 2019-20 | 11-26→11-28 | 3 | -8.4% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2019-20 | 12-08→12-08 | 1 | -4.5% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2019-20 | 12-10→12-11 | 2 | -2.8% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2023-24 | 03-19→03-19 | 1 | -8.4% | TIDAK | TIDAK | **YA** | 1 | RECOVERED |
| 2023-24 | 03-22→03-23 | 2 | -2.6% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2023-24 | 04-02→04-03 | 2 | -6.0% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2023-24 | 04-12→04-30 | 19 | -13.4% | TIDAK | TIDAK | **YA** | 1 | **BREAKDOWN** |
| 2023-24 | 05-21→06-23 | 34 | -11.5% | TIDAK | **YA** | TIDAK | 1 | **BREAKDOWN** |
| 2023-24 | 12-22→12-23 | 2 | -2.5% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2023-24 | 12-26→01-02 | 8 | -6.8% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |

## Persentase per kondisi (n=14, threshold K2)

| Kondisi | Terpenuhi | % |
|---|---|---|
| F&G ≤ 35 | 1/14 | 7% |
| STH Loss ≥ 70% | 1/14 | 7% |
| min(aSOPR,STH-SOPR) ≤ 0.98 | 2/14 | 14% |

Distribusi: 0/3 = 10 episode (71%), 1/3 = 4 episode (29%), 2/3 = 0%, 3/3 = 0%.
(Threshold lebih ketat → tidak ada lagi episode 2/3, dibanding versi K5
sebelumnya yang punya 1 episode 2/3.)

## Breakdown resolusi per jumlah kondisi terpenuhi

| N kondisi | #Episode | #RECOVERED | #BREAKDOWN | % RECOVERED |
|---|---|---|---|---|
| 0 | 10 | 10 | 0 | **100%** |
| 1 | 4 | 1 | 3 | **25%** |

## Jawaban ke pertanyaan inti

**1. Apakah episode ≥1 kondisi masih konsisten berakhir BREAKDOWN?**
YA — malah LEBIH konsisten dari analisis sebelumnya. Dengan threshold yang
lebih ketat (K2), 3 dari 4 episode (75%) yang memenuhi kondisi berakhir
BREAKDOWN. Pola dari [[project_bull_dip_z4_conditions]] (kondisi fire →
cenderung breakdown) **menguat**, bukan melemah, di threshold yang lebih ketat.

**2. Apakah ada episode RECOVERED yang juga memenuhi kondisi (genuine buy
signal candidate)?**
Ada **1 dari 14** — episode 2024-03-19 (RECOVERED, SOPR min 0.964). Tapi ini
episode yang sama yang sudah muncul di analisis threshold K5 sebelumnya (SOPR
≤0.98 tidak berubah antara versi K5 dan K2), jadi bukan temuan baru dari
pengetatan threshold F&G/STH Loss.

**3. Hit rate: dari episode ≥1 kondisi, berapa yang RECOVERED?**
**1/4 = 25%.** Ini adalah kebalikan dari yang diinginkan untuk sinyal BUY —
kalau kondisi ini dipakai sebagai trigger K2 (asumsi "kondisi fire = beli"),
75% dari waktu justru salah arah (breakdown, bukan recovery).

## Kesimpulan

**Ketiga kondisi ini TIDAK layak jadi genuine buy signal K2**, bahkan dengan
threshold yang sudah disesuaikan lebih ketat untuk konteks Z4/Z5. Alih-alih
jadi filter yang menyaring bull dip yang "akan recovery", pola yang muncul
justru terbalik — kondisi ini fire justru saat dip berisiko breakdown, BUKAN
saat dip akan bounce balik ke Z5.

**Fungsi yang tepat: WARNING FLAG, bukan BUY trigger.** Kalau salah satu dari
3 kondisi ini fire selama bull dip di Z4, itu sinyal untuk WASPADA (kemungkinan
dip lebih dalam dari bull dip normal, cek BT1/S2), bukan sinyal untuk deploy
capital tambahan. Base rate tanpa kondisi (0/3) justru O% breakdown (100%
recovered) — jadi "tidak ada kondisi fire" adalah kondisi paling aman untuk
asumsi bull dip normal, sementara "kondisi fire" adalah alasan untuk lebih
hati-hati, bukan lebih agresif.

**Catatan sample:** n=14 episode, cuma 4 yang punya ≥1 kondisi (3 breakdown,
1 recovered) — masih sangat kecil. Kesimpulan "warning flag bukan buy signal"
cukup jelas arahnya, tapi presisi angka (75% breakdown rate) perlu divalidasi
ulang kalau ada data cycle tambahan (2025+).
