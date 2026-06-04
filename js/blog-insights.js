/**
 * Renders homepage insights + service-page related articles from blog/data/posts.json
 */
(function () {
  'use strict';

  var READ_SVG =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>';
  var ARROW_SVG =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>';
  var IMG_PLACEHOLDER =
    '<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>';

  var TOPIC_THEME = {
    seo: { color: 'var(--yb-cyan)', hex: '#2BC4F0', grad: 'linear-gradient(135deg,#2bc4f0,#3f6fd6)' },
    'google-ads': { color: 'var(--yb-coral)', hex: '#FF6B57', grad: 'linear-gradient(135deg,#ff6b57,#ff9478)' },
    'social-media': { color: 'var(--yb-amber)', hex: '#c77f12', grad: 'linear-gradient(135deg,#e8a020,#c77f12)' },
    'web-design': { color: 'var(--yb-mint)', hex: '#159468', grad: 'linear-gradient(135deg,#2dd4a0,#159468)' },
    content: { color: 'var(--yb-violet)', hex: '#7B5BE6', grad: 'linear-gradient(135deg,#7b5be6,#3f6fd6)' },
    strategy: { color: 'var(--yb-blue)', hex: '#3F6FD6', grad: 'linear-gradient(135deg,#3f6fd6,#22314f)' },
    news: { color: 'var(--yb-blue)', hex: '#3F6FD6', grad: 'linear-gradient(135deg,#3f6fd6,#22314f)' },
    general: { color: 'var(--yb-violet)', hex: '#7B5BE6', grad: 'linear-gradient(135deg,#7b5be6,#3f6fd6)' },
  };

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function truncate(str, max) {
    var s = String(str || '').replace(/\s+/g, ' ').trim();
    if (s.length <= max) return s;
    return s.slice(0, max).replace(/\s+\S*$/, '') + '…';
  }

  function themeFor(topic) {
    return TOPIC_THEME[topic] || TOPIC_THEME.general;
  }

  function pickPosts(posts, topicAttr, count) {
    var topics = topicAttr
      ? topicAttr
          .split(',')
          .map(function (t) {
            return t.trim();
          })
          .filter(Boolean)
      : [];
    var picked = [];
    var seen = {};

    if (topics.length) {
      posts.forEach(function (p) {
        if (topics.indexOf(p.topic) !== -1 && picked.length < count) {
          picked.push(p);
          seen[p.slug] = true;
        }
      });
    }

    posts.forEach(function (p) {
      if (picked.length >= count) return;
      if (!seen[p.slug]) {
        picked.push(p);
        seen[p.slug] = true;
      }
    });

    return picked.slice(0, count);
  }

  function postHref(base, slug) {
    return base + 'blog/posts/' + slug + '.html';
  }

  function renderHomeCard(post, index, base) {
    var featured = index === 0;
    var theme = themeFor(post.topic);
    var href = postHref(base, post.slug);
    var thumbClass = featured ? 'blog-thumb blog-thumb-lg' : 'blog-thumb blog-thumb-sm';
    var bodyClass = featured ? 'blog-body blog-body-lg' : 'blog-body';
    var titleSize = featured ? '22px' : '18px';
    var thumbInner = post.image
      ? '<img src="' +
        escapeHtml(post.image) +
        '" alt="' +
        escapeHtml(post.title) +
        '" loading="lazy" style="width:100%;height:100%;object-fit:cover;position:absolute;inset:0">'
      : IMG_PLACEHOLDER;
    var thumbStyle = post.image ? '' : ' style="background:' + theme.grad + '"';

    return (
      '<a href="' +
      escapeHtml(href) +
      '" class="blog-card">' +
      '<div class="' +
      thumbClass +
      '"' +
      thumbStyle +
      '>' +
      thumbInner +
      '<span class="blog-cat" style="color:' +
      theme.color +
      '">' +
      escapeHtml(post.topicLabel) +
      '</span></div>' +
      '<div class="' +
      bodyClass +
      '">' +
      '<h3 class="yb-h3" style="font-size:' +
      titleSize +
      '">' +
      escapeHtml(post.title) +
      '</h3>' +
      '<p>' +
      escapeHtml(truncate(post.excerpt, featured ? 200 : 120)) +
      '</p>' +
      '<div class="blog-meta">' +
      '<span class="blog-read">' +
      READ_SVG +
      post.readingTime +
      ' min read</span>' +
      '<span class="blog-more" style="color:' +
      theme.color +
      '">Read More ' +
      ARROW_SVG +
      '</span></div></div></a>'
    );
  }

  function renderRelatedCard(post, accent, base) {
    var theme = themeFor(post.topic);
    var badgeColor = accent || theme.hex;
    var href = postHref(base, post.slug);
    var thumbInner = post.image
      ? '<img src="' +
        escapeHtml(post.image) +
        '" alt="' +
        escapeHtml(post.title) +
        '" loading="lazy">'
      : '<div style="position:absolute;inset:0;background:' +
        theme.grad +
        '"></div>' +
        IMG_PLACEHOLDER;

    return (
      '<a href="' +
      escapeHtml(href) +
      '" class="insights-card">' +
      '<div class="insights-card-thumb">' +
      thumbInner +
      '<span class="insights-card-badge" style="background:' +
      escapeHtml(badgeColor) +
      '">' +
      escapeHtml(post.topicLabel) +
      '</span></div>' +
      '<div class="insights-card-body">' +
      '<h3>' +
      escapeHtml(post.title) +
      '</h3>' +
      '<p>' +
      escapeHtml(truncate(post.excerpt, 130)) +
      '</p>' +
      '<span class="insights-card-more" style="color:' +
      escapeHtml(badgeColor) +
      '">Read More ' +
      ARROW_SVG +
      '</span></div></a>'
    );
  }

  function renderGrid(el, posts) {
    var base = el.getAttribute('data-base') || '';
    var topic = el.getAttribute('data-topic') || '';
    var variant = el.getAttribute('data-variant') || 'related';
    var count = parseInt(el.getAttribute('data-count') || '3', 10);
    var accent = el.getAttribute('data-accent') || '';
    var picked = pickPosts(posts, topic, count);

    if (!picked.length) {
      el.innerHTML =
        '<p class="insights-loading">No articles available yet. <a href="' +
        escapeHtml(base + 'insights.html') +
        '">View all insights</a>.</p>';
      return;
    }

    el.innerHTML =
      variant === 'home'
        ? picked.map(function (p, i) {
            return renderHomeCard(p, i, base);
          }).join('')
        : picked
            .map(function (p) {
              return renderRelatedCard(p, accent, base);
            })
            .join('');

    if (typeof window.ybRefreshScrollReveal === 'function') {
      window.ybRefreshScrollReveal();
    }
  }

  function init() {
    var grids = document.querySelectorAll('[data-blog-insights]');
    if (!grids.length) return;

    var base = grids[0].getAttribute('data-base') || '';
    grids.forEach(function (el) {
      el.innerHTML = '<p class="insights-loading">Loading articles…</p>';
    });

    fetch(base + 'blog/data/posts.json')
      .then(function (res) {
        if (!res.ok) throw new Error('posts.json ' + res.status);
        return res.json();
      })
      .then(function (posts) {
        grids.forEach(function (el) {
          renderGrid(el, posts);
        });
      })
      .catch(function () {
        grids.forEach(function (el) {
          el.innerHTML =
            '<p class="insights-loading">Unable to load articles. <a href="' +
            escapeHtml((el.getAttribute('data-base') || '') + 'insights.html') +
            '">View all insights</a>.</p>';
        });
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
