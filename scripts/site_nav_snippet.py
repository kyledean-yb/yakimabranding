"""Full site header nav (matches insights.html / about.html)."""

from typing import Optional

from about_nav_snippet import about_nav_shell
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
  <div class="container header-inner">
    <a class="logo" href="{page_href_lang('index.html', lang)}">
      <img src="{prefix}assets/yb-logo-color.png" alt="YB Marketing logo" style="width:44px;height:44px">
      <span class="logo-text">YB <span>Marketing</span></span>
    </a>
    <nav class="nav">
      <a href="{page_href_lang('index.html', lang)}" class="nav-a">{t("Home", lang)}</a>
      {about_nav_shell(prefix, about_active, about_btn_style, lang)}
      <div class="nav-services" id="navServices">
        <button class="nav-svc-btn" type="button">{t("Services", lang)}
          <svg class="nav-chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="nav-dd">
          <div class="nav-dd-arrow"></div>
          <div class="nav-dd-grid">
            <a href="{page_href_lang('services/branding.html', lang)}" class="dd-card"><div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r="0.5" fill="currentColor"/><circle cx="17.5" cy="10.5" r="0.5" fill="currentColor"/><circle cx="8.5" cy="7.5" r="0.5" fill="currentColor"/><circle cx="6.5" cy="12.5" r="0.5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg></div><div><span class="dd-name">{t("Branding & Design", lang)}</span><span class="dd-desc">{t("Logos, systems & identity", lang)}</span></div></a>
            <a href="{page_href_lang('services/web-design.html', lang)}" class="dd-card"><div class="dd-ic" style="background:var(--wash-mint);color:#159468"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg></div><div><span class="dd-name">{t("Web Design", lang)}</span><span class="dd-desc">{t("WordPress, Wix & custom sites", lang)}</span></div></a>
            <a href="{page_href_lang('services/social-media.html', lang)}" class="dd-card"><div class="dd-ic" style="background:var(--wash-amber);color:#c77f12"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/></svg></div><div><span class="dd-name">{t("Social Media", lang)}</span><span class="dd-desc">{t("Grow your following", lang)}</span></div></a>
            <a href="{page_href_lang('services/google-ads.html', lang)}" class="dd-card"><div class="dd-ic" style="background:var(--wash-coral);color:var(--yb-coral)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg></div><div><span class="dd-name">{t("Google Ads", lang)}</span><span class="dd-desc">{t("PPC that converts", lang)}</span></div></a>
            <a href="{page_href_lang('services/seo.html', lang)}" class="dd-card"><div class="dd-ic" style="background:var(--wash-cyan);color:var(--yb-cyan)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div><div><span class="dd-name">{t("SEO", lang)}</span><span class="dd-desc">{t("Rank higher on Google", lang)}</span></div></a>
            <a href="{page_href_lang('services/press-releases.html', lang)}" class="dd-card"><div class="dd-ic" style="background:var(--wash-pink);color:var(--yb-pink)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2z"/></svg></div><div><span class="dd-name">{t("Press Releases", lang)}</span><span class="dd-desc">{t("Get published", lang)}</span></div></a>
            <a href="{page_href_lang('services/content-creation.html', lang)}" class="dd-card"><div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></div><div><span class="dd-name">{t("Content & Blogging", lang)}</span><span class="dd-desc">{t("Copy that converts", lang)}</span></div></a>
          </div>
        </div>
      </div>
      <a href="{page_href_lang('insights.html', lang)}" class="nav-a">{t("Insights", lang)}</a>
      <a href="{page_href_lang('contact.html', lang)}" class="nav-a">{t("Contact", lang)}</a>
    </nav>
    <div class="btn-hdr" style="display:flex;align-items:center;gap:8px">
      {switcher}
      <a href="tel:5099019735" class="btn btn-hdr-phone">{PHONE_ICON_SVG}509-901-9735</a>
      <a href="{page_href_lang('contact.html', lang)}" class="btn btn-grad">{t("Get Started", lang)}</a>
    </div>
    <button class="hamburger" id="hamburger" type="button" aria-label="{t("Open menu", lang)}"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    <a href="{page_href_lang('index.html', lang)}">{t("Home", lang)}</a>
    <a href="#" onclick="document.getElementById('mobileAboutList').classList.toggle('open');return false" style="display:flex;justify-content:space-between;align-items:center">{t("About", lang)} <span>▾</span></a>
    <div class="mobile-svc-list" id="mobileAboutList">
      <a href="{page_href_lang('about.html', lang)}" class="mobile-about-row"><strong>{t("About Us", lang)}</strong><span>{t("Meet our team & our story", lang)}</span></a>
      <a href="{page_href_lang('about/case-studies/index.html', lang)}" class="mobile-about-row"><strong>{t("Case Studies", lang)}</strong><span>{t("Client results & project highlights", lang)}</span></a>
      <a href="{page_href_lang('washington-state-sales-tax.html', lang)}" class="mobile-about-row"><strong>{t("WA Sales Tax Notice", lang)}</strong><span>{t("Oct 2025 tax updates", lang)}</span></a>
    </div>
    <a href="{page_href_lang('insights.html', lang)}">{t("Insights", lang)}</a>
    <a href="{page_href_lang('contact.html', lang)}">{t("Contact", lang)}</a>
    <div class="mobile-menu-lang">{switcher}</div>
  </div>
</div>"""
