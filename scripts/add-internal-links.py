#!/usr/bin/env python3
"""Static internal links between service pages, case studies, and blog posts.

- Service pages: a Related Articles grid with the matching case study and posts,
  written into the HTML (fills the existing JS grid, or adds a section).
- Homepage: prerenders the insights scroller cards so crawlers see the links.
- Blog posts: a Keep reading block with related posts.
- Case studies: a Related services row linking to the services they show.

Idempotent: every block sits between marker comments and is replaced on rerun.
"""
from __future__ import annotations

import json
import re
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = json.loads((ROOT / "blog" / "data" / "posts.json").read_text(encoding="utf-8"))
BY_SLUG = {p["slug"]: p for p in POSTS}

OFF_TOPIC = {p["slug"] for p in POSTS if p["topic"] == "general"} | {
    "best-business-entity-for-franchisees",
    "what-drives-consumer-spending",
    "resolving-employee-disputes-before-you-are-sued",
}

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
READ = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'

TOPIC_HEX = {
    "seo": "#2BC4F0", "google-ads": "#FF6B57", "social-media": "#c77f12", "web-design": "#159468",
    "content": "#7B5BE6", "strategy": "#3F6FD6", "news": "#3F6FD6", "general": "#7B5BE6",
}
TOPIC_VAR = {
    "seo": "var(--yb-cyan)", "google-ads": "var(--yb-coral)", "social-media": "var(--yb-amber)",
    "web-design": "var(--yb-mint)", "content": "var(--yb-violet)", "strategy": "var(--yb-blue)",
    "news": "var(--yb-blue)", "general": "var(--yb-violet)",
}
TOPIC_ES = {
    "SEO": "SEO", "Strategy": "Estrategia", "Web Design": "Diseño web", "Social Media": "Redes sociales",
    "Google Ads": "Google Ads", "Content": "Contenido", "News": "Noticias", "General": "General",
}

T = {
    "en": {"case": "Case Study", "read": "Read More", "read_case": "Read the case study", "min": "min read",
           "eyebrow": "From Insights", "h2": "Related Articles",
           "lead": "Guides and results that go deeper on this service.",
           "keep": "Keep reading", "keep_lead": "More from the YB Marketing blog.",
           "rel_services": "Related services"},
    "es": {"case": "Caso de éxito", "read": "Leer más", "read_case": "Ver el caso de éxito", "min": "min de lectura",
           "eyebrow": "Desde el blog", "h2": "Artículos relacionados",
           "lead": "Guías y resultados que profundizan en este servicio.",
           "keep": "Siga leyendo", "keep_lead": "Más del blog de YB Marketing.",
           "rel_services": "Servicios relacionados"},
}

