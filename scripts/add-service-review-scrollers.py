#!/usr/bin/env python3
"""Insert a Google review scroller on service pages.

Services with matching reviews get it directly below the hero; the rest
(generic reviews) get it just above the FAQ.

Idempotent: replaces any existing block between the svc-reviews markers.
Re-run after regenerating service pages.
"""
from __future__ import annotations

import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from site_lead_form_snippet import lead_form_html
_src = (ROOT / "scripts" / "add-reviews-page.py").read_text(encoding="utf-8")
_ns: dict = {}
exec(_src[_src.index("REVIEWS = ["):_src.index("\n]\n", _src.index("REVIEWS = [")) + 3], _ns)
REVIEWS: dict[str, str] = dict(_ns["REVIEWS"])
for _line in _src.splitlines():
    if _line.startswith(("YELP_URL =", "YELP_STARS =", "GOOGLE_REVIEWS_URL =", "GOOGLE_G =")):
        exec(_line, _ns)
YELP_URL, YELP_STARS = _ns["YELP_URL"], _ns["YELP_STARS"]
GOOGLE_REVIEWS_URL, GOOGLE_G = _ns["GOOGLE_REVIEWS_URL"], _ns["GOOGLE_G"]

GROUPS = {
    "seo": ["Apex Dentures", "Law Office", "Josh DeBoer"],
    "web-design": ["Doug Turner", "The Healthy Worker", "Emily Schwab", "Heather Hellums", "Luis Fernandez",
                   "Kitt Murry", "Chris Hutchens", "Law Office"],
    "branding": ["Groundwork Systems", "Mike Nielsen", "JLS Custom Construction", "Josh DeBoer"],
    "generic": ["Josh DeBoer", "Heather Underwood", "Chris Hutchens", "Heather Hellums", "PMI Supplies",
                "Kitt Murry", "The Healthy Worker"],
}

SERVICE_DIRS = {
    "seo": "seo", "web-design": "web-design", "branding": "branding",
    "google-ads": "generic", "social-media": "generic", "content-marketing": "generic",
    "press-releases": "generic", "customer-growth": "generic",
    "ai-for-business": "generic", "ai-for-small-business": "generic",
}

COPY = {
    "en": {
        "eyebrow": "Client Reviews",
        "seo": "What clients say about our SEO work",
        "web-design": "What clients say about their new websites",
        "branding": "What clients say about their logos and branding",
        "generic": "What our clients say",
        "on": "on",
        "all": "Read all reviews",
        "href": "/reviews",
        "form_lead": "Tell us about your business and we'll talk through where we'd start.",
        "submit": "Send Message",
    },
    "es": {
        "eyebrow": "Reseñas de clientes",
        "seo": "Lo que dicen nuestros clientes sobre nuestro trabajo de SEO",
        "web-design": "Lo que dicen nuestros clientes sobre sus nuevos sitios web",
        "branding": "Lo que dicen nuestros clientes sobre sus logos y marca",
        "generic": "Lo que dicen nuestros clientes",
        "on": "en",
        "all": "Ver todas las reseñas",
        "href": "/es/reviews",
        "form_lead": "Cuéntenos sobre su negocio y hablaremos de por dónde empezaríamos.",
        "submit": "Enviar mensaje",
    },
}

AVATARS = ["var(--grad-brand)", "var(--grad-sunset)", "linear-gradient(135deg,#7c5cff,#2bc4f0)",
           "linear-gradient(135deg,#16b38a,#2bc4f0)", "linear-gradient(135deg,#f5a524,#ff6b6b)"]
STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
CHECK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'

