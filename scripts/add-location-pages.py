#!/usr/bin/env python3
"""Build /locations (Locations We Serve hub) and the focus region pages."""

from __future__ import annotations

import importlib.util
import sys
from html import escape
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from schema_markup import SITE, breadcrumb, global_schemas, render_schema_head, webpage_schema
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_footer_snippet import site_footer_html
from site_lead_form_snippet import lead_form_html, lead_form_script_tags
from site_nav_snippet import site_header_html
from site_schedule_grid_snippet import TEAM_SCHEDULE
from site_tracking_snippet import ATTRIBUTER_FOOTER_BLOCK, GTM_BODY_NOSCRIPT_BLOCK, TRACKING_HEAD_BLOCK


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_seo = _load("seo_sub", "add-seo-subpages.py")
_rv = _load("rv_page", "add-reviews-page.py")
BASE_CSS = _seo.BASE_CSS
ARROW = _seo.ARROW
STAR = _rv.STAR
GOOGLE_G = _rv.GOOGLE_G
YELP_STARS = _rv.YELP_STARS
YELP_URL = _rv.YELP_URL
GOOGLE_REVIEWS_URL = _rv.GOOGLE_REVIEWS_URL
REVIEWS = dict(_rv.REVIEWS)
initials = _rv.initials
CL = _load("clutch_reviews", "clutch_reviews.py")

PHONE = "509-901-9735"

PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>'
PLUS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>'

SVC_ICONS = {
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "layout": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/>',
    "spark": '<path d="M12 3l1.9 5.8L20 10l-6.1 1.2L12 17l-1.9-5.8L4 10l6.1-1.2z"/><path d="M19 17l.8 2.2L22 20l-2.2.8L19 23l-.8-2.2L16 20l2.2-.8z"/>',
}


def icon(name: str) -> str:
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{SVC_ICONS[name]}</svg>'


SERVICES = [
    ("SEO", "/seo", "search", "var(--yb-cyan)", "var(--wash-cyan)",
     "Show up in Google Maps, organic results, and AI answers when people search for what you do.",
     [("Local SEO", "/seo/local-seo"), ("AI Search (GEO)", "/seo/ai-search"), ("Technical SEO", "/seo/technical-seo"), ("Website Migrations", "/seo/website-migration")]),
    ("Paid Ads", "/google-ads", "target", "var(--yb-coral)", "var(--wash-coral)",
     "Google, Bing, and Meta ads with call tracking, so you know which clicks turned into customers.",
     [("Google Ads Management", "/google-ads"), ("Social Media Ads", "/social-media"), ("Call Tracking", "/google-ads"), ("Landing Pages", "/web-design")]),
    ("Websites & Branding", "/web-design", "layout", "#159468", "var(--wash-mint)",
     "Websites that load fast, work on a phone, and make it easy for people to call you.",
     [("Web Design", "/web-design"), ("Branding & Logos", "/branding"), ("Content & Blogging", "/content-marketing"), ("Press Releases", "/press-releases")]),
    ("AI & Automation", "/ai-for-business", "spark", "var(--yb-violet)", "var(--wash-violet)",
     "Follow up with every lead automatically and give your team AI tools they'll actually use.",
     [("AI for Business", "/ai-for-business"), ("AI for Small Business", "/ai-for-small-business"), ("Customer Growth & Communication Tool", "/customer-growth"), ("Chat & Voice Agents", "/ai-for-business")]),
]

CASES = {
    "electrical": ("+204%", "page one keywords in two years", "Bay Area Electrical Contractor",
                   "Organic traffic up 112% year over year and search impressions up 366% at peak.",
                   "/about/case-studies/local-electrical-contractor-seo-growth", "#3F6FD6"),
    "refrig": ("+2,900%", "page one keywords", "Central Washington Refrigeration",
               "Organic traffic doubled in seven months and top three rankings grew 57% in a year.",
               "/about/case-studies/local-refrigeration-services-seo-growth", "#12946F"),
    "tire": ("+613%", "page one keywords over three years", "Regional Tire & Auto Shop",
             "Organic traffic up 46% year over year and search impressions up 243% at peak.",
             "/about/case-studies/regional-tire-auto-seo-growth", "#D9532F"),
    "wp": ("130", "websites cleaned in 15 days", "WordPress Portfolio Cleanup",
           "Hidden malware got Google Ads accounts suspended. We found it, removed it, and locked the sites down.",
           "/about/case-studies/wordpress-portfolio-malware-remediation", "#5B45C9"),
}

REMOTE_FAQ = ("Do we need to be local to work with you?",
              "No. We're a fully remote team and work with clients all over the country by phone, Zoom, and email. You'll have a direct line to the people doing the work, and we keep the same hours you do.")

