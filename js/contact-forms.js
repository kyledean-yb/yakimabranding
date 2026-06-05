/**
 * YB Marketing — contact form submit → thank-you redirect
 */
(function () {
  'use strict';

  function thankYouUrl() {
    var path = window.location.pathname || '';
    var parts = path.split('/').filter(Boolean);
    if (parts.length && /\.html?$/i.test(parts[parts.length - 1])) {
      parts.pop();
    }
    var prefix = parts.length ? '../'.repeat(parts.length) : '';
    return prefix + 'thank-you.html';
  }

  function redirectThankYou() {
    window.location.href = thankYouUrl();
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
      redirectThankYou();
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
