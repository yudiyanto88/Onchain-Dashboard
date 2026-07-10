# MVRV Z-Score Rolling Window — Divergensi Price vs Z-Score (K1)

**Tanggal sesi:** 2026-07-10
**Fokus:** K1 (signal exhaustion/topping cycle)
**Tools:** Tab "MVRV Z-Score Lab" (app.py) — cumulative window & rolling 1-year window
**Formula:** `Z = (MVRV_ratio − rolling_mean(MVRV_ratio)) / rolling_std(MVRV_ratio)`, `min_periods=30`

---

## 1. Observasi awal user (cumulative window, all-time)

Dari chart MVRV Z-Score dengan window cumulative (all-time), user mengamati garis merah (trendline manual) di price panel dan Z-score panel:

- Periode **Juli–Oktober 2025**: price jelas bikin **higher high**, tapi MVRV Z-score turun bentuk **lower high** terus.
- Local top **Maret 2024**: tidak kelihatan sebagai divergensi karena price juga **lower high** dan MVRV Z-score juga **lower high** (dua-duanya turun bareng, no divergence).
- **Januari 2025**: ada sedikit price **higher high**, tapi MVRV Z-score **lower high**.

## 2. Validasi numerik — cumulative window

Dihitung ulang pakai formula persis dari tab (`expanding()` window, dari 2010):

| Local top | Tanggal | Price | Z-Score |
|---|---|---|---|
| Mar 2024 ATH | 13-Mar-24 | $73,095 | **1.136** |
| Post-ATH corrective high | 05-Jun-24 | $71,119 (LH) | 0.661 (LH) — *tidak divergen, dua-duanya turun* |
| Dec 2024 high | 17-Dec-24 | $106,169 (HH) | 1.058 |
| Jan 2025 ATH | 21-Jan-25 | $106,188 (HH tipis) | **0.862 (LH)** |
| Jul-Oct 2025 top | 06-Oct-25 | $124,715 (HH jelas) | **0.564–0.723 (LH)** |

Cocok persis dengan narasi user: Mar 2024→Jun 2024 dua-duanya lower high (no divergence), lalu tiga local top berturut-turut sejak itu (Dec2024→Jan2025→Jul-Oct2025) semua price higher high tapi Z-score lower high — 3x divergensi beruntun dalam satu cycle yang sama.

### Cross-check ke cycle sebelumnya (cumulative window)

| Cycle | Transisi | Price | Z-Score | Hasil |
|---|---|---|---|---|
| 2013 double top | Apr → Nov | $231 → $1,156 (HH) | 3.05 → 2.65 | LH ✓ divergen |
| 2017 | Jun → Sep | $2,977 → $4,901 (HH) | 1.86 → 1.31 | LH ✓ divergen |
| 2017 (blow-off) | Sep → Dec | $4,901 → $19,538 (HH) | 1.31 → 2.54 | **HH ✗ tidak divergen** |
| 2021 double top | Apr → Nov | $63,551 → $67,525 (HH) | 1.77 → 1.12 | LH ✓ divergen |

**Kesimpulan cumulative:** Pola "price HH, Z-score LH" valid di n=4 cycle (memenuhi syarat minimum framework), memperkuat K1 signal #1 dengan granularitas intra-cycle. Tapi ada 1 pengecualian penting: leg blow-off final 2017 (Sep→Dec) — Z-score ikut re-accelerate bareng price di fase parabolic, sinyal divergensi hilang justru di titik paling kritis.

---

## 3. Rolling window 1 tahun — struktur lebih jelas

User meminta fokus ke rolling window 1 tahun untuk memperjelas divergensi, dari sisi struktur **price vs MVRV Z-score**:

- Local top **Mar 2024 → Jan 2025 → cycle peak Jul-Oct 2025**: price jelas **higher high**, tapi MVRV Z-score jelas **lower high**.
- Bull dip **Jul-Aug 2024 → Mar-Apr 2025**: price **higher low**, tapi MVRV Z-score **lower low**.

### Validasi numerik — TOPS (rolling 1Y)

| Local top | Price | Z (1Y) |
|---|---|---|
| Mar 2024 | $73,095 | **3.255** |
| Jan 2025 | $106,188 (HH) | **1.237** (LH) |
| Jul-Oct 2025 | $124,715 (HH) | **0.290** (LH) |

### Validasi numerik — DIPS (rolling 1Y)

| Bull dip | Price | Z (1Y) |
|---|---|---|
| Aug 2024 | $53,998 | **-0.795** |
| Apr 2025 | $76,270 (HL) | **-1.761** (LL) |

Struktur user terkonfirmasi 100% — price bikin higher high di top dan higher low di dip, tapi Z-score konsisten bikin lower high dan lower low di dua-duanya. Pola ini jauh lebih bersih/monoton dibanding versi cumulative.

### Decomposisi — genuine vs artifak mekanik window

Z didekomposisi jadi `(MVRV_raw − RollMean) / RollStd` untuk cek apakah pola ini genuine atau sebagian cuma efek rolling window:

| Titik | MVRV raw | RollMean(1Y) | RollStd(1Y) | Z |
|---|---|---|---|---|
| TOP Mar 2024 | 2.745 | 1.621 | 0.345 | 3.255 |
| TOP Jan 2025 | 2.523 | 2.203 | 0.259 | 1.237 |
| TOP Jul-Oct 2025 | 2.285 | 2.227 | 0.201 | 0.290 |
| DIP Aug 2024 | 1.715 | 1.987 | 0.342 | -0.795 |
| DIP Apr 2025 | **1.742** | 2.161 | 0.238 | -1.761 |

