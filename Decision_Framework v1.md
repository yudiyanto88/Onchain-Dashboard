# Framework Investasi BTC — Ringkasan Eksekusi
*Versi final. Semua K-node locked.*

---

## ZONE STRUCTURE

Zona ditentukan dari posisi harga relatif terhadap level on-chain. Setiap zona punya satu K yang aktif sebagai panduan utama.

```
Z1   │ Price < STH RP  (STH RP < RP — ordering terbalik)   │ K4
Z1b  │ STH RP ≤ Price < RP  (STH RP masih < LTH RP)        │ K4 wrap-up
Z2   │ STH RP ≈ RP ≈ LTH RP  (ketiganya konvergen)         │ K5 mulai
Z3   │ RP ≤ Price < AVIV Mean                               │ K5 aktif
Z4   │ AVIV Mean ≤ Price < AVIV Upper                       │ K6 / K2 dari Z5
Z5   │ Price ≥ AVIV Upper                                   │ K1 / K2 ke Z4
─────────────────────────────────────────────────────────────
CVDD │ Flag ekstrem dalam Z1 — Price/CVDD < 1.0 = langka sekali
```

**Level yang jadi batas zona:**
- STH RP = rata-rata harga beli holder baru (< 155 hari)
- RP = rata-rata harga beli semua holder (Realized Price)
- LTH RP = rata-rata harga beli holder lama (> 155 hari)
- AVIV Mean = rata-rata harga beli investor aktif
- AVIV Upper = batas atas AVIV (+0.5 SD dari mean)
- CVDD = batas bawah historis paling ekstrem

**Cara baca zona:** Z1 = bear bottom paling dalam. Z5 = puncak siklus. Trajectory (dari mana harga datang) menentukan K mana yang aktif di Z4.

---

## K1 — Kurangi Posisi di Puncak Siklus

**Kapan relevan:** Harga pernah bertahan di Z5 minimal 14 hari dalam siklus ini.

**Dua syarat awal yang harus aktif dulu:**
- MVRV di setiap ATH baru lebih rendah dari ATH sebelumnya dalam siklus yang sama
- aSOPR di setiap ATH baru juga lebih rendah dari sebelumnya

Kalau dua ini belum terpenuhi, K1 tidak perlu dipikirin sama sekali.

**5 sinyal peringatan (perlu dicek aktif tidaknya):**

| # | Sinyal | Sumber |
|---|--------|--------|
| 1 | MVRV turun di setiap ATH baru (diminishing returns) | MVRV KB v1.4 |
| 2 | aSOPR turun di setiap ATH baru | SOPR KB v1.4 |
| 3 | Harga di atas STH RP tapi STH-MVRV mendekati 1.0 | MVRV KB v1.4 |
| 4 | Gap MA90-MA60 di STH-SOPR sudah memuncak dan mulai turun | SOPR KB v1.4 |
| 5 | Supply in Profit di atas 90% dan mulai turun | Supply KB v1.4 |

**Trigger eksekusi — OR gate (mana yang muncul duluan):**
- Harga turun dari Z5 ke Z4 (AVIV Upper cross-down) **ATAU**
- Gap MA90-MA60 STH-SOPR memuncak dan turun minimal 14 hari berturutan

Mana yang muncul duluan = eksekusi K1 sekarang. Tidak perlu tunggu keduanya.

**Aksi K1:**
- Lunasi semua loan yang aktif → loan = 0
- Jual 20–30% dari total BTC → parkir ke USDT

**Catatan penting:** Window antara sinyal awal dan deadline sudah menyempit dari ~30 hari (2017) jadi bisa sesempit 6 hari (2025). Jangan tunda.

---

## K2 — Masuk di Bull Dip

**Kapan berlaku:** Harga turun dari Z5 ke Z4, atau dari Z4 ke Z3 — dan K3 Stage 2 belum aktif. Kalau bear sudah terkonfirmasi, ini bukan bull dip.

