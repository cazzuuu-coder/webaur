(() => {
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const body = document.body, top = $('.top'), concept = $('.concept');

  /* page enter + leave transitions */
  requestAnimationFrame(() => requestAnimationFrame(() => body.classList.add('ready')));
  addEventListener('pageshow', e => { if (e.persisted) body.classList.remove('leaving'); body.classList.add('ready'); });
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]'); if (!a || RM) return;
    const url = new URL(a.href, location.href);
    if (a.target || e.metaKey || e.ctrlKey || e.shiftKey || e.button || url.origin !== location.origin || !/\.html$/.test(url.pathname) || url.pathname === location.pathname || a.hasAttribute('download')) return;
    e.preventDefault(); body.classList.add('leaving'); setTimeout(() => { location.href = a.href; }, 360);
  });

  /* split headings into lines (by <br>) for the mask reveal */
  $$('.split-lines').forEach(h => {
    const parts = h.innerHTML.split(/<br\s*\/?>/i);
    h.innerHTML = parts.map((p, i) => `<span class="ln" style="--i:${i}"><span>${p.trim()}</span></span>`).join('');
  });

  /* reveal on scroll */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -10% 0px' });
  $$('.rv, .split-lines').forEach(el => RM ? el.classList.add('in') : io.observe(el));

  /* header: solid after hero, hides on scroll down, follows concept bar */
  const fixedTop = body.matches('.is-home, .is-seasons');
  let lastY = scrollY, ticking = false;
  const onScroll = () => {
    const y = scrollY, cb = concept.offsetHeight;
    if (fixedTop) top.style.top = Math.max(0, cb - y) + 'px';
    top.classList.toggle('solid', fixedTop ? y > innerHeight * .6 : y > cb);
    if (!top.classList.contains('menu-open')) top.classList.toggle('hide', y > lastY && y > innerHeight * .9);
    lastY = y;
    // intro words
    words.forEach(w => { const r = w.getBoundingClientRect(); w.classList.toggle('on', r.top < innerHeight * .72); });
    // parallax
    if (!RM) par.forEach(([el, k]) => { const r = el.parentElement.getBoundingClientRect(); if (r.bottom < -100 || r.top > innerHeight + 100) return; const c = (r.top + r.height / 2 - innerHeight / 2); el.style.transform = `translate3d(0,${(-c * k).toFixed(1)}px,0)`; });
    ticking = false;
  };
  const words = [];
  $$('.words').forEach(p => { p.innerHTML = p.textContent.trim().split(/\s+/).map(w => `<span class="w">${w}</span>`).join(' '); words.push(...$$('.w', p)); });
  const par = $$('[data-parallax]').map(el => [el, +el.dataset.parallax]);
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener('resize', onScroll); onScroll();

  /* mobile menu */
  const burger = $('.burger'), nav = $('#nav');
  const setMenu = o => { nav.classList.toggle('is-open', o); top.classList.toggle('menu-open', o); burger.setAttribute('aria-expanded', o); document.documentElement.style.overflow = o ? 'hidden' : ''; };
  burger.addEventListener('click', () => setMenu(!nav.classList.contains('is-open')));
  addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('is-open')) { setMenu(false); burger.focus(); } });

  /* local time in Inari */
  const clock = $('.clock__t');
  if (clock) { const f = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Helsinki' }); const t = () => clock.textContent = f.format(new Date()); t(); setInterval(t, 20000); }

  /* cabins tabs */
  const tabs = $$('.tab');
  if (tabs.length) {
    const ink = $('.tabs__ink');
    const place = t => { ink.style.width = t.offsetWidth - parseFloat(getComputedStyle(t).paddingRight) + "px"; ink.style.transform = `translateX(${t.offsetLeft}px)`; };
    const select = (t, focus) => {
      tabs.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; const p = document.getElementById(x.getAttribute('aria-controls')); p.hidden = !on; p.classList.toggle('is-on', on); });
      place(t); if (focus) t.focus();
    };
    tabs.forEach((t, i) => { t.addEventListener('click', () => select(t)); t.addEventListener('keydown', e => { const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (d) { e.preventDefault(); select(tabs[(i + d + tabs.length) % tabs.length], true); } }); });
    const fromHash = () => { const a = location.hash && document.querySelector(`.anchor${location.hash}`); if (a) select(document.getElementById(a.dataset.tab)); };
    addEventListener('hashchange', fromHash); addEventListener('resize', () => place($('.tab[aria-selected="true"]')));
    document.fonts.ready.then(() => { place($('.tab[aria-selected="true"]')); fromHash(); });
  }

  /* experiences filter */
  const fbtns = $$('.fbtn');
  if (fbtns.length) {
    const items = $$('.ex'), count = $('.filter__count b');
    fbtns.forEach(b => b.addEventListener('click', () => {
      const f = b.dataset.f; fbtns.forEach(x => { x.classList.toggle('is-on', x === b); x.setAttribute('aria-pressed', x === b); });
      let n = 0;
      items.forEach(it => { const show = f === 'any' || it.dataset.season === f || it.dataset.season === 'all'; if (show) n++;
        if (show) { it.classList.remove('out'); it.classList.add('fade'); requestAnimationFrame(() => requestAnimationFrame(() => it.classList.remove('fade'))); } else it.classList.add('out'); });
      count.textContent = n;
    }));
  }

  /* season toggle + months */
  const season = $('.season');
  if (season) {
    const btns = $$('.toggle button');
    const setS = s => { season.dataset.season = s; btns.forEach(b => b.setAttribute('aria-checked', b.dataset.s === s));
      $$('.season__img').forEach(x => x.classList.toggle('is-on', x.dataset.for === s));
      $$('.scopy').forEach(x => { const on = x.dataset.for === s; x.hidden = !on; x.classList.toggle('is-on', on); }); };
    btns.forEach(b => b.addEventListener('click', () => setS(b.dataset.s)));
    $('.toggle').addEventListener('keydown', e => { if (/Arrow(Left|Right)/.test(e.key)) { e.preventDefault(); const s = season.dataset.season === 'winter' ? 'summer' : 'winter'; setS(s); btns.find(b => b.dataset.s === s).focus(); } });
    if (location.hash === '#summer') setS('summer');
    const data = JSON.parse($('#months-data').textContent), md = $('.mdetail'), full = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const mb = $$('.m');
    const setM = i => { mb.forEach((b, k) => b.setAttribute('aria-pressed', k === i)); const d = data[i];
      md.classList.remove('swap'); void md.offsetWidth; md.classList.add('swap');
      $('.mdetail__m', md).innerHTML = `${full[i]} <span class="mdetail__h">${d.h === 0 ? 'Polar night, no sunrise' : d.h === 24 ? 'Midnight sun, 24 h daylight' : '≈ ' + d.h + ' h daylight'}</span>`; $('.mdetail__t', md).textContent = d.t; $('.mdetail__d', md).textContent = d.d; };
    mb.forEach((b, i) => b.addEventListener('click', () => setM(i)));
    const now = new Date().getMonth(); setM(now);
  }

  /* gallery lightbox */
  const lb = $('.lb');
  if (lb) {
    const btns = $$('.gi__btn'), im = $('.lb__img'), cap = $('.lb__cap'), cnt = $('.lb__count'); let cur = 0, opener = null;
    const show = i => { cur = (i + btns.length) % btns.length; const src = $('img', btns[cur]);
      im.src = src.currentSrc || src.src; im.alt = src.alt; cap.textContent = src.alt; cnt.textContent = `${cur + 1} / ${btns.length}`;
      im.style.animation = 'none'; void im.offsetWidth; im.style.animation = ''; };
    btns.forEach((b, i) => b.addEventListener('click', () => { opener = b; const s = $('img', b); s.loading = 'eager'; show(i); lb.showModal(); }));
    $('.lb__x').addEventListener('click', () => lb.close());
    $('.lb__prev').addEventListener('click', () => show(cur - 1));
    $('.lb__next').addEventListener('click', () => show(cur + 1));
    lb.addEventListener('click', e => { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', e => { if (e.key === 'ArrowRight') show(cur + 1); if (e.key === 'ArrowLeft') show(cur - 1); });
    lb.addEventListener('close', () => opener && opener.focus());
    let sx = null; lb.addEventListener('touchstart', e => sx = e.touches[0].clientX, { passive: true });
    lb.addEventListener('touchend', e => { if (sx === null) return; const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); sx = null; });
  }

  /* booking request form */
  const bf = $('.bform');
  if (bf) {
    const PRICE = { revontuli: 320, kuura: 260, tunturi: 480 }, NAME = { revontuli: 'Revontuli', kuura: 'Kuura', tunturi: 'Tunturi' }, MAX = { revontuli: 4, kuura: 2, tunturi: 6 };
    const ADD = { 'Aurora night': 85, 'Husky trail': 190, 'Breakfast basket': 0 };
    const out = $('output', bf), minus = $('[data-step="-1"]', bf), plus = $('[data-step="1"]', bf), st = $('.bform__status');
    const q = new URLSearchParams(location.search).get('cabin'); if (q && PRICE[q]) bf.querySelector(`input[value="${q}"]`).checked = true;
    const iso = d => d.toISOString().slice(0, 10);
    const t0 = new Date(); t0.setDate(t0.getDate() + 1); bf.arrive.min = iso(t0);
    const bump = el => { el.classList.remove('bump'); void el.offsetWidth; el.classList.add('bump'); };
    const fmt = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short' });
    const upd = () => {
      const c = bf.cabin.value; let g = +out.value; if (g > MAX[c]) g = MAX[c]; out.value = g;
      minus.disabled = g <= 1; plus.disabled = g >= MAX[c];
      if (bf.arrive.value) { const m = new Date(bf.arrive.value + 'T12:00'); m.setDate(m.getDate() + 1); bf.depart.min = iso(m); }
      const a = bf.arrive.value && new Date(bf.arrive.value + 'T12:00'), d = bf.depart.value && new Date(bf.depart.value + 'T12:00');
      const n = a && d && d > a ? Math.round((d - a) / 864e5) : 0;
      const adds = $$('input[name="addon"]:checked', bf).map(x => x.value);
      const set = (s, v) => { const el = $(s); if (el.textContent !== String(v)) { el.textContent = v; bump(el); } };
      set('.summary__cabin', NAME[c] + ' cabin');
      set('.s-dates', n ? `${fmt.format(a)} – ${fmt.format(d)}` : 'Choose dates');
      set('.s-nights', n || '–'); set('.s-guests', g); set('.s-add', adds.length ? adds.join(', ') : 'None');
      const est = n ? n * PRICE[c] + adds.reduce((s, x) => s + ADD[x] * g, 0) : 0;
      set('.s-est', est ? '€' + est.toLocaleString('en-GB') : '–');
    };
    bf.addEventListener('input', upd); bf.addEventListener('change', upd);
    [minus, plus].forEach(b => b.addEventListener('click', () => { out.value = +out.value + +b.dataset.step; upd(); }));
    upd();
    bf.addEventListener('submit', e => { e.preventDefault();
      const ok = bf.name.value.trim() && /^\S+@\S+\.\S+$/.test(bf.email.value) && bf.arrive.value && bf.depart.value && bf.depart.value > bf.arrive.value;
      st.textContent = ok ? 'Thank you! This is a concept demo, so nothing was sent.' : 'Please add your dates, name and a valid email.'; });
  }
})();
