# Video Breakdown: Bitcoin Whales Are Accumulating Right Now

- **URL:** https://www.youtube.com/watch?v=eavpxyuWrvE
- **Channel:** On-Chain Mind
- **Tanggal video:** 2025-01-27
- **Tanggal breakdown:** 2026-07-11
- **Fokus khusus:** tidak ada — semua klaim di video diproses

## Ringkasan Sederhana

Video ini video lama (18 bulan lalu), membahas kondisi Bitcoin akhir Januari 2025: whale lagi nambah koleksi, holder kecil lagi jual, sell pressure mereda pasca rally Desember 2024, tapi demand mulai melambat. Dari 7 klaim yang diucapkan, 2 langsung di luar scope (angka snapshot lama dan bahasan Ethereum — framework kita cuma BTC). Dari 4 klaim yang berpotensi baru, semuanya gagal di tahap kritik: 3 butuh data yang tidak kita punya (whale-by-wallet-size, apparent demand, demand momentum — bukan metrik yang di-pull ChartInspect), dan 1 klaim (realized profit $ turun = sell pressure lewat) ternyata bertentangan dengan hasil riset kita sendiri di KB SOPR — pola serupa historically justru sering jadi awal bear onset, bukan sinyal rally lanjut. Satu klaim ambigu ("profit margin trader turun 60%→0%") kemungkinan besar itu NUPL, dan sudah redundan sama rule yang sudah ada di KB NUPL. **Tidak ada perubahan framework yang diusulkan dari video ini.**

## Tabel Semua Klaim

| No | Klaim | Klasifikasi | Verdict skeptic | Hasil uji | Verdict akhir |
|----|-------|-------------|------------------|-----------|---------------|
| 1 | Whale holdings monthly growth rate spike (-0.25%→2%) sebelum inaugurasi Trump | OUT-OF-SCOPE | - | - | REJECT (point-in-time, one-off event) |
| 2 | Divergensi whale accumulation (16.2M→16.4M) vs small holder distribution (1.75M→1.69M) sebagai driver harga | NOVEL | NEEDS-DATA-WE-DONT-HAVE | tidak diuji | NEEDS-MORE-DATA (butuh data whale/entity yang tidak kita punya) |
| 3 | Realized profit $ volume turun $10B→$2-3B/hari = sell pressure mereda | NOVEL | REJECT-NOW | tidak diuji | REJECT (kontradiksi KB SOPR — pola ini historis 4/4 justru mendahului bear onset) |
| 4 | Trader profit margin turun ~60%→~0% = sinyal price floor | TESTED-BEFORE (dengan catatan) | REJECT-NOW | tidak diuji | REJECT (redundan Rule S2/B2/B3 KB NUPL) |
| 5 | Apparent demand masih positif tapi rate turun tajam (279k→75k BTC/bulan) | NOVEL | NEEDS-DATA-WE-DONT-HAVE | tidak diuji | NEEDS-MORE-DATA (metrik "apparent demand" tidak ada di data kita) |
| 6 | Demand momentum anjlok (1.7M→100k BTC) = buying pressure melemah | NOVEL | NEEDS-DATA-WE-DONT-HAVE | tidak diuji | NEEDS-MORE-DATA (turunan dari klaim 5, root cause sama) |
| 7 | ETH underperform BTC 43% karena ETH kembali inflationary pasca-Merge | OUT-OF-SCOPE | - | - | REJECT (altcoin, di luar scope BTC framework) |

## Detail per Kandidat NOVEL

### Divergensi whale accumulation vs small holder distribution
- Apa yang video bilang: Wallet besar ("whale") terus nambah BTC sementara wallet kecil terus jual, dan video bilang ini yang dorong harga naik.
- Kata skeptic: Metrik ini beda total dari STH/LTH kita — punya kita berbasis lama pegang koin (holding-time), video ini berbasis besar saldo wallet (wallet-size). Data whale/entity balance tidak ada di `data_dictionary.md` kita — memang eksplisit tercatat sebagai salah satu yang TIDAK kita punya.
- Hasil uji data: Tidak diuji — datanya tidak ada.
- **Verdict akhir: NEEDS-MORE-DATA** — kalau suatu saat kita punya data whale-by-wallet-size, klaim ini perlu dirumuskan ulang jadi aturan if-then yang jelas dulu (bukan sekadar narasi "divergensi = driver"), baru diuji.