# page key -> (html file, case study slug or None, post slugs, accent)
SERVICES = {
    "seo": ("seo/index.html", "custom-home-builder-website-seo",
            ["how-long-does-seo-take", "seo-audit-what-actually-matters"], "#2BC4F0"),
    "seo/local-seo": ("seo/local-seo.html", "tree-services-local-seo",
                      ["local-service-page-seo-washington", "local-seo-washington-city-pages"], "#2BC4F0"),
    "seo/technical-seo": ("seo/technical-seo.html", "wordpress-portfolio-malware-remediation",
                          ["seo-audit-what-actually-matters", "should-you-rebuild-your-website"], "#2BC4F0"),
    "seo/website-migration": ("seo/website-migration.html", "equipment-manufacturer-website-redesign",
                              ["should-you-rebuild-your-website", "what-business-website-needs-2026"], "#2BC4F0"),
    "seo/ai-search": ("seo/ai-search.html", None,
                      ["how-to-show-up-chatgpt-ai-search", "does-seo-still-matter-with-ai-search",
                       "zero-click-local-marketing-washington"], "#2BC4F0"),
    "google-ads": ("google-ads/index.html", None,
                   ["seo-vs-google-ads-pacific-northwest", "5-paid-search-tactics-to-help-you-generate-leads",
                    "how-did-this-restaurants-pay-per-click-campaign-improve-so-drastically"], "#FF6B57"),
    "web-design": ("web-design/index.html", "equipment-manufacturer-website-redesign",
                   ["what-business-website-needs-2026", "what-is-a-landing-page-why-is-it-important"], "#159468"),
    "branding": ("branding/index.html", "fortune-500-multilingual-accessibility",
                 ["5-creative-ways-to-enhance-your-website-using-video",
                  "how-to-create-a-portfolio-website-for-your-small-business"], "#7B5BE6"),
    "social-media": ("social-media/index.html", "roofing-contractor-inbound-marketing",
                     ["social-media-management-vs-growth",
                      "7-ways-to-convert-social-media-followers-into-paying-customers"], "#c77f12"),
    "content-marketing": ("content-marketing/index.html", "environmental-engineering-content-marketing",
                          ["how-to-create-content-for-every-stage-in-the-buyers-journey",
                           "how-often-should-you-run-content-audits-and-update-your-site"], "#7B5BE6"),
    "press-releases": ("press-releases/index.html", "environmental-engineering-content-marketing",
                       ["yb-marketing-announces-strategic-acquisition-of-encite-branding-marketing-creative",
                        "how-to-create-content-for-every-stage-in-the-buyers-journey"], "#3F6FD6"),
    "customer-growth": ("customer-growth/index.html", "local-refrigeration-services-seo-growth",
                        ["why-you-should-be-using-customer-satisfaction-surveys",
                         "3-ways-to-close-more-internet-leads"], "#3F6FD6"),
    "ai-for-business": ("ai-for-business/index.html", None,
                        ["why-yb-builds-marketing-tools", "how-to-show-up-chatgpt-ai-search",
                         "does-seo-still-matter-with-ai-search"], "#7B5BE6"),
    "ai-for-small-business": ("ai-for-small-business/index.html", None,
                              ["why-yb-builds-marketing-tools", "local-business-marketing-budget",
                               "how-to-show-up-chatgpt-ai-search"], "#7B5BE6"),
}

SVC_LABELS = {
    "/seo": ("SEO", "SEO"), "/seo/local-seo": ("Local SEO", "SEO local"),
    "/seo/technical-seo": ("Technical SEO", "SEO técnico"), "/seo/website-migration": ("Website Migrations", "Migraciones de sitios web"),
    "/google-ads": ("Google Ads", "Google Ads"), "/web-design": ("Web Design", "Diseño web"),
    "/branding": ("Branding & Design", "Marca y diseño"), "/social-media": ("Social Media", "Redes sociales"),
    "/content-marketing": ("Content & Blogging", "Contenido y blogs"),
}
CASE_SERVICES = {
    "custom-home-builder-website-seo": ["/web-design", "/seo"],
    "ems-contract-manufacturer-google-ads-seo": ["/google-ads", "/seo"],
    "environmental-engineering-content-marketing": ["/content-marketing", "/seo"],
    "equipment-manufacturer-website-redesign": ["/web-design", "/seo/website-migration", "/seo"],
    "fortune-500-multilingual-accessibility": ["/web-design", "/branding"],
    "local-electrical-contractor-seo-growth": ["/seo", "/seo/local-seo"],
    "local-refrigeration-services-seo-growth": ["/seo", "/seo/local-seo"],
    "regional-tire-auto-seo-growth": ["/seo", "/seo/local-seo"],
    "roofing-contractor-inbound-marketing": ["/content-marketing", "/seo", "/google-ads", "/social-media"],
    "tree-services-local-seo": ["/seo/local-seo", "/seo"],
    "wordpress-portfolio-malware-remediation": ["/google-ads", "/seo/technical-seo", "/web-design"],
}