**Dua situasi berbeda:**

Setelah K1 jalan: ada cash 20–30% USDT dari hasil jual. Cash habis dulu, baru loan masuk. Confidence minimum: medium.

Tanpa K1: tidak ada cash. Langsung pakai sisa kapasitas loan. Confidence minimum: high atau very high saja.

**5 kondisi untuk tentukan confidence:**

| # | Kondisi | Sumber |
|---|---------|--------|
| 1 | STH-MVRV di bawah 0.95 saat dip, rasio LTH-MVRV dibagi STH-MVRV naik dalam 14 hari sebelum dip | MVRV KB v1.4 |
| 2 | STH-SOPR di bawah 0.97 tapi belum bertahan lebih dari 14 hari, aSOPR masih di atas 0.95 | SOPR KB v1.4 |
| 3 | Total Supply in Profit masih di atas 60%, bagian STH profit turun | Supply KB v1.4 |
| 4 | Bagian LTH profit stabil, tidak ikut turun lebih dari 2% dari rata-rata 30 hari sebelumnya | Supply KB v1.4 |
| 5 | Harga close di bawah AVIV Mean, lalu close kembali di atas sebelum atau tepat di hari ke-4. Dihitung dari hari pertama close di bawah, tidak direset. Terkonfirmasi setelah bounce, bukan saat entry | Price Level KB v1.4 |

- 2 dari 5: Low — tidak ada aksi
- 3 dari 5: Medium
- 4 dari 5: High
- 5 dari 5: Very High (kondisi ke-5 hanya bisa dikonfirmasi setelah bounce)

**Tabel deploy:**

| Confidence | Price action | Cash deploy | Loan deploy | LTV setelah |
|------------|-------------|-------------|-------------|-------------|
| Low | Apapun | 0% | 0% | — |
| Medium | Masih turun | 100% cash | 0% | — |
| Medium | Sideways | 100% cash | 20% | < 40% |
| Medium | Higher low | 100% cash | 40% | < 45% |
| High | Masih turun | 100% cash | 40% | < 48% |
| High | Sideways | 100% cash | 60% | < 50% |
| High | Higher low | 100% cash | 80% | < 52% |
| Very High | Higher low + konfirmasi bounce AVIV Mean | 100% cash | 100% | < 52% |

Untuk situasi tanpa K1: kolom cash selalu 0%, loan langsung dari sisa kapasitas, confidence minimum high.

**Kalau ternyata salah — staged cut:**

| LTV | Yang dilakukan |
|-----|----------------|
| 58–60% | Jual collateral, bawa LTV balik ke 53–54% |
| 62–63% | Jual lebih besar, target 55% |
| 65% | Jual besar, target di bawah 50% |

Komitmen keras: LTV 60% = jual collateral dan bayar loan sekarang, tidak perlu tunggu analisis apapun.

Cut-loss: harga turun 20% dari titik masuk → jual collateral, bayar sebagian besar loan, target LTV di bawah 50%.

---

## K3 — Short/Hedge saat Bear Mulai

**Kapan relevan:** Setelah K1 selesai. Loan sudah nol.

**Dua syarat awal yang harus aktif dulu (sama dengan K1):**
- MVRV turun di setiap ATH baru dalam siklus yang sama
- aSOPR turun di setiap ATH baru dalam siklus yang sama

**Stage 1 — Waspada (mana yang muncul duluan):**
- Harga turun dari Z5 menembus AVIV Upper ke bawah **ATAU**
- Gap MA90-MA60 STH-SOPR memuncak dan mulai turun

Mana yang muncul duluan = Stage 1 aktif. Aksi: tidak ada. Pantau sinyal kedua saja.

**Stage 2 — Konfirmasi:**
Sinyal yang belum muncul di Stage 1 sekarang ikut muncul juga. Dua sinyal dari dua sumber berbeda saling mengkonfirmasi.

Aksi: buka short sebesar 30% dari BTC yang masih dipegang.

