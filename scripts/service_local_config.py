"""Service-specific config for localized landing pages."""

PROCESS_STEPS = {
    "web-design": [
        (
            "DISCOVERY & SITE REVIEW",
            "We learn how your business works, review your current site, and identify what is helping or hurting conversions.",
        ),
        (
            "CUSTOM DESIGN & BUILD PLAN",
            "Together we define structure, messaging, and functionality so your site supports sales, service, and search.",
        ),
        (
            "LAUNCH A SITE THAT CONVERTS",
            "From mobile performance to clear calls-to-action, we deliver a polished site built to earn trust and generate inquiries.",
        ),
    ],
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
    "social-media": [
        (
            "CHANNEL & COMPETITOR AUDIT",
            "We review your profiles, content, and competitors to find quick wins and long-term opportunities.",
        ),
        (
            "CONTENT CALENDAR & BRAND VOICE",
            "Together we plan posts, reels, and campaigns that stay on-brand and speak directly to your ideal customers.",
        ),
        (
            "GROW REACH & ENGAGEMENT",
            "With consistent publishing, community management, and paid boost when it makes sense, we help your brand stay top of mind.",
        ),
    ],
    "branding": [
        (
            "DISCOVERY & BRAND VISIONING",
            "We learn your story, audience, and differentiators — through research, journey mapping, and conversations with you and your clients.",
        ),
        (
            "STRATEGY & DESIGN SYSTEM",
            "Together we define your brand story, logo, typography, color, and graphic standards — a flexible system your team can use with confidence.",
        ),
        (
            "LAUNCH A COHESIVE BRAND",
            "From logo guides to print, packaging, signage, and web — we deliver assets that look and feel like family everywhere your brand appears.",
        ),
    ],
}

SERVICE_CONFIGS = {
    "web-design": {
        "export_name": "webDesignLocations",
        "data_file": "webDesignLocations.js",
        "folder": "web-design",
        "parent_href": "/web-design",
        "parent_name": "Web Design",
        "service_label": "Web Design",
        "accent": "#159468",
        "wash": "var(--wash-mint)",
        "hub_image": "svc-hub-web-design.webp",
        "orbit_style": "--orbit-feat-wash:var(--wash-mint);--orbit-feat-color:#159468;--orbit-feat-glow:rgba(21,148,104,0.22)",
        "why_eyebrow": "Why YB for Web Design",
        "process_title": "How We Build Your Site",
        "cta_heading": "Let's Build Your Website",
        "cta_sub": "Schedule a free consultation and let our team build a custom website strategy for your business.",
        "layout": "web-design",
        "features_partial": "wd-features.html",
        "platforms_partial": "wd-platforms.html",
    },
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
    "social-media": {
        "export_name": "socialMediaLocations",
        "data_file": "socialMediaLocations.js",
        "folder": "social-media",
        "parent_href": "/social-media",
        "parent_name": "Social Media",
        "service_label": "Social Media",
        "accent": "#c77f12",
        "wash": "var(--wash-amber)",
        "hub_image": "svc-hub-social.webp",
        "orbit_style": "--orbit-feat-wash:var(--wash-amber);--orbit-feat-color:#c77f12;--orbit-feat-glow:rgba(199,127,18,0.22)",
        "why_eyebrow": "Why YB for Social Media",
        "process_title": "How We Grow Your Social Presence",
        "cta_heading": "Let's Talk About Your Goals",
        "cta_sub": "Schedule a free consultation and let our team build a custom social media strategy for your business.",
        "layout": "social-media",
        "features_partial": "sm-features.html",
        "platforms_partial": "sm-platforms.html",
    },
    "branding": {
        "export_name": "brandingLocations",
        "data_file": "brandingLocations.js",
        "folder": "branding",
        "parent_href": "/branding",
        "parent_name": "Branding",
        "service_label": "Branding",
        "accent": "var(--yb-violet)",
        "wash": "var(--wash-violet)",
        "hub_image": "svc-hub-branding.webp",
        "orbit_style": "--orbit-feat-wash:var(--wash-violet);--orbit-feat-color:var(--yb-violet);--orbit-feat-glow:rgba(123,91,230,0.22)",
        "why_eyebrow": "Why YB for Branding",
        "process_title": "How We Build Your Brand",
        "cta_heading": "Let's Build Your Brand Identity",
        "cta_sub": "Schedule a free consultation and let's discuss strategy, story, and design for your business.",
        "layout": "branding",
        "accordion_partial": "br-accordion.html",
    },
}
