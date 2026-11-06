#!/usr/bin/env python3
"""Build /industries (Industries We Serve hub) and one page per industry."""

from __future__ import annotations

import importlib.util
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from schema_markup import SITE  # noqa: E402
from site_lead_form_snippet import lead_form_html  # noqa: E402

_spec = importlib.util.spec_from_file_location("yb_locations", ROOT / "scripts" / "add-location-pages.py")
loc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(loc)

ARROW, CHECK, PHONE = loc.ARROW, loc.CHECK, loc.PHONE
SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><line x1="20" y1="20" x2="16.2" y2="16.2"/></svg>'
TAG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>'

loc.CASES.update({
    "roofing": ("+271%", "organic traffic over three years", "Local Roofing Contractor",
                "Form submissions up 120%, phone calls up 160%, and revenue tripled with SEO, ads, content, and social.",
                "/about/case-studies/roofing-contractor-inbound-marketing", "#C2410C"),
    "tree": ("+108%", "search visibility in one year", "Southern California Tree Services",
             "Website traffic up 75% in a year after the company had given up on running ads alone.",
             "/about/case-studies/tree-services-local-seo", "#15803D"),
    "custom": ("+108%", "search visibility in one year", "Northern California Custom Home Builder",
               "A rebuilt website and SEO grew traffic 75% in one year and brought in better fit leads.",
               "/about/case-studies/custom-home-builder-website-seo", "#9A6B1F"),
    "env": ("+93%", "search visibility in one year", "California Environmental Engineering Firm",
            "A website redesign and steady content grew traffic 57% in one year for a professional services firm.",
            "/about/case-studies/environmental-engineering-content-marketing", "#0E7490"),
})

FEATURES = {
    "refrig": ("A Local Refrigeration Services Provider Had the Technicians. Search Visibility Hadn't Caught Up.",
               [("+2,900%", "Page one keywords"), ("+100%", "Organic traffic in seven months"), ("+57%", "Top three rankings in a year")]),
    "electrical": ("A Local Electrical Contractor Had the Crews and the Reputation. Search Wasn't Sending the Calls.",
                   [("+112%", "Organic traffic year over year"), ("+204%", "Page one keywords"), ("+366%", "Peak search impressions")]),
    "roofing": ("A Local Roofing Company Was Busy in the Rainy Season. They Needed Leads All Year.",
                [("+120%", "Form submissions"), ("+160%", "Phone calls"), ("+271%", "Organic traffic over three years"), ("3x", "Revenue growth")]),
    "tree": ("A Tree Services Company Couldn't Find Its Own Website in Local Searches. That Changed Fast.",
             [("+75%", "Website traffic in one year"), ("+108%", "Search visibility in one year")]),
    "custom": ("A Custom Home Builder Had Beautiful Work. Not Enough of the Right People Were Seeing It.",
               [("+75%", "Website traffic in one year"), ("+108%", "Search visibility in one year")]),
    "env": ("An Environmental Engineering Firm Knew Its Content Mattered. It Just Never Got Written.",
            [("+57%", "Website traffic in one year"), ("+93%", "Search visibility in one year")]),
    "tire": ("A Local Tire & Auto Provider Had the Garage Covered. Google Search Was a Different Story.",
             [("+613%", "Page one keywords"), ("+46%", "Organic traffic year over year"), ("+243%", "Peak search impressions")]),
}

HOME = ["Josh DeBoer", "JLS Custom Construction", "Chris Hutchens"]

GROUPS = [
    ("home", "Home Services", "#1D6FD8"),
    ("auto", "Automotive", "#C2410C"),
    ("health", "Health & Wellness", "#0E8A6A"),
    ("pro", "Professional Services", "#6D4BD8"),
]

