#!/usr/bin/env python3
"""Generate privacy-policy.html from yakimabranding.com privacy policy copy."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_footer_snippet import site_footer_html
from site_nav_snippet import site_header_html
from site_staging_seo_snippet import STAGING_ROBOTS_META

PREFIX = ""
header = site_header_html(PREFIX).strip()
footer = site_footer_html(PREFIX).strip()
schema_head = seo_head_html("privacy-policy.html")

CONTENT = """
      <section class="news-block">
        <h2>What information do we collect?</h2>
        <p>We collect information from you when you register on our site, subscribe to our newsletter, visit our site, or fill out a form.</p>
        <p>When registering on our site you may be asked to enter your name, e-mail address, mailing address, or phone number.</p>
      </section>

      <section class="news-block">
        <h2>What do we use your information for?</h2>
        <p>Any of the information we collect from you may be used in one of the following ways:</p>
        <ul>
          <li>To personalize your experience (your information helps us to better respond to your individual needs)</li>
          <li>To improve our website (we continually strive to improve our website offerings based on the information and feedback we receive from you)</li>
          <li>To improve customer service (your information helps us to more effectively respond to your customer service requests and support needs)</li>
          <li>To send periodic emails</li>
        </ul>
        <p>The email address you provide for order processing will only be used to send you information and updates pertaining to your order.</p>
        <p>If you decide to opt-in to our mailing list, you will receive emails that may include company news, updates, related product or service information, etc.</p>
        <p><strong>Note:</strong> If at any time you would like to unsubscribe from receiving future emails, we include detailed unsubscribe instructions at the bottom of each email.</p>
      </section>

      <section class="news-block">
        <h2>Do we use cookies?</h2>
        <p>Yes. Cookies are small files that a site or its service provider transfers to your computer&rsquo;s hard drive through your web browser (if you allow) that enable the site or service provider&rsquo;s systems to recognize your browser and capture and remember certain information.</p>
        <p>We use cookies to compile aggregate data about site traffic and site interaction so that we can offer better site experiences and tools in the future.</p>
        <p>When you visit or log in to our website, cookies and similar technologies may be used by our online data partners or vendors to associate these activities with other personal information they or others have about you, including by association with your email or home address. We (or service providers on our behalf) may then send communications and marketing to these email or home addresses. You may opt out of receiving this advertising by visiting <a href="https://app.retention.com/optout" target="_blank" rel="noopener noreferrer">https://app.retention.com/optout</a>.</p>
      </section>

      <section class="news-block">
        <h2>Do we disclose any information to outside parties?</h2>
        <p>We do not sell, trade, or otherwise transfer to outside parties your personally identifiable information. This does not include trusted third parties who assist us in operating our website, conducting our business, or servicing you, so long as those parties agree to keep this information confidential. We may also release your information when we believe release is appropriate to comply with the law, enforce our site policies, or protect ours or others&rsquo; rights, property, or safety. However, non-personally identifiable visitor information may be provided to other parties for marketing, advertising, or other uses.</p>
        <p>No mobile information will be shared with third parties/affiliates for marketing/promotional purposes. All the above categories exclude text messaging originator opt-in data and consent; this information will not be shared with any third parties.</p>
      </section>

      <section class="news-block">
        <h2>Online Privacy Policy Only</h2>
        <p>This online privacy policy applies only to information collected through our website and not to information collected offline.</p>
      </section>

      <section class="news-block">
        <h2>Your Consent</h2>
        <p>By using our site, you consent to our privacy policy.</p>
      </section>

      <section class="news-block">
        <h2>Changes to Our Privacy Policy</h2>
        <p>If we decide to change our privacy policy, we will post those changes on this page, and/or update the Privacy Policy modification date below.</p>
        <p>This policy was last modified on <strong>January 1, 2024</strong>.</p>
      </section>

      <section class="news-block">
        <h2>Contacting Us</h2>
        <p>If there are any questions regarding this privacy policy, you may contact us using the information below.</p>
        <p><strong>Corporate Office</strong><br>
        85 Bassett St.<br>
        San Jose, CA 95110<br>
        Phone: <a href="tel:5106879737">510-687-9737</a></p>
        <p><strong>Headquarters</strong><br>
        Yakima, WA: <a href="tel:5099019735">(509) 901-9735</a><br>
        Scottsdale, AZ: <a href="tel:5106879737">(510) 687-9737</a><br>
        Toll Free: <a href="tel:8773171960">(877) 317-1960</a></p>
        <p>Email: <a href="mailto:info@yakimabranding.com">info@yakimabranding.com</a></p>
      </section>
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{STAGING_ROBOTS_META}
<link rel="icon" href="{PREFIX}favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{PREFIX}favicon.png">
<title>Privacy Policy — YB Marketing</title>
<meta name="description" content="YB Marketing privacy policy — how we collect, use, and protect your information when you visit our website or contact us.">
<link rel="canonical" href="https://yakimabranding.com/privacy-policy">
<link rel="stylesheet" href="{PREFIX}colors_and_type.css">
<link rel="stylesheet" href="{PREFIX}site.css">
<link rel="stylesheet" href="{PREFIX}news-page.css">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font-body);background:var(--bg);color:var(--fg1);-webkit-font-smoothing:antialiased;overflow-x:hidden}}
a{{color:inherit;text-decoration:none}}
.news-content a{{color:var(--yb-blue);font-weight:600;text-decoration:underline;text-underline-offset:2px}}
.news-content a:hover{{color:var(--ink)}}
.news-content ul{{margin:12px 0 16px 1.25rem;display:grid;gap:8px}}
.news-content li{{color:var(--fg2);line-height:1.7;font-size:16px}}
</style>
{schema_head}
</head>
<body>
{ACCESSIBE_BODY_SCRIPT}

{header}

<main class="news-page">
  <header class="news-hero">
    <div class="news-hero-mesh" aria-hidden="true"></div>
    <div class="hero-logo-overlay hero-logo-overlay--left" aria-hidden="true">
      <img src="{PREFIX}assets/yb-logo-white.png" alt="">
    </div>
    <div class="container news-hero-inner">
      <span class="eyebrow">Legal</span>
      <h1 class="news-title">Privacy Policy</h1>
    </div>
  </header>

  <div class="news-body">
    <div class="container news-content">
{CONTENT}
    </div>
  </div>
</main>

{footer}

<script src="{PREFIX}js/newsletter-popup.js" defer></script>
<script src="{PREFIX}js/site.js" defer></script>
</body>
</html>
"""

def main() -> None:
    out = ROOT / "privacy-policy.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
