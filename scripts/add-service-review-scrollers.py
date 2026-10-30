#!/usr/bin/env python3
"""Insert a Google review scroller on service pages.

Services with matching reviews get it directly below the hero; the rest
(generic reviews) get it just above the FAQ.

Idempotent: replaces any existing block between the svc-reviews markers.
Re-run after regenerating service pages.
"""
from __future__ import annotations

import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_src = (ROOT / "scripts" / "add-reviews-page.py").read_text(encoding="utf-8")
_ns: dict = {}
exec(_src[_src.index("REVIEWS = ["):_src.index("\n]\n", _src.index("REVIEWS = [")) + 3], _ns)
REVIEWS: dict[str, str] = dict(_ns["REVIEWS"])

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
    "press-releases": "generic", "customer-growth": "generic", "growth-marketing": "generic",
    "ai-for-business": "generic", "ai-for-small-business": "generic",
}

COPY = {
    "en": {
        "eyebrow": "Client Reviews",
        "seo": "What clients say about our SEO work",
        "web-design": "What clients say about their new websites",
        "branding": "What clients say about their logos and branding",
        "generic": "What our clients say",
        "badge": "48 Google Reviews",
        "all": "Read all reviews",
        "href": "/reviews",
    },
    "es": {
        "eyebrow": "Reseñas de clientes",
        "seo": "Lo que dicen nuestros clientes sobre nuestro trabajo de SEO",
        "web-design": "Lo que dicen nuestros clientes sobre sus nuevos sitios web",
        "branding": "Lo que dicen nuestros clientes sobre sus logos y marca",
        "generic": "Lo que dicen nuestros clientes",
        "badge": "48 reseñas en Google",
        "all": "Ver todas las reseñas",
        "href": "/es/reviews",
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

START, END = "<!-- svc-reviews:start -->", "<!-- svc-reviews:end -->"


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
    <a class="svr-badge" href="{c['href']}"><span class="svr-stars">{STAR * 5}</span><b>5.0</b><span>· {escape(c['badge'])}</span></a>
  </div>
  <div class="svr-viewport">
    <div class="svr-track" style="--svr-dur:{dur}s">{half}{hidden}</div>
  </div>
  <p class="svr-all"><a href="{c['href']}">{escape(c['all'])} &rarr;</a></p>
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
    html = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S)
    if 'class="reviews-bg"' in html:
        return False
    lang = "es" if path.relative_to(ROOT).parts[0] == "es" else "en"
    if service == "generic" and (pos := find_faq_anchor(html)) is not None:
        bg = prev_section_bg(html, pos)
    else:
        pos = find_anchor(html)
        if pos is None:
            print(f"  no hero anchor: {path.relative_to(ROOT)}")
            return False
        bg = section_bg(html, pos)
    new = html[:pos] + "\n" + block(service, lang, bg) + html[pos:]
    path.write_text(new, encoding="utf-8")
    return True


def main() -> None:
    n = 0
    for folder, service in SERVICE_DIRS.items():
        for base in (ROOT / folder, ROOT / "es" / folder):
            for f in sorted(base.glob("*.html")):
                if process(f, service):
                    n += 1
    print(f"inserted review scrollers on {n} pages")


if __name__ == "__main__":
    main()
