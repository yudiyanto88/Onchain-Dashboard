# Framework Investasi BTC — Ringkasan Eksekusi
*Versi 2.0 (18 Jul 2026). Basis: v1.1 + hasil review framework Jul 2026 (research/findings/findings_framework_review_metrics_thresholds_2026-07-17.md + research/framework_review_2026-07/). Status: AKTIF — menggantikan v1.1. Catatan: backtest mesin utuh vs HODL/DCA masih pending (lihat § Governance butir 4); sampai selesai, treat semua angka sebagai panduan arah.*

**Ringkasan perubahan besar dari v1.1:**
1. Zona ditulis ulang: dua dimensi (struktur ordering × posisi harga) — tidak ada lagi hari tanpa zona atau dobel-zona. Zona baru: ZC (capitulation) dan ZD (dip dalam).
2. Dua definisi "bear terkonfirmasi": versi PRESISI (untuk K3 short) dan versi CEPAT (untuk aturan sisi-beli).
3. K2 dirombak: sistem 5 kondisi + confidence tier DIGANTI struktur gate + veto. Kondisi #1 lama dihapus (terbukti mati secara matematis).
4. Loan K2: cap 45% saat entry, top-up pasca bullish cross maksimal LTV gabungan 48%.
5. Loan K5: cap turun dari 52% ke 45%. Agresivitas diekspresikan lewat kecepatan deploy, bukan tinggi LTV.
6. K4 dapat dua jalur baru: K4-tanpa-Z1 dan lantai waktu.
7. Level jual tangga LTV dipasang sebagai order siap-eksekusi di platform, bukan keputusan manual.

---

## 0. STATUS PASAR (baru di v2)

Setiap hari, tentukan dulu status pasar. Status menentukan aturan mana yang hidup.

**Alarm bear CEPAT (untuk aturan sisi-beli: K4-tanpa-Z1, guard K2):**
Pool 4 sinyal — bunyi kalau 2 dari 4 nyala (dalam window pairing 90 hari):
1. Harga turun dari Z5 menembus AVIV Upper ke bawah (setelah ≥7 hari di Z5)
2. Gap MA90−MA60 STH-SOPR memuncak lalu turun ≥14 hari berturut
3. MVRV Momentum bearish cross: SMA30(MVRV Ratio) memotong ke bawah SMA30-dari-SMA30-nya, bertahan ≥7 hari
4. MVRV Ratio close di bawah SMA180-nya ≥7 hari, DAN kunjungan Z5 terakhir ≤~120 hari

Karakter: sigap (Okt 2025: +4 hari setelah peak) tapi bisa salah bunyi di koreksi yang recover (Mei 2021). Biaya salah bunyi di sisi beli = cuma pause — bisa diterima.

**Alarm bear PRESISI (khusus K3 short):**
Hanya sinyal 1 + 2 (dua-duanya harus muncul), PLUS syarat awal: MVRV dan aSOPR diminishing di setiap ATH baru, PLUS K1 sudah selesai. Salah bunyi di short = rugi nyata, jadi sengaja lambat.

**Status bear berakhir (unlock):** STH RP cross naik melewati RP (masuk Z2) — BUKAN saat harga balik ke Z5. *(⚠ pending validasi backtest final — perbaikan atas lubang Sep 2018, lihat findings_k2_loan_policy.md)*

---

## 1. ZONE STRUCTURE v2

Dua dimensi. Setiap hari punya tepat satu label.

**Dimensi 1 — STRUKTUR (ordering level):**
- N = Normal: STH RP > RP
- C = Konvergen: jarak STH RP–RP dan RP–LTH RP keduanya < 2%
- T = Terbalik: STH RP < RP

**Dimensi 2 — POSISI HARGA** (relatif ke level, urut dari bawah).

