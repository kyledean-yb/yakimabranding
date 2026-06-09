/**
 * YB Marketing — newsletter signup popup (non-intrusive)
 * Dismissal is stored in localStorage so close/submit persists across visits.
 */
(function () {
  'use strict';

  var STORAGE_CLOSED = 'ybNewsletterClosed';
  var STORAGE_SUBMITTED = 'ybNewsletterSubmitted';
  var SHOW_DELAY_MS = 8000;

  var HS_PORTAL_ID = '243964841';
  var HS_REGION = 'na2';
  var HS_EMBED_SRC = 'https://js-na2.hsforms.net/forms/embed/' + HS_PORTAL_ID + '.js';
  var NEWSLETTER_FORM_ID = 'b3ac7d7d-6b8a-4e85-adc2-41cc98a8cdad';

  var POPUP_THEME_VARS = {
    '--hsf-global__font-family': "'Plus Jakarta Sans', system-ui, -apple-system, sans-serif",
    '--hsf-global__font-size': '14px',
    '--hsf-global__color': '#16203A',
    '--hsf-background__background-color': 'transparent',
    '--hsf-background__border-width': '0',
    '--hsf-background__padding': '0',
    '--hsf-row__vertical-spacing': '0',
    '--hsf-row__horizontal-spacing': '10px',
    '--hsf-module__vertical-spacing': '0',
    '--hsf-field-label__font-size': '0',
    '--hsf-field-label__padding': '0',
    '--hsf-field-label__margin': '0',
    '--hsf-field-input__font-family': "'Plus Jakarta Sans', system-ui, -apple-system, sans-serif",
    '--hsf-field-input__font-size': '14px',
    '--hsf-field-input__color': '#16203A',
    '--hsf-field-input__background-color': '#fff',
    '--hsf-field-input__placeholder-color': '#7C879E',
    '--hsf-field-input__border-color': '#CFD8E8',
    '--hsf-field-input__border-width': '1px',
    '--hsf-field-input__border-radius': '10px',
    '--hsf-field-input__padding': '12px 14px',
    '--hsf-button__font-family': "'Plus Jakarta Sans', system-ui, -apple-system, sans-serif",
    '--hsf-button__font-size': '14px',
    '--hsf-button__font-weight': '700',
    '--hsf-button__color': '#fff',
    '--hsf-button__background-color': '#3F6FD6',
    '--hsf-button__background-image': 'linear-gradient(135deg, #3F6FD6 0%, #2BC4F0 100%)',
    '--hsf-button__border-radius': '10px',
    '--hsf-button__padding': '12px 18px',
    '--hsf-button__box-shadow': '0 8px 22px rgba(63, 111, 214, 0.28)',
    '--hsf-heading__font-size': '0',
    '--hsf-heading__margin': '0',
    '--hsf-richtext__font-size': '0',
    '--hsf-richtext__margin': '0',
  };

  function shouldSkip() {
    try {
      return (
        localStorage.getItem(STORAGE_CLOSED) === '1' ||
        localStorage.getItem(STORAGE_SUBMITTED) === '1'
      );
    } catch (e) {
      return false;
    }
  }

  function persistDismissal(key) {
    try {
      localStorage.setItem(key, '1');
    } catch (e) {
      /* ignore */
    }
  }

  function staticFormHtml() {
    return (
      '<form class="yb-newsletter-popup__form" action="#" method="post" novalidate>' +
      '  <label class="yb-newsletter-popup__label" for="yb-newsletter-email">Email address</label>' +
      '  <div class="yb-newsletter-popup__fields">' +
      '    <input id="yb-newsletter-email" class="yb-newsletter-popup__input" type="email" name="email" autocomplete="email" placeholder="you@company.com" required>' +
      '    <button type="submit" class="yb-newsletter-popup__submit">Sign Up</button>' +
      '  </div>' +
      '</form>'
    );
  }

  function hubspotFormHtml() {
    return (
      '<div class="yb-newsletter-popup__fields yb-newsletter-popup__fields--hs">' +
      '  <div class="yb-hs-form yb-newsletter-popup__hs" data-source="Newsletter Popup" data-no-redirect="true">' +
      '    <div class="hs-form-frame" data-region="' +
      HS_REGION +
      '" data-form-id="' +
      NEWSLETTER_FORM_ID +
      '" data-portal-id="' +
      HS_PORTAL_ID +
      '"></div>' +
      '  </div>' +
      '</div>'
    );
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

    var formBlock = NEWSLETTER_FORM_ID ? hubspotFormHtml() : staticFormHtml();

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
      formBlock +
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
    if (persist) persistDismissal(STORAGE_CLOSED);
    root.classList.remove('is-visible');
    root.setAttribute('aria-hidden', 'true');

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
    var form = root.querySelector('.yb-newsletter-popup__form, .yb-newsletter-popup__fields--hs');
    var success = root.querySelector('.yb-newsletter-popup__success');
    if (form) form.hidden = true;
    if (success) success.hidden = false;
    persistDismissal(STORAGE_SUBMITTED);
    setTimeout(function () {
      hidePopup(root, false);
    }, 2800);
  }

  function applyHubSpotTheme(root) {
    root.querySelectorAll('.yb-newsletter-popup__hs .hs-form-frame, .yb-newsletter-popup__hs').forEach(function (el) {
      Object.keys(POPUP_THEME_VARS).forEach(function (key) {
        el.style.setProperty(key, POPUP_THEME_VARS[key]);
      });
    });
  }

  function populateTrackingFields(event) {
    if (!NEWSLETTER_FORM_ID || !event.detail || event.detail.formId !== NEWSLETTER_FORM_ID) return;
    if (!window.HubSpotFormsV4) return;

    var frame = document.querySelector('#yb-newsletter-popup .hs-form-frame[data-form-id="' + NEWSLETTER_FORM_ID + '"]');
    if (!frame) return;

    var form;
    try {
      form = HubSpotFormsV4.getFormFromEvent(event);
    } catch (err) {
      return;
    }
    if (!form) return;

    var pagePath = window.location.pathname + window.location.search;
    ['0-1/form_submission_page', 'form_submission_page', '0-1/page_url', 'page_url'].forEach(function (name) {
      try {
        form.setFieldValue(name, pagePath);
      } catch (err) {
        /* field not on this form */
      }
    });
  }

  function loadHubSpotEmbed(root, callback) {
    var frame = root.querySelector('.hs-form-frame');
    var scriptSelector = 'script[src*="hsforms.net/forms/embed/' + HS_PORTAL_ID + '"]';

    function done() {
      applyHubSpotTheme(root);
      if (typeof callback === 'function') callback();
    }

    function loadScript() {
      var script = document.createElement('script');
      script.src = HS_EMBED_SRC;
      script.defer = true;
      script.onload = done;
      document.head.appendChild(script);
    }

    if (!frame) {
      done();
      return;
    }

    // HubSpot scans the DOM when its embed script runs — load after the frame exists.
    if (!document.querySelector(scriptSelector)) {
      loadScript();
      return;
    }

    // Script already on page (e.g. home/contact) — re-run embed so the popup frame renders.
    if (!frame.querySelector('iframe')) {
      loadScript();
      return;
    }

    done();
  }

  function bindHubSpot(root) {
    if (!NEWSLETTER_FORM_ID) return;

    loadHubSpotEmbed(root, function () {
      applyHubSpotTheme(root);
    });

    window.addEventListener('hs-form-event:on-ready', function (event) {
      if (!event.detail || event.detail.formId !== NEWSLETTER_FORM_ID) return;
      if (!root.querySelector('.hs-form-frame[data-form-id="' + NEWSLETTER_FORM_ID + '"]')) return;
      applyHubSpotTheme(root);
      populateTrackingFields(event);
    });

    window.addEventListener('hs-form-event:on-submission:success', function (event) {
      if (!event.detail || event.detail.formId !== NEWSLETTER_FORM_ID) return;
      if (!root.querySelector('.hs-form-frame[data-form-id="' + NEWSLETTER_FORM_ID + '"]')) return;
      showSuccess(root);
    });
  }

  function bindStaticForm(root) {
    var form = root.querySelector('.yb-newsletter-popup__form');
    var emailInput = root.querySelector('#yb-newsletter-email');
    if (!form || !emailInput) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!emailInput.checkValidity()) {
        emailInput.reportValidity();
        return;
      }
      showSuccess(root);
    });
  }

  function init() {
    if (shouldSkip()) return;

    var root = buildPopup();
    var closeBtn = root.querySelector('.yb-newsletter-popup__close');
    var showTimer;

    closeBtn.addEventListener('click', function () {
      clearTimeout(showTimer);
      persistDismissal(STORAGE_CLOSED);
      hidePopup(root, false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && root.classList.contains('is-visible')) {
        clearTimeout(showTimer);
        persistDismissal(STORAGE_CLOSED);
        hidePopup(root, false);
      }
    });

    if (NEWSLETTER_FORM_ID) {
      bindHubSpot(root);
    } else {
      bindStaticForm(root);
    }

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