REGIONS = [
    {
        "slug": "san-francisco-bay-area",
        "name": "San Francisco Bay Area",
        "short": "Bay Area",
        "where": "the Bay Area",
        "state": "California",
        "group": "California",
        "accent": "var(--yb-cyan)",
        "h1": "Digital Marketing for <span>Bay Area</span> Businesses",
        "lead": "SEO, Google Ads, and websites for companies from San Francisco to San Jose. Planned around leads and revenue, with reporting you can actually read.",
        "intro": [
            "Bay Area businesses pay some of the highest click prices in the country, and you're competing with national brands for the same searches. Mistakes get expensive quickly.",
            "We plan SEO, ads, and your website together, and we tell you plainly what is working and what isn't. When you call, you talk to the people doing the work.",
        ],
        "industries": ["Contractors & trades", "Professional services", "Healthcare & dental", "Tech & SaaS", "Restaurants & hospitality"],
        "cities": ["San Francisco", "Oakland", "San Jose", "Berkeley", "San Mateo", "Palo Alto", "Fremont", "Walnut Creek"],
        "cases": ["electrical", "refrig", "tire"],
        "channels": "For most Bay Area service businesses we start with Google Business Profile, local SEO, and tightly targeted Google Ads. Click prices are high here, so we spend time on negative keywords, call tracking, and landing pages before we scale spend.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "denver-co",
        "name": "Denver",
        "short": "Denver",
        "state": "Colorado",
        "group": "Colorado",
        "accent": "var(--yb-violet)",
        "h1": "Digital Marketing for <span>Denver</span> Businesses",
        "lead": "SEO, Google Ads, and websites for companies in Denver, Boulder, Aurora, and the surrounding cities.",
        "intro": [
            "Searches like \"roofer near me\" or \"Denver dentist\" show ads, map listings, and directory sites before the regular results. Each one is a place a competitor can take the call.",
            "We help Denver businesses show up in all three, then make sure your website turns those visits into phone calls and booked jobs.",
        ],
        "industries": ["Home services", "Construction", "Healthcare", "Outdoor & recreation", "Professional services"],
        "cities": ["Denver", "Aurora", "Lakewood", "Boulder", "Littleton", "Arvada", "Centennial", "Englewood"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Denver service businesses get the fastest return from Google Business Profile and local SEO, with Google Ads covering the gaps while rankings build. For seasonal work like roofing and landscaping, we adjust ad budgets around the busy months.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "central-washington",
        "name": "Central Washington",
        "short": "Central Washington",
        "state": "Washington",
        "group": "Washington",
        "accent": "#159468",
        "h1": "Digital Marketing for <span>Central Washington</span>",
        "lead": "We work with businesses in Yakima, Ellensburg, Wenatchee, and nearby towns.",
        "intro": [
            "In Central Washington, word of mouth still matters, and most people look you up on their phone before they call. We focus on what brings in calls here: showing up in Google Maps, a website that works well on a phone, and ads aimed only at the towns you serve.",
            "We work with everyone from family run shops to industrial companies that sell across the whole state. Many of our clients have been with us for years, and a lot of new ones come from their referrals.",
        ],
        "industries": ["Agriculture & food processing", "Industrial services", "Auto & tire", "Healthcare", "Wineries & tourism"],
        "cities": ["Yakima", "Ellensburg", "Wenatchee", "Selah", "Sunnyside", "Union Gap", "Moses Lake", "Toppenish"],
        "city_links": {"Yakima": "/locations/yakima-wa", "Ellensburg": "/locations/ellensburg-wa", "Wenatchee": "/locations/wenatchee-wa"},
        "cases": ["refrig", "tire", "electrical"],
        "channels": "For most Central Washington businesses we start with Google Business Profile and local SEO, because that's where people look first. Google Ads work well here too, and clicks cost far less than in Seattle, so a modest budget goes a long way.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "eastern-washington",
        "name": "Eastern Washington",
        "short": "Eastern Washington",
        "state": "Washington",
        "group": "Washington",
        "accent": "var(--yb-coral)",
        "h1": "Digital Marketing for <span>Eastern Washington</span>",
        "lead": "SEO, Google Ads, and websites for businesses in Spokane, the Tri-Cities, Walla Walla, and everywhere in between.",
        "intro": [
            "Eastern Washington businesses often serve a big area with a lot of driving in between. Your customers search by town, so your marketing has to show up town by town, not just in the city you're based in.",
            "We work with businesses across the region and know what it takes to show up in each town you serve.",
        ],
        "industries": ["Contractors & trades", "Healthcare", "Agriculture", "Wineries & tourism", "Professional services"],
        "cities": ["Spokane", "Spokane Valley", "Kennewick", "Pasco", "Richland", "Walla Walla", "Pullman", "Cheney"],
        "city_links": {"Spokane": "/locations/spokane-wa", "Kennewick": "/locations/tri-cities-wa", "Pasco": "/locations/tri-cities-wa", "Richland": "/locations/tri-cities-wa", "Walla Walla": "/locations/walla-walla-wa"},
        "cases": ["tire", "refrig", "electrical"],
        "channels": "If you serve more than one town, we usually start with your Google Business Profile and a set of location pages so you can rank in each place you work. Google Ads fill in while that builds, targeted only to the towns you actually serve.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "chicago-il",
        "name": "Chicago",
        "short": "Chicago",
        "state": "Illinois",
        "group": "Illinois",
        "accent": "var(--yb-blue)",
        "h1": "Digital Marketing for <span>Chicago</span> Businesses",
        "lead": "SEO, Google Ads, and websites for companies in Chicago and the suburbs. Built around the neighborhoods you actually serve.",
        "intro": [
            "Chicago is one of the most competitive search markets in the country. Every neighborhood has its own map results, and the suburbs behave like separate cities. A campaign that targets \"Chicago\" as one big area wastes a lot of money.",
            "We build your SEO and ads around the areas you serve, so you show up in Lincoln Park or Naperville when that's where your customers are, and you're not paying for clicks from people who will never drive to you.",
        ],
        "industries": ["Manufacturing & distribution", "Law firms", "Healthcare", "Contractors & trades", "Restaurants"],
        "cities": ["Chicago", "Naperville", "Evanston", "Schaumburg", "Oak Park", "Aurora", "Joliet", "Elgin"],
        "cases": ["electrical", "refrig", "tire"],
        "channels": "In a market this size, we almost always split the work by area. Local SEO and location pages for the neighborhoods and suburbs you serve, plus Google Ads with tight geographic targeting. B2B companies often add LinkedIn and content marketing.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "phoenix-az",
        "name": "Phoenix",
        "short": "Phoenix",
        "state": "Arizona",
        "group": "Arizona",
        "accent": "#c77f12",
        "h1": "Digital Marketing for <span>Phoenix</span> Businesses",
        "lead": "SEO, Google Ads, and websites for companies in Phoenix, Scottsdale, Mesa, and the surrounding cities.",
        "intro": [
            "The Phoenix area is spread out. A customer in Gilbert usually isn't looking for a company in Glendale, and Google shows them businesses close by. Ranking for \"Phoenix\" alone won't bring in calls from the other cities you serve.",
            "We build location pages, Google Business Profiles, and ad targeting around the cities you work in. We also plan around the seasons, because summer changes what people in Phoenix search for.",
        ],
        "industries": ["HVAC & home services", "Solar", "Real estate", "Healthcare", "Contractors & trades"],
        "cities": ["Phoenix", "Scottsdale", "Mesa", "Tempe", "Chandler", "Gilbert", "Glendale", "Peoria"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Summer is the busiest season for most Phoenix home service companies. We usually pair local SEO with Google Ads that increase before summer starts, plus call tracking so you can see which campaigns booked jobs.",
        "local_faq": REMOTE_FAQ,
    },
]


CITIES = [
    {
        "slug": "yakima-wa", "name": "Yakima", "short": "Yakima", "state": "Washington", "region": "central-washington",
        "title": "Digital Marketing Agency Yakima WA | YB Marketing",
        "h1": "Digital Marketing for <span>Yakima</span> Businesses",
        "lead": "SEO, Google Ads, websites, and branding for Yakima businesses, with a sales rep here who can meet with you in person.",
        "intro": [
            "We work with a lot of businesses in Yakima. People here still ask friends for recommendations, but they check Google before they call. If you don't show up there, the referral often goes to someone else.",
            "We help Yakima businesses show up in Google Maps and search, build websites that work well on a phone, and run ads that only reach the towns you serve.",
        ],
        "cities": ["Yakima", "Selah", "Union Gap", "Moxee", "Terrace Heights", "Wapato", "Toppenish", "Sunnyside"],
        "cases": ["refrig", "tire", "electrical"],
        "channels": "Most Yakima businesses get the best return from Google Business Profile and local SEO. Google Ads cost much less here than in Seattle, so a modest budget can bring in steady calls. Seasonal businesses tied to harvest or tourism can raise ad budgets during their busy months.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "ellensburg-wa", "name": "Ellensburg", "short": "Ellensburg", "state": "Washington", "region": "central-washington",
        "title": "Digital Marketing Agency Ellensburg WA | YB Marketing",
        "h1": "Digital Marketing for <span>Ellensburg</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Ellensburg and across Kittitas County.",
        "intro": [
            "Ellensburg businesses serve a mix of longtime locals, Central Washington University students, and people passing through on I-90. Each group searches differently, and your website and Google listing need to work for all of them.",
            "We help you show up when people nearby search for what you do, and we make sure your website gives them a clear reason to call.",
        ],
        "cities": ["Ellensburg", "Cle Elum", "Kittitas", "Roslyn", "Thorp", "Easton"],
        "cases": ["refrig", "tire", "electrical"],
        "channels": "For most Ellensburg businesses we start with Google Business Profile and local SEO. If you rely on students or travelers, Google Ads and social media ads timed around the school year and travel seasons can fill the gaps.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "wenatchee-wa", "name": "Wenatchee", "short": "Wenatchee", "state": "Washington", "region": "central-washington",
        "title": "Digital Marketing Agency Wenatchee WA | YB Marketing",
        "h1": "Digital Marketing for <span>Wenatchee</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Wenatchee, East Wenatchee, and the surrounding towns.",
        "intro": [
            "People drive into Wenatchee from towns all over North Central Washington for services they can't get at home. That means your customers are searching from Leavenworth, Chelan, and Cashmere, not just Wenatchee.",
            "We set up your website, Google listing, and ads to reach the towns your customers actually come from, so you show up for the people willing to make the drive.",
        ],
        "cities": ["Wenatchee", "East Wenatchee", "Cashmere", "Leavenworth", "Chelan", "Quincy"],
        "cases": ["refrig", "electrical", "tire"],
        "channels": "If you serve customers from several towns, we usually start with your Google Business Profile and a set of location pages. Google Ads targeted to those towns bring in calls while SEO builds.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "spokane-wa", "name": "Spokane", "short": "Spokane", "state": "Washington", "region": "eastern-washington",
        "title": "Digital Marketing Agency Spokane WA | YB Marketing",
        "h1": "Digital Marketing for <span>Spokane</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Spokane, Spokane Valley, and the surrounding area.",
        "intro": [
            "Spokane is the biggest market in Eastern Washington, and it's competitive. You're up against strong local companies and national brands for the same searches, and customers compare a few options before they call.",
            "We help you show up in Google Maps and search across the neighborhoods and towns you serve, build a website that earns trust, and make sure leads get a fast follow up so you win the job.",
        ],
        "cities": ["Spokane", "Spokane Valley", "Liberty Lake", "Cheney", "Airway Heights", "Mead", "Deer Park"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "In a market Spokane's size, we usually pair local SEO with Google Ads targeted to the parts of town you serve. Call tracking shows which campaigns turn into booked jobs so the budget goes where it works.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "tri-cities-wa", "name": "Tri-Cities", "short": "Tri-Cities", "where": "the Tri-Cities", "state": "Washington", "region": "eastern-washington",
        "title": "Digital Marketing Agency Tri-Cities WA | Kennewick, Pasco & Richland | YB Marketing",
        "h1": "Digital Marketing for <span>Tri-Cities</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Kennewick, Pasco, Richland, and West Richland.",
        "intro": [
            "Kennewick, Pasco, and Richland are close together, but customers still search city by city. A business that only ranks in Kennewick can miss most of the calls coming from Pasco and Richland.",
            "We build your website and Google presence so you show up in each city you serve. For businesses with Spanish speaking customers, we can also create Spanish pages and ads.",
        ],
        "cities": ["Kennewick", "Pasco", "Richland", "West Richland", "Benton City", "Burbank"],
        "cases": ["tire", "refrig", "electrical"],
        "channels": "Most Tri-Cities businesses start with Google Business Profile and a page for each city they serve. Google Ads can target each city separately, so you can put more budget where your best customers are.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "walla-walla-wa", "name": "Walla Walla", "short": "Walla Walla", "state": "Washington", "region": "eastern-washington",
        "title": "Digital Marketing Agency Walla Walla WA | YB Marketing",
        "h1": "Digital Marketing for <span>Walla Walla</span> Businesses",
        "lead": "SEO, Google Ads, and websites for wineries, restaurants, and local businesses across Walla Walla County.",
        "intro": [
            "Walla Walla businesses serve two groups: visitors who come for wine country and locals who keep you busy the rest of the year. Visitors plan their trips online, often weeks ahead, while locals search when they need something today.",
            "We help you reach both. That means a website and Google listing that sell the experience to visitors, plus local SEO and ads that keep calls coming in during the slower months.",
        ],
        "cities": ["Walla Walla", "College Place", "Milton-Freewater", "Waitsburg", "Dayton"],
        "cases": ["refrig", "tire", "electrical"],
        "channels": "Wineries, hotels, and restaurants usually get the most from Google Business Profile, a strong website, and ads aimed at people planning a trip. Local service businesses do best with local SEO and Google Ads focused on Walla Walla and College Place.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "tacoma-wa", "name": "Tacoma", "short": "Tacoma", "state": "Washington", "region": None,
        "title": "Digital Marketing Agency Tacoma WA | YB Marketing",
        "h1": "Digital Marketing for <span>Tacoma</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Tacoma and across Pierce County.",
        "intro": [
            "Tacoma customers like supporting local businesses, but they also see Seattle companies in the same search results. If your website and Google listing don't look as strong, you can lose the call to someone farther away.",
            "We help you show up for searches in Tacoma and the nearby cities you serve, and we build websites that make it clear you're local, established, and easy to reach.",
        ],
        "cities": ["Tacoma", "Lakewood", "Puyallup", "University Place", "Gig Harbor", "Fife", "Federal Way"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Tacoma businesses start with Google Business Profile and local SEO. Click prices are higher than in Eastern Washington, so we spend time on call tracking and landing pages before increasing Google Ads budgets.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "vancouver-wa", "name": "Vancouver", "short": "Vancouver", "state": "Washington", "region": None,
        "title": "Digital Marketing Agency Vancouver WA | YB Marketing",
        "h1": "Digital Marketing for <span>Vancouver, WA</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Vancouver, Camas, and across Clark County.",
        "intro": [
            "Vancouver businesses often compete with Portland companies in the same search results. Many Clark County customers would rather hire a Washington business, but only if they can find you and tell you're local.",
            "We set up your website, Google listing, and ads so it's clear where you are and which areas you serve, and we keep ad spend focused on the Washington side of the river.",
        ],
        "cities": ["Vancouver", "Camas", "Washougal", "Battle Ground", "Ridgefield", "Hazel Dell"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "We usually start with Google Business Profile and local SEO focused on Clark County. Google Ads can be limited to Washington zip codes so you're not paying for clicks from customers you don't serve.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "boise-id", "name": "Boise", "short": "Boise", "state": "Idaho", "region": None,
        "title": "Digital Marketing Agency Boise ID | YB Marketing",
        "h1": "Digital Marketing for <span>Boise</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Boise, Meridian, Nampa, and the surrounding area.",
        "intro": [
            "Boise has grown quickly, and so has the number of businesses competing for the same customers. Searches that used to show a few local options now include national brands and new competitors.",
            "We help you stand out without overspending. We start with what will bring in leads soonest, then add more once it's working.",
        ],
        "cities": ["Boise", "Meridian", "Nampa", "Eagle", "Caldwell", "Kuna", "Star"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Boise businesses start with Google Business Profile and local SEO, with Google Ads bringing in calls while rankings build. If you serve Meridian, Nampa, or Eagle, we add location pages so you show up there too.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "coeur-dalene-id", "name": "Coeur d'Alene", "short": "Coeur d'Alene", "state": "Idaho", "region": None,
        "title": "Digital Marketing Agency Coeur d'Alene ID | YB Marketing",
        "h1": "Digital Marketing for <span>Coeur d'Alene</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Coeur d'Alene, Post Falls, and across Kootenai County.",
        "intro": [
            "Coeur d'Alene businesses get a rush of summer visitors and rely on locals the rest of the year. Visitors search on their phones while they're in town, and locals search when they need something done.",
            "We help you show up for both. That means a strong Google listing and website for visitors, plus local SEO and ads that keep calls coming in during the off season.",
        ],
        "cities": ["Coeur d'Alene", "Post Falls", "Hayden", "Rathdrum", "Sandpoint"],
        "cases": ["refrig", "tire", "electrical"],
        "channels": "Restaurants, lodging, and marinas usually get the most from Google Business Profile and a mobile friendly website. Trades and service businesses do best with local SEO and Google Ads focused on the towns they serve.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "aurora-co", "name": "Aurora", "short": "Aurora", "state": "Colorado", "region": "denver-co",
        "accent": "var(--yb-violet)",
        "title": "Digital Marketing Agency Aurora CO | YB Marketing",
        "h1": "Digital Marketing for <span>Aurora</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Aurora and across the east side of the Denver metro.",
        "intro": [
            "Aurora is the third largest city in Colorado and stretches across Arapahoe, Adams, and Douglas counties. A customer near Southlands and one near the Anschutz Medical Campus see different map results, so ranking in one part of town doesn't cover the rest.",
            "There's also an Aurora in Illinois. Your Google listing, website, and ads need to say Aurora, Colorado clearly so you're not losing searches or paying for clicks meant for someone else.",
        ],
        "cities": ["Aurora", "Denver", "Centennial", "Parker", "Englewood", "Commerce City"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Aurora service businesses start with Google Business Profile and local SEO, plus location pages for the parts of town they serve. Google Ads targeted by zip code keep spend inside your service area while rankings build.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "lakewood-co", "name": "Lakewood", "short": "Lakewood", "state": "Colorado", "region": "denver-co",
        "accent": "var(--yb-violet)",
        "title": "Digital Marketing Agency Lakewood CO | YB Marketing",
        "h1": "Digital Marketing for <span>Lakewood</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Lakewood and across Jefferson County.",
        "intro": [
            "Lakewood is the largest city in Jefferson County and sits right between Denver and the foothills. Customers here search for nearby options, and they compare you with companies in Denver, Golden, and Littleton in the same results.",
            "There's also a Lakewood in Washington, California, and Ohio. We make sure your listing and pages say Lakewood, Colorado so Google shows you to the right people.",
        ],
        "cities": ["Lakewood", "Denver", "Golden", "Wheat Ridge", "Littleton", "Morrison"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "For most Lakewood businesses we start with Google Business Profile and local SEO focused on Jefferson County. Google Ads fill in while rankings build, targeted to the neighborhoods and nearby cities you actually serve.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "boulder-co", "name": "Boulder", "short": "Boulder", "state": "Colorado", "region": "denver-co",
        "accent": "var(--yb-violet)",
        "title": "Digital Marketing Agency Boulder CO | YB Marketing",
        "h1": "Digital Marketing for <span>Boulder</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Boulder and across Boulder County.",
        "intro": [
            "Boulder is its own market. People here search for Boulder businesses, not Denver ones, and they read reviews and compare websites before they reach out.",
            "Demand also shifts with the University of Colorado calendar. Restaurants, retail, and rental businesses see big changes when students leave for the summer, and your marketing should plan for that.",
        ],
        "cities": ["Boulder", "Louisville", "Lafayette", "Superior", "Longmont", "Broomfield"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Boulder businesses get the best return from Google Business Profile, steady reviews, and a website that answers questions clearly. Google Ads work well for urgent services, and we adjust budgets around the school year when that affects your demand.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "littleton-co", "name": "Littleton", "short": "Littleton", "state": "Colorado", "region": "denver-co",
        "accent": "var(--yb-violet)",
        "title": "Digital Marketing Agency Littleton CO | YB Marketing",
        "h1": "Digital Marketing for <span>Littleton</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Littleton and the south Denver suburbs.",
        "intro": [
            "A Littleton mailing address covers a lot more than the city itself. Ken Caryl, Columbine, and other unincorporated areas use it too, so customers who say they live in Littleton may be miles from downtown Littleton.",
            "We build your website, Google listing, and ads around the areas you actually serve, including Highlands Ranch and Centennial nearby, so you show up for the right searches.",
        ],
        "cities": ["Littleton", "Highlands Ranch", "Ken Caryl", "Centennial", "Englewood", "Lakewood"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Littleton service businesses start with Google Business Profile and local SEO, plus pages for the nearby communities they serve. Google Ads targeted by zip code bring in calls while SEO builds.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "arvada-co", "name": "Arvada", "short": "Arvada", "state": "Colorado", "region": "denver-co",
        "accent": "var(--yb-violet)",
        "title": "Digital Marketing Agency Arvada CO | YB Marketing",
        "h1": "Digital Marketing for <span>Arvada</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Arvada and the northwest Denver suburbs.",
        "intro": [
            "Arvada sits in Jefferson and Adams counties, between Denver, Westminster, and Golden. Customers here have a lot of nearby options, and Google tends to show the closest businesses with strong reviews first.",
            "Olde Town Arvada and the G Line draw people in from other parts of the metro. For shops and restaurants, that means reaching visitors as well as neighbors.",
        ],
        "cities": ["Arvada", "Westminster", "Wheat Ridge", "Golden", "Broomfield", "Lakewood"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Arvada businesses start with Google Business Profile and local SEO. Service businesses add Google Ads targeted to the northwest metro, and shops and restaurants usually focus on reviews, photos, and social media.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "centennial-co", "name": "Centennial", "short": "Centennial", "state": "Colorado", "region": "denver-co",
        "accent": "var(--yb-violet)",
        "title": "Digital Marketing Agency Centennial CO | YB Marketing",
        "h1": "Digital Marketing for <span>Centennial</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Centennial and around the Denver Tech Center.",
        "intro": [
            "Centennial is home to a lot of company offices around the Denver Tech Center, along with busy residential neighborhoods. B2B companies and home service businesses here need very different marketing.",
            "Many businesses in the area have Englewood or Littleton mailing addresses even though they're in Centennial. Your Google listing and website should make your location and service area clear.",
        ],
        "cities": ["Centennial", "Greenwood Village", "Englewood", "Littleton", "Aurora", "Lone Tree"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Home service businesses usually start with Google Business Profile, local SEO, and Google Ads. B2B companies around the Tech Center often get more from SEO, LinkedIn, and content that answers buyers' questions.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "englewood-co", "name": "Englewood", "short": "Englewood", "state": "Colorado", "region": "denver-co",
        "accent": "var(--yb-violet)",
        "title": "Digital Marketing Agency Englewood CO | YB Marketing",
        "h1": "Digital Marketing for <span>Englewood</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Englewood and the south Denver metro.",
        "intro": [
            "Englewood borders Denver to the south and is home to Swedish Medical Center and Craig Hospital, plus the shops along South Broadway. Customers here easily choose between businesses in Englewood and Denver.",
            "Englewood zip codes also reach well beyond the city, into the Tech Center and parts of Centennial. We make sure Google knows exactly where you are and which areas you serve.",
        ],
        "cities": ["Englewood", "Denver", "Littleton", "Sheridan", "Cherry Hills Village", "Centennial"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Englewood businesses start with Google Business Profile and local SEO. Healthcare and professional service offices get a lot from reviews and clear service pages, and trades add Google Ads targeted to the south metro.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "naperville-il", "name": "Naperville", "short": "Naperville", "state": "Illinois", "region": "chicago-il",
        "accent": "var(--yb-blue)",
        "title": "Digital Marketing Agency Naperville IL | YB Marketing",
        "h1": "Digital Marketing for <span>Naperville</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Naperville and the western suburbs.",
        "intro": [
            "Naperville spans DuPage and Will counties, and the north and south ends of town feel like different markets. A customer near the Riverwalk and one down by Route 59 see different map results, so ranking downtown doesn't cover the whole city.",
            "Customers here compare options carefully and read reviews before they call. We help you show up across the parts of Naperville you serve and give people a website that answers their questions up front.",
        ],
        "cities": ["Naperville", "Aurora", "Lisle", "Wheaton", "Bolingbrook", "Plainfield"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Naperville businesses start with Google Business Profile, reviews, and local SEO. Google Ads targeted to the zip codes you serve bring in calls while rankings build, and location pages help you show up in Aurora, Lisle, and Plainfield too.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "evanston-il", "name": "Evanston", "short": "Evanston", "state": "Illinois", "region": "chicago-il",
        "accent": "var(--yb-blue)",
        "title": "Digital Marketing Agency Evanston IL | YB Marketing",
        "h1": "Digital Marketing for <span>Evanston</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Evanston and the North Shore.",
        "intro": [
            "Evanston sits right on the Chicago border, so your business shows up next to companies from Rogers Park and the rest of the North Side. Customers here can just as easily pick someone a few blocks into Chicago.",
            "Northwestern University also brings in students, staff, and visiting families every year. We help you show up for both the people who live here and the ones who are only in town for a while.",
        ],
        "cities": ["Evanston", "Chicago", "Skokie", "Wilmette", "Glenview", "Winnetka"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Evanston businesses get the most from Google Business Profile, reviews, and local SEO. Restaurants and shops add social media around the Northwestern calendar, and service businesses add Google Ads targeted to Evanston and the North Shore.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "schaumburg-il", "name": "Schaumburg", "short": "Schaumburg", "state": "Illinois", "region": "chicago-il",
        "accent": "var(--yb-blue)",
        "title": "Digital Marketing Agency Schaumburg IL | YB Marketing",
        "h1": "Digital Marketing for <span>Schaumburg</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Schaumburg and the northwest suburbs.",
        "intro": [
            "Schaumburg is home to Woodfield Mall and a lot of corporate offices along I-90. That brings in shoppers and office workers from all over the northwest suburbs, not just people who live in town.",
            "Customers here search for businesses close to where they work or shop, then compare you with companies in Hoffman Estates, Arlington Heights, and Palatine. We help you show up in the towns your customers come from.",
        ],
        "cities": ["Schaumburg", "Hoffman Estates", "Arlington Heights", "Palatine", "Elk Grove Village", "Rolling Meadows"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Retail and restaurants usually start with Google Business Profile and local SEO. B2B companies near the I-90 office corridor often add LinkedIn and content marketing, and trades add Google Ads targeted to the northwest suburbs.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "oak-park-il", "name": "Oak Park", "short": "Oak Park", "state": "Illinois", "region": "chicago-il",
        "accent": "var(--yb-blue)",
        "title": "Digital Marketing Agency Oak Park IL | YB Marketing",
        "h1": "Digital Marketing for <span>Oak Park</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Oak Park and the near west suburbs.",
        "intro": [
            "Oak Park borders Chicago's West Side, and a lot of people here walk or take the Green Line to the shops they use. Your Google listing is often what decides whether someone stops in or goes somewhere closer.",
            "Customers here also have plenty of Chicago options a few minutes away. We help you show up for searches in Oak Park, River Forest, Forest Park, and Berwyn, and make it clear you're the local choice.",
        ],
        "cities": ["Oak Park", "Chicago", "River Forest", "Forest Park", "Berwyn", "Cicero"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "For most Oak Park businesses we start with Google Business Profile, reviews, and local SEO. Shops and restaurants add social media, and service businesses add Google Ads targeted to Oak Park and the nearby towns they serve.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "aurora-il", "name": "Aurora", "short": "Aurora", "state": "Illinois", "region": "chicago-il",
        "accent": "var(--yb-blue)",
        "title": "Digital Marketing Agency Aurora IL | YB Marketing",
        "h1": "Digital Marketing for <span>Aurora</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Aurora and the Fox Valley.",
        "intro": [
            "Aurora is the second largest city in Illinois and stretches across Kane, DuPage, Will, and Kendall counties. Customers on the far east side near Naperville and those near downtown on the Fox River see different map results.",
            "There's also an Aurora in Colorado. Your Google listing, website, and ads need to say Aurora, Illinois clearly so you're not losing searches or paying for clicks meant for someone else.",
        ],
        "cities": ["Aurora", "Naperville", "North Aurora", "Montgomery", "Oswego", "Batavia"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Aurora businesses start with Google Business Profile and local SEO, plus location pages for the parts of town and nearby Fox Valley towns they serve. Many also add Spanish pages and ads to reach Aurora's large Spanish speaking community.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "joliet-il", "name": "Joliet", "short": "Joliet", "state": "Illinois", "region": "chicago-il",
        "accent": "var(--yb-blue)",
        "title": "Digital Marketing Agency Joliet IL | YB Marketing",
        "h1": "Digital Marketing for <span>Joliet</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Joliet and across Will County.",
        "intro": [
            "Joliet is the Will County seat and sits where I-80 and I-55 meet, which makes it one of the biggest warehouse and logistics hubs in the Chicago area. A lot of the businesses here sell to other businesses, not just to homeowners.",
            "Homeowners in Joliet compare you with companies in Plainfield, Lockport, and New Lenox. We help you show up in the towns you serve, whether your customers are households or the companies along the interstate.",
        ],
        "cities": ["Joliet", "Plainfield", "Shorewood", "Lockport", "New Lenox", "Romeoville"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Home service businesses usually start with Google Business Profile, local SEO, and Google Ads targeted to Will County. Logistics and industrial suppliers do better with a strong website, LinkedIn, and search ads aimed at the companies they sell to.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "elgin-il", "name": "Elgin", "short": "Elgin", "state": "Illinois", "region": "chicago-il",
        "accent": "var(--yb-blue)",
        "title": "Digital Marketing Agency Elgin IL | YB Marketing",
        "h1": "Digital Marketing for <span>Elgin</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Elgin and the northern Fox Valley.",
        "intro": [
            "Elgin sits on the Fox River and spans Kane and Cook counties. Customers here compare you with businesses in South Elgin, Bartlett, and St. Charles, and Google shows them whoever is closest and best reviewed.",
            "Elgin also has a large Spanish speaking community. If those are your customers, Spanish pages, a Spanish Google listing description, and Spanish ads can reach people your competitors miss.",
        ],
        "cities": ["Elgin", "South Elgin", "Bartlett", "Streamwood", "Carpentersville", "St. Charles"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Elgin businesses start with Google Business Profile and local SEO. Google Ads targeted to the towns you serve bring in calls while rankings build, and Spanish pages and ads are worth adding if many of your customers speak Spanish.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "selah-wa", "name": "Selah", "short": "Selah", "state": "Washington", "region": "central-washington",
        "title": "Digital Marketing Agency Selah WA | YB Marketing",
        "h1": "Digital Marketing for <span>Selah</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Selah and the Upper Valley.",
        "intro": [
            "Selah sits just north of Yakima through the Selah Gap, and a lot of people here drive into Yakima for work and shopping. When they search for a service, Google often shows Yakima companies first unless your listing makes it clear you're right here in town.",
            "We help Selah businesses show up for the people who live nearby, from Naches to East Selah, and build websites that make it easy to call.",
        ],
        "cities": ["Selah", "Yakima", "Naches", "Gleed", "Moxee", "Terrace Heights"],
        "cases": ["refrig", "tire", "electrical"],
        "channels": "Most Selah businesses get the best return from Google Business Profile, reviews, and local SEO. Google Ads targeted to Selah and the Upper Valley cost little here and can bring in steady calls.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "sunnyside-wa", "name": "Sunnyside", "short": "Sunnyside", "state": "Washington", "region": "central-washington",
        "title": "Digital Marketing Agency Sunnyside WA | YB Marketing",
        "h1": "Digital Marketing for <span>Sunnyside</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Sunnyside and the Lower Yakima Valley.",
        "intro": [
            "Sunnyside is the center of the Lower Valley, and people come in from Grandview, Granger, Mabton, and Outlook to shop and get things done. Your customers are searching from all of those towns, not just Sunnyside.",
            "Most of the families here speak Spanish at home. If that describes your customers, a Spanish website, a Spanish Google listing description, and Spanish ads can reach people your competitors miss.",
        ],
        "cities": ["Sunnyside", "Grandview", "Granger", "Mabton", "Outlook", "Zillah"],
        "cases": ["refrig", "tire", "electrical"],
        "channels": "We usually start with Google Business Profile and local SEO in English and Spanish. Google Ads and Facebook ads targeted to the Lower Valley towns are inexpensive here and bring in calls quickly.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "union-gap-wa", "name": "Union Gap", "short": "Union Gap", "state": "Washington", "region": "central-washington",
        "title": "Digital Marketing Agency Union Gap WA | YB Marketing",
        "h1": "Digital Marketing for <span>Union Gap</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Union Gap and the south end of Yakima.",
        "intro": [
            "Union Gap is home to the Valley Mall and a long stretch of auto dealers, retailers, and service shops near I-82. Shoppers come from across the Yakima Valley, so your customers are searching from Wapato, Moxee, and Yakima as much as Union Gap.",
            "Because Union Gap and Yakima run together, Google can mix up where you are. We make sure your listing and website say clearly where you're located and which towns you serve.",
        ],
        "cities": ["Union Gap", "Yakima", "Moxee", "Parker", "Wapato", "Selah"],
        "cases": ["tire", "refrig", "electrical"],
        "channels": "Retail and auto businesses usually start with Google Business Profile, reviews, and local SEO. Google Ads and Facebook ads targeted to the whole valley help bring in shoppers who make the drive.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "moses-lake-wa", "name": "Moses Lake", "short": "Moses Lake", "state": "Washington", "region": "central-washington",
        "title": "Digital Marketing Agency Moses Lake WA | YB Marketing",
        "h1": "Digital Marketing for <span>Moses Lake</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Moses Lake and across the Columbia Basin.",
        "intro": [
            "Moses Lake is the hub of the Columbia Basin. Farm families, plant workers, and people from Othello, Ephrata, and Warden all come here to shop and hire local services, so your customers are spread over a big area.",
            "New manufacturing jobs have brought a lot of new residents who don't know the local businesses yet. They find you on Google, so your listing and website need to look as good as the companies they knew back home.",
        ],
        "cities": ["Moses Lake", "Ephrata", "Othello", "Quincy", "Soap Lake", "Warden"],
        "cases": ["refrig", "tire", "electrical"],
        "channels": "Most Moses Lake businesses start with Google Business Profile and local SEO, plus location pages for the Basin towns they serve. Google Ads cost much less here than in Seattle or Spokane, so a small budget goes a long way.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "toppenish-wa", "name": "Toppenish", "short": "Toppenish", "state": "Washington", "region": "central-washington",
        "title": "Digital Marketing Agency Toppenish WA | YB Marketing",
        "h1": "Digital Marketing for <span>Toppenish</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Toppenish and the Yakama Nation.",
        "intro": [
            "Toppenish is known for its murals and sits within the Yakama Nation, with customers coming in from Wapato, Harrah, White Swan, and Zillah. Visitors also stop through for the murals and the rodeo, and most of them find you on their phone.",
            "Many families here speak Spanish at home. We help you show up for both local customers and visitors, in English and Spanish when it makes sense.",
        ],
        "cities": ["Toppenish", "Wapato", "Zillah", "Harrah", "White Swan", "Granger"],
        "cases": ["refrig", "tire", "electrical"],
        "channels": "We usually start with Google Business Profile and local SEO, then add Spanish pages and Facebook ads if many of your customers speak Spanish. Google Ads here are inexpensive and easy to target to the towns you serve.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "spokane-valley-wa", "name": "Spokane Valley", "short": "Spokane Valley", "state": "Washington", "region": "eastern-washington",
        "title": "Digital Marketing Agency Spokane Valley WA | YB Marketing",
        "h1": "Digital Marketing for <span>Spokane Valley</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Spokane Valley, Liberty Lake, and the east side of Spokane County.",
        "intro": [
            "Spokane Valley became its own city in 2003, but Google still lumps a lot of searches in with Spokane. If your listing and website don't say Spokane Valley clearly, you can end up competing with every company downtown.",
            "Customers here search from along Sprague and I-90 out to Liberty Lake and Otis Orchards. We help you show up in the parts of the Valley you serve and turn those searches into calls.",
        ],
        "cities": ["Spokane Valley", "Spokane", "Liberty Lake", "Millwood", "Otis Orchards", "Newman Lake"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Spokane Valley businesses start with Google Business Profile, reviews, and local SEO. Google Ads targeted to the Valley zip codes keep you from paying for clicks across the county.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "pullman-wa", "name": "Pullman", "short": "Pullman", "state": "Washington", "region": "eastern-washington",
        "title": "Digital Marketing Agency Pullman WA | YB Marketing",
        "h1": "Digital Marketing for <span>Pullman</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Pullman and across the Palouse.",
        "intro": [
            "Pullman is home to Washington State University, and the town's population swings with the school year. A big share of your customers turns over every fall, and new students and staff find businesses almost entirely through Google.",
            "Moscow, Idaho is only eight miles away, so customers compare you with businesses across the state line. We help you show up on both sides and give people a clear reason to pick you.",
        ],
        "cities": ["Pullman", "Moscow", "Colfax", "Palouse", "Albion", "Uniontown"],
        "cases": ["tire", "refrig", "electrical"],
        "channels": "Most Pullman businesses get the best return from Google Business Profile and local SEO. Restaurants and shops add social media around the WSU calendar, and service businesses add Google Ads targeted to Pullman and Moscow.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "cheney-wa", "name": "Cheney", "short": "Cheney", "state": "Washington", "region": "eastern-washington",
        "title": "Digital Marketing Agency Cheney WA | YB Marketing",
        "h1": "Digital Marketing for <span>Cheney</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Cheney and the West Plains.",
        "intro": [
            "Cheney is home to Eastern Washington University and sits about 20 minutes southwest of Spokane. Students, staff, and families in Medical Lake and Airway Heights all search for local options before driving into Spokane.",
            "If you don't show up in those searches, Google sends them to a Spokane company. We help you rank in Cheney and the West Plains towns you serve, so the local choice is the one they see first.",
        ],
        "cities": ["Cheney", "Spokane", "Airway Heights", "Medical Lake", "Four Lakes", "Spangle"],
        "cases": ["tire", "refrig", "electrical"],
        "channels": "Most Cheney businesses start with Google Business Profile and local SEO. Shops and restaurants add social media around the EWU school year, and service businesses add Google Ads targeted to the West Plains.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "oakland-ca", "name": "Oakland", "short": "Oakland", "state": "California", "region": "san-francisco-bay-area",
        "accent": "var(--yb-cyan)",
        "title": "Digital Marketing Agency Oakland CA | YB Marketing",
        "h1": "Digital Marketing for <span>Oakland</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Oakland and the East Bay.",
        "intro": [
            "Oakland customers like to support local businesses, but San Francisco companies show up in the same search results and bid on the same ads. Your listing and website need to make it obvious you're right here in the East Bay.",
            "Oakland is also a city of neighborhoods. Someone in Rockridge and someone in Fruitvale see different map results, so we build your SEO and ads around the parts of town you actually serve.",
        ],
        "cities": ["Oakland", "Berkeley", "Alameda", "Emeryville", "San Leandro", "Piedmont"],
        "cases": ["electrical", "refrig", "tire"],
        "channels": "Most Oakland businesses start with Google Business Profile, reviews, and local SEO. Click prices are high across the Bay Area, so we set up call tracking and tight targeting before increasing Google Ads budgets.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "san-jose-ca", "name": "San Jose", "short": "San Jose", "state": "California", "region": "san-francisco-bay-area",
        "accent": "var(--yb-cyan)",
        "title": "Digital Marketing Agency San Jose CA | YB Marketing",
        "h1": "Digital Marketing for <span>San Jose</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in San Jose and across Silicon Valley.",
        "intro": [
            "San Jose is the biggest city in the Bay Area and it's spread out. A homeowner in Willow Glen and one in Evergreen or Berryessa see different businesses in Google Maps, so ranking for \"San Jose\" alone misses a lot of calls.",
            "Customers here are used to good websites and fast replies. We help you show up across the parts of San Jose you serve and make sure every lead gets a quick follow up.",
        ],
        "cities": ["San Jose", "Santa Clara", "Campbell", "Milpitas", "Los Gatos", "Cupertino"],
        "cases": ["electrical", "refrig", "tire"],
        "channels": "We usually pair Google Business Profile and local SEO with location pages for the neighborhoods and nearby cities you serve. Google Ads here are expensive, so we start with tight targeting, negative keywords, and call tracking.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "berkeley-ca", "name": "Berkeley", "short": "Berkeley", "state": "California", "region": "san-francisco-bay-area",
        "accent": "var(--yb-cyan)",
        "title": "Digital Marketing Agency Berkeley CA | YB Marketing",
        "h1": "Digital Marketing for <span>Berkeley</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Berkeley and the inner East Bay.",
        "intro": [
            "Berkeley customers do their homework. They read reviews, check your website, and often care about how you run your business as much as what you charge. A thin website or a listing with a few old reviews loses them quickly.",
            "UC Berkeley also brings in students, staff, and visiting families all year. We help you show up for both the people who live here and the ones only in town for a while, from Telegraph to Fourth Street.",
        ],
        "cities": ["Berkeley", "Oakland", "Albany", "El Cerrito", "Emeryville", "Richmond"],
        "cases": ["electrical", "refrig", "tire"],
        "channels": "Most Berkeley businesses get the most from Google Business Profile, reviews, and a website that tells your story clearly. Restaurants and shops add social media, and service businesses add Google Ads targeted to Berkeley and nearby cities.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "san-mateo-ca", "name": "San Mateo", "short": "San Mateo", "state": "California", "region": "san-francisco-bay-area",
        "accent": "var(--yb-cyan)",
        "title": "Digital Marketing Agency San Mateo CA | YB Marketing",
        "h1": "Digital Marketing for <span>San Mateo</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in San Mateo and along the Peninsula.",
        "intro": [
            "San Mateo sits in the middle of the Peninsula, between San Francisco and Silicon Valley. Customers here can just as easily hire someone from Burlingame, Foster City, or Redwood City, and Google shows them whoever is closest and best reviewed.",
            "We help you show up across the Peninsula towns you serve and build a website that earns trust with customers who expect a polished experience.",
        ],
        "cities": ["San Mateo", "Burlingame", "Foster City", "Belmont", "Redwood City", "Hillsborough"],
        "cases": ["electrical", "refrig", "tire"],
        "channels": "Most San Mateo businesses start with Google Business Profile, reviews, and local SEO. Google Ads work well when they're limited to the Peninsula towns you serve, with call tracking so you can see which clicks turn into jobs.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "palo-alto-ca", "name": "Palo Alto", "short": "Palo Alto", "state": "California", "region": "san-francisco-bay-area",
        "accent": "var(--yb-cyan)",
        "title": "Digital Marketing Agency Palo Alto CA | YB Marketing",
        "h1": "Digital Marketing for <span>Palo Alto</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Palo Alto and the surrounding Peninsula cities.",
        "intro": [
            "Palo Alto has some of the most expensive advertising in the country. Clicks for common services can cost more than a meal downtown, so a campaign that isn't set up carefully burns through budget fast.",
            "Customers here, from Stanford staff to families in Old Palo Alto, expect a good website and quick answers. We help you show up in Palo Alto, Menlo Park, and Mountain View and make every click count.",
        ],
        "cities": ["Palo Alto", "Menlo Park", "Mountain View", "Los Altos", "Stanford", "East Palo Alto"],
        "cases": ["electrical", "refrig", "tire"],
        "channels": "We usually lean on local SEO, Google Business Profile, and reviews here, because they keep bringing in calls without paying per click. When we run Google Ads, we start small with tight targeting and call tracking.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "fremont-ca", "name": "Fremont", "short": "Fremont", "state": "California", "region": "san-francisco-bay-area",
        "accent": "var(--yb-cyan)",
        "title": "Digital Marketing Agency Fremont CA | YB Marketing",
        "h1": "Digital Marketing for <span>Fremont</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Fremont and the southern East Bay.",
        "intro": [
            "Fremont is one of the largest cities in the Bay Area and one of the most diverse. Many households speak a language other than English at home, and they search in the language they're most comfortable with.",
            "Fremont is also home to a lot of factories and suppliers. We help homeowners and businesses in Fremont, Newark, and Union City find you, whether you sell to families or other companies.",
        ],
        "cities": ["Fremont", "Newark", "Union City", "Hayward", "Milpitas", "Pleasanton"],
        "cases": ["electrical", "refrig", "tire"],
        "channels": "Most Fremont businesses start with Google Business Profile and local SEO. B2B suppliers add LinkedIn and search ads aimed at the companies they sell to, and we can add pages in other languages if your customers need them.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "walnut-creek-ca", "name": "Walnut Creek", "short": "Walnut Creek", "state": "California", "region": "san-francisco-bay-area",
        "accent": "var(--yb-cyan)",
        "title": "Digital Marketing Agency Walnut Creek CA | YB Marketing",
        "h1": "Digital Marketing for <span>Walnut Creek</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Walnut Creek and central Contra Costa County.",
        "intro": [
            "Walnut Creek is the shopping and dining center of central Contra Costa County. People drive in from Lafayette, Pleasant Hill, Concord, and Danville, so your customers are searching from all over the 680 corridor.",
            "Homeowners here compare a few options and read reviews before they call. We help you show up in the towns you serve and give them a website that makes the decision easy.",
        ],
        "cities": ["Walnut Creek", "Concord", "Lafayette", "Pleasant Hill", "Danville", "Martinez"],
        "cases": ["electrical", "refrig", "tire"],
        "channels": "Most Walnut Creek businesses start with Google Business Profile, reviews, and local SEO. Service businesses add Google Ads targeted to the 680 corridor, with call tracking so the budget goes to what books jobs.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "scottsdale-az", "name": "Scottsdale", "short": "Scottsdale", "state": "Arizona", "region": "phoenix-az",
        "accent": "#c77f12",
        "title": "Digital Marketing Agency Scottsdale AZ | YB Marketing",
        "h1": "Digital Marketing for <span>Scottsdale</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Scottsdale, Paradise Valley, and the north valley.",
        "intro": [
            "Scottsdale customers expect a lot. Whether they're booking a med spa, a pool builder, or a table in Old Town, they judge you by your website and reviews before they ever call.",
            "The city also fills up with winter visitors and resort guests from fall through spring. We help you reach year round residents and seasonal visitors, and plan ad budgets around the busy months.",
        ],
        "cities": ["Scottsdale", "Paradise Valley", "Fountain Hills", "Cave Creek", "Phoenix", "Tempe"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Scottsdale businesses start with Google Business Profile, reviews, and a website that looks the part. Google Ads and social media ads work well when they're timed around the winter season and targeted to the neighborhoods you serve.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "mesa-az", "name": "Mesa", "short": "Mesa", "state": "Arizona", "region": "phoenix-az",
        "accent": "#c77f12",
        "title": "Digital Marketing Agency Mesa AZ | YB Marketing",
        "h1": "Digital Marketing for <span>Mesa</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Mesa and across the East Valley.",
        "intro": [
            "Mesa is the third largest city in Arizona and covers a lot of ground, from the Tempe border out past the 202. A customer in west Mesa and one near Eastmark see different map results, so one listing downtown won't cover the whole city.",
            "Mesa also has a big winter population living in RV parks and retirement communities. We help you reach year round families and seasonal residents, each when they're most likely to call.",
        ],
        "cities": ["Mesa", "Gilbert", "Tempe", "Chandler", "Apache Junction", "Queen Creek"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Mesa businesses start with Google Business Profile and local SEO, plus location pages for the parts of the East Valley they serve. Home service companies add Google Ads that ramp up before summer.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "tempe-az", "name": "Tempe", "short": "Tempe", "state": "Arizona", "region": "phoenix-az",
        "accent": "#c77f12",
        "title": "Digital Marketing Agency Tempe AZ | YB Marketing",
        "h1": "Digital Marketing for <span>Tempe</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Tempe and the central East Valley.",
        "intro": [
            "Tempe is home to Arizona State University, and a big part of the city turns over every school year. New students and staff don't know the local businesses yet, so they find them on Google.",
            "Tempe also has a lot of offices and longtime homeowners south of the US 60. We help you show up for the customers you want, whether that's students near Mill Avenue or families in south Tempe.",
        ],
        "cities": ["Tempe", "Mesa", "Chandler", "Scottsdale", "Phoenix", "Guadalupe"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Restaurants and shops usually start with Google Business Profile and social media timed around the ASU calendar. Service businesses do best with local SEO and Google Ads targeted to the parts of Tempe they serve.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "chandler-az", "name": "Chandler", "short": "Chandler", "state": "Arizona", "region": "phoenix-az",
        "accent": "#c77f12",
        "title": "Digital Marketing Agency Chandler AZ | YB Marketing",
        "h1": "Digital Marketing for <span>Chandler</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Chandler and the southeast valley.",
        "intro": [
            "Chandler has grown into one of the East Valley's biggest job centers, with Intel and a long list of tech companies along the Price Road corridor. A lot of residents are newer to the area and pick businesses based on what they find online.",
            "Customers here compare you with companies in Gilbert, Tempe, and Mesa. We help you show up in the parts of Chandler and the nearby cities you serve, and turn those searches into calls.",
        ],
        "cities": ["Chandler", "Gilbert", "Tempe", "Mesa", "Sun Lakes", "Queen Creek"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Chandler businesses start with Google Business Profile, reviews, and local SEO. Home service companies add Google Ads before summer, and B2B companies serving the tech corridor add LinkedIn and search ads.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "gilbert-az", "name": "Gilbert", "short": "Gilbert", "state": "Arizona", "region": "phoenix-az",
        "accent": "#c77f12",
        "title": "Digital Marketing Agency Gilbert AZ | YB Marketing",
        "h1": "Digital Marketing for <span>Gilbert</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Gilbert and the southeast valley.",
        "intro": [
            "Gilbert has grown fast, and a lot of the families here moved in during the last twenty years. They don't have a go to plumber, dentist, or landscaper yet, so they search Google and ask in neighborhood Facebook groups.",
            "Being visible in both places matters here. We help you show up in Google Maps across Gilbert and earn the reviews that get you recommended, from the Heritage District to the south end of town.",
        ],
        "cities": ["Gilbert", "Mesa", "Chandler", "Queen Creek", "San Tan Valley", "Tempe"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Gilbert businesses start with Google Business Profile, reviews, and local SEO. Facebook ads work well for reaching families here, and home service companies add Google Ads that ramp up before summer.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "glendale-az", "name": "Glendale", "short": "Glendale", "state": "Arizona", "region": "phoenix-az",
        "accent": "#c77f12",
        "title": "Digital Marketing Agency Glendale AZ | YB Marketing",
        "h1": "Digital Marketing for <span>Glendale</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Glendale and the West Valley.",
        "intro": [
            "Glendale is home to State Farm Stadium and Westgate, which bring in big crowds on game and event days. Restaurants, hotels, and shops nearby can win a lot of that traffic if they show up when visitors search.",
            "There's also a Glendale in California. Your listing, website, and ads need to say Glendale, Arizona clearly so you're not losing searches or paying for clicks meant for someone else.",
        ],
        "cities": ["Glendale", "Peoria", "Phoenix", "Surprise", "Sun City", "El Mirage"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Glendale businesses start with Google Business Profile and local SEO. Restaurants and hotels add ads timed around the event calendar, and home service companies add Google Ads targeted to the West Valley.",
        "local_faq": REMOTE_FAQ,
    },
    {
        "slug": "peoria-az", "name": "Peoria", "short": "Peoria", "state": "Arizona", "region": "phoenix-az",
        "accent": "#c77f12",
        "title": "Digital Marketing Agency Peoria AZ | YB Marketing",
        "h1": "Digital Marketing for <span>Peoria</span> Businesses",
        "lead": "SEO, Google Ads, and websites for businesses in Peoria and the northwest valley.",
        "intro": [
            "Peoria stretches from the older neighborhoods near Glendale all the way north to Lake Pleasant. Customers at each end see different businesses in Google Maps, so we build your marketing around the parts of town you actually serve.",
            "Spring training brings crowds to the Peoria Sports Complex every year, and winter visitors fill the nearby retirement communities. We help you plan for the busy months and keep calls coming the rest of the year.",
        ],
        "cities": ["Peoria", "Glendale", "Surprise", "Sun City", "Sun City West", "Phoenix"],
        "cases": ["electrical", "tire", "refrig"],
        "channels": "Most Peoria businesses start with Google Business Profile, reviews, and local SEO. Home service companies add Google Ads that ramp up before summer, and restaurants add ads around spring training season.",
        "local_faq": REMOTE_FAQ,
    },
]
for _c in CITIES:
    _c.setdefault("accent", "var(--yb-blue)")

PAGE_CSS = """
.lc-hero{position:relative;overflow:hidden;background:var(--grad-navy);padding:84px 0 120px}
.lc-hero::before{content:'';position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.85;pointer-events:none}
.lc-hero::after{content:'';position:absolute;right:-160px;top:-160px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(43,196,240,.18),transparent 65%);pointer-events:none}
.lc-hero .container{position:relative;z-index:1}
.lc-hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:56px;align-items:center}
.lc-pin{display:inline-flex;align-items:center;gap:8px;padding:7px 14px 7px 10px;border-radius:var(--r-pill);background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);color:#fff;font-size:13px;font-weight:700;letter-spacing:.02em}
.lc-pin svg{width:16px;height:16px;color:var(--yb-cyan)}
.lc-hero h1{color:#fff;font-size:clamp(2.3rem,4.2vw,3.5rem);line-height:1.08;margin:20px 0 18px}
.lc-hero h1 span{background:var(--grad-brand);-webkit-background-clip:text;background-clip:text;color:transparent}
.lc-hero-lead{color:var(--fg2-on-dark);font-size:17.5px;line-height:1.7;max-width:540px;margin:0 0 28px}
.lc-proof{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:30px}
.lc-proof span{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:var(--r-pill);background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);color:#fff;font-size:13.5px;font-weight:600}
.lc-proof svg{width:13px;height:13px;color:var(--yb-cyan)}
.lc-ratings{display:flex;flex-wrap:wrap;gap:28px}
.lc-rating{display:flex;align-items:center;gap:14px;text-decoration:none}
.lc-rating .yelp-stars{gap:3px}
.lc-rating .yelp-star{width:18px;height:18px;border-radius:3px;background:#FF1A1A;display:flex;align-items:center;justify-content:center}
.lc-rating .yelp-star svg{width:12px;height:12px}
.yelp-word{font-family:var(--font-display);font-weight:800;font-size:14px;color:#FF1A1A;letter-spacing:-.02em}
.lc-rating-num{font-family:var(--font-display);font-weight:800;font-size:40px;color:#fff;line-height:1}
.lc-rating-stars{display:flex;gap:3px;color:var(--yb-amber)}
.lc-rating-stars svg{width:18px;height:18px}
.lc-rating-label{display:flex;align-items:center;gap:6px;color:var(--fg2-on-dark);font-size:13px;font-weight:600;margin-top:5px}
.lc-rating-label svg{width:15px;height:15px}
.lc-form-card{background:#fff;border-radius:var(--r-xl,24px);padding:32px 32px 26px;box-shadow:0 30px 80px rgba(8,16,40,.45);position:relative}
.lc-form-card::before{content:'';position:absolute;left:28px;right:28px;top:-1px;height:4px;border-radius:0 0 4px 4px;background:var(--grad-brand)}
.lc-form-card h2{font-size:24px;margin:0 0 6px}
.lc-form-card > p{font-size:14.5px;color:var(--fg2);margin:0 0 20px;line-height:1.6}
.lc-form-card .yb-lead-form textarea{min-height:84px}
.lc-section{padding:88px 0}
.lc-soft{background:var(--bg-soft)}
.lc-head{max-width:720px;margin:0 auto 44px;text-align:center}
.lc-head h2{margin:12px 0 14px;text-wrap:balance}
.lc-head p{color:var(--fg2);font-size:16.5px;line-height:1.7;margin:0}
.lc-reviews{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:-64px;position:relative;z-index:2}
.lc-review{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:24px;box-shadow:var(--sh-md);display:flex;flex-direction:column}
.lc-review-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.lc-review-top .rv-stars{display:flex;gap:2px;color:var(--yb-amber)}
.lc-review-top .rv-stars svg{width:15px;height:15px}
.lc-review-top .g svg{width:19px;height:19px;display:block}
.lc-review p{font-size:14.5px;line-height:1.65;color:var(--ink);margin:0 0 16px;flex:1}
.lc-review-by{display:flex;align-items:center;gap:10px;font-weight:700;font-size:14px;color:var(--ink)}
.lc-avatar{width:34px;height:34px;border-radius:50%;background:var(--grad-brand);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-family:var(--font-display);font-weight:700}
.lc-reviews-link{text-align:center;margin-top:22px;font-weight:700;font-size:14.5px}
.lc-reviews-link a{color:var(--yb-blue);text-decoration:none}
.lc-intro{display:grid;grid-template-columns:1.15fr .85fr;gap:56px;align-items:start}
.lc-intro h2{margin:12px 0 18px}
.lc-intro p{font-size:16.5px;line-height:1.75;color:var(--fg2);margin:0 0 16px}
.lc-panel{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:28px;box-shadow:var(--sh-sm)}
.lc-panel h3{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--fg3);margin:0 0 12px}
.lc-panel h3 + .lc-chips{margin-bottom:24px}
.lc-panel .lc-chips:last-child{margin-bottom:0}
.lc-chips{display:flex;flex-wrap:wrap;gap:8px}
.lc-chips span,.lc-chips a{display:inline-flex;align-items:center;gap:6px;padding:7px 12px;border-radius:var(--r-pill);background:var(--bg-soft);border:1px solid var(--line);font-size:13.5px;font-weight:600;color:var(--ink);text-decoration:none}
.lc-chips a{color:var(--yb-blue);border-color:rgba(43,108,240,.25);background:var(--wash-blue)}
.lc-chips a:hover{background:#fff}
.lc-chips svg{width:12px;height:12px}
.lc-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:56px}
.lc-stat{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:26px 22px;box-shadow:var(--sh-sm);position:relative;overflow:hidden}
.lc-stat::before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--grad-brand)}
.lc-stat > *{position:relative}
.lc-ai{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.lc-ai-card{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:26px 24px;box-shadow:var(--sh-sm)}
.lc-ai-card h3{font-size:18px;margin:0 0 8px}
.lc-ai-card p{font-size:14.5px;line-height:1.65;color:var(--fg2);margin:0}
.lc-ai-tag{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--yb-blue,#2B6CB0);background:rgba(43,108,176,.08);border-radius:999px;padding:5px 11px;margin-bottom:14px}
.lc-ai-more{text-align:center;margin-top:30px;font-size:15px}
.lc-ai-more a{font-weight:700}
.lc-stat strong{display:block;font-family:var(--font-display);font-size:34px;line-height:1;background:var(--grad-brand);-webkit-background-clip:text;background-clip:text;color:transparent;margin-bottom:8px}
.lc-stat span{color:var(--fg2);font-size:13.5px;line-height:1.45}
.lc-why{display:grid;grid-template-columns:.9fr 1.1fr;gap:56px;align-items:center}
.lc-why h2{margin:12px 0 18px}
.lc-why p{font-size:16.5px;line-height:1.75;color:var(--fg2);margin:0 0 16px}
.lc-why-list{display:grid;gap:14px}
.lc-why-item{display:flex;gap:16px;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:20px 22px;box-shadow:var(--sh-sm)}
.lc-why-num{flex:none;width:38px;height:38px;border-radius:12px;background:var(--grad-brand);color:#fff;display:flex;align-items:center;justify-content:center;font-family:var(--font-display);font-weight:800;font-size:15px}
.lc-why-item h3{font-size:16.5px;margin:2px 0 4px}
.lc-why-item p{font-size:14.5px;margin:0;line-height:1.6}
.lc-cases{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.lc-case{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;text-decoration:none;color:inherit;box-shadow:var(--sh-sm);transition:transform .25s ease,box-shadow .25s ease}
.lc-case:hover{transform:translateY(-5px);box-shadow:var(--sh-md)}
.lc-case-top{padding:26px 26px 20px;border-top:4px solid var(--ac);border-bottom:1px solid var(--line);margin:0 0 0}
.lc-case-top strong{display:block;font-family:var(--font-display);font-size:44px;line-height:1;margin-bottom:8px;color:var(--ac)}
.lc-case-top span{font-size:13px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--fg3,#6B7591)}
.lc-case-body{padding:20px 26px 24px;display:flex;flex-direction:column;flex:1}
.lc-case-body h3{font-size:17.5px;margin:0 0 8px}
.lc-case-body p{font-size:14.5px;line-height:1.6;color:var(--fg2);margin:0 0 16px;flex:1}
.lc-case-more{display:inline-flex;align-items:center;gap:6px;font-weight:700;font-size:14px;color:var(--yb-blue)}
.lc-case-more svg{width:15px;height:15px}
.lc-svcs{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.lc-svc{background:#fff;border:1px solid var(--line);border-top:4px solid var(--ac);border-radius:var(--r-lg);padding:26px 24px;box-shadow:var(--sh-sm);display:flex;flex-direction:column}
.lc-svc-chip{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;margin-bottom:16px}
.lc-svc-chip svg{width:22px;height:22px}
.lc-svc h3{font-size:19px;margin:0 0 8px}
.lc-svc h3 a{color:inherit;text-decoration:none}
.lc-svc > p{font-size:14.5px;line-height:1.6;color:var(--fg2);margin:0 0 16px}
.lc-svc ul{list-style:none;padding:0;margin:0 0 18px;display:grid;gap:9px;flex:1;align-content:start}
.lc-svc li a{display:flex;align-items:center;gap:9px;font-size:14px;font-weight:600;color:var(--ink);text-decoration:none}
.lc-svc li a:hover{color:var(--ac)}
.lc-svc li span{flex:none;width:18px;height:18px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.lc-svc li span svg{width:10px;height:10px}
.lc-svc-more{font-weight:700;font-size:14px;color:var(--ac);text-decoration:none;display:inline-flex;align-items:center;gap:6px}
.lc-svc-more svg{width:15px;height:15px}
.lc-book{position:relative;overflow:hidden;background:var(--grad-navy);padding:88px 0}
.lc-book::before{content:'';position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.75;pointer-events:none}
.lc-book .container{position:relative;z-index:1}
.lc-book-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:56px;align-items:center}
.lc-book h2{color:#fff;margin:12px 0 16px}
.lc-book p{color:var(--fg2-on-dark);font-size:16.5px;line-height:1.7;margin:0 0 22px}
.lc-book-list{list-style:none;padding:0;margin:0;display:grid;gap:10px}
.lc-book-list li{display:flex;align-items:center;gap:10px;color:#fff;font-weight:600;font-size:15px}
.lc-book-list li span{width:22px;height:22px;border-radius:50%;background:rgba(43,196,240,.18);color:var(--yb-cyan);display:flex;align-items:center;justify-content:center}
.lc-book-list svg{width:12px;height:12px}
.lc-team{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.lc-person{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:var(--r-lg);padding:24px 18px;text-align:center;backdrop-filter:blur(6px)}
.lc-person img{width:84px;height:84px;border-radius:50%;object-fit:cover;border:3px solid rgba(255,255,255,.2);margin-bottom:12px}
.lc-person strong{display:block;color:#fff;font-size:16px}
.lc-person small{display:block;color:var(--fg2-on-dark);font-size:12.5px;margin:2px 0 14px}
.lc-person .btn{width:100%;justify-content:center;padding:10px 12px;font-size:13.5px}
.lc-person a.meet{display:block;margin-top:10px;font-size:12.5px;color:var(--fg2-on-dark);font-weight:600}
.lc-faq{max-width:820px;margin:0 auto;display:grid;gap:12px}
.lc-faq details{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);box-shadow:var(--sh-sm);overflow:hidden}
.lc-faq summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:20px 24px;font-weight:700;font-size:16.5px;color:var(--ink)}
.lc-faq summary::-webkit-details-marker{display:none}
.lc-faq summary span{flex:none;width:30px;height:30px;border-radius:50%;background:var(--bg-soft);display:flex;align-items:center;justify-content:center;color:var(--yb-blue);transition:transform .2s ease}
.lc-faq summary svg{width:14px;height:14px}
.lc-faq details[open] summary span{transform:rotate(45deg);background:var(--wash-blue)}
.lc-faq details p{margin:0;padding:0 24px 22px;color:var(--fg2);font-size:15.5px;line-height:1.7}
.lc-more{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.lc-more-box{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:26px}
.lc-more-box h3{font-size:17px;margin:0 0 14px}
.lc-cta{position:relative;overflow:hidden;background:var(--grad-navy);padding:80px 0;text-align:center}
.lc-cta::before{content:'';position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.7;pointer-events:none}
.lc-cta .container{position:relative;z-index:1}
.lc-cta h2{color:#fff;margin:14px 0 14px}
.lc-cta p{color:var(--fg2-on-dark);font-size:16px;max-width:560px;margin:0 auto 28px}
.lc-cta-btns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.lc-regions{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.lc-region{position:relative;display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:28px 26px 24px;text-decoration:none;color:inherit;box-shadow:var(--sh-sm);overflow:hidden;transition:transform .25s ease,box-shadow .25s ease}
.lc-region::before{content:'';position:absolute;left:0;right:0;top:0;height:4px;background:var(--ac)}
.lc-region::after{content:'';position:absolute;right:-70px;top:-70px;width:180px;height:180px;border-radius:50%;background:var(--ac);opacity:.07;transition:transform .35s ease}
.lc-region:hover{transform:translateY(-5px);box-shadow:var(--sh-md)}
.lc-region:hover::after{transform:scale(1.25)}
.lc-region-state{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ac)}
.lc-region-state svg{width:14px;height:14px}
.lc-region h3{font-size:24px;margin:10px 0 10px}
.lc-region p{font-size:14.5px;line-height:1.6;color:var(--fg2);margin:0 0 16px}
.lc-region-cities{font-size:13px;color:var(--fg3);font-weight:600;line-height:1.6;margin:0 0 18px;flex:1}
.lc-region-go{display:inline-flex;align-items:center;gap:6px;font-weight:700;font-size:14px;color:var(--ac)}
.lc-region-go svg{width:15px;height:15px;transition:transform .2s ease}
.lc-region:hover .lc-region-go svg{transform:translateX(4px)}
.lc-dir{display:grid;grid-template-columns:repeat(4,1fr);gap:40px 32px}
.lc-dir h3{font-size:20px;margin:0 0 14px;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.lc-dir h3 small{font-size:12px;font-weight:700;color:var(--fg3);letter-spacing:.06em;text-transform:uppercase}
.lc-dir h3 > a{font:inherit;color:inherit !important;text-decoration:none}
.lc-dir h3 > a:hover{color:var(--yb-blue) !important}
.lc-dir ul{list-style:none;padding:0;margin:0;display:grid;gap:8px}
.lc-dir a{color:var(--yb-blue);font-weight:600;font-size:15px;text-decoration:none}
.lc-dir a:hover{text-decoration:underline}
.lc-dir li.lead{margin-top:6px}.lc-dir li.lead a{font-weight:800;color:var(--ink);display:inline-flex;align-items:center;gap:6px}.lc-dir li.lead svg{width:14px;height:14px}
.lc-dir-region{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--fg3);margin:0 0 22px;padding-bottom:12px;border-bottom:1px solid var(--line)}
.lc-dir-region + .lc-dir{margin-bottom:56px}
.lc-hub-hero{text-align:center;padding-bottom:130px}
.lc-hub-hero .lc-hero-lead{margin:22px auto 28px;max-width:640px;font-size:20px}
.lc-hub-hero .lc-proof{justify-content:center}
.lc-hub-regions{margin-top:-80px;position:relative;z-index:2}
@media(max-width:1080px){.lc-svcs{grid-template-columns:repeat(2,1fr)}.lc-stats{grid-template-columns:repeat(2,1fr)}}
@media(max-width:980px){.lc-ai{grid-template-columns:1fr}.lc-hero-grid,.lc-intro,.lc-why,.lc-book-grid{grid-template-columns:1fr;gap:40px}.lc-reviews,.lc-cases,.lc-regions{grid-template-columns:1fr 1fr}.lc-dir{grid-template-columns:1fr 1fr}.lc-reviews{margin-top:-60px}}
@media(max-width:680px){.lc-hero{padding:56px 0 100px}.lc-section{padding:64px 0}.lc-reviews,.lc-cases,.lc-regions,.lc-svcs,.lc-more,.lc-team,.lc-dir{grid-template-columns:1fr}.lc-stats{grid-template-columns:1fr 1fr}.lc-form-card{padding:26px 20px 20px}.lc-reviews .lc-review:nth-child(n+2){display:none}}
"""

WAVE_NAVY_TO_SOFT = '<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>'


def wave(top: str, bottom: str) -> str:
    return f'<div class="wave-div" style="background:{top}"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,40 C480,70 960,10 1440,35 L1440,70 L0,70 Z" fill="{bottom}"/></svg></div>'


REGION_ORDER = ["central-washington", "eastern-washington", "phoenix-az", "denver-co", "chicago-il", "san-francisco-bay-area"]
REGIONS.sort(key=lambda r: REGION_ORDER.index(r["slug"]))


IN_PERSON_AREAS = {
    "Yakima Valley": {
        "slugs": {"yakima-wa", "selah-wa", "union-gap-wa", "sunnyside-wa", "toppenish-wa"},
        "intro": "Our sales team lives in the Yakima Valley, so we can sit down with you at your business whenever you'd like.",
        "faq": "Yes. Our sales team lives in the Yakima Valley and is happy to meet you at your business. Day to day, most of the work happens by phone, Zoom, and email.",
    },
    "Chicago area": {
        "slugs": {"chicago-il", "naperville-il", "evanston-il", "schaumburg-il", "oak-park-il", "aurora-il", "joliet-il", "elgin-il"},
        "intro": "We have a sales rep in the Chicago area who can meet with you in person at your business.",
        "faq": "Yes. We have a sales rep in the Chicago area who is happy to meet you at your business. Day to day, most of the work happens by phone, Zoom, and email.",
    },
    "Phoenix area": {
        "slugs": {"phoenix-az", "scottsdale-az", "mesa-az", "tempe-az", "chandler-az", "gilbert-az", "glendale-az", "peoria-az"},
        "intro": "We have a sales rep in Scottsdale who can meet with you in person anywhere in the Phoenix area.",
        "faq": "Yes. We have a sales rep in Scottsdale who is happy to meet you at your business anywhere in the Phoenix area. Day to day, most of the work happens by phone, Zoom, and email.",
    },
}


def in_person_area(slug: str) -> Optional[dict]:
    return next((a for a in IN_PERSON_AREAS.values() if slug in a["slugs"]), None)


def proof_pills(slug: str = "") -> str:
    items = ["No long sales pitch", "Talk to the people doing the work"]
    if in_person_area(slug):
        items.insert(0, "Meet with us in person")
    return '<div class="lc-proof">' + "".join(f"<span>{CHECK}{escape(i)}</span>" for i in items) + "</div>"


def rating_block() -> str:
    return f"""<div class="lc-ratings">
      <a class="lc-rating" href="{GOOGLE_REVIEWS_URL}" target="_blank" rel="noopener">
        <span class="lc-rating-num">5.0</span>
        <div>
          <div class="lc-rating-stars" aria-label="5 out of 5 stars">{STAR * 5}</div>
          <div class="lc-rating-label">{GOOGLE_G} 48 Google reviews</div>
        </div>
      </a>
      <a class="lc-rating" href="{YELP_URL}" target="_blank" rel="noopener">
        <span class="lc-rating-num">5.0</span>
        <div>
          <div class="lc-rating-stars yelp-stars" aria-label="5 out of 5 stars">{YELP_STARS}</div>
          <div class="lc-rating-label"><span class="yelp-word">yelp</span> 5 star rating</div>
        </div>
      </a>
    </div>"""


def review_cards(names: list[str]) -> str:
    out = []
    for n in names:
        text = REVIEWS[n]
        if len(text) > 230:
            text = text[:text.rfind(" ", 0, 220)].rstrip(",.!") + " …"
        out.append(f"""      <article class="lc-review">
        <div class="lc-review-top"><div class="rv-stars" aria-label="5 out of 5 stars">{STAR * 5}</div><span class="g">{GOOGLE_G}</span></div>
        <p>"{escape(text, quote=False)}"</p>
        <div class="lc-review-by"><span class="lc-avatar">{initials(n)}</span>{escape(n)}</div>
      </article>""")
    return "\n".join(out)


def case_cards(keys: list[str]) -> str:
    out = []
    for k in keys:
        num, label, title, body, url, bg = CASES[k]
        out.append(f"""      <a class="lc-case" href="{url}">
        <div class="lc-case-top" style="--ac:{bg}"><strong>{num}</strong><span>{escape(label)}</span></div>
        <div class="lc-case-body"><h3>{escape(title)}</h3><p>{escape(body)}</p><span class="lc-case-more">Read the case study {ARROW}</span></div>
      </a>""")
    return "\n".join(out)


LOCAL_SERVICE_ROOTS = ("/seo", "/google-ads")


def local_service_url(url: str, slug: str) -> str:
    if url in LOCAL_SERVICE_ROOTS and (ROOT / url.lstrip("/") / f"{slug}.html").exists():
        return f"{url}/{slug}"
    return url


def service_cards(region_short: str, slug: str = "") -> str:
    out = []
    for name, url, ic, ac, wash, blurb, links in SERVICES:
        url = local_service_url(url, slug)
        links = [(t, local_service_url(u, slug)) for t, u in links]
        lis = "".join(f'<li><a href="{u}"><span style="background:{wash};color:{ac}">{CHECK}</span>{escape(t)}</a></li>' for t, u in links)
        out.append(f"""      <div class="lc-svc" style="--ac:{ac}">
        <div class="lc-svc-chip" style="background:{wash};color:{ac}">{icon(ic)}</div>
        <h3><a href="{url}">{escape(name)}</a></h3>
        <ul>{lis}</ul>
        <a class="lc-svc-more" href="{url}">Explore {escape(name)} {ARROW}</a>
      </div>""")
    return "\n".join(out)


TEAM_TITLES = {"jacob": "Account Executive", "kevin": "Owner", "sophie": "Account Executive"}


def team_cards() -> str:
    out = []
    for m in TEAM_SCHEDULE:
        out.append(f"""        <div class="lc-person">
          <img src="/assets/{m['photo']}" alt="{escape(m['name'])}" width="84" height="84" loading="lazy">
          <strong>{escape(m['name'])}</strong>
          <small>{TEAM_TITLES.get(m['slug'], '')}</small>
          <a class="btn btn-grad" href="{escape(m['calendly'])}" target="_blank" rel="noopener noreferrer">Book a Call</a>
          <a class="meet" href="/about/{m['slug']}">Meet {escape(m['short'])}</a>
        </div>""")
    return "\n".join(out)


def faqs_for(r: dict) -> list[tuple[str, str]]:
    short = r["short"]
    where = r.get("where", short)
    return [
        ("How long does it take to see results?",
         f"Ads can bring in calls within the first couple of weeks, because you're paying for placement. SEO takes longer. Most businesses see real movement in three to six months, and competitive searches in {where} can take closer to a year. A lot of our clients run both so the phone rings while SEO builds."),
        (f"Which channels make sense for {'an' if short[0] in 'AEIOU' else 'a'} {short} business?", r["channels"]),
        ("Can we meet in person?", in_person_area(r["slug"])["faq"]) if in_person_area(r["slug"]) else r["local_faq"],
        ("How do you report on results?",
         "You get a monthly report in plain English: calls, form fills, rankings, ad spend, and what each lead cost. If you'd rather talk it through, we'll walk you through it on a call."),
        ("Can you work with our in house marketing person?",
         "Yes. Some clients hand us everything. Others have someone in house and want help with SEO, ads, or the website. We'll fit around how you already work."),
        ("Do you build websites too?",
         "Yes. We design and build websites on WordPress and Wix, and we can move your current site to a new one without losing your Google rankings."),
    ]


def faq_html(items: list[tuple[str, str]]) -> str:
    return "\n".join(
        f'      <details{" open" if i == 0 else ""}><summary>{escape(q)}<span>{PLUS}</span></summary><p>{escape(a)}</p></details>'
        for i, (q, a) in enumerate(items)
    )


def faq_schema(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items],
    }


def shell(*, title: str, meta: str, path: str, crumbs: list[tuple[str, str]], body: str, extra_schema: list[dict] | None = None, form: bool = False) -> str:
    url = f"{SITE}{path}"
    header = site_header_html("/", current_path=path).strip()
    footer = site_footer_html("/", current_path=path).strip()
    crumb_items = [(i + 1, n, f"{SITE}{p}") for i, (n, p) in enumerate(crumbs)]
    schemas = global_schemas() + [breadcrumb(crumb_items), webpage_schema(title, url, meta)] + (extra_schema or [])
    form_tags = lead_form_script_tags("/") if form else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/favicon.png" type="image/png">
<title>{escape(title, quote=False)}</title>
<meta name="description" content="{escape(meta)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Yakima Branding">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(meta)}">
<link rel="stylesheet" href="/colors_and_type.css">
<style>{BASE_CSS}{PAGE_CSS}</style>
<link rel="stylesheet" href="/site.css">
{form_tags}
{render_schema_head(schemas)}
{TRACKING_HEAD_BLOCK}
</head>
<body>
{GTM_BODY_NOSCRIPT_BLOCK}
{ACCESSIBE_BODY_SCRIPT}
{header}

{body}

{footer}

<script src="/js/newsletter-popup.js" defer></script>
<script src="/js/chat-widget.js" defer></script>
<script src="/js/site.js?v=2" defer></script>
<script>
document.getElementById('hamburger')?.addEventListener('click', function () {{
  document.getElementById('mobileMenu')?.classList.toggle('open');
}});
</script>
{ATTRIBUTER_FOOTER_BLOCK}
</body>
</html>
"""


def cta_section(h2: str, p: str) -> str:
    return f"""<section class="lc-cta">
  <div class="container">
    <span class="eyebrow" style="color:var(--yb-cyan)">Let's Talk</span>
    <h2>{h2}</h2>
    <p>{p}</p>
    <div class="lc-cta-btns">
      <a href="#get-in-touch" class="btn btn-grad btn-lg">Let's Get in Touch {ARROW}</a>
      <a href="tel:5099019735" class="btn btn-ghost-white btn-lg">{PHONE}</a>
    </div>
  </div>
</section>"""


CITY_PAGE_LINKS = {(c["name"], c["state"]): f"/locations/{c['slug']}" for c in CITIES}
CITY_PAGE_LINKS.update({(r["name"], r["state"]): f"/locations/{r['slug']}" for r in REGIONS if r["name"] != r["state"]})
CITY_PAGE_LINKS.update({(n, "Washington"): "/locations/tri-cities-wa" for n in ("Kennewick", "Pasco", "Richland")})


def city_links_for(r: dict) -> dict[str, str]:
    links = {name: url for (name, state), url in CITY_PAGE_LINKS.items() if state == r["state"]}
    return {**links, **r.get("city_links", {})}


def city_chips(r: dict) -> str:
    own = f"/locations/{r['slug']}"
    links = {k: v for k, v in city_links_for(r).items() if v != own}
    return "".join(
        f'<a href="{links[c]}">{PIN}{escape(c)}</a>' if c in links else f"<span>{escape(c)}</span>"
        for c in r["cities"]
    )


def region_page(r: dict) -> str:
    name, short = r["name"], r["short"]
    where = r.get("where", short)
    path = f"/locations/{r['slug']}"
    faqs = faqs_for(r)
    review_names = ["Josh DeBoer", "Heather Hellums", "Chris Hutchens"]
    clutch = CL.for_location(short, r["state"], r["slug"]) if r["state"] == "Colorado" else []
    if clutch:
        reviews_html = f"<style>{CL.CSS}</style>\n" + "\n".join(CL.card(c) for c in clutch)
        reviews_link = "/reviews#clutch"
    else:
        reviews_html = review_cards(review_names)
        reviews_link = "/reviews"
    by_slug = {o["slug"]: o for o in REGIONS}
    if r in CITIES:
        parent = by_slug.get(r.get("region") or "")
        others = ([parent] if parent else []) + [c for c in CITIES if c is not r and c["state"] == r["state"]]
    else:
        others = [o for o in REGIONS if o is not r]
    other_links = "".join(f'<a href="/locations/{o["slug"]}">{PIN}{escape(o["name"])}</a>' for o in others)
    svc_links = "".join(f'<a href="{local_service_url(u, r["slug"])}">{escape(n)}</a>' for n, u, *_ in SERVICES)
    form = lead_form_html(f"Location - {name}", submit_label="Send Message")
    body = f"""<section class="lc-hero">
  <div class="container lc-hero-grid">
    <div>
      <span class="lc-pin">{PIN}{escape(name if r['state'] in name else f"{name}, {r['state']}")}</span>
      <h1>{r['h1']}</h1>
      <p class="lc-hero-lead">{escape(r['lead'])}</p>
      {proof_pills(r["slug"])}
      {rating_block()}
    </div>
    <div class="lc-form-card" id="get-in-touch">
      <h2>Let's get in touch</h2>
      <p>Tell us a little about your business and what you're hoping to fix. Someone from our team will reach out by the next business day.</p>
{form}
    </div>
  </div>
</section>
{WAVE_NAVY_TO_SOFT}

<section class="lc-soft" style="padding:0 0 88px">
  <div class="container">
    <div class="lc-reviews">
{reviews_html}
    </div>
    <p class="lc-reviews-link"><a href="{reviews_link}">Read more client reviews {ARROW}</a></p>

    <div class="lc-intro" style="margin-top:72px">
      <div>
        <span class="eyebrow">Digital Marketing in {escape(where)}</span>
        <h2>What it takes to win in {escape(where)}</h2>
        {''.join(f'<p>{escape(p)}</p>' for p in r['intro'] + ([in_person_area(r['slug'])['intro']] if in_person_area(r['slug']) else []))}
      </div>
      <div class="lc-panel">
        <h3>Service area</h3>
        <div class="lc-chips">{city_chips(r)}</div>
      </div>
    </div>

    <div class="lc-stats">
      <div class="lc-stat"><strong>22</strong><span>Years in business</span></div>
      <div class="lc-stat"><strong>250+</strong><span>Active clients</span></div>
      <div class="lc-stat"><strong>40+</strong><span>Industries served</span></div>
      <div class="lc-stat"><strong>5.0</strong><span>Stars across 48 Google reviews</span></div>
    </div>
  </div>
</section>
{wave('#F6F8FC', '#ffffff')}

<section class="lc-section" style="background:#fff">
  <div class="container lc-why">
    <div>
      <span class="eyebrow">Why YB Marketing</span>
      <h2>The people you meet are the people doing the work</h2>
      <p>When you work with us, you talk to the people building your website and running your campaigns. Nobody reading from a script, and no handoffs to someone you've never met.</p>
      <p>We'll also tell you what not to spend money on. If Google Ads won't pay off for your kind of business in {escape(where)}, we'll say so and point you to what will.</p>
    </div>
    <div class="lc-why-list">
      <div class="lc-why-item"><span class="lc-why-num">1</span><div><h3>We start with your numbers</h3><p>What a new customer is worth to you, and what you can afford to pay for one. Everything else follows from that.</p></div></div>
      <div class="lc-why-item"><span class="lc-why-num">2</span><div><h3>SEO, ads, and website planned together</h3><p>Your website, rankings, and ads all affect each other. We plan them as one thing instead of three separate projects.</p></div></div>
      <div class="lc-why-item"><span class="lc-why-num">3</span><div><h3>Reports you can actually read</h3><p>Calls, form fills, and cost per lead every month. No 40 page PDF full of charts nobody asked for.</p></div></div>
    </div>
  </div>
</section>
{wave('#ffffff', '#F6F8FC')}

<section class="lc-section lc-soft">
  <div class="container">
    <div class="lc-head">
      <span class="eyebrow">Case Studies</span>
      <h2>See the results for yourself</h2>
      <p>Real numbers from real clients. Click through to see exactly what we did and how long it took.</p>
    </div>
    <div class="lc-cases">
{case_cards(r['cases'])}
    </div>
  </div>
</section>
{wave('#F6F8FC', '#ffffff')}

<section class="lc-section" style="background:#fff">
  <div class="container">
    <div class="lc-head">
      <span class="eyebrow">Services</span>
      <h2>Our {escape(short)} digital marketing services</h2>
      <p>Pick one or put them together. Most clients start with one thing and add more once they see it working.</p>
    </div>
    <div class="lc-svcs">
{service_cards(short, r["slug"])}
    </div>
  </div>
</section>
{wave('#ffffff', '#F6F8FC')}

<section class="lc-section lc-soft">
  <div class="container">
    <div class="lc-head">
      <span class="eyebrow">AI Search</span>
      <h2>Show up when {escape(short)} buyers ask AI</h2>
      <p>More people now ask ChatGPT or Google's AI for a recommendation before they ever click a link. Those tools pull from websites they can understand and trust. Every SEO plan we build for {escape(where)} businesses is set up to get picked in those answers, not just ranked on Google.</p>
    </div>
    <div class="lc-ai">
      <div class="lc-ai-card"><span class="lc-ai-tag">ChatGPT</span><h3>Give it something to quote</h3><p>When someone asks ChatGPT who to hire, it looks for clear answers about what you do, where you work, and why people pick you. We write your pages so those answers are easy to find.</p></div>
      <div class="lc-ai-card"><span class="lc-ai-tag">Google AI Overviews</span><h3>Get into the summary at the top</h3><p>Google's AI summary now sits above the regular results. Structured data, solid service pages, and a well kept Google Business Profile give you a real shot at being named in it.</p></div>
      <div class="lc-ai-card"><span class="lc-ai-tag">Perplexity &amp; Gemini</span><h3>Be the source it links to</h3><p>These tools show their sources. Helpful pages and consistent business info across the web make your site the one they point people to instead of a competitor's.</p></div>
    </div>
    <p class="lc-ai-more"><a href="/blog/posts/how-to-show-up-chatgpt-ai-search">How to show up in ChatGPT and AI search {ARROW}</a></p>
  </div>
</section>
{wave('#F6F8FC', '#1B2A4A')}

<section class="lc-book" id="book">
  <div class="container lc-book-grid">
    <div>
      <span class="eyebrow" style="color:var(--yb-cyan)">Schedule a Meeting</span>
      <h2>Book 30 minutes with our team</h2>
      <p>Tell us about your business, your goals, and what hasn't worked so far. We'll tell you honestly what we'd do in your shoes. It's a conversation, not a sales pitch.</p>
      <ul class="lc-book-list">
        <li><span>{CHECK}</span>30 minutes on Zoom or by phone</li>
        <li><span>{CHECK}</span>A quick look at your site and Google presence</li>
        <li><span>{CHECK}</span>Clear next steps, whether or not you hire us</li>
      </ul>
    </div>
    <div class="lc-team">
{team_cards()}
    </div>
  </div>
</section>
{wave('#1B2A4A', '#F6F8FC')}

<section class="lc-section lc-soft">
  <div class="container">
    <div class="lc-head">
      <span class="eyebrow">FAQ</span>
      <h2>Questions about marketing in {escape(where)}</h2>
    </div>
    <div class="lc-faq">
{faq_html(faqs)}
    </div>
    <div class="lc-more" style="margin-top:56px">
      <div class="lc-more-box"><h3>Our services in {escape(where)}</h3><div class="lc-chips">{svc_links}</div></div>
      <div class="lc-more-box"><h3>{"Nearby areas we serve" if r in CITIES else "Other markets we serve"}</h3><div class="lc-chips">{other_links}<a href="/locations">{PIN}All locations</a></div></div>
    </div>
  </div>
</section>
{wave('#F6F8FC', '#1B2A4A')}

{cta_section(f"Ready to grow your {escape(short)} business?", "Tell us what you're working on and we'll tell you where we'd start. No contracts to sign just to talk.")}"""
    title = r.get("title") or f"{name} Digital Marketing Agency | SEO & Google Ads | YB Marketing"
    meta = f"Digital marketing for {name} businesses: SEO, Google Ads, web design, and AI automation. 5.0 stars on Google. Talk with YB Marketing about growing your business."
    return shell(
        title=title, meta=meta, path=path,
        crumbs=[("Home", "/"), ("About", "/about"), ("Locations We Serve", "/locations")]
        + ([(by_slug[r["region"]]["name"], f"/locations/{r['region']}")] if r.get("region") else [])
        + [(name, path)],
        body=body, extra_schema=[faq_schema(faqs)], form=True,
    )


def hub_page() -> str:
    region_cards = []
    for r in REGIONS:
        region_cards.append(f"""      <a class="lc-region" href="/locations/{r['slug']}" style="--ac:{r['accent']}">
        <span class="lc-region-state">{PIN}{escape(r['state'])}</span>
        <h3>{escape(r['name'])}</h3>
        <p class="lc-region-cities">{escape(', '.join(r['cities'][:6]))}</p>
        <span class="lc-region-go">Marketing in {escape(r.get('where', r['short']))} {ARROW}</span>
      </a>""")

    by_slug = {r["slug"]: r for r in REGIONS}

    def region_col(slug: str, title: str) -> str:
        r = by_slug[slug]
        links = city_links_for(r)
        lis = "".join(
            f'<li><a href="{links.get(c, "/locations/" + slug)}">{escape(c)}</a></li>'
            for c in r["cities"]
        )
        return (f'<div><h3><a href="/locations/{slug}">{escape(title)}</a> <small>{escape(r["state"])}</small></h3>'
                f'<ul>{lis}<li class="lead"><a href="/locations/{slug}">See {escape(r.get("where", r["short"]))} {ARROW}</a></li></ul></div>')

    def plain_col(title: str, state: str, cities: list[tuple[str, str]]) -> str:
        lis = "".join(f'<li><a href="{h}">{escape(c)}</a></li>' for c, h in cities)
        small = f' <small>{escape(state)}</small>' if state else ''
        return f'<div><h3>{escape(title)}{small}</h3><ul>{lis}</ul></div>'

    directory = f"""    <p class="lc-dir-region">Pacific Northwest</p>
    <div class="lc-dir">{region_col('central-washington', 'Central Washington')}{region_col('eastern-washington', 'Eastern Washington')}{plain_col('Western Washington', 'Washington', [("Tacoma", "/locations/tacoma-wa"), ("Vancouver", "/locations/vancouver-wa")])}{plain_col('Idaho', '', [("Boise", "/locations/boise-id"), ("Coeur d'Alene", "/locations/coeur-dalene-id")])}</div>
    <p class="lc-dir-region">West &amp; Southwest</p>
    <div class="lc-dir">{region_col('phoenix-az', 'Phoenix Area')}{region_col('denver-co', 'Denver Area')}{region_col('san-francisco-bay-area', 'Bay Area')}</div>
    <p class="lc-dir-region">Midwest</p>
    <div class="lc-dir">{region_col('chicago-il', 'Chicago Area')}</div>"""

    body = f"""<section class="lc-hero lc-hub-hero">
  <div class="container">
    <span class="lc-pin">{PIN}Locations We Serve</span>
    <h1 class="visually-hidden">Locations We Serve</h1>
    <p class="lc-hero-lead">You work with the same small team the whole way through, and you can always reach the people doing the work.</p>
    {proof_pills()}
  </div>
</section>
{WAVE_NAVY_TO_SOFT}

<section class="lc-soft" style="padding:0 0 88px">
  <div class="container">
    <div class="lc-regions lc-hub-regions">
{chr(10).join(region_cards)}
    </div>
  </div>
</section>
{wave('#F6F8FC', '#ffffff')}

<section class="lc-section" style="background:#fff">
  <div class="container">
    <div class="lc-head">
      <span class="eyebrow">Every City We Serve</span>
      <h2>Find your area</h2>
      <p>Don't see your city? We probably still work there. Most of our work happens over Zoom and phone, so distance isn't a problem.</p>
    </div>
{directory}
  </div>
</section>
{wave('#ffffff', '#F6F8FC')}

<section class="lc-section lc-soft">
  <div class="container">
    <div class="lc-head">
      <h2>Case Studies</h2>
    </div>
    <div class="lc-cases">
{case_cards(['electrical', 'refrig', 'tire'])}
    </div>
  </div>
</section>
{wave('#F6F8FC', '#1B2A4A')}

<section class="lc-cta">
  <div class="container">
    <span class="eyebrow" style="color:var(--yb-cyan)">Let's Talk</span>
    <h2>Wherever you are, let's see what's possible</h2>
    <p>Tell us about your business and we'll talk through where we'd start.</p>
    <div class="lc-cta-btns">
      <a href="/contact" class="btn btn-grad btn-lg">Schedule a Meeting {ARROW}</a>
      <a href="tel:5099019735" class="btn btn-ghost-white btn-lg">{PHONE}</a>
    </div>
  </div>
</section>"""
    return shell(
        title="Locations We Serve | YB Marketing | 509-901-9735",
        meta="YB Marketing works with businesses across Washington, Idaho, California, Colorado, Arizona, and Illinois. SEO, Google Ads, web design, and AI automation.",
        path="/locations",
        crumbs=[("Home", "/"), ("About", "/about"), ("Locations We Serve", "/locations")],
        body=body,
    )


def main() -> None:
    out_dir = ROOT / "locations"
    (out_dir / "index.html").write_text(hub_page(), encoding="utf-8")
    print("wrote locations/index.html")
    for r in REGIONS + CITIES:
        (out_dir / f"{r['slug']}.html").write_text(region_page(r), encoding="utf-8")
        print(f"wrote locations/{r['slug']}.html")


if __name__ == "__main__":
    main()
