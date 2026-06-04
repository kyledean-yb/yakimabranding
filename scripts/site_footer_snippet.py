"""Site footer markup (matches index.html)."""


def site_footer_html(prefix: str = "") -> str:
    p = prefix
    return f"""
<footer class="footer">
  <div class="footer-mesh"></div>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div style="display:flex;align-items:center;gap:11px;margin-bottom:14px">
          <img src="{p}assets/yb-logo-white.png" alt="YB" style="width:44px;height:44px;filter:drop-shadow(0 0 3px rgba(255,255,255,.4))">
          <span style="font-family:var(--font-display);font-weight:800;font-size:22px;color:#fff">YB <span style="color:var(--yb-cyan)">Marketing</span></span>
        </div>
        <p>Award-winning digital marketing agency helping businesses grow through strategic branding, SEO, and comprehensive digital solutions.</p>
        <div style="display:grid;gap:9px;margin:16px 0">
          <a href="tel:5099019735" style="color:var(--fg2-on-dark);font-size:14px;display:flex;align-items:center;gap:9px"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--yb-cyan)" stroke-width="2.2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>(509) 901-9735</a>
          <a href="mailto:info@yakimabranding.com" style="color:var(--fg2-on-dark);font-size:14px;display:flex;align-items:center;gap:9px"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--yb-cyan)" stroke-width="2" stroke-linecap="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>info@yakimabranding.com</a>
        </div>
        <div class="footer-socials">
          <a href="https://www.facebook.com/yakimabranding" class="social-btn" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" width="17" height="17"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
          <a href="https://www.instagram.com/yb.marketing_/" class="social-btn" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="17" height="17"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".5" fill="currentColor"/></svg></a>
          <a href="https://www.linkedin.com/company/18939370" class="social-btn" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" width="17" height="17"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Navigation</h4>
        <ul>
          <li><a href="{p}index.html">Home</a></li>
          <li><a href="{p}about.html">About</a></li>
          <li><a href="{p}index.html#services">Services</a></li>
          <li><a href="{p}insights.html">Insights</a></li>
          <li><a href="{p}contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <ul>
          <li><a href="{p}services/branding.html">Branding &amp; Design</a></li>
          <li><a href="{p}services/web-design.html">Web Design</a></li>
          <li><a href="{p}services/seo.html">SEO Optimization</a></li>
          <li><a href="{p}services/google-ads.html">Google Ads</a></li>
          <li><a href="{p}services/social-media.html">Social Media</a></li>
          <li><a href="{p}services/press-releases.html">Press Releases</a></li>
          <li><a href="{p}services/content-creation.html">Content Marketing</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Our Reach</h4>
        <p style="color:var(--fg2-on-dark);font-size:14px;line-height:1.7;margin-bottom:14px">Yakima Branding is centered in Central Washington, with deep roots in the Yakima community. From our home base in Yakima, we proudly serve businesses across the entire Pacific Northwest with strategic marketing, website design, SEO, advertising, and branding support.</p>
        <div style="display:flex;align-items:center;gap:7px;font-size:13px;color:var(--yb-cyan);font-weight:600"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--yb-cyan)" stroke-width="2.2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>Yakima, WA &nbsp;·&nbsp; Pacific Northwest</div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 YB Marketing. All rights reserved.</span>
      <div style="display:flex;gap:18px"><a href="#">Privacy Policy</a><a href="#">Sitemap</a></div>
    </div>
  </div>
</footer>"""
