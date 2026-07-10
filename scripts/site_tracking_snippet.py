"""Sitewide tracking widgets and tags (head, GTM body, footer).

Tracking scripts are consent-gated via /js/cookie-consent.js and only load
after the visitor accepts cookies (California opt-in pattern).
"""

TRACKING_HEAD_START = "<!-- yb-tracking-head-start -->"
TRACKING_HEAD_END = "<!-- yb-tracking-head-end -->"
GTM_BODY_START = "<!-- yb-gtm-body-start -->"
GTM_BODY_END = "<!-- yb-gtm-body-end -->"
ATTRIBUTER_START = "<!-- yb-attributer-start -->"
ATTRIBUTER_END = "<!-- yb-attributer-end -->"

TRACKING_HEAD_BLOCK = f"""{TRACKING_HEAD_START}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap"></noscript>
<link rel="stylesheet" href="/cookie-consent.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="/cookie-consent.css"></noscript>
<script src="/js/cookie-consent.js" defer></script>
{TRACKING_HEAD_END}"""

# GTM noscript is injected by cookie-consent.js after acceptance.
GTM_BODY_NOSCRIPT_BLOCK = f"""{GTM_BODY_START}
{GTM_BODY_END}"""

# Attributer loads after cookie consent.
ATTRIBUTER_FOOTER_BLOCK = f"""{ATTRIBUTER_START}
{ATTRIBUTER_END}"""
