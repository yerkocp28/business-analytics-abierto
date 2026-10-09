(() => {
  'use strict';
  const formulas = [...document.querySelectorAll('main math')].map((math, i) => {
    const wrap = document.createElement('span');
    wrap.className = 'ba-math' + (math.getAttribute('display') === 'block' ? ' ba-display' : '');
    wrap.setAttribute('role', 'group'); wrap.setAttribute('aria-label', `Expresión matemática ${i + 1}`);
    math.before(wrap); wrap.append(math); return wrap;
  });
  const focusFormulas = () => formulas.forEach(wrap => {
    if (wrap.scrollWidth > wrap.clientWidth + 1) wrap.tabIndex = 0;
    else wrap.removeAttribute('tabindex');
  });
  focusFormulas(); window.addEventListener('resize', focusFormulas);
  const menu = document.getElementById('ba-menu'), panel = document.getElementById('ba-panel-indice');
  const setMenu = open => { panel.classList.toggle('ba-abierto', open); menu.setAttribute('aria-expanded', String(open)); menu.textContent = open ? 'Cerrar índice' : 'Mostrar índice'; };
  menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { setMenu(false); menu.focus(); } });
  const normal = value => value.toLocaleLowerCase('es').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const search = document.getElementById('buscar') || document.getElementById('ba-buscar');
  const results = document.getElementById('ba-resultados'), count = document.getElementById('ba-conteo');
  const chapters = [...document.querySelectorAll('main > section[id],main > header[id]')];
  const index = chapters.map(section => ({section, title:section.querySelector('h1,h2')?.textContent.trim() || section.id, text:normal(section.textContent)}));
  function clearSearch() {
    search.value = ''; search.dispatchEvent(new Event('input', {bubbles:true}));
    document.querySelectorAll('section.level1').forEach(section => { section.hidden = false; });
    const empty = document.getElementById('sin-resultados'); if (empty) empty.hidden = true;
  }
  search.addEventListener('input', () => {
    const q = normal(search.value.trim()); results.replaceChildren();
    const found = q ? index.filter(item => item.text.includes(q)) : [];
    count.textContent = q ? `${found.length} capítulos encontrados` : '';
    found.forEach(item => { const li = document.createElement('li'), a = document.createElement('a'); a.href = '#' + item.section.id; a.textContent = item.title; li.append(a); results.append(li); });
    results.hidden = !q;
  });
  document.addEventListener('click', e => {
    const link = e.target.closest('a[href^="#"]'); if (!link) return;
    const target = document.getElementById(decodeURIComponent(link.hash.slice(1))); if (!target) return;
    if (search.value) clearSearch();
    setMenu(false);
    requestAnimationFrame(() => { target.setAttribute('tabindex','-1'); target.focus({preventScroll:true}); target.scrollIntoView({block:'start'}); });
  });
  const links = [...panel.querySelectorAll('nav a[href^="#"]')];
  let scheduled = false;
  function markCurrent() {
    const visible = chapters.filter(s => !s.hidden && s.getBoundingClientRect().top < innerHeight * .35);
    const id = (visible.at(-1) || chapters[0])?.id;
    links.forEach(link => { if (link.hash === '#' + id) link.setAttribute('aria-current','location'); else link.removeAttribute('aria-current'); });
    scheduled = false;
  }
  window.addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(markCurrent); } }, {passive:true}); markCurrent();
  const mode = document.getElementById('clase-toggle');
  mode.addEventListener('change', () => { document.body.classList.toggle('ba-clase',mode.checked); document.body.classList.toggle('clase',mode.checked); window.dispatchEvent(new Event('resize')); });
  document.querySelectorAll('[data-ba-ruta]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('[data-ba-ruta]').forEach(b => b.setAttribute('aria-pressed',String(b === button)));
    document.querySelectorAll('[data-ba-calendario]').forEach(p => { p.hidden = p.dataset.baCalendario !== button.dataset.baRuta; });
  }));
  document.querySelectorAll('input[type=range]').forEach(input => {
    const update = () => input.setAttribute('aria-valuetext', `${input.value}${input.dataset.unidad ? ' ' + input.dataset.unidad : ''}`);
    update(); input.addEventListener('input', update);
  });
})();