# service page key -> {lang: (eyebrow, h2, lead, link label, [(case slug, tag, name, big, big label, second, second label, desc)])}
RESULTS = {
    "google-ads": {
        "en": ("Results", "Google Ads Results",
               "Three clients with three different problems: a tight budget, leads that dried up off season, and ad accounts that kept getting suspended.",
               "Read the case study", [
            ("ems-contract-manufacturer-google-ads-seo", "Silicon Valley, CA", "Electronics Manufacturer", "10×", "Ad budget growth",
             "+75%", "website traffic in one year",
             "We started with a small, tightly targeted Google Ads budget. Those ads paid for the first round of growth, and the budget grew tenfold from there."),
            ("roofing-contractor-inbound-marketing", "Local Service Business", "Roofing Contractor", "+160%", "Phone calls",
             "+120%", "form submissions",
             "We combined Google Ads, SEO, content, and social media so leads kept coming in outside the rainy season."),
            ("wordpress-portfolio-malware-remediation", "130-Site Portfolio", "WordPress Agency", "130", "Sites cleaned in 15 days",
             "Reinstated", "Google Ads accounts",
             "Their Google Ads accounts kept getting suspended. We found hidden malware sending paid traffic to rogue sites, cleaned all 130 sites, and got the accounts back."),
        ]),
        "es": ("Resultados", "Resultados con Google Ads",
               "Tres clientes con tres problemas distintos: un presupuesto ajustado, clientes potenciales que desaparecían fuera de temporada y cuentas de anuncios que seguían siendo suspendidas.",
               "Ver el caso de éxito", [
            ("ems-contract-manufacturer-google-ads-seo", "Silicon Valley, CA", "Fabricante de electrónica", "10×", "Crecimiento del presupuesto de anuncios",
             "+75%", "tráfico del sitio web en un año",
             "Empezamos con un presupuesto pequeño y muy específico en Google Ads. Esos anuncios financiaron la primera etapa de crecimiento y el presupuesto se multiplicó por diez."),
            ("roofing-contractor-inbound-marketing", "Negocio de servicios locales", "Contratista de techos", "+160%", "Llamadas telefónicas",
             "+120%", "envíos de formularios",
             "Combinamos Google Ads, SEO, contenido y redes sociales para que los clientes potenciales siguieran llegando fuera de la temporada de lluvias."),
            ("wordpress-portfolio-malware-remediation", "Cartera de 130 sitios", "Agencia de WordPress", "130", "Sitios limpiados en 15 días",
             "Restablecidas", "cuentas de Google Ads",
             "Sus cuentas de Google Ads seguían siendo suspendidas. Encontramos malware oculto que desviaba el tráfico pagado, limpiamos los 130 sitios y recuperamos las cuentas."),
        ]),
    },
}

RESULTS_CSS = """<style>
.yb-results-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.yb-result-card{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--r-xl);padding:30px 28px;box-shadow:0 2px 10px rgba(22,32,58,.05);color:var(--ink);text-decoration:none;transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}
.yb-result-card:hover{transform:translateY(-3px);box-shadow:var(--sh-md);border-color:rgba(255,107,87,.5)}
.yb-result-tag{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--fg3)}
.yb-result-name{font-family:var(--font-display);font-weight:700;font-size:19px;margin:6px 0 20px}
.yb-result-big{font-family:var(--font-display);font-weight:800;font-size:clamp(2.6rem,4vw,3.4rem);line-height:1;background:var(--grad-sunset);-webkit-background-clip:text;background-clip:text;color:transparent}
.yb-result-big-label{font-size:14px;font-weight:600;color:var(--fg2);margin:8px 0 18px}
.yb-result-second{display:flex;align-items:baseline;gap:10px;padding:14px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-bottom:18px}
.yb-result-second strong{font-family:var(--font-display);font-size:24px;font-weight:800;color:var(--ink)}
.yb-result-second span{font-size:13.5px;color:var(--fg2)}
.yb-result-desc{font-size:14.5px;line-height:1.6;color:var(--fg2);margin:0 0 20px;flex:1}
.yb-result-link{font-size:14px;font-weight:700;color:var(--yb-coral);margin-top:auto}
@media(max-width:980px){.yb-results-grid{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.yb-results-grid{grid-template-columns:1fr}}
</style>"""


