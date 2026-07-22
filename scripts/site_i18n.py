"""Language helpers for English / Spanish site mirrors."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit, urlunsplit

from site_urls import ROOT, absolute_clean_url, clean_segment, page_href

SITE = "https://yakimabranding.com"
SUPPORTED_LANGS = ("en", "es")

# Curated chrome strings (nav/footer). Page body uses machine translation.
UI_ES: dict[str, str] = {
    "Home": "Inicio",
    "About": "Nosotros",
    "Services": "Servicios",
    "Insights": "Ideas",
    "Contact": "Contacto",
    "Get Started": "Empezar",
    "Open menu": "Abrir menú",
    "About Us": "Sobre nosotros",
    "Meet our team & our story": "Conoce al equipo y nuestra historia",
    "Case Studies": "Casos de éxito",
    "Client results & project highlights": "Resultados de clientes y proyectos destacados",
    "WA Sales Tax Notice": "Aviso de impuestos de WA",
    "Oct 2025 tax updates": "Actualizaciones fiscales de oct. 2025",
    "Oct 2025 advertising & software tax info": "Info fiscal de publicidad y software, oct. 2025",
    "About YB Marketing": "Sobre YB Marketing",
    "Pacific Northwest agency · Washington State": "Agencia del Pacífico Noroeste · Estado de Washington",
    "Branding & Design": "Marca y diseño",
    "Logos, systems & identity": "Logos, sistemas e identidad",
    "Web Design": "Diseño web",
    "WordPress, Wix & custom sites": "WordPress, Wix y sitios a medida",
    "Social Media": "Redes sociales",
    "Grow your following": "Haz crecer tu audiencia",
    "Google Ads": "Google Ads",
    "PPC that converts": "PPC que convierte",
    "SEO": "SEO",
    "Rank higher on Google": "Posiciónate mejor en Google",
    "Press Releases": "Comunicados de prensa",
    "Get published": "Publica tu marca",
    "Content & Blogging": "Contenido y blogs",
    "Copy that converts": "Textos que convierten",
    "Navigation": "Navegación",
    "Our Reach": "Nuestro alcance",
    "Locations": "Ubicaciones",
    "Privacy Policy": "Política de privacidad",
    "Sitemap": "Mapa del sitio",
    "SEO Optimization": "Optimización SEO",
    "Content Marketing": "Marketing de contenidos",
    "All rights reserved.": "Todos los derechos reservados.",
    "Award-winning digital marketing agency helping businesses grow through strategic branding, SEO, and comprehensive digital solutions.": (
        "Agencia de marketing digital galardonada que ayuda a las empresas a crecer "
        "mediante branding estratégico, SEO y soluciones digitales integrales."
    ),
    "Yakima Branding is centered in Central Washington, with deep roots in the Yakima community. From our home base in Yakima, we proudly serve businesses across the entire Pacific Northwest with strategic marketing, website design, SEO, advertising, and branding support.": (
        "Yakima Branding tiene su centro en el centro de Washington, con profundas raíces "
        "en la comunidad de Yakima. Desde nuestra sede en Yakima, servimos con orgullo a "
        "empresas de todo el Pacífico Noroeste con marketing estratégico, diseño web, SEO, "
        "publicidad y soporte de marca."
    ),
    "Language": "Idioma",
}


def t(text: str, lang: str = "en") -> str:
    if lang != "es":
        return text
    return UI_ES.get(text, text)


def page_href_lang(path: str, lang: str = "en", anchor: Optional[str] = None) -> str:
    href = page_href(path, anchor)
    if lang != "es":
        return href
    if href == "/":
        return "/es/"
    if href.startswith("/"):
        return f"/es{href}"
    return f"/es/{href}"


def file_to_clean_path(rel_html: str) -> str:
    """Repo-relative HTML path → clean URL path (no leading slash, '' for home)."""
    return clean_segment(rel_html.replace("\\", "/"))


def clean_path_from_file(path: Path) -> str:
    rel = path.resolve().relative_to(ROOT.resolve()).as_posix()
    if rel.startswith("es/"):
        rel = rel[3:]
    return file_to_clean_path(rel)


def localize_clean_path(clean: str, lang: str) -> str:
    clean = clean.strip("/")
    if lang == "es":
        return "/es/" if not clean else f"/es/{clean}"
    return "/" if not clean else f"/{clean}"


def alternate_path(current_clean: str, target_lang: str) -> str:
    """current_clean is without /es prefix ('' for home)."""
    return localize_clean_path(current_clean, target_lang)


def strip_es_prefix(url_path: str) -> str:
    path = url_path.split("?", 1)[0].split("#", 1)[0]
    if path.startswith("/es/") or path == "/es":
        path = path[3:] or "/"
    return path


def language_switcher_html(current_clean: str, lang: str = "en", variant: str = "header") -> str:
    """EN / ES segmented switcher."""
    en_href = alternate_path(current_clean, "en")
    es_href = alternate_path(current_clean, "es")
    label = t("Language", lang)
    cls = "lang-switch lang-switch--header" if variant == "header" else "lang-switch lang-switch--footer"
    en_active = " is-active" if lang == "en" else ""
    es_active = " is-active" if lang == "es" else ""
    en_aria = ' aria-current="page"' if lang == "en" else ""
    es_aria = ' aria-current="page"' if lang == "es" else ""
    return f"""<div class="{cls}" role="group" aria-label="{html.escape(label)}">
  <a class="lang-switch-opt{en_active}" href="{html.escape(en_href)}"{en_aria} lang="en" hreflang="en">EN</a>
  <a class="lang-switch-opt{es_active}" href="{html.escape(es_href)}"{es_aria} lang="es" hreflang="es">ES</a>
