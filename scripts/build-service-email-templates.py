#!/usr/bin/env python3
"""Generate GoHighLevel thank-you email templates for service hub forms."""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "emails"

SERVICES = [
    {
        "slug": "seo",
        "label": "SEO",
        "source": "SEO Service Page",
        "service_url": "https://yakimabranding.com/seo/",
        "preheader": "We've received your SEO inquiry. A YB specialist will be in touch within 1 business day.",
        "headline": "Thank You for Your<br>Interest in SEO!",
        "hero_lead": (
            "we've received your inquiry about SEO and a member of our team will be in touch within "
            "<strong style=\"color:#ffffff;\">1 business day</strong>. "
            "We look forward to learning how we can help your business rank higher and get found online."
        ),
        "step1_title": "We Review Your SEO Goals",
        "step1": (
            "A real member of our SEO team reviews every inquiry personally — looking at your visibility, "
            "competition, and where the biggest ranking opportunities are."
        ),
        "step2_title": "We Reach Out Within 1 Business Day",
        "step2": (
            "Expect a call or email from our team within 1 business day. "
            "Want to skip the wait? Book a free intro call and we'll start with a quick look at your site."
        ),
        "step3_title": "We Build Your SEO Roadmap",
        "step3": (
            "Once we connect, we'll audit your website and search presence — then map out a strategy "
            "tailored to your market, whether that's local SEO, technical fixes, or content that ranks."
        ),
        "cta": "Book a Free SEO Consultation",
    },
    {
        "slug": "google-ads",
        "label": "Google Ads",
        "source": "Google Ads Service Page",
        "service_url": "https://yakimabranding.com/google-ads/",
        "preheader": "We've received your Google Ads inquiry. A YB PPC specialist will be in touch within 1 business day.",
        "headline": "Thank You for Your<br>Interest in Google Ads!",
        "hero_lead": (
            "we've received your inquiry about Google Ads management and a member of our team will be in touch within "
            "<strong style=\"color:#ffffff;\">1 business day</strong>. "
            "We look forward to learning how we can help you drive more qualified leads from paid search."
        ),
        "step1_title": "We Review Your Ad Goals",
        "step1": (
            "Our certified PPC specialists review every inquiry personally — looking at your current spend, "
            "campaign structure, and where wasted budget might be hiding."
        ),
        "step2_title": "We Reach Out Within 1 Business Day",
        "step2": (
            "Expect a call or email from our team within 1 business day. "
            "Prefer to get on the calendar right away? Book a free intro call using the button below."
        ),
        "step3_title": "We Build Your Campaign Strategy",
        "step3": (
            "When we connect, we'll walk through your goals, your current campaigns, and where the biggest "
            "opportunities are — then outline a plan to improve results and ROI."
        ),
        "cta": "Book a Free Ads Consultation",
    },
    {
        "slug": "web-design",
        "label": "Web Design",
        "source": "Web Design Service Page",
        "service_url": "https://yakimabranding.com/web-design/",
        "preheader": "We've received your web design inquiry. A YB specialist will be in touch within 1 business day.",
        "headline": "Thank You for Your<br>Interest in Web Design!",
        "hero_lead": (
            "we've received your inquiry about web design and a member of our team will be in touch within "
            "<strong style=\"color:#ffffff;\">1 business day</strong>. "
            "We look forward to learning about your project and how we can build a site that converts."
        ),
        "step1_title": "We Review Your Project",
        "step1": (
            "Our web team reviews every inquiry personally — looking at your goals, timeline, and what "
            "you need from a new or redesigned website."
        ),
        "step2_title": "We Reach Out Within 1 Business Day",
        "step2": (
            "Expect a call or email from our team within 1 business day. "
            "Want to talk sooner? Book a free intro call and tell us about your vision."
        ),
        "step3_title": "We Plan Your Website",
        "step3": (
            "Once we connect, we'll discuss your brand, features, and budget — then outline a path forward, "
            "whether that's WordPress, Wix, or a custom build."
        ),
        "cta": "Book a Free Web Design Consultation",
    },
    {
        "slug": "social-media",
        "label": "Social Media",
        "source": "Social Media Service Page",
        "service_url": "https://yakimabranding.com/social-media/",
        "preheader": "We've received your social media inquiry. A YB specialist will be in touch within 1 business day.",
        "headline": "Thank You for Your<br>Interest in Social Media!",
        "hero_lead": (
            "we've received your inquiry about social media management and a member of our team will be in touch within "
            "<strong style=\"color:#ffffff;\">1 business day</strong>. "
            "We look forward to learning how we can help you grow your audience and turn followers into customers."
        ),
        "step1_title": "We Review Your Social Presence",
        "step1": (
            "Our social team reviews every inquiry personally — looking at your current channels, content, "
            "and where the biggest growth opportunities are."
        ),
        "step2_title": "We Reach Out Within 1 Business Day",
        "step2": (
            "Expect a call or email from our team within 1 business day. "
            "Want to get ahead of the queue? Book a free intro call below."
        ),
        "step3_title": "We Build Your Content Plan",
        "step3": (
            "When we connect, we'll dig into your brand voice, platforms, and goals — then shape a content "
            "strategy that grows reach and drives real engagement."
        ),
        "cta": "Book a Free Social Media Consultation",
    },
    {
        "slug": "branding",
        "label": "Branding",
        "source": "Branding Service Page",
        "service_url": "https://yakimabranding.com/branding/",
        "preheader": "We've received your branding inquiry. A YB designer will be in touch within 1 business day.",
        "headline": "Thank You for Your<br>Interest in Branding!",
        "hero_lead": (
            "we've received your inquiry about branding and design and a member of our team will be in touch within "
            "<strong style=\"color:#ffffff;\">1 business day</strong>. "
            "We look forward to learning about your business and how we can help your brand stand out."
        ),
        "step1_title": "We Review Your Brand Needs",
        "step1": (
            "Our design team reviews every inquiry personally — looking at where you are today and what "
            "you need, from a new logo to a complete visual identity system."
        ),
        "step2_title": "We Reach Out Within 1 Business Day",
        "step2": (
            "Expect a call or email from our team within 1 business day. "
            "Ready to talk through your vision? Book a free intro call using the button below."
        ),
        "step3_title": "We Shape Your Brand Direction",
        "step3": (
            "Once we connect, we'll discuss your story, audience, and goals — then outline how strategy, "
            "design, and deliverables can bring consistency to everything customers see."
        ),
        "cta": "Book a Free Branding Consultation",
    },
    {
        "slug": "content-creation",
        "label": "Content Marketing",
        "source": "Content Creation Service Page",
        "service_url": "https://yakimabranding.com/content-marketing/",
        "preheader": "We've received your content marketing inquiry. A YB specialist will be in touch within 1 business day.",
        "headline": "Thank You for Your<br>Interest in Content Marketing!",
        "hero_lead": (
            "we've received your inquiry about content marketing and a member of our team will be in touch within "
            "<strong style=\"color:#ffffff;\">1 business day</strong>. "
            "We look forward to learning how we can help you create content that ranks and converts."
        ),
        "step1_title": "We Review Your Content Goals",
        "step1": (
            "Our content team reviews every inquiry personally — looking at your current site, blog, "
            "and where stronger copy or a content plan could move the needle."
        ),
        "step2_title": "We Reach Out Within 1 Business Day",
        "step2": (
            "Expect a call or email from our team within 1 business day. "
            "Want to skip the wait? Book a free intro call and tell us what you're working on."
        ),
        "step3_title": "We Build Your Content Strategy",
        "step3": (
            "When we connect, we'll talk through your audience, topics, and goals — then outline a plan "
            "for blog posts, website copy, and content that builds authority over time."
        ),
        "cta": "Book a Free Content Consultation",
    },
    {
        "slug": "press-releases",
        "label": "Press Releases",
        "source": "Press Releases Service Page",
        "service_url": "https://yakimabranding.com/press-releases/",
        "preheader": "We've received your press release inquiry. A YB specialist will be in touch within 1 business day.",
        "headline": "Thank You for Your<br>Interest in Press Releases!",
        "hero_lead": (
            "we've received your inquiry about press release writing and distribution and a member of our team will be in touch within "
            "<strong style=\"color:#ffffff;\">1 business day</strong>. "
            "We look forward to learning about your announcement and how we can help you get the word out."
        ),
        "step1_title": "We Review Your Announcement",
        "step1": (
            "Our team reviews every inquiry personally — looking at your news, timing, and whether "
            "you need writing, distribution, or both."
        ),
        "step2_title": "We Reach Out Within 1 Business Day",
        "step2": (
            "Expect a call or email from our team within 1 business day. "
            "Have a launch date coming up? Book a free intro call to get the ball rolling."
        ),
        "step3_title": "We Plan Your Release",
        "step3": (
            "Once we connect, we'll discuss your story, target outlets, and timeline — then outline "
            "how we'll craft and distribute a release that gets noticed."
        ),
        "cta": "Book a Free Consultation",
    },
]


