# Uji Hipotesis: Apparent Demand

- **Asal klaim:** video "Bitcoin Whales Are Accumulating Right Now" (On-Chain Mind, 2025-01-27) — lihat `video_whale-accumulation-2025_findings.md`
- **Tanggal uji:** 2026-07-11
- **Data:** `data_apparent_demand.csv` / master, full history 2010-07-17 s/d sekarang (5.839 hari)
- **Script:** `research/analyze_apparent_demand.py`

## Ringkasan Sederhana

Video bilang: demand Bitcoin masih tumbuh tapi laju pertumbuhannya melambat tajam, jadi butuh demand "rebound" dulu sebelum harga bisa rally lanjut. Setelah data apparent demand ditarik dan diuji ke seluruh histori sejak 2010 (bukan cuma periode video), klaim ini **tidak terbukti** sebagai pola general. Kebetulan cocok untuk momen spesifik yang dibahas video (Januari 2025), tapi di cycle-cycle lain (2011-2013, 2015-2017) justru harga rally besar meski demand-nya "melambat" dengan cara yang sama. Metrik apparent demand sendiri memang membawa informasi yang beda dari metrik yang sudah kita punya (bukan duplikat) — tapi informasi itu belum terbukti berguna buat prediksi. **Kesimpulan: apparent demand belum layak masuk framework sebagai sinyal.** Data-nya tetap disimpan (sudah di-pull permanen) kalau suatu saat mau dieksplorasi lagi dengan definisi event yang lebih ketat.

## Hipotesis & Hasil

| Hipotesis | Verdict | Ringkasan |
|-----------|---------|-----------|
| H1 — apparent demand negatif = bear, positif = bull (base rate) | **MIXED** | Arah kecenderungan benar, tapi overlap besar (48% hari "positif" tetap dalam drawdown ≥20%) dan tidak konsisten antar cycle |
| H2 — demand melambat tajam (masih positif) → forward return lebih lemah (klaim inti video) | **NOT-SUPPORTED** | n=26 event lintas 6 cycle, tapi hasil sangat rapuh: leave-one-cycle-out bikin median forward return 90 hari lompat dari 3% ke 84% tergantung cycle mana yang dikeluarkan. Mean vs median juga berlawanan arah |
| H3 — apparent demand cuma reskin dari metrik existing (net realized P/L, realized cap growth) | **NOT-SUPPORTED (redundansi ditolak)** | Korelasi cuma moderat (0.2–0.6), bahkan sempat negatif di bear 2022. Artinya metrik ini genuinely beda info — tapi beda info bukan berarti berguna (lihat H2) |

## Detail penting

- Kasus spesifik dari video (peak demand 7 Jan 2025, sinyal 6 Feb 2025) memang match klaim: forward return 30d -10.7%, 60d -18.0%, 90d hampir flat (+0.5%). Tapi ini cuma **1 dari 26 kejadian serupa** sepanjang sejarah — bukan pola, cuma kebetulan yang sama dengan cerita video.
- Dari 59 event "demand naik lalu turun tajam" yang ditemukan, cuma 26 (44%) yang tetap positif seperti skenario video — mayoritas (33/59) malah sudah nyeberang ke negatif. Skenario video sendiri itu minoritas kasus.
- Sample H2 timpang: didominasi cycle 2011-2013 (9 event) dan 2023-2025 (7 event), sementara 2013-2015 dan 2018-2019 cuma 1 event masing-masing — generalisasi riskan.

## Verdict akhir

**REJECT sebagai sinyal framework.** Tidak ada threshold/rule apparent demand yang diusulkan ke `Decision_Framework v1.md`. Data mentah (`apparent_demand` di master CSV) tetap disimpan untuk referensi masa depan, tapi butuh definisi event yang jauh lebih ketat dan sample lebih besar sebelum layak diuji ulang.
