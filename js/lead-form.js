/**
 * YB Marketing — custom lead forms (GoHighLevel webhook).
 *
 * Forms: form.yb-lead-form
 * Config: /js/lead-form-config.js → window.YB_LEAD_FORM.webhookUrl
 * Optional override: data-webhook on the form element
 */
(function () {
  'use strict';

  function cfg() {
    return window.YB_LEAD_FORM || {};
  }

  function thankYouUrl(form) {
    var redirect = form.getAttribute('data-redirect');
    if (redirect) return redirect;
    if (form.dataset.thankYou) return form.dataset.thankYou;
    return '/thank-you';
  }

  function buildRedirect(base, source) {
    if (!source) return base;
    var sep = base.indexOf('?') >= 0 ? '&' : '?';
    return base + sep + 'source=' + encodeURIComponent(source);
  }

  function setStatus(form, message, isError) {
    var el = form.querySelector('.yb-lead-form__status');
    if (!el) return;
    el.hidden = !message;
    el.textContent = message || '';
    el.classList.toggle('is-error', !!isError);
  }

  function payloadFromForm(form) {
    var fd = new FormData(form);
    var pageUrl = window.location.href;
    var pagePath = window.location.pathname + window.location.search;
    var interestSelect = form.querySelector('[name="interest"]');
    var interestLabel = '';
    if (interestSelect && interestSelect.selectedIndex >= 0) {
      interestLabel = interestSelect.options[interestSelect.selectedIndex].text || '';
    }
    var c = cfg();
    return {
      name: (fd.get('name') || '').toString().trim(),
      email: (fd.get('email') || '').toString().trim(),
      phone: (fd.get('phone') || '').toString().trim(),
      company: (fd.get('company') || '').toString().trim(),
      interest: (fd.get('interest') || '').toString().trim(),
      interest_label: interestLabel,
      message: (fd.get('message') || '').toString().trim(),
      source: (fd.get('source') || form.getAttribute('data-source') || '').toString().trim(),
      site: (c.site || 'YB Marketing').toString(),
      site_domain: (c.siteDomain || 'yakimabranding.com').toString(),
      page_url: pageUrl,
      page_path: pagePath,
      submitted_at: new Date().toISOString(),
    };
  }

  function webhookUrl(form) {
    return (
      (form.getAttribute('data-webhook') || '').trim() ||
      (cfg().webhookUrl || '').trim()
    );
  }

  function postWebhook(url, data) {
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(data),
      mode: 'cors',
      keepalive: true,
    });
  }

  function bindForm(form) {
    if (!form || form.dataset.ybLeadBound) return;
    form.dataset.ybLeadBound = '1';

    var pageInput = form.querySelector('input[name="page_url"]');
    if (pageInput) pageInput.value = window.location.href;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (typeof form.checkValidity === 'function' && !form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var btn = form.querySelector('.yb-lead-form__submit, button[type="submit"]');
      var data = payloadFromForm(form);
      var redirect = buildRedirect(thankYouUrl(form), data.source);
      var url = webhookUrl(form);

      if (btn) {
        btn.disabled = true;
        btn.classList.add('is-loading');
      }
      setStatus(form, 'Sending…', false);

      function finishOk() {
        window.location.href = redirect;
      }

      function finishErr(msg) {
        if (btn) {
          btn.disabled = false;
          btn.classList.remove('is-loading');
        }
        setStatus(
          form,
          msg || 'Something went wrong. Please try again or call (509) 901-9735.',
          true
        );
      }

      if (!url) {
        finishOk();
        return;
      }

      postWebhook(url, data)
        .then(function (res) {
          if (!res.ok) throw new Error('Webhook status ' + res.status);
          finishOk();
        })
        .catch(function () {
          // GHL often accepts the request even when the browser cannot read CORS response.
          finishOk();
        });
    });
  }

  function init() {
    document.querySelectorAll('form.yb-lead-form').forEach(bindForm);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
