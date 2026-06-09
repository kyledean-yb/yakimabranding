/**
 * YB Marketing — shared HubSpot embed form
 *
 * Use the same form ID on every page. Per-page behavior is controlled with
 * data attributes on the .yb-hs-form wrapper:
 *
 *   data-redirect="../thank-you.html"  — thank-you page (auto-calculated if omitted)
 *   data-source="SEO Service Page"     — label sent as ?source= for analytics
 *   data-source-field="0-1/..."        — optional HubSpot hidden field internal name
 *
 * HubSpot also records the submission page URL automatically — you do not need
 * a separate form per page for CRM tracking.
 */
(function () {
  'use strict';

  var DEFAULT_FORM_ID = 'c7a3c349-a4e9-4608-9771-9aa39c7f05e1';

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

  function thankYouUrl() {
    var path = window.location.pathname || '/';
    var parts = path.split('/').filter(Boolean);
    if (parts.length && /\.html?$/i.test(parts[parts.length - 1])) {
      parts.pop();
    }
    var depth = parts.length;
    if (depth === 0) {
      return '/thank-you';
    }
    if (depth === 1 && parts[0] === 'services') {
      return '/services/thank-you';
    }
    if (parts[0] === 'about' && parts.length >= 2) {
      return '/about/thank-you-' + parts[1].replace(/\.html$/i, '');
    }
    if (parts[0] === 'locations' && parts.length >= 2) {
      return '/locations/thank-you-' + parts[1].replace(/\.html$/i, '');
    }
    return '/thank-you';
  }

  function getWrapper(frameEl) {
    return frameEl.closest('.yb-hs-form') || frameEl.parentElement;
  }

  function getConfig(frameEl) {
    var wrap = getWrapper(frameEl);
    var redirect = (wrap && wrap.getAttribute('data-redirect')) || thankYouUrl();
    var source =
      (wrap && wrap.getAttribute('data-source')) ||
      document.title.replace(/\s*\|\s*YB Marketing\s*$/i, '').trim();
    var sourceField = wrap && wrap.getAttribute('data-source-field');
    var pageUrl = window.location.href;
    var pagePath = window.location.pathname + window.location.search;
    return {
      formId: frameEl.getAttribute('data-form-id') || DEFAULT_FORM_ID,
      redirect: redirect,
      source: source,
      sourceField: sourceField,
      pageUrl: pageUrl,
      pagePath: pagePath,
    };
  }

  function buildRedirectUrl(base, source) {
    if (!source) return base;
    var sep = base.indexOf('?') >= 0 ? '&' : '?';
    return base + sep + 'source=' + encodeURIComponent(source);
  }

  function applyTheme() {
    document.querySelectorAll('.yb-hs-form .hs-form-frame, .yb-hs-form-panel').forEach(function (el) {
      Object.keys(THEME_VARS).forEach(function (key) {
        el.style.setProperty(key, THEME_VARS[key]);
      });
    });
  }

  function populateTrackingFields(event) {
    var formId = event.detail && event.detail.formId;
    if (!formId || !window.HubSpotFormsV4) return;

    document.querySelectorAll('.hs-form-frame[data-form-id="' + formId + '"]').forEach(function (frame) {
      var cfg = getConfig(frame);
      var form;
      try {
        form = HubSpotFormsV4.getFormFromEvent(event);
      } catch (err) {
        return;
      }
      if (!form) return;

      if (cfg.sourceField) {
        form.setFieldValue(cfg.sourceField, cfg.source);
      }

      // Common optional field names — set only if present on the form.
      ['0-1/form_submission_page', 'form_submission_page', '0-1/page_url', 'page_url'].forEach(function (name) {
        try {
          form.setFieldValue(name, cfg.pagePath);
        } catch (err) {
          /* field not on this form */
        }
      });
    });
  }

  window.addEventListener('hs-form-event:on-ready', function (event) {
    applyTheme();
    populateTrackingFields(event);
  });

  window.addEventListener('hs-form-event:on-submission:success', function (event) {
    var formId = event.detail && event.detail.formId;
    if (!formId) return;

    document.querySelectorAll('.hs-form-frame[data-form-id="' + formId + '"]').forEach(function (frame) {
      var wrap = getWrapper(frame);
      if (wrap && wrap.getAttribute('data-no-redirect') === 'true') return;
      var cfg = getConfig(frame);
      window.location.href = buildRedirectUrl(cfg.redirect, cfg.source);
    });
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyTheme);
  } else {
    applyTheme();
  }
})();
