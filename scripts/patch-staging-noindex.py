#!/usr/bin/env python3
"""DEPRECATED staging helper — do not run on production.

Previously injected noindex/nofollow across the site for staging.
Production pages are indexable; thank-you pages keep noindex via
THANK_YOU_ROBOTS_META in site_staging_seo_snippet.py.
"""

raise SystemExit(
    "patch-staging-noindex.py is disabled for production. "
    "Public pages should be indexable; thank-you pages use THANK_YOU_ROBOTS_META."
)