def template(service: dict) -> str:
    label = html.escape(service["label"])
    service_url = html.escape(service["service_url"])
    booking = "https://yakimabranding.com/contact#book"

    return f"""<!--
  GoHighLevel email template — thank you / {label} service form
  Form source: {html.escape(service["source"])}
-->
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="x-apple-disable-message-reformatting">
  <title>Thank You | {label} | YB Marketing</title>
  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <![endif]-->
  <style type="text/css">
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
    table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
    img {{ -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
    body {{ margin: 0 !important; padding: 0 !important; width: 100% !important; }}
    a {{ color: #3F6FD6; text-decoration: none; }}
    @media screen and (max-width: 620px) {{
      .email-container {{ width: 100% !important; }}
      .mobile-pad {{ padding-left: 24px !important; padding-right: 24px !important; }}
    }}
  </style>
</head>
<body style="margin:0;padding:0;background-color:#F6F8FC;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;">

  <div style="display:none;font-size:1px;color:#F6F8FC;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">
    {html.escape(service["preheader"])}
  </div>

  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color:#F6F8FC;">
    <tr>
      <td align="center" style="padding:32px 16px;">
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" class="email-container" style="max-width:600px;width:100%;">

          <tr>
            <td style="background-color:#1B2A4A;border-radius:16px 16px 0 0;padding:36px 40px 40px;text-align:center;" class="mobile-pad">
              <a href="https://yakimabranding.com" target="_blank" style="text-decoration:none;display:inline-block;margin:0 auto 14px;">
                <span style="display:inline-block;background-color:#ffffff;border-radius:12px;padding:10px;line-height:0;">
                  <img src="https://www.yakimabranding.com/assets/yb-logo-color.png" alt="YB Marketing" width="52" height="52" style="display:block;border:0;">
                </span>
              </a>
              <p style="margin:0 0 32px;font-family:'Sora',Arial,Helvetica,sans-serif;font-size:22px;font-weight:800;color:#ffffff;letter-spacing:-0.02em;">
                YB <span style="color:#2BC4F0;">Marketing</span>
              </p>

              <p style="margin:0 0 16px;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:11px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#FF6B57;">
                &#9679;&nbsp; Message Received
              </p>
              <h1 style="margin:0 0 16px;font-family:'Sora',Arial,Helvetica,sans-serif;font-size:28px;font-weight:800;line-height:1.15;color:#ffffff;letter-spacing:-0.02em;">
                {service["headline"]}
              </h1>
              <p style="margin:0 0 28px;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:16px;line-height:1.65;color:#B8C4DE;">
                Hi {{{{contact.first_name}}}}, {service["hero_lead"]}
              </p>

              <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width:480px;margin:0 auto;">
                <tr>
                  <td style="background-color:#22314F;border:1px solid #2C3E63;border-radius:12px;padding:20px 24px;text-align:center;">
                    <p style="margin:0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65;color:#B8C4DE;">
                      <strong style="color:#ffffff;">Need something urgent?</strong><br>
                      Call us at <a href="tel:5099019735" style="color:#2BC4F0;font-weight:600;text-decoration:none;">(509) 901-9735</a>
                      or email <a href="mailto:info@yakimabranding.com" style="color:#2BC4F0;font-weight:600;text-decoration:none;">info@yakimabranding.com</a>
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="background-color:#ffffff;padding:40px;" class="mobile-pad">
              <p style="margin:0 0 6px;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:11px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#3F6FD6;">
                &#9679;&nbsp; What to Expect
              </p>
              <h2 style="margin:0 0 24px;font-family:'Sora',Arial,Helvetica,sans-serif;font-size:22px;font-weight:800;color:#16203A;letter-spacing:-0.02em;">
                Here's What Happens Next
              </h2>

              <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-bottom:12px;">
                <tr>
                  <td style="background-color:#F6F8FC;border:1px solid #E3E9F2;border-radius:16px;padding:24px;">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                      <tr>
                        <td width="56" valign="top" style="padding-right:16px;">
                          <div style="width:48px;height:48px;background-color:#EDF2FD;border-radius:12px;text-align:center;line-height:48px;font-size:20px;">&#128197;</div>
                        </td>
                        <td valign="top">
                          <p style="margin:0 0 6px;font-family:'Sora',Arial,Helvetica,sans-serif;font-size:13px;font-weight:800;letter-spacing:0.04em;text-transform:uppercase;color:#16203A;">{html.escape(service["step1_title"])}</p>
                          <p style="margin:0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65;color:#4A5673;">{html.escape(service["step1"])}</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-bottom:12px;">
                <tr>
                  <td style="background-color:#F6F8FC;border:1px solid #E3E9F2;border-radius:16px;padding:24px;">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                      <tr>
                        <td width="56" valign="top" style="padding-right:16px;">
                          <div style="width:48px;height:48px;background-color:#E4F7FE;border-radius:12px;text-align:center;line-height:48px;font-size:20px;">&#128222;</div>
                        </td>
                        <td valign="top">
                          <p style="margin:0 0 6px;font-family:'Sora',Arial,Helvetica,sans-serif;font-size:13px;font-weight:800;letter-spacing:0.04em;text-transform:uppercase;color:#16203A;">{html.escape(service["step2_title"])}</p>
                          <p style="margin:0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65;color:#4A5673;">{html.escape(service["step2"])}</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-bottom:32px;">
                <tr>
                  <td style="background-color:#F6F8FC;border:1px solid #E3E9F2;border-radius:16px;padding:24px;">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                      <tr>
                        <td width="56" valign="top" style="padding-right:16px;">
                          <div style="width:48px;height:48px;background-color:#E3F8F1;border-radius:12px;text-align:center;line-height:48px;font-size:20px;">&#128200;</div>
                        </td>
                        <td valign="top">
                          <p style="margin:0 0 6px;font-family:'Sora',Arial,Helvetica,sans-serif;font-size:13px;font-weight:800;letter-spacing:0.04em;text-transform:uppercase;color:#16203A;">{html.escape(service["step3_title"])}</p>
                          <p style="margin:0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65;color:#4A5673;">{html.escape(service["step3"])}</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-bottom:16px;">
                <tr>
                  <td align="center">
                    <!--[if mso]>
                    <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{booking}" style="height:52px;v-text-anchor:middle;width:320px;" arcsize="20%" strokecolor="#3F6FD6" fillcolor="#3F6FD6">
                      <w:anchorlock/>
                      <center style="color:#ffffff;font-family:Arial,sans-serif;font-size:16px;font-weight:bold;">{html.escape(service["cta"])} &rarr;</center>
                    </v:roundrect>
                    <![endif]-->
                    <!--[if !mso]><!-->
                    <a href="{booking}" target="_blank" style="display:inline-block;background-color:#3F6FD6;color:#ffffff;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:16px;font-weight:700;text-decoration:none;padding:16px 32px;border-radius:12px;mso-hide:all;">
                      {html.escape(service["cta"])} &rarr;
                    </a>
                    <!--<![endif]-->
                  </td>
                </tr>
              </table>

              <p style="margin:0;text-align:center;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65;color:#4A5673;">
                Or <a href="{service_url}" style="color:#3F6FD6;font-weight:600;text-decoration:underline;">learn more about our {label} services</a>
              </p>
            </td>
          </tr>

          <tr>
            <td style="background-color:#1B2A4A;border-radius:0 0 16px 16px;padding:32px 40px;text-align:center;" class="mobile-pad">
              <p style="margin:0 0 16px;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65;color:#B8C4DE;">
                Award-winning digital marketing agency helping businesses grow through strategic branding, SEO, and comprehensive digital solutions.
              </p>
              <p style="margin:0 0 20px;">
                <a href="https://www.facebook.com/yakimabranding" target="_blank" style="color:#2BC4F0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:13px;font-weight:600;margin:0 10px;">Facebook</a>
                <a href="https://www.instagram.com/yb.marketing_/" target="_blank" style="color:#2BC4F0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:13px;font-weight:600;margin:0 10px;">Instagram</a>
                <a href="https://www.linkedin.com/company/18939370" target="_blank" style="color:#2BC4F0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:13px;font-weight:600;margin:0 10px;">LinkedIn</a>
              </p>
              <p style="margin:0 0 12px;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:12px;line-height:1.6;color:#7C879E;">
                YB Marketing<br>
                17775 E Veit Springs Drive Suite 100<br>
                Rio Verde, Arizona 85263
              </p>
              <p style="margin:0 0 12px;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:12px;color:#7C879E;">
                <a href="{{{{unsubscribe_url}}}}" style="color:#7C879E;text-decoration:underline;">Unsubscribe</a>
                &nbsp;&middot;&nbsp;
                <a href="https://yakimabranding.com/privacy-policy" style="color:#7C879E;text-decoration:underline;">Privacy Policy</a>
              </p>
              <p style="margin:0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:12px;color:#7C879E;">
                &copy; 2026 YB Marketing. All rights reserved.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for service in SERVICES:
        path = OUT_DIR / f"thank-you-{service['slug']}.html"
        path.write_text(template(service), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}  ({service['source']})")


if __name__ == "__main__":
    main()
