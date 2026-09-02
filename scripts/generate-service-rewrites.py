#!/usr/bin/env python3
"""One-shot generator for humanized web design, Google Ads, social, and SEO copy."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CITY_META = {
    "yakima-wa": {
        "city": "Yakima",
        "state": "WA",
        "region": "Yakima Valley",
        "localSignals": ["Yakima, WA", "Selah, WA", "Union Gap, WA", "Yakima Valley"],
        "schema_service": "Yakima",
        "schema_seo": "Yakima",
    },
    "ellensburg-wa": {
        "city": "Ellensburg",
        "state": "WA",
        "region": "Kittitas County",
        "localSignals": ["Ellensburg, WA", "Kittitas County", "CWU", "Central Washington"],
        "schema_service": "Ellensburg",
        "schema_seo": "Ellensburg",
    },
    "tri-cities-wa": {
        "city": "Tri-Cities",
        "state": "WA",
        "region": "Columbia Basin",
        "localSignals": ["Kennewick, WA", "Pasco, WA", "Richland, WA", "Columbia Basin"],
        "schema_service": "Kennewick",
        "schema_seo": "Tri-Cities",
    },
    "spokane-wa": {
        "city": "Spokane",
        "state": "WA",
        "region": "Inland Northwest",
        "localSignals": ["Spokane, WA", "Spokane Valley", "Liberty Lake", "Inland Northwest"],
        "schema_service": "Spokane",
        "schema_seo": "Spokane",
    },
    "boise-id": {
        "city": "Boise",
        "state": "ID",
        "region": "Treasure Valley",
        "localSignals": ["Boise, ID", "Meridian, ID", "Nampa, ID", "Treasure Valley"],
        "schema_service": "Boise",
        "schema_seo": "Boise",
    },
    "coeur-dalene-id": {
        "city": "Coeur d'Alene",
        "state": "ID",
        "region": "North Idaho",
        "localSignals": ["Coeur d'Alene, ID", "Post Falls, ID", "Hayden, ID", "North Idaho"],
        "schema_service": "Coeur d'Alene",
        "schema_seo": "Coeur d'Alene",
    },
    "tacoma-wa": {
        "city": "Tacoma",
        "state": "WA",
        "region": "South Sound",
        "localSignals": ["Tacoma, WA", "Lakewood, WA", "Pierce County", "South Sound"],
        "schema_service": "Tacoma",
        "schema_seo": "Tacoma",
    },
    "vancouver-wa": {
        "city": "Vancouver",
        "state": "WA",
        "region": "Clark County",
        "localSignals": ["Vancouver, WA", "Clark County", "Camas, WA", "Ridgefield, WA"],
        "schema_service": "Vancouver",
        "schema_seo": "Vancouver",
    },
    "wenatchee-wa": {
        "city": "Wenatchee",
        "state": "WA",
        "region": "North Central Washington",
        "localSignals": ["Wenatchee, WA", "East Wenatchee, WA", "Leavenworth, WA", "North Central Washington"],
        "schema_service": "Wenatchee",
        "schema_seo": "Wenatchee",
    },
    "walla-walla-wa": {
        "city": "Walla Walla",
        "state": "WA",
        "region": "Wine Country",
        "localSignals": ["Walla Walla, WA", "Wine Country", "Walla Walla County", "Whitman College"],
        "schema_service": "Walla Walla",
        "schema_seo": "Walla Walla",
    },
}

SLUGS = list(CITY_META.keys())

FEATURE_TITLES = [
    "Personalization",
    "Visibility",
    "Spread the Word",
    "Google's Friend",
    "Increase Keywords",
    "Increase Traffic",
]


def js_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def tri_title(service_label: str) -> str:
    return f"{service_label} Tri-Cities WA | Kennewick, Pasco & Richland | YB Marketing"


def render_faqs(faqs: list[tuple[str, str]]) -> str:
    lines = ["    faqs: ["]
    for q, a in faqs:
        lines.append("      {")
        lines.append(f"        q: {js_str(q)},")
        lines.append(f"        a: {js_str(a)},")
        lines.append("      },")
    lines.append("    ],")
    return "\n".join(lines)


def write_web_design():
    parts = ["export const webDesignLocations = ["]
    for slug in SLUGS:
        meta = CITY_META[slug]
        city = meta["city"]
        state = meta["state"]
        loc = WEB_DESIGN[slug]
        tri = slug == "tri-cities-wa"
        title = tri_title("Web Design") if tri else f"Web Design {city} {state} | YB Marketing"
        parts.append("  {")
        parts.append(f"    slug: {js_str(slug)},")
        parts.append("    service: 'web-design',")
        parts.append(f"    city: {js_str(city)},")
        parts.append(f"    state: {js_str(state)},")
        parts.append(f"    region: {js_str(meta['region'])},")
        parts.append(f"    titleTag: {js_str(title)},")
        parts.append(f"    metaDescription: {js_str(loc['metaDescription'])},")
        parts.append(f"    canonicalUrl: 'https://yakimabranding.com/web-design/{slug}',")
        parts.append("    hero: {")
        parts.append("      eyebrow: 'CUSTOM WEB DEVELOPMENT',")
        parts.append(f"      headline: {js_str(loc['hero_headline'])},")
        parts.append(f"      subheadline: {js_str(loc['hero_subheadline'])},")
        parts.append(f"      body: {js_str(loc['hero_body'])},")
        parts.append("    },")
        parts.append("    whatWeDo: {")
        parts.append("      heading: 'Custom Website Development',")
        parts.append(f"      intro: {js_str(loc['intro'])},")
        parts.append(f"      localParagraph: {js_str(loc['localParagraph'])},")
        parts.append("    },")
        parts.append("    whyYb: {")
        parts.append(f"      heading: {js_str(loc['why_heading'])},")
        parts.append(f"      body: {js_str(loc['why_body'])},")
        parts.append("    },")
        signals = ", ".join(js_str(s) for s in meta["localSignals"])
        parts.append(f"    localSignals: [{signals}],")
        parts.append(render_faqs(loc["faqs"]))
        parts.append("    schema: {")
        parts.append("      service: 'Web Design',")
        parts.append(f"      addressLocality: {js_str(meta['schema_service'])},")
        parts.append(f"      addressRegion: {js_str(state)},")
        parts.append("      addressCountry: 'US',")
        parts.append("    },")
        parts.append("  },")
    parts.append("];")
    parts.append("")
    (ROOT / "data" / "webDesignLocations.js").write_text("\n".join(parts), encoding="utf-8")


def write_google_ads():
    parts = ["export const googleAdsLocations = ["]
    for slug in SLUGS:
        meta = CITY_META[slug]
        city = meta["city"]
        state = meta["state"]
        loc = GOOGLE_ADS[slug]
        tri = slug == "tri-cities-wa"
        title = tri_title("Google Ads Management") if tri else f"Google Ads Management {city} {state} | YB Marketing"
        parts.append("  {")
        parts.append(f"    slug: {js_str(slug)},")
        parts.append("    service: 'google-ads',")
        parts.append(f"    city: {js_str(city)},")
        parts.append(f"    state: {js_str(state)},")
        parts.append(f"    region: {js_str(meta['region'])},")
        parts.append(f"    titleTag: {js_str(title)},")
        parts.append(f"    metaDescription: {js_str(loc['metaDescription'])},")
        parts.append(f"    canonicalUrl: 'https://yakimabranding.com/google-ads/{slug}',")
        parts.append("    hero: {")
        parts.append("      eyebrow: 'GOOGLE ADS MANAGEMENT',")
        parts.append(f"      headline: {js_str(loc['hero_headline'])},")
        parts.append(f"      subheadline: {js_str(loc['hero_subheadline'])},")
        parts.append(f"      body: {js_str(loc['hero_body'])},")
        parts.append("    },")
        parts.append("    googleAdsIntro: {")
        parts.append("      heading: 'Managed by Experts Since 2005',")
        parts.append(f"      intro: {js_str(loc['intro'])},")
        parts.append(f"      localParagraph: {js_str(loc['localParagraph'])},")
        parts.append("    },")
        parts.append("    whyYb: {")
        parts.append(f"      heading: {js_str(loc['why_heading'])},")
        parts.append(f"      body: {js_str(loc['why_body'])},")
        parts.append("    },")
        signals = ", ".join(js_str(s) for s in meta["localSignals"])
        parts.append(f"    localSignals: [{signals}],")
        parts.append(render_faqs(loc["faqs"]))
        parts.append("    schema: {")
        parts.append("      service: 'Google Ads',")
        parts.append(f"      addressLocality: {js_str(meta['schema_service'])},")
        parts.append(f"      addressRegion: {js_str(state)},")
        parts.append("      addressCountry: 'US',")
        parts.append("    },")
        parts.append("  },")
    parts.append("];")
    parts.append("")
    (ROOT / "data" / "googleAdsLocations.js").write_text("\n".join(parts), encoding="utf-8")


def write_social_media():
    parts = ["export const socialMediaLocations = ["]
    for slug in SLUGS:
        meta = CITY_META[slug]
        city = meta["city"]
        state = meta["state"]
        loc = SOCIAL_MEDIA[slug]
        tri = slug == "tri-cities-wa"
        title = tri_title("Social Media Management") if tri else f"Social Media Management {city} {state} | YB Marketing"
        parts.append("  {")
        parts.append(f"    slug: {js_str(slug)},")
        parts.append("    service: 'social-media',")
        parts.append(f"    city: {js_str(city)},")
        parts.append(f"    state: {js_str(state)},")
        parts.append(f"    region: {js_str(meta['region'])},")
        parts.append(f"    titleTag: {js_str(title)},")
        parts.append(f"    metaDescription: {js_str(loc['metaDescription'])},")
        parts.append(f"    canonicalUrl: 'https://yakimabranding.com/social-media/{slug}',")
        parts.append("    hero: {")
        parts.append("      eyebrow: 'SOCIAL MEDIA MANAGEMENT',")
        parts.append(f"      headline: {js_str(loc['hero_headline'])},")
        parts.append(f"      subheadline: {js_str(loc['hero_subheadline'])},")
        parts.append(f"      body: {js_str(loc['hero_body'])},")
        parts.append("    },")
        parts.append("    whatWeDo: {")
        parts.append("      heading: 'Social Media Management & Growth',")
        parts.append(f"      intro: {js_str(loc['intro'])},")
        parts.append(f"      localParagraph: {js_str(loc['localParagraph'])},")
        parts.append("    },")
        parts.append("    whyYb: {")
        parts.append(f"      heading: {js_str(loc['why_heading'])},")
        parts.append(f"      body: {js_str(loc['why_body'])},")
        parts.append("    },")
        signals = ", ".join(js_str(s) for s in meta["localSignals"])
        parts.append(f"    localSignals: [{signals}],")
        parts.append(render_faqs(loc["faqs"]))
        parts.append("    schema: {")
        parts.append("      service: 'Social Media',")
        parts.append(f"      addressLocality: {js_str(meta['schema_service'])},")
        parts.append(f"      addressRegion: {js_str(state)},")
        parts.append("      addressCountry: 'US',")
        parts.append("    },")
        parts.append("  },")
    parts.append("];")
    parts.append("")
    (ROOT / "data" / "socialMediaLocations.js").write_text("\n".join(parts), encoding="utf-8")


def write_seo():
    parts = ["export const seoLocations = ["]
    for slug in SLUGS:
        meta = CITY_META[slug]
        city = meta["city"]
        state = meta["state"]
        loc = SEO[slug]
        tri = slug == "tri-cities-wa"
        if tri:
            title = "Tri-Cities SEO Services | Kennewick, Pasco & Richland | YB Marketing"
        else:
            title = f"{city} SEO Services | YB Marketing"
        parts.append("  {")
        parts.append(f"    slug: {js_str(slug)},")
        parts.append(f"    city: {js_str(city)},")
        parts.append(f"    state: {js_str(state)},")
        parts.append(f"    region: {js_str(meta['region'])},")
        parts.append(f"    titleTag: {js_str(title)},")
        parts.append(f"    metaDescription: {js_str(loc['metaDescription'])},")
        parts.append(f"    canonicalUrl: 'https://yakimabranding.com/seo/{slug}',")
        parts.append("    hero: {")
        parts.append(f"      headline: {js_str(loc['hero_headline'])},")
        parts.append(f"      subheadline: {js_str(loc['hero_subheadline'])},")
        parts.append(f"      body: {js_str(loc['hero_body'])},")
        parts.append("    },")
        parts.append("    whatIsSeo: {")
        parts.append("      heading: 'What Is Search Engine Optimization?',")
        parts.append(f"      intro: {js_str(loc['intro'])},")
        parts.append(f"      localParagraph: {js_str(loc['localParagraph'])},")
        parts.append("    },")
        parts.append("    features: [")
        for title_key, body in zip(FEATURE_TITLES, loc["features"]):
            parts.append("      {")
            parts.append(f"        title: {js_str(title_key)},")
            parts.append(f"        body: {js_str(body)},")
            parts.append("      },")
        parts.append("    ],")
        parts.append("    whyYb: {")
        parts.append(f"      heading: {js_str(loc['why_heading'])},")
        parts.append(f"      body: {js_str(loc['why_body'])},")
        parts.append("    },")
        signals = ", ".join(js_str(s) for s in meta["localSignals"])
        parts.append(f"    localSignals: [{signals}],")
        parts.append(render_faqs(loc["faqs"]))
        parts.append("    schema: {")
        parts.append(f"      addressLocality: {js_str(meta['schema_seo'])},")
        parts.append(f"      addressRegion: {js_str(state)},")
        parts.append("      addressCountry: 'US',")
        parts.append("    },")
        parts.append("  },")
    parts.append("];")
    parts.append("")
    (ROOT / "data" / "seoLocations.js").write_text("\n".join(parts), encoding="utf-8")


WEB_DESIGN = {
    "yakima-wa": {
        "metaDescription": "Custom WordPress and Wix websites for Yakima Valley businesses. Fast, mobile-ready sites built to rank in local search and turn visitors into calls and form fills.",
        "hero_headline": "Yakima Web Design That Earns Trust on First Click",
        "hero_subheadline": "Custom Websites for Yakima and Yakima Valley Businesses",
        "hero_body": "Valley customers check your site before they call. If it loads slow, looks dated, or hides your phone number, they move on. We build Yakima websites that look professional, work on every phone, and make contacting you obvious.",
        "intro": "We design and build on WordPress and Wix depending on what fits your team. Some businesses need a simple service site. Others need e-commerce, booking, or custom integrations. We scope it honestly and build something you can actually maintain.",
        "localParagraph": "Yakima runs on referrals, but referrals still start with a Google search. Wineries need tasting room pages that convert tourists. Contractors need project galleries that build confidence. Healthcare offices need clear service pages patients can skim in thirty seconds. We have built sites across those categories in the Valley and know which details local buyers look for before they reach out.",
        "why_heading": "Websites Built for How Yakima Customers Decide",
        "why_body": "Your site should answer the questions Yakima customers ask before they call: what you do, where you serve, proof you are legit, and an easy way to contact you. We build that foundation on every project, then layer in SEO structure so you can grow organic traffic over time.",
        "faqs": [
            ("What does a web design project cost for a Yakima business?", "It depends on pages, features, and whether you need e-commerce or custom functionality. Most small business sites fall in a few-thousand-dollar range. We provide a clear proposal before any work starts."),
            ("Do you build websites for Yakima Valley wineries and agricultural businesses?", "Yes. We handle tasting room sites, wine club pages, seasonal promotions, and the visual storytelling wineries need. Ag and food brands get the same attention to mobile speed and local SEO."),
            ("How long does a Yakima web design project take?", "Most standard business sites launch in 4 to 8 weeks depending on content readiness. Larger builds with e-commerce or custom features take longer. You get a timeline at kickoff."),
            ("Will my Yakima website be optimized for Google?", "Yes. Every build includes clean heading structure, fast load times, mobile optimization, and technical SEO basics. We can add ongoing SEO if you want to push rankings further."),
            ("Can you redesign my existing Yakima business website?", "Absolutely. We preserve what is working, especially existing rankings, while updating design, speed, and conversion paths so the site feels current."),
            ("Do you provide website maintenance after launch?", "Yes. We offer hosting guidance, security updates, plugin management, and content changes so your site stays fast and secure after go-live."),
        ],
    },
    "ellensburg-wa": {
        "metaDescription": "Custom websites for Ellensburg and Kittitas County businesses. WordPress and Wix sites that speak to students, locals, and I-90 corridor traffic.",
        "hero_headline": "Ellensburg Web Design for a Town With Two Audiences",
        "hero_subheadline": "Custom Websites for Ellensburg and Kittitas County",
        "hero_body": "Ellensburg customers range from CWU students on their phones to longtime county residents who check reviews before they hire. Your website needs to work for both without feeling generic. We build sites that load fast, explain your services clearly, and make trust obvious.",
        "intro": "Ellensburg businesses often need sites that handle seasonal swings and multiple customer types. We start with who you are trying to reach, then pick the right platform and page structure so updates stay simple after launch.",
        "localParagraph": "A downtown retailer, a ranch supply company, and a student-focused restaurant all need different messaging, but they share one problem: if the site looks outdated, people assume the business is too. We build Ellensburg sites with clear service pages, strong mobile layouts, and local copy that helps you rank in Kittitas County searches.",
        "why_heading": "Sites That Work for Students and Lifelong Residents",
        "why_body": "Ellensburg is small enough that reputation matters and big enough that you still compete online. We build websites with the technical foundation Google expects and the straightforward messaging real local customers respond to.",
        "faqs": [
            ("What types of websites do you build for Ellensburg businesses?", "Service business sites, multi-page professional sites, and e-commerce builds on WordPress or Wix. We recommend the platform based on how hands-on you want to be with updates."),
            ("Can you help an Ellensburg business that has never had a website?", "Yes. We guide you through domain, hosting, design, content, and launch. No technical background required."),
            ("How do you handle content for my Ellensburg website?", "You can provide copy or we can write it. Location-specific pages and service descriptions help Ellensburg sites perform in local search."),
            ("Will my Ellensburg website work well on mobile?", "Every site we build is mobile responsive. That matters in a market with a large student population browsing on phones."),
            ("Can you build a site my team can update easily?", "Yes. WordPress and Wix both support user-friendly editing so you are not stuck calling a developer for every small change."),
            ("Do you build sites for businesses serving the broader I-90 corridor?", "Yes. We can structure service area pages for Cle Elum, Kittitas, and corridor traffic when that is where your customers come from."),
        ],
    },
    "tri-cities-wa": {
        "metaDescription": "Custom websites for Kennewick, Pasco, and Richland businesses. Fast WordPress and Wix sites built for the full Tri-Cities market.",
        "hero_headline": "Tri-Cities Web Design for Kennewick, Pasco, and Richland",
        "hero_subheadline": "Custom Websites Built for the Columbia Basin",
        "hero_body": "Tri-Cities customers search from three cities with different demographics and expectations. A site that only mentions one town or loads slow on mobile will cost you leads. We build websites that communicate your service area clearly and convert visitors across the Basin.",
        "intro": "Tri-Cities businesses need sites that work at metro scale: clear location messaging, fast mobile performance, and structure that supports SEO in Kennewick, Pasco, and Richland. We build on WordPress or Wix with those priorities from day one.",
        "localParagraph": "Pasco buyers may search in Spanish. Richland professionals compare you to larger firms. Kennewick retail and hospitality customers decide on phones during lunch breaks. One template cannot cover all of that. We map your real service area, build location-aware pages where they help, and design layouts that make calling or booking easy no matter which city the visitor comes from.",
        "why_heading": "Websites Built for Three Cities, One Brand",
        "why_body": "Most template sites treat the Tri-Cities like a single dot on a map. We build sites that reflect how you actually operate: where you serve, who you serve, and what proof you can show customers in each part of the metro.",
        "faqs": [
            ("Do you build websites that rank in Kennewick, Pasco, and Richland?", "Yes. We structure location pages, service area copy, and technical SEO so you can compete across the full Tri-Cities metro."),
            ("What industries do you serve with web design in the Tri-Cities?", "Healthcare, legal, construction, wineries, restaurants, retail, and professional services. If customers find you online first, a strong site pays off."),
            ("Can you handle bilingual content for Pasco-area customers?", "Yes. We can build bilingual pages or sections when that matches how your customers search and buy."),
            ("How long does a Tri-Cities web design project take?", "Most business sites take 4 to 8 weeks. E-commerce and custom functionality add time. We set expectations at the start."),
            ("Do you offer hosting and maintenance for Tri-Cities businesses?", "Yes. We help with hosting setup, security updates, and ongoing content changes after launch."),
            ("Can you redesign a Tri-Cities site without losing SEO rankings?", "Yes. We audit what is ranking, preserve valuable URLs and content, then modernize design and conversion paths."),
        ],
    },
    "spokane-wa": {
        "metaDescription": "Professional web design for Spokane and Inland Northwest businesses. Custom WordPress and Wix sites built to compete in Eastern Washington's largest market.",
        "hero_headline": "Spokane Web Design That Looks Credible Next to Big Competitors",
        "hero_subheadline": "Custom Websites for Spokane and the Inland Northwest",
        "hero_body": "Spokane buyers compare you to national chains and well-funded local firms before they call. Your website is part of that comparison. We build fast, professional sites that earn trust in seconds and make the next step easy.",
        "intro": "Spokane is a real city market with real competition. We build websites with strong service pages, proof elements, and technical performance that matches what customers expect from larger players.",
        "localParagraph": "Healthcare groups, law firms, contractors, and retailers all need different site structures, but they share one need: clarity. Spokane customers do not have patience for vague copy or buried contact forms. We build sites that state what you do, show who you have helped, and load quickly on mobile from South Hill to Spokane Valley.",
        "why_heading": "Spokane Sites With Regional Polish",
        "why_body": "You should not need a Seattle budget to look credible in Spokane. We deliver professional design, solid SEO structure, and conversion-focused layouts sized for Inland Northwest businesses.",
        "faqs": [
            ("What does web design cost for a Spokane business?", "Cost depends on scope, pages, and features. We quote after understanding your goals and provide a clear proposal before work begins."),
            ("Do you build WordPress and Wix sites for Spokane companies?", "Yes. We recommend the platform based on your team, budget, and how much you want to manage in-house."),
            ("Can you improve an outdated Spokane business website?", "Yes. Redesigns are common for us. We keep what is working for SEO and upgrade design, speed, and user experience."),
            ("Will my Spokane site be mobile-friendly?", "Every site is built mobile-first. A large share of Spokane searches happen on phones."),
            ("Do you build e-commerce sites for Spokane retailers?", "Yes. We build WooCommerce and Wix stores with product pages, checkout, and the SEO structure retail needs."),
            ("Can you add landing pages for specific Spokane neighborhoods or services?", "Yes. Targeted landing pages help with paid ads and local SEO for service-area businesses."),
        ],
    },
    "boise-id": {
        "metaDescription": "Custom websites for Boise and Treasure Valley businesses. Modern WordPress and Wix builds for a fast-growing market with rising design expectations.",
        "hero_headline": "Boise Web Design for a Market That Keeps Getting Busier",
        "hero_subheadline": "Custom Websites for Treasure Valley Businesses",
        "hero_body": "Boise customers notice design quality. Relocated professionals and national brands raised the bar. If your site looks like it was built in 2015, people assume your business runs the same way. We build modern sites that help you compete in the Treasure Valley.",
        "intro": "Boise businesses need sites that look current, load fast, and scale as they grow. We build on WordPress or Wix with clean structure so you can add locations, services, or e-commerce without starting over.",
        "localParagraph": "Outdoor brands, home services, medical offices, and food businesses all fight for attention in Boise, Meridian, and Nampa searches. Your site needs clear differentiation, not another stock photo hero. We talk through your offer, your proof, and your service area before we design so the finished site feels like your company, not a template with your logo swapped in.",
        "why_heading": "Websites Built to Scale With Boise",
        "why_body": "Whether you are launching a new concept or refreshing an old site, we deliver something your team can use as you hire, expand service areas, and invest more in marketing.",
        "faqs": [
            ("How much does a Boise business website cost?", "Most projects range from a few thousand dollars upward depending on pages and features. We scope honestly and quote before work starts."),
            ("Do you build sites for Boise home service and contractor businesses?", "Yes. We build lead-focused sites with strong calls to action, service pages, and mobile performance for trades and home services."),
            ("How long does a Treasure Valley web project take?", "Typical business sites launch in 4 to 8 weeks. Larger builds take longer. We set a timeline at kickoff."),
            ("Can you help my Boise site rank in Meridian and Nampa too?", "Yes. Service area pages and local SEO structure help you show up across the Treasure Valley."),
            ("Do you offer website maintenance for Boise businesses?", "Yes. Security updates, content changes, and performance monitoring keep your site healthy after launch."),
            ("Can you integrate booking, forms, or CRM tools?", "Yes. We connect contact forms, scheduling tools, and CRMs so leads do not fall through the cracks."),
        ],
    },
    "coeur-dalene-id": {
        "metaDescription": "Custom websites for Coeur d'Alene and North Idaho businesses. WordPress and Wix sites built for tourism season and year-round local customers.",
        "hero_headline": "Coeur d'Alene Web Design for Lake Country Businesses",
        "hero_subheadline": "Custom Websites for CDA and Kootenai County",
        "hero_body": "CDA customers often decide on their phones while they are already out and about. Your site needs to load fast, look polished, and make booking or calling simple. We build websites that work for summer visitors and loyal local customers alike.",
        "intro": "North Idaho businesses juggle seasonal traffic and a local base that values trust over hype. We build sites with strong visuals when they help, clear information always, and mobile performance that does not drop off on the lake.",
        "localParagraph": "Marinas, restaurants, lodging, and home service companies all need different site features, but they share one risk: looking like a generic resort template. We design for CDA with real photography direction, honest service copy, and SEO that captures both visitor-intent and local searches from Post Falls to Hayden.",
        "why_heading": "Sites That Work in Peak Season and Off Season",
        "why_body": "Your website should help you capture summer demand and still generate local leads when tourism slows. We build with both calendars in mind.",
        "faqs": [
            ("Do you build websites for Coeur d'Alene hospitality businesses?", "Yes. Restaurants, hotels, marinas, and activity providers get booking-focused layouts, galleries, and mobile-first design."),
            ("Can you help my CDA site attract tourists and locals?", "Yes. We structure content for visitor searches and local service searches so you are not relying on one audience."),
            ("What platforms do you use for North Idaho web design?", "WordPress and Wix depending on your needs. We recommend what fits your team and budget."),
            ("How important is mobile performance for CDA businesses?", "Very. Visitors research on phones constantly. Slow sites lose bookings."),
            ("Do you offer maintenance after launch?", "Yes. Updates, security, and content changes so your site stays current through seasonal shifts."),
            ("Can you redesign an outdated Coeur d'Alene website?", "Yes. We modernize design and speed while protecting existing search visibility where possible."),
        ],
    },
    "tacoma-wa": {
        "metaDescription": "Custom websites for Tacoma and Pierce County businesses. Professional WordPress and Wix builds for South Sound companies with local loyalty and regional competition.",
        "hero_headline": "Tacoma Web Design for a City That Rewards Quality",
        "hero_subheadline": "Custom Websites for Tacoma and Pierce County",
        "hero_body": "Tacoma customers support local when local earns it. They also compare you to Seattle options online. Your website needs neighborhood credibility and regional polish. We build sites that deliver both.",
        "intro": "Tacoma businesses need websites that tell a real story: who you serve, what you do well, and why someone in Pierce County should choose you. We build that story into every page, not just the homepage.",
        "localParagraph": "Contractors, clinics, restaurants, and professional firms across Tacoma and Lakewood all compete for the same click. We build service pages with proof, fast mobile layouts, and contact paths that work for customers researching on the bus or at home after work. The goal is simple: look credible, answer questions, make outreach easy.",
        "why_heading": "South Sound Sites With Local Voice",
        "why_body": "You should not have to sound like a Seattle agency to look professional in Tacoma. We build direct, polished sites tied to how Pierce County customers actually choose providers.",
        "faqs": [
            ("What does web design cost for a Tacoma business?", "It varies by pages and features. We provide a written proposal after scoping your project."),
            ("Do you build sites for Tacoma contractors and home services?", "Yes. Lead generation, service area pages, and mobile performance are standard on those builds."),
            ("Can you help my Tacoma site compete with Seattle companies?", "Yes. Professional design, clear messaging, and local SEO help you win Washington-side searches."),
            ("How long does a Tacoma web project take?", "Most sites launch in 4 to 8 weeks depending on complexity and content readiness."),
            ("Will my site work well on mobile?", "Yes. Mobile-first design is standard on every project."),
            ("Do you provide post-launch support?", "Yes. Maintenance, updates, and security monitoring are available after go-live."),
        ],
    },
    "vancouver-wa": {
        "metaDescription": "Custom websites for Vancouver, WA and Clark County businesses. WordPress and Wix sites that establish your Washington-side presence distinct from Portland.",
        "hero_headline": "Vancouver Web Design for Clark County Customers",
        "hero_subheadline": "Custom Websites on the Washington Side of the River",
        "hero_body": "Many Clark County customers want to hire Washington businesses. Your website should make that choice easy with clear local proof, service area messaging, and a professional first impression. We build Vancouver sites that own your side of the river.",
        "intro": "Vancouver businesses often compete with Portland brands that dominate search results. We build sites with Clark County language, location signals, and structure that helps you rank for Washington-side searches.",
        "localParagraph": "Camas professionals, Ridgefield families, and longtime Vancouver operators all search differently. We build service pages and local copy that match those searches, plus fast mobile layouts for customers comparing options on their commute. The site should say clearly: we are here, we serve you, here is how to reach us.",
        "why_heading": "A Vancouver Site That Is Not a Portland Afterthought",
        "why_body": "We build Clark County websites on purpose: local proof, Washington service area messaging, and design quality that stands up next to Oregon competition.",
        "faqs": [
            ("Do you build websites for Vancouver and Clark County businesses?", "Yes. We serve Vancouver, Camas, Ridgefield, and surrounding Clark County markets."),
            ("Can you help me rank for Vancouver WA searches instead of Portland results?", "Yes. Local pages, Google Business Profile alignment, and technical SEO all support Washington-side visibility."),
            ("What platforms do you recommend for Vancouver businesses?", "WordPress or Wix depending on your team and goals. We explain the tradeoffs before you decide."),
            ("Can you redesign an existing Vancouver business website?", "Yes. We preserve rankings where possible and improve design, speed, and conversions."),
            ("Do you build e-commerce sites for Clark County retailers?", "Yes. Product catalogs, checkout, and SEO structure for online sales."),
            ("Do you offer ongoing website maintenance?", "Yes. Security, updates, and content support after launch."),
        ],
    },
    "wenatchee-wa": {
        "metaDescription": "Custom websites for Wenatchee and North Central Washington businesses. WordPress and Wix sites built for a regional hub that serves the whole valley.",
        "hero_headline": "Wenatchee Web Design for NCW's Regional Hub",
        "hero_subheadline": "Custom Websites for Wenatchee and North Central Washington",
        "hero_body": "Customers drive to Wenatchee for services they cannot get at home. Your website is often the reason they choose you over a closer option. We build sites that signal regional authority and make the call easy.",
        "intro": "Wenatchee businesses serve a wide draw radius: East Wenatchee, Leavenworth, Chelan, and orchard country. We build sites with service area clarity, mobile performance, and local SEO for the towns that send you revenue.",
        "localParagraph": "Ag operations, medical offices, contractors, and hospitality businesses all need different features, but they share one need online: trust at a glance. We build Wenatchee sites with proof, clear service pages, and fast load times for customers searching from across NCW on spotty cell connections.",
        "why_heading": "Sites Built for a Regional Customer Base",
        "why_body": "Your website should convince customers in surrounding towns that the trip to Wenatchee is worth it. We build with that regional mindset from the first wireframe.",
        "faqs": [
            ("Do you build websites for Wenatchee agricultural and food businesses?", "Yes. Packaging brands, orchards, and food companies get sites that support both local and regional buyers."),
            ("Can my site rank in East Wenatchee and Leavenworth too?", "Yes. Service area pages and local SEO help you show up across NCW."),
            ("How long does a Wenatchee web project take?", "Most business sites take 4 to 8 weeks. Larger builds take longer."),
            ("Will my site work well on mobile?", "Yes. Mobile-first design matters for customers searching on the road."),
            ("Do you offer website maintenance?", "Yes. Updates, security, and content changes after launch."),
            ("Can you help a business that serves the whole Wenatchee Valley?", "Yes. We structure service area messaging and pages for regional coverage."),
        ],
    },
    "walla-walla-wa": {
        "metaDescription": "Custom websites for Walla Walla wine country and local businesses. WordPress and Wix builds that impress tourists and earn trust from locals.",
        "hero_headline": "Walla Walla Web Design for Wine Country Standards",
        "hero_subheadline": "Custom Websites for Wine Country and Local Business",
        "hero_body": "Walla Walla visitors plan trips online before they arrive. Locals compare you to the best businesses in town. Your website needs to meet both expectations: beautiful enough for tourism, credible enough for year-round customers.",
        "intro": "Wine country sets a high bar for design. We build sites for wineries, hospitality, and local service businesses with strong visuals, fast mobile performance, and the booking or contact paths that turn research into visits.",
        "localParagraph": "Wineries need tasting room pages, wine club flows, and e-commerce options. Restaurants need menus, reservations, and photography that sells the experience. Trades and professional firms need proof and clarity. We have built across those categories and know how to balance aesthetics with the practical details Walla Walla buyers expect.",
        "why_heading": "Websites That Meet Wine Country Expectations",
        "why_body": "Your site should look like it belongs in Walla Walla without copying every other tasting room template. We design for your brand, your audience, and the searches that bring both locals and visitors to your door.",
        "faqs": [
            ("Do you build websites for Walla Walla wineries and tasting rooms?", "Yes. Visual storytelling, events, reservations, and wine club or e-commerce functionality are all in scope."),
            ("Can you integrate wine club or bottle sales?", "Yes. WooCommerce and Wix e-commerce with the product and checkout flows wineries need."),
            ("How important is mobile for Walla Walla tourism businesses?", "Critical. Many visit decisions happen on phones while travelers are already in the area."),
            ("Do you build sites for restaurants and hotels in Walla Walla?", "Yes. Menus, galleries, booking integrations, and local SEO for hospitality."),
            ("Can you serve non-wine Walla Walla businesses too?", "Yes. Contractors, healthcare, retail, and professional services all benefit from strong web design here."),
            ("Can one site target both visitors and local customers?", "Yes. We structure content for destination searches and resident searches on the same site."),
        ],
    },
}

GOOGLE_ADS = {
    "yakima-wa": {
        "metaDescription": "Google Ads management for Yakima Valley businesses since 2005. Expert PPC campaigns with local targeting, conversion tracking, and budgets aligned to seasonal demand.",
        "hero_headline": "Yakima Google Ads That Stop Burning Budget on Bad Clicks",
        "hero_subheadline": "Expert PPC for Yakima and Yakima Valley Businesses Since 2005",
        "hero_body": "Most Yakima businesses running their own Google Ads pay for clicks that never become jobs. Wrong keywords, loose targeting, and weak landing pages drain budget fast. We have managed campaigns since 2005 and know how to make every dollar work harder in the Valley.",
        "intro": "Google Ads change constantly. Most owners do not have time to watch search terms, adjust bids, and rewrite ads every week. That is why campaigns drift into waste or get turned off entirely. We manage accounts full time so yours stays focused on leads, not clicks.",
        "localParagraph": "Yakima search behavior has real seasonality. Ag and winery traffic spikes at different times. Contractors surge after storms and in spring. Healthcare stays steadier year round. Generic national PPC playbooks miss those patterns. We build Yakima campaigns around your industry's calendar, your service area, and the keywords that actually produce calls in Selah, Union Gap, and across the Valley.",
        "why_heading": "PPC Built Around Yakima's Seasons and Search Habits",
        "why_body": "We structure campaigns around your services, margins, and local competition. You get conversion tracking, monthly reporting in plain language, and ongoing optimization so spend moves toward what works.",
        "faqs": [
            ("How much should a Yakima business spend on Google Ads?", "It depends on industry and competition. Many service businesses start around $500 to $1,500 per month in ad spend. We audit your market before recommending a budget."),
            ("How quickly can Google Ads generate leads in Yakima?", "Ads can produce leads within days of launch. Most campaigns improve over the first 2 to 4 weeks as we gather data and refine targeting."),
            ("Do you manage Google Ads for Yakima wineries and seasonal businesses?", "Yes. We ramp spend during peak seasons and tighten targeting during slower months so budget follows demand."),
            ("What is included in Yakima Google Ads management?", "Keyword research, ad copy, bid management, landing page recommendations, call tracking, monthly reporting, and ongoing optimization."),
            ("Can you fix an existing Google Ads account that wastes money?", "Yes. Account audits and rebuilds are common. We find wasted spend, fix structure, and improve performance without always starting from zero."),
            ("Do Google Ads and SEO work together for Yakima businesses?", "They complement each other. Ads deliver immediate visibility while SEO builds long-term rankings. Many Valley businesses run both strategically."),
        ],
    },
    "ellensburg-wa": {
        "metaDescription": "Google Ads management for Ellensburg and Kittitas County businesses. Expert PPC since 2005 with targeting for students, locals, and I-90 corridor traffic.",
        "hero_headline": "Ellensburg Google Ads With Smarter Local Targeting",
        "hero_subheadline": "PPC Management for Ellensburg and Kittitas County",
        "hero_body": "Ellensburg's market is smaller than Seattle, which can mean lower cost per click and better ROI when campaigns are set up right. It also means sloppy targeting wastes budget fast. We build Ellensburg campaigns that reach the right people in the right season.",
        "intro": "Running Google Ads without daily attention leads to broad keywords, irrelevant clicks, and budgets that disappear before the phone rings. We have managed PPC since 2005 and treat account structure, negative keywords, and conversion tracking as non-negotiable.",
        "localParagraph": "Ellensburg has two distinct audiences: CWU students who search differently than longtime Kittitas County residents, plus I-90 travelers who need services now. A single broad campaign rarely serves all three well. We segment messaging and geography where it matters so your spend reaches students during the academic year, locals year round, and corridor traffic when that is part of your business.",
        "why_heading": "PPC Tuned for Ellensburg's Mixed Audience",
        "why_body": "Smaller markets reward precision. We build Ellensburg campaigns with tight geographic targeting, audience-aware ad copy, and reporting that shows which searches turn into real leads.",
        "faqs": [
            ("Is Google Ads worth it for a small Ellensburg business?", "Often yes. Less competition than larger cities can mean better ROI with proper management. We assess your niche before recommending spend."),
            ("Can Google Ads help me reach CWU students?", "Yes. We use geographic radius targeting, seasonal scheduling, and keywords that match how students search for your services."),
            ("What is a realistic Google Ads budget in Ellensburg?", "Many businesses start around $300 to $800 per month in ad spend for less competitive categories. We give honest guidance before you commit."),
            ("How do you track whether Google Ads are working?", "Call tracking, form conversions, and monthly reports that tie spend to leads, not just clicks."),
            ("Do you manage ads for businesses serving the I-90 corridor?", "Yes. We can expand targeting to Cle Elum, Kittitas, and corridor searches when that matches your service area."),
            ("Can you fix a Google Ads account that failed before?", "Yes. Poor structure is common with DIY accounts. We audit, rebuild, and optimize for performance."),
        ],
    },
    "tri-cities-wa": {
        "metaDescription": "Google Ads management for Kennewick, Pasco, and Richland businesses. Expert PPC since 2005 with city-level targeting across the Columbia Basin.",
        "hero_headline": "Tri-Cities Google Ads for Kennewick, Pasco, and Richland",
        "hero_subheadline": "PPC Campaigns Built for the Full Columbia Basin",
        "hero_body": "A single Tri-Cities campaign set to cover all three cities often underperforms all three. Search behavior, competition, and demographics differ between Kennewick, Pasco, and Richland. We structure campaigns with the specificity this market requires.",
        "intro": "Tri-Cities PPC needs more than a radius on a map. Budget allocation, ad copy, and landing pages should reflect where your best customers actually search. We have managed Google Ads since 2005 and apply that experience to multi-city metros like the Basin.",
        "localParagraph": "Pasco's bilingual audience, Richland's professional base, and Kennewick's retail and hospitality economy respond to different messages. We build campaign structures that split budget by city and service line where data supports it, unify messaging where it does not, and track conversions so you know which city drives revenue.",
        "why_heading": "PPC for Three Cities, Not One Blob",
        "why_body": "Most agencies flatten the Tri-Cities into one target. We treat Kennewick, Pasco, and Richland as distinct markets inside one strategy so your budget follows results.",
        "faqs": [
            ("Do you run separate campaigns for Kennewick, Pasco, and Richland?", "Often yes, or city-level ad groups when that improves performance. Structure depends on your services and where leads come from."),
            ("How much should a Tri-Cities business spend on Google Ads?", "Budget varies by industry. Competitive categories like legal and home services often need more. We recommend spend after reviewing your market."),
            ("Can you manage ads for bilingual Pasco audiences?", "Yes. We build campaigns and landing pages that match how your customers search and buy."),
            ("How fast can Tri-Cities Google Ads generate leads?", "Many accounts see leads within the first few weeks. Optimization continues as data accumulates."),
            ("What is included in Tri-Cities PPC management?", "Setup or audit, keywords, ad copy, bid management, conversion tracking, landing page guidance, and monthly reporting."),
            ("Can you rescue a Tri-Cities account that wasted budget?", "Yes. We audit structure, search terms, and targeting, then rebuild what is broken."),
        ],
    },
    "spokane-wa": {
        "metaDescription": "Google Ads management for Spokane and Inland Northwest businesses. Expert PPC since 2005 with conversion tracking and competitive keyword strategy.",
        "hero_headline": "Spokane Google Ads That Compete in a Crowded Auction",
        "hero_subheadline": "PPC Management for Spokane and the Inland Northwest",
        "hero_body": "Spokane's ad auctions are competitive. Broad keywords and weak landing pages burn budget without producing jobs. We build structured campaigns with negative keywords, conversion tracking, and ongoing optimization so spend protects your margins.",
        "intro": "Google Ads reward accounts that are maintained weekly, not set up once and ignored. We have managed PPC since 2005 and focus on account structure, search term reviews, and landing pages that match ad intent.",
        "localParagraph": "Healthcare, home services, legal, and retail all compete for the same Spokane searches. Winning requires tight keyword groups, ads that speak to local buyers, and landing pages that make calling easy. We build Spokane campaigns sized for Inland Northwest competition, not small-town budgets with big-city auction prices.",
        "why_heading": "Spokane PPC With Accountability",
        "why_body": "You get clear reporting on cost per lead, regular optimization, and honest recommendations when a keyword or campaign is not pulling its weight.",
        "faqs": [
            ("How much do Spokane businesses spend on Google Ads?", "Varies widely by industry. Home services and legal often need higher budgets. We assess competition before recommending spend."),
            ("How quickly do Spokane Google Ads produce leads?", "Many campaigns generate leads within days. Performance typically improves over the first month as we optimize."),
            ("Do you manage Google Ads for Spokane healthcare and professional firms?", "Yes. We work with regulated and competitive categories that need careful keyword and landing page strategy."),
            ("What is included in Spokane PPC management?", "Keyword research, ad copy, bid management, conversion tracking, landing page recommendations, and monthly reporting."),
            ("Can you improve an underperforming Spokane account?", "Yes. Account audits and restructures are a core part of our work."),
            ("Do Google Ads help Spokane businesses compete with national brands?", "Yes. Well-managed local campaigns can win high-intent searches even when national players advertise."),
        ],
    },
    "boise-id": {
        "metaDescription": "Google Ads management for Boise and Treasure Valley businesses. Expert PPC since 2005 built for a fast-growing, competitive Idaho market.",
        "hero_headline": "Boise Google Ads for a Market With Rising CPCs",
        "hero_subheadline": "PPC Management for Treasure Valley Businesses",
        "hero_body": "Boise competition pushes click costs up every year. Campaigns without structure, tracking, and weekly optimization waste money fast. We manage Google Ads with the discipline growing Treasure Valley businesses need.",
        "intro": "Boise adds new advertisers constantly. Accounts that worked two years ago may bleed budget today without refreshed keywords, negatives, and landing pages. We manage PPC full time so yours keeps pace with the market.",
        "localParagraph": "Home services, medical, legal, and outdoor brands all bid on Treasure Valley searches. We build Boise campaigns around your profit per job, not just click volume. That means geographic targeting across Boise, Meridian, and Nampa where you actually serve, ad copy that differentiates you, and conversion tracking that shows which keywords deserve more budget.",
        "why_heading": "Treasure Valley PPC That Scales With Growth",
        "why_body": "Start focused, expand what works. We align ad spend with lead quality and margins so you can grow into new services or cities without guessing.",
        "faqs": [
            ("How much should a Boise business spend on Google Ads?", "Depends on category and goals. Competitive trades and legal often need $1,500 plus per month in ad spend. We recommend after a market review."),
            ("How fast can Boise Google Ads generate leads?", "Often within the first week of launch. Optimization continues as data comes in."),
            ("Do you manage ads across Boise, Meridian, and Nampa?", "Yes. Geographic targeting and separate campaigns or ad groups when performance data supports it."),
            ("What is included in Boise PPC management?", "Account setup or audit, keywords, ads, bids, tracking, landing page guidance, and monthly reporting."),
            ("Can you fix a Boise account that did not work before?", "Yes. We diagnose structure, match types, and landing pages, then rebuild for performance."),
            ("Do Google Ads and SEO work together in Boise?", "Yes. Many Treasure Valley businesses use ads for immediate visibility while SEO builds long-term organic traffic."),
        ],
    },
    "coeur-dalene-id": {
        "metaDescription": "Google Ads management for Coeur d'Alene and North Idaho businesses. Expert PPC since 2005 with seasonal campaigns for tourism and year-round local leads.",
        "hero_headline": "Coeur d'Alene Google Ads for Seasonal and Local Demand",
        "hero_subheadline": "PPC Management for CDA and Kootenai County",
        "hero_body": "CDA businesses face two calendars: summer tourism and year-round local service. Google Ads should follow that rhythm. We manage campaigns that ramp when demand is high and stay efficient when it is not.",
        "intro": "Lake country search volume swings with the season. Campaigns left on autopilot overspend in winter or miss peak summer demand. We have managed Google Ads since 2005 and build seasonal strategies into North Idaho accounts.",
        "localParagraph": "Hospitality, recreation, and home services all search differently in Coeur d'Alene, Post Falls, and Hayden. Visitors search on phones for things to do tonight. Locals search for providers they can trust next month. We target each intent with the right keywords, ad copy, and landing pages so budget follows real booking and call data.",
        "why_heading": "PPC That Respects CDA Seasonality",
        "why_body": "We adjust bids, budgets, and creative as tourism and local demand shift so you are not paying peak-season rates for off-season clicks.",
        "faqs": [
            ("Do you manage seasonal Google Ads for Coeur d'Alene businesses?", "Yes. We plan budget and targeting around your peak and off-peak months."),
            ("How much should a CDA business spend on Google Ads?", "Varies by industry. Hospitality often needs higher summer spend. Service businesses may run steadier year-round budgets."),
            ("Can Google Ads reach tourists and locals?", "Yes. We separate campaigns or keywords by intent when that improves performance."),
            ("What is included in CDA PPC management?", "Setup, keywords, ads, bid management, conversion tracking, and monthly reporting."),
            ("How quickly can Google Ads produce leads in North Idaho?", "Many accounts see results within the first few weeks of launch."),
            ("Can you fix an underperforming Coeur d'Alene account?", "Yes. We audit and rebuild accounts that wasted spend on poor structure or targeting."),
        ],
    },
    "tacoma-wa": {
        "metaDescription": "Google Ads management for Tacoma and Pierce County businesses. Expert PPC since 2005 with geo-targeting that prioritizes South Sound leads.",
        "hero_headline": "Tacoma Google Ads That Win South Sound Searches",
        "hero_subheadline": "PPC Management for Tacoma and Pierce County",
        "hero_body": "Tacoma advertisers compete with Seattle budgets if targeting is too broad. We geo-fence campaigns to Pierce County, write ads that sound local, and track conversions so you know which keywords produce calls.",
        "intro": "Google Ads fail when accounts are too broad, too stale, or missing conversion tracking. We manage PPC with weekly attention and reporting tied to leads, not vanity metrics.",
        "localParagraph": "Tacoma customers search for contractors, clinics, restaurants, and professional services with local intent. We build campaigns that prioritize South Sound zip codes, filter irrelevant Seattle traffic when needed, and send clicks to landing pages that make contacting you easy.",
        "why_heading": "Tacoma PPC Without Wasted Seattle Clicks",
        "why_body": "Your budget should go toward Pierce County leads. We structure campaigns and negatives to protect spend and improve cost per lead over time.",
        "faqs": [
            ("How much should a Tacoma business spend on Google Ads?", "Depends on industry and competition. We recommend budget after reviewing your market and goals."),
            ("Can you target Tacoma without paying for Seattle clicks?", "Yes. Geographic targeting and negative keywords help focus spend on South Sound."),
            ("How fast do Tacoma Google Ads generate leads?", "Many campaigns produce leads within days. Optimization continues monthly."),
            ("What is included in Tacoma PPC management?", "Keywords, ad copy, bids, tracking, landing page recommendations, and reporting."),
            ("Do you work with Tacoma contractors and home services?", "Yes. High-intent local keywords and call tracking are standard for trades."),
            ("Can you improve an existing Tacoma Google Ads account?", "Yes. Audits and restructures are common engagements for us."),
        ],
    },
    "vancouver-wa": {
        "metaDescription": "Google Ads management for Vancouver, WA and Clark County businesses. Expert PPC since 2005 with targeting that favors Washington-side leads over Portland noise.",
        "hero_headline": "Vancouver Google Ads for Clark County Customers",
        "hero_subheadline": "PPC Management on the Washington Side of the River",
        "hero_body": "Vancouver businesses often compete with Portland advertisers in the same auction. Without tight geo-targeting and Washington-focused messaging, budget leaks across the river. We build Clark County campaigns that keep spend local.",
        "intro": "Clark County PPC requires deliberate geography and messaging. We have managed Google Ads since 2005 and know how to structure accounts so Vancouver searches do not fund Portland leads.",
        "localParagraph": "Customers in Vancouver, Camas, and Ridgefield often want a Washington provider. Your ads and landing pages should say that clearly. We target Clark County zip codes, use local proof in ad copy, and track calls and forms so you see which campaigns drive Washington-side revenue.",
        "why_heading": "Washington-Side PPC, Measured",
        "why_body": "We report leads by campaign and location so you know what is working in Vancouver versus Camas or Ridgefield.",
        "faqs": [
            ("Can Google Ads help me compete against Portland businesses?", "Yes. Tight geo-targeting and local ad copy help you win Clark County searches."),
            ("How much should a Vancouver WA business spend on Google Ads?", "Varies by industry. We assess competition and recommend realistic budgets."),
            ("Do you target Vancouver, Camas, and Ridgefield?", "Yes. Geographic structure follows where you actually serve and where leads come from."),
            ("What is included in Vancouver PPC management?", "Account setup or audit, keywords, ads, bids, tracking, and monthly reporting."),
            ("How quickly can Google Ads produce leads in Clark County?", "Many accounts see leads within the first few weeks."),
            ("Can you fix a Google Ads account that wasted budget?", "Yes. We audit structure and rebuild for Clark County performance."),
        ],
    },
    "wenatchee-wa": {
        "metaDescription": "Google Ads management for Wenatchee and North Central Washington businesses. Expert PPC since 2005 with seasonal and regional targeting across NCW.",
        "hero_headline": "Wenatchee Google Ads for NCW's Regional Draw",
        "hero_subheadline": "PPC Management for Wenatchee and North Central Washington",
        "hero_body": "Wenatchee businesses draw customers from across the valley. Google Ads should target the towns that send you revenue, not just city limits. We build regional campaigns with seasonal adjustments for tourism and ag peaks.",
        "intro": "NCW search patterns shift with harvest, tourism, and weather. Campaigns that never change miss those swings. We manage Google Ads with seasonal calendars and geographic targeting that matches your real service area.",
        "localParagraph": "Customers in East Wenatchee, Leavenworth, and Chelan search for Wenatchee providers when local options are limited. We build campaigns that capture that regional intent, plus steady local service keywords year round. Conversion tracking shows which towns and keywords produce calls.",
        "why_heading": "Regional PPC With Geographic Precision",
        "why_body": "We target the communities that send you jobs, adjust for seasonal demand, and report in plain language so you know where spend works.",
        "faqs": [
            ("Do you manage Google Ads for Wenatchee seasonal businesses?", "Yes. Tourism, ag, and hospitality campaigns get seasonal budget and keyword adjustments."),
            ("Can ads target East Wenatchee and Leavenworth too?", "Yes. Geographic targeting expands to your actual draw radius."),
            ("How much should a Wenatchee business spend on Google Ads?", "Depends on category. We recommend after reviewing NCW competition."),
            ("What is included in Wenatchee PPC management?", "Keywords, ads, bids, tracking, landing page guidance, and monthly reporting."),
            ("How fast can Google Ads produce leads in NCW?", "Many campaigns see leads within the first few weeks."),
            ("Can you fix an underperforming Wenatchee account?", "Yes. We audit and optimize accounts that wasted spend."),
        ],
    },
    "walla-walla-wa": {
        "metaDescription": "Google Ads management for Walla Walla wine country and local businesses. Expert PPC since 2005 for tourism peaks and year-round local leads.",
        "hero_headline": "Walla Walla Google Ads for Wine Country and Local Service",
        "hero_subheadline": "PPC Management for Walla Walla Businesses",
        "hero_body": "Walla Walla marketing runs on two clocks: weekend visitors and loyal locals. Google Ads should capture high-intent searches in both seasons. We manage campaigns that ramp for events and tourism without ignoring year-round service demand.",
        "intro": "Wine country advertisers compete for limited high-intent searches on busy weekends. Off-season, local service keywords matter more. We manage Google Ads with that calendar built in.",
        "localParagraph": "Wineries, restaurants, hotels, and trades all need different keyword strategies in Walla Walla. Visitors search for experiences and reservations. Locals search for providers they can trust all year. We build campaigns and landing pages for both, track conversions, and shift budget as seasons change.",
        "why_heading": "PPC That Matches Wine Country Rhythm",
        "why_body": "Creative quality and measurable leads should not be an either-or. We optimize for bookings and calls with reporting you can act on.",
        "faqs": [
            ("Do you manage Google Ads for Walla Walla wineries?", "Yes. Tasting room, event, and wine tourism keywords with seasonal budget shifts."),
            ("Can ads target both tourists and local customers?", "Yes. We separate intent where it improves performance and ROI."),
            ("How much should a Walla Walla business spend on Google Ads?", "Varies by season and industry. We recommend budgets after reviewing your market."),
            ("What is included in Walla Walla PPC management?", "Setup, keywords, ads, bids, tracking, and monthly reporting."),
            ("How quickly can Google Ads produce leads in Walla Walla?", "Many accounts see results within the first few weeks."),
            ("Can you rescue a Google Ads account that underperformed?", "Yes. We audit structure and rebuild for wine country and local service goals."),
        ],
    },
}


SOCIAL_MEDIA = {
    "yakima-wa": {
        "metaDescription": "Social media management for Yakima businesses on Facebook, Instagram, and LinkedIn. Strategy, content, and growth focused on Valley audiences.",
        "hero_headline": "Yakima Social Media That Reaches Beyond Your Existing Followers",
        "hero_subheadline": "Facebook, Instagram, and LinkedIn for Yakima Valley Businesses",
        "hero_body": "Posting without a plan keeps you talking to the same small circle. Yakima customers respond to local storytelling, not generic stock content. We build social strategies that grow reach across the Valley and turn attention into calls and visits.",
        "intro": "Social media works when it has a plan: who you are talking to, what you post, how often, and what you measure. We handle strategy, content creation, scheduling, and reporting so your channels stay active and on brand.",
        "localParagraph": "The Yakima Valley has a strong sense of place: ag, wine, outdoor life, and community pride. Generic branded posts fall flat here. We create content that fits harvest season, local events, and the mix of audiences many Valley businesses serve, including bilingual communities where that matters for your brand.",
        "why_heading": "Social Content Rooted in Yakima Identity",
        "why_body": "We grow followers with people likely to become customers, not random engagement. Consistent voice, local context, and clear calls to action keep your social channels working for the business.",
        "faqs": [
            ("What platforms work best for Yakima businesses?", "Facebook still drives local discovery for many Valley customers. Instagram fits visual brands like wineries and contractors. LinkedIn helps B2B and professional services. We recommend the right mix for your audience."),
            ("How often should my Yakima business post?", "Most businesses do well with 3 to 5 posts per week. Consistency and variety matter more than posting every day with weak content."),
            ("Can you create content for Yakima's ag and wine culture?", "Yes. Seasonal storytelling, harvest content, and local proof perform well for Valley brands."),
            ("Do you run paid social ads for Yakima businesses?", "Yes. We manage Facebook and Instagram ads with geographic targeting across the Valley."),
            ("How do you measure social media results?", "Follower growth, reach, engagement, website clicks, and leads. Monthly reports focus on business outcomes, not just likes."),
            ("Can you manage social for multiple Valley locations?", "Yes. Unified or location-specific strategies for Yakima, Selah, Union Gap, and nearby towns."),
        ],
    },
    "ellensburg-wa": {
        "metaDescription": "Social media management for Ellensburg businesses. Content strategies for Facebook, Instagram, and LinkedIn that reach CWU students and Kittitas County residents.",
        "hero_headline": "Ellensburg Social Media for Students and Lifelong Locals",
        "hero_subheadline": "Facebook, Instagram, and LinkedIn for Ellensburg Businesses",
        "hero_body": "Ellensburg's audience splits between CWU students on Instagram and longtime residents on Facebook. One generic posting schedule misses half the room. We build social plans that speak to both with the right content on the right platforms.",
        "intro": "Effective social media starts with knowing who follows you and who should. We plan content calendars, create posts, manage engagement, and report on growth so Ellensburg businesses stay visible without living on their phones.",
        "localParagraph": "Students respond to visual, timely content. County residents respond to trust and community ties. Rodeo season, university events, and Main Street businesses all offer real content hooks if you use them honestly. We help Ellensburg brands show up in both feeds without sounding like a corporate template.",
        "why_heading": "Social Strategy for Ellensburg's Two Audiences",
        "why_body": "We bridge student and resident audiences with platform-specific content, paid boosts when they help, and reporting that shows what drives foot traffic and inquiries.",
        "faqs": [
            ("How do I reach CWU students on social media?", "Instagram and short-form video perform well. We use campus-adjacent targeting and content that matches student habits during the academic year."),
            ("What works for longtime Ellensburg residents?", "Facebook community content, local stories, and behind-the-scenes posts that build trust over time."),
            ("How often should my Ellensburg business post?", "3 to 4 quality posts per week is a solid baseline for most local businesses."),
            ("Do you run paid social for Ellensburg businesses?", "Yes. Geo-targeted Facebook and Instagram campaigns for Kittitas County audiences."),
            ("Can you reflect Ellensburg's rodeo and local culture?", "Yes, when it fits your brand. We use local touchstones authentically, not as decoration."),
            ("How do you measure social ROI in Ellensburg?", "Reach, engagement, clicks, and lead inquiries with monthly plain-language reports."),
        ],
    },
    "tri-cities-wa": {
        "metaDescription": "Social media management for Kennewick, Pasco, and Richland businesses. Growth strategies for Facebook, Instagram, and LinkedIn across the Columbia Basin.",
        "hero_headline": "Tri-Cities Social Media for Kennewick, Pasco, and Richland",
        "hero_subheadline": "Facebook, Instagram, and LinkedIn for Columbia Basin Businesses",
        "hero_body": "The Tri-Cities is not one audience. Pasco, Richland, and Kennewick engage differently on social. We build content strategies that respect those differences and grow your following across the full metro.",
        "intro": "Social growth requires consistent posting, clear brand voice, and content people actually want to share. We handle planning, creation, publishing, and optimization so your Tri-Cities brand stays active across platforms.",
        "localParagraph": "Pasco's bilingual community, Richland's professional base, and Kennewick's hospitality and retail economy each respond to different tones and formats. We build content options that fit each community, including bilingual posts when appropriate, without treating the Basin like a single generic market.",
        "why_heading": "Social Built for Three Distinct Communities",
        "why_body": "We grow followers across Kennewick, Pasco, and Richland with messaging and visuals tuned to each city's audience, not one-size-fits-all posts.",
        "faqs": [
            ("Do you create bilingual social content for Pasco audiences?", "Yes, when it matches your customers and brand. Bilingual posts can expand reach in the Tri-Cities."),
            ("Which platforms work best in the Tri-Cities?", "Facebook for broad local reach, Instagram for visual brands, LinkedIn for B2B and professional services. We tailor the mix to your business."),
            ("How often should a Tri-Cities business post?", "3 to 5 posts per week is typical. We prioritize consistency and quality."),
            ("Do you run paid social ads in the Tri-Cities?", "Yes. Geo-targeted campaigns across Kennewick, Pasco, and Richland."),
            ("Can you manage social for businesses serving all three cities?", "Yes. Unified branding with city-specific content when it helps performance."),
            ("How do you measure Tri-Cities social results?", "Growth, engagement, clicks, and leads with monthly reporting tied to business goals."),
        ],
    },
    "spokane-wa": {
        "metaDescription": "Social media management for Spokane and Inland Northwest businesses. Strategy and content for Facebook, Instagram, and LinkedIn in a competitive regional market.",
        "hero_headline": "Spokane Social Media That Competes for Attention",
        "hero_subheadline": "Facebook, Instagram, and LinkedIn for Spokane Businesses",
        "hero_body": "Spokane feeds are crowded. Businesses that post randomly get buried. We build social strategies with consistent content, local relevance, and paid support when it accelerates growth.",
        "intro": "Social media should support your brand and drive measurable action. We plan content, produce posts, manage channels, and report on what moves the needle for Spokane businesses.",
        "localParagraph": "Neighborhood pride, local events, and community involvement perform well in Spokane when they are genuine. We create content that feels Inland Northwest without clichés, plus the professional polish healthcare, legal, and retail brands need to look credible next to larger competitors.",
        "why_heading": "Spokane Social With Regional Standards",
        "why_body": "Consistent voice, strong visuals, and clear calls to action help Spokane businesses stay top of mind when customers are ready to buy.",
        "faqs": [
            ("What platforms should Spokane businesses prioritize?", "Depends on your audience. Facebook for local consumers, Instagram for visual brands, LinkedIn for B2B. We recommend based on your goals."),
            ("How often should my Spokane business post?", "3 to 5 posts per week works for most businesses. We build calendars that stay sustainable."),
            ("Do you run paid social for Spokane businesses?", "Yes. Targeted Facebook and Instagram ads with conversion-focused creative."),
            ("Can you create community-focused Spokane content?", "Yes. Local events, partnerships, and neighborhood stories when they fit your brand."),
            ("How do you measure social media success?", "Reach, engagement, website traffic, and leads. Reports explain what is working in plain language."),
            ("Can you manage multiple Spokane-area locations?", "Yes. Location-specific or unified strategies for Spokane Valley and surrounding areas."),
        ],
    },
    "boise-id": {
        "metaDescription": "Social media management for Boise and Treasure Valley businesses. Content and growth strategy for Facebook, Instagram, and LinkedIn in Idaho's busiest market.",
        "hero_headline": "Boise Social Media for a Crowded Feed",
        "hero_subheadline": "Facebook, Instagram, and LinkedIn for Treasure Valley Businesses",
        "hero_body": "Boise customers scroll past generic content all day. To grow, you need a clear voice, consistent posting, and creative that feels local. We build social plans that help Treasure Valley businesses stand out without trying too hard.",
        "intro": "We handle strategy, content creation, scheduling, community management, and paid social so your Boise brand stays visible and on message.",
        "localParagraph": "Outdoor culture, neighborhood loyalty, and fast growth shape how Boise buys. We create social content that reflects those realities: real projects, real people, direct language. No stock mountain-badge posts unless that is actually your brand.",
        "why_heading": "Treasure Valley Social That Scales",
        "why_body": "As you add services or locations, your social presence should stay coherent. We build systems and content libraries that grow with your business.",
        "faqs": [
            ("What platforms work best in Boise?", "Instagram and Facebook lead for many consumer brands. LinkedIn for B2B. TikTok for younger audiences when relevant."),
            ("How often should a Boise business post?", "3 to 5 times per week is a strong baseline. We adjust based on your capacity and results."),
            ("Do you run paid social in the Treasure Valley?", "Yes. Geo-targeted campaigns for Boise, Meridian, and Nampa."),
            ("Can you help a new Boise business build a following from zero?", "Yes. Content strategy, posting consistency, and paid boosts to reach ideal local audiences."),
            ("How do you measure social ROI?", "Follower quality, engagement, clicks, and leads. Monthly reporting tied to business goals."),
            ("Can you match Boise's outdoor and lifestyle aesthetic?", "Yes, when it fits your brand authentically. We avoid generic clichés."),
        ],
    },
    "coeur-dalene-id": {
        "metaDescription": "Social media management for Coeur d'Alene and North Idaho businesses. Visual content and strategy for Facebook, Instagram, and LinkedIn in lake country.",
        "hero_headline": "Coeur d'Alene Social Media for Visitors and Locals",
        "hero_subheadline": "Facebook, Instagram, and LinkedIn for North Idaho Businesses",
        "hero_body": "CDA social feeds are visual and competitive. Summer visitors and year-round locals both judge your brand by what they see online. We create content that looks polished without feeling like a resort template.",
        "intro": "We plan, create, and publish social content with a strategy behind it: brand voice, posting cadence, seasonal campaigns, and metrics that matter.",
        "localParagraph": "Marinas, restaurants, lodging, and home services need different social tones, but all need authenticity. We build North Idaho content that works in peak season and keeps local engagement strong in the off season.",
        "why_heading": "Lake Country Social Without the Clichés",
        "why_body": "Elevated visuals when they help, honest local voice always. We grow audiences with people who book, visit, or hire, not just like posts.",
        "faqs": [
            ("What platforms work best in Coeur d'Alene?", "Instagram for visual hospitality and recreation. Facebook for local service businesses. LinkedIn for professional firms."),
            ("Can you handle seasonal social campaigns?", "Yes. We ramp content and paid spend for summer peaks and maintain local presence year round."),
            ("How often should a CDA business post?", "3 to 5 posts per week for most businesses. Quality over volume."),
            ("Do you run paid social in North Idaho?", "Yes. Geo-targeted ads for CDA, Post Falls, and Hayden."),
            ("Can you create visual content for hospitality brands?", "Yes. Photography direction, reels, and stories that showcase experiences without looking stock."),
            ("How do you measure social results?", "Reach, engagement, bookings, and leads with monthly reporting."),
        ],
    },
    "tacoma-wa": {
        "metaDescription": "Social media management for Tacoma and Pierce County businesses. Community-focused content for Facebook, Instagram, and LinkedIn in the South Sound.",
        "hero_headline": "Tacoma Social Media With Neighborhood Credibility",
        "hero_subheadline": "Facebook, Instagram, and LinkedIn for Tacoma Businesses",
        "hero_body": "Tacoma customers notice when a brand shows up in the community. They also ignore content that could belong to any city. We build social strategies with local proof, consistent voice, and creative that earns Pierce County attention.",
        "intro": "We manage social end to end: strategy, content, publishing, engagement, and paid campaigns when they accelerate growth.",
        "localParagraph": "Local partnerships, events, and behind-the-scenes content perform well in Tacoma when they are real. We help South Sound businesses tell those stories alongside promotional posts so feeds feel human, not corporate.",
        "why_heading": "South Sound Social With Local Proof",
        "why_body": "Community credibility plus professional execution. Your social channels should reflect both as Tacoma keeps growing.",
        "faqs": [
            ("What platforms should Tacoma businesses use?", "Facebook for local reach, Instagram for visual brands, LinkedIn for professional services. We tailor to your audience."),
            ("How often should my Tacoma business post?", "3 to 5 posts per week is typical. We build sustainable calendars."),
            ("Do you run paid social for Tacoma businesses?", "Yes. Geo-targeted Pierce County campaigns."),
            ("Can you highlight community involvement?", "Yes. Local events and partnerships when they fit your brand authentically."),
            ("How do you measure social success?", "Engagement, reach, clicks, and leads with clear monthly reports."),
            ("Can you manage social for multiple Pierce County locations?", "Yes. Unified or location-specific approaches."),
        ],
    },
    "vancouver-wa": {
        "metaDescription": "Social media management for Vancouver, WA and Clark County businesses. Local content for Facebook, Instagram, and LinkedIn on the Washington side.",
        "hero_headline": "Vancouver Social Media for Clark County Pride",
        "hero_subheadline": "Facebook, Instagram, and LinkedIn for Washington-Side Businesses",
        "hero_body": "Clark County customers want to support Washington businesses. Your social content should make that choice easy with local proof, clear service area messaging, and a voice that sounds like the Washington side, not Portland.",
        "intro": "We build social strategies that reinforce your Clark County identity: what you do, where you serve, and why local customers choose you.",
        "localParagraph": "Projects, reviews, community involvement, and Washington-specific messaging help Vancouver businesses stand out from Oregon competitors in the feed. We create that content consistently so your brand stays visible when customers are ready to hire.",
        "why_heading": "Clark County Social, Clearly Washington",
        "why_body": "Local proof and professional creative so your social presence matches the quality customers expect on the Washington side of the river.",
        "faqs": [
            ("What platforms work best in Vancouver WA?", "Facebook for local consumers, Instagram for visual brands, LinkedIn for B2B. We match platforms to your goals."),
            ("How often should my Vancouver business post?", "3 to 5 posts per week for most Clark County businesses."),
            ("Do you run paid social in Clark County?", "Yes. Geo-targeted campaigns for Vancouver, Camas, and Ridgefield."),
            ("Can social content emphasize Washington-side identity?", "Yes. Local proof and Clark County messaging are core to our approach."),
            ("How do you measure social ROI?", "Reach, engagement, website clicks, and leads with monthly reports."),
            ("Can you manage multiple Clark County locations?", "Yes. Location-specific content when it helps."),
        ],
    },
    "wenatchee-wa": {
        "metaDescription": "Social media management for Wenatchee and NCW businesses. Content rooted in orchard country, outdoor recreation, and regional community events.",
        "hero_headline": "Wenatchee Social Media for NCW's Regional Audience",
        "hero_subheadline": "Facebook, Instagram, and LinkedIn for North Central Washington",
        "hero_body": "Wenatchee businesses serve customers across the valley. Social content should reflect that regional role with local storytelling, seasonal hooks, and posts people in East Wenatchee and Leavenworth actually share.",
        "intro": "We plan and publish social content that keeps your brand visible across NCW: strategy, creative, scheduling, and reporting included.",
        "localParagraph": "Orchard season, outdoor recreation, and community events give Wenatchee brands natural content angles. We use them without overdoing the apple clichés, and we tailor posts for the towns that send you customers.",
        "why_heading": "Regional Social With Local Roots",
        "why_body": "Content that reaches beyond city limits while still feeling grounded in Wenatchee and the valley communities you serve.",
        "faqs": [
            ("What platforms work best in Wenatchee?", "Facebook for broad local reach, Instagram for ag, food, and tourism brands, LinkedIn for professional services."),
            ("Can you create seasonal content for NCW?", "Yes. Harvest, tourism peaks, and winter campaigns aligned to your business calendar."),
            ("How often should a Wenatchee business post?", "3 to 5 posts per week is a solid target for most businesses."),
            ("Do you run paid social in NCW?", "Yes. Geo-targeted campaigns across your service area."),
            ("Can you reach customers in East Wenatchee and Leavenworth?", "Yes. Content and targeting reflect your regional draw."),
            ("How do you measure social results?", "Growth, engagement, clicks, and leads with monthly plain-language reports."),
        ],
    },
    "walla-walla-wa": {
        "metaDescription": "Social media management for Walla Walla wine country and local businesses. Visual storytelling for Facebook, Instagram, and LinkedIn.",
        "hero_headline": "Walla Walla Social Media for Wine Country Audiences",
        "hero_subheadline": "Facebook, Instagram, and LinkedIn for Wine Country and Local Business",
        "hero_body": "Walla Walla social feeds are visual and competitive. Visitors and locals both expect quality. We create content that showcases your brand beautifully without looking like every other tasting room account.",
        "intro": "We handle strategy, visual content, posting, and paid social so your Walla Walla brand stays active through harvest, events, and the quieter months.",
        "localParagraph": "Releases, events, behind-the-scenes moments, and local community ties all perform well here when they are authentic. We build content calendars that balance tourism season pushes with year-round local engagement for wineries, hospitality, and service businesses alike.",
        "why_heading": "Social That Meets Wine Country Standards",
        "why_body": "Strong visuals and clear calls to action so social supports tastings, bookings, and local loyalty at the same time.",
        "faqs": [
            ("What platforms work best in Walla Walla?", "Instagram for visual brands and tourism. Facebook for local service businesses and events. LinkedIn for professional firms."),
            ("Can you create content for winery releases and events?", "Yes. Launch posts, event promotion, and stories that drive visits and DTC interest."),
            ("How often should a Walla Walla business post?", "3 to 5 posts per week, with more during peak event seasons when relevant."),
            ("Do you run paid social in wine country?", "Yes. Targeted campaigns for weekends, events, and high-intent local keywords."),
            ("Can you serve non-wine Walla Walla businesses?", "Yes. Restaurants, hotels, retail, and trades all benefit from strong social here."),
            ("How do you measure social ROI?", "Reach, engagement, website traffic, bookings, and leads with monthly reporting."),
        ],
    },
}

SEO = {
    "yakima-wa": {
        "metaDescription": "Local SEO for Yakima Valley businesses. Rank higher on Google, improve Maps visibility, and turn searches into calls with a team that knows this market.",
        "hero_headline": "Yakima SEO That Puts You in Front of Valley Customers",
        "hero_subheadline": "Helping Yakima Businesses Rank Higher and Grow Faster",
        "hero_body": "Most Yakima customers search before they call. If you are not on page one, you are invisible to a large share of that demand. We build SEO strategies for Valley businesses based on how people here actually search.",
        "intro": "SEO is how you show up when customers search on Google without paying for every click. We handle technical fixes, content, and local signals so your site earns rankings over time.",
        "localParagraph": "Yakima's economy mixes ag, wine, healthcare, trades, and retail. Each niche searches differently. A contractor in Selah and a winery on the tasting loop need different keyword strategies. We build local SEO around your services, neighborhoods, and seasons instead of copying a national checklist.",
        "features": [
            "Keyword plans tailored to your Yakima industry, whether you are in healthcare, hospitality, ag, or home services.",
            "Stronger visibility across Yakima, Selah, Union Gap, and Valley searches that drive real local customers.",
            "Accurate listings on Google Maps, Apple Maps, Yelp, and local directories so customers find you everywhere they look.",
            "Faster pages, clean code, mobile optimization, and structured data so Google trusts your Yakima site.",
            "Steady expansion into more keywords your Valley customers type each month.",
            "More qualified organic traffic that turns into calls, form fills, and foot traffic.",
        ],
        "why_heading": "SEO Strategy Built Around Yakima Search Behavior",
        "why_body": "We are not guessing from out of state. We build custom search plans around your services, competition, and goals so rankings turn into revenue.",
        "faqs": [
            ("What is SEO and why does my Yakima business need it?", "SEO helps your site rank higher in Google results. When someone searches for your service in Yakima, you want to appear before competitors. Most people never scroll past page one."),
            ("How long does SEO take to work in Yakima?", "Many businesses see movement in 3 to 4 months, with stronger gains over 6 to 12 months. SEO compounds over time unlike ads that stop when spend stops."),
            ("Do you offer local SEO for Yakima specifically?", "Yes. Google Business Profile, local citations, and location content are core to our Yakima work."),
            ("Can SEO help me show up in AI search results?", "Yes. Authority, relevance, and trust signals help in traditional Google and newer AI-driven results."),
            ("What Yakima industries do you work with?", "Wineries, contractors, healthcare, restaurants, retail, and professional services across the Valley."),
            ("How is YB different from other SEO agencies?", "We understand the Yakima market, report in plain language, and build strategy for your business, not a template package."),
        ],
    },
    "ellensburg-wa": {
        "metaDescription": "SEO for Ellensburg and Kittitas County businesses. Custom search strategies for CWU traffic, locals, and Central Washington customers.",
        "hero_headline": "Ellensburg SEO for Kittitas County Growth",
        "hero_subheadline": "Helping Ellensburg Businesses Get Found Online",
        "hero_body": "Ellensburg customers search on Google before they visit Main Street or call a contractor. Strong local SEO captures students, county residents, and I-90 travelers who need your service now.",
        "intro": "SEO improves your visibility in Google without paying per click. We handle the technical work, content, and local signals so you can focus on running your business.",
        "localParagraph": "Ellensburg sits between university traffic and ranch country. That means multiple search audiences and less room for generic content. We target Kittitas County keywords, optimize your Google Business Profile, and build pages that speak to how Ellensburg customers actually search.",
        "features": [
            "Keyword research focused on Ellensburg and Kittitas County searches, not broad terms that bring the wrong traffic.",
            "Visibility with CWU students, faculty, local families, and county residents actively looking for your services.",
            "Consistent presence on Google Maps, Bing, Yelp, and local directories across Central Washington.",
            "Technical SEO that keeps your Ellensburg site fast, structured, and aligned with Google's standards.",
            "Growing keyword coverage month over month for the searches that matter in Ellensburg.",
            "More qualified organic visitors who are already looking for what you sell locally.",
        ],
        "why_heading": "SEO Built for Ellensburg's Mixed Market",
        "why_body": "University town plus county hub requires targeted content and local signals. We build Ellensburg SEO that reaches the audiences driving your revenue.",
        "faqs": [
            ("Why does SEO matter for my Ellensburg business?", "Customers search before they buy. Ranking locally captures students, residents, and travelers you would otherwise miss."),
            ("How long before SEO results in Ellensburg?", "Early movement often appears in 3 to 4 months, with stronger traffic in 6 to 12 months. Less saturated niches can move faster."),
            ("Do you do local SEO for Kittitas County?", "Yes. Profile optimization, citations, and location-specific content are standard."),
            ("Can SEO reach both students and longtime residents?", "Yes. We target multiple keyword groups and content types for different audiences."),
            ("What Ellensburg industries do you serve?", "Restaurants, retail, contractors, medical offices, and ag businesses throughout the county."),
            ("Why choose YB over a national SEO agency?", "We treat Ellensburg as a real market with real search patterns, not a generic small town."),
        ],
    },
    "tri-cities-wa": {
        "metaDescription": "SEO for Kennewick, Pasco, and Richland businesses. Multi-city local search strategies that grow visibility across the Columbia Basin.",
        "hero_headline": "Tri-Cities SEO for Kennewick, Pasco, and Richland",
        "hero_subheadline": "Helping Columbia Basin Businesses Rank Higher",
        "hero_body": "Tri-Cities customers search from three cities with different habits. SEO that only targets one zip code leaves leads on the table. We build search strategies that cover the full metro.",
        "intro": "SEO puts your business in front of high-intent searches without ongoing ad spend. We manage strategy, technical health, and content so rankings grow across the Basin.",
        "localParagraph": "Kennewick retail searches differ from Pasco bilingual queries and Richland professional services. We build multi-location SEO with city-aware pages, map optimization, and content that signals you serve the entire Tri-Cities metro, not just one neighborhood.",
        "features": [
            "Keyword strategies targeting Kennewick, Pasco, and Richland search patterns separately where competition differs.",
            "Metro-wide visibility so customers in all three cities find your business when they search.",
            "Accurate listings and citations across the Tri-Cities and Columbia Basin directories.",
            "Technical improvements that help Google trust your site across a multi-city service area.",
            "Expanding keyword rankings month over month in each city you serve.",
            "More organic traffic from qualified searches across the full Tri-Cities market.",
        ],
        "why_heading": "SEO for Three Cities, One Strategy",
        "why_body": "We do not flatten the Tri-Cities into one target. We build search visibility that matches how you actually operate across Kennewick, Pasco, and Richland.",
        "faqs": [
            ("Do you do SEO for all three Tri-Cities?", "Yes. Kennewick, Pasco, and Richland are all part of our local SEO approach."),
            ("How long does Tri-Cities SEO take?", "Many businesses see early gains in 3 to 4 months, with stronger results over 6 to 12 months."),
            ("Can SEO help bilingual Pasco customers find me?", "Yes. Content and optimization can target how Pasco audiences search."),
            ("What industries do you serve in the Tri-Cities?", "Healthcare, legal, construction, wineries, hospitality, and professional services across the Basin."),
            ("Do SEO and Google Ads work together here?", "Yes. Ads for immediate visibility, SEO for long-term rankings. Many Tri-Cities businesses use both."),
            ("How is YB different from other agencies?", "We understand the three-city dynamic and build strategy around it."),
        ],
    },
    "spokane-wa": {
        "metaDescription": "SEO for Spokane and Inland Northwest businesses. Competitive local search strategies for Eastern Washington's largest market.",
        "hero_headline": "Spokane SEO That Competes in a Tough Market",
        "hero_subheadline": "Helping Spokane Businesses Rank Higher and Win More Leads",
        "hero_body": "Spokane search results are competitive. National brands and sharp local firms fight for the same keywords. We build SEO strategies that help Inland Northwest businesses earn visibility and convert it.",
        "intro": "SEO is long-term visibility in Google. We handle technical SEO, content, and local signals so your Spokane site compounds in value over time.",
        "localParagraph": "From South Hill to Spokane Valley, customers search with local intent. We build competitive keyword strategies, fix technical issues holding rankings back, and create content that earns trust in a market where buyers compare multiple options before calling.",
        "features": [
            "Industry-specific keyword strategy for Spokane's competitive search landscape.",
            "Visibility across Spokane, Spokane Valley, Liberty Lake, and Inland Northwest searches.",
            "Strong map pack presence and accurate citations across local directories.",
            "Site speed, mobile performance, and structured data tuned for Spokane rankings.",
            "Month-over-month growth in keywords that drive high-intent local traffic.",
            "More organic visits from customers ready to hire or buy in Spokane.",
        ],
        "why_heading": "Spokane SEO With Accountability",
        "why_body": "Clear goals, monthly reporting, and strategy adjustments when something is not working. No black-box promises.",
        "faqs": [
            ("Why does my Spokane business need SEO?", "Buyers compare online first. Ranking high captures demand before competitors do."),
            ("How long does Spokane SEO take?", "Movement often starts in 3 to 4 months. Competitive categories may take longer to break through."),
            ("Do you do local SEO for Spokane Valley too?", "Yes. We target the neighborhoods and cities that send you revenue."),
            ("Can SEO help me compete with national brands?", "Yes. Local relevance and strong technical SEO help local businesses win high-intent searches."),
            ("What Spokane industries do you work with?", "Healthcare, home services, legal, retail, and professional services across Eastern Washington."),
            ("How is YB different from other SEO agencies?", "Strategy built for Spokane competition, not generic small-business SEO templates."),
        ],
    },
    "boise-id": {
        "metaDescription": "SEO for Boise and Treasure Valley businesses. Local search strategies for Idaho's fastest-growing, most competitive market.",
        "hero_headline": "Boise SEO for a Noisy Search Market",
        "hero_subheadline": "Helping Treasure Valley Businesses Rank Higher",
        "hero_body": "Boise adds competitors every quarter. If your site is slow, thin on content, or missing local signals, you fall behind fast. We build SEO that helps Treasure Valley businesses earn rankings and keep them.",
        "intro": "SEO delivers organic visibility without paying per click. We manage technical health, content, and local optimization for Boise businesses ready to invest long term.",
        "localParagraph": "Boise, Meridian, and Nampa searches are crowded in home services, medical, legal, and outdoor brands. We research the keywords that match your margins, build location pages where they help, and fix the technical issues that block growth.",
        "features": [
            "Keyword strategy tuned to Boise industries and the terms that convert, not just high volume.",
            "Visibility across Boise, Meridian, Nampa, and Treasure Valley local searches.",
            "Optimized Google Business Profile and citations across Idaho directories.",
            "Technical SEO for speed, mobile, and structured data in a competitive market.",
            "Steady keyword expansion as your Boise rankings grow month over month.",
            "More qualified organic traffic that turns into leads across the Valley.",
        ],
        "why_heading": "Treasure Valley SEO That Scales",
        "why_body": "Start focused, expand what works. We align SEO with your growth stage instead of selling a bloated package on day one.",
        "faqs": [
            ("How long does Boise SEO take?", "Early movement in 3 to 4 months is common. Competitive niches may need 6 to 12 months for strong gains."),
            ("Do you target Meridian and Nampa too?", "Yes. Service area SEO covers the Treasure Valley markets you serve."),
            ("Is SEO worth it in competitive Boise categories?", "Yes, when strategy matches your margins and competition. We assess honestly before recommending."),
            ("Can SEO work with Google Ads?", "Yes. Many Boise businesses run ads now and build SEO for long-term organic traffic."),
            ("What industries do you serve in Boise?", "Home services, medical, legal, food and beverage, outdoor brands, and professional services."),
            ("How is YB different?", "Realistic timelines, plain reporting, and strategy tied to lead quality."),
        ],
    },
    "coeur-dalene-id": {
        "metaDescription": "SEO for Coeur d'Alene and North Idaho businesses. Local search for tourism season and year-round Kootenai County customers.",
        "hero_headline": "Coeur d'Alene SEO for Lake Country Businesses",
        "hero_subheadline": "Helping North Idaho Businesses Get Found Online",
        "hero_body": "CDA businesses need visibility with summer visitors and loyal locals. SEO should capture both: destination searches when tourism peaks and service keywords that keep leads flowing in winter.",
        "intro": "SEO helps customers find you in Google organically. We build local strategies for North Idaho businesses with seasonal calendars in mind.",
        "localParagraph": "Post Falls, Hayden, and Coeur d'Alene searches mix hospitality, recreation, and home services. We optimize profiles, build content for visitor and local intent, and improve technical health so your site ranks when demand spikes and when it does not.",
        "features": [
            "Keywords for CDA hospitality, recreation, and local service businesses.",
            "Visibility across Coeur d'Alene, Post Falls, Hayden, and North Idaho searches.",
            "Accurate map listings and citations for Kootenai County directories.",
            "Fast, mobile-friendly technical SEO for customers searching on the go.",
            "Growing keyword coverage through seasonal and year-round content.",
            "More organic traffic from tourists and locals ready to book or call.",
        ],
        "why_heading": "SEO That Respects CDA Seasonality",
        "why_body": "We plan content and optimization around your revenue calendar so search visibility matches when you need it most.",
        "faqs": [
            ("Does SEO help CDA tourism businesses?", "Yes. Destination keywords and local SEO capture visitors planning trips online."),
            ("How long does North Idaho SEO take?", "Many businesses see movement in 3 to 4 months, with stronger results over 6 to 12 months."),
            ("Do you target Post Falls and Hayden?", "Yes. We cover your full Kootenai County service area."),
            ("Can SEO work in the off season?", "Yes. Local service keywords and content keep leads coming when tourism slows."),
            ("What industries do you serve in CDA?", "Hospitality, recreation, home services, retail, and professional firms."),
            ("How is YB different?", "We understand lake country seasonality and build strategy around it."),
        ],
    },
    "tacoma-wa": {
        "metaDescription": "SEO for Tacoma and Pierce County businesses. Local search strategies for South Sound companies competing regionally.",
        "hero_headline": "Tacoma SEO for South Sound Visibility",
        "hero_subheadline": "Helping Tacoma Businesses Rank Higher Online",
        "hero_body": "Tacoma customers search locally but compare regionally. Your SEO needs neighborhood relevance and the technical strength to compete with larger players. We build both.",
        "intro": "SEO earns organic rankings in Google over time. We handle technical fixes, local signals, and content for Pierce County businesses.",
        "localParagraph": "Lakewood, Tacoma, and broader Pierce County searches each matter. We build local pages, optimize your profile, and create content that reflects how South Sound customers search for contractors, clinics, restaurants, and professional services.",
        "features": [
            "Keyword plans for Tacoma industries and the neighborhoods that send you leads.",
            "Visibility across Tacoma, Lakewood, and Pierce County local searches.",
            "Map pack optimization and citations for South Sound directories.",
            "Technical SEO for speed, mobile, and trust signals Google rewards.",
            "Month-over-month keyword growth for high-intent Tacoma searches.",
            "More organic traffic that converts into calls and form fills.",
        ],
        "why_heading": "Tacoma SEO Without Seattle Pretense",
        "why_body": "Direct communication, realistic goals, and work tied to leads and revenue for Pierce County businesses.",
        "faqs": [
            ("Why does my Tacoma business need SEO?", "Local search drives calls and visits. If you are not visible, competitors capture that demand."),
            ("How long does Tacoma SEO take?", "Many see early gains in 3 to 4 months, with stronger results over 6 to 12 months."),
            ("Do you target Lakewood and Pierce County?", "Yes. We optimize for the cities and neighborhoods you actually serve."),
            ("Can SEO help me compete with Seattle companies?", "Yes. Strong local relevance helps you win South Sound searches."),
            ("What Tacoma industries do you work with?", "Contractors, healthcare, restaurants, retail, and professional services."),
            ("How is YB different?", "Neighborhood-aware strategy and reporting focused on leads."),
        ],
    },
    "vancouver-wa": {
        "metaDescription": "SEO for Vancouver, WA and Clark County businesses. Washington-side local search that competes with Portland dominance.",
        "hero_headline": "Vancouver SEO for Clark County Customers",
        "hero_subheadline": "Helping Washington-Side Businesses Rank Higher",
        "hero_body": "Portland brands often dominate search results. Clark County customers still want Washington providers. Local SEO with clear location signals helps you win those searches.",
        "intro": "SEO improves organic visibility in Google. We build Clark County strategies that emphasize your Washington presence and service area.",
        "localParagraph": "Vancouver, Camas, and Ridgefield each have distinct search patterns. We create location content, optimize listings, and fix technical issues so you rank for Washington-side queries instead of getting lost behind Oregon competitors.",
        "features": [
            "Keywords targeting Vancouver WA searches distinct from Portland results.",
            "Visibility across Vancouver, Camas, Ridgefield, and Clark County.",
            "Google Business Profile and citation work focused on the Washington side.",
            "Technical SEO that helps Google understand your Clark County service area.",
            "Steady keyword expansion for local searches that drive Washington leads.",
            "More organic traffic from customers who want a local Washington provider.",
        ],
        "why_heading": "Clark County SEO, Measured",
        "why_body": "Track visibility and leads by city so you know what is working in Vancouver versus Camas or Ridgefield.",
        "faqs": [
            ("Can SEO help me rank for Vancouver WA instead of Portland?", "Yes. Local pages, citations, and profile optimization support Washington-side visibility."),
            ("How long does Clark County SEO take?", "Movement often starts in 3 to 4 months, with stronger gains over 6 to 12 months."),
            ("Do you target Camas and Ridgefield?", "Yes. We cover your full Clark County service area."),
            ("Why do Vancouver businesses struggle with SEO?", "Portland competition and unclear location signals. We fix both."),
            ("What industries do you serve in Vancouver?", "Contractors, healthcare, legal, retail, and professional services."),
            ("How is YB different?", "We specialize in the Portland shadow problem Clark County businesses face."),
        ],
    },
    "wenatchee-wa": {
        "metaDescription": "SEO for Wenatchee and North Central Washington businesses. Regional local search for the Apple Capital and surrounding valley towns.",
        "hero_headline": "Wenatchee SEO for NCW's Regional Hub",
        "hero_subheadline": "Helping North Central Washington Businesses Rank Higher",
        "hero_body": "Wenatchee serves customers from across the valley. Your SEO should too. We build regional search strategies that capture traffic from East Wenatchee, Leavenworth, Chelan, and beyond.",
        "intro": "SEO brings organic visibility in Google without per-click costs. We manage technical health, content, and local signals for NCW businesses.",
        "localParagraph": "Regional providers need service area clarity in search. We optimize for Wenatchee core keywords plus the surrounding towns that send you revenue, with seasonal content for tourism and ag peaks.",
        "features": [
            "Keywords for Wenatchee industries and regional towns in your draw radius.",
            "Visibility across Wenatchee, East Wenatchee, Leavenworth, and NCW searches.",
            "Map listings and citations for North Central Washington directories.",
            "Technical SEO tuned for mobile searchers on the road across the valley.",
            "Month-over-month keyword growth for regional and local intent.",
            "More organic traffic from customers willing to drive to Wenatchee for your service.",
        ],
        "why_heading": "NCW SEO With Geographic Precision",
        "why_body": "We target the communities that send you revenue, not just a pin on the map inside city limits.",
        "faqs": [
            ("Does SEO help Wenatchee regional businesses?", "Yes. Service area pages and local signals capture searches from surrounding towns."),
            ("How long does NCW SEO take?", "Many businesses see movement in 3 to 4 months, with stronger results over 6 to 12 months."),
            ("Do you target East Wenatchee and Leavenworth?", "Yes. We optimize for your full service area."),
            ("Can SEO help seasonal NCW businesses?", "Yes. Content and optimization align with tourism and ag calendars."),
            ("What industries do you serve in Wenatchee?", "Ag, food, healthcare, contractors, hospitality, and retail."),
            ("How is YB different?", "Regional mindset built into keyword and content strategy from day one."),
        ],
    },
    "walla-walla-wa": {
        "metaDescription": "SEO for Walla Walla wine country and local businesses. Search strategies for tourism peaks and year-round community customers.",
        "hero_headline": "Walla Walla SEO for Wine Country and Local Search",
        "hero_subheadline": "Helping Walla Walla Businesses Rank Higher Online",
        "hero_body": "Visitors plan Walla Walla trips on Google. Locals search for providers the same way. SEO should capture both audiences with content and technical work that matches wine country expectations.",
        "intro": "SEO builds organic visibility over time. We create search strategies for wineries, hospitality, and local service businesses in Walla Walla.",
        "localParagraph": "Wine tourism keywords spike on weekends and events. Local service keywords run year round. We balance both with destination content, strong profiles, and technical SEO so your site ranks when visitors plan trips and when neighbors need you tomorrow.",
        "features": [
            "Keywords for wine tourism, events, and local Walla Walla service searches.",
            "Visibility for visitor-intent and resident searches on the same site.",
            "Optimized listings across wine country and local Walla Walla directories.",
            "Technical SEO and speed for mobile travelers researching on the road.",
            "Growing keyword coverage through seasonal and evergreen content.",
            "More organic traffic that converts into tastings, bookings, and local leads.",
        ],
        "why_heading": "SEO That Matches Wine Country Expectations",
        "why_body": "Creative quality and measurable search growth. You should not have to choose one over the other.",
        "faqs": [
            ("Does SEO help Walla Walla wineries?", "Yes. Destination keywords, events, and local SEO drive tasting room and DTC traffic."),
            ("How long does Walla Walla SEO take?", "Early movement in 3 to 4 months is common, with stronger gains over 6 to 12 months."),
            ("Can one SEO strategy target tourists and locals?", "Yes. We structure content for both search intents."),
            ("Do you serve non-wine Walla Walla businesses?", "Yes. Restaurants, hotels, retail, and trades all benefit from local SEO."),
            ("Can SEO help during slow seasons?", "Yes. Local service keywords and content maintain visibility year round."),
            ("How is YB different?", "We understand wine country search patterns and build strategy around them."),
        ],
    },
}


def main():
    write_web_design()
    write_google_ads()
    write_social_media()
    write_seo()
    print("Wrote data/webDesignLocations.js")
    print("Wrote data/googleAdsLocations.js")
    print("Wrote data/socialMediaLocations.js")
    print("Wrote data/seoLocations.js")


if __name__ == "__main__":
    main()