CSS = """<style>
.svr{padding:56px 0 8px;overflow:hidden}
.svr-head{text-align:center;max-width:680px;margin:0 auto 36px;padding:0 20px}
.svr-head h2{margin:14px 0 16px;text-wrap:balance}
.svr-badge{display:inline-flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--line);border-radius:var(--r-pill);padding:8px 18px;box-shadow:var(--sh-xs);text-decoration:none}
.svr-badges{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.svr-gicon svg{width:16px;height:16px;display:block}
.svr-ystars{display:flex;gap:2px}
.svr-ystars .yelp-star{width:16px;height:16px;border-radius:3px;background:#FF1A1A;display:flex;align-items:center;justify-content:center}
.svr-ystars .yelp-star svg{width:11px;height:11px}
.svr-yelp{font-style:normal;font-weight:800;color:#D32323}
.svr-badge b{font-weight:800;font-size:16px;color:var(--ink)}
.svr-badge span{color:var(--fg3);font-size:13px;font-weight:600}
.svr-badge .svr-stars{color:var(--yb-amber)}
.svr-stars{display:flex;gap:2px;color:var(--yb-amber)}
.svr-stars svg{width:15px;height:15px}
.svr-viewport{overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
.svr-track{display:flex;width:max-content;gap:22px;padding:6px 0 18px;animation:svr-scroll var(--svr-dur,60s) linear infinite}
.svr-track:hover{animation-play-state:paused}
.svr-card{width:330px;flex:none;display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:22px;box-shadow:var(--sh-sm)}
.svr-card .svr-stars{margin-bottom:12px}
.svr-card p{margin:0 0 16px;font-size:14.5px;font-weight:500;color:var(--ink);line-height:1.6;flex:1;display:-webkit-box;-webkit-line-clamp:6;-webkit-box-orient:vertical;overflow:hidden}
.svr-foot{display:flex;align-items:center;justify-content:space-between;border-top:1px solid var(--line);padding-top:12px}
.svr-who{display:flex;align-items:center;gap:9px}
.svr-av{width:36px;height:36px;border-radius:50%;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-family:var(--font-display);font-size:12px;flex:none}
.svr-who span{font-weight:700;font-size:13px;color:var(--ink)}
.svr-g{font-size:11px;font-weight:800;color:var(--yb-blue);display:inline-flex;align-items:center;gap:4px}
.svr-all{text-align:center;margin:18px 0 0;font-weight:700;font-size:14.5px}
@keyframes svr-scroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@media(prefers-reduced-motion:reduce){.svr-track{animation:none;flex-wrap:wrap;justify-content:center;width:auto}.svr-track [aria-hidden]{display:none}}
@media(max-width:600px){.svr{padding-top:64px}.svr-card{width:280px}}
</style>"""

SPLIT_PAGES = {
    "seo": ("SEO Reviews Form", "Let's talk about your SEO", "Hablemos de su SEO"),
    "google-ads": ("Google Ads Reviews Form", "Let's talk about your Google Ads", "Hablemos de sus anuncios de Google"),
    "web-design": ("Web Design Reviews Form", "Let's talk about your website", "Hablemos de su sitio web"),
    "branding": ("Branding Reviews Form", "Let's talk about your brand", "Hablemos de su marca"),
    "social-media": ("Social Media Reviews Form", "Let's talk about your social media", "Hablemos de sus redes sociales"),
    "content-marketing": ("Content Reviews Form", "Let's talk about your content", "Hablemos de su contenido"),
    "press-releases": ("Press Releases Reviews Form", "Let's talk about your press release", "Hablemos de su comunicado de prensa"),
    "customer-growth": ("Customer Growth Reviews Form", "Let's talk about growing your customer base", "Hablemos de cómo hacer crecer su clientela"),
    "ai-for-business": ("AI for Business Reviews Form", "Let's talk about AI for your business", "Hablemos de IA para su empresa"),
    "ai-for-small-business": ("AI for Small Business Reviews Form", "Let's talk about AI for your business", "Hablemos de IA para su empresa"),
    "seo/local-seo": ("Local SEO Reviews Form", "Let's talk about your local SEO", "Hablemos de su SEO local"),
    "seo/ai-search": ("AI Search Reviews Form", "Let's talk about showing up in AI search", "Hablemos de aparecer en la búsqueda con IA"),
    "seo/technical-seo": ("Technical SEO Reviews Form", "Let's talk about your technical SEO", "Hablemos de su SEO técnico"),
    "seo/website-migration": ("Website Migration Reviews Form", "Let's talk about your website migration", "Hablemos de la migración de su sitio web"),
    "home": ("Home Page Reviews Form", "Let's talk about your marketing", "Hablemos de su marketing"),
}

HOME_HEAD = {
    "en": ("Client Love", "What Our Clients Say"),
    "es": ("Reseñas de clientes", "Lo que dicen nuestros clientes"),
}

ES_OPTIONS = {
    "web-design": "Diseño web", "seo": "SEO", "google-ads": "Google Ads", "branding": "Marca y diseño",
    "social-media": "Redes sociales", "content-marketing": "Marketing de contenidos",
    "press-releases": "Comunicados de prensa", "customer-growth": "Herramienta de crecimiento y comunicación",
    "ai-for-business": "IA para empresas", "ai-for-small-business": "IA para pequeñas empresas",
    "video-animation": "Animación de vídeo", "other": "No estoy seguro / Otro",
}

