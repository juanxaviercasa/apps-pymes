(function () {
  'use strict';
  var KEY = 'np_theme';
  var root = document.documentElement;
  var media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function valid(value) { return value === 'light' || value === 'dark'; }
  function preferred() {
    try {
      var saved = window.localStorage.getItem(KEY);
      if (valid(saved)) return saved;
    } catch (error) {}
    return media && media.matches ? 'dark' : 'light';
  }
  function apply(theme) {
    theme = valid(theme) ? theme : 'light';
    root.setAttribute('data-np-theme', theme);
    root.style.colorScheme = theme;
    if (document.body) document.body.setAttribute('data-np-brand', 'true');
    try { window.localStorage.setItem(KEY, theme); } catch (error) {}
    var toggle = document.querySelector('[data-np-theme-toggle]');
    if (toggle) {
      toggle.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
      toggle.setAttribute('aria-label', theme === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');
      var label = toggle.querySelector('.np-theme-toggle-label');
      if (label) label.textContent = theme === 'dark' ? 'Modo oscuro' : 'Modo claro';
      var icon = toggle.querySelector('.np-theme-toggle-icon');
      if (icon) icon.textContent = theme === 'dark' ? '☾' : '☼';
    }
    document.dispatchEvent(new CustomEvent('np:themechange', { detail: { theme: theme } }));
  }
  function createToggle() {
    var existing = document.querySelector('[data-np-theme-toggle], button[role="switch"][aria-label*="modo" i]');
    if (existing) {
      existing.setAttribute('data-np-theme-toggle', 'true');
      existing.addEventListener('click', function () {
        window.setTimeout(function () { apply(root.getAttribute('data-np-theme') === 'dark' ? 'dark' : 'light'); }, 0);
      });
      apply(root.getAttribute('data-np-theme') || preferred());
      return;
    }
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'np-theme-toggle';
    button.setAttribute('data-np-theme-toggle', 'true');
    button.setAttribute('aria-pressed', 'false');
    button.innerHTML = '<span class="np-theme-toggle-icon" aria-hidden="true">☼</span><span class="np-theme-toggle-label">Modo claro</span>';
    button.addEventListener('click', function () {
      apply(root.getAttribute('data-np-theme') === 'dark' ? 'light' : 'dark');
    });
    document.body.appendChild(button);
    apply(root.getAttribute('data-np-theme') || preferred());
  }

  apply(preferred());
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      document.body.setAttribute('data-np-brand', 'true');
      createToggle();
    }, { once: true });
  } else {
    document.body.setAttribute('data-np-brand', 'true');
    createToggle();
  }
  if (media && media.addEventListener) {
    media.addEventListener('change', function (event) {
      try { if (!window.localStorage.getItem(KEY)) apply(event.matches ? 'dark' : 'light'); } catch (error) {}
    });
  }
  window.npTheme = { get: function () { return root.getAttribute('data-np-theme'); }, set: apply };
}());