| Struktur | Posisi harga | Zona | K aktif |
|----------|-------------|------|---------|
| N | P < RP | **ZC — Capitulation** | K3 pegang (kalau short aktif); K4-tanpa-Z1 / lantai waktu bila syaratnya nyala; selain itu TUNGGU — jangan deploy |
| N | RP ≤ P < STH RP | **ZD — Dip dalam** | K2 (kalau status bull) / tunggu (kalau alarm cepat bunyi) |
| N | STH RP ≤ P < AVIV Mean | **Z3** | K5 (kalau naik dari bawah, status bull) / K2 (kalau dip dari atas) / tunggu (status bear) |
| N | AVIV Mean ≤ P < AVIV Upper | **Z4** | K6 (dari bawah) / K2 (dip dari Z5) / K1 (trigger turun dari Z5) |
| N / C / T | P ≥ AVIV Upper | **Z5** | K1 / K2 ke Z4. *(Historis 2011–2026: seluruh 703 hari Z5 terjadi di struktur N; C/T dicantumkan hanya supaya tabel lengkap — tidak boleh ada kombinasi tanpa label)* |
| T | P < STH RP | **Z1 — Bear bottom** | K4 |
| T | STH RP ≤ P < RP | **Z1b** | K4 wrap-up |
| T | P ≥ RP | **Z2-transisi** (jarang, sebentar) | K5 bersiap |
| C | P < AVIV Mean | **Z2 — Konvergensi** | K5 mulai. Kalau bentrok label dengan Z1/Z1b: Z2 menang (K5 > K4) |
| C | AVIV Mean ≤ P < AVIV Upper | Z4 | K6 |

Level: STH RP = modal rata-rata holder <155 hari · RP = Realized Price · LTH RP = modal holder >155 hari · AVIV Mean & Upper (+0.5 SD) · CVDD = flag ekstrem dalam Z1 (Price/CVDD < 1.0 = langka sekali).

Kenapa ZC penting: di v1.1, 300 hari historis (Nov 2018, Mar 2020, Jun & Sep 2022, dst — justru fase capitulation) tidak punya zona sama sekali, dan bear 2025-26 berlabel "Z3/K5 aktif" 8 bulan. v2 menutup dua-duanya.

---

## K1 — Kurangi Posisi di Puncak Siklus

*(Tidak berubah dari v1.1, kecuali koreksi teks di catatan K3.)*

**Kapan relevan:** Harga pernah bertahan di Z5 minimal 14 hari dalam siklus ini.

**Dua syarat awal:** MVRV di setiap ATH baru lebih rendah dari ATH sebelumnya; aSOPR juga. Kalau belum terpenuhi, K1 tidak perlu dipikirkan.

**5 sinyal peringatan:** (1) MVRV turun di setiap ATH baru; (2) aSOPR turun di setiap ATH baru; (3) harga di atas STH RP tapi STH-MVRV mendekati 1.0; (4) gap MA90−MA60 STH-SOPR memuncak dan mulai turun; (5) Supply in Profit >90% dan mulai turun.

Catatan baca signal #1 (Z-Score rolling sebagai alat bantu visual) dan confirming context F&G SMA30: sama dengan v1.1.

**Trigger eksekusi — OR gate:** harga turun dari Z5 ke Z4 ATAU gap MA90−MA60 STH-SOPR memuncak dan turun ≥14 hari. Mana duluan = eksekusi sekarang.

**Aksi:** lunasi semua loan → 0; jual 20–30% BTC → USDT.

**Catatan:** window sinyal→deadline menyempit antar siklus (~30 hari di 2017 → bisa 6 hari di 2025). Jangan tunda.

---

## K2 — Masuk di Bull Dip (DIROMBAK di v2)

**Kapan berlaku:** Status bull (alarm cepat tidak bunyi), harga di ZD / Z3 / Z4 setelah dip. Episode dibuka oleh MVRV Momentum bearish cross (sama dengan v1.1).

### Struktur baru: GATE → VETO → MASUK. Bukan hitung-hitungan 5 kondisi lagi.

