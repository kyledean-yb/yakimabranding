/**
 * Theme Advice Local visibility widget to match YB Marketing design system.
 * Widget uses shadow DOM; styles are injected after mount.
 */
(function () {
  var SELECTOR = '.visibility-widget-wrap widget-app';
  var STYLE_ID = 'yb-visibility-theme';

  var THEME_CSS = [
    '.static-position {',
    '  --font-family: "Plus Jakarta Sans", system-ui, sans-serif !important;',
    '  --primary-color: #3F6FD6 !important;',
    '  --primary-text-color: #ffffff !important;',
    '  --header-color: #3F6FD6 !important;',
    '  --body-text-color: #4A5673 !important;',
    '  --focus-ring: #2BC4F0 !important;',
    '}',
    '.open-container {',
    '  background: #ffffff !important;',
    '  background-image: none !important;',
    '}',
    '.header-static, .open-container > div:first-child {',
    '  background: linear-gradient(135deg, #3F6FD6 0%, #2BC4F0 100%) !important;',
    '  color: #ffffff !important;',
    '}',
    '.header-static p, .open-container p {',
    '  font-family: var(--font-family) !important;',
    '}',
    'input, select, textarea {',
    '  font-family: var(--font-family) !important;',
    '  border-radius: 10px !important;',
    '  border-color: #CFD8E8 !important;',
    '  color: #16203A !important;',
    '}',
    'input::placeholder, textarea::placeholder {',
    '  color: #7C879E !important;',
    '}',
    'button, [type="submit"], .btn, .button {',
    '  font-family: var(--font-family) !important;',
    '  font-weight: 700 !important;',
    '  border-radius: 10px !important;',
    '  background: linear-gradient(135deg, #3F6FD6 0%, #2BC4F0 100%) !important;',
    '  color: #ffffff !important;',
    '  border: none !important;',
    '  box-shadow: 0 14px 30px -10px rgba(63, 111, 214, 0.4) !important;',
    '}',
    'h2, h3, h4, strong {',
    '  font-family: "Sora", system-ui, sans-serif !important;',
    '  color: #16203A !important;',
    '}'
  ].join('\n');

  function injectTheme(app) {
    if (!app || !app.shadowRoot) return false;
    if (app.shadowRoot.getElementById(STYLE_ID)) return true;

    var style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = THEME_CSS;
    app.shadowRoot.appendChild(style);

    var wrap = app.closest('.visibility-widget-wrap');
    if (wrap) wrap.classList.add('is-ready');
    return true;
  }

  function poll() {
    var app = document.querySelector(SELECTOR);
    if (injectTheme(app)) return;
  }

  function init() {
    var wrap = document.querySelector('.visibility-widget-wrap');
    if (!wrap) return;

    poll();
    var tries = 0;
    var interval = setInterval(function () {
      poll();
      tries += 1;
      if (tries > 40) clearInterval(interval);
    }, 250);

    var observer = new MutationObserver(poll);
    observer.observe(wrap, { childList: true, subtree: true });
    setTimeout(function () {
      observer.disconnect();
      clearInterval(interval);
    }, 12000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
