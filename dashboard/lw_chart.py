"""Chart lightweight yang digambar langsung di browser.

Legend on/off dan mode sorot diproses di browser, jadi tidak memicu rerun
Streamlit. Python hanya mengirim data saat data atau pengaturan chart berubah.
"""
import json

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

LWC_URLS = [
    "https://cdn.jsdelivr.net/npm/lightweight-charts@4.2.3/dist/lightweight-charts.standalone.production.js",
    "https://unpkg.com/lightweight-charts@4.2.3/dist/lightweight-charts.standalone.production.js",
]
TOOLBAR_H = 40
PANE_GAP = 6

TEMPLATE = """
<style>
  html, body { margin: 0; background: #131722; overflow: hidden; }
  body { font: 12px Inter, system-ui, sans-serif; color: #c9d1d9; }
  /* Tinggi baris ini ikut isinya: kalau legend atau tombol sorot tidak muat satu baris,
     baris baru ditambahkan dan tinggi pane chart dikurangi sebesar itu (lihat
     sesuaikanTinggi di bawah), jadi tinggi total chart tetap dan legend tidak terpotong.
     Satu baris tetap setinggi __TOOLBAR__ px seperti sebelumnya. */
  #bar { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 12px;
         min-height: __TOOLBAR__px; padding-top: 4px; padding-bottom: 4px; box-sizing: border-box; }
  /* Legend minimal 320 px; kalau sisa tempat lebih sempit, kelompok tombol sorot yang
     turun ke baris sendiri (rata kanan), bukan legend yang diperas jadi banyak baris. */
  #legend { flex: 1 1 320px; min-width: 0; display: flex; flex-wrap: wrap; gap: 4px 10px;
            align-content: center; }
  .lgroup { display: inline-flex; align-items: center; gap: 3px; flex: none; }
  /* Jarak atas 0 dan bawah 2 px, bukan 1/1: tinta "1y" (ekor y) jatuh 1,5 px di bawah
     tengah kotak dan "30" 0,5 px. Dinaikkan 1 px supaya keduanya terlihat di tengah. */
  .lgdot { font-size: 11px; padding: 0 5px 2px; border: 1px solid #232838; border-radius: 5px;
           line-height: 1.2; color: #b9c3cd; }
  #hl { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 4px; align-items: center;
        flex: 0 1 auto; margin-left: auto; }
  /* Sempat diredupkan ke 11px #6E7681 supaya beda dari tombol di sebelahnya; dicoba dan
     ditolak karena jadi sulit dibaca. Dibiarkan setara tombol. */
  .hllabel { font-size: 12px; color: #8B949E; margin-right: 2px; }
  button { cursor: pointer; font: 12px Inter, system-ui, sans-serif; background: transparent;
           border: 1px solid transparent; border-radius: 6px; padding: 3px 8px; color: #e2e8ef; }
  .lg { display: inline-flex; align-items: center; gap: 6px; flex: none; }
  /* Nama kelompok tanpa garis utama (Rolling Z-Score) berupa keterangan, bukan tombol.
     Jarak dalam dan garis tepinya disamakan dengan tombol, supaya contoh warnanya mulai
     di posisi yang sama dengan baris di atasnya saat kelompok ini membuka baris baru. */
  span.lg { padding: 3px 8px; border: 1px solid transparent; }
  .sw { width: 14px; height: 0; display: inline-block; }
  .off { opacity: 0.62; text-decoration: line-through; }
  .hl { color: #8B949E; border-color: #232838; }
  .hl.on { background: rgba(0, 109, 119, 0.40); border-color: #006d77; color: #fff; }
  .fssep { width: 1px; height: 16px; background: #232838; margin: 0 4px; flex: none; }
  .fsbtn { display: inline-flex; align-items: center; gap: 6px; }
  .fsbtn svg { width: 12px; height: 12px; }
  #panes > div + div { margin-top: __GAP__px; }
  /* Tooltip: angka di tanggal bawah kursor. Diparkir di pojok kiri atas area gambar dan
     pindah ke kanan atas kalau kursor mendekat, supaya tidak menutupi garis yang dibaca.
     Satu baris per metrik; periode smoothing jadi kolom. */
  #tip { position: absolute; z-index: 5; pointer-events: none; display: none;
         background: rgba(28, 34, 48, 0.94); border: 1px solid #2a2e39; border-radius: 6px;
         padding: 6px 10px; font-size: 12px; line-height: 1.55; color: #c9d1d9; white-space: nowrap; }
  #tip .tgl { color: #fff; font-weight: 600; margin-bottom: 2px; }
  #tip table { border-collapse: collapse; }
  #tip td, #tip th { padding: 0 0 0 14px; text-align: right; font-variant-numeric: tabular-nums; }
  #tip td:first-child, #tip th:first-child { padding-left: 0; text-align: left; }
  #tip th { font-weight: 400; color: #8b949e; font-size: 11px; }
  #tip .v { color: #fff; font-weight: 600; }
  #tip .tsw { display: inline-block; width: 14px; height: 0; border-top: 2px solid; vertical-align: 4px; margin-right: 6px; }
  #tip .tbox { display: inline-block; width: 11px; height: 9px; border-radius: 2px; margin-right: 6px; vertical-align: -1px; }
  #err { color: #DA3633; padding: 16px; }
</style>
<div id="bar">
  <div id="legend"></div>
  <!-- "Highlight" adalah keterangan, bukan tombol. Warnanya diturunkan satu tingkat
       dari tombol di sebelahnya supaya tidak terbaca sebagai tombol yang sedang mati. -->
  <div id="hl"><span class="hllabel">Highlight</span></div>
</div>
<div id="panes"></div>
<div id="tip"></div>
<div id="err"></div>
<script>
const D = __DATA__;
const S = __SPECS__;
const C = __CONFIG__;
const URLS = __URLS__;

// Klik dan tombol di dalam chart tidak sampai ke halaman Streamlit, jadi popover yang
// sedang terbuka tidak tahu ada klik di luar. Teruskan ke halaman induk agar tertutup.
function parentDoc() {
  try { return window.parent.document; } catch (e) { return null; }
}
function popoverOpen(doc) {
  return doc && doc.querySelector('button[data-testid="stPopoverButton"][aria-expanded="true"]');
}
document.addEventListener('pointerdown', () => {
  const doc = parentDoc();
  if (popoverOpen(doc)) doc.body.dispatchEvent(new MouseEvent('click', { bubbles: true }));
}, true);
document.addEventListener('keydown', event => {
  const doc = parentDoc();
  if (event.key === 'Escape' && popoverOpen(doc)) {
    doc.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', code: 'Escape', bubbles: true }));
  }
}, true);

function loadLib(i) {
  return new Promise((ok, fail) => {
    if (window.LightweightCharts) return ok();
    if (i >= URLS.length) return fail(new Error('pustaka chart gagal dimuat'));
    const tag = document.createElement('script');
    tag.src = URLS[i];
    tag.onload = ok;
    tag.onerror = () => loadLib(i + 1).then(ok, fail);
    document.head.appendChild(tag);
  });
}

// Pilihan disimpan di halaman induk supaya bertahan saat Streamlit rerun.
// Kalau browser menolak akses penyimpanan, chart tetap jalan tanpa mengingat pilihan.
function readState() {
  try { return JSON.parse(window.parent.localStorage.getItem(C.store)) || {}; } catch (e) { return {}; }
}
function writeState(value) {
  try { window.parent.localStorage.setItem(C.store, JSON.stringify(value)); } catch (e) {}
}

function dimmed(color, alpha) {
  if (!color.startsWith('#')) return color;
  const [r, g, b] = [1, 3, 5].map(i => parseInt(color.slice(i, i + 2), 16));
  return `rgba(${r},${g},${b},${alpha})`;
}

// Format angka per seri (precision dari registry), dipakai sumbu, label nilai terakhir,
// dan tooltip. Harga (precision 0) tanpa desimal dengan pemisah ribuan; harga di bawah
// 100 tetap diberi desimal supaya harga BTC 2010 ($0.05) tidak terbaca "0".
function angka(v, p) {
  if (v === null || v === undefined || !isFinite(v)) return '';
  let min = p, max = p;
  if (p === 0 && Math.abs(v) < 100) {
    // Di bawah 1 sampai 4 desimal tapi nol di belakang dibuang: 0.60 dan 0.0495, bukan 0.6000.
    min = 2;
    max = Math.abs(v) < 1 ? 4 : 2;
  }
  return v.toLocaleString('en-US', { minimumFractionDigits: min, maximumFractionDigits: max });
}
function formatSeri(spec) {
  const p = Number.isInteger(spec.precision) ? spec.precision : 2;
  return { type: 'custom', minMove: p === 0 ? 0.0001 : Math.pow(10, -p), formatter: v => angka(v, p) };
}

// Pita smoothing digambar tembus pandang, jadi warna dasarnya sudah mengandung alpha.
function baseColor(spec) {
  return spec.alpha < 1 ? dimmed(spec.color, spec.alpha) : spec.color;
}

function chartOptions(height, left, right, showLeft, showRight, timeVisible) {
  return {
    width: document.body.clientWidth,
    height,
    layout: { background: { type: 'solid', color: '#131722' }, textColor: '#d1d4dc', fontSize: 11 },
    grid: { vertLines: { color: 'rgba(42,46,57,0.3)' }, horzLines: { color: 'rgba(42,46,57,0.3)' } },
    crosshair: { mode: 0 },
    leftPriceScale: Object.assign({ visible: showLeft, borderVisible: false }, left),
    rightPriceScale: Object.assign({ visible: showRight, borderVisible: false }, right),
    // minBarSpacing kecil supaya fitContent() sanggup menampilkan seluruh sejarah harian.
    timeScale: { borderVisible: false, visible: timeVisible, minBarSpacing: 0.005 },
  };
}

loadLib(0).then(() => {
  const LC = window.LightweightCharts;
  const panes = {};
  const charts = [];

  // Pane dibangun dari daftar C.panes, urut dari atas ke bawah: harga (bila dipisah),
  // metrik, lalu pane tambahan seperti Z-Score. Semua pane wajib menampilkan sisi sumbu
  // yang sama — kalau tidak, area gambarnya bergeser dan tanggal yang sama jatuh di
  // posisi berbeda antar-pane. Sumbu waktu hanya digambar di pane paling bawah.
  const wadahPane = document.getElementById('panes');
  C.panes.forEach((p, i) => {
    const div = document.createElement('div');
    div.id = p.id;
    div.style.height = p.height + 'px';
    wadahPane.appendChild(div);
    const chart = LC.createChart(div, chartOptions(
      p.height, p.left, p.right, C.showLeft, C.showRight, i === C.panes.length - 1));
    panes[p.id] = chart;
    charts.push(chart);
  });

  // Seri jangkar tak terlihat di setiap pane: semua pane punya jumlah bar yang sama,
  // sehingga zoom dan geser antar-pane tersinkron tepat.
  for (const chart of charts) {
    const anchor = chart.addLineSeries({
      color: 'rgba(0,0,0,0)', priceScaleId: 'anchor', lastValueVisible: false,
      priceLineVisible: false, crosshairMarkerVisible: false,
    });
    anchor.setData(D.t.map(t => ({ time: t, value: 0 })));
  }

  const handles = [];
  for (const spec of S) {
    const values = D.cols[spec.col];
    const points = [];
    for (let i = 0; i < D.t.length; i++) {
      if (values[i] !== null) points.push({ time: D.t[i], value: values[i] });
    }
    const umum = {
      color: baseColor(spec),
      priceScaleId: spec.pane === 'price' ? 'right' : spec.axis,
      title: spec.group ? spec.name : '',
      priceLineVisible: false,
      lastValueVisible: !!spec.group,
      priceFormat: formatSeri(spec),
    };
    // Batang digambar dari garis nol, jadi nilai negatif turun ke bawah sendiri.
    const line = spec.kind === 'histogram'
      ? panes[spec.pane].addHistogramSeries(Object.assign({ base: 0 }, umum))
      : panes[spec.pane].addLineSeries(Object.assign({
          lineWidth: spec.width,
          lineStyle: spec.style,
          lineType: spec.steps ? 1 : 0,
          crosshairMarkerVisible: !!spec.group,
        }, umum));
    line.setData(points);
    handles.push({ spec, line });
  }
  // Tampilan awal: pulihkan zoom terakhir, atau tampilkan seluruh data.
  // Sidik data ikut disimpan, jadi kalau rentang tanggalnya memang berubah
  // (tombol Range), zoom lama tidak dipakai.
  // fitContent() tidak bekerja selama lebar chart masih 0 (mis. panel belum tampil),
  // dan hasilnya chart berhenti di lebar bar bawaan (sekitar 160 hari terakhir).
  // Karena itu tampilan awal diulang sampai chart benar-benar punya lebar.
  // Posisi bar (logical range) dipakai, bukan tanggal: memulihkan tanggal membuat
  // tepi kiri bergeser sedikit tiap kali karena dibulatkan ke bar terdekat.
  const dataSig = D.t.length + ':' + D.t[0] + ':' + D.t[D.t.length - 1];
  const simpanan = readState();
  const pulihkanZoom = simpanan.bars && simpanan.sig === dataSig ? simpanan.bars : null;
  let tampilanAwalSelesai = false;
  // Selama fase pemulihan, zoom simpanan boleh ditarik kembali kalau ada yang menggesernya.
  // Lebar sumbu harga baru mengendap sekitar satu-dua detik setelah chart tampil (label
  // "300000.00" jauh lebih lebar daripada "1.50", dan kedua pane disamakan lebarnya).
  // Chart mempertahankan lebar bar, bukan rentangnya, jadi area gambar yang menyusut
  // menggeser tepi kiri — inilah yang membuat zoom mengecil tiap kali Overlay <->
  // Separate pane. Memeriksa sekali di awal tidak cukup: geseran itu datang belakangan.
  let fasePemulihan = false;

  // Kesiapan diukur dari pane utama: pane harga punya skala waktu tersembunyi,
  // sehingga lebarnya selalu 0 dan tidak bisa dipakai sebagai penanda.
  // Lebar chart > 0 saja juga tidak cukup sebagai tanda "tampilan awal beres": hasilnya
  // diperiksa, zoom baru dianggap terpasang kalau rentang yang tampil benar-benar cocok.
  function rentangCocok(target) {
    const r = panes.main.timeScale().getVisibleLogicalRange();
    return !!r && Math.abs(r.from - target.from) < 1 && Math.abs(r.to - target.to) < 1;
  }

  function tampilkanAwal() {
    for (const chart of charts) {
      if (pulihkanZoom) {
        try { chart.timeScale().setVisibleLogicalRange(pulihkanZoom); } catch (e) { chart.timeScale().fitContent(); }
      } else {
        chart.timeScale().fitContent();
      }
    }
    if (panes.main.timeScale().width() <= 0) return;
    tampilanAwalSelesai = pulihkanZoom ? rentangCocok(pulihkanZoom) : true;
  }

  tampilkanAwal();
  fasePemulihan = !!pulihkanZoom;
  const pollAwal = setInterval(() => {
    if (!tampilanAwalSelesai) { tampilkanAwal(); return; }
    if (!fasePemulihan) { clearInterval(pollAwal); return; }
    // Zoom sudah pernah terpasang benar; kalau bergeser sendiri (lebar sumbu berubah),
    // tarik kembali. Penyimpanan aman: penulisnya membaca ulang rentang setelah jeda
    // 300 ms, jadi yang tercatat adalah rentang yang sudah dikoreksi.
    if (!rentangCocok(pulihkanZoom)) {
      for (const chart of charts) {
        try { chart.timeScale().setVisibleLogicalRange(pulihkanZoom); } catch (e) { /* diulang di putaran berikutnya */ }
      }
    }
  }, 120);
  // Batas waktu: fase pemulihan ditutup apa adanya. Tanpa ini chart berhenti mengingat
  // zoom baru dari pengguna, karena penyimpanan memang menunggu bendera tampilan awal.
  setTimeout(() => {
    clearInterval(pollAwal);
    fasePemulihan = false;
    tampilanAwalSelesai = true;
  }, 6000);
  // Begitu pengguna menggeser atau zoom sendiri, pemulihan berhenti supaya tidak
  // tarik-menarik dengan tangan pengguna.
  for (const ev of ['wheel', 'mousedown', 'touchstart']) {
    document.addEventListener(ev, () => {
      fasePemulihan = false;
      tampilanAwalSelesai = true;
    }, { capture: true, once: true });
  }

  // Lebar sumbu ikut panjang label ("180000.00" vs "1.50"), jadi disamakan ke yang
  // paling lebar di tiap sisi. Diulang setelah zoom/geser karena label bisa berubah.
  // Legend dan tombol diluruskan dengan area gambar, bukan dengan tepi iframe. Tanpa ini
  // tombol paling kanan berdiri di atas strip sumbu harga — terlihat keluar dari kotak chart.
  // Jarak minimal tetap dijaga: kalau semua metrik dipindah ke sumbu kiri, sumbu kanan
  // hilang dan lebarnya jadi 0 — tanpa jarak minimal tombol paling kanan menempel ke
  // tepi dan terlihat keluar dari batas chart.
  const JARAK_TEPI_MIN = 10;
  let tinggiSiap = false;   // true setelah fungsi tinggi pane di bawah terdefinisi
  function rapikanBar() {
    const sisi = s => Math.max(s.options().visible ? s.width() : 0, JARAK_TEPI_MIN);
    const bar = document.getElementById('bar');
    bar.style.paddingLeft = sisi(panes.main.priceScale('left')) + 'px';
    bar.style.paddingRight = sisi(panes.main.priceScale('right')) + 'px';
    // Jarak kiri-kanan bisa membuat legend membungkus ke baris baru. ResizeObserver
    // pada baris ini seharusnya menangkapnya, tapi tidak berbunyi kalau frame sedang
    // tidak digambar; pemeriksaan di sini (ikut timer rapikanBar) jadi cadangannya.
    if (tinggiSiap) sesuaikanTinggiLayar();
  }

  let syncPending = false;
  function syncScaleWidths() {
    syncPending = false;
    if (charts.length > 1) {
      for (const side of ['left', 'right']) {
        const scales = charts.map(chart => chart.priceScale(side)).filter(s => s.options().visible);
        if (scales.length < 2) continue;
        const target = Math.max(...scales.map(s => s.width()));
        if (target <= 0) continue;
        for (const s of scales) {
          if (s.options().minimumWidth !== target) s.applyOptions({ minimumWidth: target });
        }
      }
    }
    rapikanBar();
  }
  function scheduleScaleSync() {
    if (syncPending) return;
    syncPending = true;
    requestAnimationFrame(() => requestAnimationFrame(syncScaleWidths));
  }
  scheduleScaleSync();
  // Lebar sumbu harga baru diketahui sesudah chart menggambar, jadi perataan bar
  // diulang beberapa detik pertama — sekali di boot saja hasilnya masih nol.
  const pollBar = setInterval(rapikanBar, 150);
  setTimeout(() => clearInterval(pollBar), 4000);

  if (charts.length > 1) {
    // Pemberitahuan zoom datang tertunda, jadi penanda "sedang sinkron" tidak bisa diandalkan.
    // Pane tujuan hanya digeser bila rentangnya memang berbeda, supaya tidak saling memantul.
    const same = (a, b) => a && b && Math.abs(a.from - b.from) < 0.5 && Math.abs(a.to - b.to) < 0.5;
    for (const source of charts) {
      source.timeScale().subscribeVisibleLogicalRangeChange(range => {
        if (!range) return;
        scheduleScaleSync();
        for (const target of charts) {
          if (target === source) continue;
          if (!same(target.timeScale().getVisibleLogicalRange(), range)) {
            target.timeScale().setVisibleLogicalRange(range);
          }
        }
      });
    }
  }

  // Chart mempertahankan lebar bar, bukan rentangnya. Kalau chart melebar (mis. masuk
  // layar penuh) saat seluruh sejarah sedang tampil, tepi kiri melewati data pertama dan
  // muncul celah kosong. Jadi kalau sebelum berubah lebar seluruh data tampil, chart
  // dipaskan ulang; kalau pengguna sedang zoom ke rentang pendek, zoom-nya dibiarkan.
  const tampilSemua = () => {
    const r = panes.main.timeScale().getVisibleLogicalRange();
    return !!r && r.from <= 0.5 && r.to >= D.t.length - 1.5;
  };
  new ResizeObserver(() => {
    const semua = tampilanAwalSelesai && tampilSemua();
    charts.forEach(chart => chart.applyOptions({ width: document.body.clientWidth }));
    if (!tampilanAwalSelesai) tampilkanAwal();
    else if (semua) charts.forEach(chart => chart.timeScale().fitContent());
    scheduleScaleSync();
  }).observe(document.body);

  const legendItems = handles.filter(h => h.spec.group);
  const groups = [...new Set(legendItems.map(h => h.spec.group))];
  // Beberapa garis bisa disorot sekaligus. Penyimpanan lama berisi satu nama
  // (highlight: 'MVRV' atau 'none'), jadi diubah ke daftar bila masih format lama.
  const saved = readState();
  const savedHighlights = Array.isArray(saved.highlights) ? saved.highlights
    : (saved.highlight && saved.highlight !== 'none' ? [saved.highlight] : []);
  // Seri yang ditandai hidden_default lahir dalam keadaan mati, tapi hanya sekali:
  // daftar "seen" mencatat seri yang pernah muncul, jadi kalau pengguna menyalakannya
  // pilihan itu tidak ditimpa lagi di kunjungan berikutnya.
  const dikenal = Array.isArray(saved.seen) ? saved.seen : [];
  const tersembunyi = Array.isArray(saved.hidden) ? saved.hidden.slice() : [];
  for (const h of legendItems) {
    if (h.spec.hidden_default && !dikenal.includes(h.spec.name)
        && !tersembunyi.includes(h.spec.name)) {
      tersembunyi.push(h.spec.name);
    }
  }
  const state = Object.assign({}, saved, {
    highlights: savedHighlights.filter(group => groups.includes(group)),
    hidden: tersembunyi,
    seen: [...new Set(dikenal.concat(legendItems.map(h => h.spec.name)))],
  });
  delete state.highlight;   // sisa format lama, sudah digantikan highlights

  // Legend dikelompokkan per metrik: satu label untuk garis utama, lalu titik kecil
  // berisi angka periode untuk tiap garis smoothing-nya. Tanpa ini, satu metrik dengan
  // tiga smoothing memakan empat label dan legend jadi harus digeser ke samping.
  const legendEl = document.getElementById('legend');
  const legendButtons = [];

  function toggleHidden(name) {
    state.hidden = state.hidden.includes(name)
      ? state.hidden.filter(x => x !== name)
      : state.hidden.concat(name);
    apply();
  }

  for (const group of groups) {
    const anggota = legendItems.filter(h => h.spec.group === group);
    // Ada dua bentuk kelompok:
    //   1. ada seri yang namanya persis nama kelompok (MVRV + titik periode smoothing)
    //      -> nama kelompok jadi tombol yang menyalakan seri itu.
    //   2. tidak ada (Rolling Z-Score 1y/2y/4y) -> nama kelompok cuma keterangan,
    //      dan semua anggotanya muncul sebagai kotak angka yang bisa diklik sendiri.
    const utama = anggota.find(h => h.spec.name === group);
    const contoh = utama || anggota[0];
    const wadah = document.createElement('span');
    wadah.className = 'lgroup';

    const button = document.createElement(utama ? 'button' : 'span');
    button.className = 'lg';
    const swatch = document.createElement('span');
    swatch.className = 'sw';
    if (contoh.spec.kind === 'histogram') {
      swatch.style.height = '9px';
      swatch.style.width = '11px';
      swatch.style.borderRadius = '2px';
      swatch.style.background = baseColor(contoh.spec);
    } else {
      swatch.style.borderTop = `${contoh.spec.alpha < 1 ? 3 : 2}px `
        + `${contoh.spec.style === 1 ? 'dotted' : contoh.spec.style ? 'dashed' : 'solid'} `
        + `${baseColor(contoh.spec)}`;
    }
    button.append(swatch, document.createTextNode(group));
    if (utama) {
      button.onclick = () => toggleHidden(utama.spec.name);
      legendButtons.push({ button, handle: utama });
    }
    wadah.appendChild(button);

    for (const handle of anggota) {
      if (handle === utama) continue;
      const dalamKurung = handle.spec.name.split('(')[1];
      const titik = document.createElement('button');
      titik.className = 'lgdot';
      titik.textContent = dalamKurung ? dalamKurung.replace(')', '') : handle.spec.name;
      titik.title = handle.spec.name;
      titik.style.borderColor = baseColor(handle.spec);
      titik.onclick = () => toggleHidden(handle.spec.name);
      wadah.appendChild(titik);
      legendButtons.push({ button: titik, handle });
    }

    legendEl.appendChild(wadah);
  }

  const hlEl = document.getElementById('hl');
  // Nama pendek dari registry dipakai kalau ada; tanpa itu dua seri yang namanya
  // berawalan sama ("MVRV Z-Score" dan "MVRV Z-Score 1Y") jadi kembar di tombol.
  const namaPendek = {};
  for (const h of handles) {
    if (h.spec.group && h.spec.short) namaPendek[h.spec.group] = h.spec.short;
  }
  const hlButtons = ['none'].concat(groups).map(group => {
    const button = document.createElement('button');
    button.className = 'hl';
    button.textContent = group === 'none' ? 'None' : (namaPendek[group] || group.split(' ')[0]);
    button.title = group === 'none' ? 'Clear highlight' : group;
    // None mematikan semua sorotan; tombol garis menyala/mati setiap diklik.
    button.onclick = () => {
      if (group === 'none') state.highlights = [];
      else if (state.highlights.includes(group)) state.highlights = state.highlights.filter(g => g !== group);
      else state.highlights = state.highlights.concat(group);
      apply();
    };
    hlEl.appendChild(button);
    return { button, group };
  });

  // Tombol layar penuh hidup di dalam chart, bukan di baris kontrol Streamlit.
  // Kliknya sudah merupakan gestur pengguna, jadi requestFullscreen() boleh dipanggil
  // langsung — tidak perlu skrip penyisip yang memasang pendengar ke tombol Streamlit,
  // dan tidak ada status di Python yang bisa hilang saat satu putaran terpotong.
  // Kerangka Streamlit disembunyikan oleh aturan CSS :fullscreen di app_v2.py.
  const IKON_PENUH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>';
  const IKON_KELUAR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5"/></svg>';
  const docInduk = () => { try { return window.parent.document; } catch (e) { return null; } };
  const sedangPenuh = () => { const d = docInduk(); return !!(d && d.fullscreenElement); };

  // Saat layar penuh, chart ikut memanjang mengisi sisa tinggi jendela. Tinggi iframe
  // ditetapkan Streamlit lewat gaya inline pada iframe dan wadahnya, jadi keduanya
  // ditimpa sementara lalu dikembalikan persis seperti semula saat keluar.
  const bingkai = window.frameElement;
  const wadahBingkai = bingkai ? bingkai.parentElement : null;
  const tinggiBingkaiAwal = bingkai ? bingkai.style.height : '';
  const tinggiWadahAwal = wadahBingkai ? wadahBingkai.style.height : '';

  const tinggiAwal = C.panes.map(p => p.height);
  const totalTinggiAwal = tinggiAwal.reduce((a, b) => a + b, 0);
  let totalTerpasang = null;
  function terapkanTinggi(total) {
    total = Math.max(120, Math.round(total));
    if (total === totalTerpasang) return false;   // tidak ada yang berubah: jangan gambar ulang
    totalTerpasang = total;
    let sisa = total;
    C.panes.forEach((p, i) => {
      const h = i === C.panes.length - 1 ? sisa
        : Math.round(total * tinggiAwal[i] / totalTinggiAwal);
      sisa -= h;
      document.getElementById(p.id).style.height = h + 'px';
      panes[p.id].applyOptions({ height: h });
    });
    return true;
  }

  // Tinggi pane = tinggi bingkai - tinggi baris legend yang sebenarnya - jarak antar-pane.
  // Baris legend bisa lebih dari satu (layar sempit, garis banyak); tambahannya diambil
  // dari pane, bukan dari bingkai, jadi tinggi total chart di halaman tidak berubah dan
  // pane paling bawah (dengan sumbu waktunya) tidak terdorong keluar bingkai.
  const barEl = document.getElementById('bar');
  function sesuaikanTinggiLayar() {
    let tinggiBingkai = C.frameHeight;
    if (bingkai && sedangPenuh()) {
      const atas = bingkai.getBoundingClientRect().top;
      tinggiBingkai = Math.max(320, (window.parent.innerHeight || 0) - atas - 8);
      bingkai.style.height = tinggiBingkai + 'px';
      if (wadahBingkai) wadahBingkai.style.height = tinggiBingkai + 'px';
    } else if (bingkai) {
      bingkai.style.height = tinggiBingkaiAwal;
      if (wadahBingkai) wadahBingkai.style.height = tinggiWadahAwal;
    }
    // Sinkron sumbu hanya kalau tinggi benar-benar berubah: rapikanBar memanggil fungsi
    // ini, dan sinkron sumbu memanggil rapikanBar — tanpa syarat ini keduanya berputar.
    if (terapkanTinggi(tinggiBingkai - barEl.offsetHeight - __GAP__ * (C.panes.length - 1))) {
      scheduleScaleSync();
    }
  }
  tinggiSiap = true;
  // Tinggi baris legend berubah saat lebar chart berubah atau jarak kiri-kanannya
  // diluruskan ke sumbu (rapikanBar), jadi tinggi pane dihitung ulang setiap kali.
  new ResizeObserver(() => sesuaikanTinggiLayar()).observe(barEl);

  const fsSep = document.createElement('span');
  fsSep.className = 'fssep';
  const fsBtn = document.createElement('button');
  fsBtn.className = 'hl fsbtn';
  function perbaruiFs() {
    const penuh = sedangPenuh();
    fsBtn.innerHTML = (penuh ? IKON_KELUAR : IKON_PENUH) + (penuh ? 'Exit' : 'Full');
    fsBtn.title = penuh ? 'Leave full screen (Esc)' : 'Full screen';
    sesuaikanTinggiLayar();
  }
  fsBtn.onclick = () => {
    const d = docInduk();
    if (!d) return;
    // Janji dari kedua perintah ini bisa ditolak browser; ditangkap supaya tidak
    // muncul sebagai error yang tidak tertangani di console.
    const janji = d.fullscreenElement ? d.exitFullscreen() : d.documentElement.requestFullscreen();
    if (janji && janji.catch) janji.catch(() => {});
  };
  perbaruiFs();
  hlEl.append(fsSep, fsBtn);
  // Esc keluar dari layar penuh tanpa melewati tombol ini, jadi tampilannya
  // disesuaikan dari peristiwa dokumen induk, bukan dari klik. Ukuran jendela juga
  // diikuti supaya chart tetap pas saat layar penuh dipindah ke monitor lain.
  const dInduk = docInduk();
  if (dInduk) dInduk.addEventListener('fullscreenchange', perbaruiFs);
  try { window.parent.addEventListener('resize', sesuaikanTinggiLayar); } catch (e) {}

  function apply() {
    for (const { button, handle } of legendButtons) {
      const hidden = state.hidden.includes(handle.spec.name);
      const faded = state.highlights.length > 0 && !state.highlights.includes(handle.spec.group);
      const fadedAlpha = handle.spec.dim * (handle.spec.alpha < 1 ? handle.spec.alpha : 1);
      handle.line.applyOptions({
        visible: !hidden,
        color: faded ? dimmed(handle.spec.color, fadedAlpha) : baseColor(handle.spec),
      });
      button.classList.toggle('off', hidden);
    }
    for (const { button, group } of hlButtons) {
      button.classList.toggle('on', group === 'none'
        ? state.highlights.length === 0
        : state.highlights.includes(group));
    }
    writeState(state);
  }

  apply();

  // ---------------------------------------------------------------- tooltip
  // Isi: garis yang ON di legend; kalau Highlight aktif, hanya kelompok yang disorot.
  // BTC Price selalu tampil. Seri pane bawah hanya ada kalau pane-nya menyala (kalau
  // Hidden, serinya memang tidak dikirim). Garis acuan (tanpa group) tidak ikut.
  const tipEl = document.getElementById('tip');
  const panesEl = document.getElementById('panes');
  const indeksTanggal = new Map(D.t.map((t, i) => [t, i]));
  const BULAN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const HARGA = 'BTC Price';
  // Regex ditulis tanpa backslash: TEMPLATE adalah string Python biasa, dan backslash di
  // dalamnya memicu peringatan escape sequence di Python.
  const periodeDari = nama => { const m = /[(]([0-9]+)[)]$/.exec(nama); return m ? +m[1] : null; };
  const teksWaktu = t => typeof t === 'string' ? t
    : `${t.year}-${String(t.month).padStart(2, '0')}-${String(t.day).padStart(2, '0')}`;
  const nilaiDi = (spec, i) => { const v = D.cols[spec.col][i]; return v === null ? null : v; };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

  function contohWarna(spec) {
    return spec.kind === 'histogram'
      ? `<span class="tbox" style="background:${baseColor(spec)}"></span>`
      : `<span class="tsw" style="border-color:${spec.color}"></span>`;
  }

  function isiTooltip(i) {
    const baris = [];
    const semuaPeriode = new Set();
    for (const group of groups) {
      if (state.highlights.length > 0 && group !== HARGA && !state.highlights.includes(group)) continue;
      const anggota = legendItems.filter(h => h.spec.group === group && !state.hidden.includes(h.spec.name));
      if (anggota.length === 0) continue;
      const utama = anggota.find(h => h.spec.name === group);
      const smoothing = anggota.filter(h => h !== utama && periodeDari(h.spec.name) !== null);
      const lainnya = anggota.filter(h => h !== utama && !smoothing.includes(h));
      if (utama || smoothing.length > 0) {
        const kolom = new Map();
        for (const h of smoothing) {
          const p = periodeDari(h.spec.name);
          semuaPeriode.add(p);
          kolom.set(p, angka(nilaiDi(h.spec, i), h.spec.precision));
        }
        const contoh = (utama || smoothing[0]).spec;
        baris.push({ label: group, spec: contoh,
                     nilai: utama ? angka(nilaiDi(utama.spec, i), utama.spec.precision) : '', kolom });
      }
      // Kelompok tanpa garis utama (Rolling Z-Score 1y/2y/4y): tiap anggota satu baris.
      for (const h of lainnya) {
        baris.push({ label: h.spec.name, spec: h.spec,
                     nilai: angka(nilaiDi(h.spec, i), h.spec.precision), kolom: new Map() });
      }
    }
    const periode = [...semuaPeriode].sort((a, b) => a - b);
    const [y, m, d] = D.t[i].split('-');
    let html = `<div class="tgl">${d} ${BULAN[+m - 1]} ${y}</div><table>`;
    if (periode.length > 0) {
      html += '<tr><th></th><th>Value</th>' + periode.map(p => `<th>${p}d</th>`).join('') + '</tr>';
    }
    for (const b of baris) {
      html += `<tr><td>${contohWarna(b.spec)}${esc(b.label)}</td><td class="v">${b.nilai}</td>`
        + periode.map(p => `<td class="v">${b.kolom.get(p) || ''}</td>`).join('') + '</tr>';
    }
    tipEl.innerHTML = html + '</table>';
  }

  // Pojok kiri atas area gambar; pindah ke kanan atas kalau kursor mendekati kotak.
  let kursorX = null;
  function posisikanTooltip() {
    const lebarSumbu = side => {
      const s = panes.main.priceScale(side);
      return s.options().visible ? s.width() : 0;
    };
    const lebar = tipEl.offsetWidth;
    const kiri = lebarSumbu('left') + 8;
    const kanan = document.body.clientWidth - lebarSumbu('right') - 8 - lebar;
    const dekat = kursorX !== null && kursorX < kiri + lebar + 24;
    tipEl.style.left = (dekat ? Math.max(kiri, kanan) : kiri) + 'px';
    tipEl.style.top = (panesEl.offsetTop + 8) + 'px';
  }

  let paneAktif = null;
  for (const chart of charts) {
    chart.subscribeCrosshairMove(param => {
      const i = param && param.time && param.point ? indeksTanggal.get(teksWaktu(param.time)) : undefined;
      if (i === undefined) {
        // Hanya pane yang sedang memegang tooltip yang boleh menyembunyikannya; saat kursor
        // pindah pane, pane lama melapor "kosong" setelah pane baru sudah mengisinya.
        if (paneAktif === chart) { tipEl.style.display = 'none'; paneAktif = null; }
        return;
      }
      paneAktif = chart;
      isiTooltip(i);
      tipEl.style.display = 'block';
      posisikanTooltip();
    });
  }
  panesEl.addEventListener('mousemove', event => {
    kursorX = event.clientX;
    if (tipEl.style.display === 'block') posisikanTooltip();
  });
  panesEl.addEventListener('mouseleave', () => { tipEl.style.display = 'none'; paneAktif = null; kursorX = null; });

  // Rentang waktu yang sedang tampil ikut disimpan bersama pilihan legend dan sorot.
  let simpanRangePending = false;
  panes.main.timeScale().subscribeVisibleTimeRangeChange(range => {
    // Jangan simpan apa pun sebelum tampilan awal beres, supaya rentang sementara
    // (saat lebar chart masih 0) tidak ikut tersimpan.
    if (!range || simpanRangePending || !tampilanAwalSelesai) return;
    simpanRangePending = true;
    setTimeout(() => {
      simpanRangePending = false;
      const sekarang = panes.main.timeScale().getVisibleLogicalRange();
      if (!sekarang) return;
      state.bars = { from: sekarang.from, to: sekarang.to };
      state.sig = dataSig;
      delete state.range;   // format lama (tanggal)
      writeState(state);
    }, 300);
  });

  // Garis tangga hanya terlihat kalau satu hari memakan beberapa piksel. Saat zoom jauh
  // anak tangganya mustahil tampak dan garisnya jadi mirip garis biasa yang lebih tebal,
  // jadi pada zoom itu polanya diganti putus-putus panjang. Datanya tidak diubah.
  // Ambang dinaikkan supaya bentuk tangga baru dipakai saat anak tangganya benar-benar
  // lebar; di bawah itu polanya putus panjang, bukan tangga yang nyaris rata.
  const PIKSEL_PER_BAR_TANGGA = 6;
  const garisTangga = handles.filter(h => h.spec.steps);
  let polaTanggaSekarang = null;

  function sesuaikanTangga() {
    if (garisTangga.length === 0) return;
    const ts = panes.main.timeScale();
    const rentang = ts.getVisibleLogicalRange();
    const lebar = ts.width();
    if (!rentang || lebar <= 0) return;
    const perBar = lebar / Math.max(1, rentang.to - rentang.from);
    const pola = perBar >= PIKSEL_PER_BAR_TANGGA ? 0 : 3;   // 0 = penuh, 3 = putus panjang
    if (pola === polaTanggaSekarang) return;
    polaTanggaSekarang = pola;
    for (const handle of garisTangga) handle.line.applyOptions({ lineStyle: pola });
  }

  sesuaikanTangga();
  panes.main.timeScale().subscribeVisibleLogicalRangeChange(() => sesuaikanTangga());

  // Mode sorot: menarik area chart ke atas/bawah menggeser semua sumbu milik garis yang
  // disorot di pane itu (kiri, kanan, atau keduanya dengan jarak yang sama).
  // Tanpa sorotan, perilaku bawaan library berlaku.
  // Library 4.x tidak punya perintah untuk mengatur rentang sumbu harga, jadi rentangnya
  // dikunci lewat autoscaleInfoProvider pada semua garis di sumbu tersebut.
  // Klik dua kali di chart mengembalikan semua sumbu ke Auto.
  const sideOf = spec => spec.pane === 'price' ? 'right' : spec.axis;
  const seriesOn = (pane, side) =>
    handles.filter(h => h.spec.pane === pane && sideOf(h.spec) === side).map(h => h.line);
  const locked = new Map();

  function paneHeight(pane) {
    const cell = document.getElementById(pane).querySelector('tr > td:nth-child(2)');
    return cell ? cell.clientHeight : 0;
  }

  function lockScale(pane, side, lo, hi) {
    locked.set(pane + ':' + side, { lo, hi });
    panes[pane].priceScale(side).applyOptions({ autoScale: true });
    for (const line of seriesOn(pane, side)) {
      line.applyOptions({ autoscaleInfoProvider: () => ({ priceRange: { minValue: lo, maxValue: hi } }) });
    }
  }

  // Rentang harga yang sedang tampil, di luar margin atas/bawah bawaan sumbu.
  function visibleRange(pane, side) {
    const saved = locked.get(pane + ':' + side);
    if (saved && panes[pane].priceScale(side).options().autoScale) return saved;
    const line = seriesOn(pane, side)[0];
    const margins = panes[pane].priceScale(side).options().scaleMargins;
    const height = paneHeight(pane);
    const lo = line.coordinateToPrice(height * (1 - margins.bottom));
    const hi = line.coordinateToPrice(height * margins.top);
    return lo === null || hi === null ? null : { lo, hi };
  }

  function resetScales() {
    locked.clear();
    for (const { line } of handles) line.applyOptions({ autoscaleInfoProvider: original => original() });
    charts.forEach(chart => ['left', 'right'].forEach(side =>
      chart.priceScale(side).applyOptions({ autoScale: true })));
  }

  // Sumbu baru dikunci setelah tarikan jelas ke atas/bawah. Klik biasa atau geser ke
  // samping tidak mengunci apa pun, supaya sumbu tetap Auto saat chart digeser.
  const VERTICAL_START = 6;   // piksel
  let pending = null;
  let drag = null;

  function startDrag({ pane, sides }, y) {
    // Sumbu lain yang sedang manual dikunci dulu, supaya tidak ikut digeser library.
    for (const other of ['left', 'right']) {
      if (sides.includes(other) || seriesOn(pane, other).length === 0) continue;
      if (!panes[pane].priceScale(other).options().autoScale) {
        const r = visibleRange(pane, other);
        if (r) lockScale(pane, other, r.lo, r.hi);
      }
    }

    const height = paneHeight(pane);
    const targets = [];
    for (const side of sides) {
      const range = visibleRange(pane, side);
      if (!range) continue;
      const scale = panes[pane].priceScale(side);
      const margins = scale.options().scaleMargins;
      lockScale(pane, side, range.lo, range.hi);
      targets.push({
        side, lo: range.lo, hi: range.hi,
        yLo: height * (1 - margins.bottom), yHi: height * margins.top,
        log: scale.options().mode === 1 && range.lo > 0,
      });
    }
    return targets.length > 0 ? { pane, y, targets } : null;
  }

  for (const pane of Object.keys(panes)) {
    const el = document.getElementById(pane);
    el.addEventListener('mousedown', event => {
      if (event.button !== 0 || state.highlights.length === 0) return;
      // Hanya area gambar (kolom tengah baris pertama), bukan angka sumbu.
      const cell = event.target.closest('td');
      if (!cell || cell.cellIndex !== 1 || cell.parentElement.rowIndex !== 0) return;
      const sides = [...new Set(handles
        .filter(h => h.spec.pane === pane && state.highlights.includes(h.spec.name))
        .map(h => sideOf(h.spec)))];
      if (sides.length === 0) return;
      pending = { pane, sides, x: event.clientX, y: event.clientY };
    }, true);
    el.addEventListener('dblclick', resetScales);
  }

  document.addEventListener('mousemove', event => {
    if (!drag && !pending) return;
    if (event.buttons === 0) { drag = null; pending = null; return; }
    if (!drag) {
      const dx = event.clientX - pending.x;
      const dy = event.clientY - pending.y;
      if (Math.abs(dy) >= VERTICAL_START && Math.abs(dy) > Math.abs(dx)) {
        drag = startDrag(pending, pending.y);   // dihitung dari titik klik: garis ikut kursor
        pending = null;
      } else if (Math.abs(dx) >= VERTICAL_START) {
        pending = null;   // geser ke samping: biarkan library yang mengurus
      }
      return;
    }
    const dy = event.clientY - drag.y;
    // Rentang baru dihitung dari posisi awal tarikan supaya galat tidak menumpuk.
    for (const t of drag.targets) {
      const toScale = v => t.log ? Math.log10(v) : v;
      const fromScale = v => t.log ? Math.pow(10, v) : v;
      const priceAt = y => fromScale(toScale(t.hi)
        + (y - t.yHi) * (toScale(t.lo) - toScale(t.hi)) / (t.yLo - t.yHi));
      lockScale(drag.pane, t.side, priceAt(t.yLo - dy), priceAt(t.yHi - dy));
    }
  });
  document.addEventListener('mouseup', () => { drag = null; pending = null; });
  window.addEventListener('blur', () => { drag = null; pending = null; });

  window.__chart = { charts, handles, locked, resetScales, bootedAt: Date.now() };
}).catch(err => {
  document.getElementById('err').textContent = 'Chart gagal dimuat: ' + err.message;
});
</script>
"""