INDUSTRIES = [
    {
        "slug": "hvac", "group": "home", "name": "HVAC", "plural": "HVAC companies", "h1": "HVAC Companies",
        "title": "HVAC Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for heating and cooling companies. More booked calls in the busy season and steadier work when the weather is mild.",
        "why_h2": "Marketing an HVAC company is mostly about timing",
        "why": ["When the first heat wave or cold snap hits, people search, call the first two or three companies they see, and book whoever answers. If you aren't in the map results that week, you miss a lot of the year's easiest jobs.",
                "The slow months matter just as much. Maintenance plans, tune ups, and replacement quotes keep your techs busy when emergency calls drop off, and those are the searches most competitors ignore."],
        "terms": ["ac repair near me", "furnace repair", "heat pump installation", "hvac company near me", "ac not cooling", "furnace tune up"],
        "ads": "Google Ads and Local Services Ads that increase before the heat and cold hit, with call tracking on every number.",
        "web": "Pages for each service and town you cover, financing details, and a phone number that's easy to tap.",
        "faqs": [("Should HVAC companies run Google Local Services Ads?", "Usually, yes. Local Services Ads show above regular ads, you pay per lead instead of per click, and the Google Guaranteed badge helps people trust you. We run them alongside regular search ads and track which one books more jobs."),
                 ("How do you handle the slow season?", "We shift budget toward maintenance plans, tune ups, and replacement quotes, and keep SEO content working on those searches year round so you aren't starting from zero every spring."),
                 ("Can you help us get more reviews?", "Yes. We set up automatic review requests after each job and help you reply to reviews. More recent reviews is one of the biggest things that moves you up in Google Maps.")],
        "feature": "refrig", "cases": ["refrig", "electrical", "roofing"], "reviews": HOME,
        "related": [("HVAC Marketing in Phoenix", "/phx-hvac")],
        "alt": "HVAC technician checking refrigerant pressure on an outdoor air conditioning unit",
    },
    {
        "slug": "plumbing", "group": "home", "name": "Plumbing", "plural": "plumbing companies", "h1": "Plumbing Companies",
        "title": "Plumbing Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for plumbing companies. Show up first when a pipe bursts and keep the schedule full with drain, water heater, and repipe work.",
        "why_h2": "Most plumbing calls are urgent, so the first result wins",
        "why": ["Someone with water on the floor isn't comparing ten websites. They call the first plumber in the map results who looks trustworthy and answers the phone.",
                "Bigger jobs like water heaters, repipes, and sewer lines work differently. People research those for a few days, read reviews, and compare prices, so your website and reviews have to do more of the selling."],
        "terms": ["plumber near me", "emergency plumber", "water heater replacement", "drain cleaning", "leak detection", "sewer line repair"],
        "ads": "Search ads and Local Services Ads for emergency calls, scheduled around the hours you actually answer the phone.",
        "web": "Clear pages for water heaters, drains, and repipes, with pricing guidance and a fast way to call.",
        "faqs": [("Should we run ads 24 hours a day?", "Only if someone answers. We set ad schedules around the hours you can take calls, so you aren't paying for clicks that go to voicemail at 2 a.m."),
                 ("Which services should we focus on first?", "Usually the jobs with the best margins that people search for most, like water heaters and drain cleaning. We look at your numbers and your market before deciding."),
                 ("Can you help us get more reviews?", "Yes. We set up automatic review requests after each job and help you reply to reviews. Recent reviews are one of the biggest things that move you up in Google Maps.")],
        "feature": "electrical", "cases": ["electrical", "refrig", "roofing"], "reviews": HOME,
        "alt": "Plumber tightening a fitting on a residential water heater",
    },
    {
        "slug": "roofing", "group": "home", "name": "Roofing", "plural": "roofing contractors", "h1": "Roofing Contractors",
        "title": "Roofing Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for roofing contractors. More inspection requests after storms and steady leads the rest of the year.",
        "why_h2": "Roofing leads come in waves",
        "why": ["After a hail storm or a wet winter, everyone needs a roofer at once, and homeowners book the companies they can find and trust quickly. The rest of the year, replacement jobs come from people who research for weeks before they ask for a quote.",
                "Good roofing marketing handles both: ads and map rankings that catch the rush, and a website with photos, reviews, and financing details that wins the slower, bigger jobs."],
        "terms": ["roofer near me", "roof replacement cost", "roof repair", "storm damage roof inspection", "metal roofing contractor", "roof leak repair"],
        "ads": "Google Ads and Local Services Ads that ramp up after storms, aimed at the neighborhoods you want to work in.",
        "web": "Project galleries, financing details, and quote forms that work well on a phone.",
        "faqs": [("How did you help a roofing company triple its revenue?", "We combined local SEO, Google Ads, content, and social media over three years. Form submissions grew 120%, phone calls grew 160%, and organic traffic grew 271%. The case study walks through what we did."),
                 ("Do you work with storm restoration companies?", "Yes. We plan ad budgets that can increase quickly after a storm and build pages for insurance claims and inspections, so you're ready before the phone starts ringing."),
                 ("How do we get more replacement jobs instead of small repairs?", "We build pages and ads around replacement searches, show your past projects, and make financing easy to find. Those are the details homeowners look for before a big decision.")],
        "feature": "roofing", "cases": ["roofing", "custom", "electrical"], "reviews": HOME,
        "alt": "Roofers in safety harnesses installing new asphalt shingles",
    },
    {
        "slug": "electrical", "group": "home", "name": "Electrician", "plural": "electricians", "h1": "Electricians &amp; Electrical Contractors",
        "title": "Electrician Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for electricians and electrical contractors, residential and commercial.",
        "why_h2": "People hire the electrician they can find and trust",
        "why": ["Most homeowners only need an electrician a few times, so they don't have one saved in their phone. They search, check reviews, and call whoever looks licensed and local.",
                "Commercial and new construction work is different. General contractors and property managers look for proof that you can handle bigger jobs, so your website needs project photos, licensing details, and a clear list of services."],
        "terms": ["electrician near me", "panel upgrade", "ev charger installation", "generator installation", "commercial electrician", "outlet repair"],
        "ads": "Search ads for high value jobs like panel upgrades, EV chargers, and generators, not just small service calls.",
        "web": "Separate pages for residential and commercial work, licensing details, and project photos.",
        "faqs": [("What results have you gotten for an electrical contractor?", "For a Bay Area electrical contractor, organic traffic grew 112% year over year and page one keywords grew 204% in two years. The case study shows exactly what we changed."),
                 ("Can you help us get more commercial work?", "Yes. We build separate pages and campaigns for commercial and residential services, because the people searching and the words they use are different."),
                 ("Which jobs should we advertise?", "Usually the ones with the best margins that people search for, like panel upgrades, EV chargers, and generators. We look at your numbers before we spend anything.")],
        "feature": "electrical", "cases": ["electrical", "refrig", "roofing"], "reviews": HOME,
        "alt": "Electrician on a ladder installing recessed lights in a new kitchen",
    },
    {
        "slug": "pest-control", "group": "home", "name": "Pest Control", "plural": "pest control companies", "h1": "Pest Control Companies",
        "title": "Pest Control Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for pest control companies. Win the one time calls and turn more of them into recurring service plans.",
        "why_h2": "The real money is in recurring plans",
        "why": ["Most people find a pest control company when they have a problem right now: ants in the kitchen, a wasp nest, or signs of mice. They search, pick someone from the map results, and call.",
                "The companies that grow turn those one time calls into quarterly service plans. That takes a website that explains your plans clearly, follow up that happens without anyone having to remember it, and reviews that show people stay with you."],
        "terms": ["pest control near me", "exterminator", "termite inspection", "bed bug treatment", "rodent removal", "wasp nest removal"],
        "ads": "Seasonal ads for ants, wasps, and rodents, timed to when those calls actually come in.",
        "web": "Clear service plan pages, pages for each pest, and online booking.",
        "faqs": [("When should we spend more on ads?", "Most pest control searches follow the seasons. We raise budgets before your busy months and pull back when calls slow down, based on your own call data."),
                 ("How do we turn one time customers into plans?", "Automated follow up after the first visit, a clear plan offer on your website, and reminders before pests come back. We set that up and track how many customers sign on."),
                 ("Can you help with Google Local Services Ads?", "Yes. Pest control is one of the categories where Local Services Ads work well. We set them up, dispute bad leads, and compare them against regular search ads.")],
        "feature": "tree", "cases": ["tree", "roofing", "electrical"], "reviews": HOME,
        "alt": "Pest control technician inspecting a home's foundation with a flashlight",
    },
    {
        "slug": "landscaping", "group": "home", "name": "Landscaping", "plural": "landscaping companies", "h1": "Landscaping Companies",
        "title": "Landscaping Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for landscaping and lawn care companies. Fill the spring schedule and book more design and hardscape work.",
        "why_h2": "Landscaping customers buy with their eyes",
        "why": ["Weekly maintenance customers search nearby and pick someone with good reviews who can start soon. Design, hardscape, and irrigation customers are different. They want to see your past work before they ever call.",
                "That means your Google profile and website need lots of real project photos, and your ads need to start before spring, not after your competitors have already filled their calendars."],
        "terms": ["landscaping company near me", "lawn care service", "landscape design", "paver patio installation", "sprinkler repair", "retaining wall contractor"],
        "ads": "Google Ads that start before spring, with separate campaigns for maintenance and design build work.",
        "web": "Project galleries, service area pages, and a quote form that asks the right questions.",
        "faqs": [("When should landscapers start advertising?", "Before the season starts. Most homeowners plan spring projects in late winter, so we start ads and content early enough to fill your schedule before competitors do."),
                 ("How do we get more design and hardscape jobs?", "Separate pages and ads for those services, plenty of project photos, and a quote form that asks for budget and timeline so your team can follow up with the right people."),
                 ("Do you help with Google Business Profile photos?", "Yes. We help you post project photos regularly and keep your profile current, which helps you show up in Google Maps.")],
        "feature": "tree", "cases": ["tree", "custom", "roofing"], "reviews": ["Groundwork Systems", "Josh DeBoer", "Chris Hutchens"],
        "alt": "Landscaper planting shrubs in a freshly mulched garden bed",
    },
    {
        "slug": "garage-door", "group": "home", "name": "Garage Door", "plural": "garage door companies", "h1": "Garage Door Companies",
        "title": "Garage Door Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for garage door companies. Get the urgent repair calls and more of the new door installs.",
        "why_h2": "A stuck garage door is an emergency",
        "why": ["When a spring breaks or a door won't close, people search, call the first company that looks reliable, and book whoever can come today. Map rankings and fast phone answers decide who gets those jobs.",
                "New door and opener installs take more convincing. Homeowners compare styles and prices, so your website needs photos, product options, and an easy way to ask for a quote."],
        "terms": ["garage door repair near me", "broken garage door spring", "garage door opener installation", "new garage door cost", "garage door off track", "commercial garage doors"],
        "ads": "Search ads for same day repairs and new installs, with call tracking and schedules that match your dispatch hours.",
        "web": "Pages for repairs, new doors, and openers, with photos of real installs and quick quote forms.",
        "faqs": [("Garage door ads are expensive. Are they worth it?", "They can be, if the targeting is tight. We focus on the towns you serve, block searches that don't turn into jobs, and track every call so you can see what each booked job cost."),
                 ("How do we compete with franchises?", "Franchises spend a lot on ads, but local companies often win in Google Maps with more reviews and better answered calls. We focus on the things that help you stand out locally."),
                 ("Can you help us get more reviews?", "Yes. We set up automatic review requests after each job. Recent reviews are one of the biggest factors in who shows up first in Google Maps.")],
        "feature": "electrical", "cases": ["electrical", "roofing", "tire"], "reviews": HOME,
        "alt": "Garage door technician adjusting the opener track on a new carriage style door",
    },
    {
        "slug": "tree-service", "group": "home", "name": "Tree Service", "plural": "tree service companies", "h1": "Tree Service Companies",
        "title": "Tree Service Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for tree service companies and arborists. More calls for removals, trimming, and storm cleanup.",
        "why_h2": "Most tree work starts with a Google search",
        "why": ["People don't call a tree company often, so they rarely have one in mind. A storm brings a limb down or a tree starts to lean, and they search for help nearby.",
                "One of our tree service clients had stopped running ads and couldn't find their own website in local searches. A year of local SEO grew their traffic 75% and their search visibility 108%."],
        "terms": ["tree removal near me", "tree trimming", "stump grinding", "emergency tree removal", "arborist near me", "tree removal cost"],
        "ads": "Ads that ramp up after storms and in the seasons people plan trimming, aimed at the towns you work in.",
        "web": "Before and after photos, service area pages, and a quote form that lets people send photos of the job.",
        "faqs": [("What results have you gotten for a tree service company?", "For a Southern California tree service company, local SEO grew website traffic 75% and search visibility 108% in one year. The case study shows how."),
                 ("Should we run ads or focus on SEO?", "Most tree companies do best with strong local SEO and Google Maps rankings, plus ads during storm season and busy months. We'll look at your market and tell you what we'd do."),
                 ("Can you help us after a big storm?", "Yes. We can raise ad budgets quickly, update your Google profile, and make sure your phone number is easy to find when demand spikes.")],
        "feature": "tree", "cases": ["tree", "roofing", "custom"], "reviews": HOME,
        "alt": "Arborist pruning a large tree from a bucket lift",
    },
    {
        "slug": "window-installation", "group": "home", "name": "Window Company", "plural": "window installers", "h1": "Window Installers",
        "title": "Window Company Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for window and door installers. More estimate requests from homeowners ready to replace.",
        "why_h2": "Window customers research for weeks",
        "why": ["Replacing windows is a big purchase. Homeowners compare brands, read reviews, ask about energy savings, and get several quotes before they decide.",
                "The companies that win show up throughout that research: in Google Maps, in the answers to their questions, and with a website that makes it easy to book an in home estimate."],
        "terms": ["window replacement near me", "window installation cost", "energy efficient windows", "vinyl window replacement", "patio door installation", "window contractor"],
        "ads": "Search ads for replacement and installation searches, plus retargeting that keeps you in front of people while they compare.",
        "web": "Product and brand pages, financing details, project photos, and an easy estimate request form.",
        "faqs": [("How long do window customers take to decide?", "Often several weeks. That's why we pair search ads with retargeting and helpful content, so you stay in front of homeowners until they're ready to book an estimate."),
                 ("Should we write content about energy savings and brands?", "Yes. Those are the questions people ask before they call. Clear answers help you rank and help AI tools like ChatGPT recommend you."),
                 ("Do you track which leads become sales?", "Yes. We set up call and form tracking, and we can connect them to your CRM so you see which campaigns lead to signed jobs, not just calls.")],
        "feature": "custom", "cases": ["custom", "roofing", "electrical"], "reviews": HOME,
        "alt": "Two installers fitting a new black framed replacement window",
    },
    {
        "slug": "dental", "group": "health", "name": "Dental", "plural": "dental practices", "h1": "Dental Practices",
        "title": "Dental Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for dental practices. More new patients for checkups, implants, and cosmetic work.",
        "why_h2": "New patients pick a dentist on Google",
        "why": ["When people move, change insurance, or have a toothache, they search for a dentist nearby, compare star ratings, and check whether you take their insurance.",
                "Higher value work like implants, Invisalign, and cosmetic dentistry takes more research. Those patients want before and after photos, clear pricing guidance, and a reason to trust you."],
        "terms": ["dentist near me", "emergency dentist", "dental implants cost", "teeth whitening", "invisalign dentist", "dentist that takes my insurance"],
        "ads": "Search ads for high value treatments like implants and Invisalign, plus emergency dental searches.",
        "web": "Pages for each treatment, insurance and financing details, and online booking that works on a phone.",
        "faqs": [("Do you work with dental practices?", "Yes. We build websites, SEO, and ads for dental practices. One dental client told us that after two big projects with us, their business has been leaping up Google's results in organic searches."),
                 ("How do you handle patient privacy?", "We keep health information out of marketing tools and set up forms and tracking so they don't collect details they shouldn't. We work with your existing booking and practice software instead of replacing it."),
                 ("Which treatments should we advertise?", "Usually the ones with the most value and search demand in your area, like implants, Invisalign, and emergency care. We look at your capacity and goals before we recommend a budget.")],
        "feature": None, "spotlight": "Apex Dentures", "cases": ["electrical", "tire", "refrig"],
        "reviews": ["Apex Dentures", "Heather Hellums", "Kitt Murry"],
        "alt": "Dentist talking with a smiling patient in a bright dental office",
    },
    {
        "slug": "physical-therapy", "group": "health", "name": "Physical Therapy", "plural": "physical therapy clinics", "h1": "Physical Therapy Clinics",
        "title": "Physical Therapy Marketing | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for physical therapy clinics. More patients who book directly instead of waiting on a referral.",
        "why_h2": "More patients are finding PT on their own",
        "why": ["Every state now lets patients see a physical therapist without a referral in at least some cases, and more people are searching for help with back pain, sports injuries, and recovery after surgery.",
                "Those patients pick a clinic based on location, insurance, reviews, and whether they understand what you treat. A clear website and strong Google Maps presence bring them to you, and good relationships with local doctors keep referrals coming."],
        "terms": ["physical therapy near me", "sports physical therapy", "back pain physical therapist", "physical therapy after knee surgery", "dry needling", "pelvic floor therapy"],
        "ads": "Search ads for the conditions you treat most, aimed at people near each of your clinics.",
        "web": "Pages for each condition and service, insurance details, and online scheduling.",
        "faqs": [("Can you market a clinic with multiple locations?", "Yes. We set up a Google Business Profile and a local page for each location so each clinic can rank in its own neighborhood."),
                 ("Should we advertise specific conditions?", "Yes. People search for the problem they have, like back pain or a knee injury, more than for physical therapy in general. We build pages and ads around those searches."),
                 ("How do you handle patient privacy?", "We keep health details out of marketing tools and set up forms and tracking so they collect only what's needed to contact someone. Your scheduling and records stay in your own systems.")],
        "feature": None, "spotlight": "The Healthy Worker", "cases": ["electrical", "tire", "refrig"],
        "reviews": ["The Healthy Worker", "Heather Hellums", "Kitt Murry"],
        "alt": "Physical therapist guiding a patient through a knee exercise",
    },
    {
        "slug": "cpa", "group": "pro", "name": "CPA", "plural": "CPA firms", "h1": "CPA Firms &amp; Accountants",
        "title": "CPA Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for CPA firms and accountants. Attract better clients year round, not just in tax season.",
        "why_h2": "The best CPA clients are looking all year",
        "why": ["Individuals search for tax help in February and March. Business owners looking for an accountant they can keep for years search all year, often after a bad experience with their last firm.",
                "Those clients want to know what you specialize in, who you work with, and whether you'll actually return their calls. Clear service pages and helpful articles answer those questions and help you rank for them."],
        "terms": ["cpa near me", "small business accountant", "tax preparation near me", "cpa for small business", "business tax planning", "fractional cfo services"],
        "ads": "Search ads for business accounting and tax planning, with tighter budgets outside tax season.",
        "web": "Clear service and industry pages, team bios, and a simple way to book a consultation.",
        "faqs": [("How do we attract business clients instead of one time tax returns?", "We build pages and content around business services like tax planning, advisory, and bookkeeping, and aim ads at business owners rather than individual filers."),
                 ("Should we write articles?", "A few good ones, yes. Articles that answer common tax and accounting questions help you rank, show your expertise, and give AI search tools something to quote."),
                 ("Do you work with firms that only want a website?", "Yes. Some firms just need a better website. Others want SEO and ads too. We'll fit around what you need.")],
        "feature": "env", "cases": ["env", "electrical", "tire"],
        "reviews": ["Heather Underwood", "Kitt Murry", "Josh DeBoer"],
        "alt": "Accountant reviewing financial reports with a small business owner",
    },
    {
        "slug": "bookkeeping", "group": "pro", "name": "Bookkeeping", "plural": "bookkeeping firms", "h1": "Bookkeeping Firms",
        "title": "Bookkeeping Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for bookkeeping firms. Reach small business owners who are tired of doing their own books.",
        "why_h2": "Bookkeeping clients stay for years",
        "why": ["A good bookkeeping client can stay with you for years, which makes each new one worth a lot. Most of them start searching after a messy tax season or when their business grows past what they can handle.",
                "They want to know which software you use, what it costs, and whether you understand their kind of business. A website that answers those questions directly turns more visits into calls."],
        "terms": ["bookkeeper near me", "small business bookkeeping services", "quickbooks bookkeeper", "monthly bookkeeping cost", "catch up bookkeeping", "virtual bookkeeping services"],
        "ads": "Search ads aimed at business owners, including catch up bookkeeping searches before tax deadlines.",
        "web": "Pricing guidance, software pages like QuickBooks and Xero, and pages for the industries you serve.",
        "faqs": [("Can a bookkeeping firm work with clients nationwide?", "Yes, and many do. We can target your local area, specific states, or the whole country depending on how you work."),
                 ("Should we show pricing on our website?", "Usually some guidance helps. People want a rough idea before they call, and showing starting prices filters out poor fits."),
                 ("What content works best for bookkeepers?", "Plain answers to the questions owners ask, like what bookkeeping costs and when to hire help, plus pages for the software and industries you specialize in.")],
        "feature": "env", "cases": ["env", "electrical", "tire"],
        "reviews": ["Heather Underwood", "Kitt Murry", "Josh DeBoer"],
        "alt": "Bookkeeper working at a desk with bookkeeping dashboards on two monitors",
    },
    {
        "slug": "attorneys", "group": "pro", "name": "Law Firm", "plural": "law firms", "h1": "Attorneys &amp; Law Firms",
        "title": "Law Firm Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for attorneys and law firms. More consultations from people who need the kinds of cases you take.",
        "why_h2": "People hire the lawyer they find and trust first",
        "why": ["Most people have never hired an attorney before. They search for help with a specific problem, read reviews, and call the firms that seem to understand their situation.",
                "Legal searches are some of the most expensive to advertise on, so the firms that do well combine strong local SEO, clear practice area pages, and ads that only run for the cases they actually want."],
        "terms": ["lawyer near me", "personal injury attorney", "family law attorney", "estate planning lawyer", "criminal defense attorney", "dui lawyer"],
        "ads": "Search ads only for the practice areas and case types you want, with call tracking so you know your cost per case.",
        "web": "Practice area pages, attorney bios, and an easy way to request a consultation.",
        "faqs": [("Do you work with law firms?", "Yes. We work with solo attorneys and small firms. One attorney client told us we designed their website, host it, maintain the SEO, and are good at targeting the right clients for their business."),
                 ("Will our ads follow state bar rules?", "We write ads and pages with your state bar's advertising rules in mind and send everything to you for approval before it goes live. You always have the final say."),
                 ("Legal clicks are expensive. How do you keep costs down?", "Tight targeting by practice area and location, negative keywords that block searches that won't become cases, and tracking so we can move budget to what actually signs clients.")],
        "feature": None, "spotlight": "Law Office", "cases": ["env", "electrical", "tire"],
        "reviews": ["Law Office", "Emily Schwab", "Doug Turner"],
        "alt": "Attorney explaining a document to two clients in a law office",
    },
    {
        "slug": "auto-repair", "group": "auto", "name": "Auto Repair", "plural": "auto repair shops", "h1": "Auto Repair Shops",
        "title": "Auto Repair Marketing Agency | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for auto repair shops. More cars in the bays and more customers who come back.",
        "why_h2": "Drivers pick a shop from the map",
        "why": ["When a check engine light comes on, most drivers search for a shop nearby, look at star ratings, and call the one that seems honest. Showing up in the top three map results matters more than almost anything else.",
                "Keeping those customers matters just as much. Reminders for oil changes and maintenance bring people back without spending more on ads."],
        "terms": ["auto repair near me", "mechanic near me", "brake repair", "check engine light diagnostic", "oil change near me", "transmission repair"],
        "ads": "Search ads for higher ticket repairs like brakes and transmissions, aimed at drivers near your shop.",
        "web": "Service pages, online appointment requests, and your reviews front and center.",
        "faqs": [("What results have you gotten for an auto shop?", "For a regional tire and auto shop, page one keywords grew 613% over three years and organic traffic grew 46% year over year. The case study walks through it."),
                 ("How do we get more repeat customers?", "Automated maintenance reminders by text and email, review requests after each visit, and offers for the service each customer needs next."),
                 ("Can you help a shop with more than one location?", "Yes. Each location gets its own Google Business Profile and local page so it can rank in its own area.")],
        "feature": "tire", "cases": ["tire", "electrical", "refrig"],
        "reviews": ["Josh DeBoer", "Chris Hutchens", "Luis Fernandez"],
        "alt": "Mechanic running a diagnostic scan on a car in a repair shop",
    },
    {
        "slug": "auto-body", "group": "auto", "name": "Auto Body Shop", "plural": "auto body shops", "h1": "Auto Body &amp; Collision Shops",
        "title": "Auto Body Shop Marketing | SEO, Google Ads & Web Design",
        "lead": "SEO, Google Ads, and websites for auto body and collision repair shops. More estimates from drivers who get to choose their shop.",
        "why_h2": "Drivers can choose their collision shop",
        "why": ["After an accident, insurance companies often suggest a preferred shop, but most drivers can choose. The ones who look for themselves search nearby, check reviews, and look for photos of finished work.",
                "Your Google profile, reviews, and before and after photos do most of the selling. A simple way to send photos for an estimate makes it easy to pick you."],
        "terms": ["auto body shop near me", "collision repair", "car paint repair", "dent repair", "bumper repair cost", "insurance approved body shop"],
        "ads": "Search ads for collision and paint repair, aimed at drivers near your shop.",
        "web": "Before and after galleries, insurance information, and a photo estimate form.",
        "faqs": [("How do we get drivers to choose us over the insurance company's shop?", "Strong reviews, clear information about the driver's right to choose, and before and after photos. We make those easy to find on your website and Google profile."),
                 ("Should body shops run Google Ads?", "Often, yes, for collision and paint searches in your area. We track calls and estimate requests so you can see which ads bring in work."),
                 ("Can customers send photos for an estimate?", "Yes. We can add a form that lets people upload photos from their phone, which makes it easier to start the conversation.")],
        "feature": "tire", "cases": ["tire", "roofing", "electrical"],
        "reviews": ["Josh DeBoer", "Chris Hutchens", "Luis Fernandez"],
        "alt": "Auto body technician polishing a freshly painted car fender",
    },
]