### Realized profit $ volume turun tajam = sell pressure mereda
- Apa yang video bilang: Setelah rally Desember 2024 ke dekat $100K, profit yang dicairkan investor turun drastis dari $10 miliar/hari ke $2-3 miliar/hari. Video bilang ini tanda sell pressure sudah mereda, siap-siap rally lagi.
- Kata skeptic: Ini pada dasarnya reskin dari pola SOPR (rasio profit saat jual) yang sudah diteliti dalam di KB kita. Hasilnya malah kebalikan dari klaim video: aSOPR dan STH-SOPR yang turun tajam pasca-rally itu, di 4 dari 4 kasus historis, justru jadi tanda AWAL bear onset — bukan tanda sell pressure sudah selesai. Video ini snapshot Januari 2025, dan faktanya cycle itu memang berakhir dengan Lower High terkonfirmasi Oktober 2025 — jadi klaim bullish di video ini secara historis tidak terbukti benar untuk cycle yang sama.
- Hasil uji data: Tidak diuji lebih lanjut — sudah cukup bukti dari KB yang ada kalau klaim ini kontradiktif dengan riset kita sendiri.
- **Verdict akhir: REJECT**

### Trader profit margin turun ~60%→~0% = sinyal price floor
- Apa yang video bilang: Margin profit trader (istilah yang dipakai video ambigu, ketuker antara "unrealized" dan "realized") turun dari 60% (November-Desember, "overheated") ke hampir 0% (pertengahan Januari). Video bilang ini tanda trader kurang insentif jual, pasar mendekati titik stabil.
- Kata skeptic: Paling cocok diinterpretasi sebagai NUPL (Net Unrealized Profit/Loss) — angka 60% di Nov-Des match dengan NUPL historis kita di Local Top Desember 2024 (0.634), sedangkan aSOPR di titik yang sama cuma 15%, tidak match. Tapi pola ini sudah persis sama dengan Rule S2 dan B2/B3 di KB NUPL kita — sudah diuji lengkap termasuk kasus-kasus false signal-nya (Bull Dip Juli 2024, Yen Carry Trade Agustus 2024). Tidak ada informasi baru dari klaim video ini.
- Hasil uji data: Tidak diuji ulang — sudah redundan dengan rule yang sudah divalidasi.
- **Verdict akhir: REJECT**

### Apparent demand masih positif tapi rate turun tajam
- Apa yang video bilang: Demand Bitcoin masih tumbuh (bukan negatif) tapi laju pertumbuhannya melambat drastis — dari 279 ribu BTC/bulan (awal Desember) ke cuma 75 ribu BTC/bulan (Januari). Video bilang ini perlu rebound dulu sebelum rally lanjut bisa terjadi.
- Kata skeptic: "Apparent Demand" (30 hari perubahan circulating supply, gaya Glassnode) sama sekali tidak ada di 105 kolom `data_master_all_metrics.csv` kita, dan tidak ada proxy langsung dari kolom yang ada.
- Hasil uji data: Tidak diuji — datanya tidak ada.
- **Verdict akhir: NEEDS-MORE-DATA** — kalau mau diuji nanti, perlu tambah pull metrik "apparent demand" ke `auto_update.py` dulu.

### Demand momentum anjlok = buying pressure melemah
- Apa yang video bilang: Turunan dari demand growth (momentum-nya) jatuh drastis dari 1.7 juta BTC ke 100 ribu BTC di periode yang sama. Video bilang ini tanda buying pressure melemah.
- Kata skeptic: Ini turunan langsung dari klaim Apparent Demand di atas — root cause sama, data dasarnya tidak ada.
- Hasil uji data: Tidak diuji — datanya tidak ada.
- **Verdict akhir: NEEDS-MORE-DATA** — sama seperti klaim Apparent Demand, tergantung data yang belum kita pull.

## Usulan Perubahan Framework

Tidak ada — tidak ada klaim yang lolos ke ADD.

## Butuh Judgment Yudi

1. Ada 3 klaim (whale-by-wallet-size, apparent demand, demand momentum) yang kena `NEEDS-MORE-DATA` karena kita memang tidak pull metrik itu dari ChartInspect. Apakah Yudi mau menambah metrik ini ke `auto_update.py`, atau memang sengaja tidak dipakai karena framework kita sudah cukup dengan STH/LTH + SOPR + supply-in-profit? Kalau tidak berencana pakai, klaim-klaim ini bisa ditandai selesai (tidak perlu dikejar lagi).
2. Tidak ada pertanyaan lain — sisanya verdict sudah jelas (REJECT karena kontradiksi atau redundan dengan KB yang sudah ada).