SPLIT_CSS = """<style>
.svr--split{padding:64px 0 72px}
.svr-split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px;align-items:start}
.svr--split .svr-head{text-align:left;margin:0 0 24px;padding:0;max-width:none}
.svr--split .svr-badges{justify-content:flex-start}
.svr-vp{height:470px;overflow:hidden;-webkit-mask-image:linear-gradient(180deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(180deg,transparent,#000 8%,#000 92%,transparent)}
.svr-vtrack{display:flex;flex-direction:column;animation:svr-vscroll var(--svr-dur,60s) linear infinite}
.svr-vtrack:hover{animation-play-state:paused}
.svr-vtrack .svr-card{width:auto;margin:0 4px 16px}
.svr--split .svr-all{text-align:left;margin-top:14px}
.svr-form-card{background:#fff;border:1px solid var(--line);border-radius:var(--r-xl,24px);padding:32px;box-shadow:var(--sh-md)}
.svr-form-card h3{font-family:var(--font-display);font-size:24px;font-weight:800;color:var(--ink);margin:0 0 8px}
.svr-form-card > p{color:var(--fg2);font-size:15px;line-height:1.6;margin:0 0 22px}
@keyframes svr-vscroll{from{transform:translateY(0)}to{transform:translateY(-50%)}}
@media(prefers-reduced-motion:reduce){.svr-vtrack{animation:none}.svr-vp{height:auto}.svr-vtrack [aria-hidden]{display:none}}
@media(max-width:900px){.svr-split{grid-template-columns:1fr;gap:40px}.svr-vp{height:380px}}
</style>"""

ES_FORM = [
    ("Name *", "Nombre *"), ('placeholder="Your name"', 'placeholder="Su nombre"'),
    ("Email *", "Correo electrónico *"), ("Phone *", "Teléfono *"),
    ("Company or URL", "Empresa o URL"), ('placeholder="yourcompany.com"', 'placeholder="suempresa.com"'),
    ("I'm interested in *", "Estoy interesado en *"), ("How can we help? *", "¿Cómo podemos ayudar? *"),
    ('placeholder="Tell us about your goals…"', 'placeholder="Cuéntenos sus objetivos…"'),
    ("We respond by the next business day. Your information is never shared.",
     "Respondemos el siguiente día hábil. Nunca compartimos su información."),
    ('redirect="/thank-you"', 'redirect="/es/thank-you"'),
    ("What are you interested in?", "¿Qué te interesa?"),
]


START, END = "<!-- svc-reviews:start -->", "<!-- svc-reviews:end -->"


def badges(c: dict) -> str:
    return (
        f'<div class="svr-badges">'
        f'<a class="svr-badge" href="{GOOGLE_REVIEWS_URL}" target="_blank" rel="noopener"><span class="svr-gicon">{GOOGLE_G}</span>'
        f'<span class="svr-stars">{STAR * 5}</span><b>5.0</b><span>{c["on"]} Google</span></a>'
        f'</div>'
    )