SHARED_FAQS = [
    ("Do we need to be local to work with you?", loc.REMOTE_FAQ[1]),
    ("How do you report on results?",
     "You get a monthly report in plain English: calls, form fills, rankings, ad spend, and what each lead cost. If you'd rather talk it through, we'll walk you through it on a call."),
]

IND_CSS = """
.in-top-reviews{margin-top:-64px;position:relative;z-index:2;grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:calc((100% - 40px) / 3);overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding:8px 16px 30px;margin-left:-16px;margin-right:-16px;margin-bottom:-14px;scroll-padding:0 16px}
.in-top-reviews::-webkit-scrollbar{display:none}
.in-top-reviews .lc-review{scroll-snap-align:start}
.in-top-reviews .lc-review:nth-child(n){display:flex}
.in-rv-nav{display:flex;align-items:center;justify-content:center;gap:18px;margin-top:10px;font-weight:700;font-size:14.5px}
.in-rv-nav a{color:var(--yb-blue);text-decoration:none}
.in-rv-btn{width:40px;height:40px;border-radius:50%;border:1px solid var(--line);background:#fff;color:var(--fg1);display:inline-flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:var(--sh-sm)}
.in-rv-btn:hover{color:var(--yb-blue);border-color:var(--yb-blue)}
.in-top-reviews .lc-review{box-shadow:0 6px 14px rgba(15,30,60,.08)}
.in-stats3{grid-template-columns:repeat(3,1fr)}
.in-markets-box{grid-column:1/-1}
.in-cta-form{text-align:left;padding:96px 0}
.in-cta-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.in-cta-form .lc-form-card h2{color:var(--ink);margin:0 0 6px;font-size:24px}
.in-cta-form .lc-form-card > p{color:var(--fg2);max-width:none;margin:0 0 20px}
.in-cta-form .lc-form-card p.yb-lead-form-footnote{color:var(--fg3);max-width:none;margin:12px 0 0;font-size:13px}
.in-cta-copy h2{font-size:clamp(28px,3.4vw,40px)}
.in-cta-copy p{margin:0 0 22px}
.in-cta-copy .lc-book-list{margin:0 0 28px}
.in-cta-copy .lc-book-list li{color:#fff}
.in-case-wide{margin-bottom:22px}
.in-case{background:#fff;border:1px solid var(--line);border-top:4px solid var(--ac);border-radius:var(--r-lg);padding:30px 30px 26px;box-shadow:var(--sh-md);display:flex;flex-direction:column}
.in-case .eyebrow{color:var(--fg3)}
.in-case h2{font-size:clamp(1.3rem,2vw,1.6rem);line-height:1.25;margin:10px 0 12px;text-wrap:balance}
.in-case > p{color:var(--fg2);font-size:15px;line-height:1.65;margin:0 0 20px}
.in-case-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin:0 0 20px}
.in-case-stats div{background:var(--bg-soft);border-radius:14px;padding:16px}
.in-case-stats strong{display:block;font-family:var(--font-display);font-size:30px;line-height:1;color:var(--ac);margin-bottom:6px}
.in-case-stats span{font-size:13px;color:var(--fg2);line-height:1.4}
.in-case a.lc-case-more{margin-top:auto;text-decoration:none}
.in-spot-tag{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--fg3);margin-bottom:10px}
.in-why{display:grid;grid-template-columns:1.05fr .95fr;gap:56px;align-items:center}
.in-why h2{margin:12px 0 18px}
.in-why p{font-size:16.5px;line-height:1.75;color:var(--fg2);margin:0 0 16px}
.in-why img{width:100%;height:auto;border-radius:var(--r-xl,24px);box-shadow:var(--sh-md);display:block}
.in-terms-h{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--fg3);margin:26px 0 12px;font-weight:800}
.in-terms{display:flex;flex-wrap:wrap;gap:8px}
.in-terms span{display:inline-flex;align-items:center;gap:7px;padding:8px 13px;border-radius:var(--r-pill);background:#fff;border:1px solid var(--line);font-size:13.5px;font-weight:600;color:var(--ink);box-shadow:var(--sh-sm)}
.in-terms svg{width:13px;height:13px;color:var(--yb-blue)}
.in-svcs{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.in-svc{background:#fff;border:1px solid var(--line);border-top:4px solid var(--ac);border-radius:var(--r-lg);padding:26px 24px;box-shadow:var(--sh-sm);display:flex;flex-direction:column}
.in-svc .lc-svc-chip{margin-bottom:14px}
.in-svc h3{font-size:18px;margin:0 0 8px}
.in-svc p{font-size:14.5px;line-height:1.6;color:var(--fg2);margin:0 0 16px;flex:1}
.in-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;counter-reset:step}
.in-step{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:24px 22px;box-shadow:var(--sh-sm)}
.in-step b{display:flex;width:40px;height:40px;border-radius:12px;background:var(--grad-brand);color:#fff;align-items:center;justify-content:center;font-family:var(--font-display);font-size:15px;margin-bottom:14px}
.in-step b svg{width:20px;height:20px}
.in-step h3{font-size:17px;margin:0 0 8px}
.in-step p{font-size:14.5px;line-height:1.6;color:var(--fg2);margin:0}
.in-group{margin-bottom:56px}
.in-group:last-child{margin-bottom:0}
.in-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.in-card{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;text-decoration:none;color:inherit;box-shadow:var(--sh-sm);transition:transform .25s ease,box-shadow .25s ease}
.in-card:hover{transform:translateY(-5px);box-shadow:var(--sh-md)}
.in-card img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}
.in-card div{padding:20px 22px 22px;display:flex;flex-direction:column;flex:1;border-top:4px solid var(--ac)}
.in-card h3{font-size:19px;margin:0 0 8px}
.in-card p{font-size:14.5px;line-height:1.6;color:var(--fg2);margin:0 0 14px;flex:1}
.in-card span{display:inline-flex;align-items:center;gap:6px;font-weight:700;font-size:14px;color:var(--yb-blue)}
.in-card span svg{width:15px;height:15px}
@media(max-width:1080px){.in-steps{grid-template-columns:repeat(2,1fr)}}
@media(max-width:980px){.in-cta-grid{grid-template-columns:1fr;gap:36px}.in-top-reviews{grid-auto-columns:calc((100% - 20px) / 2)}.in-why{grid-template-columns:1fr;gap:28px}.in-svcs,.in-cards{grid-template-columns:1fr 1fr}}
@media(max-width:680px){.in-stats3{grid-template-columns:repeat(3,1fr);gap:10px}.in-stats3 .lc-stat{padding:18px 12px}.in-stats3 .lc-stat strong{font-size:26px}.in-stats3 .lc-stat span{font-size:12px}.in-top-reviews{margin-top:-60px;grid-auto-columns:88%}.in-svcs,.in-cards,.in-steps{grid-template-columns:1fr}}
"""

