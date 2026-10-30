"""Site footer markup (matches index.html)."""

from __future__ import annotations

import html
from pathlib import Path

from mega_nav import href as nav_href, tr as nav_tr
from site_i18n import language_switcher_html, page_href_lang, t

ROOT = Path(__file__).resolve().parents[1]

FOOTER_COLUMNS = [
    ("Digital Marketing", [
        ("SEO Services", "/seo"),
        ("Local SEO", "/seo/local-seo"),
        ("Technical SEO", "/seo/technical-seo"),
        ("Website Migrations", "/seo/website-migration"),
        ("Google Ads Management", "/google-ads"),
        ("Social Media Marketing", "/social-media"),
    ]),
    ("Web & Brand", [
        ("Web Design Services", "/web-design"),
        ("Branding & Design", "/branding"),
        ("Content & Blogging", "/content-marketing"),
        ("Press Releases", "/press-releases"),
        ("Customer Growth & Communication Tool", "/customer-growth"),
    ]),
    ("AI", [
        ("AI for Business", "/ai-for-business"),
        ("AI for Small Business", "/ai-for-small-business"),
        ("AI Search (GEO)", "/seo/ai-search"),
        ("Show Up in ChatGPT & AI Search", "/blog/posts/how-to-show-up-chatgpt-ai-search"),
    ]),
    ("Company", [
        ("About Us", "/about"),
        ("Case Studies", "/about/case-studies"),
        ("Client Reviews", "/reviews"),
        ("Blog", "/insights"),
        ("Client Corner", "/client-corner"),
        ("CRM Tutorials", "/crm-tutorials"),
        ("Contact", "/contact"),
    ]),
    ("Locations", [
        ("All Locations", "/locations"),
        ("Central Washington", "/locations/central-washington"),
        ("Eastern Washington", "/locations/eastern-washington"),
        ("San Francisco Bay Area", "/locations/san-francisco-bay-area"),
        ("Denver Area", "/locations/denver-co"),
        ("Phoenix Area", "/locations/phoenix-az"),
        ("Chicago Area", "/locations/chicago-il"),
    ]),
]

FOOTER_BLURB = "YB Marketing has helped businesses grow since 2004 with marketing, website design, SEO, advertising, and branding."

FOOTER_ES = {
    "Web & Brand": "Web y marca",
    "Locations": "Ubicaciones",
    "All Locations": "Todas las ubicaciones",
    "Central Washington": "Centro de Washington",
    "Eastern Washington": "Este de Washington",
    "San Francisco Bay Area": "Área de la Bahía de San Francisco",
    "Denver Area": "Área de Denver",
    "Phoenix Area": "Área de Phoenix",
    "Chicago Area": "Área de Chicago",
    "Contact": "Contacto",
    "Get in Touch": "Contáctenos",
    "Let's get in touch": "Hablemos",
    "Our Locations": "Nuestras ubicaciones",
    FOOTER_BLURB: "YB Marketing ayuda a las empresas a crecer desde 2004 con marketing, diseño de sitios web, SEO, publicidad y branding.",
}

OFFICES = [
    ("Scottsdale, AZ", "/locations/phoenix-az"),
    ("Yakima, WA", "/locations/yakima-wa"),
    ("San Francisco, CA", "/locations/san-francisco-bay-area"),
    ("Chicago, IL", "/locations/chicago-il"),
]


def ft(text: str, lang: str) -> str:
    if lang != "es":
        return text
    return FOOTER_ES.get(text) or nav_tr(text, lang)


PHONE_SVG = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--yb-cyan)" stroke-width="2.2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
MAIL_SVG = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--yb-cyan)" stroke-width="2" stroke-linecap="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'
PIN_SVG = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--yb-cyan)" stroke-width="2.2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
ARROW_SVG = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--yb-cyan)" stroke-width="2.2" stroke-linecap="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>'


def footer_link_columns(lang: str) -> str:
    cols = []
    for title, links in FOOTER_COLUMNS:
        items = "\n".join(
            f'          <li><a href="{nav_href(h, lang)}">{html.escape(ft(label, lang))}</a></li>' for label, h in links
        )
        cols.append(f"""      <div class="footer-col">
        <h4>{html.escape(ft(title, lang))}</h4>
        <ul>
{items}
        </ul>
      </div>""")
    return "\n".join(cols)


def footer_offices(lang: str) -> str:
    return "\n".join(
        f'          <li><a href="{nav_href(path, lang)}">{PIN_SVG}{html.escape(label)}</a></li>'
        for label, path in OFFICES
    )


def site_footer_html(prefix: str = "", lang: str = "en", current_path: str = "", switcher: str | None = None) -> str:
    p = prefix
    if switcher is None:
        switcher = language_switcher_html(current_path, lang, variant="footer")
    contact = page_href_lang("contact.html", lang)
    return f"""
<footer class="footer">
  <div class="footer-mesh"></div>
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <div style="display:flex;align-items:center;gap:11px;margin-bottom:14px">
          <img src="{p}assets/yb-logo-white.png" alt="YB" style="width:44px;height:44px;filter:drop-shadow(0 0 3px rgba(255,255,255,.4))">
          <span style="font-family:var(--font-display);font-weight:800;font-size:22px;color:#fff">YB <span style="color:var(--yb-cyan)">Marketing</span></span>
        </div>
        <p>{ft(FOOTER_BLURB, lang)}</p>
        <div class="footer-socials">
          <a href="https://www.facebook.com/yakimabranding" class="social-btn" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor" width="17" height="17"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
          <a href="https://www.instagram.com/yb.marketing_/" class="social-btn" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="17" height="17"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".5" fill="currentColor"/></svg></a>
          <a href="https://www.linkedin.com/company/18939370" class="social-btn" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" width="17" height="17"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></a>
        </div>
      </div>
      <div class="footer-col footer-contact">
        <h4>{ft("Get in Touch", lang)}</h4>
        <ul>
          <li><a href="tel:5099019735">{PHONE_SVG}(509) 901-9735</a></li>
          <li><a href="mailto:info@yakimabranding.com">{MAIL_SVG}info@yakimabranding.com</a></li>
          <li><a href="{contact}">{ARROW_SVG}{ft("Let's get in touch", lang)}</a></li>
        </ul>
      </div>
      <div class="footer-col footer-contact">
        <h4>{ft("Our Locations", lang)}</h4>
        <ul>
{footer_offices(lang)}
        </ul>
      </div>
    </div>
    <div class="footer-links">
{footer_link_columns(lang)}
    </div>
    <div class="footer-bottom">
      <span>© 2026 YB Marketing. {t("All rights reserved.", lang)}</span>
      <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap">
        {switcher}
        <a href="{page_href_lang('privacy-policy.html', lang)}">{t("Privacy Policy", lang)}</a>
        <a href="{page_href_lang('sitemap.html', lang)}">{t("Sitemap", lang)}</a>
      </div>
    </div>
  </div>
</footer>"""
