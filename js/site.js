/**
 * YB Marketing — shared nav dropdown + scroll reveal animations
 */
(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initNavDropdown() {
    document.querySelectorAll('.nav-services, .nav-about').forEach(function (nav) {
      var btn = nav.querySelector('.nav-svc-btn');
      var closeTimer;

      function open() {
        clearTimeout(closeTimer);
        nav.classList.add('is-open');
      }

      function scheduleClose() {
        closeTimer = setTimeout(function () {
          nav.classList.remove('is-open');
        }, 160);
      }

      nav.addEventListener('mouseenter', open);
      nav.addEventListener('mouseleave', scheduleClose);
      nav.addEventListener('focusin', open);
      nav.addEventListener('focusout', function (e) {
        if (!nav.contains(e.relatedTarget)) scheduleClose();
      });

      if (btn) {
        btn.addEventListener('click', function (e) {
          if (window.matchMedia('(max-width: 900px)').matches) return;
          e.preventDefault();
          nav.classList.toggle('is-open');
        });
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        document.querySelectorAll('.nav-services.is-open, .nav-about.is-open').forEach(function (n) {
          n.classList.remove('is-open');
        });
      }
    });

    document.addEventListener('click', function (e) {
      if (!e.target.closest('.nav-services') && !e.target.closest('.nav-about')) {
        document.querySelectorAll('.nav-services.is-open, .nav-about.is-open').forEach(function (n) {
          n.classList.remove('is-open');
        });
      }
    });
  }

  function initHeaderScroll() {
    var hdr = document.getElementById('header');
    if (!hdr) return;

    function update() {
      var scrolled = window.scrollY > 20;
      hdr.classList.toggle('solid', scrolled);
      hdr.classList.toggle('top', !scrolled);
    }

    update();
    window.addEventListener('scroll', update, { passive: true });
  }

  function markHeroEntrance() {
    if (prefersReducedMotion) return;

    document.querySelectorAll('.hero .eyebrow, .svc-hero .eyebrow, .blog-hero .eyebrow').forEach(function (el) {
      el.classList.add('hero-reveal');
    });
    document.querySelectorAll('.hero h1, .svc-hero h1, .blog-hero h1').forEach(function (el) {
      el.classList.add('hero-reveal', 'hero-reveal-d1');
    });
    document.querySelectorAll(
      '.hero .hero-lead, .svc-hero .hero-lead, .hero p.hero-lead, .blog-hero p'
    ).forEach(function (el) {
      el.classList.add('hero-reveal', 'hero-reveal-d2');
    });
    document.querySelectorAll('.hero-actions, .svc-hero-actions').forEach(function (el) {
      el.classList.add('hero-reveal', 'hero-reveal-d3');
    });
    document.querySelectorAll('.hero-visual, .svc-hero-visual').forEach(function (el) {
      el.classList.add('hero-reveal', 'hero-reveal-d4');
    });
  }

  function applyRevealClasses() {
    if (prefersReducedMotion) return;

    document.querySelectorAll('section').forEach(function (section) {
      if (
        section.classList.contains('hero') ||
        section.classList.contains('svc-hero') ||
        section.classList.contains('blog-hero')
      ) {
        return;
      }

      var container = section.querySelector(':scope > .container');
      if (!container) return;

      var intro = container.querySelector(':scope > div:first-child');
      if (intro && intro.querySelector('.eyebrow, h2, h1')) {
        if (!intro.classList.contains('reveal-fade')) intro.classList.add('reveal-fade');
        intro.querySelectorAll('.eyebrow').forEach(function (el) {
          if (!el.classList.contains('reveal-text')) el.classList.add('reveal-text');
        });
        intro.querySelectorAll('h2, h1').forEach(function (el) {
          if (!el.classList.contains('reveal-text')) el.classList.add('reveal-text');
        });
        intro.querySelectorAll('p').forEach(function (el, i) {
          if (i === 0 && !el.classList.contains('reveal-text')) el.classList.add('reveal-text');
        });
      }
    });

    document.querySelectorAll('.sec-header').forEach(function (el) {
      el.classList.add('reveal-fade');
      el.querySelectorAll('.eyebrow, h2, h3').forEach(function (t) {
        t.classList.add('reveal-text');
      });
    });

    var staggerSelectors = [
      '.feat-grid',
      '.svc-grid',
      '.blog-grid',
      '.blog-card-grid',
      '.reviews-grid',
      '.contact-cards',
      '.why-tiles-grid',
      '.meet-grid',
      '.why-grid',
    ];

    staggerSelectors.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (grid) {
        if (!grid.classList.contains('reveal-stagger')) grid.classList.add('reveal-stagger');
      });
    });

    document.querySelectorAll(
      '.feat-card, .svc-card, .blog-card, .contact-card, .rv-card, .rv-scroll-card, .why-item, .faq-item'
    ).forEach(function (el) {
      if (!el.closest('.reveal-stagger')) el.classList.add('reveal');
    });

    document.querySelectorAll('.why-main-grid > div:first-child').forEach(function (el) {
      el.classList.add('reveal');
      el.querySelectorAll('.eyebrow, h2, h3, p').forEach(function (t) {
        t.classList.add('reveal-text');
      });
    });
  }

  function revealInViewport(observer) {
    var vh = window.innerHeight || document.documentElement.clientHeight;
    document.querySelectorAll('.reveal, .reveal-text, .reveal-fade, .reveal-stagger').forEach(function (el) {
      if (el.classList.contains('is-visible')) return;
      var rect = el.getBoundingClientRect();
      if (rect.top < vh * 0.92 && rect.bottom > 0) {
        el.classList.add('is-visible');
        observer.unobserve(el);
      }
    });
  }

  var scrollRevealObserver;

  function initScrollReveal() {
    if (prefersReducedMotion) return;

    markHeroEntrance();
    applyRevealClasses();

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -4% 0px' }
    );

    scrollRevealObserver = observer;

    document.querySelectorAll('.reveal, .reveal-text, .reveal-fade, .reveal-stagger').forEach(function (el) {
      observer.observe(el);
    });

    revealInViewport(observer);
    window.addEventListener('load', function () {
      revealInViewport(observer);
    });
    window.addEventListener(
      'resize',
      function () {
        revealInViewport(observer);
      },
      { passive: true }
    );
  }

  window.ybRefreshScrollReveal = function () {
    if (prefersReducedMotion || !scrollRevealObserver) return;
    applyRevealClasses();
    document.querySelectorAll('.reveal, .reveal-text, .reveal-fade, .reveal-stagger').forEach(function (el) {
      scrollRevealObserver.observe(el);
    });
    revealInViewport(scrollRevealObserver);
  };

  function init() {
    initNavDropdown();
    initHeaderScroll();
    initScrollReveal();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