NOUN = {
    "hvac": "HVAC company", "plumbing": "plumbing company", "roofing": "roofing company", "electrical": "electrical business",
    "pest-control": "pest control company", "landscaping": "landscaping company", "garage-door": "garage door company",
    "tree-service": "tree service", "window-installation": "window company", "dental": "dental practice",
    "physical-therapy": "physical therapy clinic", "cpa": "CPA firm", "bookkeeping": "bookkeeping firm",
    "attorneys": "law firm", "auto-repair": "auto repair shop", "auto-body": "body shop",
}
BY_SLUG = {i["slug"]: i for i in INDUSTRIES}
GROUP_NAME = {k: n for k, n, _ in GROUPS}
GROUP_COLOR = {k: c for k, _, c in GROUPS}


def page(**kw) -> str:
    html = loc.shell(**kw)
    return html.replace("</style>", IND_CSS + "</style>", 1)


CHEV_L = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg>'
CHEV_R = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg>'
RV_JS = """(function(){var t=document.getElementById('in-rv');if(!t)return;
function go(d){var max=t.scrollWidth-t.clientWidth-4;if(d>0&&t.scrollLeft>=max){t.scrollTo({left:0,behavior:'smooth'});return}if(d<0&&t.scrollLeft<=4){t.scrollTo({left:t.scrollWidth,behavior:'smooth'});return}t.scrollBy({left:d*t.clientWidth,behavior:'smooth'})}
document.querySelectorAll('.in-rv-btn').forEach(function(b){b.addEventListener('click',function(){go(+b.dataset.dir);paused=true})});
var paused=false;['mouseenter','focusin','touchstart'].forEach(function(e){t.addEventListener(e,function(){paused=true},{passive:true})});
t.addEventListener('mouseleave',function(){paused=false});
if(!matchMedia('(prefers-reduced-motion: reduce)').matches)setInterval(function(){if(!paused&&!document.hidden)go(1)},7000);})();"""

