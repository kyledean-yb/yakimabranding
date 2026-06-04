(function () {
  'use strict';

  var acc = document.querySelector('.brand-acc');
  if (!acc) return;

  var items = Array.prototype.slice.call(acc.querySelectorAll('.brand-acc-item'));

  function setPanelHeight(item, open) {
    var panel = item.querySelector('.brand-acc-panel');
    if (!panel) return;
    if (open) {
      panel.style.maxHeight = panel.scrollHeight + 'px';
    } else {
      panel.style.maxHeight = '0';
    }
  }

  function openItem(item, scroll) {
    items.forEach(function (other) {
      var isTarget = other === item;
      other.classList.toggle('is-open', isTarget);
      var btn = other.querySelector('.brand-acc-trigger');
      if (btn) btn.setAttribute('aria-expanded', isTarget ? 'true' : 'false');
      setPanelHeight(other, isTarget);
    });
    if (scroll) {
      window.setTimeout(function () {
        item.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 80);
    }
  }

  items.forEach(function (item) {
    var btn = item.querySelector('.brand-acc-trigger');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var willOpen = !item.classList.contains('is-open');
      if (willOpen) {
        openItem(item, false);
      } else {
        item.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
        setPanelHeight(item, false);
      }
    });
  });

  items.forEach(function (item) {
    setPanelHeight(item, item.classList.contains('is-open'));
  });

  window.addEventListener('resize', function () {
    items.forEach(function (item) {
      if (item.classList.contains('is-open')) setPanelHeight(item, true);
    });
  });
})();