**Dua GATE (dua-duanya harus terbuka):**
1. **Gate valuasi:** STH-MVRV di band **0,80–0,97** (holder baru rugi 3–20% — diskon sehat; di bawah 0,80 = wilayah bear, bukan K2)
2. **Gate perilaku:** STH-SOPR < 0,97 belum bertahan >14 hari, DAN aSOPR > 0,95

**Tiga VETO (satu saja nyala = jangan masuk, apapun kata gate):**
1. Supply in Profit ≤ 60% — kerusakan pasar sudah meluas
2. LTH profit share turun >2 poin di bawah rata-rata 30 harinya — holder lama ikut berdarah
3. **Sinyal penghenti:** MVRV Ratio < SMA180-nya ≥7 hari DAN kunjungan Z5 terakhir ≤~120 hari — koreksi ini kemungkinan bukan bull dip. (Peran sinyal ini = penghenti pembelian; JANGAN dipakai sebagai konfirmasi bear — dua pekerjaan berbeda, dia cuma jago yang pertama. Lihat findings_bear_confirmed_v2_mvrv.md)

**Pengubah ukuran (bukan pembuka pintu):**
- Funding rate < 0 saat pintu terbuka → tranche boleh diperbesar (data 2020+, n efektif 31 episode — flag)
- F&G < 30 → BUKAN lampu hijau, artinya kelas dip dalam: periksa gate & veto lebih ketat
- Bounce AVIV Mean ≤4 hari / bullish cross → konfirmasi post-hoc, membuka penyelesaian sisa kapasitas

**Kondisi #1 lama (rasio LTH/STH-MVRV) DIHAPUS** — terbukti mati secara matematis: rasionya identik dengan rasio cost-basis, harga saling coret; nyala 6 hari dari 1.790 hari dip (findings Temuan 3a).

### Cash (sama dengan v1.1)

Sejak bearish cross (episode terbuka, alarm cepat belum bunyi, harga di atas RP): pembelian bertahap cash boleh mulai — 25–30% cash K2 per pembelian, jarak ~2 minggu ATAU tiap turun ~7%, mana duluan. Cash tidak punya risiko LTV.

### Loan (keputusan 18 Jul 2026)

- **Entry:** gate + veto semua bersih → loan masuk, **cap LTV 45%**
- **Top-up:** setelah MVRV Momentum bullish cross terkonfirmasi (≥7 hari) DAN gate/veto/penghenti masih bersih → boleh tambah loan **inkremental**, LTV gabungan maksimal **48%** — TIDAK PERNAH 52%. Alasan: di 48%, cut-loss sadar (−20%) masih mendahului aturan wajib-jual LTV-60 (yang bunyi di −20% untuk cap 48%, tapi di −13% untuk cap 52%). Di 52%, sistem menjualmu sebelum kamu memutuskan — mekanisme Okt 2025. (findings_k2_loan_policy.md: usulan 52% ditolak — kena aturan-60 melonjak 17%→50%)
- **DILARANG:** entry loan hanya-di-cross tanpa gate dip (kebijakan terburuk yang diuji — worst case likuidasi total Apr 2022)

### Penutupan episode

Bullish cross terkonfirmasi → koreksi selesai, sisa kapasitas boleh diselesaikan. Alarm bear cepat bunyi → episode gugur, semua pembelian berhenti, kelola posisi via staged cut.

### Kalau salah — staged cut (order SIAP-PASANG di platform, bukan manual)

| LTV | Aksi |
|-----|------|
| 58–60% | Jual collateral, LTV balik ke 53–54% |
| 62–63% | Jual lebih besar, target 55% |
| 65% | Jual besar, target <50% |

LTV 60% = jual sekarang, tanpa analisis. Cut-loss: −20% dari entry → jual collateral, bayar sebagian besar loan, target LTV <50%. Alasan order siap-pasang: 92 kejadian historis harga turun ≥13% dalam ≤3 hari — tangga bisa dilompati satu candle.

---

## K3 — Short/Hedge saat Bear Mulai

*(Mekanika tidak berubah; definisi konfirmasi = alarm PRESISI; koreksi teks.)*