FILL = ["Heather Hellums", "Kitt Murry", "Mike Nielsen", "Doug Turner", "Heather Underwood", "Luis Fernandez",
        "Josh DeBoer", "JLS Custom Construction", "Chris Hutchens"]


def top_reviews_html(i: dict) -> str:
    names = ([i["spotlight"]] if i.get("spotlight") else []) + i["reviews"]
    names = list(dict.fromkeys(names + FILL))[:6]
    cards = loc.review_cards(names)
    if i.get("spotlight"):
        cards = cards.replace('<article class="lc-review">', f'<article class="lc-review"><span class="in-spot-tag">From a {escape(NOUN[i["slug"]])} we work with</span>', 1)
    return f"""    <div class="lc-reviews in-top-reviews" id="in-rv" tabindex="0" aria-label="Client reviews">
{cards}
    </div>
    <div class="in-rv-nav">
      <button class="in-rv-btn" type="button" data-dir="-1" aria-label="Previous reviews" aria-controls="in-rv">{CHEV_L}</button>
      <a href="/reviews">Read all 48 Google reviews {ARROW}</a>
      <button class="in-rv-btn" type="button" data-dir="1" aria-label="Next reviews" aria-controls="in-rv">{CHEV_R}</button>
    </div>
    <script>{RV_JS}</script>"""


