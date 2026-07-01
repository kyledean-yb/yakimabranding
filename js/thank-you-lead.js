(function () {
  'use strict';

  var fired = false;
  var source = document.documentElement.getAttribute('data-yb-lead-source') || 'thank_you';

  function hasConsent() {
    return window.ybCookieConsent && window.ybCookieConsent.hasAccepted();
  }

  function fireLeadEvents() {
    if (fired || !hasConsent()) return;
    fired = true;

    if (typeof window.gtag === 'function') {
      window.gtag('event', 'generate_lead', { lead_source: source });
    }
    if (typeof window.fbq === 'function') {
      window.fbq('track', 'Lead');
    }
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'generate_lead',
      lead_source: source,
    });
  }

  function whenReady() {
    if (!hasConsent()) return;

    if (document.documentElement.getAttribute('data-yb-tracking') === 'loaded') {
      fireLeadEvents();
      return;
    }

    document.addEventListener('yb:tracking-loaded', fireLeadEvents, { once: true });

    var attempts = 0;
    (function poll() {
      if (document.documentElement.getAttribute('data-yb-tracking') === 'loaded' || attempts > 60) {
        fireLeadEvents();
        return;
      }
      attempts += 1;
      setTimeout(poll, 100);
    })();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', whenReady);
  } else {
    whenReady();
  }
})();
