(() => {
  'use strict';
  const main = document.querySelector('main');
  if (!main || main.querySelector('.ba-manual-recursos')) return;
  const key = location.pathname.split('/').pop().slice(0, 3).toLowerCase();
  const guide = key === 'fba' ? 'ba' : key;
  const nav = document.createElement('nav');
  nav.className = 'ba-manual-recursos'; nav.setAttribute('aria-label', 'Recursos del manual');
  [['../../index.html', 'Biblioteca'], [`../guia_maestra_${guide}.html`, 'Guía y actividades'], ['#title-block-header', 'Inicio del manual']].forEach(([href, text]) => {
    const a = document.createElement('a'); a.href = href; a.textContent = text; nav.append(a);
  });
  main.prepend(nav);
  const formulas = [...main.querySelectorAll('math')].map((math, i) => {
    const wrap = document.createElement('span');
    wrap.className = 'ba-math' + (math.getAttribute('display') === 'block' ? ' ba-display' : '');
    wrap.setAttribute('role', 'group');
    wrap.setAttribute('aria-label', `Expresión matemática ${i + 1}`);
    math.before(wrap); wrap.append(math); return wrap;
  });
  const focusFormulas = () => formulas.forEach(wrap => {
    if (wrap.scrollWidth > wrap.clientWidth + 1) wrap.tabIndex = 0;
    else wrap.removeAttribute('tabindex');
  });
  focusFormulas(); window.addEventListener('resize', focusFormulas);
  main.querySelectorAll('table').forEach((table, i) => {
    const wrap = document.createElement('div'); wrap.className = 'ba-scroll'; wrap.tabIndex = 0;
    wrap.setAttribute('role', 'region');
    wrap.setAttribute('aria-label', table.querySelector('caption')?.textContent.trim() || `Tabla ${i + 1}; desplazamiento horizontal cuando sea necesario`);
    table.before(wrap); wrap.append(table);
  });
  const dialog = document.createElement('dialog'); dialog.className = 'ba-figura-dialogo';
  dialog.innerHTML = '<button class="ba-ampliar" type="button">Cerrar figura</button><p id="ba-figura-descripcion"></p><div class="ba-figura-grande" tabindex="0" role="region" aria-label="Figura ampliada con desplazamiento"><img alt=""></div>';
  dialog.setAttribute('aria-labelledby', 'ba-figura-descripcion'); document.body.append(dialog);
  let trigger;
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => trigger?.focus());
  main.querySelectorAll('img').forEach((img, i) => {
    const button = document.createElement('button'); button.type = 'button'; button.className = 'ba-ampliar';
    button.textContent = 'Ampliar figura'; button.setAttribute('aria-label', `Ampliar figura ${i + 1}: ${img.alt}`);
    img.closest('a')?.contains(img) ? img.closest('a').after(button) : img.after(button);
    button.addEventListener('click', () => {
      trigger = button; const large = dialog.querySelector('img'); large.src = img.src; large.alt = img.alt;
      large.style.width = `${img.naturalWidth}px`;
      dialog.querySelector('p').textContent = img.alt; dialog.showModal(); dialog.querySelector('button').focus();
    });
  });
})();
