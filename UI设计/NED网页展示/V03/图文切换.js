// Enhance each gallery independently; without JS, the original compositions stay readable in sequence.
document.querySelectorAll('[data-aplus-switcher]').forEach(carousel => {
  const nav = carousel.querySelector('.aplus__nav');
  const list = nav.querySelector('.aplus__tabs');
  const tabs = [...list.querySelectorAll('[data-aplus-target]')];
  const panels = tabs.map(tab => document.getElementById(tab.dataset.aplusTarget));
  const status = nav.querySelector('[data-aplus-status]');
  if (tabs.length < 2 || panels.some(panel => !panel || !carousel.contains(panel))) return;
  list.setAttribute('role', 'tablist');
  tabs.forEach((tab, i) => {
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-controls', panels[i].id);
    panels[i].setAttribute('role', 'tabpanel');
    panels[i].setAttribute('aria-labelledby', tab.id);
    panels[i].tabIndex = 0;
  });
  const wrap = index => (index + tabs.length) % tabs.length;
  const setTabStop = index => tabs.forEach((tab, i) => { tab.tabIndex = i === index ? 0 : -1; });
  let active = -1;
  const select = (index, announce = false) => {
    if (index === active) return;
    active = index;
    setTabStop(index);
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === active));
      panels[i].hidden = i !== active;
    });
    if (announce) status.textContent = tabs[index].textContent.trim() + ', ' + (index + 1) + ' of ' + tabs.length;
  };
  list.addEventListener('click', event => {
    const index = tabs.indexOf(event.target.closest('button'));
    if (index >= 0) select(index);
  });
  list.addEventListener('keydown', event => {
    const index = tabs.indexOf(event.target);
    if (index < 0) return;
    const destinations = { ArrowLeft: wrap(index - 1), ArrowRight: wrap(index + 1), Home: 0, End: tabs.length - 1 };
    if (!Object.hasOwn(destinations, event.key)) return;
    event.preventDefault();
    const next = destinations[event.key];
    setTabStop(next);
    tabs[next].focus({ preventScroll: true });
  });
  list.addEventListener('focusout', event => {
    if (!list.contains(event.relatedTarget)) setTabStop(active);
  });
  nav.addEventListener('click', event => {
    const arrow = event.target.closest('[data-aplus-step]');
    if (arrow) select(wrap(active + Number(arrow.dataset.aplusStep)), true);
  });
  const stage = carousel.querySelector('.aplus__slides');
  let touchStart = null;
  stage.addEventListener('pointerdown', event => {
    if (event.pointerType !== 'touch' || !event.isPrimary) {
      touchStart = null;
      return;
    }
    touchStart = { id: event.pointerId, x: event.clientX, y: event.clientY };
  });
  stage.addEventListener('pointercancel', () => { touchStart = null; });
  stage.addEventListener('pointerup', event => {
    const start = touchStart;
    touchStart = null;
    if (start?.id !== event.pointerId) return;
    const x = event.clientX - start.x;
    const y = event.clientY - start.y;
    if (Math.abs(x) > 48 && Math.abs(x) > Math.abs(y) * 1.5) {
      select(wrap(active + (x < 0 ? 1 : -1)), true);
    }
  });
  select(0);
  carousel.dataset.aplusReady = '';
  nav.hidden = false;
});
