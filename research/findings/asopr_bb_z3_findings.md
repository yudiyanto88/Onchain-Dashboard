# aSOPR Bollinger Band Upper — Signal Validation di Z3 (2019 & 2023-2024)

Script: `analyze_asopr_bb_z3.py`. Dikerjakan 2026-07-05.

**Z3 def dipakai:** RP (Realized Price) <= Price <= AVIV Mean. Dihitung langsung
dari data historis (bukan hardcode tanggal) — RP selalu di bawah AVIV Mean
sepanjang histori jadi definisi "antara" aman pakai `rp <= price <= aviv_mean`.

**BB:** rolling MA + rolling std dihitung dari full historical aSOPR (kontinu),
lalu signal dicek hanya pada hari yang termasuk window Z3. Upper Band = MA + mult*std.
Signal = aSOPR menyentuh/melewati upper band; hari-hari konsekutif digabung jadi
1 signal (tanggal signal = hari pertama nyentuh).

## Z3 windows ditemukan

**2019 — DIFILTER ke leg awal recovery saja (1 window, 79 hari):**
- 2019-04-02 → 2019-06-19 (harga naik dari ~$4.9k bottom)
- (window Agu-Des 2019 DIBUANG — itu fase harga jatuh balik ke Z3 setelah peak
  $13.8k Juni, bukan recovery)

**2023-2024 (10 window terpakai, total 465 hari, tidak difilter):**
- 2023-01-13 → 2023-12-04 (window utama, 326 hari)
- + 9 window lain lebih pendek tersebar Des 2023 - Okt 2024

## Tabel hasil 6 kombinasi (2019 = leg awal recovery only)

| MA | Std | # Signal | # Koreksi ≥5% | # False | Hit Rate |
|---|---|---|---|---|---|
| 14 | 1.5 | 41 | 12 | 29 | 29% |
| 14 | 2.0 | 20 | 4 | 16 | 20% |
| 20 | 1.5 | 38 | 11 | 27 | 29% |
| 20 | 2.0 | 20 | 6 | 14 | 30% |
| 30 | 1.5 | 32 | 9 | 23 | 28% |
| 30 | 2.0 | 23 | 6 | 17 | 26% |

(Hit rate = koreksi≥5% / total signal yang punya data lengkap 14 hari ke depan)

**Perubahan vs versi sebelumnya (2019 termasuk fase decline Agu-Des):**
Membuang window Agu-Des 2019 menghapus 3-4 signal per kombinasi (termasuk
2019-11-13, sinyal koreksi terbesar -19.6%, dan beberapa sinyal Des 2019 yang
juga corrected). Hasilnya hit rate turun sedikit di semua kombinasi (mis.
MA14/Std1.5: 32%→29%; MA14/Std2.0: 28%→20%) — artinya sebagian sinyal "bagus"
di versi awal justru berasal dari fase decline yang sudah dibuang, bukan dari
leg recovery aslinya.

**Sisa signal di leg awal recovery 2019** (2019-04-02→06-19) konsisten di
semua kombinasi: 2019-05-13 dan 2019-05-29 selalu koreksi ≥5% (drop -6.9% dan
-11.7%), sementara 2019-04-02, 2019-04-19, 2019-05-11 tidak pernah koreksi
berarti. Dari 4-6 signal per kombinasi di window ini, hanya 1-2 yang valid —
hit rate lokal 2019 recovery-only sekitar 17-33%, sama rendahnya dengan
gabungan.

## Observasi

1. **Std multiplier lebih berpengaruh dari MA period.** Menaikkan std dari 1.5→2.0
   memangkas jumlah signal hampir separuh (41→20-23) tapi hit rate TIDAK naik
   proporsional (29%→20-30%, malah turun di beberapa kombinasi) — band yang
   lebih lebar menyaring signal marginal tapi tidak secara sistematis
   meningkatkan presisi.
2. **MA period (14/20/30) hampir tidak berpengaruh** pada hit rate di std=1.5
   (28-29%, jumlah signal 32-41). Bollinger aSOPR relatif tidak sensitif
   terhadap pilihan lookback dalam rentang ini.
3. **Hit rate keseluruhan rendah (~20-30%)**, malah sedikit lebih rendah
   setelah filter recovery-only — mayoritas signal (70-80%) TIDAK diikuti
   koreksi ≥5% dalam 14 hari. Sebagai standalone trigger, sinyal ini noisy,
   dan filter ke "recovery only" TIDAK memperbaiki presisi.
4. **Overlap dengan tanggal signifikan:** beberapa signal berimpit dengan
   pullback yang sudah diidentifikasi di [[project_k5_dip_entry_trigger]]
   (mis. 2023-05-03, 2023-05-07 — trigger StH+SOPR combo yang gagal align
   sebelumnya), tapi juga banyak fire di tengah uptrend (2023-10, 2023-11)
   yang TIDAK menghasilkan koreksi.
5. Signal terbesar di window recovery-only 2019 adalah 2019-05-29 (-11.7%);
   signal terbesar overall tetap 2024-08-23 (-15.8%, di 2023-2024 episode yang
   tidak difilter).

## Kesimpulan

aSOPR BB upper-touch selama Z3, dalam bentuk apa pun dari 6 kombinasi yang
dites — baik pakai seluruh window Z3 maupun difilter ke leg recovery murni —
**bukan sinyal yang bersih** (hit rate ~20-33%, false rate ~70-80%). Filter
ke "recovery only" tidak memperbaiki presisi, malah menurunkannya sedikit
karena membuang beberapa signal koreksi besar yang justru terjadi di fase
decline. Tidak direkomendasikan sebagai trigger standalone maupun kandidat
N-of-M tanpa kombinasi dengan indikator lain (STH Supply in Loss, SOPR level
absolut, supply in profit) untuk menyaring konteks. Sesuai Hard Constraint #3,
jangan dipakai sendirian untuk keputusan sizing/deploy.
