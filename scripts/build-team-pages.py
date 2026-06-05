#!/usr/bin/env python3
"""Generate team profile pages in about/ from yakimabranding.com content."""

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ABOUT_DIR = ROOT / "about"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_nav_snippet import site_header_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_staging_seo_snippet import STAGING_ROBOTS_META
from site_footer_snippet import site_footer_html

PREFIX = "../"
CALENDLY_URL = "https://calendly.com/yakimabranding"
ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
CAL_ICON = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">'
    '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/>'
    '<line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
)
SEND_ICON = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">'
    '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>'
)


def header_html():
    return site_header_html(PREFIX, about_active="about")


def footer_html():
    return site_footer_html(PREFIX)


def shell(title, desc, theme, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{STAGING_ROBOTS_META}
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="{PREFIX}colors_and_type.css">
<link rel="stylesheet" href="{PREFIX}site.css">
<link rel="stylesheet" href="{PREFIX}team-profile.css">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--font-body);background:var(--bg);color:var(--fg1);-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
.container{{width:100%;max-width:var(--container);margin:0 auto;padding:0 28px}}
.btn{{display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer;font-family:var(--font-body);font-weight:700;font-size:15px;border-radius:var(--r-md);padding:13px 22px}}
.btn-grad{{background:var(--grad-brand);color:#fff;box-shadow:var(--sh-blue)}}
.logo img{{width:44px;height:44px}}
</style>
</head>
<body class="team-profile-page team-{theme}">
{ACCESSIBE_BODY_SCRIPT}
{header_html()}
{body}
{footer_html()}
<script src="{PREFIX}js/newsletter-popup.js" defer></script>
<script src="{PREFIX}js/site.js" defer></script>
<script>
document.getElementById('hamburger')?.addEventListener('click', function () {{
  document.getElementById('mobileMenu')?.classList.toggle('open');
}});
document.querySelectorAll('.team-faq-q').forEach(function (btn) {{
  btn.addEventListener('click', function () {{
    btn.closest('.team-faq-item').classList.toggle('open');
  }});
}});
</script>
</body>
</html>"""


def hero_actions(contacts):
    """Build primary + secondary CTAs from contact tuples (label, href, icon)."""
    primary = None
    email = None
    phone = None
    for label, href, _icon in contacts:
        if "calendly" in href and primary is None:
            primary = (label, href)
        elif href.startswith("mailto:") and email is None:
            email = (label, href)
        elif href.startswith("tel:") and phone is None:
            phone = (label, href)
    if primary is None:
        primary = ("Get in Touch", f"{PREFIX}contact.html")
    ext = ' target="_blank" rel="noopener"' if primary[1].startswith("http") else ""
    parts = [
        f'<a href="{html.escape(primary[1])}" class="btn btn-hero-primary"{ext}>{html.escape(primary[0])}</a>'
    ]
    if email:
        parts.append(
            f'<a href="{html.escape(email[1])}" class="btn btn-hero-ghost">Email</a>'
        )
    if phone:
        parts.append(
            f'<a href="{html.escape(phone[1])}" class="btn btn-hero-ghost">Call {html.escape(phone[0])}</a>'
        )
    return "\n        ".join(parts)


PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
MAIL_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'


def hero_block(name, role, lead, photo, contacts):
    return f"""
<section class="team-hero">
  <div class="team-hero-mesh"></div>
  <div class="hero-logo-overlay hero-logo-overlay--right" aria-hidden="true">
    <img src="{PREFIX}assets/yb-logo-white.png" alt="">
  </div>
  <div class="container team-hero-grid">
    <div class="team-hero-photo"><img src="{PREFIX}{photo}" alt="{html.escape(name)}"></div>
    <div>
      <nav class="team-breadcrumb" aria-label="Breadcrumb">
        <a href="{PREFIX}about.html">About</a><span>/</span><a href="{PREFIX}about.html#team">Team</a><span>/</span><span>{html.escape(name)}</span>
      </nav>
      <p class="team-hero-eyebrow">Your YB Marketing contact</p>
      <h1>{html.escape(name)}</h1>
      <p class="team-hero-role">{html.escape(role)}</p>
      <p class="team-hero-lead">{lead}</p>
      <div class="team-hero-actions">
        {hero_actions(contacts)}
      </div>
      <div class="team-back-row">
        <a href="{PREFIX}about.html#team" class="team-back-link" style="color:rgba(255,255,255,.88)">← Back to full team</a>
      </div>
    </div>
  </div>
</section>"""


def team_calendly_card_html(member_name: str) -> str:
    name = html.escape(member_name)
    return f"""
    <div class="team-aside-card team-aside-calendly">
      <div class="team-calendly-intro">
        <div class="team-calendly-avatar">YB</div>
        <div class="team-calendly-meta">YB Marketing · {name}</div>
        <div class="team-calendly-title">Introduction Meeting</div>
        <div class="team-calendly-duration"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 30 min</div>
        <p class="team-calendly-desc">Book time to discuss your business and how YB Marketing can help you grow.</p>
      </div>
      <a href="{CALENDLY_URL}" class="btn btn-grad team-calendly-btn" target="_blank" rel="noopener">Book a Meeting {CAL_ICON}</a>
      <p class="team-calendly-note">Replace with your Calendly inline embed when ready.</p>
    </div>"""


def team_contact_form_html() -> str:
    return f"""
    <div class="team-aside-card team-aside-form">
      <h3>Send a message</h3>
      <p class="team-form-lead">Fill out the form and we&rsquo;ll be in touch as soon as possible.</p>
      <form class="team-form yb-contact-form" action="#" method="post">
        <div class="team-form-row">
          <div class="team-form-field">
            <label for="team-name">Name *</label>
            <input id="team-name" type="text" name="name" placeholder="What's your name?" autocomplete="name">
          </div>
          <div class="team-form-field">
            <label for="team-email">Email *</label>
            <input id="team-email" type="email" name="email" placeholder="What's your email?" autocomplete="email">
          </div>
        </div>
        <div class="team-form-row">
          <div class="team-form-field">
            <label for="team-company">Company or URL *</label>
            <input id="team-company" type="text" name="company" placeholder="What's your company?">
          </div>
          <div class="team-form-field">
            <label for="team-phone">Cell # *</label>
            <input id="team-phone" type="tel" name="phone" placeholder="What's your cell #?" autocomplete="tel">
          </div>
        </div>
        <div class="team-form-field">
          <label for="team-message">Message</label>
          <textarea id="team-message" name="message" placeholder="What can we help you with?" rows="4"></textarea>
        </div>
        <div class="team-form-captcha" aria-hidden="true">
          <div class="team-form-captcha-check"><span class="team-form-captcha-box"></span> I&rsquo;m not a robot</div>
          <div class="team-form-captcha-brand">reCAPTCHA<br><span>Privacy · Terms</span></div>
        </div>
        <button type="submit" class="btn btn-grad team-form-submit">Send Message {SEND_ICON}</button>
      </form>
    </div>"""


def team_contact_aside_html(member_name: str, extra_cards: str = "") -> str:
    return f"""<aside class="team-aside-stack">
{extra_cards}{team_calendly_card_html(member_name)}{team_contact_form_html()}
</aside>"""


def team_contact_section_html(member_name: str) -> str:
    return f"""
<section class="team-contact-section" id="contact">
  <div class="container">
    <div class="team-contact-intro">
      <span class="eyebrow">Get Started</span>
      <h2>Book a meeting or send a message</h2>
      <p>Schedule a free 30-minute introduction with {html.escape(member_name)} or use the form below.</p>
    </div>
    <div class="team-contact-grid">
      {team_calendly_card_html(member_name)}
      {team_contact_form_html()}
    </div>
  </div>
</section>"""


def cta_strip():
    return f"""
<section class="team-cta-strip">
  <div class="container">
    <span class="eyebrow" style="color:var(--yb-blue)">How Can We Help?</span>
    <h2>Let's discuss your next project</h2>
    <p>Contact us to talk through your goals and how YB Marketing can help you grow.</p>
    <a href="{PREFIX}contact.html" class="btn btn-grad">Contact Us {ARROW}</a>
  </div>
</section>"""


PAGES = []


def page_kevin():
    body = hero_block(
        "Kevin Dean",
        "Owner",
        "Certified advertising professional and SEO expert leading YB Marketing with a focus on superior service, clear communication, and measurable ROI.",
        "assets/kevin-headshot.webp",
        [
            ("kevin@yakimabranding.com", "mailto:kevin@yakimabranding.com", MAIL_SVG),
            ("510-687-9737", "tel:5106879737", PHONE_SVG),
            ("509-901-9735 x1001", "tel:5099019735", PHONE_SVG),
        ],
    )
    body += f"""
<section class="team-body" style="background:#fff">
  <div class="container team-layout-split">
    <div class="team-prose">
      <p>Our driving goal at YB Marketing is to provide superior customer service by developing the best solutions for clients, and communicating clearly and effectively. I specialize in helping businesses grow through better utilization of the Internet to generate leads and increase visibility.</p>
      <p>As a Certified Advertising Professional and trained Search Engine Optimization expert, I work with our talented team to find opportunities for increasing online branding, lead generation opportunities, and overall return on investment through better web strategies.</p>
      <p>I started our Internet Marketing business in 2003 after 20 years in high-tech management and operations. I bring a unique blend of business background including an MBA, senior management experience, and advanced marketing skills to businesses of all sizes.</p>
      <p>We recently moved to North Scottsdale, AZ. We are excited to bring our high quality marketing and branding services to Arizona and the Southwest. We look forward to working with you!</p>
      <h2>Some FAQs</h2>
      <div class="team-faq">
        <div class="team-faq-item">
          <button class="team-faq-q" type="button">Why did you go into Internet Marketing?<svg class="team-faq-chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg></button>
          <div class="team-faq-a">In 2003, the Internet was still young. We were moving past dial-up, Google was just getting started, and laptops didn't really exist. But the future was obvious — the Internet was the place to be. I wanted to start my own company to help clients grow by using this new technology.</div>
        </div>
        <div class="team-faq-item">
          <button class="team-faq-q" type="button">What is your management philosophy?<svg class="team-faq-chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg></button>
          <div class="team-faq-a">We do all we can to help the customer. We educate our customers as to what we think are the best steps and methods to help them achieve their goals. We do not chase the latest technologies — we may be slower to latch onto the next trend so we understand how something works best.</div>
        </div>
        <div class="team-faq-item">
          <button class="team-faq-q" type="button">What motivates you?<svg class="team-faq-chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg></button>
          <div class="team-faq-a">I enjoy talking to customers who put their faith in us to help them grow. The Internet can be a scary place for some business owners — but our systems and tools are time-tested. We follow up, we communicate, and we admit when we need to fix something.</div>
        </div>
        <div class="team-faq-item">
          <button class="team-faq-q" type="button">What Internet Marketing technique is best for my business?<svg class="team-faq-chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg></button>
          <div class="team-faq-a">That depends on your industry, demographic, ideal customer, and brand voice. It can be a mix of several platforms. Each platform delivers to a specific group — reach out so we can determine which will deliver you the best results.</div>
        </div>
        <div class="team-faq-item">
          <button class="team-faq-q" type="button">Are you more expensive than other agencies?<svg class="team-faq-chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg></button>
          <div class="team-faq-a">We are different in that we do not try to be the cheapest agency. We trust our systems and services and can show using real data that they work. It is not about what you are paying — it is about what we can make for you. Low pricing is forgotten once you get the deal; low performance is felt for a long time.</div>
        </div>
      </div>
    </div>
    {team_contact_aside_html("Kevin Dean")}
  </div>
</section>"""
    body += cta_strip()
    return "kevin", "Kevin Dean — Owner | YB Marketing", "Meet Kevin Dean, owner of YB Marketing. Digital marketing, SEO, and advertising strategy for growing businesses.", body


def page_jacob():
    body = hero_block(
        "Jacob Ross",
        "Account Executive",
        "Digital marketing expert and self-proclaimed grill master — building memorable brands with data-driven campaigns.",
        "assets/jacob-headshot.webp",
        [
            ("jacob@yakimabranding.com", "mailto:jacob@yakimabranding.com", MAIL_SVG),
            ("509-203-1007", "tel:5092031007", PHONE_SVG),
            ("Book a 30-Min Call", "https://calendly.com/yakimabranding", PHONE_SVG),
        ],
    )
    quotes = [
        ("Great company to work with. I've completed two big projects and the business has been leaping up the Google results page with organic searches.", "Apex Dentures"),
        ("Worked with Jacob and his team and had a great experience building a new website! They were professional and easy to work with.", "The Healthy Worker"),
        ("Had a great experience working with Jacob. As a company we are just beginning our branding efforts and he and his team guided us through developing a logo and initial branding efforts.", "Groundwork Systems"),
        ("Yakima Branding was instrumental in the successful launch of my business and brand.", "JLS Custom Construction"),
    ]
    qhtml = "".join(
        f'<blockquote class="team-quote"><p>"{html.escape(q)}"</p><cite>— {html.escape(c)}</cite></blockquote>'
        for q, c in quotes
    )
    body += f"""
<section class="team-body" style="background:var(--bg-soft)">
  <div class="container team-layout-split">
    <div class="team-prose">
      <p><strong>Digital Marketing Expert. Self Proclaimed Grill Master.</strong></p>
      <p>Jacob believes good is never enough when greatness is within reach. With more than four years of digital marketing sales experience, he brings the best ingredients to every project so each client's brand stands out and stays memorable.</p>
      <p>He takes pride in working closely with businesses to uncover what makes them unique, identify their ideal audience, and design campaigns that place their brand directly in front of the people who matter most.</p>
      <p>Recognizing that no two businesses are alike, Jacob creates custom strategies tailored to each client's goals and market. His mission is simple: combine proven expertise with fresh creativity so every brand he touches is truly unforgettable.</p>
      <h2>Interested in?</h2>
      <div class="team-interest-row">
        <span class="team-interest">Website</span>
        <span class="team-interest">SEO</span>
        <span class="team-interest">Google Ads</span>
        <span class="team-interest">Social Media</span>
      </div>
      <h2>Verticals we work with</h2>
      <div class="team-chips">
        <span class="team-chip">Landscaping</span>
        <span class="team-chip">Construction</span>
        <span class="team-chip">Manufacturing</span>
        <span class="team-chip">Legal</span>
        <span class="team-chip">Real Estate</span>
        <span class="team-chip">Small Businesses</span>
      </div>
      <h2>How we work together</h2>
      <div class="team-steps">
        <div class="team-step"><div class="team-step-num">1</div><h3>Personalized Audit</h3><p>It all starts with a free audit of your website and marketing channels.</p></div>
        <div class="team-step"><div class="team-step-num">2</div><h3>Customized Strategy</h3><p>Together, we'll build a strategy that prioritizes your business goals.</p></div>
        <div class="team-step"><div class="team-step-num">3</div><h3>Grow Your Business</h3><p>With our goals aligned and strategy in place, we take action to grow your business.</p></div>
      </div>
      <h2>Testimonials</h2>
      <div class="team-quote-grid">{qhtml}</div>
    </div>
    {team_contact_aside_html("Jacob Ross")}
  </div>
</section>"""
    body += cta_strip()
    return "jacob", "Jacob Ross — Account Executive | YB Marketing", "Meet Jacob Ross, account executive at YB Marketing. Custom digital marketing, SEO, Google Ads, and web strategy.", body


def page_kristin():
    body = hero_block(
        "Kristin Sparling",
        "Account Executive",
        "Strategy-first account executive helping Pacific Northwest businesses grow with tailored digital marketing plans.",
        "assets/kristin-headshot.webp",
        [
            ("Book a Meeting", "https://calendly.com/yakimabranding", PHONE_SVG),
            ("kristin@yakimabranding.com", "mailto:kristin@yakimabranding.com", MAIL_SVG),
            ("509-940-1799", "tel:5099401799", PHONE_SVG),
        ],
    )
    locs = ["Yakima", "Ellensburg", "Wenatchee", "Chelan", "Leavenworth", "Cashmere"]
    chips = "".join(f'<span class="team-chip">{html.escape(l)}</span>' for l in locs)
    body += f"""
<section class="team-body" style="background:#fff">
  <div class="container team-layout-split">
    <div class="team-prose">
      <p>Kristin comes from a family deeply rooted in coaching and leadership. This foundation of teamwork, leadership, and mentorship carries over into every aspect of her professional endeavors.</p>
      <p>With over three years of experience in digital marketing, Kristin brings strategic insight and hands-on expertise to YB Marketing. She is committed to understanding each client's story, identifying their goals, and developing tailored marketing plans that drive measurable growth.</p>
      <p>Internet Marketing does not mean using the same solutions for every business. YB Marketing works with you to build a custom strategy to drive relevant visitors and conversions based on your business, goals, and budget.</p>
      <h2>Where I spend my time</h2>
      <div class="team-chips">{chips}</div>
      <h2>Keep us in mind for</h2>
      <div class="team-chips">
        <span class="team-chip">Website Creation</span>
        <span class="team-chip">Social Media</span>
        <span class="team-chip">SEO</span>
        <span class="team-chip">Google Ads</span>
        <span class="team-chip">Graphic Design</span>
        <span class="team-chip">Logos</span>
      </div>
      <p>I look forward to connecting with you. My mission is to help your business grow and see you succeed by establishing a strong online presence in this amazing, but crazy digital landscape.</p>
      <div class="team-steps">
        <div class="team-step"><div class="team-step-num">1</div><h3>Personalized Audit</h3><p>Free audit of your website and marketing channels.</p></div>
        <div class="team-step"><div class="team-step-num">2</div><h3>Customized Strategy</h3><p>A plan built around your business goals.</p></div>
        <div class="team-step"><div class="team-step-num">3</div><h3>Grow Your Business</h3><p>Aligned goals, then action.</p></div>
      </div>
    </div>
    {team_contact_aside_html("Kristin Sparling")}
  </div>
</section>"""
    body += cta_strip()
    return "kristin", "Kristin Sparling — Account Executive | YB Marketing", "Meet Kristin Sparling at YB Marketing. Custom SEO, web, social, and Google Ads for Washington businesses.", body


def page_sophie():
    body = hero_block(
        "Sophie Mann",
        "Account Executive",
        "Strategic communications specialist with deep expertise in education and manufacturing — now serving clients from Chicago.",
        "assets/sophie-headshot.webp",
        [
            ("sophie@yakimabranding.com", "mailto:sophie@yakimabranding.com", MAIL_SVG),
            ("303-955-6979", "tel:3039556979", PHONE_SVG),
        ],
    )
    body += """
<section class="team-body" style="background:#fff">
  <div class="container">
    <div class="team-prose" style="max-width:780px;margin:0 auto">
      <p>Sophie is a proud University of Kansas graduate with a Bachelor's degree in Strategic Communications and a Business minor. Over the past seven-plus years, she's honed her skills in agency life, starting her career in Denver and collaborating with clients across a wide range of industries.</p>
      <div class="team-pull-quote"><p>She thrives on building lasting partnerships and turning big ideas into smart, measurable campaigns.</p></div>
      <p>Her deepest expertise lies in education and manufacturing, where she's helped brands sharpen their voice and connect with the audiences that matter most.</p>
      <p>Now part of the YB Marketing team in Chicago, Sophie brings energy and insight to every project. Whether she's shaping content strategy, guiding creative direction, or being a reliable sounding board for clients, she helps brands rise above the competition.</p>
      <p>When she's not brainstorming her next campaign, you'll find her cheering on the Jayhawks during basketball season, hopping on the Chiefs bandwagon come fall, or seeking out the best Kansas City barbecue in the Midwest. A writer at heart, Sophie also has a bucket-list dream of publishing a short story or novel someday.</p>
    </div>
  </div>
</section>"""
    body += team_contact_section_html("Sophie Mann")
    body += cta_strip()
    return "sophie", "Sophie Mann — Account Executive | YB Marketing", "Meet Sophie Mann, account executive at YB Marketing based in Chicago.", body


def page_kayelyn():
    body = hero_block(
        "Kayelyn Aggett",
        "Social Media Manager",
        "Five-plus years of social media and digital marketing experience dedicated to content that helps clients reach their goals.",
        "assets/kayelyn-headshot.webp",
        [
            ("kayelyn@yakimabranding.com", "mailto:kayelyn@yakimabranding.com", MAIL_SVG),
            ("509-204-0632", "tel:5092040632", PHONE_SVG),
        ],
    )
    body += f"""
<section class="team-body" style="background:var(--bg-soft)">
  <div class="container" style="max-width:720px">
    <div class="team-prose" style="text-align:center">
      <p>Kayelyn brings valuable expertise to the table with over 5 years of experience in the fields of social media management and digital marketing. Her commitment to delivering top-notch content to clients is a testament to her dedication to helping them reach their goals and drive successful growth.</p>
    </div>
    <div class="team-social-band">
      <h3>Social media that supports your brand</h3>
      <p>From content planning to publishing and engagement, Kayelyn helps your social channels work as part of a complete marketing strategy — not an afterthought.</p>
      <div style="margin-top:22px">
        <a href="{PREFIX}services/social-media.html" class="btn btn-grad">Explore Social Media Services</a>
      </div>
    </div>
  </div>
</section>"""
    body += team_contact_section_html("Kayelyn Aggett")
    body += cta_strip()
    return "kayelyn", "Kayelyn Aggett — Social Media Manager | YB Marketing", "Meet Kayelyn Aggett, social media manager at YB Marketing.", body


def page_kirsten():
    body = hero_block(
        "Kirsten Gonzalez",
        "Marketing Administrator",
        "Versatile marketing professional specializing in brand reputation, social media, and cross-channel project support.",
        "assets/kirsten-headshot.webp",
        [
            ("kirsten@yakimabranding.com", "mailto:kirsten@yakimabranding.com", MAIL_SVG),
        ],
    )
    body += f"""
<section class="team-body" style="background:#fff">
  <div class="container team-layout-split">
    <div class="team-prose">
      <p>With 3+ years of experience as a versatile marketing professional, Kirsten Gonzalez has established herself as a true jack-of-all-trades. While she specializes in brand reputation and social media marketing, she brings a strategic, creative, and solutions-focused approach to every project.</p>
      <p>At YB, she provides tailored marketing support to clients and team members across a wide range of industries. She ensures each project aligns with specific goals and needs — whether it involves administrative assistance, social media management, email marketing, SEO, website maintenance, or broader initiatives.</p>
      <p>Her overarching goal is to build meaningful, trust-driven relationships with clients, ensuring they feel supported, confident, and equipped to thrive in an ever-evolving digital landscape.</p>
      <h2>How she supports your marketing</h2>
      <div class="team-skill-grid">
        <span class="team-skill">Social Media</span>
        <span class="team-skill">Email Marketing</span>
        <span class="team-skill">SEO Support</span>
        <span class="team-skill">Website Updates</span>
        <span class="team-skill">Brand Reputation</span>
        <span class="team-skill">Admin &amp; Coordination</span>
      </div>
    </div>
    {team_contact_aside_html("Kirsten Gonzalez", f'''
    <div class="team-aside-card team-aside-info">
      <h3>Work with Kirsten</h3>
      <p class="team-aside-info-text">Kirsten coordinates behind the scenes so your campaigns stay on track and your brand stays consistent across channels.</p>
    </div>''')}
  </div>
</section>"""
    body += cta_strip()
    return "kirsten", "Kirsten Gonzalez — Marketing Administrator | YB Marketing", "Meet Kirsten Gonzalez, marketing administrator at YB Marketing.", body


BUILDERS = [page_kevin, page_jacob, page_kristin, page_sophie, page_kayelyn, page_kirsten]

# kirsten URL on live site is about-kirsten - use kirsten.html locally


def update_about_links():
    path = ROOT / "about.html"
    text = path.read_text(encoding="utf-8")
    profile_btn = '          <a href="{href}" class="team-link team-link-profile">Meet {first}</a>\n'
    pairs = [
        ("<!-- Kevin Dean -->", "about/kevin.html", "Kevin"),
        ("<!-- Jacob Ross -->", "about/jacob.html", "Jacob"),
        ("<!-- Kristin Sparling -->", "about/kristin.html", "Kristin"),
        ("<!-- Sophie Mann -->", "about/sophie.html", "Sophie"),
        ("<!-- Kayelyn Aggett -->", "about/kayelyn.html", "Kayelyn"),
        ("<!-- Kirsten Gonzalez", "about/kirsten.html", "Kirsten"),
    ]
    for marker, href, first in pairs:
        start = text.find(marker)
        if start == -1:
            continue
        end = text.find("<!--", start + len(marker))
        if end == -1:
            end = len(text)
        block = text[start:end]
        if "team-link-profile" in block:
            continue
        insert = profile_btn.format(href=href, first=first)
        block = block.replace("        </div>\n      </div>", f"{insert}        </div>\n      </div>", 1)
        text = text[:start] + block + text[end:]
    path.write_text(text, encoding="utf-8")


def main():
    ABOUT_DIR.mkdir(parents=True, exist_ok=True)
    for builder in BUILDERS:
        theme, title, desc, body = builder()
        out = ABOUT_DIR / f"{theme}.html"
        out.write_text(shell(title, desc, theme, body), encoding="utf-8")
        print(f"  · about/{theme}.html")
    update_about_links()
    print("\nUpdated about.html team links")


if __name__ == "__main__":
    main()
