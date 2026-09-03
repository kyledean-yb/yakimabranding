"""Shared Insights dropdown HTML for site nav."""

from typing import Optional

from site_i18n import page_href_lang, t


def insights_nav_dropdown(prefix: str, active: Optional[str] = None, lang: str = "en") -> str:
    """active: 'blog' | 'client-corner' | 'crm-tutorials' | None"""
    _ = prefix
    blog_cls = " is-active" if active == "blog" else ""
    corner_cls = " is-active" if active == "client-corner" else ""
    crm_cls = " is-active" if active == "crm-tutorials" else ""
    return f"""        <div class="nav-dd nav-dd-about">
          <div class="nav-dd-arrow"></div>
          <div class="nav-dd-about-inner">
            <div class="nav-dd-about-banner">
              <span class="nav-dd-eyebrow">{t("YB Marketing Insights", lang)}</span>
              <p class="nav-dd-banner-text">{t("Articles, Marketing Minute & CRM guides", lang)}</p>
            </div>
            <div class="nav-dd-about-grid">
              <a href="{page_href_lang('insights.html', lang)}" class="dd-card{blog_cls}">
                <div class="dd-ic" style="background:var(--wash-cyan);color:var(--yb-cyan)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>
                <div><span class="dd-name">{t("Blog", lang)}</span><span class="dd-desc">{t("Marketing tips & articles", lang)}</span></div>
              </a>
              <a href="{page_href_lang('client-corner/index.html', lang)}" class="dd-card{corner_cls}">
                <div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg></div>
                <div><span class="dd-name">{t("Client Corner", lang)}</span><span class="dd-desc">{t("Resources & Marketing Minute", lang)}</span></div>
              </a>
              <a href="{page_href_lang('crm-tutorials/index.html', lang)}" class="dd-card{crm_cls}">
                <div class="dd-ic" style="background:var(--wash-blue);color:var(--yb-blue)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg></div>
                <div><span class="dd-name">{t("CRM Tutorials", lang)}</span><span class="dd-desc">{t("How-to videos for your CRM", lang)}</span></div>
              </a>
            </div>
          </div>
        </div>"""


def insights_nav_shell(
    prefix: str,
    active: Optional[str] = None,
    btn_style: str = "",
    lang: str = "en",
) -> str:
    style_attr = f' style="{btn_style}"' if btn_style else ""
    return f"""      <div class="nav-insights" id="navInsights">
        <button class="nav-svc-btn" type="button"{style_attr}>{t("Insights", lang)}
          <svg class="nav-chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
{insights_nav_dropdown(prefix, active, lang)}
      </div>"""


def insights_mobile_block(lang: str = "en") -> str:
    return f"""    <a href="#" onclick="document.getElementById('mobileInsightsList').classList.toggle('open');return false" style="display:flex;justify-content:space-between;align-items:center">{t("Insights", lang)} <span>▾</span></a>
    <div class="mobile-svc-list" id="mobileInsightsList">
      <a href="{page_href_lang('insights.html', lang)}" class="mobile-about-row"><strong>{t("Blog", lang)}</strong><span>{t("Marketing tips & articles", lang)}</span></a>
      <a href="{page_href_lang('client-corner/index.html', lang)}" class="mobile-about-row"><strong>{t("Client Corner", lang)}</strong><span>{t("Resources & Marketing Minute", lang)}</span></a>
      <a href="{page_href_lang('crm-tutorials/index.html', lang)}" class="mobile-about-row"><strong>{t("CRM Tutorials", lang)}</strong><span>{t("How-to videos for your CRM", lang)}</span></a>
    </div>"""
