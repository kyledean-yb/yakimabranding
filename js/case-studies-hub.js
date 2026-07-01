(function () {
  'use strict';

  var filters = document.querySelectorAll('.cs-hub-filter');
  var cards = document.querySelectorAll('.cs-hub-card');
  var status = document.getElementById('csHubFilterStatus');
  if (!filters.length || !cards.length) return;

  function applyFilter(key) {
    var visible = 0;
    cards.forEach(function (card) {
      var categories = (card.getAttribute('data-cs-categories') || '').split(/\s+/);
      var show = key === 'all' || categories.indexOf(key) !== -1;
      card.hidden = !show;
      if (show) visible += 1;
    });

    if (status) {
      if (key === 'all') {
        status.textContent = '';
      } else {
        status.textContent =
          visible === 1 ? 'Showing 1 case study' : 'Showing ' + visible + ' case studies';
      }
    }
  }

  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var key = btn.getAttribute('data-cs-filter') || 'all';
      filters.forEach(function (other) {
        other.classList.toggle('is-active', other === btn);
      });
      applyFilter(key);
    });
  });
})();
