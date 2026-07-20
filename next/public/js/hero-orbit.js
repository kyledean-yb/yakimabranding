/**
 * YB Marketing — orbiting service icons (home + service heroes)
 * Rotation tracked via JS clock (matches CSS --orbit-dur), not getComputedStyle.
 */
(function () {
  'use strict';

  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var DEFAULT_ORBIT_MS = 24000;

  function parseDurationMs(value) {
    if (!value) return DEFAULT_ORBIT_MS;
    var trimmed = String(value).trim();
    if (trimmed.endsWith('ms')) {
      var ms = parseFloat(trimmed);
      return isFinite(ms) && ms > 0 ? ms : DEFAULT_ORBIT_MS;
    }
    if (trimmed.endsWith('s')) {
      var sec = parseFloat(trimmed);
      return isFinite(sec) && sec > 0 ? sec * 1000 : DEFAULT_ORBIT_MS;
    }
    var n = parseFloat(trimmed);
    return isFinite(n) && n > 0 ? n : DEFAULT_ORBIT_MS;
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

    var orbitDurMs = parseDurationMs(
      getComputedStyle(orbit).getPropertyValue('--orbit-dur')
    );
    var startTime = performance.now();
    var pausedElapsed = 0;
    var pauseStartedAt = 0;
    var isPaused = false;

    function getSpinDeg(now) {
      var elapsed = pausedElapsed;
      if (!isPaused) {
        elapsed += now - startTime;
      }
      var progress = (elapsed % orbitDurMs) / orbitDurMs;
      return progress * 360;
    }

    function pauseClock() {
      if (isPaused) return;
      isPaused = true;
      pauseStartedAt = performance.now();
      pausedElapsed += pauseStartedAt - startTime;
      orbit.classList.add('is-paused');
    }

    function resumeClock() {
      if (!isPaused) return;
      isPaused = false;
      startTime = performance.now();
      orbit.classList.remove('is-paused');
    }

    if (pauseOnHover) {
      orbit.addEventListener('mouseenter', pauseClock);
      orbit.addEventListener('mouseleave', resumeClock);
      orbit.addEventListener('focusin', pauseClock);
      orbit.addEventListener('focusout', function (e) {
        if (!orbit.contains(e.relatedTarget)) resumeClock();
      });
    }

    function updateOrbitDepth(now) {
      var spinDeg = getSpinDeg(now);
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

    function tick(now) {
      if (!running) return;
      updateOrbitDepth(now);
      rafId = requestAnimationFrame(tick);
    }

    if (prefersReducedMotion) {
      orbit.classList.add('is-static');
      applyStaticOrbit();
      return;
    }

    rafId = requestAnimationFrame(tick);

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        running = false;
        cancelAnimationFrame(rafId);
        if (!isPaused) {
          pausedElapsed += performance.now() - startTime;
          isPaused = true;
          pauseStartedAt = performance.now();
        }
      } else {
        if (isPaused && !orbit.classList.contains('is-paused')) {
          isPaused = false;
          startTime = performance.now();
        } else if (isPaused) {
          // Stay paused (hover); clock already frozen in pausedElapsed
        } else {
          startTime = performance.now();
        }
        running = true;
        rafId = requestAnimationFrame(tick);
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
