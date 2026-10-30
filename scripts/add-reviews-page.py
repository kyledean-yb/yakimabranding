#!/usr/bin/env python3
"""Build /reviews: every client review we have on file."""

from __future__ import annotations

import importlib.util
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from schema_markup import SITE, breadcrumb, global_schemas, render_schema_head, webpage_schema
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_footer_snippet import site_footer_html
from site_nav_snippet import site_header_html
from site_tracking_snippet import ATTRIBUTER_FOOTER_BLOCK, GTM_BODY_NOSCRIPT_BLOCK, TRACKING_HEAD_BLOCK

_spec = importlib.util.spec_from_file_location("seo_sub", ROOT / "scripts" / "add-seo-subpages.py")
_seo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_seo)
BASE_CSS = _seo.BASE_CSS
ARROW = _seo.ARROW

YELP_URL = "https://www.yelp.com/search?find_desc=YB.+Marketing&find_loc=Yakima%2C+WA"
YELP_STARS = "".join('<span class="yelp-star"><svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><polygon points="12 3 14.8 8.9 21 9.6 16.4 13.8 17.7 20 12 16.8 6.3 20 7.6 13.8 3 9.6 9.2 8.9"/></svg></span>' for _ in range(5))
GOOGLE_REVIEWS_URL = "https://www.google.com/search?q=yakima+branding#lrd=0x808fcc994b2e85bd:0xf6698f50d2169f4d,1,,,,"

# (name, review). Reviews ending in "…" are excerpts.
REVIEWS = [
    ("Josh DeBoer", "Yakima Branding is an excellent choice for all of your SEO, marketing, branding, logos, websites and more. I have had the pleasure of working with Jacob Ross at Yakima Branding. He is extremely knowledgeable and easy to work with to tailor your marketing needs whether you're geo-farming or using SEO, Jacob is wonderful to work with. I highly recommend Yakima Branding and Jacob Ross!"),
    ("Heather Hellums", "Yakima Branding's team is professional, creative, accommodating and very patient! We made several changes, pivoted on our initial concept, and they stayed with us every step of the way. We are very happy with our website, we look forward to engaging them for SEO and targeted marketing in the future."),
    ("Kitt Murry", "Jacob is knowledgeable, professional and extremely accommodating to our needs. Has helped us build our new site and we were so satisfied we're discussing how to utilize his team for additional services they provide starting with SEO."),
    ("Chris Hutchens", "Yakima Branding built us a website and we also use them for our marketing. They are easy to work with and very helpful. If you're looking for a website, marketing or both I would highly recommend Yakima Branding!"),
    ("The Healthy Worker", "Worked with Jacob and his team and had a great experience building a new website! They were professional and easy to work with through the whole process."),
    ("Mike Nielsen", "Yakima Branding worked with me to create a business logo, they were helpful, informative and friendly from the beginning to the end. I'd highly recommend them for any needs you might have."),
    ("Heather Underwood", "Very easy to deal with. Been using them for a few years now. Always helpful and share my cost concerns for this type of service, very reasonable."),
    ("Apex Dentures", "Great company to work with. I've completed two big projects and the business has been leaping up the Google results page with organic searches. …"),
    ("Law Office", "Yakima Branding designed my website, hosts it and maintains the SEO. They are good at targeting the right clients for my business. …"),
    ("Luis Fernandez", "This company has been awesome. Jacob answered all my questions and did an awesome job with the website. …"),
    ("JLS Custom Construction", "Yakima Branding was instrumental in the successful launch of my business and brand. …"),
    ("Groundwork Systems", "Had a great experience working with Jacob. He and his team guided us through developing a logo and initial branding. …"),
    ("Doug Turner", "Jacob and Kyle came through on time when I needed a website rebuild with a tight deadline. …"),
    ("Emily Schwab", "Jacob and his team were awesome to work with in designing my law firm's website. …"),
    ("PMI Supplies", "Great group to work with. Very knowledgeable and friendly."),
]

