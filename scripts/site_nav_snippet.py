"""Full site header nav (matches insights.html / about.html)."""

from typing import Optional

from mega_nav import desktop_nav_html, mobile_menu_items_html
from site_i18n import language_switcher_html, page_href_lang, t

PHONE_ICON_SVG = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 '
    '19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 '
    '0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 '
    '16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/>'
    '</svg>'
)


def site_header_html(
    prefix: str = "",
    about_active: Optional[str] = None,
    lang: str = "en",
    current_path: str = "",
) -> str:
    """about_active: 'about' | 'tax' | 'case-studies' | None — highlights About dropdown item.
    current_path: clean URL path without /es prefix ('' for home).
    """
    about_btn_style = "color:var(--yb-blue)" if about_active in ("about", "case-studies") else ""
    switcher = language_switcher_html(current_path, lang, variant="header")
    return f"""
<div class="header top" id="header">
  <div class="header-topbar"><div class="container header-topbar-inner"><div class="header-topbar-actions">
      {switcher}
      <a href="tel:5099019735" class="btn btn-hdr-phone">{PHONE_ICON_SVG}509-901-9735</a>
      <a href="{page_href_lang('contact.html', lang)}" class="btn btn-grad">{t("Get Started", lang)}</a>
  </div></div></div>
  <div class="container header-inner">
    <a class="logo" href="{page_href_lang('index.html', lang)}">
      <img src="{prefix}assets/yb-logo-color.png" alt="YB Marketing logo" style="width:44px;height:44px">
      <span class="logo-text">YB <span>Marketing</span></span>
    </a>
    {desktop_nav_html(lang)}
    <button class="hamburger" id="hamburger" type="button" aria-label="{t("Open menu", lang)}"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
  </div>
  <div class="mobile-menu" id="mobileMenu">
{mobile_menu_items_html(lang)}
    <div class="mobile-menu-lang">{switcher}</div>
  </div>
</div>"""
