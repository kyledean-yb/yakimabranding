"""Mega menu site navigation (desktop + mobile), shared by generators and the site-wide patch."""

from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ICONS = {
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "megaphone": '<path d="M3 11l18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "chart": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "spark": '<path d="M12 3l1.9 5.8L20 10l-6.1 1.2L12 17l-1.9-5.8L4 10l6.1-1.2z"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M16 6h.01M12 6h.01M8 10h.01M16 10h.01M12 10h.01M8 14h.01M16 14h.01M12 14h.01"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
}

CASE_ELECTRICAL = ("+204%", "Page one keywords for a Bay Area electrical contractor", "/about/case-studies/local-electrical-contractor-seo-growth")
CASE_REFRIG = ("+2,900%", "Page one keywords for a Central Washington refrigeration company", "/about/case-studies/local-refrigeration-services-seo-growth")
CASE_TIRE = ("+613%", "Page one keywords for a regional tire and auto shop", "/about/case-studies/regional-tire-auto-seo-growth")
CASE_EMS = ("10×", "Ad budget growth for a Silicon Valley electronics manufacturer", "/about/case-studies/ems-contract-manufacturer-google-ads-seo")
CASE_ROOF = ("+160%", "More phone calls for a local roofing contractor", "/about/case-studies/roofing-contractor-inbound-marketing")
CASE_WP = ("130", "WordPress websites cleaned and secured in 15 days", "/about/case-studies/wordpress-portfolio-malware-remediation")

MENUS: list[dict] = [
    {
        "label": "Digital Marketing",
        "cols": [
            {"title": "SEO", "icon": "search", "links": [
                ("SEO Services", "/seo"),
                ("Local SEO", "/seo/local-seo"),
                ("AI Search (GEO)", "/seo/ai-search"),
                ("Technical SEO", "/seo/technical-seo"),
                ("Website Migrations", "/seo/website-migration"),
            ]},
            {"title": "Paid Advertising", "icon": "target", "links": [
                ("Google Ads Management", "/google-ads"),
                ("SEO or Google Ads?", "/blog/posts/seo-vs-google-ads-pacific-northwest"),
                ("5 Paid Search Tactics", "/blog/posts/5-paid-search-tactics-to-help-you-generate-leads"),
                ("Types of Facebook Ads", "/blog/posts/types-of-facebook-ads"),
            ]},
            {"title": "Online Marketing", "icon": "megaphone", "links": [
                ("Social Media Marketing", "/social-media"),
                ("Content & Blogging", "/content-marketing"),
                ("Press Releases", "/press-releases"),
                ("Branding & Design", "/branding"),
                ("Customer Growth & Communication Tool", "/customer-growth"),
            ]},
        ],
        "feature": {"title": "Case Studies", "cards": [CASE_REFRIG, CASE_TIRE], "more": ("All case studies", "/about/case-studies")},
    },
    {
        "label": "AI",
        "cols": [
            {"title": "AI Services", "icon": "spark", "links": [
                ("AI for Business", "/ai-for-business"),
                ("AI for Small Business", "/ai-for-small-business"),
                ("AI Search (GEO)", "/seo/ai-search"),
            ]},
            {"title": "Learn", "icon": "book", "links": [
                ("Show Up in ChatGPT & AI Search", "/blog/posts/how-to-show-up-chatgpt-ai-search"),
                ("Does SEO Still Matter With AI?", "/blog/posts/does-seo-still-matter-with-ai-search"),
                ("Why YB Builds Marketing Tools", "/blog/posts/why-yb-builds-marketing-tools"),
            ]},
        ],
    },
    {
        "label": "SEO",
        "cols": [
            {"title": "SEO Services", "icon": "search", "links": [
                ("SEO Services", "/seo"),
                ("Local SEO", "/seo/local-seo"),
                ("AI Search (GEO)", "/seo/ai-search"),
                ("Technical SEO", "/seo/technical-seo"),
                ("Website Migrations", "/seo/website-migration"),
            ]},
        ],
        "feature": {"title": "SEO Results", "cards": [CASE_ELECTRICAL, CASE_REFRIG], "more": ("SEO case studies", "/about/case-studies")},
    },
    {
        "label": "Web Design",
        "cols": [
            {"title": "Web Design", "icon": "monitor", "links": [
                ("Web Design Services", "/web-design"),
                ("Branding & Design", "/branding"),
                ("Website Migrations", "/seo/website-migration"),
                ("Technical SEO", "/seo/technical-seo"),
            ]},
        ],
        "feature": {"title": "Case Study", "cards": [CASE_WP], "more": ("All case studies", "/about/case-studies")},
    },
    {
        "label": "Paid Ads",
        "cols": [
            {"title": "Paid Advertising", "icon": "target", "links": [
                ("Google Ads Management", "/google-ads"),
                ("SEO or Google Ads?", "/blog/posts/seo-vs-google-ads-pacific-northwest"),
                ("5 Paid Search Tactics", "/blog/posts/5-paid-search-tactics-to-help-you-generate-leads"),
                ("Types of Facebook Ads", "/blog/posts/types-of-facebook-ads"),
            ]},
        ],
        "feature": {"title": "Ads Results", "cards": [CASE_EMS, CASE_ROOF], "more": ("All case studies", "/about/case-studies")},
    },
    {
        "label": "Insights",
        "cols": [
            {"title": "Resources", "icon": "book", "links": [
                ("Blog", "/insights"),
                ("Client Corner", "/client-corner"),
                ("CRM Tutorials", "/crm-tutorials"),
            ]},
            {"title": "Popular Articles", "icon": "file", "links": [
                ("How Long Does SEO Take?", "/blog/posts/how-long-does-seo-take"),
                ("What a Business Website Needs in 2026", "/blog/posts/what-business-website-needs-2026"),
                ("Setting a Local Marketing Budget", "/blog/posts/local-business-marketing-budget"),
            ]},
        ],
    },
    {
        "label": "About",
        "cols": [
            {"title": "Company", "icon": "building", "links": [
                ("About Us", "/about"),
                ("Our Team", "/about#team"),
                ("Case Studies", "/about/case-studies"),
                ("Client Reviews", "/reviews"),
                ("Locations We Serve", "/locations"),
                ("WA Sales Tax Notice", "/washington-state-sales-tax-notice"),
            ]},
        ],
    },
]