def _num(value):
    if pd.isna(value):
        return None
    value = float(value)
    return round(value, 2) if abs(value) >= 1000 else round(value, 4)


def _scale(mode):
    """Auto/Linear/Log ke opsi priceScale lightweight-charts."""
    return {"mode": 1 if mode == "Log" else 0, "autoScale": mode != "Linear"}


def render(df, lines, price_line, extra_lines, height, metric_mode, price_mode, store_key):
    """Gambar chart.

    price_line: garis harga BTC bila dipisah ke pane sendiri (pane paling atas).
    extra_lines: garis untuk pane tambahan paling bawah (mis. Z-Score), atau kosong.
    Tinggi dibagi menurut jumlah pane; perbandingannya dipakai lagi saat layar penuh.
    """
    extra_lines = extra_lines or []
    specs = [dict(vars(ln), pane="main") for ln in lines]
    specs += [dict(vars(ln), pane="extra") for ln in extra_lines]
    if price_line is not None:
        specs.insert(0, dict(vars(price_line), pane="price"))

    columns = {spec["col"] for spec in specs}
    payload = {
        "t": df["Date"].dt.strftime("%Y-%m-%d").tolist(),
        "cols": {col: [_num(v) for v in df[col]] for col in columns},
    }

    # Sumbu yang isinya hanya harga BTC memakai skala harga. Kalau harga berbagi sumbu
    # dengan metrik (halaman yang metriknya sendiri berupa harga), skala metrik yang
    # dipakai supaya satu sumbu tidak punya dua aturan.
    def _mode_sumbu(side):
        harga = any(ln.axis == side and ln.group == "BTC Price" for ln in lines)
        metrik = any(ln.axis == side and ln.group != "BTC Price" for ln in lines)
        return price_mode if harga and not metrik else metric_mode

    # Pembagian tinggi: pane harga dan pane tambahan mengambil porsi tetap, sisanya
    # untuk pane metrik yang tetap jadi yang terbesar.
    porsi_harga = 0.30 if price_line is not None and extra_lines else 0.45
    tinggi_harga = int(height * porsi_harga) if price_line is not None else 0
    tinggi_extra = int(height * (0.25 if price_line is not None else 0.30)) if extra_lines else 0

    daftar_pane = []
    if price_line is not None:
        daftar_pane.append({"id": "price", "height": tinggi_harga,
                            "left": _scale(price_mode), "right": _scale(price_mode)})
    daftar_pane.append({"id": "main", "height": height - tinggi_harga - tinggi_extra,
                        "left": _scale(_mode_sumbu("left")), "right": _scale(_mode_sumbu("right"))})
    if extra_lines:
        # Pane Z-Score selalu linear: angkanya melewati nol, jadi skala log tidak berlaku.
        daftar_pane.append({"id": "extra", "height": tinggi_extra,
                            "left": _scale("Auto"), "right": _scale("Auto")})

    banyak_pane = len(daftar_pane) > 1
    jarak = PANE_GAP * (len(daftar_pane) - 1)
    total_height = TOOLBAR_H + height + jarak
    config = {
        "store": store_key,
        "panes": daftar_pane,
        # Tinggi bingkai tetap; tinggi pane dihitung ulang di browser dari tinggi baris
        # legend yang sebenarnya (bisa lebih dari satu baris).
        "frameHeight": total_height,
        # Semua pane menampilkan sisi sumbu yang sama supaya area gambarnya sejajar.
        "showLeft": any(ln.axis == "left" for ln in lines) or banyak_pane,
        "showRight": any(ln.axis == "right" for ln in lines) or banyak_pane,
    }

    html = (TEMPLATE
            .replace("__TOOLBAR__", str(TOOLBAR_H))
            .replace("__GAP__", str(PANE_GAP))
            .replace("__DATA__", json.dumps(payload, separators=(",", ":")))
            .replace("__SPECS__", json.dumps(specs))
            .replace("__CONFIG__", json.dumps(config))
            .replace("__URLS__", json.dumps(LWC_URLS)))

    # st.iframe menggantikan components.html yang dijadwalkan dihapus Streamlit.
    embed = getattr(st, "iframe", None)
    if embed is not None:
        embed(html, height=total_height)
    else:
        components.html(html, height=total_height)
