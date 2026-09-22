/**
 * YB Marketing — custom lead forms (GoHighLevel webhook).
 *
 * Forms: form.yb-lead-form
 * Config: /js/lead-form-config.js → window.YB_LEAD_FORM.webhookUrl
 * Optional override: data-webhook on the form element
 *
 * Spam defenses (client-side):
 * - Honeypot field (injected if missing)
 * - Minimum time-to-submit
 * - Interaction required (focus/input before submit)
 * - Gibberish name heuristics
 * - Phone digit count check
 */
(function () {
  'use strict';

  var MIN_SUBMIT_MS = 2800;
  var HP_NAME = 'company_website';

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

  function ensureAntiSpamFields(form) {
    if (!form.querySelector('[name="' + HP_NAME + '"]')) {
      var wrap = document.createElement('div');
      wrap.className = 'yb-lead-form__hp';
      wrap.setAttribute('aria-hidden', 'true');
      wrap.innerHTML =
        '<label>Company website' +
        '<input type="text" name="' +
        HP_NAME +
        '" value="" tabindex="-1" autocomplete="off">' +
        '</label>';
      form.appendChild(wrap);
    }

    if (!form.querySelector('[name="form_started"]')) {
      var started = document.createElement('input');
      started.type = 'hidden';
      started.name = 'form_started';
      started.value = String(Date.now());
      form.appendChild(started);
    } else if (!form.querySelector('[name="form_started"]').value) {
      form.querySelector('[name="form_started"]').value = String(Date.now());
    }
  }

  function markInteracted(form) {
    form.dataset.ybInteracted = '1';
  }

  function vowelRatio(str) {
    var letters = (str.match(/[a-z]/gi) || []).length;
    if (!letters) return 0;
    var vowels = (str.match(/[aeiou]/gi) || []).length;
    return vowels / letters;
  }

  function looksGibberishName(name) {
    var cleaned = name.replace(/\s+/g, ' ').trim();
    if (cleaned.length < 2) return true;

    // Too few letters overall
    var lettersOnly = cleaned.replace(/[^a-z]/gi, '');
    if (lettersOnly.length < 2) return true;

    // Very low vowel density across the whole name (bots like "Sczkkgxk Vhkeuxtk")
    if (lettersOnly.length >= 8 && vowelRatio(lettersOnly) < 0.18) return true;

    var parts = cleaned.split(' ').filter(Boolean);
    if (parts.length >= 2) {
      var gibberishParts = 0;
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i].replace(/[^a-z]/gi, '');
        if (p.length < 2) continue;
        var vr = vowelRatio(p);
        var hasRareCluster = /[bcdfghjklmnpqrstvwxyz]{5,}/i.test(p) || /[xqzjk]{2,}/i.test(p);
        if ((p.length >= 5 && vr < 0.2) || (p.length >= 6 && hasRareCluster && vr < 0.28)) {
          gibberishParts++;
        }
      }
      if (gibberishParts >= 2) return true;
    } else if (lettersOnly.length >= 8 && vowelRatio(lettersOnly) < 0.22) {
      return true;
    }

    // Keyboard-smash: many identical adjacent consonants
    if (/(.)\1{3,}/i.test(lettersOnly)) return true;

    return false;
  }

  function phoneDigitCount(phone) {
    return (phone.match(/\d/g) || []).length;
  }

  function spamReason(form, data) {
    var hp = form.querySelector('[name="' + HP_NAME + '"]');
    if (hp && String(hp.value || '').trim()) {
      return 'honeypot';
    }

    var startedEl = form.querySelector('[name="form_started"]');
    var started = startedEl ? parseInt(startedEl.value, 10) : 0;
    if (!started || Date.now() - started < MIN_SUBMIT_MS) {
      return 'too_fast';
    }

    if (form.dataset.ybInteracted !== '1') {
      return 'no_interaction';
    }

    if (looksGibberishName(data.name)) {
      return 'gibberish_name';
    }

    if (phoneDigitCount(data.phone) < 10) {
      return 'bad_phone';
    }

    // Obvious disposable / role-spam patterns (light touch)
    var email = data.email.toLowerCase();
    if (/@(mailinator|guerrillamail|tempmail|10minutemail|yopmail|trashmail)\./i.test(email)) {
      return 'disposable_email';
    }

    return '';
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

    ensureAntiSpamFields(form);

    var pageInput = form.querySelector('input[name="page_url"]');
    if (pageInput) pageInput.value = window.location.href;

    form.addEventListener(
      'focusin',
      function () {
        markInteracted(form);
      },
      true
    );
    form.addEventListener(
      'input',
      function () {
        markInteracted(form);
      },
      true
    );

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
      var reason = spamReason(form, data);

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

      // Soft user-facing rejects (likely a real person who typed badly)
      if (reason === 'gibberish_name') {
        finishErr('Please enter your real first and last name.');
        return;
      }
      if (reason === 'bad_phone') {
        finishErr('Please enter a valid phone number.');
        return;
      }
      if (reason === 'disposable_email') {
        finishErr('Please use a permanent work or personal email address.');
        return;
      }

      // Silent bot rejects: fake success, do not hit GHL
      if (reason === 'honeypot' || reason === 'too_fast' || reason === 'no_interaction') {
        finishOk();
        return;
      }

      if (btn) {
        btn.disabled = true;
        btn.classList.add('is-loading');
      }
      setStatus(form, 'Sending…', false);

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