ES = {
    "Digital Marketing": "Marketing digital",
    "AI": "IA",
    "Web Design": "Diseño web",
    "Paid Ads": "Publicidad",
    "Insights": "Recursos",
    "About": "Nosotros",
    "Contact Us": "Contáctenos",
    "Paid Advertising": "Publicidad pagada",
    "Online Marketing": "Marketing en línea",
    "Case Studies": "Casos de éxito",
    "Case Study": "Caso de éxito",
    "All case studies": "Todos los casos",
    "SEO case studies": "Casos de SEO",
    "SEO Results": "Resultados de SEO",
    "SEO Services": "Servicios de SEO",
    "Local SEO": "SEO local",
    "AI Search (GEO)": "Búsqueda con IA (GEO)",
    "Technical SEO": "SEO técnico",
    "Website Migrations": "Migraciones de sitios web",
    "Google Ads Management": "Gestión de Google Ads",
    "SEO or Google Ads?": "¿SEO o Google Ads?",
    "5 Paid Search Tactics": "5 tácticas de búsqueda pagada",
    "Types of Facebook Ads": "Tipos de anuncios en Facebook",
    "Social Media Marketing": "Marketing en redes sociales",
    "Content & Blogging": "Contenido y blogs",
    "Press Releases": "Comunicados de prensa",
    "Branding & Design": "Marca y diseño",
    "Customer Growth & Communication Tool": "Herramienta de crecimiento y comunicación",
    "AI Services": "Servicios de IA",
    "AI for Business": "IA para empresas",
    "AI for Small Business": "IA para pequeñas empresas",
    "Learn": "Aprenda",
    "Show Up in ChatGPT & AI Search": "Aparezca en ChatGPT y búsquedas con IA",
    "Does SEO Still Matter With AI?": "¿Sigue importando el SEO con la IA?",
    "Why YB Builds Marketing Tools": "Por qué YB crea herramientas de marketing",
    "SEO by City": "SEO por ciudad",
    "Web Design Services": "Servicios de diseño web",
    "Web Design by City": "Diseño web por ciudad",
    "Google Ads by City": "Google Ads por ciudad",
    "Resources": "Recursos",
    "Blog": "Blog",
    "Client Corner": "Rincón del cliente",
    "CRM Tutorials": "Tutoriales de CRM",
    "Popular Articles": "Artículos populares",
    "How Long Does SEO Take?": "¿Cuánto tarda el SEO?",
    "What a Business Website Needs in 2026": "Lo que necesita un sitio web en 2026",
    "Setting a Local Marketing Budget": "Presupuesto de marketing local",
    "Company": "Empresa",
    "About Us": "Sobre nosotros",
    "WA Sales Tax Notice": "Aviso de impuesto de WA",
    "Client Reviews": "Reseñas de clientes",
    "Locations We Serve": "Dónde trabajamos",
    "Our Team": "Nuestro equipo",
    "Kevin Dean, Owner": "Kevin Dean, Propietario",
    "Jacob Ross, Account Executive": "Jacob Ross, Ejecutivo de cuentas",
    "Sophie Mann, Account Executive": "Sophie Mann, Ejecutiva de cuentas",
    "Kirsten Gonzalez, Marketing Administrator": "Kirsten Gonzalez, Administradora de marketing",
    "Kayelyn Aggett, Social Media Manager": "Kayelyn Aggett, Gerente de redes sociales",
    "Page one keywords for a Bay Area electrical contractor": "Palabras clave en la primera página para un contratista eléctrico",
    "Page one keywords for a Central Washington refrigeration company": "Palabras clave en la primera página para una empresa de refrigeración",
    "Page one keywords for a regional tire and auto shop": "Palabras clave en la primera página para un taller de llantas",
    "WordPress websites cleaned and secured in 15 days": "Sitios WordPress limpiados y protegidos en 15 días",
    "Ad budget growth for a Silicon Valley electronics manufacturer": "Crecimiento del presupuesto de anuncios para un fabricante de electrónica",
    "More phone calls for a local roofing contractor": "Más llamadas para un contratista de techos local",
    "Ads Results": "Resultados de anuncios",
}


