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

  /** Compact horizontal header form on HVAC landing page */
  var LANDING_HEADER_THEME_VARS = {
    '--hsf-button__font-family': "'Plus Jakarta Sans', system-ui, -apple-system, sans-serif",
    '--hsf-button__font-size': '15px',
    '--hsf-button__font-weight': '700',
    '--hsf-button__color': '#244aa3',
    '--hsf-button__background-color': '#ffffff',
    '--hsf-button__background-image': 'none',
    '--hsf-button__border-radius': '16px',
    '--hsf-button__padding': '13px 18px',
    '--hsf-button__box-shadow': '0 8px 20px -6px rgba(16, 28, 58, 0.45)',
    '--hsf-field-label__color': 'rgba(255, 255, 255, 0.9)',
    '--hsf-field-label__font-size': '12px',
    '--hsf-field-label__font-weight': '700',
    '--hsf-field-input__border-radius': '14px',
    '--hsf-field-input__border-color': 'transparent',
    '--hsf-field-input__padding': '11px 14px',
    '--hsf-field-phone__border-radius': '14px',
    '--hsf-field-phone__border-color': 'transparent',
    '--hsf-field-phone__padding': '11px 14px',
    '--hsf-row__vertical-spacing': '0px',
    '--hsf-row__horizontal-spacing': '10px',
    '--hsf-module__vertical-spacing': '0px',
    '--hsf-background__padding': '0px',
    '--hsf-background__background-color': 'transparent',
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
    if (parts[0] === 'phx-hvac' || parts[0] === 'landing-page') {
      return '/thank-you-landing-page';
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
    document.querySelectorAll('.hs-form-frame, .yb-hs-form-panel').forEach(function (el) {
      var wrap =
        (el.closest && el.closest('.yb-hs-form')) ||
        (el.closest && el.closest('[data-yb-theme]')) ||
        el.parentElement;
      var themeName = wrap && wrap.getAttribute && wrap.getAttribute('data-yb-theme');
      var vars = themeName === 'landing-header' ? LANDING_HEADER_THEME_VARS : THEME_VARS;
      Object.keys(vars).forEach(function (key) {
        el.style.setProperty(key, vars[key]);
      });
    });
  }

  /** HubSpot V4 may rewrite CSS vars after mount — re-apply for themed embeds. */
  function applyThemePersistent() {
    applyTheme();
    [50, 200, 600, 1200, 2500, 5000].forEach(function (ms) {
      setTimeout(applyTheme, ms);
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
    applyThemePersistent();
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
