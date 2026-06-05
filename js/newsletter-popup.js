/**
 * YB Marketing — newsletter signup popup (non-intrusive, session-scoped)
 */
(function () {
  'use strict';

  var STORAGE_CLOSED = 'ybNewsletterClosed';
  var STORAGE_SUBMITTED = 'ybNewsletterSubmitted';
  var SHOW_DELAY_MS = 8000;

  function shouldSkip() {
    try {
      return (
        sessionStorage.getItem(STORAGE_CLOSED) === '1' ||
        sessionStorage.getItem(STORAGE_SUBMITTED) === '1'
      );
    } catch (e) {
      return false;
    }
  }

  function setSession(key) {
    try {
      sessionStorage.setItem(key, '1');
    } catch (e) {
      /* ignore */
    }
  }

  function buildPopup() {
    var root = document.createElement('aside');
    root.id = 'yb-newsletter-popup';
    root.className = 'yb-newsletter-popup';
    root.setAttribute('role', 'dialog');
    root.setAttribute('aria-modal', 'false');
    root.setAttribute('aria-labelledby', 'yb-newsletter-title');
    root.setAttribute('aria-describedby', 'yb-newsletter-desc');
    root.setAttribute('aria-hidden', 'true');
    root.hidden = true;

    root.innerHTML =
      '<div class="yb-newsletter-popup__card">' +
      '  <button type="button" class="yb-newsletter-popup__close" aria-label="Close newsletter signup">' +
      '    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true">' +
      '      <path d="M18 6L6 18M6 6l12 12"/>' +
      '    </svg>' +
      '  </button>' +
      '  <div class="yb-newsletter-popup__content">' +
      '    <p class="yb-newsletter-popup__eyebrow">Newsletter</p>' +
      '    <h2 id="yb-newsletter-title" class="yb-newsletter-popup__title">Get Marketing Tips That Actually Help</h2>' +
      '    <p id="yb-newsletter-desc" class="yb-newsletter-popup__body">Join our newsletter for practical digital marketing insights, website tips, and ideas to help your business grow.</p>' +
      '    <form class="yb-newsletter-popup__form" action="#" method="post" novalidate>' +
      '      <label class="yb-newsletter-popup__label" for="yb-newsletter-email">Email address</label>' +
      '      <div class="yb-newsletter-popup__fields">' +
      '        <input id="yb-newsletter-email" class="yb-newsletter-popup__input" type="email" name="email" autocomplete="email" placeholder="you@company.com" required>' +
      '        <button type="submit" class="yb-newsletter-popup__submit">Sign Up</button>' +
      '      </div>' +
      '    </form>' +
      '    <p class="yb-newsletter-popup__success" role="status" aria-live="polite" hidden>Thanks for signing up! Check your inbox soon.</p>' +
      '  </div>' +
      '</div>';

    document.body.appendChild(root);
    return root;
  }

  function showPopup(root) {
    root.hidden = false;
    root.setAttribute('aria-hidden', 'false');
    requestAnimationFrame(function () {
      root.classList.add('is-visible');
    });
  }

  function hidePopup(root, persist) {
    root.classList.remove('is-visible');
    root.setAttribute('aria-hidden', 'true');
    if (persist) setSession(STORAGE_CLOSED);

    function onEnd(e) {
      if (e.propertyName !== 'transform' && e.propertyName !== 'opacity') return;
      root.removeEventListener('transitionend', onEnd);
      if (!root.classList.contains('is-visible')) {
        root.hidden = true;
      }
    }
    root.addEventListener('transitionend', onEnd);
    setTimeout(function () {
      if (!root.classList.contains('is-visible')) root.hidden = true;
    }, 500);
  }

  function showSuccess(root) {
    var form = root.querySelector('.yb-newsletter-popup__form');
    var success = root.querySelector('.yb-newsletter-popup__success');
    if (form) form.hidden = true;
    if (success) success.hidden = false;
    setSession(STORAGE_SUBMITTED);
    setTimeout(function () {
      hidePopup(root, false);
    }, 2800);
  }

  function init() {
    if (shouldSkip()) return;

    var root = buildPopup();
    var closeBtn = root.querySelector('.yb-newsletter-popup__close');
    var form = root.querySelector('.yb-newsletter-popup__form');
    var emailInput = root.querySelector('#yb-newsletter-email');
    var showTimer;

    closeBtn.addEventListener('click', function () {
      clearTimeout(showTimer);
      hidePopup(root, true);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && root.classList.contains('is-visible')) {
        hidePopup(root, true);
      }
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!emailInput.checkValidity()) {
        emailInput.reportValidity();
        return;
      }
      showSuccess(root);
    });

    showTimer = setTimeout(function () {
      if (shouldSkip()) return;
      showPopup(root);
    }, SHOW_DELAY_MS);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
