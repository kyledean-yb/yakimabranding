(function () {
  'use strict';

  var STORAGE_KEY = 'yb_cookie_consent';
  var CONSENT_VERSION = '1';
  var loaded = false;

  var IDS = {
    ga4: 'G-3VYDDP5HRC',
    gtm: 'GTM-MTPC7RXT',
    fb: '3203577076442176',
  };

  function readConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var data = JSON.parse(raw);
      if (!data || data.version !== CONSENT_VERSION) return null;
      return data.choice;
    } catch (e) {
      return null;
    }
  }

  function writeConsent(choice) {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ choice: choice, version: CONSENT_VERSION, ts: Date.now() })
      );
    } catch (e) {
      /* ignore */
    }
  }

  function injectScript(src, attrs) {
    var s = document.createElement('script');
    s.src = src;
    s.async = true;
    if (attrs) {
      Object.keys(attrs).forEach(function (key) {
        s.setAttribute(key, attrs[key]);
      });
    }
    (document.head || document.documentElement).appendChild(s);
    return s;
  }

  function injectInlineScript(code) {
    var s = document.createElement('script');
    s.text = code;
    (document.head || document.documentElement).appendChild(s);
  }

  function injectStylesheet(href) {
    if (document.querySelector('link[href="' + href + '"]')) return;
    var l = document.createElement('link');
    l.rel = 'stylesheet';
    l.href = href;
    (document.head || document.documentElement).appendChild(l);
  }

  function loadAdviceLocal() {
    injectStylesheet('https://widget.advicelocal.com/bundle.css');
    injectScript('https://widget.advicelocal.com/bundle.js', { defer: '', async: '' });
    injectScript('https://widget.advicelocal.com/bundle.js.map', { defer: '', async: '' });
  }

  function loadGA4() {
    window.dataLayer = window.dataLayer || [];
    window.gtag =
      window.gtag ||
      function () {
        window.dataLayer.push(arguments);
      };
    window.gtag('js', new Date());
    window.gtag('config', IDS.ga4);
    injectScript('https://www.googletagmanager.com/gtag/js?id=' + IDS.ga4);
  }

  function loadGTM() {
    (function (w, d, s, l, i) {
      w[l] = w[l] || [];
      w[l].push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
      var f = d.getElementsByTagName(s)[0];
      var j = d.createElement(s);
      var dl = l !== 'dataLayer' ? '&l=' + l : '';
      j.async = true;
      j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
      f.parentNode.insertBefore(j, f);
    })(window, document, 'script', 'dataLayer', IDS.gtm);

    if (!document.getElementById('yb-gtm-noscript')) {
      var noscript = document.createElement('noscript');
      noscript.id = 'yb-gtm-noscript';
      noscript.innerHTML =
        '<iframe src="https://www.googletagmanager.com/ns.html?id=' +
        IDS.gtm +
        '" height="0" width="0" style="display:none;visibility:hidden"></iframe>';
      document.body.appendChild(noscript);
    }
  }

  function loadFacebookPixel() {
    !(function (f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n;
      n.loaded = !0;
      n.version = '2.0';
      n.queue = [];
      t = b.createElement(e);
      t.async = !0;
      t.src = v;
      s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', IDS.fb);
    window.fbq('track', 'PageView');
  }

  function loadZoomInfo() {
    injectInlineScript(
      "window[(function(_YRK,_Le){var _pUnlL='';for(var _D6FvKd=0;_D6FvKd<_YRK.length;_D6FvKd++){_pUnlL==_pUnlL;var _qjOs=_YRK[_D6FvKd].charCodeAt();_Le>9;_qjOs!=_D6FvKd;_qjOs-=_Le;_qjOs+=61;_qjOs%=94;_qjOs+=33;_pUnlL+=String.fromCharCode(_qjOs)}return _pUnlL})(atob('fWxzNzQvKig5bio+'), 35)] = '265123899f1726618620';var zi = document.createElement('script');(zi.type = 'text/javascript'),(zi.async = true),(zi.src = (function(_gNy,_HO){var _W0lBx='';for(var _dYyvji=0;_dYyvji<_gNy.length;_dYyvji++){var _VGTg=_gNy[_dYyvji].charCodeAt();_VGTg-=_HO;_VGTg+=61;_HO>9;_VGTg%=94;_W0lBx==_W0lBx;_VGTg!=_dYyvji;_VGTg+=33;_W0lBx+=String.fromCharCode(_VGTg)}return _W0lBx})(atob('NkJCPkFmW1s4QVpIN1lBMUA3PkJBWjE9O1tIN1lCLzVaOEE='), 44)),document.readyState === 'complete'?document.body.appendChild(zi):window.addEventListener('load', function(){document.body.appendChild(zi)});"
    );
  }

  function loadAttributer() {
    if (document.querySelector('script[src*="attributer.js"]')) return;
    injectScript('https://d1b3llzbo1rqxo.cloudfront.net/attributer.js');
  }

  function loadAllTracking() {
    if (loaded) return;
    loaded = true;
    loadAdviceLocal();
    loadGA4();
    loadGTM();
    loadFacebookPixel();
    loadZoomInfo();
    loadAttributer();
    document.documentElement.setAttribute('data-yb-tracking', 'loaded');
    document.dispatchEvent(new CustomEvent('yb:tracking-loaded'));
  }

  function hideBanner() {
    var banner = document.getElementById('ybCookieBanner');
    if (banner) banner.hidden = true;
  }

  function showBanner() {
    if (document.getElementById('ybCookieBanner')) return;

    var privacyHref = '/privacy-policy';
    var banner = document.createElement('div');
    banner.id = 'ybCookieBanner';
    banner.className = 'yb-cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-live', 'polite');
    banner.setAttribute('aria-label', 'Cookie consent');
    banner.innerHTML =
      '<div class="yb-cookie-banner__panel">' +
      '<p class="yb-cookie-banner__copy">' +
      '<span class="yb-cookie-banner__title">We value your privacy</span>' +
      'We use cookies and similar technologies for analytics, advertising, and marketing. ' +
      'Under California privacy law, you can choose whether non-essential cookies are used. ' +
      'Essential site features work without accepting. ' +
      '<a href="' +
      privacyHref +
      '">Privacy Policy</a>.' +
      '</p>' +
      '<div class="yb-cookie-banner__actions">' +
      '<button type="button" class="yb-cookie-banner__btn yb-cookie-banner__btn--reject" data-yb-cookie-choice="rejected">Reject</button>' +
      '<button type="button" class="yb-cookie-banner__btn yb-cookie-banner__btn--accept" data-yb-cookie-choice="accepted">Accept</button>' +
      '</div>' +
      '</div>';

    document.body.appendChild(banner);

    banner.addEventListener('click', function (event) {
      var btn = event.target.closest('[data-yb-cookie-choice]');
      if (!btn) return;
      var choice = btn.getAttribute('data-yb-cookie-choice');
      writeConsent(choice);
      hideBanner();
      if (choice === 'accepted') loadAllTracking();
    });
  }

  function init() {
    var choice = readConsent();
    if (choice === 'accepted') {
      loadAllTracking();
      return;
    }
    if (choice === 'rejected') {
      return;
    }
    if (document.body) {
      showBanner();
    } else {
      document.addEventListener('DOMContentLoaded', showBanner);
    }
  }

  window.ybCookieConsent = {
    getChoice: readConsent,
    hasAccepted: function () {
      return readConsent() === 'accepted';
    },
    loadTracking: loadAllTracking,
  };

  init();
})();
