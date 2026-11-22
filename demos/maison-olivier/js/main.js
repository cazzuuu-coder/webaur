(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const CAPTURE = !!window.__capture; // deterministic recording mode

  const P = [
    { id:'vierge',   name:'Vierge',    fr:'Huile d’Olive Vierge Extra', notes:'Green almond, artichoke, peppery finish', desc:'Our house oil. Green almond, artichoke and a gentle peppery finish — for every day.', price:'€28', size:'500 ml', h:1,   bg:'#34401f', ink:'#efe6d2', arch:'#47562e', tag:'Olive oil' },
    { id:'citron',   name:'Citron',    fr:'Huile d’Olive au Citron',    notes:'Whole lemons, cold-pressed with the olives', desc:'Pressed together with whole lemons. Bright and floral — made for fish and summer salads.', price:'€22', size:'250 ml', h:.86, bg:'#d6a11e', ink:'#2b2108', arch:'#e1b33e', tag:'Infused oil' },
    { id:'tapenade', name:'Tapenade',  fr:'Tapenade Noire',             notes:'Black olives, capers, pounded by hand', desc:'Black olives and capers, pounded by hand in small batches. Spread thickly on warm bread.', price:'€12', size:'100 g',  h:.66, bg:'#ad5238', ink:'#f7ebdd', arch:'#ba6046', tag:'Preserve' },
    { id:'confits',  name:'Confits',   fr:'Citrons Confits',            notes:'Lemons cured slowly in salt and bay', desc:'Whole lemons cured slowly in salt and bay leaf. Soft, sharp and deeply aromatic.', price:'€16', size:'250 g', h:.86, bg:'#78855a', ink:'#f5f0e1', arch:'#849166', tag:'Preserve' },
    { id:'grandcru', name:'Grand Cru', fr:'Huile d’Olive Grand Cru',     notes:'Single terrace, oldest trees', desc:'A single-terrace oil from our oldest trees, pressed once a year and tinned to keep out the light.', price:'€36', size:'500 ml', h:.92, bg:'#e7dbc4', ink:'#2b2a1c', arch:'#ddcfb3', tag:'Olive oil' },
    { id:'lavande',  name:'Lavande',   fr:'Miel de Lavande',            notes:'Pale, creamy, from the plateau', desc:'Pale, creamy honey from hives set among the lavender of the Haute-Provence plateau.', price:'€18', size:'250 g', h:.74, bg:'#877c9f', ink:'#f7f1ea', arch:'#9389aa', tag:'Honey' },
  ];
  const N = P.length, SLOTS = 18;

  /* ---------- build wheel ---------- */
  const wheel = $('.wheel');
  for (let i = 0; i < SLOTS; i++) {
    const p = P[i % N];
    const s = document.createElement('div');
    s.className = 'slot'; s.style.setProperty('--i', i);
    s.innerHTML = `<div class="prod" data-slot="${i}" style="--h:${p.h};--k:${i % 6}"><div class="prod__float"><img src="img/${p.id}.webp" alt="" draggable="false" decoding="async" ${i < 2 || i > 15 ? '' : 'loading="lazy"'}></div><span class="prod__label">${p.name} · ${p.price}</span></div>`;
    wheel.appendChild(s);
  }
  /* arch words */
  const archG = $('.arch__words'), NS = 'http://www.w3.org/2000/svg';
  P.forEach((p, i) => {
    const t = document.createElementNS(NS, 'text'); t.setAttribute('class', 'w' + (i === 0 ? ' is-on' : ''));
    const tp = document.createElementNS(NS, 'textPath'); tp.setAttribute('href', '#archPath'); tp.setAttribute('startOffset', '50%'); tp.textContent = p.name;
    t.appendChild(tp); archG.appendChild(t);
  });
  const words = $$('.arch .w');
  /* ring text */
  const ring = $('.ring');
  function buildRing() {
    const d = ring.getBoundingClientRect().width || 1; const u = d / 200; // px per unit
    const fs = (innerWidth < 760 ? 10 : 11.5) / u; const r = 96; const C = 2 * Math.PI * r;
    const phrase = 'MAISON OLIVIER  ✦  HUILES & CONSERVES DE PROVENCE  ✦  PRESSED IN GRASSE  ✦  SMALL BATCH  ✦  ';
    const estChar = fs * 0.62 + fs * 0.28; const reps = Math.max(1, Math.round(C / (phrase.length * estChar)));
    ring.innerHTML = `<svg viewBox="0 0 200 200"><defs><path id="ringPath" d="M100,100 m-${r},0 a${r},${r} 0 1,1 ${2*r},0 a${r},${r} 0 1,1 -${2*r},0"/></defs><text style="font-size:${fs}px;letter-spacing:${fs*.28}px"><textPath href="#ringPath" textLength="${C.toFixed(1)}" lengthAdjust="spacing">${phrase.repeat(reps).replace(/&/g,'&amp;')}</textPath></text></svg>`;
  }
  buildRing();

  /* dots */
  const dots = $('.dots');
  P.forEach((p, i) => { const b = document.createElement('button'); b.type = 'button'; b.setAttribute('role', 'tab'); b.setAttribute('aria-label', p.fr); b.addEventListener('click', () => goTo(i)); dots.appendChild(b); });

  /* ---------- state ---------- */
  const hero = $('#hero'), stick = $('.hero__stick'); const slots = $$('.prod', wheel);
  let idx = -1, lap = 0, step = 0;
  const elIdx = $('.js-idx'), elFr = $('.js-fr'), elDesc = $('.js-desc'), elPrice = $('.js-price');
  const swapEls = [elFr, elDesc, elPrice.parentElement];
  swapEls.forEach(e => e.classList.add('swap'));
  function setTheme(p) { root.style.setProperty('--bg', p.bg); root.style.setProperty('--ink', p.ink); root.style.setProperty('--arch', p.arch);
    $('meta[name="theme-color"]').setAttribute('content', p.bg); }
  function apply(newIdx, newStep, instant) {
    const prevStep = step; step = newStep;
    stick.style.setProperty('--step', step);
    slots.forEach((el, i) => { let rel = ((i - step) % SLOTS + SLOTS) % SLOTS; if (rel > SLOTS / 2) rel -= SLOTS; const a = Math.abs(rel);
      el.classList.toggle('is-side', a === 1); el.classList.toggle('is-far', a > 1); });
    const dir = Math.sign(step - prevStep) || 1;
    if (newIdx === idx && !instant) return;
    const old = idx; idx = newIdx; const p = P[idx];
    setTheme(p);
    words.forEach((w, i) => { w.classList.toggle('is-on', i === idx); w.classList.toggle('is-prev', i !== idx && (dir > 0 ? true : false)); });
    // words that are not on: entering side depends on direction; set non-active ones to the side they should exit/enter from
    words.forEach((w, i) => { if (i !== idx) { w.classList.toggle('is-prev', dir > 0); } });
    $$('button', dots).forEach((b, i) => b.setAttribute('aria-selected', i === idx));
    const txt = () => { elIdx.textContent = String(idx + 1).padStart(2, '0'); elFr.textContent = p.fr; elDesc.textContent = p.desc; elPrice.textContent = p.price + ' · ' + p.size; };
    if (old < 0 || instant || reduce) { txt(); return; }
    swapEls.forEach(e => e.classList.add('out'));
    clearTimeout(apply._t); apply._t = setTimeout(() => { txt(); swapEls.forEach(e => e.classList.remove('out')); }, 380);
  }

  /* scroll → wheel */
  const segs = () => { const r = hero.offsetTop, h = hero.offsetHeight - innerHeight; return { top: r, len: h }; };
  function idxFromScroll() { const { top, len } = segs(); const p = (scrollY - top) / len; return Math.max(0, Math.min(N - 1, Math.floor(p * N))); }
  function scrollForIdx(i) { const { top, len } = segs(); return top + (i + 0.5) * len / N; }
  function onScrollHero() {
    if (reduce) return;
    const i = idxFromScroll();
    if (i !== idx) apply(i, i + lap * N);
  }
  function goTo(i, dir) {
    if (reduce || hero.offsetHeight <= innerHeight + 5) { // no scroll range → free stepping
      const ns = dir ? step + dir : step + (i - idx); apply(((ns % N) + N) % N, ns); return; }
    let target = i;
    if (dir) { target = idx + dir; if (target >= N) { lap++; target = 0; } else if (target < 0) { lap--; target = N - 1; } }
    const inHero = scrollY >= hero.offsetTop - 2 && scrollY <= hero.offsetTop + hero.offsetHeight - innerHeight + 2;
    if (!inHero) { lap = 0; }
    window.scrollTo({ top: scrollForIdx(target), behavior: 'instant' });
    apply(target, target + lap * N);
  }
  window.__go = (d) => goTo(null, d);
  $$('.arrow').forEach(b => b.addEventListener('click', () => goTo(null, +b.dataset.dir)));
  addEventListener('keydown', e => {
    const r = hero.getBoundingClientRect(); if (r.bottom < innerHeight * .5) return;
    if (e.key === 'ArrowRight') { e.preventDefault(); goTo(null, 1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(null, -1); }
  });
  // swipe
  let tx = 0, ty = 0, tt = 0;
  stick.addEventListener('touchstart', e => { const t = e.touches[0]; tx = t.clientX; ty = t.clientY; tt = Date.now(); }, { passive: true });
  stick.addEventListener('touchend', e => { const t = e.changedTouches[0]; const dx = t.clientX - tx, dy = t.clientY - ty;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.3 && Date.now() - tt < 700) goTo(null, dx < 0 ? 1 : -1); }, { passive: true });
  // click side product
  wheel.addEventListener('click', e => { const pr = e.target.closest('.prod'); if (!pr) return;
    const s = +pr.dataset.slot; let rel = ((s - step) % SLOTS + SLOTS) % SLOTS; if (rel > SLOTS / 2) rel -= SLOTS;
    if (rel === 0) document.getElementById('range').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }); else goTo(null, Math.sign(rel)); });

  apply(0, 0, true);

  /* ---------- intro ---------- */
  const firstImgs = $$('.wheel img').slice(0, 2).concat($$('.wheel img').slice(-2));
  Promise.all([document.fonts ? document.fonts.ready : 0, ...firstImgs.map(i => i.decode ? i.decode().catch(() => {}) : 0)]).then(() => {
    requestAnimationFrame(() => { root.classList.add('is-intro'); requestAnimationFrame(() => { root.classList.remove('is-loading'); setTimeout(() => root.classList.remove('is-intro'), 2000); window.__ready = true; }); });
  });
  setTimeout(() => { root.classList.remove('is-loading'); window.__ready = true; }, 3500);

  /* ---------- cursor ---------- */
  const cur = $('.cursor'); let mx = -100, my = -100, cx = -100, cy = -100;
  if (matchMedia('(hover:hover) and (pointer:fine)').matches) {
    addEventListener('pointermove', e => { mx = e.clientX; my = e.clientY; cur.classList.add('on'); }, { passive: true });
    document.addEventListener('pointerleave', () => cur.classList.remove('on'));
    document.addEventListener('pointerover', e => { const big = !!e.target.closest('.prod, .card'); cur.classList.toggle('big', big); });
    (function loop() { cx += (mx - cx) * .16; cy += (my - cy) * .16; cur.style.transform = `translate3d(${cx}px,${cy}px,0)`; requestAnimationFrame(loop); })();
  }
  function cursorColor() { const r = hero.getBoundingClientRect(); const inHero = r.bottom > my;
    cur.style.setProperty('--cc', inHero ? 'var(--ink)' : (my > 0 && document.elementFromPoint(mx, my)?.closest('.pour,.atelier,.letters,.foot') ? '#f3ecdf' : '#1b1f14'));
    cur.style.setProperty('--cl', inHero ? 'var(--bg)' : '#f3ecdf'); }

  /* ---------- range cards ---------- */
  $('.cards').innerHTML = P.map((p, i) => `<li class="card reveal" style="--d:${i % 3};--c:${p.bg};--ci:${p.ink};--h:${p.h}">
    <div class="card__media"><span class="card__tag">${p.tag}</span><img src="img/${p.id}.webp" alt="${p.fr} by Maison Olivier" loading="lazy" decoding="async"></div>
    <div class="card__body"><h3>${p.fr.replace('Huile d’Olive ', 'Huile ')}</h3><span class="card__price">${p.price}</span><p class="card__notes">${p.notes} · ${p.size}</p><span class="card__ex">Example price</span></div></li>`).join('');

  /* ---------- reveals ---------- */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: .12 });
  $$('.reveal, .reveal-img, .fade').forEach(el => io.observe(el));
  $$('.pour__step').forEach(s => $$('.fade', s).forEach((f, i) => f.style.setProperty('--d', i * 2)));

  /* statement words */
  const st = $('.statement__text');
  st.innerHTML = st.textContent.trim().split(/\s+/).map(w => `<span class="wd">${w}</span>`).join(' ');
  const wds = $$('.wd', st);
  function onStatement() { const r = st.getBoundingClientRect(); const p = (innerHeight * .85 - r.top) / (r.height + innerHeight * .35);
    const n = Math.round(Math.max(0, Math.min(1, p)) * wds.length); wds.forEach((w, i) => w.classList.toggle('on', i < n)); }

  /* ---------- scrub video ---------- */
  const pour = $('#pour'), vid = $('.pour__video'), bar = $('.pour__bar');
  vid.src = matchMedia('(max-width: 700px)').matches ? 'media/pour-720sq.mp4' : 'media/pour-1600.mp4';
  $$('source', vid).forEach(s => s.remove());
  vid.load();
  let vT = 0, vTarget = 0, dur = 8;
  vid.addEventListener('loadedmetadata', () => { dur = vid.duration || 8; });
  const unlock = () => { vid.play().then(() => vid.pause()).catch(() => {}); removeEventListener('touchstart', unlock); };
  addEventListener('touchstart', unlock, { passive: true });
  function pourProgress() { const r = pour.getBoundingClientRect(); const len = pour.offsetHeight - innerHeight; return Math.max(0, Math.min(1, -r.top / len)); }
  function seek(t) { return new Promise(res => { if (Math.abs(vid.currentTime - t) < 0.001 || vid.readyState < 1) return res();
    const done = () => { vid.removeEventListener('seeked', done); res(); }; vid.addEventListener('seeked', done); vid.currentTime = t; setTimeout(res, 1500); }); }
  window.__seekTo = async () => { const t = Math.min(dur - 0.05, pourProgress() * dur); vT = t; await seek(t); };
  function videoLoop() {
    if (!CAPTURE && !reduce) {
      vT += (vTarget - vT) * 0.18;
      if (!vid.seeking && vid.readyState >= 1 && Math.abs(vid.currentTime - vT) > 1 / 60) vid.currentTime = vT;
    }
    requestAnimationFrame(videoLoop);
  }
  requestAnimationFrame(videoLoop);

  /* ---------- nav ---------- */
  const nav = $('.nav');
  function onNav() {
    const hb = hero.offsetTop + hero.offsetHeight - 80;
    nav.classList.toggle('is-paper', scrollY > hb);
    const r = pour.getBoundingClientRect(); nav.classList.toggle('is-hidden', r.top < 60 && r.bottom > 200);
  }

  /* ---------- main scroll ---------- */
  function onScroll() {
    onScrollHero(); onStatement(); onNav();
    const p = pourProgress(); vTarget = Math.min(dur - 0.05, p * dur); bar.style.setProperty('--p', p);
    if (reduce) { /* keep poster */ }
    cursorColor();
  }
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', () => { buildRing(); onScroll(); });
  onScroll();

  /* ---------- demo-only actions ---------- */
  const toast = $('.toast'); let tt2;
  const say = (m) => { toast.textContent = m; toast.classList.add('on'); clearTimeout(tt2); tt2 = setTimeout(() => toast.classList.remove('on'), 2600); };
  $$('[data-demo]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); say('Concept demo — this is a fictional shop.'); }));
  $('.letters__form').addEventListener('submit', e => { e.preventDefault(); say('Concept demo — nothing was sent.'); });
})();
