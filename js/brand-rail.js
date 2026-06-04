(function () {
  'use strict';

  var rail = document.querySelector('.brand-rail');
  if (!rail) return;

  var links = Array.prototype.slice.call(rail.querySelectorAll('a[href^="#"]'));
  var blocks = links.map(function (link) {
    var id = link.getAttribute('href').slice(1);
    return document.getElementById(id);
  }).filter(Boolean);

  if (!blocks.length) return;

  function setActive(id) {
    links.forEach(function (link) {
      var match = link.getAttribute('href') === '#' + id;
      link.classList.toggle('is-active', match);
    });
  }

  links.forEach(function (link) {
    link.addEventListener('click', function (e) {
      var target = document.querySelector(link.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setActive(target.id);
    });
  });

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) setActive(entry.target.id);
        });
      },
      { rootMargin: '-40% 0px -45% 0px', threshold: 0 }
    );
    blocks.forEach(function (block) { observer.observe(block); });
  }
})();