AVATAR_BGS = ["var(--grad-brand)", "var(--grad-sunset)", "linear-gradient(135deg,#7c5cff,#2bc4f0)", "linear-gradient(135deg,#16b38a,#2bc4f0)", "linear-gradient(135deg,#f5a524,#ff6b6b)"]

STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
GOOGLE_G = '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'

PAGE_CSS = """
.rv-hero{position:relative;overflow:hidden;background:var(--grad-navy);padding:96px 0 110px;text-align:center}
.rv-hero::before{content:'';position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.8;pointer-events:none}
.rv-hero .container{position:relative;z-index:1}
.rv-hero h1{color:#fff;font-size:clamp(2.4rem,4.4vw,3.6rem);line-height:1.08;margin:16px auto 18px;max-width:760px}
.rv-hero h1 span{background:var(--grad-brand);-webkit-background-clip:text;background-clip:text;color:transparent}
.rv-hero p{color:var(--fg2-on-dark);font-size:17px;line-height:1.7;max-width:600px;margin:0 auto 30px}
.rv-score{display:inline-flex;align-items:center;gap:16px;padding:14px 24px;border-radius:var(--r-pill);background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);margin-bottom:30px}
.rv-score-num{font-family:var(--font-display);font-weight:800;font-size:34px;color:#fff;line-height:1}
.rv-score-stars{display:flex;gap:3px;color:var(--yb-amber)}
.rv-score-stars svg{width:20px;height:20px}
.rv-score-meta{display:flex;flex-direction:column;align-items:flex-start;gap:4px}
.rv-score-label{display:inline-flex;align-items:center;gap:6px;color:var(--fg2-on-dark);font-size:13px;font-weight:600}
.rv-score-label svg{width:16px;height:16px}
.rv-scores{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-bottom:30px}
.rv-scores .rv-score{margin-bottom:0;text-decoration:none;transition:background .2s ease}
.rv-scores .rv-score:hover{background:rgba(255,255,255,.14)}
.yelp-stars{gap:3px}
.yelp-star{width:20px;height:20px;border-radius:3px;background:#FF1A1A;display:flex;align-items:center;justify-content:center}
.yelp-star svg{width:14px;height:14px}
.yelp-word{font-family:var(--font-display);font-weight:800;font-size:15px;color:#FF1A1A;letter-spacing:-.02em}
.rv-hero-actions{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.rv-grid{columns:3 320px;column-gap:22px}
.rv-card{break-inside:avoid;margin:0 0 22px;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:26px 26px 22px;box-shadow:var(--sh-sm);transition:transform .25s ease,box-shadow .25s ease}
.rv-card:hover{transform:translateY(-3px);box-shadow:var(--sh-md)}
.rv-card-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.rv-stars{display:flex;gap:2px;color:var(--yb-amber)}
.rv-stars svg{width:16px;height:16px}
.rv-g{width:20px;height:20px}
.rv-g svg{width:20px;height:20px;display:block}
.rv-text{margin:0 0 20px;font-size:15.5px;line-height:1.65;color:var(--ink)}
.rv-card--lead .rv-text{font-size:17px}
.rv-author{display:flex;align-items:center;gap:12px;padding-top:16px;border-top:1px solid var(--line)}
.rv-avatar{width:40px;height:40px;border-radius:50%;color:#fff;display:flex;align-items:center;justify-content:center;font-family:var(--font-display);font-weight:700;font-size:13px;flex:none}
.rv-name{display:block;font-weight:700;font-size:14.5px;color:var(--ink)}
.rv-source{display:block;font-size:12.5px;color:var(--fg3);font-weight:600}
.rv-more{text-align:center;margin-top:20px}
.rv-cta{position:relative;overflow:hidden;background:var(--grad-navy);padding:80px 0;text-align:center}
.rv-cta::before{content:'';position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.7;pointer-events:none}
.rv-cta .container{position:relative;z-index:1}
.rv-cta h2{color:#fff;margin:14px 0 14px}
.rv-cta p{color:var(--fg2-on-dark);font-size:16px;max-width:560px;margin:0 auto 28px}
@media(max-width:640px){.rv-score{flex-direction:column;gap:10px;border-radius:var(--r-lg)}.rv-score-meta{align-items:center}}
"""


