# aSOPR SMA30 / SMA365 Crossover — Findings Summary

**Disiapkan:** Juni 2026  
**Konteks:** Analisis sinyal aSOPR (Adjusted SOPR) menggunakan crossover SMA30 vs SMA365 untuk integrasi ke Signal Framework v1.0.3

---

## Temuan Utama

### Dua tipe crossover UP yang berbeda

Dari total 34 crossover UP (SMA30 melintasi naik SMA365) sejak 2012, terbagi menjadi dua karakter yang fundamentally berbeda berdasarkan satu filter: **level SMA30 saat crossover terjadi**.

---

## Tipe 1 — PRE-DETECTION Signal (SMA30 < 1.0 saat crossing)

**Definisi:** SMA30 masih di bawah 1.0 saat melintasi SMA365 ke atas. Artinya aSOPR masih dalam kondisi tertekan (rata-rata transaksi 30 hari masih rugi) — ini adalah tanda genuine bear market recovery.

**Events yang teridentifikasi:**

| Date | Price | SMA30 | Supply% | Zone Framework |
|------|-------|-------|---------|----------------|
| 2015-03-11 | $297 | 0.9843 | 58.7% | HIJAU |
| 2015-04-07 | $254 | 0.9837 | 49.1% | HIJAU TUA (BB1) |
| 2015-05-15 | $238 | 0.9826 | 47.5% | HIJAU TUA (BB1) |
| 2015-06-16 | $252 | 0.9771 | 54.4% | HIJAU |
| 2016-02-14 | $408 | 0.9968 | 73.7% | HIJAU |
| 2019-03-06 | $3,916 | 0.9779 | 56.9% | BIRU (PD1) |
| 2023-01-21 | $22,779 | 0.9840 | 70.0% | HIJAU |
| 2023-08-26 | $26,033 | 0.9932 | 58.7% | BIRU (PD1) |
| 2023-09-17 | $26,538 | 0.9939 | 62.5% | BIRU (PD1) |

**Gap vs Pre Detection events yang ditandai:**

| Cycle | PD Event | aSOPR Crossover | Gap |
|-------|----------|-----------------|-----|
| 2019 | Feb 22 (Ref) → Mar 21–26 (Main) | Mar 6 | +12 hari setelah Ref, **15 hari sebelum** konfirmasi utama |
| 2023 | Jan 10–12 | Jan 21 | **+11 hari setelah** PD window |

**Kesimpulan Tipe 1:**
- Bukan early warning — ini **confirming signal**, fire ~10–15 hari setelah pre-detection period dimulai oleh metrik lain
- Posisi di framework: **PD1 trigger tambahan (trigger ke-4 atau ke-5)**, bukan trigger pertama
- Metrik yang lebih early: MVRV dan STH-MVRV (keduanya drop signifikan lebih dulu)
- Filter yang tepat: `SMA30 ≤ 1.00` saat crossover untuk validasi genuine pre-detection

---

## Tipe 2 — MID-BULL Recovery Signal (SMA30 > 1.0 saat crossing)

Dibahas terpisah. Lihat bagian "Clean Mid-Bull Crossovers" di dokumen framework.

---

## Implikasi untuk Signal Framework

### Integrasi ke PD1

Trigger kandidat tambahan untuk PD1 (zona BIRU, Supply 50–65%):

> **aSOPR SMA30 cross UP SMA365, dengan SMA30 ≤ 1.00 saat crossover**

- Bobot: 1 dari 5 trigger PD1
- Karakteristik: confirming trigger, bukan leading
- Valid: crossover harus sustained (tidak langsung cross DOWN dalam 7 hari)

### Threshold filter (dari sesi analisis sebelumnya)

| Tipe | Filter Level | Interpretasi |
|------|-------------|--------------|
| Pre-detection valid | SMA30 ≤ 1.00 | aSOPR masih tertekan, genuine distress |
| Early recovery | SMA30 1.00–1.005 | Transisi, perlu konfirmasi metrik lain |
| Mid-bull (Tipe 2) | SMA30 > 1.01 | Konteks berbeda, bukan PD1 trigger |