**Temuan penting:** Di sisi dip, MVRV ratio raw Apr 2025 (1.742) justru **sedikit lebih tinggi** dari Aug 2024 (1.715) — bukan lebih rendah. Tapi Z-score jauh lebih negatif (-1.761 vs -0.795), murni karena RollMean bergeser naik (window "mengejar" level harga makin tinggi selama bull run) dan RollStd menyusut (volatility compression). **Divergensi di sisi dip sebagian besar artifak mekanik rolling window, bukan cerminan stress on-chain yang benar-benar lebih dalam.**

Di sisi top, MVRV raw memang genuinely turun tiap puncak (2.745→2.523→2.285, konsisten dengan diminishing-peaks yang sudah established) — jadi ini genuine, walau tetap diperkuat tambahan oleh RollMean yang naik (efek mekanik searah).

**Kesimpulan:** Sisi TOP (price HH/Z LH) valid dipakai sebagai confirming K1 — kombinasi genuine diminishing MVRV + efek window searah, tidak saling kontradiksi. Sisi DIP (price HL/Z LL) **jangan dipakai** sebagai sinyal terpisah karena mayoritas cuma efek rolling-window, bukan sinyal on-chain riil.

## 4. Cross-check pola TOP (rolling 1Y) ke cycle sebelumnya

| Transisi | Price | Z (1Y) | Pattern |
|---|---|---|---|
| 2013: Apr → Nov | $231 → $1,156 (HH) | 4.384 → 2.895 | **LH ✓ divergen** |
| 2017: Jun → Sep | $2,977 → $4,901 (HH) | 3.407 → 1.591 | **LH ✓ divergen** |
| 2017: Sep → Dec (blow-off) | $4,901 → $19,538 (HH) | 1.591 → 3.308 | **HH ✗ tidak divergen** |
| 2021: Apr → Nov | $63,551 → $67,525 (HH) | 1.561 → 0.448 | **LH ✓ divergen** |
| 2024: Mar → Jan'25 | $73,095 → $106,188 (HH) | 3.255 → 1.237 | **LH ✓ divergen** |
| 2025: Jan → Jul-Oct | $106,188 → $124,715 (HH) | 1.237 → 0.290 | **LH ✓ divergen** |

**Hit rate: 5/6 transisi (83%) di 4 cycle berbeda** — memenuhi syarat sample minimum framework sendiri (≥3-4 cycle). Pola "price HH, Z-score(1Y) LH" konsisten sebagai sinyal exhaustion/divergensi intra-cycle.

**Satu-satunya exception:** 2017 Sep→Dec — leg blow-off parabolic terakhir sebelum ATH final. Raw MVRV-nya naik dari 3.118→4.387 (bukan cuma mekanik window — MVRV ratio genuinely melonjak, buying frenzy asli). Jadi pengecualiannya bukan noise, ada penjelasan struktural: kalau leg terakhir menuju cycle top benar-benar parabolic/blow-off, sinyal divergensi ini bisa gagal justru di titik paling kritis (top yang sebenarnya).

**Decomposisi genuine vs mekanik (5 kasus yang divergen):** penurunan Z didorong kombinasi (a) raw MVRV ratio yang genuinely turun tiap puncak (fenomena diminishing-peaks yang sudah established) + (b) RollMean yang naik karena window mengejar level harga baru (efek mekanik, searah memperkuat). Di kasus exception (2017 blow-off), efek (a) berbalik arah (MVRV genuinely naik) dan cukup kuat mengalahkan (b).

---

## 5. Kesimpulan untuk K1

Pola price-HH/Z-LH (rolling 1Y) solid dipakai sebagai confirming signal exhaustion intra-cycle (5/6 cycle, n=4 cycle), dengan catatan eksplisit: **tidak reliable untuk memanggil top yang persis** kalau kondisi pasar sedang di fase parabolic/blow-off (volume/momentum ekstrem), karena preseden 2017 nunjukkin sinyal bisa gagal tepat di situ. Cocok dipakai sebagai warning "cycle mulai capek" secara umum, bukan trigger presisi timing top.

Sisi dip (price HL/Z LL) tidak direkomendasikan sebagai sinyal K5/dip-entry terpisah — mayoritas artifak mekanik rolling window (RollMean naik + RollStd menyusut), bukan sinyal on-chain genuine, terbukti dari raw MVRV yang justru flat/naik tipis di dip Apr 2025 dibanding Aug 2024.

---

## 6. Belum diselesaikan / next step

- Belum dicari indikator pengganti untuk sisi dip (K5) yang bebas dari artifak rolling-window mekanik.
- Belum ditest apakah pola ini juga berlaku untuk siklus 2011 (single spike top, tidak ada struktur multi-local-top untuk dibandingkan) atau 2019 mini-cycle (top Jun 2019).
- Perlu dibawa ke Claude.ai project untuk interpretasi lebih dalam sebelum revisi Decision Framework — terutama soal bagaimana K1 signal #1 sebaiknya direvisi untuk menangkap granularitas intra-cycle ini tanpa kehilangan awareness soal exception blow-off.