ALL_SERVICES = [
    ("SEO", "/seo"), ("Local SEO", "/seo/local-seo"), ("AI Search", "/seo/ai-search"),
    ("Technical SEO", "/seo/technical-seo"), ("Google Ads", "/google-ads"), ("Web Design", "/web-design"),
    ("Branding & Design", "/branding"), ("Social Media", "/social-media"), ("Content & Blogging", "/content-marketing"),
    ("Press Releases", "/press-releases"), ("Customer Growth Tool", "/customer-growth"),
    ("AI for Business", "/ai-for-business"), ("AI for Small Business", "/ai-for-small-business"),
]
def markets_html() -> str:
    chips = "".join(f'<a href="/locations/{r["slug"]}">{loc.PIN}{escape(r["name"])}</a>' for r in loc.REGIONS)
    return f'''      <div class="lc-more-box in-markets-box"><h3>Markets we serve</h3><div class="lc-chips">{chips}<a href="/locations">{loc.PIN}All locations</a></div></div>'''


CASE_POOL = ["roofing", "electrical", "tire", "refrig", "tree", "custom", "env"]


def more_cases(i: dict) -> list[str]:
    return [c for c in dict.fromkeys(i["cases"] + CASE_POOL) if c != i.get("feature")][:3]


def feature_html(i: dict) -> str:
    if not i.get("feature"):
        return ""
    _, _, title, body, url, color = loc.CASES[i["feature"]]
    headline, stats = FEATURES[i["feature"]]
    cells = "".join(f"<div><strong>{escape(n)}</strong><span>{escape(l)}</span></div>" for n, l in stats)
    return f"""    <div class="in-case in-case-wide" style="--ac:{color}">
      <span class="eyebrow">Case Study: {escape(title)}</span>
      <h2>{escape(headline)}</h2>
      <p>{escape(body)}</p>
      <div class="in-case-stats">{cells}</div>
      <a class="lc-case-more" href="{url}">Read the full case study {ARROW}</a>
    </div>"""