**Cara keluar dari posisi short:**

| Kondisi | Aksi |
|---------|------|
| 4 hari berturutan close di atas AVIV Mean, tapi harga masih di bawah STH RP | Kurangi ukuran short (bukan tutup) |
| Harga kembali ke Z5 dan bertahan | Tutup short sepenuhnya — K3 baca salah |
| K4 mulai aktif | Tutup short, beralih ke mode akumulasi |

**Catatan:** Urutan Stage 1 dan 2 tidak selalu sama tiap siklus. Di 2017 dan 2021, AVIV cross muncul duluan dengan jarak 45–68 hari. OR-gate sengaja dipilih supaya tidak bertaruh pada urutan yang tidak stabil.

---

## K4 — Akumulasi Agresif di Bear Bottom

**Kapan berlaku:** Z1 aktif — harga di bawah STH RP, dengan kondisi STH RP lebih rendah dari RP. Kalau belum di Z1, K4 tidak berlaku.

**4 kondisi untuk tentukan seberapa agresif beli:**

| # | Kondisi | Sumber |
|---|---------|--------|
| 1 | LTH-MVRV juga sudah di bawah 1.0 — bahkan holder lama rata-rata rugi | MVRV KB v1.4 |
| 2 | aSOPR di bawah 0.93 bertahan minimal 7 hari, DAN LTH-SOPR di bawah 0.50 | SOPR KB v1.4 |
| 3 | Total Supply in Profit di bawah 50%, DAN STH profit di bawah 10% | Supply KB v1.4 |
| 4 | Price/CVDD di bawah 1.10 — harga mendekati batas bawah paling ekstrem dalam sejarah data | Price Level KB v1.4 |

- 0–1 dari 4: Belum beli. Pantau saja.
- 2 dari 4: DCA ringan — 15% dari cash pool per bulan + income langsung masuk
- 3 dari 4: DCA lebih agresif — 25% dari cash pool per bulan + income langsung masuk
- 4 dari 4: DCA maksimal — 35% dari cash pool per bulan + income langsung masuk

**Cash pool K4 = dua sumber:**
- Cash awal dari hasil K1 + close short K3 → dibagi ke tranche bulanan sesuai confidence
- Active income yang masuk selama K4 → langsung deploy sesuai confidence saat itu, tidak perlu tunggu jadwal

**Flag ekstrem:** Kalau Price/CVDD menyentuh atau turun di bawah 1.0 (terjadi hanya 2 hari dalam 10 tahun data) → boleh deploy sekaligus 50% dari sisa cash pool di hari itu.

**K4 selesai:**
- Signal D muncul: harga naik melewati STH RP dan bertahan ≥3 hari → masuk Z1b, mode wrap-up. Selesaikan sisa alokasi yang belum masuk.
- STH RP cross naik melewati RP (masuk Z2) → K4 selesai, K5 mulai.

---

## K5 — Deploy Loan di Awal Bull

**Kapan berlaku:** STH RP sudah cross ke atas RP sampai harga cross ke atas AVIV Upper bertahan ≥3 hari. Kalau K3 Stage 2 sudah aktif, K5 tidak berlaku.

**Cara masuk:** Tunggu pullback ≥5% dari high lokal. Tidak ada masuk tanpa pullback. Pullback ≥5% = mulai perhatikan, belum beli.

**Staging dalam satu pullback:**

| Kondisi | Deploy |
|---------|--------|
| Pullback ≥5% saja | Tidak ada aksi |
| + F&G turun ke bawah 50 | Deploy 50–60% dari kapasitas yang tersisa |
| + STH Loss ≥50% atau min(aSOPR, STH-SOPR) ≤ 0.98 | Deploy 70–80% |
| + keduanya terpenuhi | Deploy 100% |

Target: habiskan kapasitas dalam satu pullback. Pullback berikutnya kemungkinan harga sudah lebih tinggi — tidak perlu aksi lagi.