T = {
    "en": dict(
        title="Client Reviews | YB Marketing | 509-901-9735",
        meta="Read what clients say about working with YB Marketing (Yakima Branding). 5.0 stars across 48 Google reviews for web design, SEO, branding, and marketing.",
        home="Home", about="About", crumb="Reviews",
        eyebrow="Client Reviews", h1a="Don't Take Our Word for It.", h1b="Take Our Clients'.",
        lead="These are reviews from the business owners we work with every day, pulled from our Google Business Profile.",
        stars="5 out of 5 stars", count="48 Google reviews", source="Google review", yelp="5 star rating",
        work="Work With Us", google="See Us on Google", all="Read All 48 Reviews on Google",
        cta_eyebrow="Your Turn", cta_h2="Ready to see what we can do for your business?",
        cta_p="Book a free 30 minute intro call. We'll talk through your goals and where we'd start.",
        cta_btn="Get Started Today",
    ),
    "es": dict(
        title="Reseñas de clientes | YB Marketing | 509-901-9735",
        meta="Lea lo que dicen los clientes sobre trabajar con YB Marketing (Yakima Branding). 5.0 estrellas en 48 reseñas de Google sobre diseño web, SEO, marca y marketing.",
        home="Inicio", about="Nosotros", crumb="Reseñas",
        eyebrow="Reseñas de clientes", h1a="No lo decimos nosotros.", h1b="Lo dicen nuestros clientes.",
        lead="Estas son reseñas de los dueños de negocios con los que trabajamos todos los días, tomadas de nuestro perfil de Google. Las reseñas se muestran en su idioma original.",
        stars="5 de 5 estrellas", count="48 reseñas en Google", source="Reseña de Google", yelp="5 estrellas",
        work="Trabaje con nosotros", google="Véanos en Google", all="Lea las 48 reseñas en Google",
        cta_eyebrow="Su turno", cta_h2="¿Listo para ver lo que podemos hacer por su negocio?",
        cta_p="Reserve una llamada introductoria gratuita de 30 minutos. Hablaremos de sus metas y de por dónde empezaríamos.",
        cta_btn="Comience hoy",
    ),
}


def initials(name: str) -> str:
    words = [w for w in name.replace("'", "").split() if w[0].isalpha()]
    return (words[0][0] + (words[1][0] if len(words) > 1 else "")).upper()


def card(i: int, name: str, text: str, lang: str = "en") -> str:
    stars = STAR * 5
    lead = " rv-card--lead" if i < 3 else ""
    return (
        f'      <article class="rv-card{lead}">\n'
        f'        <div class="rv-card-top"><div class="rv-stars" aria-label="{T[lang]["stars"]}">{stars}</div><span class="rv-g" title="{T[lang]["source"]}">{GOOGLE_G}</span></div>\n'
        f'        <p class="rv-text">"{escape(text, quote=False)}"</p>\n'
        f'        <div class="rv-author"><div class="rv-avatar" style="background:{AVATAR_BGS[i % len(AVATAR_BGS)]}">{initials(name)}</div>'
        f'<div><span class="rv-name">{escape(name)}</span><span class="rv-source">{T[lang]["source"]}</span></div></div>\n'
        f"      </article>"
    )


