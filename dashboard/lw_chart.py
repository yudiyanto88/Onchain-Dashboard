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
NAV_H = 52          # slider rentang di bawah chart; diambil dari tinggi pane, bukan ditambahkan
NAV_COL = "BTC Price"

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
  /* Slider rentang (navigator): paling bawah, di bawah sumbu tanggal. */
  #nav { margin-top: __GAP__px; }
  /* pan-y: geser jari atas-bawah di slider tetap menggulir halaman; kiri-kanan untuk slider. */
  #nav canvas { display: block; touch-action: pan-y; }
  /* Tooltip: angka di tanggal bawah kursor. Posisinya dipilih lewat kotak Tooltip
     (Fixed / Cursor / Off, lihat posisikanTooltip). Satu baris per metrik; periode
     smoothing jadi kolom. */
  #tip { position: absolute; z-index: 5; pointer-events: none; display: none;
         background: rgba(28, 34, 48, 0.94); border: 1px solid #2a2e39; border-radius: 6px;
         padding: 6px 10px; font-size: 12px; line-height: 1.55; color: #c9d1d9; white-space: nowrap; }
  #tip .tgl { color: #fff; font-weight: 600; margin-bottom: 2px; }
  #tip table { border-collapse: collapse; }
  #tip td, #tip th { padding: 0 0 0 14px; text-align: right; font-variant-numeric: tabular-nums; }
  #tip td:first-child, #tip th:first-child { padding-left: 0; text-align: left; }
  #tip th { font-weight: 400; color: #8b949e; font-size: 11px; }
  #tip .v { color: #fff; font-weight: 600; }
  /* Kolom pelengkap (Loss = 100 − Profit) sedikit diredupkan: turunan dari angka di kirinya. */
  #tip .v.sisa { color: #aeb6c2; }
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
<div id="nav"></div>
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
function angka(v, p, bulatDari) {
  if (v === null || v === undefined || !isFinite(v)) return '';
  // bulatDari (whole_from di registry): angka sebesar ini ke atas ditulis tanpa desimal.
  // Dipakai LTH-SOPR, yang dekat 1 butuh 3 desimal tapi bisa melonjak ke ratusan.
  if (bulatDari !== null && bulatDari !== undefined && Math.abs(v) >= bulatDari) {
    return v.toLocaleString('en-US', { maximumFractionDigits: 0 });
  }
  let min = p, max = p;
  if (p === 0 && Math.abs(v) < 100) {
    // Skala Log bisa membuat tick semu sedikit di bawah nol di dasar sumbu ("-0.0001"):
    // tidak diberi label. Harga di bawah 0.01 (level 2010, mis. CVDD 0.0011) ditulis
    // dengan 2 angka penting supaya tidak jadi "0.00".
    // Hanya tick semu mendekati nol yang dikosongkan: 0 tetap "0" di sumbu linear, dan
    // angka negatif sungguhan (mis. net flow nanti) tetap tampil.
    if (v === 0) return '0';
    if (v < 0 && v > -0.01) return '';
    if (v > 0 && v < 0.01) return String(Number(v.toPrecision(2)));
    // Di bawah 1 sampai 4 desimal tapi nol di belakang dibuang: 0.60 dan 0.0495, bukan 0.6000.
    min = 2;
    max = Math.abs(v) < 1 ? 4 : 2;
  }
  return v.toLocaleString('en-US', { minimumFractionDigits: min, maximumFractionDigits: max });
}
function formatSeri(spec) {
  const p = Number.isInteger(spec.precision) ? spec.precision : 2;
  return { type: 'custom', minMove: p === 0 ? 0.0001 : Math.pow(10, -p),
           formatter: v => angka(v, p, spec.whole_from) };
}
function angkaSeri(spec, v) { return angka(v, spec.precision, spec.whole_from); }

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
    // Geser jari atas-bawah di chart menggulir halaman, bukan chart (15 Sep 2026): di HP chart
    // menutupi hampir seluruh layar, jadi halaman nyaris tidak bisa digulir. Geser kiri-kanan
    // dan cubit dua jari tetap untuk chart. Mouse dan roda gulir tidak terpengaruh.
    handleScroll: { vertTouchDrag: false },
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

  // ---------------------------------------------------------------- slider rentang
  // Gaya navigator TradingView (disetujui user 14 Sep 2026): seluruh data chart digambar
  // mini (BTC Price, skala Log) dengan jendela teal yang bisa digeser dan diubah lebarnya.
  // Digambar di kanvas biasa, bukan chart kedua: letak horizontalnya diambil langsung dari
  // area gambar chart (lebar sumbu kiri + lebar skala waktu), jadi selalu selebar chart
  // tanpa perlu ikut sinkron lebar sumbu. Rentang logis 0 .. N-1 = seluruh lebar slider, sama
  // dengan hasil fitContent() di chart (Range All = jendela penuh).
  // Hidup di dalam chart: menggeser slider tidak memicu rerun Streamlit.
  let gambarNav = () => {};
  if (C.nav && D.t.length > 1) {
    const navEl = document.getElementById('nav');
    const kanvas = document.createElement('canvas');
    navEl.appendChild(kanvas);
    const ctx = kanvas.getContext('2d');
    const N = D.t.length;
    const TINGGI_NAV = C.navHeight;
    const MIN_BAR = 8;                        // jendela tersempit
    const PEGANGAN_W = 9, PEGANGAN_H = 26;    // pegangan kiri/kanan
    const JANGKAU_PEGANGAN = 7;               // jarak kursor ke tepi jendela yang masih menangkap pegangan
    const chartBawah = charts[charts.length - 1];   // skala waktunya yang terlihat

    let lmin = Infinity, lmax = -Infinity;
    const logNilai = D.cols[C.nav].map(v => {
      if (v === null || !(v > 0)) return null;
      const l = Math.log10(v);
      if (l < lmin) lmin = l;
      if (l > lmax) lmax = l;
      return l;
    });
    if (!(lmax > lmin)) { lmin -= 1; lmax += 1; }

    function geometri() {
      const kiriScale = chartBawah.priceScale('left');
      const kanan = chartBawah.priceScale('right');
      const kiri = kiriScale.options().visible ? kiriScale.width() : 0;
      let lebar = chartBawah.timeScale().width();
      if (!(lebar > 0)) {
        lebar = document.body.clientWidth - kiri - (kanan.options().visible ? kanan.width() : 0);
      }
      return { kiri, lebar };
    }
    const xDari = (g, logis) => g.kiri + logis * g.lebar / (N - 1);
    const logisDari = (g, x) => (x - g.kiri) * (N - 1) / g.lebar;
    // Jendela dijaga di dalam data; lebarnya tidak berubah saat digeser mentok ke tepi.
    function batasi(from, to) {
      const w = to - from;
      if (w >= N - 1) return { from: 0, to: N - 1 };
      if (from < 0) return { from: 0, to: w };
      if (to > N - 1) return { from: N - 1 - w, to: N - 1 };
      return { from, to };
    }

    function lukis() {
      const lebarCss = document.body.clientWidth;
      const dpr = window.devicePixelRatio || 1;
      if (kanvas.width !== Math.round(lebarCss * dpr) || kanvas.height !== Math.round(TINGGI_NAV * dpr)) {
        kanvas.width = Math.round(lebarCss * dpr);
        kanvas.height = Math.round(TINGGI_NAV * dpr);
        kanvas.style.width = lebarCss + 'px';
        kanvas.style.height = TINGGI_NAV + 'px';
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, lebarCss, TINGGI_NAV);
      const g = geometri();
      if (!(g.lebar > 0)) return;

      ctx.save();
      ctx.beginPath();
      ctx.rect(g.kiri, 0, g.lebar, TINGGI_NAV);
      ctx.clip();
      ctx.fillStyle = '#161b26';
      ctx.fillRect(g.kiri, 0, g.lebar, TINGGI_NAV);

      // Area harga BTC (Log): ruang 6 px di atas, 2 px di bawah.
      const atas = 6, bawah = TINGGI_NAV - 2;
      const yDari = l => atas + (1 - (l - lmin) / (lmax - lmin)) * (bawah - atas);
      const garis = new Path2D();
      let xAwal = null, xAkhir = null;
      for (let i = 0; i < N; i++) {
        if (logNilai[i] === null) continue;
        const x = xDari(g, i), y = yDari(logNilai[i]);
        if (xAwal === null) { garis.moveTo(x, y); xAwal = x; } else garis.lineTo(x, y);
        xAkhir = x;
      }
      if (xAwal !== null) {
        const area = new Path2D(garis);
        area.lineTo(xAkhir, TINGGI_NAV);
        area.lineTo(xAwal, TINGGI_NAV);
        area.closePath();
        ctx.fillStyle = 'rgba(91,107,128,0.35)';
        ctx.fill(area);
        ctx.strokeStyle = '#5b6b80';
        ctx.lineWidth = 1;
        ctx.stroke(garis);
      }

      const r = panes.main.timeScale().getVisibleLogicalRange();
      if (!r) { ctx.restore(); return; }
      const b = batasi(Math.max(0, r.from), Math.min(N - 1, r.to));
      const x1 = xDari(g, b.from), x2 = xDari(g, b.to);
      // Selubung gelap di luar jendela, isian teal tipis di dalamnya.
      ctx.fillStyle = 'rgba(10,12,18,0.62)';
      ctx.fillRect(g.kiri, 0, x1 - g.kiri, TINGGI_NAV);
      ctx.fillRect(x2, 0, g.kiri + g.lebar - x2, TINGGI_NAV);
      ctx.fillStyle = 'rgba(0,109,119,0.10)';
      ctx.fillRect(x1, 0, x2 - x1, TINGGI_NAV);
      ctx.strokeStyle = '#006d77';
      ctx.lineWidth = 1;
      ctx.strokeRect(Math.round(x1) + 0.5, 0.5, Math.max(0, Math.round(x2) - Math.round(x1) - 1), TINGGI_NAV - 1);
      ctx.restore();

      // Pegangan tidak dipotong batas area: di tepi data separuhnya menjorok ke sumbu.
      const yPeg = Math.round((TINGGI_NAV - PEGANGAN_H) / 2);
      for (const x of [x1, x2]) {
        const kiriPeg = Math.round(x - PEGANGAN_W / 2);
        ctx.fillStyle = '#006d77';
        ctx.beginPath();
        if (ctx.roundRect) ctx.roundRect(kiriPeg, yPeg, PEGANGAN_W, PEGANGAN_H, 3);
        else ctx.rect(kiriPeg, yPeg, PEGANGAN_W, PEGANGAN_H);
        ctx.fill();
        ctx.fillStyle = '#9fd4d8';
        ctx.fillRect(kiriPeg + 3, yPeg + 8, 1, PEGANGAN_H - 16);
        ctx.fillRect(kiriPeg + 5, yPeg + 8, 1, PEGANGAN_H - 16);
      }
    }
    gambarNav = lukis;

    function pasangRentang(from, to) {
      for (const chart of charts) {
        try { chart.timeScale().setVisibleLogicalRange({ from, to }); } catch (e) {}
      }
      lukis();
    }

    // Bagian slider di bawah kursor: pegangan kiri/kanan, jendela, atau area gelap.
    function bagianDi(x) {
      const g = geometri();
      const r = panes.main.timeScale().getVisibleLogicalRange();
      if (!r || !(g.lebar > 0)) return null;
      const b = batasi(Math.max(0, r.from), Math.min(N - 1, r.to));
      const x1 = xDari(g, b.from), x2 = xDari(g, b.to);
      // Pegangan menangkap sampai JANGKAU_PEGANGAN di luar jendela, tapi ke dalam paling
      // banyak sepertiga lebar jendela: jendela sempit tetap punya bagian tengah untuk digeser.
      const dalam = Math.min(JANGKAU_PEGANGAN, (x2 - x1) / 3);
      let jenis = 'lompat';
      if (x >= x1 - JANGKAU_PEGANGAN && x <= x1 + dalam) jenis = 'kiri';
      else if (x >= x2 - dalam && x <= x2 + JANGKAU_PEGANGAN) jenis = 'kanan';
      else if (x > x1 && x < x2) jenis = 'geser';
      return { jenis, g, from: b.from, to: b.to };
    }
    const KURSOR = { kiri: 'ew-resize', kanan: 'ew-resize', geser: 'grab', lompat: 'pointer' };
    const xKanvas = event => event.clientX - kanvas.getBoundingClientRect().left;

    let tarik = null;
    kanvas.addEventListener('pointerdown', event => {
      if (event.button !== 0) return;
      const x = xKanvas(event);
      const bagian = bagianDi(x);
      if (!bagian) return;
      let { jenis, from, to } = bagian;
      // Klik di area gelap: jendela dipindah berpusat di klik, lalu bisa langsung digeser.
      if (jenis === 'lompat') {
        const tengah = logisDari(bagian.g, x);
        const w = to - from;
        ({ from, to } = batasi(tengah - w / 2, tengah + w / 2));
        pasangRentang(from, to);
        jenis = 'geser';
      }
      tarik = { jenis, x, from, to };
      kanvas.style.cursor = jenis === 'geser' ? 'grabbing' : KURSOR[jenis];
      // Tarikan tidak putus walau kursor keluar dari slider.
      try { kanvas.setPointerCapture(event.pointerId); } catch (e) {}
      event.preventDefault();
    });
    kanvas.addEventListener('pointermove', event => {
      const x = xKanvas(event);
      if (!tarik) {
        const bagian = bagianDi(x);
        kanvas.style.cursor = bagian ? KURSOR[bagian.jenis] : 'default';
        return;
      }
      const g = geometri();
      if (!(g.lebar > 0)) return;
      const d = (x - tarik.x) * (N - 1) / g.lebar;   // piksel -> bar
      let from = tarik.from, to = tarik.to;
      if (tarik.jenis === 'geser') {
        ({ from, to } = batasi(from + d, to + d));
      } else if (tarik.jenis === 'kiri') {
        from = Math.max(0, Math.min(from + d, to - MIN_BAR));
      } else {
        to = Math.min(N - 1, Math.max(to + d, from + MIN_BAR));
      }
      pasangRentang(from, to);
    });
    const lepas = event => {
      if (!tarik) return;
      tarik = null;
      try { kanvas.releasePointerCapture(event.pointerId); } catch (e) {}
      const bagian = bagianDi(xKanvas(event));
      kanvas.style.cursor = bagian ? KURSOR[bagian.jenis] : 'default';
    };
    kanvas.addEventListener('pointerup', lepas);
    kanvas.addEventListener('pointercancel', lepas);

    // Zoom/geser di chart (mouse, tombol Range, pemulihan zoom) menggerakkan slider.
    panes.main.timeScale().subscribeVisibleLogicalRangeChange(() => lukis());
    lukis();
  }

  // Rentang tetap untuk garis metrik di pane utama (C.metricRange, mis. 0–100 untuk persen
  // supply): 50% selalu di tengah, apa pun Range-nya. Harga BTC tidak ikut. Kalau harga
  // dipindah ke sumbu yang sama, rentang sumbu itu jadi gabungan keduanya (bawaan library).
  const rentangTetap = spec => C.metricRange && spec.pane === 'main' && spec.group !== 'BTC Price'
    ? () => ({ priceRange: { minValue: C.metricRange[0], maxValue: C.metricRange[1] } })
    : null;

  // Pasangan nilai (C.complement, mis. Profit | Loss): tiap garis metrik di pane utama punya
  // kembaran 100 − nilai. Garis smoothing ikut tepat, karena rata-rata dari 100 − x =
  // 100 − rata-rata x (SMA maupun EMA). Harga BTC dan garis acuan tidak ikut.
  const [judulNilai, judulSisa] = C.complement || [null, null];
  const bisaDibalik = spec => !!C.complement && spec.pane === 'main'
    && !!spec.group && spec.group !== 'BTC Price';
  const namaSisa = teks => judulNilai ? teks.split(judulNilai).join(judulSisa) : teks;

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
    if (rentangTetap(spec)) {
      umum.autoscaleInfoProvider = rentangTetap(spec);
      // Angka di luar rentang (ruang tepi sumbu: 110, 120, -10) tidak ditulis — persen supply
      // tidak pernah di sana, jadi label itu hanya membingungkan.
      const [bawah, atas] = C.metricRange;
      const tulis = umum.priceFormat.formatter;
      umum.priceFormat = Object.assign({}, umum.priceFormat, {
        formatter: v => (v < bawah - 1e-9 || v > atas + 1e-9) ? '' : tulis(v),
      });
    }
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
    const handle = { spec, line };
    // Kembaran Loss: bentuk garis sama, lahir tersembunyi; nyala/warnanya diatur apply().
    if (bisaDibalik(spec)) {
      handle.kembar = panes[spec.pane].addLineSeries(Object.assign({
        lineWidth: spec.width,
        lineStyle: spec.style,
        lineType: spec.steps ? 1 : 0,
        crosshairMarkerVisible: true,
      }, umum, { title: namaSisa(spec.name), visible: false }));
      handle.kembar.setData(points.map(p => ({ time: p.time, value: 100 - p.value })));
    }
    handles.push(handle);
  }
  // Sumbu berentang tetap: ruang tepi bawaan (atas 20 %, bawah 10 %) dipersempit supaya
  // 0–100 memakai hampir seluruh tinggi pane dan tidak menyisakan pita kosong di atas 100.
  if (C.metricRange) {
    new Set(handles.filter(h => rentangTetap(h.spec)).map(h => h.spec.axis)).forEach(side =>
      panes.main.priceScale(side).applyOptions({ scaleMargins: { top: 0.06, bottom: 0.04 } }));
  }
  // Tampilan awal: pulihkan zoom terakhir, atau tampilkan seluruh data.
  // Sidik data ikut disimpan, jadi kalau rentang tanggalnya memang berubah
  // (tombol Range), zoom lama tidak dipakai.
  // fitContent() tidak bekerja selama lebar chart masih 0 (mis. panel belum tampil),
  // dan hasilnya chart berhenti di lebar bar bawaan (sekitar 160 hari terakhir).
  // Karena itu tampilan awal diulang sampai chart benar-benar punya lebar.
  // Posisi bar (logical range) dipakai, bukan tanggal: memulihkan tanggal membuat
  // tepi kiri bergeser sedikit tiap kali karena dibulatkan ke bar terdekat.
  // Chart menerima seluruh sejarah; kotak Range (C.view, tanggal) hanya menentukan rentang
  // yang tampil. Rentang Range ikut sidik data, jadi menekan Range tetap menang atas zoom
  // tersimpan, sedangkan rerun lain (smoothing, skala) memulihkan zoom terakhir.
  let rentangRange = null;
  if (C.view) {
    let dari = D.t.findIndex(t => t >= C.view[0]);
    let sampai = -1;
    for (let i = D.t.length - 1; i >= 0; i--) { if (D.t[i] <= C.view[1]) { sampai = i; break; } }
    if (dari < 0) dari = 0;
    if (sampai < dari) sampai = D.t.length - 1;
    rentangRange = { from: dari, to: sampai };
  }
  const dataSig = D.t.length + ':' + D.t[0] + ':' + D.t[D.t.length - 1]
    + (C.view ? ':' + C.view.join(':') : '');
  const simpanan = readState();
  const zoomSimpanan = simpanan.bars && simpanan.sig === dataSig ? simpanan.bars : null;
  // Target tampilan awal: zoom tersimpan, kalau tidak ada rentang dari kotak Range.
  const pulihkanZoom = zoomSimpanan || rentangRange;
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
    // Lebar sumbu menentukan letak area gambar, jadi slider digambar ulang di sini juga.
    gambarNav();
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
  // BTC Price selalu kelompok terakhir di legend, tombol sorot, dan tooltip. Saat Separate
  // pane seri harga disisipkan paling depan (pane atas), dan sebelum ini ikut tampil pertama.
  const groups = [...new Set(legendItems.map(h => h.spec.group))]
    .sort((a, b) => (a === 'BTC Price') - (b === 'BTC Price'));
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

  // Saklar Profit dan Loss (C.complement): dua-duanya bebas nyala/mati, termasuk mati
  // bersamaan (keputusan user 14 Sep 2026). Hidup di browser, tersimpan di localStorage.
  // Format lama (satu pilihan, state.inverse) dipindahkan sekali ke dua saklar ini.
  if (C.complement && typeof state.showProfit !== 'boolean') {
    state.showProfit = state.inverse !== true;
    state.showLoss = state.inverse === true;
  }
  delete state.inverse;
  // Garis smoothing Loss saat Profit dan Loss sama-sama menyala: mati di awal, dinyalakan
  // lewat kotak angka kedua di legend. Daftar berisi nama seri Profit induknya.
  state.lossShown = Array.isArray(state.lossShown) ? state.lossShown : [];
  const tampilProfit = () => !C.complement || state.showProfit;
  const tampilLoss = () => !!C.complement && state.showLoss;
  const hanyaLoss = () => tampilLoss() && !tampilProfit();
  const keduanyaMati = () => !!C.complement && !state.showProfit && !state.showLoss;
  const labelKelompok = [];
  const titikLoss = [];

  // Garis stroke contoh warna di legend, dengan warna tertentu.
  const garisContoh = (spec, warna) => `${spec.alpha < 1 ? 3 : 2}px `
    + `${spec.style === 1 ? 'dotted' : spec.style ? 'dashed' : 'solid'} `
    + `${spec.alpha < 1 ? dimmed(warna, spec.alpha) : warna}`;

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
    const teksKelompok = document.createTextNode(group);
    button.append(swatch);
    // Kelompok berpasangan: contoh warna kedua untuk Loss, tampil saat keduanya menyala.
    if (utama && utama.kembar) {
      const swatchSisa = document.createElement('span');
      swatchSisa.className = 'sw';
      swatchSisa.style.borderTop = garisContoh(utama.spec, utama.spec.complement_color || utama.spec.color);
      button.append(swatchSisa);
      labelKelompok.push({ node: teksKelompok, group, spec: utama.spec, swatch, swatchSisa });
    }
    button.append(teksKelompok);
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
      // Kotak kedua untuk smoothing Loss, bertepi warna Loss; hanya tampil saat Profit dan
      // Loss sama-sama menyala (kalau hanya Loss, kotak pertama yang mengaturnya).
      if (handle.kembar) {
        const kotak = document.createElement('button');
        kotak.className = 'lgdot';
        kotak.textContent = titik.textContent;
        kotak.title = namaSisa(handle.spec.name);
        kotak.style.borderColor = handle.spec.complement_color || handle.spec.color;
        kotak.onclick = () => {
          const nama = handle.spec.name;
          state.lossShown = state.lossShown.includes(nama)
            ? state.lossShown.filter(x => x !== nama) : state.lossShown.concat(nama);
          apply();
        };
        wadah.appendChild(kotak);
        titikLoss.push({ button: kotak, handle });
      }
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

  // Saklar Profit dan Loss di awal kelompok Highlight (letak B, dipilih user 14 Sep 2026),
  // dipisah garis tipis. Hanya ada di halaman yang punya pasangan nilai (C.complement).
  const saklar = [];
  if (C.complement) {
    const labelHighlight = hlEl.querySelector('.hllabel');
    for (const [judul, kunci] of [[judulNilai, 'showProfit'], [judulSisa, 'showLoss']]) {
      const button = document.createElement('button');
      button.className = 'hl';
      button.textContent = judul;
      button.title = `Show ${judul.toLowerCase()} lines (${judulNilai} + ${judulSisa} = 100)`;
      button.onclick = () => { state[kunci] = !state[kunci]; apply(); };
      hlEl.insertBefore(button, labelHighlight);
      saklar.push({ button, kunci });
    }
    const pemisah = document.createElement('span');
    pemisah.className = 'fssep';
    hlEl.insertBefore(pemisah, labelHighlight);
  }

  // Tombol layar penuh hidup di dalam chart, bukan di baris kontrol Streamlit.
  // Kliknya sudah merupakan gestur pengguna, jadi requestFullscreen() boleh dipanggil
  // langsung — tidak perlu skrip penyisip yang memasang pendengar ke tombol Streamlit,
  // dan tidak ada status di Python yang bisa hilang saat satu putaran terpotong.
  // Kerangka Streamlit disembunyikan oleh aturan CSS :fullscreen di app_v2.py.
  const IKON_PENUH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>';
  const IKON_KELUAR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5"/></svg>';
  const docInduk = () => { try { return window.parent.document; } catch (e) { return null; } };
  // Layar penuh semu (15 Sep 2026): Safari dan Chrome di iPhone tidak menyediakan Fullscreen
  // API untuk halaman, jadi tombol Full di sana hanya memasang kelas penuh-semu di halaman
  // induk. app.py memberi kelas itu aturan yang sama dengan :fullscreen, dan chart mengisi
  // sisa tinggi jendela seperti layar penuh biasa. Browser yang punya Fullscreen API
  // (laptop, Android) tidak pernah masuk jalur ini.
  const adaFullscreenApi = () => {
    const d = docInduk();
    return !!(d && d.documentElement.requestFullscreen && d.fullscreenEnabled);
  };
  const KELAS_SEMU = 'penuh-semu';
  // Kelas menempel di halaman induk, jadi tetap terbaca sesudah Streamlit membangun ulang chart.
  const sedangSemu = () => { const d = docInduk(); return !!(d && d.documentElement.classList.contains(KELAS_SEMU)); };
  const sedangPenuh = () => { const d = docInduk(); return !!(d && d.fullscreenElement) || sedangSemu(); };

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
    // Slider rentang (bila ada) juga diambil dari tinggi pane, bukan dari bingkai.
    const tinggiNav = C.nav ? C.navHeight + __GAP__ : 0;
    if (terapkanTinggi(tinggiBingkai - barEl.offsetHeight - __GAP__ * (C.panes.length - 1) - tinggiNav)) {
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
    fsBtn.title = penuh ? (sedangSemu() ? 'Leave full screen' : 'Leave full screen (Esc)') : 'Full screen';
    sesuaikanTinggiLayar();
  }
  fsBtn.onclick = () => {
    const d = docInduk();
    if (!d) return;
    if (sedangSemu() || !adaFullscreenApi()) {
      const masuk = !sedangSemu();
      d.documentElement.classList.toggle(KELAS_SEMU, masuk);
      // Halaman digulir ke atas supaya chart mulai tepat di bawah baris kontrol.
      if (masuk) {
        const utama = d.querySelector('[data-testid="stMain"]');
        if (utama) utama.scrollTop = 0;
        try { window.parent.scrollTo(0, 0); } catch (e) {}
      }
      perbaruiFs();
      // Tinggi dihitung ulang sesudah judul dan jarak halaman benar-benar berubah.
      setTimeout(perbaruiFs, 60);
      setTimeout(perbaruiFs, 300);
      return;
    }
    // Janji dari kedua perintah ini bisa ditolak browser; ditangkap supaya tidak
    // muncul sebagai error yang tidak tertangani di console.
    const janji = d.fullscreenElement ? d.exitFullscreen() : d.documentElement.requestFullscreen();
    if (janji && janji.catch) janji.catch(() => {});
  };
  perbaruiFs();
  hlEl.append(fsSep);

  // Saklar Scale, khusus perangkat sentuh (15 Sep 2026, ikon "geser vertikal" pilihan user).
  // Bawaannya geser jari atas-bawah menggulir halaman (vertTouchDrag mati, lihat
  // chartOptions). Saat saklar menyala, geser jari atas-bawah kembali menggeser skala chart.
  // Tidak disimpan: setiap chart dibuka saklar mati, supaya halaman tidak "terkunci" diam-diam.
  // Perangkat dengan mouse sebagai penunjuk utama (laptop) tidak mendapat tombol ini.
  const sentuh = (() => { try { return window.matchMedia('(pointer: coarse)').matches; } catch (e) { return false; } })();
  if (sentuh) {
    const IKON_SKALA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l3 3l3-3M12 15v6M15 6l-3-3l-3 3M12 3v6"/></svg>';
    const skalaBtn = document.createElement('button');
    skalaBtn.className = 'hl fsbtn';
    skalaBtn.innerHTML = IKON_SKALA + 'Scale';
    let geserSkala = false;
    const perbaruiSkala = () => {
      skalaBtn.classList.toggle('on', geserSkala);
      skalaBtn.title = geserSkala ? 'Vertical drag moves the scale (tap to scroll the page instead)'
        : 'Vertical drag scrolls the page (tap to move the scale instead)';
      charts.forEach(chart => chart.applyOptions({ handleScroll: { vertTouchDrag: geserSkala } }));
    };
    skalaBtn.onclick = () => { geserSkala = !geserSkala; perbaruiSkala(); };
    perbaruiSkala();
    hlEl.append(skalaBtn);
  }
  hlEl.append(fsBtn);
  // Esc keluar dari layar penuh tanpa melewati tombol ini, jadi tampilannya
  // disesuaikan dari peristiwa dokumen induk, bukan dari klik. Ukuran jendela juga
  // diikuti supaya chart tetap pas saat layar penuh dipindah ke monitor lain.
  const dInduk = docInduk();
  if (dInduk) dInduk.addEventListener('fullscreenchange', perbaruiFs);
  try { window.parent.addEventListener('resize', sesuaikanTinggiLayar); } catch (e) {}

  function apply() {
    // Tombol sorot hanya untuk kelompok yang punya garis menyala. Kelompok yang dimatikan
    // seluruhnya juga dilepas dari sorotan, supaya chart tidak meredupkan semua garis
    // demi garis yang tidak kelihatan.
    const kelompokMenyala = new Set(legendItems
      .filter(h => !state.hidden.includes(h.spec.name) && !(bisaDibalik(h.spec) && keduanyaMati()))
      .map(h => h.spec.group));
    state.highlights = state.highlights.filter(g => kelompokMenyala.has(g));
    for (const { button, group } of hlButtons) {
      if (group !== 'none') button.hidden = !kelompokMenyala.has(group);
    }
    const keduanya = tampilProfit() && tampilLoss();
    for (const { button, handle } of legendButtons) {
      const spec = handle.spec;
      const hidden = state.hidden.includes(spec.name);
      const faded = state.highlights.length > 0 && !state.highlights.includes(spec.group);
      const fadedAlpha = spec.dim * (spec.alpha < 1 ? spec.alpha : 1);
      const warna = hex => faded ? dimmed(hex, fadedAlpha)
        : (spec.alpha < 1 ? dimmed(hex, spec.alpha) : hex);
      handle.line.applyOptions({
        visible: !hidden && (!handle.kembar || tampilProfit()),
        color: warna(spec.color),
      });
      if (handle.kembar) {
        // Garis utama Loss ikut saklar legend induknya. Smoothing Loss: saat keduanya
        // menyala diatur kotak kedua (mati di awal); saat hanya Loss, ikut kotak pertama.
        const utama = spec.name === spec.group;
        const nyala = tampilLoss() && (utama || !keduanya ? !hidden
          : state.lossShown.includes(spec.name));
        handle.kembar.applyOptions({
          visible: nyala,
          // Warna Loss set B hanya saat keduanya menyala; kalau hanya Loss, warna kohort asli.
          color: warna(keduanya && spec.complement_color ? spec.complement_color : spec.color),
        });
      }
      button.classList.toggle('off', hidden);
    }
    for (const { button, handle } of titikLoss) {
      button.style.display = keduanya ? '' : 'none';
      button.classList.toggle('off', !state.lossShown.includes(handle.spec.name));
    }
    // Nama kelompok: keduanya -> nama pendek (Total) + dua contoh warna; hanya Loss ->
    // "Total in Loss"; selain itu nama asli ("Total in Profit").
    for (const { node, group, spec, swatch, swatchSisa } of labelKelompok) {
      node.textContent = keduanya ? (spec.short || group) : hanyaLoss() ? namaSisa(group) : group;
      swatchSisa.style.display = keduanya ? '' : 'none';
      swatch.style.display = '';
    }
    for (const { button, kunci } of saklar) button.classList.toggle('on', !!state[kunci]);
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
  const nilaiDi = (spec, i) => {
    const v = D.cols[spec.col][i];
    if (v === null) return null;
    return hanyaLoss() && bisaDibalik(spec) ? 100 - v : v;   // hanya Loss: kolom utama = Loss
  };
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
      // Saklar Profit dan Loss sama-sama mati: garis metrik tidak tampil, jadi barisnya juga tidak.
      const anggota = legendItems.filter(h => h.spec.group === group && !state.hidden.includes(h.spec.name)
        && !(bisaDibalik(h.spec) && keduanyaMati()));
      if (anggota.length === 0) continue;
      const utama = anggota.find(h => h.spec.name === group);
      const smoothing = anggota.filter(h => h !== utama && periodeDari(h.spec.name) !== null);
      const lainnya = anggota.filter(h => h !== utama && !smoothing.includes(h));
      if (utama || smoothing.length > 0) {
        const kolom = new Map();
        for (const h of smoothing) {
          const p = periodeDari(h.spec.name);
          semuaPeriode.add(p);
          kolom.set(p, angkaSeri(h.spec, nilaiDi(h.spec, i)));
        }
        const contoh = (utama || smoothing[0]).spec;
        const v = utama ? nilaiDi(utama.spec, i) : null;
        // Kolom pelengkap (C.complement, mis. Profit | Loss): Loss = 100 − Profit, hanya untuk
        // nilai utama metrik. Nama baris memakai nama pendek (Total · STH · LTH) supaya kotak
        // yang bertambah satu kolom tidak ikut melebar karena nama panjang.
        const lengkap = C.complement && group !== HARGA;
        baris.push({ label: lengkap && contoh.short ? contoh.short : group, spec: contoh,
                     nilai: utama ? angkaSeri(utama.spec, v) : '', kolom,
                     sisa: lengkap && v !== null ? angkaSeri(utama.spec, 100 - v) : '' });
      }
      // Kelompok tanpa garis utama (Rolling Z-Score 1y/2y/4y): satu baris mendatar, tiap
      // anggota yang ON jadi satu kolom dengan judul kecilnya sendiri (1y · 2y · 4y).
      if (lainnya.length > 0) {
        baris.push({ label: group, spec: lainnya[0].spec, jendela: lainnya.map(h => ({
          judul: (h.spec.name.split('(')[1] || h.spec.name).replace(')', ''),
          nilai: angkaSeri(h.spec, nilaiDi(h.spec, i)),
        })) });
      }
    }
    const periode = [...semuaPeriode].sort((a, b) => a - b);
    const [y, m, d] = D.t[i].split('-');
    let html = `<div class="tgl">${d} ${BULAN[+m - 1]} ${y}</div><table>`;
    // Judul kolom Profit | Loss hanya kalau ada baris metrik (saklar keduanya mati = tinggal BTC).
    if (periode.length > 0 || (C.complement && baris.some(b => b.label !== HARGA))) {
      // Hanya Loss yang menyala: urutan kolom dibalik jadi Loss | Profit.
      const [kolomNilai, kolomSisa] = !C.complement ? ['Value', null]
        : hanyaLoss() ? [judulSisa, judulNilai] : [judulNilai, judulSisa];
      html += `<tr><th></th><th>${esc(kolomNilai)}</th>`
        + (kolomSisa ? `<th>${esc(kolomSisa)}</th>` : '')
        + periode.map(p => `<th>${p}d</th>`).join('') + '</tr>';
    }
    for (const b of baris) {
      if (b.jendela) {
        // Judul kolom sendiri tepat di atas barisnya, supaya tidak tertukar dengan judul
        // periode smoothing (Value · 7d · 60d) di atas tabel.
        html += '<tr><th></th>' + b.jendela.map(j => `<th>${esc(j.judul)}</th>`).join('') + '</tr>'
          + `<tr><td>${contohWarna(b.spec)}${esc(b.label)}</td>`
          + b.jendela.map(j => `<td class="v">${j.nilai}</td>`).join('') + '</tr>';
        continue;
      }
      html += `<tr><td>${contohWarna(b.spec)}${esc(b.label)}</td><td class="v">${b.nilai}</td>`
        + (C.complement ? `<td class="v sisa">${b.sisa}</td>` : '')
        + periode.map(p => `<td class="v">${b.kolom.get(p) || ''}</td>`).join('') + '</tr>';
    }
    tipEl.innerHTML = html + '</table>';
  }

  // Posisi dipilih lewat kotak Tooltip (C.tooltip):
  //   Fixed  — pojok kiri atas area gambar; pindah ke kanan atas kalau kursor mendekati kotak.
  //   Cursor — di kiri garis kursor, tengahnya sejajar kursor (gaya ChartInspect). Kalau di
  //            kiri tidak cukup tempat, pindah ke kanan kursor supaya tidak keluar batas chart.
  //   Off    — tidak ditampilkan; garis silang dan label sumbu tetap ada.
  const JARAK_KURSOR = 16;
  let kursorX = null;
  let kursorY = null;
  function posisikanTooltip() {
    const lebarSumbu = side => {
      const s = panes.main.priceScale(side);
      return s.options().visible ? s.width() : 0;
    };
    const lebar = tipEl.offsetWidth;
    const kiri = lebarSumbu('left') + 8;
    const kanan = document.body.clientWidth - lebarSumbu('right') - 8 - lebar;
    if (C.tooltip === 'Cursor' && kursorX !== null && kursorY !== null) {
      const tinggi = tipEl.offsetHeight;
      let x = kursorX - JARAK_KURSOR - lebar;
      if (x < kiri) x = Math.min(kursorX + JARAK_KURSOR, Math.max(kiri, kanan));
      const atas = panesEl.offsetTop + 4;
      const bawah = panesEl.offsetTop + panesEl.offsetHeight - tinggi - 4;
      tipEl.style.left = x + 'px';
      tipEl.style.top = Math.max(atas, Math.min(bawah, kursorY - tinggi / 2)) + 'px';
      return;
    }
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
      if (C.tooltip === 'Off') return;
      paneAktif = chart;
      isiTooltip(i);
      tipEl.style.display = 'block';
      posisikanTooltip();
    });
  }
  panesEl.addEventListener('mousemove', event => {
    kursorX = event.clientX;
    kursorY = event.clientY;
    if (tipEl.style.display === 'block') posisikanTooltip();
  });
  panesEl.addEventListener('mouseleave', () => {
    tipEl.style.display = 'none'; paneAktif = null; kursorX = null; kursorY = null;
  });

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
    for (const handle of garisTangga) {
      handle.line.applyOptions({ lineStyle: pola });
      if (handle.kembar) handle.kembar.applyOptions({ lineStyle: pola });
    }
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
  // Kembaran Loss ikut dikunci: kalau tidak, rentangnya (0–100) bergabung dengan rentang
  // yang dikunci dan sumbu tidak bisa digeser.
  const seriesOn = (pane, side) =>
    handles.filter(h => h.spec.pane === pane && sideOf(h.spec) === side)
      .flatMap(h => h.kembar ? [h.line, h.kembar] : [h.line]);
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
    // Garis berentang tetap kembali ke rentang tetapnya, bukan ke Auto.
    for (const { spec, line, kembar } of handles) {
      const provider = rentangTetap(spec) || (original => original());
      line.applyOptions({ autoscaleInfoProvider: provider });
      if (kembar) kembar.applyOptions({ autoscaleInfoProvider: provider });
    }
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


