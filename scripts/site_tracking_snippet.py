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
<link rel="stylesheet" href="/cookie-consent.css">
<script src="/js/cookie-consent.js"></script>
{TRACKING_HEAD_END}"""

# GTM noscript is injected by cookie-consent.js after acceptance.
GTM_BODY_NOSCRIPT_BLOCK = f"""{GTM_BODY_START}
{GTM_BODY_END}"""

# Attributer loads after cookie consent.
ATTRIBUTER_FOOTER_BLOCK = f"""{ATTRIBUTER_START}
{ATTRIBUTER_END}"""
