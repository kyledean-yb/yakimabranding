"""Service-specific config for localized landing pages."""

PROCESS_STEPS = {
    "google-ads": [
        (
            "ACCOUNT & LANDING PAGE AUDIT",
            "We review your ad account, keywords, tracking, and landing pages to find waste and missed opportunities.",
        ),
        (
            "CAMPAIGN STRATEGY & SETUP",
            "Together we define targeting, ad copy, budgets, and conversion goals tailored to how you actually sell.",
        ),
        (
            "OPTIMIZE FOR MORE LEADS",
            "With ongoing bid management, testing, and reporting, we refine campaigns to lower cost per lead and scale what works.",
        ),
    ],
}

SERVICE_CONFIGS = {
    "google-ads": {
        "export_name": "googleAdsLocations",
        "data_file": "googleAdsLocations.js",
        "folder": "google-ads",
        "parent_href": "/google-ads",
        "parent_name": "Google Ads",
        "service_label": "Google Ads",
        "accent": "#FF6B57",
        "wash": "var(--wash-coral)",
        "hub_image": "svc-hub-google-ads.webp",
        "orbit_style": "--orbit-feat-wash:var(--wash-coral);--orbit-feat-color:var(--yb-coral);--orbit-feat-glow:rgba(255,107,87,0.22)",
        "why_eyebrow": "Why YB for Google Ads",
        "process_title": "How We Manage Your Campaigns",
        "cta_heading": "Let's Talk About Your Goals",
        "cta_sub": "Schedule a free consultation and let our team build a custom Google Ads strategy for your business.",
        "layout": "google-ads",
        "included_partial": "ga-included.html",
        "perfmax_partial": "ga-perfmax-seovsppc.html",
    },
}
