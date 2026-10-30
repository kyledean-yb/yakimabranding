/**
 * YB Marketing — newsletter signup popup (non-intrusive)
 * Signups post to the GoHighLevel webhook in /js/lead-form-config.js with source "Newsletter Popup".
 * Dismissal is stored in localStorage so close/submit persists across visits.
 */
(function () {
  'use strict';

  var STORAGE_CLOSED = 'ybNewsletterClosed';
  var STORAGE_SUBMITTED = 'ybNewsletterSubmitted';
  var SHOW_DELAY_MS = 8000;
  var MIN_SUBMIT_MS = 1500;
  var SOURCE = 'Newsletter Popup';
  var HP_NAME = 'company_website';

  // Used when a page loads this script without /js/lead-form-config.js
  var FALLBACK_WEBHOOK =
    'https://services.leadconnectorhq.com/hooks/0Pc2NnJAQkzYB3hhPi1b/webhook-trigger/1865a2f2-d6f5-48ec-a4a7-4d68fb92f329';

  function cfg() {
    return window.YB_LEAD_FORM || {};
  }

  function isSpanish() {
    return /^\/es(\/|$)/.test(window.location.pathname);
  }

  var COPY = isSpanish()
    ? {
        eyebrow: 'Boletín',
        title: 'Consejos de marketing que sí ayudan',
        body: 'Únase a nuestro boletín para recibir ideas prácticas de marketing digital, consejos para su sitio web y formas de hacer crecer su negocio.',
        label: 'Correo electrónico',
        placeholder: 'usted@empresa.com',
        submit: 'Suscribirse',
        sending: 'Enviando…',
        success: '¡Gracias por suscribirse! Revise su correo pronto.',
        badEmail: 'Por favor use un correo electrónico permanente.',
        close: 'Cerrar suscripción al boletín',
      }
    : {
        eyebrow: 'Newsletter',
        title: 'Get Marketing Tips That Actually Help',
        body: 'Join our newsletter for practical digital marketing insights, website tips, and ideas to help your business grow.',
        label: 'Email address',
        placeholder: 'you@company.com',
        submit: 'Sign Up',
        sending: 'Sending…',
        success: 'Thanks for signing up! Check your inbox soon.',
        badEmail: 'Please use a permanent work or personal email address.',
        close: 'Close newsletter signup',
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

  function formHtml() {
    return (
      '<form class="yb-newsletter-popup__form" action="#" method="post" novalidate>' +
      '  <label class="yb-newsletter-popup__label" for="yb-newsletter-email">' + COPY.label + '</label>' +
      '  <div class="yb-newsletter-popup__fields">' +
      '    <input id="yb-newsletter-email" class="yb-newsletter-popup__input" type="email" name="email" autocomplete="email" placeholder="' + COPY.placeholder + '" required>' +
      '    <button type="submit" class="yb-newsletter-popup__submit">' + COPY.submit + '</button>' +
      '  </div>' +
      '  <div class="yb-newsletter-popup__hp" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden">' +
      '    <label>Company website<input type="text" name="' + HP_NAME + '" value="" tabindex="-1" autocomplete="off"></label>' +
      '  </div>' +
      '  <p class="yb-newsletter-popup__error" role="alert" style="font-size:13px;font-weight:600;color:#c0392b;margin:8px 0 0" hidden></p>' +
      '</form>'
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

    root.innerHTML =
      '<div class="yb-newsletter-popup__card">' +
      '  <button type="button" class="yb-newsletter-popup__close" aria-label="' + COPY.close + '">' +
      '    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true">' +
      '      <path d="M18 6L6 18M6 6l12 12"/>' +
      '    </svg>' +
      '  </button>' +
      '  <div class="yb-newsletter-popup__content">' +
      '    <p class="yb-newsletter-popup__eyebrow">' + COPY.eyebrow + '</p>' +
      '    <h2 id="yb-newsletter-title" class="yb-newsletter-popup__title">' + COPY.title + '</h2>' +
      '    <p id="yb-newsletter-desc" class="yb-newsletter-popup__body">' + COPY.body + '</p>' +
      formHtml() +
      '    <p class="yb-newsletter-popup__success" role="status" aria-live="polite" hidden>' + COPY.success + '</p>' +
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
    var form = root.querySelector('.yb-newsletter-popup__form');
    var success = root.querySelector('.yb-newsletter-popup__success');
    if (form) form.hidden = true;
    if (success) success.hidden = false;
    persistDismissal(STORAGE_SUBMITTED);
    setTimeout(function () {
      hidePopup(root, false);
    }, 2800);
  }

  function setError(root, message) {
    var el = root.querySelector('.yb-newsletter-popup__error');
    if (!el) return;
    el.textContent = message || '';
    el.hidden = !message;
  }

  function payload(email) {
    var c = cfg();
    return {
      name: '',
      email: email,
      phone: '',
      company: '',
      interest: 'newsletter',
      interest_label: 'Newsletter',
      message: 'Newsletter signup',
      source: SOURCE,
      site: (c.site || 'YB Marketing').toString(),
      site_domain: (c.siteDomain || 'yakimabranding.com').toString(),
      language: isSpanish() ? 'es' : 'en',
      page_url: window.location.href,
      page_path: window.location.pathname + window.location.search,
      submitted_at: new Date().toISOString(),
    };
  }

  function bindForm(root, openedAt) {
    var form = root.querySelector('.yb-newsletter-popup__form');
    var emailInput = root.querySelector('#yb-newsletter-email');
    var btn = root.querySelector('.yb-newsletter-popup__submit');
    if (!form || !emailInput) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      setError(root, '');
      if (!emailInput.checkValidity()) {
        emailInput.reportValidity();
        return;
      }

      var email = emailInput.value.trim();
      var hp = form.querySelector('[name="' + HP_NAME + '"]');
      var isBot = (hp && hp.value.trim()) || Date.now() - openedAt() < MIN_SUBMIT_MS;
      if (isBot) {
        showSuccess(root);
        return;
      }

      if (/@(mailinator|guerrillamail|tempmail|10minutemail|yopmail|trashmail)\./i.test(email)) {
        setError(root, COPY.badEmail);
        return;
      }

      var url = (cfg().webhookUrl || FALLBACK_WEBHOOK).trim();
      if (btn) {
        btn.disabled = true;
        btn.textContent = COPY.sending;
      }

      fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload(email)),
        mode: 'cors',
        keepalive: true,
      })
        .catch(function () {
          /* GHL often accepts the request even when the browser cannot read the CORS response */
        })
        .then(function () {
          showSuccess(root);
        });
    });
  }

  function init() {
    if (shouldSkip()) return;

    var root = buildPopup();
    var closeBtn = root.querySelector('.yb-newsletter-popup__close');
    var showTimer;
    var shownAt = 0;

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

    bindForm(root, function () {
      return shownAt;
    });

    showTimer = setTimeout(function () {
      if (shouldSkip()) return;
      shownAt = Date.now();
      showPopup(root);
    }, SHOW_DELAY_MS);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
