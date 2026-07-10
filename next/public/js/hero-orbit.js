/**
 * YB Marketing — orbiting service icons (home + service heroes)
 */
(function () {
  'use strict';

  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function getRotationDeg(el) {
    var tr = getComputedStyle(el).transform;
    if (!tr || tr === 'none') return 0;
    var m = new DOMMatrixReadOnly(tr);
    var deg = (Math.atan2(m.b, m.a) * 180) / Math.PI;
    return deg < 0 ? deg + 360 : deg;
  }

  function initOrbit(orbit) {
    var spin = orbit.querySelector('.hero-orbit-spin');
    var icons = orbit.querySelectorAll('.hero-orbit-icon');
    if (!spin || !icons.length) return;

    var minScale = 0.76;
    var maxScale = 1.28;
    var focusAngle = 180;
    var nodeCount = icons.length;
    var stepDeg = 360 / nodeCount;

    orbit.style.setProperty('--orbit-n', String(nodeCount));
    var rafId = 0;
    var running = true;
    var pauseOnHover = orbit.classList.contains('hero-orbit--pause-hover');

    if (pauseOnHover) {
      function pause() {
        orbit.classList.add('is-paused');
      }

      function resume() {
        orbit.classList.remove('is-paused');
      }

      orbit.addEventListener('mouseenter', pause);
      orbit.addEventListener('mouseleave', resume);
      orbit.addEventListener('focusin', pause);
      orbit.addEventListener('focusout', function (e) {
        if (!orbit.contains(e.relatedTarget)) resume();
      });
    }

    function updateOrbitDepth() {
      var spinDeg = getRotationDeg(spin);
      var frontIcon = null;
      var frontT = -1;

      icons.forEach(function (icon) {
        var node = icon.closest('.hero-orbit-node');
        var pill = icon.querySelector('.hero-orbit-pill');
        var i = parseInt(node && node.style.getPropertyValue('--i'), 10) || 0;
        var armDeg = (i * stepDeg + spinDeg) % 360;
        var delta = ((armDeg - focusAngle + 540) % 360) - 180;
        var t = (Math.cos((delta * Math.PI) / 180) + 1) / 2;
        var scale = minScale + t * (maxScale - minScale);
        var opacity = 0.7 + t * 0.3;

        if (pill) {
          pill.style.transform =
            'rotate(' + (-armDeg).toFixed(2) + 'deg) scale(' + scale.toFixed(3) + ')';
        }

        icon.style.setProperty('--orbit-opacity', opacity.toFixed(3));
        icon.style.setProperty('--orbit-z', String(Math.round(2 + t * 6)));

        if (t > frontT) {
          frontT = t;
          frontIcon = icon;
        }
      });

      icons.forEach(function (icon) {
        icon.classList.toggle('is-front', icon === frontIcon && frontT > 0.85);
      });
    }

    function applyStaticOrbit() {
      icons.forEach(function (icon, idx) {
        var pill = icon.querySelector('.hero-orbit-pill');
        var armDeg = (idx * stepDeg) % 360;
        var delta = ((armDeg - focusAngle + 540) % 360) - 180;
        var t = (Math.cos((delta * Math.PI) / 180) + 1) / 2;
        var scale = minScale + t * (maxScale - minScale);
        if (pill) {
          pill.style.transform =
            'rotate(' + (-armDeg).toFixed(2) + 'deg) scale(' + scale.toFixed(3) + ')';
        }
        icon.style.setProperty('--orbit-opacity', (0.7 + t * 0.3).toFixed(3));
      });
    }

    function tick() {
      if (!running) return;
      updateOrbitDepth();
      rafId = requestAnimationFrame(tick);
    }

    if (prefersReducedMotion) {
      orbit.classList.add('is-static');
      applyStaticOrbit();
      return;
    }

    tick();

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        running = false;
        cancelAnimationFrame(rafId);
      } else {
        running = true;
        tick();
      }
    });
  }

  function init() {
    document.querySelectorAll('.hero-orbit').forEach(initOrbit);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