def build(lang: str = "en") -> str:
    L = T[lang]
    pre = "/es" if lang == "es" else ""
    url = f"{SITE}{pre}/reviews"
    title = L["title"]
    meta = L["meta"]
    header = site_header_html("/", lang=lang, current_path="/reviews").strip()
    footer = site_footer_html("/", lang=lang, current_path="/reviews").strip()
    schemas = global_schemas() + [
        breadcrumb([(1, L["home"], f"{SITE}{pre}/"), (2, L["about"], f"{SITE}{pre}/about"), (3, L["crumb"], url)]),
        webpage_schema(title, url, meta),
    ]
    cards = "\n".join(card(i, n, t, lang) for i, (n, t) in enumerate(REVIEWS))
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/favicon.png" type="image/png">
<title>{escape(title, quote=False)}</title>
<meta name="description" content="{escape(meta)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE}/reviews">
<link rel="alternate" hreflang="es" href="{SITE}/es/reviews">
<link rel="alternate" hreflang="x-default" href="{SITE}/reviews">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Yakima Branding">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(meta)}">
<link rel="stylesheet" href="/colors_and_type.css">
<style>{BASE_CSS}{PAGE_CSS}</style>
<link rel="stylesheet" href="/site.css">
{render_schema_head(schemas)}
{TRACKING_HEAD_BLOCK}
</head>
<body>
{GTM_BODY_NOSCRIPT_BLOCK}
{ACCESSIBE_BODY_SCRIPT}
{header}

<section class="rv-hero">
  <div class="container">
    <span class="eyebrow" style="color:var(--yb-cyan)">{L["eyebrow"]}</span>
    <h1>{L["h1a"]} <span>{L["h1b"]}</span></h1>
    <p>{L["lead"]}</p>
    <div class="rv-scores">
      <a class="rv-score" href="{GOOGLE_REVIEWS_URL}" target="_blank" rel="noopener">
        <span class="rv-score-num">5.0</span>
        <div class="rv-score-meta">
          <div class="rv-score-stars" aria-label="{L["stars"]}">{STAR * 5}</div>
          <span class="rv-score-label">{GOOGLE_G} {L["count"]}</span>
        </div>
      </a>
      <a class="rv-score" href="{YELP_URL}" target="_blank" rel="noopener">
        <span class="rv-score-num">5.0</span>
        <div class="rv-score-meta">
          <div class="rv-score-stars yelp-stars" aria-label="{L["stars"]}">{YELP_STARS}</div>
          <span class="rv-score-label"><span class="yelp-word">yelp</span> {L["yelp"]}</span>
        </div>
      </a>
    </div>
    <div class="rv-hero-actions">
      <a href="{pre}/contact" class="btn btn-grad btn-lg">{L["work"]} {ARROW}</a>
      <a href="{GOOGLE_REVIEWS_URL}" class="btn btn-ghost-white btn-lg" target="_blank" rel="noopener">{L["google"]}</a>
    </div>
  </div>
</section>
<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>

<section style="background:var(--bg-soft);padding-top:56px">
  <div class="container">
    <div class="rv-grid">
{cards}
    </div>
    <div class="rv-more"><a class="btn btn-ghost" href="{GOOGLE_REVIEWS_URL}" target="_blank" rel="noopener">{L["all"]}</a></div>
  </div>
</section>

<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>
<section class="rv-cta">
  <div class="container">
    <span class="eyebrow" style="color:var(--yb-cyan)">{L["cta_eyebrow"]}</span>
    <h2>{L["cta_h2"]}</h2>
    <p>{L["cta_p"]}</p>
    <div class="svc-cta-btns" style="justify-content:center">
      <a href="{pre}/contact" class="btn btn-grad btn-lg">{L["cta_btn"]} {ARROW}</a>
      <a href="tel:5099019735" class="btn btn-ghost-white btn-lg">509-901-9735</a>
    </div>
  </div>
</section>

{footer}

<script src="/js/newsletter-popup.js" defer></script>
<script src="/js/chat-widget.js" defer></script>
<script src="/js/site.js?v=2" defer></script>
<script>
document.getElementById('hamburger')?.addEventListener('click', function () {{
  document.getElementById('mobileMenu')?.classList.toggle('open');
}});
</script>
{ATTRIBUTER_FOOTER_BLOCK}
</body>
</html>
"""


def main() -> None:
    for lang, out in (("en", ROOT / "reviews.html"), ("es", ROOT / "es" / "reviews.html")):
        out.write_text(build(lang), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