def tr(text: str, lang: str) -> str:
    return ES.get(text, text) if lang == "es" else text


def _es_exists(path: str) -> bool:
    p = path.strip("/")
    if not p:
        return (ROOT / "es" / "index.html").exists()
    return (ROOT / "es" / f"{p}.html").exists() or (ROOT / "es" / p / "index.html").exists()


def href(path: str, lang: str) -> str:
    if lang == "es" and _es_exists(path):
        return "/es" + (path if path != "/" else "/")
    return path


def _icon(name: str) -> str:
    if not name:
        return ""
    return (
        '<svg class="mega-col-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


COLUMN_ACCENTS = {
    "SEO": "var(--yb-cyan)",
    "SEO Services": "var(--yb-cyan)",
    "Paid Advertising": "var(--yb-coral)",
    "Web Design": "#159468",
    "AI Services": "var(--yb-violet)",
}

SERVICE_ACCENTS = [
    ("/seo", "var(--yb-cyan)"),
    ("/google-ads", "var(--yb-coral)"),
    ("/social-media", "#c77f12"),
    ("/web-design", "#159468"),
    ("/content-marketing", "var(--yb-pink)"),
    ("/press-releases", "var(--yb-pink)"),
    ("/branding", "var(--yb-violet)"),
    ("/customer-growth", "var(--yb-blue)"),
    ("/ai-for-", "var(--yb-violet)"),
]


def _link_accent(path: str, col_accent: str | None) -> str | None:
    for prefix, color in SERVICE_ACCENTS:
        if path == prefix or path.startswith(prefix + "/") or (prefix.endswith("-") and path.startswith(prefix)):
            return color
    return col_accent


def _col_html(col: dict, lang: str) -> str:
    title = tr(col["title"], lang)
    col_accent = COLUMN_ACCENTS.get(col["title"])
    style = f' style="--col-ac:{col_accent}"' if col_accent else ""
    head = (
        f'<div class="mega-col-title">{_icon(col["icon"])}<span>{escape(title)}</span></div>'
        if title
        else '<div class="mega-col-title mega-col-title--blank" aria-hidden="true"></div>'
    )
    items = []
    for label, h in col["links"]:
        ac = _link_accent(h, col_accent)
        attr = f' class="mega-svc" style="--ac:{ac}"' if ac else ""
        items.append(f'<li><a href="{href(h, lang)}"{attr}>{escape(tr(label, lang))}</a></li>')
    return f'<div class="mega-col"{style}>{head}<ul>{"".join(items)}</ul></div>'


def _feature_html(feature: dict, lang: str) -> str:
    cards = "".join(
        f'<a class="mega-case" href="{href(h, lang)}"><span class="mega-case-num">{big}</span>'
        f'<span class="mega-case-text">{escape(tr(text, lang))}</span></a>'
        for big, text, h in feature["cards"]
    )
    more_label, more_href = feature["more"]
    return (
        f'<div class="mega-col mega-col--feature"><div class="mega-col-title">{_icon("chart")}'
        f'<span>{escape(tr(feature["title"], lang))}</span></div>{cards}'
        f'<a class="mega-more" href="{href(more_href, lang)}">{escape(tr(more_label, lang))} →</a></div>'
    )


CHEVRON = (
    '<svg class="nav-chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>'
)


def desktop_nav_html(lang: str = "en") -> str:
    items = []
    for menu in MENUS:
        cols = "".join(_col_html(c, lang) for c in menu["cols"])
        if menu.get("feature"):
            cols += _feature_html(menu["feature"], lang)
        n = len(menu["cols"]) + (1 if menu.get("feature") else 0)
        items.append(
            f'<div class="nav-mega"><button class="nav-svc-btn" type="button" aria-haspopup="true">'
            f'{escape(tr(menu["label"], lang))} {CHEVRON}</button>'
            f'<div class="mega-panel" style="--mega-cols:{n}"><div class="mega-grid">{cols}</div></div></div>'
        )
    items.append(f'<a href="{href("/contact", lang)}" class="nav-a">{escape(tr("Contact Us", lang))}</a>')
    cls = "nav nav--mega nav--es" if lang == "es" else "nav nav--mega"
    return f'<nav class="{cls}">\n      ' + "\n      ".join(items) + "\n    </nav>"


def mobile_menu_items_html(lang: str = "en") -> str:
    parts = []
    for i, menu in enumerate(MENUS):
        list_id = f"mobileNav{i}"
        rows = []
        seen = set()
        for col in menu["cols"]:
            if col.get("mobile", True) is False:
                continue
            for label, h in col["links"]:
                if h in seen:
                    continue
                seen.add(h)
                rows.append(f'      <a href="{href(h, lang)}" class="mobile-about-row"><strong>{escape(tr(label, lang))}</strong></a>')
        if menu.get("feature"):
            more_label, more_href = menu["feature"]["more"]
            if more_href not in seen:
                rows.append(f'      <a href="{href(more_href, lang)}" class="mobile-about-row"><strong>{escape(tr(more_label, lang))}</strong></a>')
        parts.append(
            f"    <a href=\"#\" onclick=\"document.getElementById('{list_id}').classList.toggle('open');return false\" "
            f'style="display:flex;justify-content:space-between;align-items:center">{escape(tr(menu["label"], lang))} <span>▾</span></a>\n'
            f'    <div class="mobile-svc-list" id="{list_id}">\n' + "\n".join(rows) + "\n    </div>"
        )
    parts.append(f'    <a href="{href("/contact", lang)}">{escape(tr("Contact Us", lang))}</a>')
    return "\n".join(parts)


# ------------------------------------------------------------ HTML patching

def _match_div(text: str, start: int) -> int:
    """Return index just past the </div> closing the <div ...> that starts at `start`."""
    depth = 0
    i = start
    while i < len(text):
        o = text.find("<div", i)
        c = text.find("</div>", i)
        if c == -1:
            return -1
        if o != -1 and o < c:
            depth += 1
            i = o + 4
        else:
            depth -= 1
            i = c + 6
            if depth == 0:
                return i
    return -1


def patch_topbar(text: str) -> str:
    """Move the header actions (language switch, phone, CTA) into a bar above the nav."""
    if 'class="header-topbar"' in text:
        return text
    hs = text.find('<div class="header top" id="header">')
    if hs == -1:
        return text
    bs = text.find('<div class="btn-hdr"', hs)
    if bs == -1:
        return text
    be = _match_div(text, bs)
    block = text[bs:be]
    inner = block[block.index(">") + 1 : -len("</div>")].strip()
    text = text[:bs].rstrip(" ") + text[be:].lstrip("\n")
    open_tag = '<div class="header top" id="header">'
    bar = (
        '\n  <div class="header-topbar"><div class="container header-topbar-inner">'
        '<div class="header-topbar-actions">\n      ' + inner + "\n  </div></div></div>"
    )
    return text[: hs + len(open_tag)] + bar + text[hs + len(open_tag):]


def patch_html(text: str, lang: str) -> str:
    text = patch_topbar(text)
    ns = text.find('<nav class="nav')
    if ns != -1:
        ne = text.find("</nav>", ns)
        if ne != -1:
            text = text[:ns] + desktop_nav_html(lang) + text[ne + len("</nav>"):]

    ms = text.find('<div class="mobile-menu" id="mobileMenu">')
    if ms != -1:
        me = _match_div(text, ms)
        if me != -1:
            block = text[ms:me]
            keep = ""
            ls = block.find('<div class="mobile-menu-lang">')
            if ls != -1:
                le = _match_div(block, ls)
                keep = "\n    " + block[ls:le]
            new_block = (
                '<div class="mobile-menu" id="mobileMenu">\n'
                + mobile_menu_items_html(lang)
                + keep
                + "\n  </div>"
            )
            text = text[:ms] + new_block + text[me:]
    return text
