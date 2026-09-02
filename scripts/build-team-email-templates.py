#!/usr/bin/env python3
"""Generate GoHighLevel thank-you email templates for team profile forms."""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "emails"

MEMBERS = [
    {
        "slug": "jacob",
        "name": "Jacob Ross",
        "short": "Jacob",
        "role": "Account Executive",
        "photo": "jacob-headshot.webp",
        "booking": "https://link.bluesoftwebsites.com/widget/booking/lRk0w69pQF0RRze2xKqx",
        "email": "jacob@yakimabranding.com",
        "phone_display": "(509) 203-1007",
        "phone_href": "tel:5092031007",
        "profile_url": "https://yakimabranding.com/about/jacob",
        "preheader": "Jacob Ross received your message and will be in touch within 1 business day.",
        "hero_lead": (
            "we've received your message and Jacob will be in touch within "
            "<strong style=\"color:#ffffff;\">1 business day</strong>. "
            "We look forward to learning more about your business and how we can help you grow."
        ),
        "step1": (
            "I read every inquiry that comes through my profile — no hand-offs to a generic inbox. "
            "I'll make sure your message gets the right attention from our team."
        ),
        "step2": (
            "Expect a call or email from me within 1 business day. "
            "Want to skip the wait? Book a free 30-minute intro call using the button below."
        ),
        "step3": (
            "Once we connect, we'll start with a clear picture of your goals and build a strategy "
            "tailored to your business — whether that's SEO, Google Ads, web, or the full picture."
        ),
        "cta": "Book a Call with Jacob",
    },
    {
        "slug": "kevin",
        "name": "Kevin Dean",
        "short": "Kevin",
        "role": "Owner",
        "photo": "kevin-headshot.webp",
        "booking": "https://link.bluesoftwebsites.com/widget/booking/UFZzPYN4w4sYMXsTvGHP",
        "email": "kevin@yakimabranding.com",
        "phone_display": "(509) 901-9735",
        "phone_href": "tel:5099019735",
        "profile_url": "https://yakimabranding.com/about/kevin",
        "preheader": "Kevin Dean received your message and will be in touch within 1 business day.",
        "hero_lead": (
            "we've received your message and Kevin will be in touch within "
            "<strong style=\"color:#ffffff;\">1 business day</strong>. "
            "We look forward to learning more about your business and where you want to take it."
        ),
        "step1": (
            "I personally review inquiries that come through my profile. "
            "Every message gets real attention from me or someone I trust on our team."
        ),
        "step2": (
            "You'll hear from me within 1 business day. "
            "Prefer to get on the calendar right away? Use the button below to book a free intro meeting."
        ),
        "step3": (
            "When we connect, we'll talk through your goals, your current marketing, and where the biggest "
            "opportunities are — then map out a plan that makes sense for your business."
        ),
        "cta": "Book a Meeting with Kevin",
    },
    {
        "slug": "sophie",
        "name": "Sophie Mann",
        "short": "Sophie",
        "role": "Account Executive",
        "photo": "sophie-headshot.webp",
        "booking": "https://link.bluesoftwebsites.com/widget/booking/dwvAN8VTyHIbsbW3OLUF",
        "email": "sophie@yakimabranding.com",
        "phone_display": "(303) 955-6979",
        "phone_href": "tel:3039556979",
        "profile_url": "https://yakimabranding.com/about/sophie",
        "preheader": "Sophie Mann received your message and will be in touch within 1 business day.",
        "hero_lead": (
            "we've received your message and Sophie will be in touch within "
            "<strong style=\"color:#ffffff;\">1 business day</strong>. "
            "We look forward to learning more about your business and how we can help you grow."
        ),
        "step1": (
            "I review every message that comes through my profile personally. "
            "No bots, no generic autoresponders — just a real conversation waiting to happen."
        ),
        "step2": (
            "Expect to hear from me within 1 business day. "
            "Want to get ahead of the queue? Book a free 30-minute intro call below."
        ),
        "step3": (
            "When we connect, we'll dig into your brand, your audience, and your goals — "
            "then shape a strategy that helps you stand out and grow."
        ),
        "cta": "Book a Call with Sophie",
    },
]


