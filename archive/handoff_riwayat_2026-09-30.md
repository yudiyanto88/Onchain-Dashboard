# Riwayat handoff — dipindah 30 Sep 2026

Catatan sejarah yang dikeluarkan dari `handoff.md` saat audit 30 Sep 2026 (disetujui user). Tidak dipakai untuk kerja sehari-hari; buka hanya kalau perlu detail.

## Hasil run bot pertama per pipeline (bagian 1 lama)

Run bot tidak perlu dicek ulang kecuali ada gejala (data berhenti, error). Pipeline 23–26 lolos (22 Sep), Pipeline 27–28 lolos run bot pertama (dicek user 24 Sep). Pipeline 29 (ETF) lolos run bot pertama (25 Sep 09:11 UTC).

## Pipeline 26 — detail lengkap (bagian 7 lama)

- **Pipeline 26 (futures basis, beres 22 Sep):** spot = **Bitstamp** BTC/USD, Binance COIN-M dari **arsip `data.binance.vision`** (zip per kontrak quarterly), Deribit dari API. Alasannya: API Binance (`dapi`) menolak server GitHub Actions (*"Service unavailable from a restricted location"*); arsip lolos. Hasil Binance identik dengan API; basis bergeser rata-rata ±0,01 poin (maks 1,4 poin, 14 Jun 2022) karena spot ganti sumber. Bar hari berjalan tidak dihitung. Kalau zip bulanan belum terbit (terbit tgl 2 ±07:30 UTC; zip harian D+1 ±06:40 UTC), zip harian bulan itu dipakai — tanpa ini run tgl 1 diam-diam kehilangan Binance sebulan (diuji dengan simulasi). Run bot ±3–4 menit. Hasil lokal = hasil GitHub.

## Hasil cek kualitas data halaman yang sudah live (bagian 7 lama)

- **`data_tradfi.csv` (21 Sep):** sejak 4 Jan 2010, tanpa 0/macet, lonjakan > 10 % hanya asli (Mar 2020, Jan 2026), 6 tanggal libur beda.
- **VIX (21 Sep):** tanpa 0/macet/celah > 5 hari; 19 lonjakan > 40 % semuanya kejadian pasar asli (maks 82,69, 16 Mar 2020). **Yields (22 Sep):** tanpa ≤ 0; lonjakan terbesar 2Y −0,57 (13 Mar 2023, SVB); FRED telat 1–2 hari bursa. **Basis (22 Sep):** hasil Pipeline 26 identik dengan `research/findings/_futures_basis_3m_history.csv`; lonjakan besar (2021, −4,7 % 11 Mar 2023) dikonfirmasi kedua bursa; 3 Sep 2020 kedua bursa berlawanan tanda (belum dicek).
- **DXY (22 Sep):** Yahoo `DX-Y.NYB` 4 Jan 2010 –, tanpa 0/macet/akhir pekan; 877 baris kosong = potongan hari Minggu (dibuang `dropna`); celah terpanjang 5 hari (badai Sandy, Okt 2012); 3 hari > 2 % (3 Des 2015, 24 Jun 2016, 10 Nov 2022). Vs DXY hitungan rumus ICE dari kurs FRED H.10 (jam 12 siang NY): median selisih 0,08 %, maks 1,2 %, korelasi perubahan mingguan 0,98; 5 dari 10 selisih terbesar = hari FOMC.

## Item bagian 6 yang dihapus (tidak relevan lagi)

- **Pola umum seri `pane="price"` — belum diputuskan** (bahas kalau ada kasus lain). Sekarang hanya LTH 30d Change.
- **Ingatan kontrol setelah reload** (pilihan b, lewat URL query) — belum diminta.
- **Kotak L/R untuk pilihan sumbu** — ditahan (tidak menghemat lebar).
- **Server localhost mati sendiri (23 Sep, 3×):** dugaan (belum pasti) — panel browser Claude dipakai membuka situs luar di tab yang sama. Buka situs luar di tab lain.

## Bagian 9 yang digabung

- **Heredoc Bash mengubah `\\n` di skrip patch jadi baris baru sungguhan** → tulis skrip dengan Write, atau pakai Edit.