**Kapan relevan:** setelah K1 selesai, loan nol. Syarat awal: MVRV & aSOPR diminishing per ATH (sama K1).

**Stage 1:** salah satu dari sinyal 1 / sinyal 2 (lihat § 0) muncul → waspada, tidak ada aksi.
**Stage 2:** sinyal satunya ikut muncul → buka short 30% dari BTC yang dipegang.

**Koreksi teks v1.1:** klaim "AVIV cross duluan 45–68 hari di 2017 & 2021" TIDAK reproduce dengan formula AVIV resmi — urutannya terbalik (GAP duluan; jarak 61 & 42 hari benar, labelnya kebalik). OR-gate menyerap ini, klaim naratifnya dikoreksi.

**Sinyal MVRV (C & D) = confirming context SAJA untuk K3, DILARANG masuk gate** — diuji: memasukkannya tidak menghapus false positive Mei 2021, malah mempercepatnya (findings_bear_confirmed_v2_mvrv.md).

**Exit short:**

| Kondisi | Aksi |
|---------|------|
| 4 hari close di atas AVIV Mean, harga masih di bawah STH RP | Kurangi short |
| Harga balik ke Z5 dan bertahan | Tutup penuh — K3 baca salah |
| K4 mulai aktif (termasuk K4-tanpa-Z1) | Tutup short, mode akumulasi |
| Lantai waktu mulai aktif | Kurangi short bertahap → tutup, baru DCA lantai jalan |

**Risiko yang diterima secara sadar:** false positive tipe Mei 2021 tidak bisa dihilangkan sinyal manapun yang diuji. Pengamannya = syarat awal + K1-selesai + sizing 30% (bukan lebih).

---

## K4 — Akumulasi di Bear Bottom (+2 jalur baru)

**Jalur utama (sama dengan v1.1):** Z1 aktif → hitung 4 kondisi: (1) LTH-MVRV <1.0; (2) aSOPR <0,93 ≥7 hari DAN LTH-SOPR <0,50; (3) Supply in Profit <50% DAN STH profit <10%; (4) Price/CVDD <1,10.
0–1: pantau · 2: DCA 15%/bulan · 3: DCA 25%/bulan · 4: DCA 35%/bulan (+ income langsung masuk). Flag ekstrem Price/CVDD ≤1,0 → deploy 50% sisa cash hari itu. Confirming context (F&G SMA30 divergence, MVRV bullish cross saat Z1): sama v1.1.

**Jalur baru 1 — K4-tanpa-Z1:** count ≥3 DAN alarm bear CEPAT sudah bunyi → K4 boleh aktif walau ordering belum terbalik (walau belum Z1). Menyelamatkan kasus 2020: count sempat 3/4 tapi Z1 tidak pernah terbentuk → framework diam dari $5k ke $60k (findings Temuan 4b).

**Jalur baru 2 — Lantai waktu:** ≥9 bulan sejak cycle peak DAN close < RP → DCA otomatis **5% cash pool/bulan** berjalan walau count <2. **Spot only — tidak pernah menyentuh loan/LTV.** Stop: Signal D (harga > STH RP ≥3 hari). Tervalidasi 3/3 bear searah; beli rata-rata +8–18% di atas hari-hari izin K4 tapi 10–15× lebih banyak hari deploy; worst case beli pertama 2014 masih turun −46% — karena itu 5% (bukan 10%) supaya ada cadangan double-bottom (findings_time_floor_validation.md).

**K4 selesai:** Signal D → Z1b wrap-up; STH RP cross naik RP → Z2, K5 mulai.

---

## K5 — Deploy Loan di Awal Bull

**Kapan berlaku:** STH RP cross ke atas RP, sampai harga cross AVIV Upper ≥3 hari. K3 Stage 2 aktif → K5 tidak berlaku.

