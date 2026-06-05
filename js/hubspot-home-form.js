/**
 * YB Marketing — HubSpot home page contact form
 * Applies brand button styling and redirects to thank-you.html on success.
 */
(function () {
  'use strict';

  var HOME_FORM_ID = 'c7a3c349-a4e9-4608-9771-9aa39c7f05e1';

  var THEME_VARS = {
    '--hsf-button__font-family': "'Plus Jakarta Sans', system-ui, -apple-system, sans-serif",
    '--hsf-button__font-size': '15px',
    '--hsf-button__font-weight': '700',
    '--hsf-button__color': '#fff',
    '--hsf-button__background-color': '#3F6FD6',
    '--hsf-button__background-image': 'linear-gradient(135deg, #3F6FD6 0%, #2BC4F0 100%)',
    '--hsf-button__border-radius': '16px',
    '--hsf-button__padding': '15px 22px',
    '--hsf-button__box-shadow': '0 14px 30px -10px rgba(63, 111, 214, 0.45)',
  };

  function applyTheme() {
    document.querySelectorAll('.yb-hs-form .hs-form-frame, .yb-hs-form-panel').forEach(function (el) {
      Object.keys(THEME_VARS).forEach(function (key) {
        el.style.setProperty(key, THEME_VARS[key]);
      });
    });
  }

  window.addEventListener('hs-form-event:on-ready', function (event) {
    if (!event.detail || event.detail.formId !== HOME_FORM_ID) return;
    applyTheme();
  });

  window.addEventListener('hs-form-event:on-submission:success', function (event) {
    if (!event.detail || event.detail.formId !== HOME_FORM_ID) return;
    window.location.href = 'thank-you.html';
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyTheme);
  } else {
    applyTheme();
  }
})();
