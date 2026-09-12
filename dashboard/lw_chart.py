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
  #bar { display: flex; align-items: center; gap: 12px; height: __TOOLBAR__px; box-sizing: border-box; }
  #legend { flex: 1; min-width: 0; display: flex; flex-wrap: wrap; gap: 1px 10px;
            align-content: center; overflow: hidden; }
  .lgroup { display: inline-flex; align-items: center; gap: 3px; flex: none; }
  .lgdot { font-size: 11px; padding: 1px 5px; border: 1px solid #232838; border-radius: 5px;
           line-height: 1.2; color: #b9c3cd; }
  #hl { display: flex; gap: 4px; align-items: center; flex: none; }
  /* Sempat diredupkan ke 11px #6E7681 supaya beda dari tombol di sebelahnya; dicoba dan
     ditolak karena jadi sulit dibaca. Dibiarkan setara tombol. */
  .hllabel { font-size: 12px; color: #8B949E; margin-right: 2px; }
  button { cursor: pointer; font: 12px Inter, system-ui, sans-serif; background: transparent;
           border: 1px solid transparent; border-radius: 6px; padding: 3px 8px; color: #e2e8ef; }
  .lg { display: inline-flex; align-items: center; gap: 6px; flex: none; }
  .sw { width: 14px; height: 0; display: inline-block; }
  .off { opacity: 0.62; text-decoration: line-through; }
  .hl { color: #8B949E; border-color: #232838; }
  .hl.on { background: rgba(0, 109, 119, 0.40); border-color: #006d77; color: #fff; }
  #top { height: __TOP__px; margin-bottom: __GAP__px; }
  #main { height: __MAIN__px; }
  #err { color: #DA3633; padding: 16px; }
</style>
<div id="bar">
  <div id="legend"></div>
  <!-- "Highlight" adalah keterangan, bukan tombol. Warnanya diturunkan satu tingkat
       dari tombol di sebelahnya supaya tidak terbaca sebagai tombol yang sedang mati. -->
  <div id="hl"><span class="hllabel">Highlight</span></div>
</div>
<div id="top"></div>
<div id="main"></div>
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

  // Di mode Separate pane kedua pane wajib punya sumbu kiri dan kanan yang sama.
  // Kalau pane harga hanya bersumbu kanan dan pane metrik hanya bersumbu kiri, area
  // gambarnya bergeser sehingga tanggal yang sama jatuh di posisi berbeda.
  const multi = C.topHeight > 0;
  if (multi) {
    panes.top = LC.createChart(document.getElementById('top'),
      chartOptions(C.topHeight, C.topScale, C.topScale, C.showLeft, true, false));
    charts.push(panes.top);
  } else {
    document.getElementById('top').style.display = 'none';
  }
  panes.main = LC.createChart(document.getElementById('main'),
    chartOptions(C.mainHeight, C.leftScale, C.rightScale, C.showLeft, C.showRight || multi, true));
  charts.push(panes.main);

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
    const line = panes[spec.pane].addLineSeries({
      color: baseColor(spec),
      lineWidth: spec.width,
      lineStyle: spec.style,
      lineType: spec.steps ? 1 : 0,
      priceScaleId: spec.pane === 'top' ? 'right' : spec.axis,
      title: spec.group ? spec.name : '',
      priceLineVisible: false,
      lastValueVisible: !!spec.group,
      crosshairMarkerVisible: !!spec.group,
    });
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
  let syncPending = false;
  function syncScaleWidths() {
    syncPending = false;
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
  function scheduleScaleSync() {
    if (charts.length < 2 || syncPending) return;
    syncPending = true;
    requestAnimationFrame(() => requestAnimationFrame(syncScaleWidths));
  }
  scheduleScaleSync();

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

  new ResizeObserver(() => {
    charts.forEach(chart => chart.applyOptions({ width: document.body.clientWidth }));
    if (!tampilanAwalSelesai) tampilkanAwal();
    scheduleScaleSync();
  }).observe(document.body);

  const legendItems = handles.filter(h => h.spec.group);
  const groups = [...new Set(legendItems.map(h => h.spec.group))];
  // Beberapa garis bisa disorot sekaligus. Penyimpanan lama berisi satu nama
  // (highlight: 'MVRV' atau 'none'), jadi diubah ke daftar bila masih format lama.
  const saved = readState();
  const savedHighlights = Array.isArray(saved.highlights) ? saved.highlights
    : (saved.highlight && saved.highlight !== 'none' ? [saved.highlight] : []);
  const state = Object.assign({}, saved, {
    highlights: savedHighlights.filter(group => groups.includes(group)),
    hidden: Array.isArray(saved.hidden) ? saved.hidden : [],
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
    const utama = anggota.find(h => h.spec.name === group) || anggota[0];
    const wadah = document.createElement('span');
    wadah.className = 'lgroup';

    const button = document.createElement('button');
    button.className = 'lg';
    const swatch = document.createElement('span');
    swatch.className = 'sw';
    swatch.style.borderTop = `${utama.spec.alpha < 1 ? 3 : 2}px `
      + `${utama.spec.style === 1 ? 'dotted' : utama.spec.style ? 'dashed' : 'solid'} `
      + `${baseColor(utama.spec)}`;
    button.append(swatch, document.createTextNode(group));
    button.onclick = () => toggleHidden(utama.spec.name);
    wadah.appendChild(button);
    legendButtons.push({ button, handle: utama });

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
  const hlButtons = ['none'].concat(groups).map(group => {
    const button = document.createElement('button');
    button.className = 'hl';
    button.textContent = group === 'none' ? 'None' : group.split(' ')[0];
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
  const sideOf = spec => spec.pane === 'top' ? 'right' : spec.axis;
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


def render(df, lines, price_line, height, metric_mode, price_mode, store_key):
    """Gambar chart; price_line berisi Line harga BTC bila dipisah ke pane sendiri."""
    specs = [dict(vars(ln), pane="main") for ln in lines]
    if price_line is not None:
        specs.insert(0, dict(vars(price_line), pane="top"))

    columns = {spec["col"] for spec in specs}
    payload = {
        "t": df["Date"].dt.strftime("%Y-%m-%d").tolist(),
        "cols": {col: [_num(v) for v in df[col]] for col in columns},
    }

    top_height = int(height * 0.45) if price_line is not None else 0
    main_height = height - top_height
    # Sumbu yang isinya hanya harga BTC memakai skala harga. Kalau harga berbagi sumbu
    # dengan metrik (halaman yang metriknya sendiri berupa harga), skala metrik yang
    # dipakai supaya satu sumbu tidak punya dua aturan.
    def _mode_sumbu(side):
        harga = any(ln.axis == side and ln.group == "BTC Price" for ln in lines)
        metrik = any(ln.axis == side and ln.group != "BTC Price" for ln in lines)
        return price_mode if harga and not metrik else metric_mode

    config = {
        "store": store_key,
        "topHeight": top_height,
        "mainHeight": main_height,
        "topScale": _scale(price_mode),
        "leftScale": _scale(_mode_sumbu("left")),
        "rightScale": _scale(_mode_sumbu("right")),
        "showLeft": any(ln.axis == "left" for ln in lines),
        "showRight": any(ln.axis == "right" for ln in lines),
    }

    html = (TEMPLATE
            .replace("__TOOLBAR__", str(TOOLBAR_H))
            .replace("__TOP__", str(top_height))
            .replace("__MAIN__", str(main_height))
            .replace("__GAP__", str(PANE_GAP if top_height else 0))
            .replace("__DATA__", json.dumps(payload, separators=(",", ":")))
            .replace("__SPECS__", json.dumps(specs))
            .replace("__CONFIG__", json.dumps(config))
            .replace("__URLS__", json.dumps(LWC_URLS)))

    total_height = TOOLBAR_H + height + (PANE_GAP if top_height else 0)
    # st.iframe menggantikan components.html yang dijadwalkan dihapus Streamlit.
    embed = getattr(st, "iframe", None)
    if embed is not None:
        embed(html, height=total_height)
    else:
        components.html(html, height=total_height)
