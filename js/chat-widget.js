/**
 * YB Marketing — floating chat widget (bottom-left)
 *
 * Add your API key later via window.YB_CHAT_CONFIG before this script loads:
 *
 *   window.YB_CHAT_CONFIG = {
 *     apiKey: 'your-api-key',
 *     apiEndpoint: 'https://your-provider.example.com/chat' // optional
 *   };
 */
(function () {
  'use strict';

  var DEFAULT_CONFIG = {
    apiKey: '',
    apiEndpoint: '',
    phone: '5099019735',
    phoneDisplay: '509-901-9735',
    email: 'info@yakimabranding.com',
    scheduleUrl: 'https://calendly.com/yakimabranding',
    officeHours: 'Office hours: 9am–5pm PST',
    welcomeMessage:
      "Hi! I'm here to help you learn more about YB Marketing. How can I assist you today?",
    offlineReply:
      'Thanks for your message! A team member will follow up soon. You can also call us or book a time using the buttons below.'
  };

  var ICONS = {
    chat:
      '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    bot:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="8" width="18" height="12" rx="2"/><path d="M12 8V5"/><circle cx="8.5" cy="14" r="1"/><circle cx="15.5" cy="14" r="1"/><path d="M9 5h6"/></svg>',
    phone:
      '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    mail:
      '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    calendar:
      '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    send:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>',
    close:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>'
  };

  function getConfig() {
    var user = window.YB_CHAT_CONFIG || {};
    var cfg = {};
    var key;
    for (key in DEFAULT_CONFIG) {
      if (Object.prototype.hasOwnProperty.call(DEFAULT_CONFIG, key)) {
        cfg[key] = user[key] !== undefined ? user[key] : DEFAULT_CONFIG[key];
      }
    }
    return cfg;
  }

  function buildWidget(cfg) {
    var root = document.createElement('div');
    root.id = 'yb-chat-widget';
    root.className = 'yb-chat-widget';
    root.innerHTML =
      '<button type="button" class="yb-chat-widget__launcher" aria-label="Open chat" aria-expanded="false" aria-controls="yb-chat-panel">' +
      ICONS.chat +
      '</button>';

    var panel = document.createElement('section');
    panel.id = 'yb-chat-panel';
    panel.className = 'yb-chat-widget__panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'true');
    panel.setAttribute('aria-labelledby', 'yb-chat-title');
    panel.setAttribute('aria-hidden', 'true');
    panel.hidden = true;
    panel.innerHTML =
      '<header class="yb-chat-widget__head">' +
      '  <div class="yb-chat-widget__brand">' +
      '    <span class="yb-chat-widget__avatar" aria-hidden="true">' + ICONS.bot + '</span>' +
      '    <div>' +
      '      <div id="yb-chat-title" class="yb-chat-widget__title">YB Marketing</div>' +
      '      <div class="yb-chat-widget__status"><span class="yb-chat-widget__status-dot" aria-hidden="true"></span>Online now</div>' +
      '      <div class="yb-chat-widget__hours">' + escapeHtml(cfg.officeHours) + '</div>' +
      '    </div>' +
      '  </div>' +
      '  <button type="button" class="yb-chat-widget__close" aria-label="Close chat">' + ICONS.close + '</button>' +
      '</header>' +
      '<div class="yb-chat-widget__messages" role="log" aria-live="polite" aria-relevant="additions"></div>' +
      '<form class="yb-chat-widget__composer" action="#" method="post">' +
      '  <label class="yb-chat-widget__composer-label" for="yb-chat-input">Type your message</label>' +
      '  <input id="yb-chat-input" class="yb-chat-widget__input" type="text" name="message" autocomplete="off" placeholder="Type your message..." maxlength="2000">' +
      '  <button type="submit" class="yb-chat-widget__send" aria-label="Send message">' + ICONS.send + '</button>' +
      '</form>' +
      '<div class="yb-chat-widget__foot">' +
      '  <div class="yb-chat-widget__ctas">' +
      '    <a class="yb-chat-widget__cta yb-chat-widget__cta--call" href="tel:' + cfg.phone + '">' + ICONS.phone + '<span>Call Us</span></a>' +
      '    <a class="yb-chat-widget__cta yb-chat-widget__cta--email" href="mailto:' + cfg.email + '">' + ICONS.mail + '<span>Email Us</span></a>' +
      '    <a class="yb-chat-widget__cta yb-chat-widget__cta--schedule" href="' + cfg.scheduleUrl + '" target="_blank" rel="noopener noreferrer">' + ICONS.calendar + '<span>Schedule Call</span></a>' +
      '  </div>' +
      '</div>';

    document.body.appendChild(root);
    document.body.appendChild(panel);

    return { root: root, panel: panel };
  }

  function appendMessage(messagesEl, text, role) {
    var row = document.createElement('div');
    row.className = 'yb-chat-widget__msg yb-chat-widget__msg--' + role;

    if (role === 'bot') {
      row.innerHTML =
        '<span class="yb-chat-widget__msg-avatar" aria-hidden="true">' + ICONS.bot + '</span>' +
        '<div class="yb-chat-widget__bubble">' + escapeHtml(text) + '</div>';
    } else {
      row.innerHTML = '<div class="yb-chat-widget__bubble">' + escapeHtml(text) + '</div>';
    }

    messagesEl.appendChild(row);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function showTyping(messagesEl) {
    var row = document.createElement('div');
    row.className = 'yb-chat-widget__msg yb-chat-widget__msg--bot yb-chat-widget__msg--typing';
    row.innerHTML =
      '<span class="yb-chat-widget__msg-avatar" aria-hidden="true">' + ICONS.bot + '</span>' +
      '<div class="yb-chat-widget__bubble yb-chat-widget__typing" aria-hidden="true"><span></span><span></span><span></span></div>';
    messagesEl.appendChild(row);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return row;
  }

  function sendToApi(cfg, text) {
    if (!cfg.apiKey) {
      return Promise.resolve(null);
    }

    var endpoint = cfg.apiEndpoint || '/api/chat';
    return fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + cfg.apiKey
      },
      body: JSON.stringify({ message: text })
    })
      .then(function (res) {
        if (!res.ok) throw new Error('Chat request failed');
        return res.json();
      })
      .then(function (data) {
        return (data && (data.reply || data.message || data.text)) || null;
      })
      .catch(function () {
        return null;
      });
  }

  function openPanel(root, panel, launcher) {
    panel.hidden = false;
    panel.setAttribute('aria-hidden', 'false');
    launcher.setAttribute('aria-expanded', 'true');
    root.classList.add('is-open');
    panel.classList.add('is-open');
    requestAnimationFrame(function () {
      panel.querySelector('#yb-chat-input').focus();
    });
  }

  function closePanel(root, panel, launcher) {
    panel.setAttribute('aria-hidden', 'true');
    launcher.setAttribute('aria-expanded', 'false');
    root.classList.remove('is-open');
    panel.classList.remove('is-open');
    setTimeout(function () {
      if (!panel.classList.contains('is-open')) panel.hidden = true;
    }, 280);
  }

  function init() {
    var cfg = getConfig();
    var widgets = buildWidget(cfg);
    var root = widgets.root;
    var panel = widgets.panel;
    var launcher = root.querySelector('.yb-chat-widget__launcher');
    var closeBtn = panel.querySelector('.yb-chat-widget__close');
    var form = panel.querySelector('.yb-chat-widget__composer');
    var input = panel.querySelector('#yb-chat-input');
    var messagesEl = panel.querySelector('.yb-chat-widget__messages');
    var welcomeShown = false;

    function ensureWelcome() {
      if (welcomeShown) return;
      welcomeShown = true;
      appendMessage(messagesEl, cfg.welcomeMessage, 'bot');
    }

    launcher.addEventListener('click', function () {
      if (panel.classList.contains('is-open')) {
        closePanel(root, panel, launcher);
      } else {
        ensureWelcome();
        openPanel(root, panel, launcher);
      }
    });

    closeBtn.addEventListener('click', function () {
      closePanel(root, panel, launcher);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('is-open')) {
        closePanel(root, panel, launcher);
      }
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var text = input.value.trim();
      if (!text) return;

      ensureWelcome();
      appendMessage(messagesEl, text, 'user');
      input.value = '';

      var typingEl = showTyping(messagesEl);

      sendToApi(cfg, text).then(function (reply) {
        if (typingEl.parentNode) typingEl.parentNode.removeChild(typingEl);
        appendMessage(messagesEl, reply || cfg.offlineReply, 'bot');
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
