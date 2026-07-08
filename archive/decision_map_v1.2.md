# DECISION MAP v1.2

**Tanggal dibuat:** 13 Juni 2026
**Update:** 14 Juni 2026 — v1.2
**Status:** Fase 1 Final — sinyal spesifik, threshold, dan confidence definition pending Fase 2

**Changelog v1.2:**
- Prerequisite dipisah dari informasi minimum di semua keputusan
- Hard Rule No. 3 (versi lama) dipisah menjadi dua rule spesifik
- Upper Range Recovery ditambah sebagai trigger partial reduce loan dan partial cash build
- Keputusan 6 difinalisasi

---

## KEPUTUSAN 1 — Reduce Exposure di Local Top / Cycle Peak

**Kapan relevan:** Sinyal Local Top atau Cycle Peak terdeteksi

**Prerequisite:** Tidak ada — ini keputusan pertama dalam cycle

**Pilihan tersedia:**
- Lunasi loan dulu lalu sell
- Sell dan lunasi bersamaan
- Tunggu konfirmasi lebih lanjut

**Informasi minimum:**
- Regime assessment: sinyal Local Top / Cycle Peak aktif?
- LTV posisi loan saat ini
- Confidence level sinyal (definisi pending Fase 2)

**Output keputusan:** Lunasi semua loan + sell 20-30% BTC jadi USDT (full cash buffer)

**Contingency:** Kalau Local Top tidak terdeteksi dan harga langsung crash ke Bear Market — ini gap eksplisit strategi ini. Mitigasinya adalah LTV monitoring ketat selama bull market late stage.

---

## KEPUTUSAN 2 — Deploy Cash dan Loan Bertahap Saat Bull Dip

**Kapan relevan:** Harga koreksi setelah Local Top, regime belum jelas apakah Bull Dip atau Mid-Cycle Correction

**Prerequisite — wajib terpenuhi sebelum eksekusi:**
- Local Top sudah terjadi sebelumnya
- Cash buffer 20-30% USDT dari Keputusan 1 sudah terbentuk
- Trigger start DCA cash sudah aktif (pending Fase 2)

**Pilihan tersedia:**
- Deploy cash
- Deploy loan
- Tahan
- Kurangi loan yang sudah ada

**Informasi minimum:**
- Confidence level sinyal (definisi pending Fase 2)
- Price action: harga masih turun / sideways / higher low terbentuk?
- LTV posisi saat ini dan proyeksi post-deploy

**Mekanisme deploy:**

*Cash:* DCA mingguan atau dua mingguan. Saat confidence naik ke High atau Very High dan higher low terbentuk — sisa cash lumpsum sekaligus.

*Loan:* Lumpsum per tahap. Satu transaksi per kenaikan confidence level. Bukan DCA — loan punya biaya bunga harian yang membuat DCA tidak efisien.

*Urutan:* Cash habis lebih dulu sebelum loan masuk.

**Tabel deploy:**

| Confidence | Price Action | Cash Deploy | Loan Deploy | LTV Post-Deploy |
|---|---|---|---|---|
| Low | Masih turun | 0% | 0% | — |
| Low | Sideways | 30-50% cash | 0% | — |
| Low | Higher Low | 50-100% cash | 0% | — |
| Medium | Masih turun | 100% cash | 20% | < 40% |
| Medium | Sideways | 100% cash | 40% | < 45% |
| Medium | Higher Low | 100% cash | 55% | < 50% |
| High | Masih turun | 100% cash | 60% | < 55% |
| High | Sideways | 100% cash | 75% | < 55% |
| High | Higher Low | 100% cash | 85% | < 55% |
| Very High | Higher Low + volume confirm | 100% cash | 100% | < 55% |

**Catatan:** "100% cash deploy" merujuk ke USDT 20-30% hasil Keputusan 1 — bukan semua aset.

**Hard override:** LTV menyentuh 65% = kurangi loan tanpa menunggu analisis apapun.

---

## KEPUTUSAN 3 — Short BTC

**Kapan relevan:** Lower High Confirm Top Cycle terdeteksi

**Prerequisite — wajib terpenuhi sebelum eksekusi:**
- Loan sudah 0
- Cash buffer sudah terbentuk
- Confidence level High atau Very High

**Pilihan tersedia:**
- Short
- Tidak short
- Tunggu konfirmasi lebih lanjut

**Informasi minimum:**
- Regime assessment: Lower High Confirm aktif?
- Confidence level sinyal (definisi pending Fase 2)

**Output keputusan:** Short BTC hanya kalau confidence High atau Very High. Low dan Medium = tidak short.

**Catatan:** Short menggunakan mekanisme BTC loan dengan collateral BTC. Detail strategi short dibahas di sesi terpisah.

---

## KEPUTUSAN 4 — Scale In di Bear Bottom

**Kapan relevan:** Sinyal Bear Bottom Near atau Pre-Detection Start of Bull aktif

**Prerequisite — wajib terpenuhi sebelum eksekusi:**
- Short position sudah ditutup
- Cash tersedia untuk di-deploy
- Trigger start DCA agresif sudah aktif (pending Fase 2)

