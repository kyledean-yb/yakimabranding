#!/usr/bin/env python3
"""One-shot generator for humanized branding + location hub copy."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BRANDING = [
    {
        "slug": "yakima-wa",
        "city": "Yakima",
        "state": "WA",
        "region": "Yakima Valley",
        "schema_locality": "Yakima",
        "localSignals": ["Yakima, WA", "Selah, WA", "Union Gap, WA", "Yakima Valley"],
        "metaDescription": "Brand strategy, logo design, and identity systems for Yakima Valley businesses. YB Marketing builds brands that look professional from the tasting room to the job site.",
        "hero": {
            "headline": "Yakima Branding That People Actually Remember",
            "subheadline": "Brand Strategy, Identity, and Design for Yakima Valley Businesses",
            "body": "Customers in the Yakima Valley notice when a business looks put together. From wine labels to contractor trucks, we build brand identities that fit this market and stay consistent as you grow.",
        },
        "whatWeDo": {
            "heading": "Logo Design, Brand Strategy, and Identity Systems",
            "intro": "We help Yakima businesses look as good in person as they do online. That means a clear brand story, a logo that holds up on a truck door and a phone screen, and standards your team can actually use.",
            "localParagraph": "Yakima is not a generic small town. You have orchard families who have been here for generations, new wineries competing for shelf space, and contractors who live off referrals. A brand that works here should feel local without looking homemade. We have built identities for Valley wineries, medical offices, retailers, and trades businesses, and we know which details matter to your customers.",
        },
        "whyYb": {
            "heading": "Branding Rooted in the Yakima Valley",
            "body": "We are based in Yakima. That shows up in how we work: we talk to your customers, we understand seasonal swings, and we design brands that still look right on a sign in January fog or on Instagram during harvest.",
        },
    },
    {
        "slug": "ellensburg-wa",
        "city": "Ellensburg",
        "state": "WA",
        "region": "Kittitas County",
        "schema_locality": "Ellensburg",
        "localSignals": ["Ellensburg, WA", "Kittitas County", "CWU", "Central Washington"],
        "metaDescription": "Branding and logo design for Ellensburg and Kittitas County businesses. YB Marketing builds identities that work for locals, students, and I-90 corridor traffic.",
        "hero": {
            "headline": "Ellensburg Branding for a Town That Knows Everyone",
            "subheadline": "Brand Identity and Design for Kittitas County Businesses",
            "body": "In Ellensburg, your logo shows up at the rodeo, on campus, and in the group text when someone asks for a recommendation. We build brands that earn trust in a market where reputation still travels fast.",
        },
        "whatWeDo": {
            "heading": "Identity Design for Kittitas County Businesses",
            "intro": "Ellensburg businesses often wear two hats: serving longtime residents and catching traffic from CWU and the I-90 corridor. We build brands that read clearly to both without feeling like they were designed somewhere else.",
            "localParagraph": "A hardware store on Main Street and a startup near campus need different tones, but both need to look credible. We start with who you serve, what you want people to say about you, and where your brand actually shows up. Then we design a system you can use on signage, uniforms, social, and your website without starting from scratch every time.",
        },
        "whyYb": {
            "heading": "Local Branding Without the Small-Town Clichés",
            "body": "We skip the stock western clip art. Ellensburg has real character: university energy, ranching history, outdoor recreation. Your brand should reflect that in a way that feels honest, not like a tourism poster.",
        },
    },
    {
        "slug": "tri-cities-wa",
        "city": "Tri-Cities",
        "state": "WA",
        "region": "Columbia Basin",
        "schema_locality": "Kennewick",
        "localSignals": ["Kennewick, WA", "Pasco, WA", "Richland, WA", "Columbia Basin"],
        "metaDescription": "Branding for Kennewick, Pasco, and Richland businesses. YB Marketing creates identity systems that work across the full Tri-Cities market.",
        "hero": {
            "headline": "Tri-Cities Branding for Three Cities, One Market",
            "subheadline": "Brand Strategy and Design for the Columbia Basin",
            "body": "Kennewick, Pasco, and Richland are not the same customer base. Your brand should feel at home in all three without looking like it was copied from a template. We build identities that travel across the Basin.",
        },
        "whatWeDo": {
            "heading": "Brand Systems Built for the Columbia Basin",
            "intro": "Tri-Cities businesses often serve customers across city lines. We design brands with clear messaging, flexible layouts, and visual language that works whether someone finds you in Pasco, Richland, or Kennewick.",
            "localParagraph": "Pasco's bilingual audience, Richland's professional workforce, and Kennewick's retail and hospitality economy all respond to different cues. The businesses that stand out here usually have a sharp point of view: wine country roots, river culture, energy sector history, or family-owned service. We help you pick the story that is actually yours and build a visual system around it.",
        },
        "whyYb": {
            "heading": "Brands That Hold Up as the Tri-Cities Grows",
            "body": "This market is changing quickly. A brand built on generic stock photos will age fast. We focus on strategy first, then design you can use on trucks, labels, websites, and trade show booths as you expand.",
        },
    },
    {
        "slug": "spokane-wa",
        "city": "Spokane",
        "state": "WA",
        "region": "Inland Northwest",
        "schema_locality": "Spokane",
        "localSignals": ["Spokane, WA", "Spokane Valley", "Liberty Lake", "Inland Northwest"],
        "metaDescription": "Branding and design for Spokane and Inland Northwest businesses. Strategy, logo design, and identity systems built for a competitive regional market.",
        "hero": {
            "headline": "Spokane Branding That Holds Up Next to the Big Players",
            "subheadline": "Brand Strategy and Identity for Inland Northwest Businesses",
            "body": "Spokane customers compare you to national chains and well-funded local competitors. Your brand needs to look professional on first glance and feel local on second glance. That is the balance we build for.",
        },
        "whatWeDo": {
            "heading": "Professional Brand Identity for Spokane Businesses",
            "intro": "Spokane is a real city market. Healthcare groups, law firms, contractors, and retailers all need brands that look intentional. We handle strategy, naming support, logo suites, and the guides that keep your team aligned.",
            "localParagraph": "The Lilac City has its own pride: neighborhoods, events, and a business community that rewards companies who show up locally. We use that context without turning your logo into a postcard. The goal is a brand that competes with larger players while still feeling like it belongs on South Hill or in the Valley.",
        },
        "whyYb": {
            "heading": "Design Quality Without Losing Spokane Character",
            "body": "We have worked across healthcare, trades, hospitality, and professional services in Eastern Washington. You get senior-level strategy and design, not a junior designer guessing at your industry.",
        },
    },
    {
        "slug": "boise-id",
        "city": "Boise",
        "state": "ID",
        "region": "Treasure Valley",
        "schema_locality": "Boise",
        "localSignals": ["Boise, ID", "Meridian, ID", "Nampa, ID", "Treasure Valley"],
        "metaDescription": "Branding for Boise and Treasure Valley businesses. Logo design and identity systems for a fast-growing market with rising design expectations.",
        "hero": {
            "headline": "Boise Branding for a Market That Keeps Getting Busier",
            "subheadline": "Brand Identity and Design for Treasure Valley Businesses",
            "body": "Boise adds new competition every month. A clear brand helps people remember you when they are comparing three quotes or scrolling past ten ads. We build identities that stand out without trying too hard.",
        },
        "whatWeDo": {
            "heading": "Brand Identity for Growing Treasure Valley Companies",
            "intro": "Boise customers notice design quality. Relocated professionals and national brands raised the bar. We help local businesses look established on day one or refresh brands that have not kept pace with the city around them.",
            "localParagraph": "Outdoor lifestyle, tech growth, and neighborhood loyalty all show up in how Boise buys. We talk through your audience, your competitors, and where you want to be in three years before we touch typefaces. That keeps your brand from looking like every other mountain-badge logo in the Valley.",
        },
        "whyYb": {
            "heading": "Brands Built to Scale With Boise",
            "body": "Whether you are launching a new concept or updating a 20-year-old mark, we deliver files, standards, and applications your team can use as you open locations, hire staff, and spend more on marketing.",
        },
    },
    {
        "slug": "coeur-dalene-id",
        "city": "Coeur d'Alene",
        "state": "ID",
        "region": "North Idaho",
        "schema_locality": "Coeur d'Alene",
        "localSignals": ["Coeur d'Alene, ID", "Post Falls, ID", "Hayden, ID", "North Idaho"],
        "metaDescription": "Branding for Coeur d'Alene and North Idaho businesses. Identity design for hospitality, recreation, and year-round local service brands.",
        "hero": {
            "headline": "Coeur d'Alene Branding With Lake Country Taste",
            "subheadline": "Brand Strategy and Design for CDA and Kootenai County",
            "body": "CDA businesses live in a visual market. Visitors photograph storefronts. Locals notice when something looks touristy versus genuinely North Idaho. We design brands that fit the Lake City without leaning on tired pine-tree clichés.",
        },
        "whatWeDo": {
            "heading": "Identity Design for North Idaho Businesses",
            "intro": "Resorts, marinas, restaurants, and home service companies all need different brand tones in Coeur d'Alene. We build systems that look good on a dock sign, a menu, and a Google Business Profile.",
            "localParagraph": "Tourism peaks matter, but your year-round reputation matters more. We design for both: memorable enough for a weekend visitor, trustworthy enough for a Hayden homeowner who needs you back next season. Color, photography direction, and typography all get defined so your team stays consistent.",
        },
        "whyYb": {
            "heading": "Branding That Feels Like It Belongs on the Lake",
            "body": "We know when to use landscape and texture and when to pull back. CDA brands should feel elevated and outdoors-influenced, not like they were ordered from a resort template shop.",
        },
    },
    {
        "slug": "tacoma-wa",
        "city": "Tacoma",
        "state": "WA",
        "region": "South Sound",
        "schema_locality": "Tacoma",
        "localSignals": ["Tacoma, WA", "Lakewood, WA", "Pierce County", "South Sound"],
        "metaDescription": "Branding for Tacoma and Pierce County businesses. Logo design and identity systems for a city with real momentum and strong local loyalty.",
        "hero": {
            "headline": "Tacoma Branding for a City on the Rise",
            "subheadline": "Brand Strategy and Design for South Sound Businesses",
            "body": "Tacoma has rebuilt its reputation block by block. Businesses tied to that story can earn fierce local loyalty. We help you look like part of where the city is going, not where it used to be.",
        },
        "whatWeDo": {
            "heading": "Brand Strategy for Pierce County Businesses",
            "intro": "Tacoma buyers are savvy. They support local when local earns it. We build brands with a real point of view: who you serve, what you refuse to compromise on, and how you show up in the neighborhood.",
            "localParagraph": "Arts, the port, Hilltop, the waterfront: Tacoma gives you plenty of raw material if you use it carefully. We connect your business story to the city in ways that feel earned. You get a logo suite, voice guidance, and standards that work on a food truck wrap or a professional services website.",
        },
        "whyYb": {
            "heading": "Local Story, Professional Execution",
            "body": "You should not have to choose between looking like Tacoma and looking credible next to Seattle competitors. We design brands that do both.",
        },
    },
    {
        "slug": "vancouver-wa",
        "city": "Vancouver",
        "state": "WA",
        "region": "Clark County",
        "schema_locality": "Vancouver",
        "localSignals": ["Vancouver, WA", "Clark County", "Camas, WA", "Ridgefield, WA"],
        "metaDescription": "Branding for Vancouver, WA and Clark County businesses. Identity systems that establish a Washington-side presence distinct from Portland.",
        "hero": {
            "headline": "Vancouver, WA Branding for Clark County Pride",
            "subheadline": "Brand Strategy and Design on the Washington Side",
            "body": "Plenty of Clark County customers want to hire Washington businesses. Your brand should make that choice easy. We build identities that feel rooted here and polished enough to compete with Portland options.",
        },
        "whatWeDo": {
            "heading": "Clark County Brand Identity, Clearly Washington",
            "intro": "Vancouver businesses often fight Portland shadow. We help you own your side of the river with messaging and design that highlight local roots, service area, and the reasons customers choose you.",
            "localParagraph": "Camas tech workers, Ridgefield families, and longtime Vancouver operators all buy differently. We map that before we design. The result is a brand that works on Clark County signage, local sponsorships, and search results when someone types 'near me' from the Washington side.",
        },
        "whyYb": {
            "heading": "A Vancouver Brand That Is Not a Portland Afterthought",
            "body": "We build Clark County identity on purpose: neighborhood language, local proof points, and visual quality that stands up in a market flooded with Oregon competition.",
        },
    },
    {
        "slug": "wenatchee-wa",
        "city": "Wenatchee",
        "state": "WA",
        "region": "North Central Washington",
        "schema_locality": "Wenatchee",
        "localSignals": ["Wenatchee, WA", "East Wenatchee, WA", "Leavenworth, WA", "North Central Washington"],
        "metaDescription": "Branding for Wenatchee and North Central Washington businesses. Logo design and identity for the Apple Capital and regional hub.",
        "hero": {
            "headline": "Wenatchee Branding for the Hub of NCW",
            "subheadline": "Brand Strategy and Design for North Central Washington",
            "body": "People drive to Wenatchee for services they cannot get at home. Your brand should signal that the trip is worth it. We build identities for businesses that serve the Valley and the towns around it.",
        },
        "whatWeDo": {
            "heading": "Regional Brand Identity for Wenatchee Businesses",
            "intro": "From orchard operations to downtown professional offices, Wenatchee brands need to look credible at a regional level. We handle strategy, packaging, signage, and digital applications in one system.",
            "localParagraph": "Apple country gives you strong visual cues if you use them with restraint. We help agricultural, food, and service brands look modern instead of dated. That matters when customers are choosing between you and a competitor in Chelan or East Wenatchee.",
        },
        "whyYb": {
            "heading": "Brands That Match Wenatchee's Regional Role",
            "body": "We design for the customer who sees your truck in Leavenworth, your label in a grocery store, and your website before they call. Consistency builds trust across North Central Washington.",
        },
    },
    {
        "slug": "walla-walla-wa",
        "city": "Walla Walla",
        "state": "WA",
        "region": "Wine Country",
        "schema_locality": "Walla Walla",
        "localSignals": ["Walla Walla, WA", "Wine Country", "Walla Walla County", "Whitman College"],
        "metaDescription": "Branding for Walla Walla wine country and local businesses. Winery identity, label design, and full brand systems for a high-expectation market.",
        "hero": {
            "headline": "Walla Walla Branding for Wine Country Standards",
            "subheadline": "Brand Strategy and Design for Wine Country and Local Business",
            "body": "Walla Walla visitors arrive with expectations. Locals know the difference between a pretty label and a real brand. We design for both audiences: tourism season and the community that stays all year.",
        },
        "whatWeDo": {
            "heading": "Winery and Local Business Branding in Wine Country",
            "intro": "Labels, tasting rooms, restaurants, and trades companies all compete in a small market with high taste levels. We build cohesive identities that work on shelf, on site, and online.",
            "localParagraph": "Winery work is a specialty: story, naming, label architecture, tasting room graphics, and web design that matches. For non-wine businesses, we apply the same rigor so you look like you belong in a town where design already matters.",
        },
        "whyYb": {
            "heading": "Design That Meets Walla Walla's Bar",
            "body": "Wine country trained local customers to notice details. We deliver brand systems that hold up in that environment and still feel like your business, not a trend from last harvest.",
        },
    },
]

HUBS = [
    {
        "slug": "yakima-wa",
        "city": "Yakima",
        "state": "WA",
        "localSignals": ["Yakima, WA", "Selah, WA", "Union Gap, WA", "Yakima Valley", "Central Washington"],
        "schema_locality": "Yakima",
        "metaDescription": "YB Marketing is a full-service digital marketing agency for Yakima Valley businesses. SEO, Google Ads, web design, social media, and branding from a team based in Yakima.",
        "hero": {
            "eyebrow": "YB MARKETING · YAKIMA, WA",
            "headline": "Digital Marketing for the Yakima Valley",
            "accentHeadline": "From a Team That Lives Here",
            "body": "We are based in Yakima and work with Valley businesses every day. Search, ads, websites, social, and branding with local context baked in, not bolted on.",
        },
        "servicesSection": {
            "eyebrow": "SERVICES IN YAKIMA",
            "heading": "Marketing Help for Yakima Valley Businesses",
            "subheading": "One team for SEO, paid search, websites, social, and brand design so your message stays consistent.",
            "cards": [
                {"title": "SEO & AI Optimization", "body": "Show up when Yakima customers search on Google and in AI tools. Local keywords, technical fixes, and content that matches how people in the Valley actually look for services."},
                {"title": "Google Ads Management", "body": "Paid search with tight geographic targeting and budgets that respect seasonal swings in agriculture, tourism, and retail."},
                {"title": "Web Design & Development", "body": "Fast, mobile-friendly sites for Yakima businesses. Built to rank, easy to update, and designed to turn visits into calls and form fills."},
                {"title": "Social Media Management", "body": "Content that fits Yakima: community events, harvest season, local partnerships, and the mix of English and Spanish audiences many Valley businesses serve."},
                {"title": "Branding & Design", "body": "Logos, brand standards, signage, and packaging for businesses that need to look credible from downtown to the warehouse district."},
            ],
        },
        "credibility": {
            "heading": "A Yakima Team, Not a Distant Account",
            "paragraphs": [
                "YB Marketing started in the Yakima Valley. We know the industries here: wine, ag, healthcare, trades, retail, and the small businesses that keep Main Street moving.",
                "When you call, you talk to people who understand your market. We have helped hundreds of local companies sharpen their brand and fix the digital basics that drive leads.",
            ],
        },
        "whyYb": {
            "heading": "Marketing Plans Built Around Your Yakima Business",
            "body": "No cookie-cutter packages. We look at your competitors, your margins, and where your best customers come from, then build a plan you can measure.",
            "steps": [
                {"label": "FREE AUDIT", "body": "We review your site, listings, and current marketing to find quick wins and bigger gaps."},
                {"label": "CLEAR STRATEGY", "body": "You get priorities, timelines, and realistic expectations for Yakima search and ad performance."},
                {"label": "MONTHLY EXECUTION", "body": "We implement, report in plain language, and adjust based on what the data shows."},
            ],
        },
    },
    {
        "slug": "ellensburg-wa",
        "city": "Ellensburg",
        "state": "WA",
        "localSignals": ["Ellensburg, WA", "Kittitas County", "Cle Elum, WA", "Kittitas, WA", "Central Washington"],
        "schema_locality": "Ellensburg",
        "metaDescription": "Digital marketing for Ellensburg and Kittitas County. SEO, Google Ads, web design, social media, and branding for Central Washington businesses.",
        "hero": {
            "eyebrow": "YB MARKETING · ELLENSBURG & KITTITAS COUNTY",
            "headline": "Marketing for Ellensburg",
            "accentHeadline": "Locals, Students, and I-90 Traffic",
            "body": "Ellensburg is small enough that word of mouth still wins, but big enough that you need a real web presence. We help Kittitas County businesses get found and look trustworthy online.",
        },
        "servicesSection": {
            "eyebrow": "ELLENSBURG SERVICES",
            "heading": "Digital Marketing for Kittitas County",
            "subheading": "Practical marketing for businesses that serve downtown Ellensburg, CWU, and drivers along I-90.",
            "cards": [
                {"title": "SEO & AI Optimization", "body": "Rank for Ellensburg and county searches. Map visibility, local pages, and content tuned to how Kittitas customers search."},
                {"title": "Google Ads Management", "body": "Geo-targeted campaigns for seasonal peaks, university move-in, and highway travelers who need services now."},
                {"title": "Web Design & Development", "body": "Clean websites that load fast on mobile and make it obvious what you do and where you serve."},
                {"title": "Social Media Management", "body": "Posts that connect with ranch families, students, and longtime residents without sounding like a corporate template."},
                {"title": "Branding & Design", "body": "Logos and identity systems that look professional on Main Street and credible to customers from outside the county."},
            ],
        },
        "credibility": {
            "heading": "We Know Ellensburg's Two Audiences",
            "paragraphs": [
                "Ellensburg blends university life with agricultural roots. Marketing here has to speak to both without alienating either.",
                "We have worked with retailers, contractors, and service businesses across Central Washington. Our approach is simple: learn your market, then build campaigns that fit it.",
            ],
        },
        "whyYb": {
            "heading": "Marketing That Fits Kittitas County",
            "body": "You do not need a Seattle agency playbook. You need someone who understands I-90 corridor traffic, CWU cycles, and how referrals work in a tight community.",
            "steps": [
                {"label": "FREE AUDIT", "body": "We check your site, Google presence, and competitors in Ellensburg and nearby towns."},
                {"label": "CLEAR STRATEGY", "body": "A plan tied to your real customers: locals, students, or regional traffic."},
                {"label": "MONTHLY EXECUTION", "body": "Steady work on SEO, ads, and content so leads keep coming between rodeo season and graduation."},
            ],
        },
    },
    {
        "slug": "tri-cities-wa",
        "city": "Tri-Cities",
        "state": "WA",
        "localSignals": ["Kennewick, WA", "Pasco, WA", "Richland, WA", "West Richland, WA", "Columbia Basin"],
        "schema_locality": "Kennewick",
        "metaDescription": "Digital marketing for Kennewick, Pasco, and Richland. SEO, Google Ads, web design, social, and branding for Tri-Cities businesses.",
        "hero": {
            "eyebrow": "YB MARKETING · TRI-CITIES, WA",
            "headline": "Tri-Cities Digital Marketing",
            "accentHeadline": "All Three Cities, One Strategy",
            "body": "Kennewick, Pasco, and Richland attract different customers. We build campaigns that respect those differences instead of blasting one generic message across the Basin.",
        },
        "servicesSection": {
            "eyebrow": "TRI-CITIES SERVICES",
            "heading": "Marketing for Kennewick, Pasco, and Richland",
            "subheading": "City-level targeting, bilingual options where they matter, and reporting you can actually read.",
            "cards": [
                {"title": "SEO & AI Optimization", "body": "Local SEO across the metro: separate landing pages, map rankings, and content for each city's search habits."},
                {"title": "Google Ads Management", "body": "Budget split by city and service line so Pasco, Richland, and Kennewick each get appropriate coverage."},
                {"title": "Web Design & Development", "body": "Sites that state your service area clearly and convert visitors whether they land from a phone search or a referral."},
                {"title": "Social Media Management", "body": "Content options for Pasco's bilingual audience, Richland's professional base, and Kennewick's hospitality sector."},
                {"title": "Branding & Design", "body": "Brand systems rooted in Columbia Basin identity: wine, river culture, energy, and fast residential growth."},
            ],
        },
        "credibility": {
            "heading": "We Treat the Tri-Cities as Three Markets",
            "paragraphs": [
                "Hanford, wine, agriculture, and housing growth all shape how people buy here. We account for that instead of copying a one-city playbook.",
                "Our team has supported Tri-Cities businesses in trades, healthcare, hospitality, and professional services. We know the seasonality and the competition.",
            ],
        },
        "whyYb": {
            "heading": "Columbia Basin Marketing Without the Guesswork",
            "body": "Most agencies flatten the Tri-Cities into one blob. We target the cities and demographics that actually drive your revenue.",
            "steps": [
                {"label": "FREE AUDIT", "body": "Review of your visibility in Kennewick, Pasco, Richland, and Maps."},
                {"label": "CLEAR STRATEGY", "body": "City-by-city priorities based on where your best jobs come from."},
                {"label": "MONTHLY EXECUTION", "body": "Ongoing SEO, ads, and content with reporting tied to leads, not vanity metrics."},
            ],
        },
    },
    {
        "slug": "spokane-wa",
        "city": "Spokane",
        "state": "WA",
        "localSignals": ["Spokane, WA", "Spokane Valley, WA", "Liberty Lake, WA", "Cheney, WA", "Inland Northwest"],
        "schema_locality": "Spokane",
        "metaDescription": "Digital marketing for Spokane and the Inland Northwest. SEO, Google Ads, web design, social media, and branding for Eastern Washington businesses.",
        "hero": {
            "eyebrow": "YB MARKETING · SPOKANE, WA",
            "headline": "Spokane Digital Marketing",
            "accentHeadline": "Built for a Competitive Market",
            "body": "Spokane is Eastern Washington's business capital. Your site and ads need to keep pace with national brands and sharp local competitors. We build strategies that earn attention and convert it.",
        },
        "servicesSection": {
            "eyebrow": "SPOKANE SERVICES",
            "heading": "Full-Service Marketing for Spokane Businesses",
            "subheading": "Healthcare, home services, legal, retail, and more. Campaigns sized for the Inland Northwest.",
            "cards": [
                {"title": "SEO & AI Optimization", "body": "Competitive local SEO from South Hill to Spokane Valley. Technical health, content, and map rankings that compound over time."},
                {"title": "Google Ads Management", "body": "PPC with conversion tracking and negative keywords that protect spend in a crowded auction."},
                {"title": "Web Design & Development", "body": "Sites that look credible next to larger competitors and load fast on mobile."},
                {"title": "Social Media Management", "body": "Community-focused content: neighborhoods, events, and the local tone Spokane customers respond to."},
                {"title": "Branding & Design", "body": "Professional identity systems for businesses that need to look established in a sophisticated market."},
            ],
        },
        "credibility": {
            "heading": "Inland Northwest Experience",
            "paragraphs": [
                "Spokane buyers compare options. We help you show up in search, look credible on your site, and follow up fast enough to win the job.",
                "We work with providers, contractors, firms, and retailers across Eastern Washington. Strategy comes first; tactics follow what your data shows.",
            ],
        },
        "whyYb": {
            "heading": "Spokane Marketing With Accountability",
            "body": "You get clear goals, regular reporting, and adjustments when something is not working. No black-box agency nonsense.",
            "steps": [
                {"label": "FREE AUDIT", "body": "SEO, ads, and site review with specific Spokane competitor context."},
                {"label": "CLEAR STRATEGY", "body": "Channel mix and budget guidance based on your industry and margins."},
                {"label": "MONTHLY EXECUTION", "body": "Optimization loops that improve cost per lead over time."},
            ],
        },
    },
    {
        "slug": "boise-id",
        "city": "Boise",
        "state": "ID",
        "localSignals": ["Boise, ID", "Meridian, ID", "Nampa, ID", "Treasure Valley"],
        "schema_locality": "Boise",
        "metaDescription": "Digital marketing for Boise and the Treasure Valley. SEO, Google Ads, web design, social media, and branding for Idaho's fastest-growing market.",
        "hero": {
            "eyebrow": "YB MARKETING · BOISE & TREASURE VALLEY",
            "headline": "Boise Digital Marketing",
            "accentHeadline": "For a Crowded, Growing Market",
            "body": "Boise adds competitors every quarter. Strong SEO, sharp ads, and a website that converts are table stakes. We help Treasure Valley businesses stand out without overspending.",
        },
        "servicesSection": {
            "eyebrow": "BOISE SERVICES",
            "heading": "Marketing for Treasure Valley Growth",
            "subheading": "From startups to established operators in Boise, Meridian, and Nampa.",
            "cards": [
                {"title": "SEO & AI Optimization", "body": "Local rankings in a noisy market. Content and technical work aimed at customers ready to buy, not just browse."},
                {"title": "Google Ads Management", "body": "Campaign structure that scales with growth and protects budget as CPCs rise."},
                {"title": "Web Design & Development", "body": "Modern sites for Boise businesses that need to look credible to transplants and longtime residents alike."},
                {"title": "Social Media Management", "body": "Brand voice that fits Boise: outdoor culture, neighborhood pride, and direct communication."},
                {"title": "Branding & Design", "body": "Identity design that avoids generic mountain-badge clichés and actually fits your company."},
            ],
        },
        "credibility": {
            "heading": "Treasure Valley Marketing That Keeps Up",
            "paragraphs": [
                "Boise's growth brought more national brands and higher customer expectations. Local businesses need marketing that looks current and performs.",
                "We partner with Boise-area companies in home services, health, food and beverage, and professional services. Plans flex as you add locations or lines of business.",
            ],
        },
        "whyYb": {
            "heading": "Boise Plans You Can Scale",
            "body": "Start focused, expand what works. We align SEO, ads, and creative with your growth stage instead of selling everything at once.",
            "steps": [
                {"label": "FREE AUDIT", "body": "Where you rank today, what ads cost, and what your site loses on mobile."},
                {"label": "CLEAR STRATEGY", "body": "Prioritized roadmap for the next 90 days and beyond."},
                {"label": "MONTHLY EXECUTION", "body": "Testing, reporting, and budget shifts based on lead quality."},
            ],
        },
    },
    {
        "slug": "coeur-dalene-id",
        "city": "Coeur d'Alene",
        "state": "ID",
        "localSignals": ["Coeur d'Alene, ID", "Post Falls, ID", "Hayden, ID", "North Idaho"],
        "schema_locality": "Coeur d'Alene",
        "metaDescription": "Digital marketing for Coeur d'Alene and North Idaho. SEO, Google Ads, web design, social, and branding for lake country businesses.",
        "hero": {
            "eyebrow": "YB MARKETING · COEUR D'ALENE, ID",
            "headline": "Coeur d'Alene Digital Marketing",
            "accentHeadline": "Tourism Season and Year-Round Locals",
            "body": "CDA businesses juggle summer visitors and loyal Kootenai County customers. We build marketing that performs in peak season and keeps leads flowing in winter.",
        },
        "servicesSection": {
            "eyebrow": "CDA SERVICES",
            "heading": "Marketing for North Idaho Businesses",
            "subheading": "Hospitality, recreation, home services, and retail with lake-country context.",
            "cards": [
                {"title": "SEO & AI Optimization", "body": "Rank for Coeur d'Alene, Post Falls, and Hayden searches. Seasonal content when tourism spikes."},
                {"title": "Google Ads Management", "body": "Campaigns timed to summer demand and local service needs in the off-season."},
                {"title": "Web Design & Development", "body": "Sites that look great on phones, load fast, and make booking or calling obvious."},
                {"title": "Social Media Management", "body": "Visual content that fits CDA without looking like a stock photo resort feed."},
                {"title": "Branding & Design", "body": "Logos and environments that feel North Idaho, not theme-park rustic."},
            ],
        },
        "credibility": {
            "heading": "Lake Country Is a Different Rhythm",
            "paragraphs": [
                "CDA marketing has to plan for swings in traffic and a local base that values trust over hype.",
                "We support marinas, restaurants, lodging, and trades across Kootenai County with campaigns tied to real booking and call data.",
            ],
        },
        "whyYb": {
            "heading": "Marketing That Respects CDA Seasonality",
            "body": "We ramp spend when demand is there and focus on retention and local SEO when it is not.",
            "steps": [
                {"label": "FREE AUDIT", "body": "Search visibility, ad history, and site conversion review."},
                {"label": "CLEAR STRATEGY", "body": "Seasonal calendar aligned to your revenue pattern."},
                {"label": "MONTHLY EXECUTION", "body": "Adjustments as tourism and local demand shift."},
            ],
        },
    },
    {
        "slug": "tacoma-wa",
        "city": "Tacoma",
        "state": "WA",
        "localSignals": ["Tacoma, WA", "Lakewood, WA", "Pierce County", "South Sound"],
        "schema_locality": "Tacoma",
        "metaDescription": "Digital marketing for Tacoma and Pierce County. SEO, Google Ads, web design, social media, and branding for South Sound businesses.",
        "hero": {
            "eyebrow": "YB MARKETING · TACOMA & PIERCE COUNTY",
            "headline": "Tacoma Digital Marketing",
            "accentHeadline": "Local Loyalty Meets Real Competition",
            "body": "Tacoma customers support businesses that show up in the community. They also compare you to Seattle options online. We help South Sound companies win both battles.",
        },
        "servicesSection": {
            "eyebrow": "TACOMA SERVICES",
            "heading": "Marketing for Pierce County Businesses",
            "subheading": "Neighborhood-aware campaigns with the polish to compete regionally.",
            "cards": [
                {"title": "SEO & AI Optimization", "body": "Local search across Tacoma, Lakewood, and Pierce County with content that reflects how people here actually search."},
                {"title": "Google Ads Management", "body": "Geo-fenced campaigns that prioritize South Sound leads over wasted Seattle clicks."},
                {"title": "Web Design & Development", "body": "Sites that tell a Tacoma story and convert visitors who found you from a referral or a search."},
                {"title": "Social Media Management", "body": "Community partnerships, local events, and creative that feels like Tacoma, not a national template."},
                {"title": "Branding & Design", "body": "Identity work for businesses tying their growth to the city's momentum."},
            ],
        },
        "credibility": {
            "heading": "South Sound Roots, Regional Standards",
            "paragraphs": [
                "Tacoma's reputation changed because local businesses invested in the city. Marketing should reflect that same pride and professionalism.",
                "We work with contractors, clinics, restaurants, and professional firms across Pierce County. Every plan starts with where your leads really come from.",
            ],
        },
        "whyYb": {
            "heading": "Tacoma Marketing Without Seattle Pretense",
            "body": "You get direct communication, realistic timelines, and work tied to leads and revenue.",
            "steps": [
                {"label": "FREE AUDIT", "body": "Site, SEO, and ad review with Tacoma competitor notes."},
                {"label": "CLEAR STRATEGY", "body": "Channel mix for your neighborhood and service area."},
                {"label": "MONTHLY EXECUTION", "body": "Reporting and optimization focused on calls and form fills."},
            ],
        },
    },
    {
        "slug": "vancouver-wa",
        "city": "Vancouver",
        "state": "WA",
        "localSignals": ["Vancouver, WA", "Clark County", "Camas, WA", "Ridgefield, WA"],
        "schema_locality": "Vancouver",
        "metaDescription": "Digital marketing for Vancouver, WA and Clark County. SEO, Google Ads, web design, social, and branding on the Washington side of the river.",
        "hero": {
            "eyebrow": "YB MARKETING · VANCOUVER, WA",
            "headline": "Vancouver Digital Marketing",
            "accentHeadline": "Clark County First",
            "body": "Many Clark County customers actively choose Washington businesses. We make sure they find you, understand why you are local, and trust what they see online.",
        },
        "servicesSection": {
            "eyebrow": "VANCOUVER SERVICES",
            "heading": "Marketing for Clark County",
            "subheading": "Washington-side SEO and ads that do not get lost in Portland noise.",
            "cards": [
                {"title": "SEO & AI Optimization", "body": "Rank for Vancouver, Camas, and Ridgefield queries with location pages and map optimization."},
                {"title": "Google Ads Management", "body": "Targeting that favors Clark County zip codes and filters out irrelevant Oregon traffic when needed."},
                {"title": "Web Design & Development", "body": "Websites that highlight your Washington presence and make contact frictionless."},
                {"title": "Social Media Management", "body": "Local proof: projects, reviews, and community involvement on the Washington side."},
                {"title": "Branding & Design", "body": "Visual identity that establishes Clark County roots distinct from Portland competitors."},
            ],
        },
        "credibility": {
            "heading": "We Know the Portland Shadow Problem",
            "paragraphs": [
                "Vancouver businesses often compete with Oregon brands that dominate search results. We fix that with local SEO, clear service-area messaging, and ads geo-locked to Clark County.",
                "Contractors, healthcare, legal, and retail across Vancouver and Camas use us to grow Washington-side leads without pretending to be a Portland agency.",
            ],
        },
        "whyYb": {
            "heading": "Washington-Side Growth, Measured",
            "body": "Track leads by city and campaign so you know what is working in Vancouver versus Camas or Ridgefield.",
            "steps": [
                {"label": "FREE AUDIT", "body": "How you appear for 'Vancouver WA' searches versus Portland competitors."},
                {"label": "CLEAR STRATEGY", "body": "Messaging that reinforces Clark County identity."},
                {"label": "MONTHLY EXECUTION", "body": "SEO and ads tuned to Washington customers who want a local provider."},
            ],
        },
    },
    {
        "slug": "wenatchee-wa",
        "city": "Wenatchee",
        "state": "WA",
        "localSignals": ["Wenatchee, WA", "East Wenatchee, WA", "Leavenworth, WA", "North Central Washington"],
        "schema_locality": "Wenatchee",
        "metaDescription": "Digital marketing for Wenatchee and North Central Washington. SEO, Google Ads, web design, social, and branding for the Apple Capital region.",
        "hero": {
            "eyebrow": "YB MARKETING · WENATCHEE & NCW",
            "headline": "Wenatchee Digital Marketing",
            "accentHeadline": "Regional Hub, Local Detail",
            "body": "Wenatchee serves the whole valley. Your marketing should too. We help NCW businesses rank regionally and convert customers who drive in from nearby towns.",
        },
        "servicesSection": {
            "eyebrow": "WENATCHEE SERVICES",
            "heading": "Marketing for North Central Washington",
            "subheading": "Ag, food, healthcare, trades, and tourism with NCW-specific messaging.",
            "cards": [
                {"title": "SEO & AI Optimization", "body": "Visibility in Wenatchee, East Wenatchee, Leavenworth, and Chelan searches."},
                {"title": "Google Ads Management", "body": "Seasonal campaigns for tourism peaks and steady local service demand."},
                {"title": "Web Design & Development", "body": "Sites that signal regional authority and make phone calls easy on mobile."},
                {"title": "Social Media Management", "body": "Content rooted in orchard country, outdoor recreation, and community events."},
                {"title": "Branding & Design", "body": "Packaging, signage, and identity for agricultural and consumer brands alike."},
            ],
        },
        "credibility": {
            "heading": "Built for a Regional Commercial Center",
            "paragraphs": [
                "Customers travel to Wenatchee for services they cannot get at home. Your online presence should convince them the trip is worth it.",
                "We work with food producers, medical offices, contractors, and hospitality businesses across NCW. Messaging always includes the towns you actually serve.",
            ],
        },
        "whyYb": {
            "heading": "NCW Marketing With Geographic Precision",
            "body": "We target the towns that send you revenue, not just the city limits on a map.",
            "steps": [
                {"label": "FREE AUDIT", "body": "Regional search review across Wenatchee and surrounding communities."},
                {"label": "CLEAR STRATEGY", "body": "Service-area SEO and ad targeting aligned to your draw radius."},
                {"label": "MONTHLY EXECUTION", "body": "Ongoing content and optimization for seasonal NCW traffic."},
            ],
        },
    },
    {
        "slug": "walla-walla-wa",
        "city": "Walla Walla",
        "state": "WA",
        "localSignals": ["Walla Walla, WA", "Wine Country", "Walla Walla County", "Whitman College"],
        "schema_locality": "Walla Walla",
        "metaDescription": "Digital marketing for Walla Walla wine country and local businesses. SEO, Google Ads, web design, social, and branding for a high-expectation market.",
        "hero": {
            "eyebrow": "YB MARKETING · WALLA WALLA, WA",
            "headline": "Walla Walla Digital Marketing",
            "accentHeadline": "Wine Country and Year-Round Community",
            "body": "Walla Walla runs on tourism and loyal locals. We build marketing that fills tasting rooms in peak season and keeps your phone ringing when visitors go home.",
        },
        "servicesSection": {
            "eyebrow": "WALLA WALLA SERVICES",
            "heading": "Marketing for Wine Country Businesses",
            "subheading": "Wineries, hospitality, retail, and trades with taste-level creative.",
            "cards": [
                {"title": "SEO & AI Optimization", "body": "Rank for wine tourism and local service searches with content that matches how visitors plan trips."},
                {"title": "Google Ads Management", "body": "Campaigns for events, weekends, and high-intent local keywords."},
                {"title": "Web Design & Development", "body": "Beautiful, fast sites for wineries and service businesses that need to impress on first click."},
                {"title": "Social Media Management", "body": "Visual storytelling for releases, events, and behind-the-scenes content locals share."},
                {"title": "Branding & Design", "body": "Label, tasting room, and identity work that meets Walla Walla's design bar."},
            ],
        },
        "credibility": {
            "heading": "Wine Country Expectations Are High",
            "paragraphs": [
                "Visitors compare you to the best labels and tasting rooms in town. Locals notice when marketing feels generic.",
                "We support wineries, restaurants, hotels, and non-wine businesses across Walla Walla County with integrated brand and performance marketing.",
            ],
        },
        "whyYb": {
            "heading": "Marketing That Matches the Market",
            "body": "Creative quality and measurable leads. You should not have to pick one.",
            "steps": [
                {"label": "FREE AUDIT", "body": "Site, SEO, and ad review with wine-country competitive context."},
                {"label": "CLEAR STRATEGY", "body": "Seasonal plan for DTC, bookings, and local leads."},
                {"label": "MONTHLY EXECUTION", "body": "Creative and performance work that adapts through harvest and event seasons."},
            ],
        },
    },
]

FAQ_ANSWERS = {
    "seo": "Yes. We handle local SEO for {place} businesses: Google Business Profile, on-page work, technical fixes, and content aimed at how people search in your market.",
    "google-ads": "Yes. We run Google Ads for {place} companies with conversion tracking, geographic targeting, and monthly optimization so spend goes toward real leads.",
    "web-design": "Yes. We build fast, mobile-ready websites for {place} businesses that are easy to update and structured for search.",
    "social-media": "Yes. We plan and publish social content for {place} brands, aligned with your voice and the seasons that matter in your market.",
    "branding": "Yes. We offer brand strategy, logo design, and identity systems for {place} businesses, from signage to digital applications.",
    "content-marketing": "Yes. We create blog posts, landing pages, and other content for {place} businesses that supports SEO and gives sales teams something useful to share.",
    "press-releases": "Yes. We write and distribute press releases for {place} companies when you have news worth covering locally or regionally.",
}


def js_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def render_branding_faqs(city: str) -> str:
  # Keep FAQs shorter; reuse structure but trim em dashes in answers via simple templates
    items = [
        (f"What branding services do you offer in {city}?",
         f"Brand strategy, logo design, color and type systems, brand guides, print, signage, packaging, and web design. Scope depends on what your {city} business needs right now."),
        (f"Do I need a full rebrand or just a new logo?",
         "We start with an honest assessment. Sometimes a logo refresh is enough. If your messaging, signage, and website all feel mismatched, a fuller identity project usually pays off."),
        (f"How long does a branding project take?",
         "Most projects run 6–12 weeks from kickoff to final files, depending on deliverables and revision rounds. You get a timeline up front."),
        (f"Can you design signage and print for my business?",
         "Yes. We design business cards, vehicle graphics, storefront signage, uniforms, and trade show materials so everything matches."),
        (f"Do you work with wineries and food brands?",
         "Yes, especially in wine and agricultural markets. We handle labels, packaging, tasting room graphics, and the digital side."),
        (f"How does branding help my marketing?",
         "A clear brand makes ads, SEO landing pages, and social posts more recognizable. People trust what they have seen before."),
    ]
    lines = ["    faqs: ["]
    for q, a in items:
        lines.append("      {")
        lines.append(f"        q: {js_str(q)},")
        lines.append(f"        a: {js_str(a)},")
        lines.append("      },")
    lines.append("    ],")
    return "\n".join(lines)


def write_branding():
    parts = ["export const brandingLocations = ["]
    for loc in BRANDING:
        city = loc["city"]
        state = loc["state"]
        slug = loc["slug"]
        tri = slug == "tri-cities-wa"
        title = (
            f"Branding & Design Tri-Cities WA | Kennewick, Pasco & Richland | YB Marketing"
            if tri
            else f"Branding & Design {city} {state} | YB Marketing"
        )
        parts.append("  {")
        parts.append(f"    slug: {js_str(slug)},")
        parts.append("    service: 'branding',")
        parts.append(f"    city: {js_str(city)},")
        parts.append(f"    state: {js_str(state)},")
        parts.append(f"    region: {js_str(loc['region'])},")
        parts.append(f"    titleTag: {js_str(title)},")
        parts.append(f"    metaDescription: {js_str(loc['metaDescription'])},")
        parts.append(f"    canonicalUrl: 'https://yakimabranding.com/branding/{slug}',")
        parts.append("    hero: {")
        parts.append("      eyebrow: 'BRANDING & DESIGN',")
        parts.append(f"      headline: {js_str(loc['hero']['headline'])},")
        parts.append(f"      subheadline: {js_str(loc['hero']['subheadline'])},")
        parts.append(f"      body: {js_str(loc['hero']['body'])},")
        parts.append("    },")
        parts.append("    whatWeDo: {")
        parts.append(f"      heading: {js_str(loc['whatWeDo']['heading'])},")
        parts.append(f"      intro: {js_str(loc['whatWeDo']['intro'])},")
        parts.append(f"      localParagraph: {js_str(loc['whatWeDo']['localParagraph'])},")
        parts.append("    },")
        parts.append("    whyYb: {")
        parts.append(f"      heading: {js_str(loc['whyYb']['heading'])},")
        parts.append(f"      body: {js_str(loc['whyYb']['body'])},")
        parts.append("    },")
        signals = ", ".join(js_str(s) for s in loc["localSignals"])
        parts.append(f"    localSignals: [{signals}],")
        parts.append(render_branding_faqs(city))
        parts.append("    schema: {")
        parts.append("      service: 'Branding',")
        parts.append(f"      addressLocality: {js_str(loc['schema_locality'])},")
        parts.append(f"      addressRegion: {js_str(state)},")
        parts.append("      addressCountry: 'US',")
        parts.append("    },")
        parts.append("  },")
    parts.append("];")
    parts.append("")
    (ROOT / "data" / "brandingLocations.js").write_text("\n".join(parts), encoding="utf-8")


def write_hubs():
    master_path = ROOT / "data" / "locationHubs.js"
    existing = master_path.read_text(encoding="utf-8")
    master_start = existing.find("export const locationHubsMaster")
    master_block = existing[master_start:] if master_start != -1 else ""

    parts = ["export const locationHubs = ["]
    for hub in HUBS:
        city = hub["city"]
        state = hub["state"]
        slug = hub["slug"]
        tri = slug == "tri-cities-wa"
        title = (
            "Digital Marketing Agency Tri-Cities WA | Kennewick, Pasco & Richland | YB Marketing"
            if tri
            else f"Digital Marketing Agency {city} {state} | YB Marketing"
        )
        parts.append("  {")
        parts.append(f'    "slug": {js_str(slug)},')
        parts.append(f'    "city": {js_str(city)},')
        parts.append(f'    "state": {js_str(state)},')
        parts.append(f'    "titleTag": {js_str(title)},')
        parts.append(f'    "metaDescription": {js_str(hub["metaDescription"])},')
        parts.append(f'    "canonicalUrl": "https://yakimabranding.com/locations/{slug}",')
        parts.append('    "hero": {')
        parts.append(f'      "eyebrow": {js_str(hub["hero"]["eyebrow"])},')
        parts.append(f'      "headline": {js_str(hub["hero"]["headline"])},')
        parts.append(f'      "accentHeadline": {js_str(hub["hero"]["accentHeadline"])},')
        parts.append(f'      "body": {js_str(hub["hero"]["body"])}')
        parts.append('    },')
        parts.append('    "servicesSection": {')
        parts.append(f'      "eyebrow": {js_str(hub["servicesSection"]["eyebrow"])},')
        parts.append(f'      "heading": {js_str(hub["servicesSection"]["heading"])},')
        parts.append(f'      "subheading": {js_str(hub["servicesSection"]["subheading"])},')
        parts.append('      "cards": [')
        for card in hub["servicesSection"]["cards"]:
            parts.append("        {")
            parts.append(f'          "title": {js_str(card["title"])},')
            parts.append(f'          "body": {js_str(card["body"])}')
            parts.append("        },")
        parts.append("      ]")
        parts.append("    },")
        parts.append('    "credibility": {')
        parts.append('      "eyebrow": "ABOUT US",')
        parts.append(f'      "heading": {js_str(hub["credibility"]["heading"])},')
        parts.append('      "paragraphs": [')
        for p in hub["credibility"]["paragraphs"]:
            parts.append(f"        {js_str(p)},")
        parts.append("      ]")
        parts.append("    },")
        parts.append('    "whyYb": {')
        parts.append('      "eyebrow": "WHY CHOOSE US",')
        parts.append(f'      "heading": {js_str(hub["whyYb"]["heading"])},')
        parts.append(f'      "body": {js_str(hub["whyYb"]["body"])},')
        parts.append('      "steps": [')
        for step in hub["whyYb"]["steps"]:
            parts.append("        {")
            parts.append(f'          "label": {js_str(step["label"])},')
            parts.append(f'          "body": {js_str(step["body"])}')
            parts.append("        },")
        parts.append("      ]")
        parts.append("    },")
        signals = ",\n      ".join(js_str(s) for s in hub["localSignals"])
        parts.append(f'    "localSignals": [\n      {signals}\n    ],')
        parts.append('    "schema": {')
        parts.append(f'      "addressLocality": {js_str(hub["schema_locality"])},')
        parts.append(f'      "addressRegion": {js_str(state)},')
        parts.append('      "addressCountry": "US"')
        parts.append("    }")
        parts.append("  },")
    parts.append("];")
    parts.append("")
    if master_block:
        parts.append(master_block.rstrip())
        parts.append("")
    (ROOT / "data" / "locationHubs.js").write_text("\n".join(parts), encoding="utf-8")


def patch_faq_py():
    path = ROOT / "scripts" / "location_hub_faqs.py"
    text = path.read_text(encoding="utf-8")
    replacements = [
        (
            '"Yes. YB Marketing provides local SEO for {place} businesses — including Google Business "\n'
            '            "Profile optimization, local keyword targeting, technical SEO, and content that helps you "\n'
            '            "rank in search and Maps."',
            '"Yes. We handle local SEO for {place} businesses: Google Business Profile, on-page work, "\n'
            '            "technical fixes, and content aimed at how people search in your market."',
        ),
        (
            '"Yes. We manage Google Ads campaigns for {place} businesses with keyword strategy, "\n'
            '            "conversion tracking, and ongoing optimization so your ad spend reaches the right local customers."',
            '"Yes. We run Google Ads for {place} companies with conversion tracking, geographic targeting, "\n'
            '            "and monthly optimization so spend goes toward real leads."',
        ),
        (
            '"Yes. We build custom, mobile-ready websites for {place} businesses that are fast, "\n'
            '            "SEO-friendly, and designed to convert visitors into leads."',
            '"Yes. We build fast, mobile-ready websites for {place} businesses that are easy to update "\n'
            '            "and structured for search."',
        ),
        (
            '"Yes. Our team creates and manages social content that reflects {city}\'s local market "\n'
            '            "and helps {place} businesses build engagement and brand awareness."',
            '"Yes. We plan and publish social content for {place} brands, aligned with your voice "\n'
            '            "and the seasons that matter in your market."',
        ),
        (
            '"Yes. We develop brand identities — logos, visual systems, and messaging — built for "\n'
            '            "{place} businesses that want to stand out in their market."',
            '"Yes. We offer brand strategy, logo design, and identity systems for {place} businesses, "\n'
            '            "from signage to digital applications."',
        ),
    ]
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
    text = text.replace(
        "<h2 style=\"margin:14px 0 14px\">{esc(place)} Digital Marketing — Frequently Asked Questions</h2>",
        "<h2 style=\"margin:14px 0 14px\">{esc(place)} Digital Marketing FAQs</h2>",
    )
    path.write_text(text, encoding="utf-8")


def main():
    write_branding()
    write_hubs()
    patch_faq_py()
    print("Wrote data/brandingLocations.js and data/locationHubs.js")


if __name__ == "__main__":
    main()