def services_html(i: dict) -> str:
    p = i["plural"]
    cards = [
        ("Local SEO &amp; Google Maps", "/seo/local-seo", "search", "var(--yb-cyan)", "var(--wash-cyan)",
         f"Rank in the map results for searches like \u201c{i['terms'][0]}\u201d and \u201c{i['terms'][2]}\u201d in every town you serve."),
        ("Google Ads", "/google-ads", "target", "var(--yb-coral)", "var(--wash-coral)", i["ads"]),
        ("Websites", "/web-design", "layout", "#159468", "var(--wash-mint)", i["web"]),
        ("Branding &amp; Design", "/branding", "layout", "#c77f12", "var(--wash-amber, #FFF4E0)",
         "A logo and look that stays consistent everywhere customers see you, from your website to your signs and business cards."),
        ("Social Media", "/social-media", "target", "#C2410C", "var(--wash-coral)",
         "Facebook, Instagram, and LinkedIn posts planned every month, so people checking you out see a business that's active and easy to trust."),
        ("Content &amp; Blogging", "/content-marketing", "search", "#0E8A6A", "var(--wash-mint)",
         "Articles that answer the questions your customers ask before they call, written to rank and to help them choose you."),
        ("AI Search", "/seo/ai-search", "spark", "var(--yb-violet)", "var(--wash-violet)",
         f"More people ask ChatGPT and Google's AI who to hire. We set up your site so those tools can find and recommend {p} like yours."),
        ("Customer Growth Tool", "/customer-growth", "spark", "var(--yb-blue)", "var(--wash-blue)",
         "Every lead, text, and email in one place, with automatic follow up so nobody slips through the cracks."),
        ("AI for Your Business", "/ai-for-small-business", "spark", "#6D4BD8", "var(--wash-violet)",
         "AI for content, follow up, chat, and voice tools that save your team time and catch more leads."),
    ]
    return "\n".join(f"""      <div class="in-svc" style="--ac:{ac}">
        <div class="lc-svc-chip" style="background:{wash};color:{ac}">{loc.icon(ic)}</div>
        <h3>{name}</h3>
        <p>{escape(text)}</p>
        <a class="lc-svc-more" href="{url}">Learn more <span class="visually-hidden">about {name}</span>{ARROW}</a>
      </div>""" for name, url, ic, ac, wash, text in cards)


STEPS = [
    ("Know who you're working with", "The team you meet on the first call is the team on your account. When you call or email, you reach the person doing the work, not someone passing notes along."),
    ("Work on your schedule", "Phone, Zoom, or email, whichever is easier for you. We're a remote team, so we keep the same hours you do wherever you're located."),
    ("One team for all of it", "Your website, branding, SEO, ads, and social media are handled by one team, so you aren't managing three vendors who never talk."),
    ("Straight answers", "We tell you plainly what's working and what isn't, and what we'd change. No 40 page reports full of numbers that don't matter."),
]


def industry_page(i: dict) -> str:
    slug, plural = i["slug"], i["plural"]
    path = f"/industries/{slug}"
    faqs = i["faqs"] + SHARED_FAQS
    others = [o for o in INDUSTRIES if o is not i]
    same = [o for o in others if o["group"] == i["group"]] + [o for o in others if o["group"] != i["group"]]
    other_links = "".join(f'<a href="/industries/{o["slug"]}">{escape(o["h1"].replace("&amp;", "&"))}</a>' for o in same)
    svc_links = "".join(f'<a href="{u}">{escape(n)}</a>' for n, u in ALL_SERVICES)
    svc_links += "".join(f'<a href="{u}">{escape(n)}</a>' for n, u in i.get("related", []))
    terms = "".join(f"<span>{SEARCH}{escape(t)}</span>" for t in i["terms"])
    steps = "".join(f'<div class="in-step"><b>{CHECK}</b><h3>{escape(h)}</h3><p>{escape(p)}</p></div>' for h, p in STEPS)
    form = lead_form_html(f"Industry - {i['name']}", submit_label="Send Message")
    form2 = lead_form_html(f"Industry - {i['name']} - Bottom", submit_label="Send Message")
    body = f"""<section class="lc-hero">
  <div class="container lc-hero-grid">
    <div>
      <span class="lc-pin">{TAG}{escape(GROUP_NAME[i['group']])}</span>
      <h1>Digital Marketing for <span>{i['h1']}</span></h1>
      <p class="lc-hero-lead">{escape(i['lead'])}</p>
      {loc.proof_pills()}
      {loc.rating_block()}
    </div>
    <div class="lc-form-card" id="get-in-touch">
      <h2>Let's get in touch</h2>
      <p>Tell us a little about your business and what you're hoping to fix. Someone from our team will reach out by the next business day.</p>
{form}
    </div>
  </div>
</section>
{loc.WAVE_NAVY_TO_SOFT}

<section class="lc-soft" style="padding:0 0 88px">
  <div class="container">
{top_reviews_html(i)}
    <div class="lc-stats in-stats3">
      <div class="lc-stat"><strong>22</strong><span>Years in business</span></div>
      <div class="lc-stat"><strong>250+</strong><span>Active clients</span></div>
      <div class="lc-stat"><strong>40+</strong><span>Industries served</span></div>
    </div>
  </div>
</section>
{loc.wave('#F6F8FC', '#ffffff')}

<section class="lc-section" style="background:#fff">
  <div class="container in-why">
    <div>
      <span class="eyebrow">Why It's Different</span>
      <h2>{escape(i['why_h2'])}</h2>
      <p>{escape(i['why'][0])}</p>
      <p>{escape(i['why'][1])}</p>
      <p class="in-terms-h">What your customers type into Google</p>
      <div class="in-terms">{terms}</div>
    </div>
    <img src="/assets/industries/{slug}.webp" srcset="/assets/industries/{slug}-600.webp 600w, /assets/industries/{slug}.webp 960w" sizes="(max-width: 980px) 100vw, 540px" width="960" height="720" alt="{escape(i['alt'])}" loading="lazy">
  </div>
</section>
{loc.wave('#ffffff', '#F6F8FC')}

<section class="lc-section lc-soft">
  <div class="container">
    <div class="lc-head">
      <span class="eyebrow">What We Do</span>
      <h2>Digital marketing built for {escape(plural)}</h2>
      <p>Everything a growing business needs to get found, look the part, and keep leads from slipping away. Start with one thing or put it all together.</p>
    </div>
    <div class="in-svcs">
{services_html(i)}
    </div>
  </div>
</section>
{loc.wave('#F6F8FC', '#ffffff')}

<section class="lc-section" style="background:#fff">
  <div class="container">
    <div class="lc-head">
      <span class="eyebrow">Results</span>
      <h2>Results for businesses like yours</h2>
      <p>Real numbers from real clients. Click through to see exactly what we did and how long it took.</p>
    </div>
{feature_html(i)}
    <div class="lc-cases">
{loc.case_cards(more_cases(i))}
    </div>
  </div>
</section>
{loc.wave('#ffffff', '#F6F8FC')}

<section class="lc-section lc-soft">
  <div class="container">
    <div class="lc-head">
      <span class="eyebrow">Why YB Marketing</span>
      <h2>What you get working with us</h2>
      <p>A small, fully remote team that knows your business and picks up the phone.</p>
    </div>
    <div class="in-steps">{steps}</div>
  </div>
</section>
{loc.wave('#F6F8FC', '#1B2A4A')}

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
{loc.team_cards()}
    </div>
  </div>
</section>
{loc.wave('#1B2A4A', '#F6F8FC')}

<section class="lc-section lc-soft">
  <div class="container">
    <div class="lc-head">
      <span class="eyebrow">FAQ</span>
      <h2>Questions about marketing for {escape(plural)}</h2>
    </div>
    <div class="lc-faq">
{loc.faq_html(faqs)}
    </div>
    <div class="lc-more" style="margin-top:56px">
      <div class="lc-more-box"><h3>Our services</h3><div class="lc-chips">{svc_links}</div></div>
      <div class="lc-more-box"><h3>Other industries we serve</h3><div class="lc-chips">{other_links}<a href="/industries">All industries</a></div></div>
{markets_html()}
    </div>
  </div>
</section>
{loc.wave('#F6F8FC', '#1B2A4A')}

<section class="lc-cta in-cta-form">
  <div class="container in-cta-grid">
    <div class="in-cta-copy">
      <span class="eyebrow" style="color:var(--yb-cyan)">Let's Talk</span>
      <h2>Ready to grow your {escape(NOUN[slug])}?</h2>
      <p>Tell us what you're working on and we'll tell you where we'd start. No contracts to sign just to talk.</p>
      <ul class="lc-book-list">
        <li><span>{CHECK}</span>A real person replies by the next business day</li>
        <li><span>{CHECK}</span>A quick look at your website and Google presence</li>
        <li><span>{CHECK}</span>Straight answers on what we'd do first</li>
      </ul>
      <a href="tel:5099019735" class="btn btn-ghost-white btn-lg">{PHONE}</a>
    </div>
    <div class="lc-form-card">
      <h2>Send us a message</h2>
      <p>Share a few details and we'll reach out to set up a time to talk.</p>
{form2}
    </div>
  </div>
</section>"""
    meta = f"Digital marketing for {plural}: SEO, Google Ads, websites, and AI search. Real case studies, 5.0 stars on Google. Talk with YB Marketing about growing your business."
    service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"{SITE}{path}#service",
        "name": f"Digital Marketing for {i['h1'].replace('&amp;', '&')}",
        "serviceType": "Digital marketing",
        "description": i["lead"],
        "url": f"{SITE}{path}",
        "provider": {"@id": f"{SITE}/#organization"},
        "areaServed": {"@type": "Country", "name": "United States"},
        "audience": {"@type": "BusinessAudience", "audienceType": plural[0].upper() + plural[1:]},
        "image": f"{SITE}/assets/industries/{slug}.webp",
    }
    return page(
        title=i["title"], meta=meta, path=path,
        crumbs=[("Home", "/"), ("About", "/about"), ("Industries We Serve", "/industries"), (i["h1"].replace("&amp;", "&"), path)],
        body=body, extra_schema=[loc.faq_schema(faqs), service], form=True,
    )


