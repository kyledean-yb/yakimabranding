/**
 * YB Marketing — contact form submit → thank-you redirect
 */
(function () {
  'use strict';

  function thankYouUrl(form) {
    if (form && form.dataset.thankYou) {
      return form.dataset.thankYou;
    }
    var path = window.location.pathname || '/';
    var parts = path.split('/').filter(Boolean);
    if (parts.length && /\.html?$/i.test(parts[parts.length - 1])) {
      parts.pop();
    }
    if (parts.length === 0) {
      return '/thank-you';
    }
    if (parts[0] === 'about' && parts.length >= 2) {
      return '/about/thank-you-' + parts[1].replace(/\.html$/i, '');
    }
    if (parts[0] === 'locations' && parts.length >= 2) {
      return '/locations/thank-you-' + parts[1].replace(/\.html$/i, '');
    }
    if (parts[0] === 'services') {
      return '/services/thank-you';
    }
    if (parts[0] === 'landing-page') {
      return '/thank-you-landing-page';
    }
    return '/thank-you';
  }

  function redirectThankYou(form) {
    window.location.href = thankYouUrl(form);
  }

  function bindForm(form) {
    if (!form || form.dataset.ybBound) return;
    form.dataset.ybBound = '1';
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (typeof form.checkValidity === 'function' && !form.checkValidity()) {
        form.reportValidity();
        return;
      }
      redirectThankYou(form);
    });
  }

  function bindSendMessageButtons() {
    document.querySelectorAll('button.btn-grad').forEach(function (btn) {
      if (btn.dataset.ybBound) return;
      if (btn.type === 'submit' && btn.closest('form.yb-contact-form, form#contactForm, form.team-form')) {
        return;
      }
      var label = (btn.textContent || '').replace(/\s+/g, ' ').trim();
      if (label.indexOf('Send Message') === -1) return;
      if (btn.closest('#cal-widget, .calendly-inline-widget')) return;

      btn.dataset.ybBound = '1';
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var panel = btn.closest('form, #contactForm, #modalForm, #ctaModal, section#contact, .team-aside-form');
        if (panel && panel.tagName === 'FORM') return;
        redirectThankYou();
      });
    });
  }

  function init() {
    document
      .querySelectorAll('form.yb-contact-form, form#contactForm, form.team-form')
      .forEach(bindForm);
    bindSendMessageButtons();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