def _num(value, digits=4):
    """digits: desimal yang dikirim untuk nilai < 1000. Bawaan 4; seri ber-precision
    lebih tinggi (gap STH-SOPR, 5 desimal) dikirim satu desimal lebih banyak supaya
    angka yang tampil tidak berasal dari nilai yang sudah dibulatkan."""
    if pd.isna(value):
        return None
    value = float(value)
    return round(value, 2) if abs(value) >= 1000 else round(value, digits)


def _scale(mode):
    """Auto/Linear/Log ke opsi priceScale lightweight-charts."""
    return {"mode": 1 if mode == "Log" else 0, "autoScale": mode != "Linear"}


def render(df, lines, price_line, extra_lines, height, metric_mode, price_mode, store_key,
           tooltip="Cursor", metric_range=None, complement=None, view=None):
    """Gambar chart.

    view: (tanggal awal, tanggal akhir) yang tampil saat chart dibuka — dari kotak Range.
    df selalu berisi seluruh sejarah; di luar view tetap bisa digeser/zoom dan tampil di slider.

    price_line: garis harga BTC bila dipisah ke pane sendiri (pane paling atas).
    extra_lines: garis untuk pane tambahan paling bawah (mis. Z-Score), atau kosong.
    Tinggi dibagi menurut jumlah pane; perbandingannya dipakai lagi saat layar penuh.
    """
    extra_lines = extra_lines or []
    specs = [dict(vars(ln), pane="main") for ln in lines]
    specs += [dict(vars(ln), pane="extra") for ln in extra_lines]
    if price_line is not None:
        specs.insert(0, dict(vars(price_line), pane="price"))

    digits = {}
    for spec in specs:
        digits[spec["col"]] = max(digits.get(spec["col"], 4), spec.get("precision", 2) + 1)
    # Slider rentang selalu berisi harga BTC, juga saat garis harganya Hidden. Halaman tanpa
    # kolom harga tidak mendapat slider.
    nav = NAV_COL in df.columns
    if nav:
        digits.setdefault(NAV_COL, 4)
    nav_h = NAV_H + PANE_GAP if nav else 0
    payload = {
        "t": df["Date"].dt.strftime("%Y-%m-%d").tolist(),
        "cols": {col: [_num(v, n) for v in df[col]] for col, n in digits.items()},
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
    # Tinggi total chart tetap; slider rentang mengambil tempatnya dari pane.
    tinggi_pane = height - nav_h
    porsi_harga = 0.30 if price_line is not None and extra_lines else 0.45
    tinggi_harga = int(tinggi_pane * porsi_harga) if price_line is not None else 0
    tinggi_extra = int(tinggi_pane * (0.25 if price_line is not None else 0.30)) if extra_lines else 0

    daftar_pane = []
    if price_line is not None:
        daftar_pane.append({"id": "price", "height": tinggi_harga,
                            "left": _scale(price_mode), "right": _scale(price_mode)})
    daftar_pane.append({"id": "main", "height": tinggi_pane - tinggi_harga - tinggi_extra,
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
        "tooltip": tooltip,   # "Fixed" / "Cursor" / "Off"
        "metricRange": list(metric_range) if metric_range else None,  # sumbu metrik tetap
        "complement": list(complement) if complement else None,       # kolom Profit | Loss
        "nav": NAV_COL if nav else None,   # kolom isi slider rentang
        "navHeight": NAV_H,
        "view": list(view) if view else None,   # rentang tampil awal (kotak Range)
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
