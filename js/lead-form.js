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
 * - US-only phone check (10 digits, valid area code, no Canada/Caribbean +1 codes)
 * - Message must include letters (blocks phone-only comments)
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

  // +1 area codes that belong to Canada and the Caribbean, not the US.
  var NON_US_AREA_CODES =
    '204 226 236 249 250 257 263 289 306 343 354 365 367 368 382 387 403 416 418 428 431 437 438 450 460 468 474 ' +
    '506 514 519 548 579 581 584 587 604 613 639 647 672 683 705 709 742 753 778 780 782 807 819 825 867 873 879 ' +
    '902 905 942 242 246 264 268 284 345 441 473 649 658 664 721 758 767 784 809 829 849 868 869 876';
  var NON_US = {};
  NON_US_AREA_CODES.split(' ').forEach(function (c) {
    NON_US[c] = true;
  });

  function isUsPhone(phone) {
    var raw = String(phone || '').trim();
    if (!raw || /[a-z]/i.test(raw)) return false;
    if (raw.charAt(0) === '+' && !/^\+\s*1(\D|$)/.test(raw)) return false;
    var digits = raw.replace(/\D/g, '');
    if (/^(011|00)/.test(digits)) return false;
    if (digits.length === 11 && digits.charAt(0) === '1') digits = digits.slice(1);
    if (digits.length !== 10) return false;
    var area = digits.slice(0, 3);
    var exchange = digits.slice(3, 6);
    if (!/^[2-9]\d\d$/.test(area) || /^[2-9]11$/.test(area)) return false;
    if (!/^[2-9]\d\d$/.test(exchange) || /^[2-9]11$/.test(exchange)) return false;
    if (NON_US[area]) return false;
    if (/^(\d)\1{9}$/.test(digits) || digits === '1234567890') return false;
    if (exchange === '555' && /^01\d\d$/.test(digits.slice(6))) return false;
    return true;
  }

  function messageHasLetters(message) {
    return /[a-zA-Z\u00C0-\u024F]/.test(message);
  }

  function messageMissingLetters(message) {
    var cleaned = message.replace(/\s+/g, ' ').trim();
    // Required: must have content with real letters (blocks empty + phone-only spam)
    if (!cleaned || !messageHasLetters(cleaned)) return true;
    return false;
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

    if (!isUsPhone(data.phone)) {
      return 'bad_phone';
    }

    if (messageMissingLetters(data.message)) {
      return 'message_no_letters';
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
        finishErr('Please enter a valid US phone number. We are not able to accept international numbers.');
        return;
      }
      if (reason === 'message_no_letters') {
        finishErr('Please enter a message with a few words about how we can help.');
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
