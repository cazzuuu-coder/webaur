(() => {
  const burger = document.querySelector('.burger'), menu = document.getElementById('menu');
  const close = () => { menu.classList.remove('is-open'); burger.setAttribute('aria-expanded', 'false'); burger.setAttribute('aria-label', 'Open menu'); };
  burger.addEventListener('click', () => { const o = menu.classList.toggle('is-open'); burger.setAttribute('aria-expanded', o); burger.setAttribute('aria-label', o ? 'Close menu' : 'Open menu'); });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
  addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  // highlight current section in the menu
  const links = [...menu.querySelectorAll('a')], map = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { links.forEach(l => l.classList.remove('is-on')); map.get(e.target.id)?.classList.add('is-on'); } }), { rootMargin: '-45% 0px -50% 0px' });
  map.forEach((a, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  ['about-title', 'hero-title'].forEach(id => { const s = document.getElementById(id)?.closest('section'); if (s) io.observe(s); });
  // demo form
  const form = document.querySelector('.form'), st = form.querySelector('.form__status');
  form.addEventListener('submit', e => { e.preventDefault();
    if (!form.name.value.trim() || !/^\S+@\S+\.\S+$/.test(form.email.value)) { st.textContent = 'Please add your name and a valid email.'; return; }
    st.textContent = 'Thanks! This is a concept demo, so nothing was sent.'; form.reset(); });
})();