def initials(name: str) -> str:
    parts = [p for p in re.split(r"\s+", name.replace("'", "")) if p[:1].isalpha()]
    return (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper()


def card(name: str, i: int) -> str:
    text = REVIEWS[name].removesuffix(" …").removesuffix("…")
    return (
        f'<div class="svr-card"><div class="svr-stars">{STAR * 5}</div>'
        f'<p>"{escape(text)}"</p>'
        f'<div class="svr-foot"><div class="svr-who"><div class="svr-av" style="background:{AVATARS[i % len(AVATARS)]}">{initials(name)}</div>'
        f'<span>{escape(name)}</span></div><span class="svr-g">{CHECK}Google</span></div></div>'
    )


def block(service: str, lang: str, bg: str) -> str:
    c = COPY[lang]
    names = GROUPS[service]
    cards = [card(n, i) for i, n in enumerate(names)]
    while len(cards) < 8:
        cards = cards + cards
    half = "".join(cards)
    hidden = half.replace('<div class="svr-card">', '<div class="svr-card" aria-hidden="true">')
    dur = max(40, len(cards) * 7)
    return f"""{START}
{CSS}
<section class="svr" style="background:{bg}" aria-label="{escape(c['eyebrow'])}">
  <div class="svr-head">
    <span class="eyebrow" style="color:var(--yb-coral)">{escape(c['eyebrow'])}</span>
    <h2>{escape(c[service])}</h2>
    {badges(c)}
  </div>
  <div class="svr-viewport">
    <div class="svr-track" style="--svr-dur:{dur}s">{half}{hidden}</div>
  </div>
  <p class="svr-all"><a href="{c['href']}">{escape(c['all'])} &rarr;</a></p>
</section>
{END}
"""


def split_block(service: str, lang: str, bg: str, folder: str) -> str:
    c = COPY[lang]
    cards = [card(n, i) for i, n in enumerate(GROUPS[service])]
    while len(cards) < 6:
        cards = cards + cards
    half = "".join(cards)
    hidden = half.replace('<div class="svr-card">', '<div class="svr-card" aria-hidden="true">')
    source, title_en, title_es = SPLIT_PAGES[folder]
    title = title_es if lang == "es" else title_en
    form = lead_form_html(source, submit_label=c["submit"], default_interest="" if folder == "home" else folder.split("/")[0])
    eyebrow, heading = HOME_HEAD[lang] if folder == "home" else (c["eyebrow"], c[service])
    if lang == "es":
        for a, b in ES_FORM:
            form = form.replace(a, b)
        form = re.sub(
            r'(<option value="([^"]+)"(?: selected)?>)[^<]*(</option>)',
            lambda m: m.group(1) + ES_OPTIONS.get(m.group(2), "") + m.group(3) if m.group(2) in ES_OPTIONS else m.group(0),
            form,
        )
    return f"""{START}
{CSS}
{SPLIT_CSS}
<section class="svr svr--split" style="background:{bg}" aria-label="{escape(eyebrow)}">
  <div class="container svr-split">
    <div class="svr-left">
      <div class="svr-head">
        <span class="eyebrow" style="color:var(--yb-coral)">{escape(eyebrow)}</span>
        <h2>{escape(heading)}</h2>
        {badges(c)}
      </div>
      <div class="svr-vp">
        <div class="svr-vtrack" style="--svr-dur:{max(30, len(cards) * 6)}s">{half}{hidden}</div>
      </div>
      <p class="svr-all"><a href="{c['href']}">{escape(c['all'])} &rarr;</a></p>
    </div>
    <div class="svr-form-card">
      <h3>{escape(title)}</h3>
      <p>{escape(c['form_lead'])}</p>
{form}
    </div>
  </div>
</section>
{END}
"""


def find_anchor(html: str) -> int | None:
    m = re.search(r'<section\b[^>]*class="svc-hero', html)
    if not m:
        return None
    end = html.index("</section>", m.start()) + len("</section>")
    wave = re.match(r'\s*<div class="wave-div"[^>]*>.*?</div>\n?', html[end:], re.S)
    return end + wave.end() if wave else end


def find_faq_anchor(html: str) -> int | None:
    m = re.search(r'<section\b[^>]*id="faq"', html)
    if m:
        start = m.start()
    elif (item := html.find('class="faq-item"')) != -1:
        start = html.rindex("<section", 0, item)
    else:
        return None
    return html.rindex("</section>", 0, start) + len("</section>")


def prev_section_bg(html: str, pos: int) -> str:
    return section_bg(html, html.rindex("<section", 0, pos))


def section_bg(html: str, pos: int) -> str:
    tag = html[html.index("<section", pos):]
    tag = tag[:tag.index(">")]
    m = re.search(r'data-bg="(#[0-9A-Fa-f]{6})"', tag) or re.search(r'background:\s*([^;"]+)', tag)
    return m.group(1).strip() if m else "#fff"


def process(path: Path, service: str) -> bool:
    html = path.read_text(encoding="utf-8")
    html = re.sub(r"\n?" + re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S)
    if 'class="reviews-bg"' in html:
        return False
    lang = "es" if path.relative_to(ROOT).parts[0] == "es" else "en"
    parts = path.relative_to(ROOT).parts[1:] if lang == "es" else path.relative_to(ROOT).parts
    folder = None
    if len(parts) == 2:
        folder = parts[0] if parts[1] == "index.html" else f"{parts[0]}/{Path(parts[1]).stem}"
    if service == "generic" and folder not in SPLIT_PAGES and (pos := find_faq_anchor(html)) is not None:
        bg = prev_section_bg(html, pos)
    else:
        pos = find_anchor(html)
        if pos is None:
            print(f"  no hero anchor: {path.relative_to(ROOT)}")
            return False
        bg = section_bg(html, pos)
    section = split_block(service, lang, bg, folder) if folder in SPLIT_PAGES else block(service, lang, bg)
    new = html[:pos] + "\n" + section + html[pos:]
    path.write_text(new, encoding="utf-8")
    return True


def process_home(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    lang = "es" if path.relative_to(ROOT).parts[0] == "es" else "en"
    section = split_block("generic", lang, "#F6F8FC", "home")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?\n?", "", html, count=1, flags=re.S)
    new = re.sub(r'(<!-- REVIEWS -->\n)?<section class="reviews-bg"[^>]*>.*?</section>\n?', "", new, count=1, flags=re.S)
    svc = re.search(r'(<!-- SERVICES -->\n)?<section class="services"', new)
    if not svc:
        print(f"  no homepage services section: {path.relative_to(ROOT)}")
        return False
    new = new[:svc.start()] + section + "\n" + new[svc.start():]
    path.write_text(new, encoding="utf-8")
    return new != html


def main() -> None:
    n = 0
    for home in (ROOT / "index.html", ROOT / "es" / "index.html"):
        if process_home(home):
            n += 1
    for folder, service in SERVICE_DIRS.items():
        for base in (ROOT / folder, ROOT / "es" / folder):
            for f in sorted(base.glob("*.html")):
                if process(f, service):
                    n += 1
    print(f"inserted review scrollers on {n} pages")


if __name__ == "__main__":
    main()
