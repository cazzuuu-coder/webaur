(() => {
  const top = document.querySelector('.top'), b = document.querySelector('.burger'), nav = document.getElementById('nav');
  const set = o => { nav.classList.toggle('is-open', o); b.setAttribute('aria-expanded', o); };
  b.addEventListener('click', () => set(!nav.classList.contains('is-open')));
  addEventListener('keydown', e => e.key === 'Escape' && set(false));
  const onS = () => top.classList.toggle('is-scrolled', scrollY > 8); onS(); addEventListener('scroll', onS, { passive: true });
  // gentle reveal
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
    const els = document.querySelectorAll('.sec__head, .tile, .split__img, .split__copy, .strip figure, .svc, .prices__in, .person, .band__in, .g, .cta__in, .phead > *');
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
    els.forEach((el, i) => { el.classList.add('rv'); el.style.transitionDelay = (el.matches('.tile, .person, .strip figure') ? (i % 4) * 70 : 0) + 'ms'; io.observe(el); });
  }
  const form = document.querySelector('.form');
  if (form) { const st = form.querySelector('.form__status');
    form.addEventListener('submit', e => { e.preventDefault();
      if (!form.name.value.trim() || !/^\S+@\S+\.\S+$/.test(form.email.value)) { st.textContent = 'Please add your name and a valid email.'; return; }
      st.textContent = 'Thank you! This is a concept demo, so nothing was sent.'; form.reset(); }); }
})();
