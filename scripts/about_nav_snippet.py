"""Shared About dropdown HTML for site nav."""

from typing import Optional

from site_urls import page_href


def about_nav_dropdown(prefix: str, active: Optional[str] = None) -> str:
    """active: 'about' | 'tax' | 'case-studies' | None"""
    _ = prefix
    about_cls = " is-active" if active == "about" else ""
    tax_cls = " is-active" if active == "tax" else ""
    cases_cls = " is-active" if active == "case-studies" else ""
    return f"""        <div class="nav-dd nav-dd-about">
          <div class="nav-dd-arrow"></div>
          <div class="nav-dd-about-inner">
            <div class="nav-dd-about-banner">
              <span class="nav-dd-eyebrow">About YB Marketing</span>
              <p class="nav-dd-banner-text">Pacific Northwest agency · Washington State</p>
            </div>
            <div class="nav-dd-about-grid">
              <a href="{page_href('about.html')}" class="dd-card{about_cls}">
                <div class="dd-ic" style="background:var(--wash-blue);color:var(--yb-blue)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div>
                <div><span class="dd-name">About Us</span><span class="dd-desc">Meet our team &amp; our story</span></div>
              </a>
              <a href="{page_href('about/case-studies/index.html')}" class="dd-card{cases_cls}">
                <div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>
                <div><span class="dd-name">Case Studies</span><span class="dd-desc">Enterprise accessibility &amp; security work</span></div>
              </a>
              <a href="{page_href('washington-state-sales-tax.html')}" class="dd-card{tax_cls}">
                <div class="dd-ic" style="background:#e8f5ee;color:#2d9a5a"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
                <div><span class="dd-name">WA Sales Tax Notice</span><span class="dd-desc">Oct 2025 advertising &amp; software tax info</span></div>
              </a>
            </div>
          </div>
        </div>"""


def about_nav_shell(prefix: str, active: Optional[str] = None, btn_style: str = "") -> str:
    style_attr = f' style="{btn_style}"' if btn_style else ""
    return f"""      <div class="nav-about" id="navAbout">
        <button class="nav-svc-btn" type="button"{style_attr}>About
          <svg class="nav-chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
{about_nav_dropdown(prefix, active)}
      </div>"""
