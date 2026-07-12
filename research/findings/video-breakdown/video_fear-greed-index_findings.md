# Video Breakdown: How to Use the Fear & Greed Index for Bitcoin

- **URL:** https://www.youtube.com/watch?v=RBWUehoqfI0
- **Channel:** On-Chain Mind
- **Tanggal video:** 2025-02-23
- **Tanggal breakdown:** 2026-07-12
- **Fokus khusus:** tidak ada, ekstraksi standar

## Ringkasan Sederhana

Video ini menjelaskan Bitcoin Fear & Greed Index (F&G) — indikator sentimen 0-100% yang skornya rendah kalau pasar takut (fear), tinggi kalau pasar euforia (greed). Video kasih beberapa klaim historis: di siklus 2021, F&G sempat mencapai puncak (92%) jauh sebelum harga BTC benar-benar top; dan saat harga betulan top, F&G sudah turun. Video juga bilang F&G versi rata-rata 30 hari (SMA30) bisa dipakai untuk melihat tren sentimen lebih halus.

Framework kita **sudah** pakai F&G — tapi cuma di K5 (F&G<50 sebagai salah satu trigger beli tambahan pas dip), dan itu sudah pernah diuji sebelumnya dengan hasil CONDITIONAL. Dua klaim baru dari video ini — F&G SMA30 sebagai versi lebih baik dari F&G harian, dan F&G peak-sebelum-top sebagai sinyal baru untuk K1 (exit puncak siklus) — sudah diuji ke data kita dan **keduanya gagal**. SMA30 justru kehilangan 60% sinyal yang tertangkap versi harian. Pola F&G turun di tiap ATH baru cuma benar 53% dari waktu (mirip lempar koin), dan satu-satunya siklus yang datanya lengkap (2021) malah berlawanan arah dengan klaim video. Sisa klaim lain di video sifatnya cuma narasi umum (definisi index, opini kondisi pasar saat itu) — tidak ada mekanik baru yang bisa diuji. Kesimpulan: video ini tidak menambah apapun ke framework, dan konfirmasi lagi kalau F&G sebaiknya tetap jadi pelengkap kecil di K5, bukan diperluas ke K-node lain.

## Tabel Semua Klaim