def hub_page() -> str:
    groups = []
    for key, name, color in GROUPS:
        cards = "\n".join(f"""      <a class="in-card" href="/industries/{i['slug']}" style="--ac:{color}">
        <img src="/assets/industries/{i['slug']}-600.webp" width="600" height="450" alt="{escape(i['alt'])}" loading="lazy">
        <div><h3>{i['h1']}</h3><p>{escape(i['lead'].split('. ')[1] if '. ' in i['lead'] else i['lead'])}</p><span>Marketing for {escape(i['plural'])} {ARROW}</span></div>
      </a>""" for i in INDUSTRIES if i["group"] == key)
        groups.append(f"""    <div class="in-group">
      <p class="lc-dir-region">{escape(name)}</p>
      <div class="in-cards">
{cards}
      </div>
    </div>""")
    body = f"""<section class="lc-hero lc-hub-hero">
  <div class="container">
    <span class="lc-pin">{TAG}Industries We Serve</span>
    <h1 class="visually-hidden">Industries We Serve</h1>
    <p class="lc-hero-lead">SEO, Google Ads, and websites planned around how customers in your industry actually search and buy.</p>
    {loc.proof_pills()}
  </div>
</section>
{loc.WAVE_NAVY_TO_SOFT}

<section class="lc-soft" style="padding:0 0 88px">
  <div class="container">
    <div class="lc-reviews">
{loc.review_cards(["JLS Custom Construction", "Apex Dentures", "Law Office"])}
    </div>
    <p class="lc-reviews-link"><a href="/reviews">Read more client reviews {ARROW}</a></p>
  </div>
</section>
{loc.wave('#F6F8FC', '#ffffff')}

<section class="lc-section" style="background:#fff">
  <div class="container">
    <div class="lc-head">
      <span class="eyebrow">Find Your Industry</span>
      <h2>Marketing for the work you do</h2>
      <p>Don't see your industry? We work with more than 40 kinds of businesses. Tell us about yours and we'll tell you where we'd start.</p>
    </div>
{chr(10).join(groups)}
  </div>
</section>
{loc.wave('#ffffff', '#F6F8FC')}

<section class="lc-section lc-soft">
  <div class="container">
    <div class="lc-head">
      <h2>Case Studies</h2>
    </div>
    <div class="lc-cases">
{loc.case_cards(['roofing', 'electrical', 'tire'])}
    </div>
  </div>
</section>
{loc.wave('#F6F8FC', '#1B2A4A')}

<section class="lc-cta">
  <div class="container">
    <span class="eyebrow" style="color:var(--yb-cyan)">Let's Talk</span>
    <h2>Whatever you do, let's see what's possible</h2>
    <p>Tell us about your business and we'll talk through where we'd start.</p>
    <div class="lc-cta-btns">
      <a href="/contact" class="btn btn-grad btn-lg">Schedule a Meeting {ARROW}</a>
      <a href="tel:5099019735" class="btn btn-ghost-white btn-lg">{PHONE}</a>
    </div>
  </div>
</section>"""
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Industries We Serve",
        "itemListElement": [
            {"@type": "ListItem", "position": n, "name": i["h1"].replace("&amp;", "&"), "url": f"{SITE}/industries/{i['slug']}"}
            for n, i in enumerate(INDUSTRIES, 1)
        ],
    }
    return page(
        title="Industries We Serve | YB Marketing | 509-901-9735",
        meta="YB Marketing does SEO, Google Ads, and web design for HVAC, plumbing, roofing, electrical, dental, legal, accounting, auto repair, and other industries nationwide.",
        path="/industries",
        crumbs=[("Home", "/"), ("About", "/about"), ("Industries We Serve", "/industries")],
        body=body, extra_schema=[item_list],
    )


def main() -> None:
    out = ROOT / "industries"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(hub_page(), encoding="utf-8")
    print("wrote industries/index.html")
    for i in INDUSTRIES:
        (out / f"{i['slug']}.html").write_text(industry_page(i), encoding="utf-8")
        print(f"wrote industries/{i['slug']}.html")


if __name__ == "__main__":
    main()