def template(member: dict) -> str:
    name = html.escape(member["name"])
    short = html.escape(member["short"])
    role = html.escape(member["role"])
    email = html.escape(member["email"])
    photo = f"https://www.yakimabranding.com/assets/{html.escape(member['photo'])}"
    booking = html.escape(member["booking"])
    profile = html.escape(member["profile_url"])
    phone_display = html.escape(member["phone_display"])
    phone_href = html.escape(member["phone_href"])

    return f"""<!--
  GoHighLevel email template — thank you / {short} profile form
-->
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="x-apple-disable-message-reformatting">
  <title>Thank You | {name} | YB Marketing</title>
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
    {html.escape(member["preheader"])}
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
                Thank You for<br>Reaching Out!
              </h1>
              <p style="margin:0 0 28px;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:16px;line-height:1.65;color:#B8C4DE;">
                Hi {{{{contact.first_name}}}}, {member["hero_lead"]}
              </p>

              <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width:480px;margin:0 auto;">
                <tr>
                  <td style="background-color:#22314F;border:1px solid #2C3E63;border-radius:12px;padding:20px 24px;text-align:center;">
                    <p style="margin:0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65;color:#B8C4DE;">
                      <strong style="color:#ffffff;">Need something urgent?</strong><br>
                      Call me at <a href="{phone_href}" style="color:#2BC4F0;font-weight:600;text-decoration:none;">{phone_display}</a>
                      or email <a href="mailto:{email}" style="color:#2BC4F0;font-weight:600;text-decoration:none;">{email}</a>
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
                          <p style="margin:0 0 6px;font-family:'Sora',Arial,Helvetica,sans-serif;font-size:13px;font-weight:800;letter-spacing:0.04em;text-transform:uppercase;color:#16203A;">I Review Your Message</p>
                          <p style="margin:0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65;color:#4A5673;">{html.escape(member["step1"])}</p>
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
                          <p style="margin:0 0 6px;font-family:'Sora',Arial,Helvetica,sans-serif;font-size:13px;font-weight:800;letter-spacing:0.04em;text-transform:uppercase;color:#16203A;">I Reach Out Within 1 Business Day</p>
                          <p style="margin:0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65;color:#4A5673;">{html.escape(member["step2"])}</p>
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
                          <p style="margin:0 0 6px;font-family:'Sora',Arial,Helvetica,sans-serif;font-size:13px;font-weight:800;letter-spacing:0.04em;text-transform:uppercase;color:#16203A;">We Build Your Custom Strategy</p>
                          <p style="margin:0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65;color:#4A5673;">{html.escape(member["step3"])}</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-bottom:32px;">
                <tr>
                  <td align="center">
                    <!--[if mso]>
                    <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{booking}" style="height:52px;v-text-anchor:middle;width:300px;" arcsize="20%" strokecolor="#3F6FD6" fillcolor="#3F6FD6">
                      <w:anchorlock/>
                      <center style="color:#ffffff;font-family:Arial,sans-serif;font-size:16px;font-weight:bold;">{html.escape(member["cta"])} &rarr;</center>
                    </v:roundrect>
                    <![endif]-->
                    <!--[if !mso]><!-->
                    <a href="{booking}" target="_blank" style="display:inline-block;background-color:#3F6FD6;color:#ffffff;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:16px;font-weight:700;text-decoration:none;padding:16px 32px;border-radius:12px;mso-hide:all;">
                      {html.escape(member["cta"])} &rarr;
                    </a>
                    <!--<![endif]-->
                  </td>
                </tr>
              </table>

              <!-- Signature -->
              <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="border-top:1px solid #E3E9F2;padding-top:28px;">
                <tr>
                  <td width="72" valign="top" style="padding-right:16px;">
                    <img src="{photo}" alt="{name}" width="64" height="64" style="display:block;border-radius:50%;border:2px solid #E3E9F2;">
                  </td>
                  <td valign="middle" style="text-align:left;">
                    <p style="margin:0 0 2px;font-family:'Sora',Arial,Helvetica,sans-serif;font-size:18px;font-weight:800;color:#16203A;letter-spacing:-0.02em;">{name}</p>
                    <p style="margin:0 0 8px;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:13px;font-weight:600;color:#3F6FD6;">{role} · YB Marketing</p>
                    <p style="margin:0;font-family:'Plus Jakarta Sans',Arial,Helvetica,sans-serif;font-size:13px;line-height:1.6;color:#4A5673;">
                      <a href="mailto:{email}" style="color:#3F6FD6;font-weight:600;text-decoration:none;">{email}</a><br>
                      <a href="{phone_href}" style="color:#4A5673;text-decoration:none;">{phone_display}</a><br>
                      <a href="{profile}" style="color:#4A5673;text-decoration:underline;">yakimabranding.com/about/{html.escape(member["slug"])}</a>
                    </p>
                  </td>
                </tr>
              </table>
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
    for member in MEMBERS:
        path = OUT_DIR / f"thank-you-{member['slug']}.html"
        path.write_text(template(member), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
