(function () {
  'use strict';

  function initBrandExplorer(root) {
    var nav = root.querySelector('.brand-explorer-nav');
    var panels = root.querySelectorAll('.brand-panel');
    if (!nav || !panels.length) return;

    nav.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-brand-tab]');
      if (!btn) return;
      var id = btn.getAttribute('data-brand-tab');
      nav.querySelectorAll('[data-brand-tab]').forEach(function (b) {
        b.classList.toggle('is-active', b === btn);
        b.setAttribute('aria-selected', b === btn ? 'true' : 'false');
      });
      panels.forEach(function (panel) {
        var show = panel.id === 'brand-panel-' + id;
        panel.classList.toggle('is-active', show);
        panel.hidden = !show;
      });
    });
  }

  function init() {
    document.querySelectorAll('.brand-explorer').forEach(initBrandExplorer);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
