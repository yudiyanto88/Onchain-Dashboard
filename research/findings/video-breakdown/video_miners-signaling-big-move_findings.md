# Video Breakdown: Bitcoin Miners Are Signaling a BIG Move!

- **URL:** https://www.youtube.com/watch?v=NS0gwz3LVlk
- **Channel:** On-Chain Mind
- **Tanggal video:** tidak tercantum eksplisit di deskripsi/frame (dari chart, harga BTC ~$98-100K — kemungkinan besar sekitar akhir 2024/awal 2025)
- **Tanggal breakdown:** 2026-07-12
- **Fokus:** tidak ada fokus khusus dari Yudi (breakdown umum)

## Ringkasan Sederhana

Video ini bahas 5 indikator dari sisi **miner** (penambang Bitcoin), bukan dari sisi holder seperti framework kita: Miners Sentiment Indicator, MPI (Miners' Position Index), Hash Ribbons, Difficulty Ribbon, dan Puell Multiple. Semua indikator ini mengukur perilaku dan tekanan jual dari penambang (bukan investor biasa).

Hasilnya: **semua 9 klaim di video OUT-OF-SCOPE**. Kenapa? Karena framework kita (`references/data_dictionary.md`) memang tidak pernah menarik data hashrate, difficulty, MPI, atau Puell Multiple dari ChartInspect — kita fokus di metrik holder-side (STH/LTH Realized Price, AVIV, MVRV, SOPR). Tidak ada satu pun klaim yang bisa diuji dengan data yang kita punya sekarang, jadi tidak ada yang lanjut ke skeptic maupun uji data.

Langkah berikutnya: tidak ada. Video ini murni informatif tentang dunia miner-side yang di luar cakupan framework kita saat ini. Kalau nanti Yudi mau menambah data miner ke pipeline, klaim-klaim ini baru layak diuji ulang — tapi itu keputusan terpisah, bukan hasil otomatis dari breakdown ini.

## Tabel Semua Klaim

| No | Klaim | Klasifikasi | Verdict skeptic | Hasil uji | Verdict akhir |
|----|-------|-------------|------------------|-----------|---------------|
| 1 | Miner sentiment shift historically mendahului price move BTC (framing pembuka, tanpa metrik konkret) | OUT-OF-SCOPE | - | - | REJECT (tidak bisa diuji, tidak ada mekanik terukur) |
| 2 | Miners Sentiment Indicator (7DMA komposit hashrate+difficulty+block count+block reward) siklus optimisme berkorelasi rally harga | OUT-OF-SCOPE | - | - | NEEDS-DATA-WE-DONT-HAVE |
| 3 | Miner sentiment saat ini "uncorrelated" dengan price yang choppy | OUT-OF-SCOPE | - | - | NEEDS-DATA-WE-DONT-HAVE |
| 4 | MPI spike = market top / miner capitulation di bear market | OUT-OF-SCOPE | - | - | NEEDS-DATA-WE-DONT-HAVE |
| 5 | MPI saat ini rendah = minim tekanan jual miner | OUT-OF-SCOPE | - | - | NEEDS-DATA-WE-DONT-HAVE |
| 6 | Hash Ribbons compression (30d/60d hashrate MA convergen) historically = price bottom major | OUT-OF-SCOPE | - | - | NEEDS-DATA-WE-DONT-HAVE |
| 7 | Difficulty Ribbon compression historically terjadi sebelum uptrend baru | OUT-OF-SCOPE | - | - | NEEDS-DATA-WE-DONT-HAVE |
| 8 | Puell Multiple green zone (miner revenue rendah) historically = price bottom | OUT-OF-SCOPE | - | - | NEEDS-DATA-WE-DONT-HAVE |
| 9 | Puell Multiple red zone (miner revenue tinggi) historically = cycle top | OUT-OF-SCOPE | - | - | NEEDS-DATA-WE-DONT-HAVE |

## Detail per Kandidat NOVEL

Tidak ada. Semua 9 klaim gugur di Stage 1 (ekstraksi) sebagai OUT-OF-SCOPE — tidak ada kandidat NOVEL yang lanjut ke `framework-skeptic` atau `data-verifier`.

**Kenapa semua OUT-OF-SCOPE, bukan cuma NEEDS-DATA:**

Video ini 100% berputar di data **miner-side** — hashrate, mining difficulty, block reward, dan turunannya (MPI, Hash Ribbons, Difficulty Ribbon, Puell Multiple). `references/data_dictionary.md` secara eksplisit mencatat metrik miner (hash rate, miner reserve, Puell Multiple) **tidak ada** di CSV kita. Framework kita (`Decision_Framework v1.md`, K1-K6) seluruhnya berbasis metrik holder-side: STH/LTH Realized Price, Realized Price, AVIV, MVRV, SOPR. Tidak ada satu K-node pun yang punya slot untuk sinyal miner-side.

**Catatan konseptual (bukan keputusan, sekadar observasi buat Yudi):** beberapa klaim video ini punya "bentuk" yang mirip logika yang sudah ada di framework kita, walau metriknya beda total:
- Hash Ribbons compression → bottom, dan Puell Multiple green zone → bottom — konsepnya mirip logika kapitulasi K4 (LTH-SOPR, aSOPR, Supply in Profit turun ekstrem), tapi diukur dari sisi miner (hashrate/revenue) bukan holder (cost-basis/profit).
- Puell Multiple red zone → cycle top — konsepnya mirip fungsi K1 (kurangi posisi di puncak siklus), tapi diukur dari miner revenue, bukan MVRV/aSOPR holder-side.

Ini bukan alasan untuk menambah data — cuma catatan supaya kalau suatu saat Yudi memang ingin evaluasi data miner secara terpisah, tahu klaim mana yang paling berpotensi.

## Usulan Perubahan Framework

Tidak ada usulan. 0 ADD.

## Butuh Judgment Yudi

Tidak ada — semua verdict sudah jelas. Video ini di luar cakupan data kita saat ini, tidak ada keputusan yang perlu diambil sekarang.

(Catatan sampingan, bukan pertanyaan yang butuh jawaban segera: kalau suatu saat Yudi tertarik menambah data miner-side — hashrate, difficulty, Puell Multiple — ke `auto_update.py`, itu keputusan produksi terpisah yang perlu diminta eksplisit di luar `/video-breakdown`, sesuai instruksi pipeline.)