def process_results(key: str, lang: str) -> bool:
    if key not in RESULTS:
        return False
    rel = SERVICES[key][0]
    path = ROOT / "es" / rel if lang == "es" else ROOT / rel
    if not path.exists():
        return False
    html = path.read_text(encoding="utf-8")
    eyebrow, h2, lead, more, cards = RESULTS[key][lang]
    pre = "/es" if lang == "es" and (ROOT / "es" / "about" / "case-studies").exists() else ""
    items = "".join(
        f'<a class="yb-result-card" href="{pre}/about/case-studies/{slug}"><span class="yb-result-tag">{escape(tag)}</span>'
        f'<span class="yb-result-name">{escape(name)}</span><span class="yb-result-big">{escape(big)}</span>'
        f'<span class="yb-result-big-label">{escape(big_l)}</span>'
        f'<div class="yb-result-second"><strong>{escape(sec)}</strong><span>{escape(sec_l)}</span></div>'
        f'<p class="yb-result-desc">{escape(desc)}</p><span class="yb-result-link">{more} &rarr;</span></a>'
        for slug, tag, name, big, big_l, sec, sec_l, desc in cards
    )
    start, end = "<!-- results:start -->", "<!-- results:end -->"
    html = re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\n?", "", html, flags=re.S)
    anchor = html.find("<!-- svc-reviews:end -->")
    if anchor == -1:
        print(f"  no reviews block for results: {path.relative_to(ROOT)}")
        return False
    anchor += len("<!-- svc-reviews:end -->")
    m = re.search(r'<section class="svr[^"]*" style="background:([^;"]+)', html)
    bg = m.group(1) if m else "#fff"
    block = (
        f'\n{start}{RESULTS_CSS}\n<section style="background:{bg};padding:24px 0 80px">\n  <div class="container">\n'
        f'    <div style="text-align:center;max-width:700px;margin:0 auto 44px">\n'
        f'      <span class="eyebrow" style="color:{SERVICES[key][3]}">{eyebrow}</span>\n'
        f'      <h2 style="margin:14px 0 16px">{h2}</h2>\n'
        f'      <p style="color:var(--fg2);font-size:16px;line-height:1.75">{lead}</p>\n    </div>\n'
        f'    <div class="yb-results-grid">{items}</div>\n  </div>\n</section>\n{end}'
    )
    new = html[:anchor] + block + html[anchor:]
    original = path.read_text(encoding="utf-8")
    if new != original:
        path.write_text(new, encoding="utf-8")
    return new != original


CSS = """<style>
.yb-related-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.yb-case-thumb{background:var(--grad-navy);color:#fff;flex-direction:column;align-items:flex-start;justify-content:flex-end;padding:22px}
.yb-case-thumb strong{font-family:var(--font-display);font-size:40px;font-weight:800;line-height:1;color:#fff}
.yb-case-thumb span.yb-case-stat{font-size:13px;font-weight:600;color:rgba(255,255,255,.8);margin-top:8px}
@media(max-width:900px){.yb-related-grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.yb-related-grid{grid-template-columns:1fr}}
</style>"""


def page_text(path: Path, pattern: str) -> str:
    m = re.search(pattern, path.read_text(encoding="utf-8"), re.S) if path.exists() else None
    return unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""


def meta_desc(path: Path) -> str:
    html = path.read_text(encoding="utf-8") if path.exists() else ""
    tag = re.search(r'<meta\b[^>]*\bname="description"[^>]*>', html)
    m = re.search(r'\bcontent="([^"]*)"', tag.group(0)) if tag else None
    return unescape(m.group(1)).strip() if m else ""


