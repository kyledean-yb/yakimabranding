/**
 * Blog listing — filter cards by topic
 */
(function () {
  'use strict';

  var grid = document.getElementById('blogCardGrid');
  if (!grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.blog-card'));
  var buttons = document.querySelectorAll('.blog-filter');
  var status = document.getElementById('blogFilterStatus');
  var empty = document.getElementById('blogFilterEmpty');
  var labels = {};

  buttons.forEach(function (btn) {
    labels[btn.getAttribute('data-filter')] = btn.textContent.trim();
  });

  function setActive(filter) {
    buttons.forEach(function (btn) {
      var on = btn.getAttribute('data-filter') === filter;
      btn.classList.toggle('is-active', on);
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  function applyFilter(filter) {
    var visible = 0;
    cards.forEach(function (card) {
      var topic = card.getAttribute('data-topic') || '';
      var show = filter === 'all' || topic === filter;
      card.classList.toggle('is-hidden', !show);
      card.setAttribute('aria-hidden', show ? 'false' : 'true');
      if (show) visible += 1;
    });

    if (status) {
      var name = labels[filter] || 'Posts';
      if (filter === 'all') {
        status.textContent = 'Showing all ' + visible + ' articles';
      } else {
        status.textContent = 'Showing ' + visible + ' ' + name + (visible === 1 ? ' article' : ' articles');
      }
    }

    if (empty) {
      empty.hidden = visible > 0;
    }

    setActive(filter);
  }

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      applyFilter(btn.getAttribute('data-filter') || 'all');
    });
  });

  applyFilter('all');
})();