</div>"""


def hreflang_links(current_clean: str) -> str:
    en = f"{SITE}{alternate_path(current_clean, 'en')}"
    es = f"{SITE}{alternate_path(current_clean, 'es')}"
    # Prefer trailing-slash-free except home EN is SITE/
    if en.endswith("/") and en != f"{SITE}/":
        en = en.rstrip("/")
    if es.endswith("/") and es != f"{SITE}/es/":
        es = es.rstrip("/")
    return "\n".join(
        [
            f'<link rel="alternate" hreflang="en" href="{html.escape(en)}">',
            f'<link rel="alternate" hreflang="es" href="{html.escape(es)}">',
            f'<link rel="alternate" hreflang="x-default" href="{html.escape(en)}">',
        ]
    )


def rewrite_internal_href_to_es(href_value: str) -> str:
    """Prefix internal absolute clean URLs with /es. Leave assets/external alone."""
    if not href_value or href_value.startswith("#"):
        return href_value
    lower = href_value.lower()
    if lower.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "data:")):
        if "yakimabranding.com" in lower:
            parsed = urlsplit(href_value)
            path = parsed.path or "/"
            if path.startswith("/es"):
                return href_value
            new_path = "/es" + (path if path.startswith("/") else f"/{path}")
            if new_path != "/es/" and new_path.endswith("/"):
                new_path = new_path.rstrip("/")
            return urlunsplit((parsed.scheme, parsed.netloc, new_path, parsed.query, parsed.fragment))
        return href_value

    parsed = urlsplit(href_value)
    path = parsed.path or ""
    if not path.startswith("/"):
        # relative — leave for asset-prefix fixer
        return href_value

    # Skip static assets
    skip_prefixes = (
        "/assets/",
        "/js/",
        "/wp-content/",
        "/_next/",
        "/favicon",
        "/colors_and_type.css",
        "/site.css",
        "/insights.css",
        "/hero-orbit.css",
        "/robots.txt",
        "/sitemap",
    )
    if path == "/favicon.png" or any(path.startswith(p) for p in skip_prefixes):
        # Allow /sitemap as a page — only skip xml-ish. /sitemap is a page.
        if path.startswith("/sitemap") and not path.endswith(".xml"):
            pass
        elif path != "/sitemap" and not path.startswith("/sitemap.html"):
            if any(
                path.startswith(p)
                for p in (
                    "/assets/",
                    "/js/",
                    "/wp-content/",
                    "/_next/",
                    "/favicon",
                    "/colors_and_type.css",
                    "/site.css",
                    "/insights.css",
                    "/hero-orbit.css",
                )
            ) or path.endswith((".css", ".js", ".png", ".jpg", ".webp", ".svg", ".ico", ".woff2", ".xml")):
                return href_value

    if path.startswith("/es/") or path == "/es":
        return href_value

    new_path = "/es" + path
    return urlunsplit(("", "", new_path, parsed.query, parsed.fragment))


def absolute_asset_url(href_value: str, source_file: Path) -> str:
    """Convert relative asset links to root-absolute paths."""
    if not href_value or href_value.startswith(("#", "data:", "mailto:", "tel:", "javascript:")):
        return href_value
    lower = href_value.lower()
    if lower.startswith(("http://", "https://", "//")):
        return href_value
    if href_value.startswith("/"):
        return href_value
    try:
        rel = (source_file.parent / href_value).resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return href_value
    return "/" + rel
