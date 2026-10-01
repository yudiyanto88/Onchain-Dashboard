# Langkah 0: Audit (dijalankan 2026-10-01)

## Akses
- Kalshi API publik: OK (200), tanpa login, termasuk `/historical/markets/{ticker}/candlesticks`.
- Binance Vision: OK. File bulanan 2023-03 sampai 2026-08 ada; 2026-09 belum terbit (404), pakai folder `daily`.
- `api.binance.com` (REST): 451 diblokir. Tidak dipakai.
- Rate limit Kalshi dari mesin ini: kena 429 sekitar 1 permintaan per detik tanpa throttle. Dipakai throttle 4 req/detik + backoff. 112 permintaan di run terakhir.

## Temuan struktur data
- 28 rapat selesai, 140 market. Tidak ada rapat yang gagal diunduh.
- Event 2023-05 sampai 2024-11 memakai prefix `FEDDECISION-` (bukan `KX`). Tiap event 4 sampai 6 market, set hasilnya beda dari asumsi brief (ada H50, TH50, TC25). Pemetaan bps harus dibaca dari `custom_strike`, bukan akhiran ticker.
- Market dengan tanggal selesai sebelum 2026-08-01 ada di endpoint `/historical`, sesudahnya di endpoint live `/series/{s}/markets/{t}/candlesticks`. Nama field beda antar endpoint (`volume` vs `volume_fp`).
- API mengirim candle 1 menit tanpa transaksi dengan volume 0 (harga lama dibawa). Total candle 28 hari: 737.467 dikirim, 289.086 punya volume > 0. Sisa menit (5,36 juta market-menit) kosong atau tidak dikirim.
- Candle 1 menit dengan end_ts=T mencakup [T-60, T). Sejajarkan dengan kline Binance dengan open_time = T-60.
- Timestamp Binance: milidetik sampai 2024-12, mikrodetik mulai 2025-01.
- Di menit yang bertransaksi, bid dan ask selalu ada (100%). Spread yang diamati 1 sen (contoh 25SEP-C25).

## Tabel audit per rapat (jendela 28 hari sebelum rapat)
Kolom "% menit ada transaksi" = menit di mana minimal satu dari market rapat itu bertransaksi.

| Rapat | Tanggal (UTC) | Market | Candle transaksi pertama | % menit ada transaksi (28h) | Tersisa 7 hari terakhir | Volume (kontrak) |
|---|---|---|---|---|---|---|
| FEDDECISION-23MAY | 2023-05-03 | 6 | 2023-04-08 | 1.4% | 3.7% | 332,257 |
| FEDDECISION-23JUN | 2023-06-14 | 5 | 2023-05-04 | 1.8% | 2.1% | 337,064 |
| FEDDECISION-23JUL | 2023-07-26 | 5 | 2023-06-15 | 0.7% | 1.0% | 212,159 |
| FEDDECISION-23SEP | 2023-09-20 | 5 | 2023-07-27 | 0.6% | 0.8% | 169,009 |
| FEDDECISION-23NOV | 2023-11-01 | 5 | 2023-09-24 | 0.8% | 0.6% | 227,655 |
| FEDDECISION-23DEC | 2023-12-13 | 5 | 2023-11-02 | 0.4% | 0.6% | 96,770 |
| FEDDECISION-24JAN31 | 2024-01-31 | 5 | 2023-12-14 | 0.3% | 0.2% | 226,181 |
| FEDDECISION-24MAR20 | 2024-03-20 | 5 | 2024-02-01 | 0.4% | 0.4% | 287,778 |
| FEDDECISION-24MAY | 2024-05-01 | 5 | 2024-03-21 | 0.6% | 0.5% | 512,033 |
| FEDDECISION-24JUN | 2024-06-12 | 4 | 2024-05-02 | 0.4% | 1.0% | 285,444 |
| FEDDECISION-24JUL | 2024-07-31 | 5 | 2024-06-12 | 1.1% | 1.6% | 936,728 |
| FEDDECISION-24SEP | 2024-09-18 | 5 | 2024-07-31 | 5.5% | 14.6% | 1,943,863 |
| FEDDECISION-24NOV | 2024-11-07 | 5 | 2024-09-18 | 2.0% | 2.1% | 472,999 |
| KXFEDDECISION-24DEC | 2024-12-18 | 5 | 2024-10-31 | 6.3% | 8.8% | 2,179,944 |
| KXFEDDECISION-25JAN | 2025-01-29 | 5 | 2024-12-19 | 2.3% | 3.4% | 1,710,317 |
| KXFEDDECISION-25MAR | 2025-03-19 | 5 | 2025-01-30 | 2.3% | 2.1% | 2,105,618 |
| KXFEDDECISION-25MAY | 2025-05-07 | 5 | 2025-03-20 | 55.6% | 59.5% | 37,979,758 |
| KXFEDDECISION-25JUN | 2025-06-18 | 5 | 2025-05-08 | 35.4% | 34.7% | 24,414,410 |
| KXFEDDECISION-25JUL | 2025-07-30 | 5 | 2025-06-19 | 37.0% | 51.4% | 38,881,066 |
| KXFEDDECISION-25SEP | 2025-09-17 | 5 | 2025-07-31 | 48.4% | 71.1% | 77,378,289 |
| KXFEDDECISION-25OCT | 2025-10-29 | 5 | 2025-08-06 | 33.6% | 41.1% | 33,761,420 |
| KXFEDDECISION-25DEC | 2025-12-10 | 5 | 2025-08-12 | 49.1% | 61.8% | 35,571,094 |
| KXFEDDECISION-26JAN | 2026-01-28 | 5 | 2025-10-07 | 49.5% | 48.7% | 31,844,544 |
| KXFEDDECISION-26MAR | 2026-03-18 | 5 | 2025-10-16 | 28.2% | 35.7% | 24,097,450 |
| KXFEDDECISION-26APR | 2026-04-29 | 5 | 2025-11-14 | 21.3% | 25.5% | 11,289,441 |
| KXFEDDECISION-26JUN | 2026-06-17 | 5 | 2025-09-30 | 26.2% | 34.9% | 24,704,170 |
| KXFEDDECISION-26JUL | 2026-07-29 | 5 | 2025-10-27 | 38.6% | 59.5% | 61,468,412 |
| KXFEDDECISION-26SEP | 2026-09-16 | 5 | 2026-01-28 | 50.6% | 82.4% | 92,135,310 |

## Penilaian
Ambang "data cukup" tidak ditentukan di brief. Asumsi saya: minimal 10% menit di jendela 28 hari ada transaksi.
- Lolos: 12 rapat (25MAY sampai 26SEP, Mei 2025 sampai Sep 2026). Hasilnya sama untuk ambang 10% sampai 20%.
- Tipis (kurang dari 7%): 16 rapat, 23MAY sampai 25MAR. Ada 2 di 3 sampai 7% (24SEP, 24DEC) yang lolos kalau ambang 5%.
- 12 >= 8, jadi syarat berhenti tidak terpicu. Per brief tetap berhenti di sini untuk laporan.
