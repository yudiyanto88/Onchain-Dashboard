---
description: Bedah video on-chain end-to-end — watch, ekstrak insight, kritik skeptic, uji ke CSV, findings doc, commit & push. Berhenti sebelum menyentuh framework.
argument-hint: <url-atau-path-video> [fokus opsional]
---

# Video Breakdown Pipeline

Argumen: `$ARGUMENTS` — argumen pertama = URL/path video, sisanya (kalau ada) = fokus khusus dari Yudi (mis. "fokus ke klaim soal LTH").

Kamu adalah **orchestrator**. Jalankan 6 stage di bawah BERURUTAN. Prinsip utama: **machine proposes, Yudi disposes** — pipeline ini mengusulkan, tidak pernah mengubah framework.

Buat task list (TaskCreate) untuk 6 stage supaya progres kelihatan.

**Folder kerja:** semua artefak video breakdown hidup di `research/findings/video-breakdown/` — folder khusus, terpisah dari file riset umum lain di `research/findings/` (K3.md, sopr_*, mvrv_*, dll). Jangan tulis apapun langsung di root `research/findings/`.

---

## Stage 0 — Watch

1. Tentukan `<slug>` pendek dari judul video (kebab-case, mis. `lth-distribution-warning`)
2. Invoke skill `watch` dengan argumen video
3. Simpan transcript lengkap ke `research/findings/video-breakdown/video_<slug>/transcript.md` — sertakan header: judul video, channel, URL, tanggal video, tanggal breakdown
4. Kalau watch gagal (video private/region-lock/dll), STOP dan laporkan ke Yudi — jangan lanjut dengan transcript kosong

## Stage 1 — Ekstrak (sub-agent `insight-extractor`)

Spawn sub-agent `insight-extractor` (synchronous). Prompt harus berisi:
- Path transcript
- Fokus khusus dari Yudi (kalau ada di `$ARGUMENTS`)
- Instruksi baca `references/Decision_Framework v1.md` + `research/findings/video-breakdown/video_index.md`

Hasil: daftar klaim terklasifikasi `DUP | TESTED-BEFORE | NOVEL | OUT-OF-SCOPE`.
Kalau hasilnya 0 klaim NOVEL → langsung lompat ke Stage 4 (findings doc tetap dibuat, isinya "tidak ada yang baru").

## Stage 2 — Skeptic (sub-agent `framework-skeptic`)

Spawn sub-agent `framework-skeptic` (synchronous). Prompt harus berisi:
- Daftar lengkap kandidat NOVEL dari Stage 1 (quote + metrik + relasi yang diklaim)
- Instruksi jalankan routing KB & jawab 6 pertanyaan serangan sesuai definisi agent-nya

Hasil: verdict per kandidat `TEST | REJECT-NOW | NEEDS-DATA-WE-DONT-HAVE` + panduan uji untuk yang TEST.
Kalau 0 kandidat TEST → lompat ke Stage 4.

## Stage 3 — Uji empiris (sub-agent `data-verifier`)

Untuk kandidat `TEST` (maksimal 3 per video — kalau lebih, pilih yang paling menyentuh K-node aktif saat ini, sisanya masuk findings sebagai "belum diuji"):

Spawn sub-agent `data-verifier` (synchronous, satu spawn bisa menangani beberapa kandidat). Prompt harus berisi:
- Definisi klaim + panduan uji + jebakan metodologi dari skeptic
- Instruksi ikuti house rigor sesuai definisi agent-nya

Hasil per kandidat: SUPPORTED / NOT-SUPPORTED / MIXED, dengan n, sebaran cycle, dan catatan bias.

**Kalau ada kandidat verdict `NEEDS-DATA-WE-DONT-HAVE`:** catat di findings sebagai gap, JANGAN pernah menambah pipeline data baru ke `auto_update.py` atau menarik data permanen sebagai bagian dari run ini — walau tergoda karena sudah tahu persis data apa yang kurang. Menambah sumber data permanen adalah keputusan produksi terpisah (biaya API call harian selamanya) yang harus Yudi minta secara eksplisit di luar `/video-breakdown`, bukan hasil ikutan otomatis dari video yang kebetulan dibedah.