**Pilihan tersedia:**
- DCA agresif
- DCA normal
- Tunggu konfirmasi lebih lanjut

**Informasi minimum:**
- Regime assessment: Bear Bottom Near atau Pre-Detection aktif?
- Confidence level sinyal (definisi pending Fase 2)

**Output keputusan:**
- Bear Bottom Near = mulai DCA agresif pakai USDT
- Pre-Detection = DCA agresif harus sudah selesai atau hampir selesai di fase ini

---

## KEPUTUSAN 5 — Deploy Loan di Awal Bull

**Kapan relevan:** Start of Bull Market Confirmation aktif

**Prerequisite — wajib terpenuhi sebelum eksekusi:**
- DCA agresif dari Keputusan 4 sudah selesai
- LTV headroom tersedia sebelum menyentuh 55%

**Pilihan tersedia:**
- Deploy loan
- Tidak deploy
- Tunggu konfirmasi lebih lanjut

**Informasi minimum:**
- Regime assessment: Start of Bull Confirmation aktif?
- Confidence level sinyal (definisi pending Fase 2)
- LTV proyeksi post-deploy

**Output keputusan:** Deploy loan. Besaran mengikuti tabel confidence yang sama dengan Keputusan 2.

---

## KEPUTUSAN 6 — Partial Reduce di Upper Range Recovery

**Kapan relevan:** Upper Range Recovery aktif — harga naik signifikan dari bottom tapi belum ATH baru

**Prerequisite:** Loan aktif dari Keputusan 5

**Pilihan tersedia:**
- Lunasi sebagian loan
- Pertahankan
- Tidak tambah loan baru

**Informasi minimum:**
- Regime assessment: Upper Range Recovery aktif?
- LTV posisi saat ini
- Confidence level (definisi pending Fase 2)

**Output keputusan:** Lunasi sebagian loan + build partial cash buffer. Tidak tambah loan baru. Agresifitas pengurangan lebih rendah dari Keputusan 1.

**Perbandingan agresifitas:**

| Regime | Aksi Loan | Build Cash | Level |
|---|---|---|---|
| Upper Range Recovery | Lunasi sebagian | Partial — % pending Fase 2 | Konservatif |
| Local Top / Cycle Peak | Lunasi semua | Full 20-30% | Agresif |

---

## HARD RULES — Berlaku di Semua Keputusan

1. **LTV 65% = override segalanya.** Kurangi loan tanpa menunggu sinyal, analisis, atau konfirmasi apapun
2. **LTV 55% = comfort ceiling.** Di atas ini mulai evaluasi pengurangan loan
3. **Loan di Bull Dip hanya boleh di-deploy kalau Local Top sudah terjadi dan cash buffer terbentuk** — ada USDT sebagai buktinya
4. **Loan di Start of Bull hanya boleh di-deploy kalau DCA agresif Bear Bottom sudah selesai**
5. **Short hanya kalau confidence High atau Very High** — Medium dan Low = tidak short
6. **Cash habis lebih dulu sebelum loan masuk** — urutan ini tidak boleh dibalik
7. **Loan deploy = lumpsum per tahap. Cash deploy = DCA mingguan** — jangan mix mekanisme keduanya
8. **Stress test wajib sebelum setiap deploy loan:** *"Kalau dua worst-case scenario terjadi bersamaan, apa yang terjadi ke LTV?"* — lesson langsung dari Oktober 2025
9. **Confidence definition belum final** — sampai Fase 2 selesai, semua confidence assessment bersifat judgment-based dan harus dicatat alasannya

---

## PENDING ITEMS — Diselesaikan di Fase 2

| Item | Keputusan yang Bergantung |
|---|---|
| Trigger start DCA cash — price threshold + sinyal onchain minimum | Keputusan 2 |
| Confidence definition — sinyal apa, berapa jumlah minimum per level | Semua keputusan |
| Trigger start DCA agresif di Bear Bottom | Keputusan 4 |
| % partial cash build di Upper Range Recovery | Keputusan 6 |
| Detail strategi short — sizing, exit, mekanisme BTC loan | Keputusan 3 |

---

## CATATAN STRUKTUR PORTOFOLIO

Portofolio terdiri murni dari BTC + USDT (cash). Tidak ada altcoin atau aset lain dalam scope framework ini.

**Alur satu cycle:**
1. Approaching Local Top / Cycle Peak → lunasi loan, sell 20-30% BTC ke USDT
2. Koreksi (Bull Dip ambigu) → deploy cash lalu loan bertahap sesuai confidence + price action
3. Lower High Confirm → short BTC kalau confidence tinggi
4. Bear Market Decline → hold, maintain short
5. Bear Bottom Near → tutup short, mulai DCA agresif
6. Pre-Detection → DCA agresif selesai
7. Start of Bull Confirmation → deploy loan
8. Upper Range Recovery → lunasi sebagian loan, partial cash buffer
9. Kembali ke siklus Local Top berikutnya