| No | Klaim | Klasifikasi | Verdict skeptic | Hasil uji | Verdict akhir |
|----|-------|-------------|------------------|-----------|---------------|
| 1 | F&G 61% = neutral (snapshot Feb 2025) | OUT-OF-SCOPE | - | - | - |
| 2 | F&G tergantung trend harga, bukan level harga absolut | NOVEL | REJECT-NOW | - | REJECT |
| 3 | F&G SMA30 sebagai smoothing tren sentimen (refinement K5) | NOVEL | TEST | NOT-SUPPORTED | REJECT |
| 4 | Definisi range F&G 0-100% | OUT-OF-SCOPE | - | - | - |
| 5 | DCA lebih besar saat fear, kurang saat greed = historically outperform | DUP (K5) | - | - | (pakai verdict K5 lama) |
| 6 | First cross extreme greed 2021 = exit prematur | NOVEL | REJECT-NOW | - | REJECT |
| 7 | F&G peak jauh sebelum price top (2021) — sinyal ke-6 K1 | NOVEL | TEST | NOT-SUPPORTED | REJECT |
| 8 | F&G cooled off (70-80%) saat price top (2021) | NOVEL | TEST (gabung #7) | NOT-SUPPORTED | REJECT |
| 9 | Fase parabolic akhir didorong FOMO/retail frenzy | OUT-OF-SCOPE | - | - | - |
| 10 | Extreme fear persistence 2022 tidak berguna timing bottom | NOVEL | REJECT-NOW | - | REJECT |
| 11 | Bull market: F&G dip + price action kuat = buy opportunity | DUP + TESTED-BEFORE | - | - | CONDITIONAL (verdict lama, `k5_fear_greed_trigger_findings.md`) |
| 12 | Zona neutral F&G → konsolidasi/choppy | OUT-OF-SCOPE | - | - | - |
| 13 | F&G 61% align dengan "indikator risiko lain" (vague) | OUT-OF-SCOPE | - | - | - |
| 14 | Struktur bullish, tidak dekat major top (opini Feb 2025) | OUT-OF-SCOPE | - | - | - |

## Detail per Kandidat NOVEL

### Kandidat 2 — F&G fungsi trend/momentum harga, bukan level harga absolut
- Apa yang video bilang: harga $96k menghasilkan F&G 81% di satu momen tapi bikin dip ke fear di momen lain — jadi F&G bukan sekadar cerminan level harga, tapi dipengaruhi trend/momentum/volatilitas.
- Kata skeptic: ini cuma penjelasan cara kerja index, bukan aturan if-then yang bisa diuji. Sudah terbukti implisit dari findings K5 lama — F&G<50 menangkap pullback yang terlewat sinyal STH+SOPR, jadi memang bukan proxy harga murni. Tidak ada mekanik baru.
- Hasil uji data: tidak diuji (REJECT-NOW dari skeptic, tidak lanjut ke data-verifier).
- **Verdict akhir: REJECT** — narasi penjelasan, bukan insight baru yang bisa ditambah ke framework.

### Kandidat 3 — F&G SMA30 sebagai refinement trigger K5
- Apa yang video bilang: F&G versi rata-rata 30 hari (SMA30) menghaluskan fluktuasi harian, jadi gambaran tren sentimen lebih bersih dibanding reading harian.
- Kata skeptic: layak diuji karena baseline K5 (raw F&G<50) sudah CONDITIONAL dengan false-rate lumayan (3/16 run 2023). SMA30 bisa jadi jawaban. Tapi ada risiko: lag besar mungkin bikin SMA30 kehilangan sinyal di recovery cepat (2019 V-shape).
- Hasil uji data: diuji di 19 episode pullback yang sama dengan findings K5 lama (2019 & 2023-2024).
  - Raw F&G<50 tersentuh di 5/19 pullback. SMA30(F&G)<50 cuma tersentuh di **2/19**.
  - **3 dari 5 sinyal raw hilang total** kalau pakai SMA30 — termasuk seluruh episode 2019 (SMA30 minimum di 63 hari episode itu = 57, tidak pernah turun ke bawah 50, padahal raw sempat sampai 27).
  - Di 2 pullback yang SMA30 memang menyala, sinyalnya telat 15-32 hari dari raw crossing pertama — bukan sinyal awal, cuma versi telat.
  - n = 19 pullback, 2 cycle (2019, 2023-2024) — sama seperti findings lama.
- **Verdict akhir: REJECT** — SMA30 bukan perbaikan, malah kehilangan 60% sinyal genuine dan sisanya cuma versi telat. Raw F&G<50 (yang sudah CONDITIONAL) tetap lebih baik.

### Kandidat 7 & 8 (digabung) — F&G peak sebelum price top / cooled off saat top (2021) — potensi sinyal ke-6 K1
- Apa yang video bilang: di 2021, F&G index mencapai puncak (92%) saat harga BTC baru $30k, jauh sebelum harga benar-benar top (~$69k). Saat harga top, F&G sudah turun ke 70-80% dari puncaknya. Video menyimpulkan puncak sentimen tidak berbarengan dengan puncak harga.
- Kata skeptic: pola ini analog ke signal #1 (MVRV turun di tiap ATH baru) dan #2 (aSOPR turun) yang sudah ada di K1. Layak diuji sebagai kandidat sinyal ke-6, dengan definisi generik "F&G turun di tiap ATH baru dalam siklus yang sama" — jangan pakai angka spesifik video sebagai threshold. Wajib cek redundansi dengan MVRV/aSOPR yang sudah ada, dan wajib sebut keterbatasan sample (data F&G cuma mulai 2018, jadi cuma bisa cek 2021 penuh + 2025 partial).
- Hasil uji data: aturan generik diuji dengan definisi ATH yang sama persis dengan cara signal #1/#2 divalidasi.
  - Uji granular (tiap ATH baru dalam siklus): 2021 → F&G turun di 3/7 pasangan (43%). 2023-2025 → turun di 5/8 pasangan (63%). Total 8/15 (53%) — hampir persis lempar koin, bukan pola turun bersih seperti MVRV.
  - Redundancy check: arah F&G sama dengan arah MVRV cuma 47% dari waktu, dengan aSOPR 27% — jadi F&G **tidak** redundan dengan sinyal existing, tapi karena arahnya juga tidak konsisten menurun, "tidak redundan" di sini berarti noise, bukan info tambahan yang berguna.
  - Uji granularitas kasar (2 titik ATH mayor per siklus, cara yang sama dipakai untuk validasi MVRV Z-score divergence sebelumnya): siklus 2021 (satu-satunya yang benar-benar matang datanya) — F&G malah **naik tipis** (74→75), berlawanan langsung dengan klaim video. Di pasangan yang sama, MVRV turun bersih (3.435→2.851) — jadi kontras jelas: MVRV konsisten, F&G tidak.
  - n = 2 cycle, tapi cuma 1 yang benar-benar matang (2021); siklus 2023-2025 baru topping ~9 bulan lalu per data terkini. Jauh lebih tipis dari sample MVRV/aSOPR yang biasa pakai 4 cycle. Cycle 2017/2013/2011 tidak bisa dicek — data F&G belum ada (NEEDS-DATA-WE-DONT-HAVE untuk cycle-cycle itu, tapi tidak akan pernah tersedia karena F&G index sendiri baru mulai dihitung 2018).
- **Verdict akhir: REJECT** — pola turun di tiap ATH baru cuma ~53% (setara lempar koin), dan satu-satunya siklus dengan data matang penuh (2021) justru berlawanan arah dengan klaim video. Sample terlalu tipis (n=2, 1 matang) untuk klaim apapun yang solid, tapi arah hasilnya sudah cukup jelas menolak — bukan kasus butuh lebih banyak data, videonya memang keliru untuk siklus yang paling lengkap datanya.

## Usulan Perubahan Framework

Tidak ada — semua kandidat REJECT.

## Butuh Judgment Yudi

Tidak ada — semua verdict sudah jelas.