**Cara masuk:** tunggu pullback ≥5% dari high lokal. Staging sama v1.1: +F&G<50 → 50–60% kapasitas; +STH Loss ≥50% atau min(aSOPR, STH-SOPR) ≤0,98 → 70–80%; keduanya → 100%. Target: habiskan kapasitas dalam satu pullback — **agresivitas = kecepatan deploy, bukan tinggi LTV.**

**LTV: maksimal 45%** (turun dari 52). Alasan: di jendela K5 historis, cap 52% kena aturan wajib-jual LTV-60 di 23% deployment; cap 45% = 1,4% — risiko turun 16× dengan loan hanya ~13% lebih kecil. Sumber risikonya koreksi 15–30% yang RUTIN di setiap early bull, bukan crash langka (findings Temuan 2 + Addendum A).

**Kalau tidak ada pullback ≥5%:** tidak masuk loan. Staged cut & cut-loss: sama K2.

**K5 selesai:** harga cross AVIV Upper ≥3 hari → K6 (di Z2/Z3) selesai juga saat itu.

---

## K6 — Kurangi Loan saat Harga Jauh dari Entry

*(Tidak berubah.)* Di Z2/Z3, setiap local high baru (lebih tinggi dari 5 hari sebelum & sesudah) → bayar loan sampai LTV turun 10 poin. Sumber dana: **cash/income, bukan jual BTC** — kalau tidak ada, tunggu local high berikutnya. Hit rate 58–62% (n=20) — diterima, tujuannya ruang napas, bukan profit.

---

## URUTAN SIKLUS PENUH v2

```
Z5 → K1: lunasi loan, jual 20–30%
Alarm presisi Stage 1 → waspada · Stage 2 → K3 short 30%
Harga tembus ke bawah RP, ordering masih normal → ZC (capitulation):
   K3 pegang · alarm cepat + count≥3 → K4-tanpa-Z1 (tutup short, mulai beli)
   · ≥9 bulan + P<RP → lantai waktu (kurangi short dulu)
Ordering terbalik → Z1: K4 penuh
Signal D → Z1b wrap-up
STH RP cross RP → Z2: status bear DIBUKA, K5 mulai (cap 45%)
Z3: K5 aktif + K6 tiap local high · K2 di dip (gate+veto, loan 45→48)
Cross AVIV Upper ≥3 hari → Z4 → pantau K1/K2 berikutnya
```

---

## HARD LIMITS LTV

Tidak berubah, tidak bisa di-override sinyal apapun:

| LTV | Aksi |
|-----|------|
| 45% | Batas deploy K2 entry & K5 |
| 48% | Batas absolut top-up K2 pasca-cross (LTV gabungan) |
| 52% | Batas atas warisan — TIDAK dipakai lagi untuk deploy baru |
| 55% | Batas absolut, hanya dengan dana top-up pasti cair |
| 58–60% | Jual collateral → 53–54% |
| 62–63% | Jual lebih besar → 55% |
| 65% | Jual besar sekarang → <50% |

LTV 60% = jual sekarang. Order tangga dipasang di muka di platform.

---

## GOVERNANCE (baru di v2)

1. **Protokol usulan sinyal baru (4 lapis):** threshold a priori tanpa grid search → independensi dari gate yang ada (|phi|<0,3) → uji inkremental (masih memisahkan hasil SETELAH gate nyala?) → konsistensi arah antar era. Gagal satu lapis = tolak. (Addendum 2 findings review)
2. Framework dibekukan per siklus; sinyal baru masuk daftar tunggu, naik kelas hanya lewat protokol di atas + data forward.
3. Semua threshold = panduan arah dari 3–4 siklus, bukan presisi. Jangan eksekusi karena selisih tipis di batas — data provider bisa revisi.
4. **Pending sebelum v2 final:** (a) backtest mesin utuh vs HODL/DCA — ujian kelulusan; (b) validasi unlock-bear-di-Z2 (tambalan lubang Sep 2018); (c) catatan rekonsiliasi count 11-vs-16 di KB MVRV § 6C.2.

Sumber data: ChartInspect.com (Glassnode). Basis: KB v1.4 + findings review Jul 2026.