## Stage 4 — Findings doc (kamu sendiri, orchestrator)

Tulis `research/findings/video-breakdown/video_<slug>_findings.md`.

**ATURAN BAHASA (penting):** Bahasa Indonesia sederhana. Kalimat pendek. Istilah teknis (MVRV, SOPR, dll) tetap English tapi dijelaskan sekali saat pertama muncul. Tidak ada jargon statistik tanpa penjelasan satu kalimat. Bahasa probabilistik selalu ("cenderung", "historically") — tidak pernah "pasti".

Struktur wajib:

```markdown
# Video Breakdown: <judul>
URL / channel / tanggal video / tanggal breakdown / fokus (kalau ada)

## Ringkasan Sederhana
<3-5 kalimat gampang: video ini intinya bilang apa, dari semua klaimnya
mana yang beneran berguna buat framework kita, mana yang tidak, dan apa
langkah berikutnya. Yudi harus bisa baca bagian ini SAJA dan sudah paham.>

## Tabel Semua Klaim
| No | Klaim | Klasifikasi | Verdict skeptic | Hasil uji | Verdict akhir |

## Detail per Kandidat NOVEL
### <nama klaim>
- Apa yang video bilang: <plain language>
- Kata skeptic: <ringkasan kritik>
- Hasil uji data: <n, sebaran cycle, hasil, catatan bias — plain language>
- **Verdict akhir: ADD / REJECT / NEEDS-MORE-DATA**

## Usulan Perubahan Framework (hanya kalau ada ADD)
<diff konkret per ADD: K-node mana, sinyal/threshold apa yang ditambah,
bunyi teksnya bagaimana. INI USULAN — belum diterapkan.>

## Butuh Judgment Yudi
<1-3 pertanyaan terbuka yang benar-benar butuh keputusan Yudi.
Kalau tidak ada, tulis "Tidak ada — semua verdict sudah jelas.">
```

Aturan verdict akhir:
- `ADD` hanya kalau: skeptic loloskan + uji data SUPPORTED + tidak bentrok hard constraint
- Uji MIXED → `NEEDS-MORE-DATA` (jangan dipaksa jadi ADD)
- `TESTED-BEFORE` pakai verdict lama dari video_index

Terakhir: **append satu baris** ke tabel "Video yang sudah dibedah" di `research/findings/video-breakdown/video_index.md` (tanggal, judul video, klaim utama + verdict singkat, nama file findings).

## Stage 5 — Commit & push

Commit HANYA artefak riset dari run ini:
- `research/findings/video-breakdown/video_<slug>/` (transcript)
- `research/findings/video-breakdown/video_<slug>_findings.md`
- `research/analyze_*.py` yang baru dibuat (script verifikasi tetap di `research/` root, bukan subfolder video-breakdown — biar reusable untuk riset non-video juga) + CSV pendukung
- `research/findings/video-breakdown/video_index.md`

Commit message: `research: video breakdown <judul singkat> — <X> ADD, <Y> REJECT, <Z> needs-more-data`. Lalu `git push`.

JANGAN commit perubahan lain yang kebetulan ada di working tree.

## Stage 6 — STOP (gated)

Pipeline SELESAI di sini. **JANGAN mengedit `references/Decision_Framework v1.md` atau file KB apapun** — walaupun verdict-nya ADD. Perubahan framework hanya dilakukan di langkah terpisah SETELAH Yudi baca findings dan approve usulan diff.

Tutup dengan ringkasan singkat ke Yudi: link findings doc, jumlah ADD/REJECT/NEEDS-MORE-DATA, dan (kalau ada) pertanyaan "Butuh Judgment Yudi" ditampilkan langsung di chat.
