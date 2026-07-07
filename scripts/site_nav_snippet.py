"""Full site header nav (matches insights.html / about.html)."""

from typing import Optional

from about_nav_snippet import about_nav_shell
from site_urls import page_href

PHONE_ICON_SVG = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 '
    '19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 '
    '0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 '
    '16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/>'
    '</svg>'
)

def site_header_html(prefix: str = "", about_active: Optional[str] = None) -> str:
    """about_active: 'about' | 'tax' | 'case-studies' | None — highlights About dropdown item."""
    about_btn_style = "color:var(--yb-blue)" if about_active in ("about", "case-studies") else ""
    return f"""
<div class="header top" id="header">
  <div class="container header-inner">
    <a class="logo" href="{page_href('index.html')}">
      <img src="{prefix}assets/yb-logo-color.png" alt="YB Marketing logo" style="width:44px;height:44px">
      <span class="logo-text">YB <span>Marketing</span></span>
    </a>
    <nav class="nav">
      <a href="{page_href('index.html')}" class="nav-a">Home</a>
      {about_nav_shell(prefix, about_active, about_btn_style)}
      <div class="nav-services" id="navServices">
        <button class="nav-svc-btn" type="button">Services
          <svg class="nav-chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="nav-dd">
          <div class="nav-dd-arrow"></div>
          <div class="nav-dd-grid">
            <a href="{page_href('services/branding.html')}" class="dd-card"><div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r="0.5" fill="currentColor"/><circle cx="17.5" cy="10.5" r="0.5" fill="currentColor"/><circle cx="8.5" cy="7.5" r="0.5" fill="currentColor"/><circle cx="6.5" cy="12.5" r="0.5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg></div><div><span class="dd-name">Branding &amp; Design</span><span class="dd-desc">Logos, systems &amp; identity</span></div></a>
            <a href="{page_href('services/web-design.html')}" class="dd-card"><div class="dd-ic" style="background:var(--wash-mint);color:#159468"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg></div><div><span class="dd-name">Web Design</span><span class="dd-desc">WordPress, Wix &amp; custom sites</span></div></a>
            <a href="{page_href('services/social-media.html')}" class="dd-card"><div class="dd-ic" style="background:var(--wash-amber);color:#c77f12"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/></svg></div><div><span class="dd-name">Social Media</span><span class="dd-desc">Grow your following</span></div></a>
            <a href="{page_href('services/google-ads.html')}" class="dd-card"><div class="dd-ic" style="background:var(--wash-coral);color:var(--yb-coral)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg></div><div><span class="dd-name">Google Ads</span><span class="dd-desc">PPC that converts</span></div></a>
            <a href="{page_href('services/seo.html')}" class="dd-card"><div class="dd-ic" style="background:var(--wash-cyan);color:var(--yb-cyan)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div><div><span class="dd-name">SEO</span><span class="dd-desc">Rank higher on Google</span></div></a>
            <a href="{page_href('services/press-releases.html')}" class="dd-card"><div class="dd-ic" style="background:var(--wash-pink);color:var(--yb-pink)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2z"/></svg></div><div><span class="dd-name">Press Releases</span><span class="dd-desc">Get published</span></div></a>
            <a href="{page_href('services/content-creation.html')}" class="dd-card"><div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></div><div><span class="dd-name">Content &amp; Blogging</span><span class="dd-desc">Copy that converts</span></div></a>
          </div>
        </div>
      </div>
      <a href="{page_href('insights.html')}" class="nav-a">Insights</a>
      <a href="{page_href('contact.html')}" class="nav-a">Contact</a>
    </nav>
    <div class="btn-hdr" style="display:flex;align-items:center;gap:8px">
      <a href="tel:5099019735" class="btn btn-hdr-phone">{PHONE_ICON_SVG}509-901-9735</a>
      <a href="{page_href('contact.html')}" class="btn btn-grad">Get Started</a>
    </div>
    <button class="hamburger" id="hamburger" type="button" aria-label="Open menu"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    <a href="{page_href('index.html')}">Home</a>
    <a href="#" onclick="document.getElementById('mobileAboutList').classList.toggle('open');return false" style="display:flex;justify-content:space-between;align-items:center">About <span>▾</span></a>
    <div class="mobile-svc-list" id="mobileAboutList">
      <a href="{page_href('about.html')}" class="mobile-about-row"><strong>About Us</strong><span>Meet our team &amp; our story</span></a>
      <a href="{page_href('about/case-studies/index.html')}" class="mobile-about-row"><strong>Case Studies</strong><span>Client results &amp; project highlights</span></a>
      <a href="{page_href('washington-state-sales-tax.html')}" class="mobile-about-row"><strong>WA Sales Tax Notice</strong><span>Oct 2025 tax updates</span></a>
    </div>
    <a href="{page_href('insights.html')}">Insights</a>
    <a href="{page_href('contact.html')}">Contact</a>
  </div>
</div>"""