**LTV:** Maksimal 52% di semua kondisi. Tidak bergerak meski kondisi sempurna.

**Kalau harga turun setelah loan masuk:** Staged cut sama dengan K2 — LTV 58–60% mulai kurangi, LTV 65% jual collateral tanpa tunggu analisis apapun.

**Kalau tidak ada pullback ≥5% sepanjang Z2/Z3:** Tidak masuk loan. Tetap pegang BTC dari K4 tanpa leverage.

**K5 selesai:** Harga cross ke atas AVIV Upper, bertahan ≥3 hari → K5 tutup, K6 mulai.

---

## K6 — Kurangi Loan saat Harga Terlalu Jauh dari Entry

**Kapan berlaku:** Selama di Z2 atau Z3. Bisa terjadi berkali-kali.

**Trigger:** Harga membentuk local high baru yang lebih tinggi dari local high sebelumnya.

Definisi local high: harga lebih tinggi dari 5 hari sebelum dan 5 hari sesudahnya.

**Aksi:** Bayar sebagian loan sampai LTV turun 10 poin dari posisi saat itu.

Contoh: LTV 50% saat K6 muncul → bayar loan sampai LTV 40%.

**K6 selesai:** Harga cross ke atas AVIV Upper bertahan ≥3 hari → masuk Z4, K6 tidak berlaku lagi.

**Catatan:** Hit rate 58–62% dari data historis (n=20, 2 siklus). Sekitar 4 dari 10 signal tidak diikuti koreksi ≥5% — artinya kamu mungkin bayar loan lebih awal padahal harga terus naik. Ini diterima karena tujuan K6 bukan profit maksimal, tapi jaga ruang napas LTV di fase early bull.

---

## URUTAN SIKLUS PENUH

```
Z5 (harga di atas AVIV Upper)
  → K1: lunasi loan, jual 20-30% BTC → cash

Tanda-tanda lower high / bear onset
  → K3 Stage 1: waspada, pantau sinyal kedua
  → K3 Stage 2: buka short 30% dari sisa BTC

Harga turun ke Z1 (di bawah STH RP, ordering terbalik)
  → K4: akumulasi agresif dengan cash + income
  → Exit K3 short

Signal D muncul (harga cross STH RP, bertahan ≥3 hari)
  → Z1b: wrap-up sisa DCA

STH RP cross naik melewati RP
  → Z2: K5 mulai, tunggu pullback untuk masuk loan

Harga naik ke Z3 (RP sampai AVIV Mean)
  → K5 masih aktif
  → K6: kurangi loan 10 poin LTV setiap local high baru terbentuk

Harga cross ke atas AVIV Upper, bertahan ≥3 hari
  → Z4: K6 selesai
  → Pantau untuk K1/K2 berikutnya
```

---

## HARD LIMITS LTV

Berlaku di semua kondisi, tidak ada sinyal on-chain yang bisa override ini.

| LTV | Yang dilakukan |
|-----|----------------|
| 52% | Batas atas saat deploy. Tidak boleh dilewati |
| 55% | Batas absolut tertinggi — hanya kalau ada dana top-up yang sudah pasti cair |
| 58–60% | Mulai jual collateral, bawa LTV balik ke 53–54% |
| 62–63% | Jual lebih besar, target 55% |
| 65% | Jual besar sekarang, target di bawah 50% |

Komitmen keras: LTV 60% = jual collateral dan bayar loan sekarang. Tidak perlu analisis. Tidak perlu tunggu.

---

## CATATAN DATA & SAMPLE SIZE

Semua threshold dan pola di framework ini dibangun dari 2–3 siklus historis (2017, 2019, 2021, 2023). Sample sangat kecil. Treat semua angka sebagai panduan arah, bukan aturan presisi. Kalau kondisi di siklus berikutnya berbeda signifikan dari historis, framework harus ditinjau ulang.

Sumber data: ChartInspect.com (Glassnode). Semua angka KB v1.4.