def clip(text: str, n: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= n else text[: n].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


def post_info(slug: str, lang: str) -> dict:
    p = BY_SLUG[slug]
    info = {"href": f"/insights/{slug}", "title": p["title"], "excerpt": p["excerpt"], "label": p["topicLabel"],
            "image": p["image"], "topic": p["topic"], "minutes": p["readingTime"]}
    es_file = ROOT / "es" / "blog" / "posts" / f"{slug}.html"
    if lang == "es":
        info["label"] = TOPIC_ES.get(p["topicLabel"], p["topicLabel"])
        if es_file.exists():
            info["href"] = f"/es/insights/{slug}"
            info["title"] = page_text(es_file, r"<h1[^>]*>(.*?)</h1>") or info["title"]
            info["excerpt"] = meta_desc(es_file) or info["excerpt"]
    return info


def post_card(slug: str, lang: str, accent: str | None = None) -> str:
    i = post_info(slug, lang)
    color = accent or TOPIC_HEX.get(i["topic"], "#3F6FD6")
    return (
        f'<a href="{i["href"]}" class="insights-card"><div class="insights-card-thumb">'
        f'<img src="{escape(i["image"])}" alt="{escape(i["title"])}" loading="lazy">'
        f'<span class="insights-card-badge" style="background:{color}">{escape(i["label"])}</span></div>'
        f'<div class="insights-card-body"><h3>{escape(i["title"])}</h3><p>{escape(clip(i["excerpt"], 130))}</p>'
        f'<span class="insights-card-more" style="color:{color}">{T[lang]["read"]} {ARROW}</span></div></a>'
    )


def case_card(slug: str, lang: str, accent: str) -> str:
    rel = f"about/case-studies/{slug}.html"
    path = ROOT / "es" / rel if lang == "es" and (ROOT / "es" / rel).exists() else ROOT / rel
    href = ("/es" if path.parts[len(ROOT.parts)] == "es" else "") + f"/about/case-studies/{slug}"
    title = page_text(path, r"<h1[^>]*>(.*?)</h1>")
    desc = meta_desc(path)
    value = page_text(path, r'cs-hero-stat__value">(.*?)</span>')
    label = page_text(path, r'cs-hero-stat__label">(.*?)</span>')
    return (
        f'<a href="{href}" class="insights-card"><div class="insights-card-thumb yb-case-thumb">'
        f'<span class="insights-card-badge" style="background:{accent}">{T[lang]["case"]}</span>'
        f'<strong>{escape(value)}</strong><span class="yb-case-stat">{escape(label)}</span></div>'
        f'<div class="insights-card-body"><h3>{escape(title)}</h3><p>{escape(clip(desc, 130))}</p>'
        f'<span class="insights-card-more" style="color:{accent}">{T[lang]["read_case"]} {ARROW}</span></div></a>'
    )


def replace_block(html: str, start: str, end: str, content: str) -> tuple[str, bool]:
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if pat.search(html):
        return pat.sub(lambda _: start + content + end, html, count=1), True
    return html, False


def section_bg(html: str, pos: int) -> str:
    tag = html[html.rindex("<section", 0, pos):]
    tag = tag[: tag.index(">")]
    m = re.search(r'background:\s*([^;"]+)', tag)
    return m.group(1).strip() if m else "#fff"


def service_cards(key: str, lang: str) -> str:
    _, case, posts, accent = SERVICES[key]
    cards = ([case_card(case, lang, accent)] if case else []) + [post_card(s, lang, accent) for s in posts]
    return "".join(cards[:3])


def process_service(key: str, lang: str) -> bool:
    rel = SERVICES[key][0]
    path = ROOT / "es" / rel if lang == "es" else ROOT / rel
    if not path.exists():
        return False
    html = path.read_text(encoding="utf-8")
    original = html
    cards = service_cards(key, lang)
    start, end = "<!-- related:start -->", "<!-- related:end -->"
    own = re.compile(re.escape(start) + r"(?:(?!" + re.escape(end) + r").)*<section.*?" + re.escape(end) + r"\n?", re.S)
    html = own.sub("", html, count=1)
    html, done = replace_block(html, start, end, CSS + cards)
    if not done:
        grid = re.search(r'<div\b([^>]*\bdata-blog-insights\b[^>]*)>\s*</div>', html)
        if grid and 'data-variant="related"' in grid.group(1):
            html = html[:grid.start()] + f'<div class="blog-grid yb-related-grid">{start}{CSS}{cards}{end}</div>' + html[grid.end():]
        else:
            t = T[lang]
            faq = re.search(r'<section\b[^>]*id="faq"', html)
            pos = faq.start() if faq else None
            if pos is None and (item := html.find('class="faq-item"')) != -1:
                pos = html.rindex("<section", 0, item)
            if pos is None:
                print(f"  no anchor for related section: {path.relative_to(ROOT)}")
                return False
            bg = section_bg(html, pos)
            block = (
                f'{start}{CSS}\n<section style="background:{bg};padding:72px 0">\n  <div class="container">\n'
                f'    <div style="text-align:center;max-width:640px;margin:0 auto 40px">\n'
                f'      <span class="eyebrow" style="color:{SERVICES[key][3]}">{t["eyebrow"]}</span>\n'
                f'      <h2 style="margin:14px 0 12px">{t["h2"]}</h2>\n'
                f'      <p style="color:var(--fg2);font-size:16px;line-height:1.7">{t["lead"]}</p>\n    </div>\n'
                f'    <div class="yb-related-grid">{cards}</div>\n  </div>\n</section>\n{end}\n'
            )
            html = html[:pos] + block + html[pos:]
    if html != original:
        path.write_text(html, encoding="utf-8")
    return html != original


def home_card(slug: str, lang: str) -> str:
    i = post_info(slug, lang)
    t = T[lang]
    color = TOPIC_VAR.get(i["topic"], "var(--yb-blue)")
    return (
        f'<a href="{i["href"]}" class="blog-card"><div class="blog-thumb blog-thumb-sm">'
        f'<img src="{escape(i["image"])}" alt="{escape(i["title"])}" loading="lazy" style="width:100%;height:100%;object-fit:cover;position:absolute;inset:0">'
        f'<span class="blog-cat" style="color:{color}">{escape(i["label"])}</span></div>'
        f'<div class="blog-body"><h3 class="yb-h3" style="font-size:18px">{escape(i["title"])}</h3>'
        f'<p>{escape(clip(i["excerpt"], 120))}</p><div class="blog-meta"><span class="blog-read">{READ}{i["minutes"]} {t["min"]}</span>'
        f'<span class="blog-more" style="color:{color}">{t["read"]} {ARROW}</span></div></div></a>'
    )


def unique_image_slugs(candidates: list[str], n: int) -> list[str]:
    seen, out = set(), []
    for s in candidates:
        img = BY_SLUG[s]["image"]
        if img in seen:
            continue
        seen.add(img)
        out.append(s)
        if len(out) == n:
            break
    return out


def process_home(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    start, end = "<!-- home-insights:start -->", "<!-- home-insights:end -->"
    slugs = unique_image_slugs([p["slug"] for p in POSTS if p["slug"] not in OFF_TOPIC], 12)
    cards = "".join(home_card(s, "es" if path.parent.name == "es" else "en") for s in slugs)
    new, done = replace_block(html, start, end, cards)
    if not done:
        m = re.search(r'<div\b([^>]*\bdata-variant="home-scroll"[^>]*)>\s*</div>', html)
        if not m:
            print(f"  no homepage insights grid: {path.relative_to(ROOT)}")
            return False
        attrs = m.group(1).replace('class="blog-grid"', 'class="blog-grid blog-grid--scroll"') + " data-prerendered"
        new = html[:m.start()] + f"<div{attrs}>{start}{cards}{end}</div>" + html[m.end():]
    if new != html:
        path.write_text(new, encoding="utf-8")
    return new != html


def related_posts(slug: str, n: int = 3) -> list[str]:
    me = BY_SLUG.get(slug)
    pool = [p["slug"] for p in POSTS if p["slug"] not in OFF_TOPIC or p["slug"] == slug]

    def around(items: list[str]) -> list[str]:
        if slug in items:
            i = items.index(slug)
            ring = items[i + 1:] + items[:i]
        else:
            k = sum(map(ord, slug)) % max(len(items), 1)
            ring = items[k:] + items[:k]
        return [s for s in ring if s != slug]

    same = around([s for s in pool if me and BY_SLUG[s]["topic"] == me["topic"]])
    core = [s for s in pool if BY_SLUG[s]["topic"] in ("seo", "strategy", "web-design", "google-ads") and s not in same]
    image = BY_SLUG[slug]["image"] if me else None
    picks = [s for s in same + around(core) if BY_SLUG[s]["image"] != image]
    return unique_image_slugs(picks, n)


def process_post(path: Path) -> bool:
    lang = "es" if path.relative_to(ROOT).parts[0] == "es" else "en"
    slug = path.stem
    if slug not in BY_SLUG:
        return False
    html = path.read_text(encoding="utf-8")
    t = T[lang]
    cards = "".join(post_card(s, lang) for s in related_posts(slug))
    start, end = "<!-- post-related:start -->", "<!-- post-related:end -->"
    block = (
        f'{CSS}\n<section style="background:#fff;padding:8px 0 72px" aria-label="{t["keep"]}">\n  <div class="container">\n'
        f'    <h2 style="margin:0 0 6px;font-size:clamp(1.5rem,2.2vw,2rem)">{t["keep"]}</h2>\n'
        f'    <p style="color:var(--fg2);margin:0 0 26px">{t["keep_lead"]}</p>\n'
        f'    <div class="yb-related-grid">{cards}</div>\n  </div>\n</section>\n'
    )
    new, done = replace_block(html, start, end, block)
    if not done:
        a = html.find('<section class="blog-article"')
        if a == -1:
            print(f"  no article section: {path.relative_to(ROOT)}")
            return False
        close = html.index("</section>", html.index("</article>", a)) + len("</section>")
        new = html[:close] + "\n" + start + block + end + html[close:]
    new = new.replace('<noscript><link rel="stylesheet" href="/insights.css">\n', "<noscript>")
    if not re.search(r'<link rel="stylesheet" href="[^"]*insights\.css">', new.split("<noscript>")[0]):
        new = re.sub(r'(<link rel="stylesheet" href="[^"]*blog\.css">)', r'\1\n<link rel="stylesheet" href="/insights.css">', new, count=1)
    if new != html:
        path.write_text(new, encoding="utf-8")
    return new != html


def process_case(path: Path) -> bool:
    lang = "es" if path.relative_to(ROOT).parts[0] == "es" else "en"
    slug = path.stem
    if slug not in CASE_SERVICES:
        return False
    html = path.read_text(encoding="utf-8")
    prefix = "/es" if lang == "es" else ""
    links = "".join(
        f'<a class="cs-meta-tag" href="{prefix}{h}" style="text-decoration:none;color:#fff;border-color:rgba(43,196,240,.7)">'
        f'{escape(SVC_LABELS[h][1 if lang == "es" else 0])}</a>'
        for h in CASE_SERVICES[slug]
        if (ROOT / ("es" if lang == "es" else "") / (h.lstrip("/") + "/index.html")).exists()
        or (ROOT / ("es" if lang == "es" else "") / (h.lstrip("/") + ".html")).exists()
    )
    item = (
        f'<div class="cs-meta-item"><span class="cs-meta-item__label">{T[lang]["rel_services"]}</span>'
        f'<span class="cs-meta-item__value"><span class="cs-meta-tags">{links}</span></span></div>'
    )
    start, end = "<!-- case-services:start -->", "<!-- case-services:end -->"
    new, done = replace_block(html, start, end, item)
    if not done:
        g = html.find('class="cs-meta-grid"')
        if g == -1:
            print(f"  no meta grid: {path.relative_to(ROOT)}")
            return False
        depth, i = 0, html.index(">", g) + 1
        for m in re.finditer(r"<div\b|</div>", html[i:]):
            if m.group(0) == "<div":
                depth += 1
            elif depth == 0:
                i += m.start()
                break
            else:
                depth -= 1
        new = html[:i] + start + item + end + html[i:]
    if new != html:
        path.write_text(new, encoding="utf-8")
    return new != html


def main() -> None:
    svc = sum(process_service(k, lang) for k in SERVICES for lang in ("en", "es"))
    svc += sum(process_results(k, lang) for k in RESULTS for lang in ("en", "es"))
    home = sum(process_home(p) for p in (ROOT / "index.html", ROOT / "es" / "index.html") if p.exists())
    posts = sum(process_post(p) for d in (ROOT / "blog" / "posts", ROOT / "es" / "blog" / "posts") for p in sorted(d.glob("*.html")))
    cases = sum(process_case(p) for d in (ROOT / "about" / "case-studies", ROOT / "es" / "about" / "case-studies") for p in sorted(d.glob("*.html")))
    print(f"service pages {svc}, homepages {home}, posts {posts}, case studies {cases}")


if __name__ == "__main__":
    main()
