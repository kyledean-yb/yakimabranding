#!/usr/bin/env python3
"""Generate privacy-policy.html from yakimabranding.com privacy policy copy."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_tracking_snippet import ATTRIBUTER_FOOTER_BLOCK, GTM_BODY_NOSCRIPT_BLOCK, TRACKING_HEAD_BLOCK
from site_footer_snippet import site_footer_html
from site_nav_snippet import site_header_html
from site_staging_seo_snippet import STAGING_ROBOTS_META

PREFIX = ""
header = site_header_html(PREFIX).strip()
footer = site_footer_html(PREFIX).strip()
schema_head = seo_head_html("privacy-policy.html")
CONTENT = (ROOT / "partials" / "privacy-policy-body.html").read_text(encoding="utf-8")

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
.privacy-updated{{color:var(--fg3);font-size:14px;margin-bottom:28px}}
.news-block h3{{font-family:var(--font-display);font-size:1.1rem;font-weight:700;color:var(--ink);margin:18px 0 10px}}
.privacy-defs{{display:grid;gap:14px;margin:16px 0 0}}
.privacy-defs dt{{font-weight:700;color:var(--ink);font-size:15px}}
.privacy-defs dd{{margin:4px 0 0;color:var(--fg2);line-height:1.7;font-size:15.5px}}
</style>
{schema_head}
{TRACKING_HEAD_BLOCK}
</head>
<body>
{GTM_BODY_NOSCRIPT_BLOCK}
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
<script src="{PREFIX}js/chat-widget.js" defer></script>
<script src="{PREFIX}js/site.js" defer></script>
{ATTRIBUTER_FOOTER_BLOCK}
</body>
</html>
"""

def main() -> None:
    out = ROOT / "privacy-policy.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
