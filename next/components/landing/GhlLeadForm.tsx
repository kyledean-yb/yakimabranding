"use client";

import Script from "next/script";

/** Same GoHighLevel webhook form as the static site (lead_form_html + /js/lead-form.js). */
export const LANDING_THANK_YOU_PATH = "/thank-you-landing-page";

const INTEREST_OPTIONS: [string, string][] = [
  ["web-design", "Web Design"],
  ["seo", "SEO"],
  ["google-ads", "Google Ads"],
  ["branding", "Branding & Design"],
  ["social-media", "Social Media"],
  ["content-marketing", "Content Marketing"],
  ["press-releases", "Press Releases"],
  ["customer-growth", "Customer Growth & Communication Tool"],
  ["ai-for-business", "AI for Business"],
  ["ai-for-small-business", "AI for Small Business"],
  ["video-animation", "Video Animation"],
  ["other", "Not sure / Other"],
];

type GhlLeadFormProps = {
  source: string;
  redirect?: string;
  submitLabel?: string;
};

export function GhlLeadForm({ source, redirect = LANDING_THANK_YOU_PATH, submitLabel = "Get Started Today" }: GhlLeadFormProps) {
  const id = (field: string) => `yb-landing-${field}`;
  return (
    <>
      <link rel="stylesheet" href="/lead-form.css" />
      <form className="yb-lead-form" action="#" method="post" data-source={source} data-redirect={redirect} noValidate>
        <div className="yb-lead-form__row">
          <div className="yb-lead-form__field">
            <label htmlFor={id("name")}>Name *</label>
            <input id={id("name")} name="name" type="text" autoComplete="name" required placeholder="Your name" />
          </div>
          <div className="yb-lead-form__field">
            <label htmlFor={id("email")}>Email *</label>
            <input id={id("email")} name="email" type="email" autoComplete="email" required placeholder="you@company.com" />
          </div>
        </div>
        <div className="yb-lead-form__row">
          <div className="yb-lead-form__field">
            <label htmlFor={id("phone")}>Phone *</label>
            <input id={id("phone")} name="phone" type="tel" autoComplete="tel" required placeholder="(480) 555-0100" />
          </div>
          <div className="yb-lead-form__field">
            <label htmlFor={id("company")}>Company or URL</label>
            <input id={id("company")} name="company" type="text" autoComplete="organization" placeholder="yourcompany.com" />
          </div>
        </div>
        <div className="yb-lead-form__field">
          <label htmlFor={id("interest")}>I&apos;m interested in *</label>
          <div className="yb-lead-form__select-wrap">
            <select id={id("interest")} name="interest" required defaultValue="">
              <option value="" disabled>
                What are you interested in?
              </option>
              {INTEREST_OPTIONS.map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </div>
        </div>
        <div className="yb-lead-form__field">
          <label htmlFor={id("message")}>How can we help? *</label>
          <textarea id={id("message")} name="message" rows={4} required placeholder="Tell us about your goals…" />
        </div>
        <div className="yb-lead-form__hp" aria-hidden="true">
          <label htmlFor={id("hp")}>Company website</label>
          <input id={id("hp")} name="company_website" type="text" defaultValue="" tabIndex={-1} autoComplete="off" />
        </div>
        <input type="hidden" name="form_started" defaultValue="" />
        <input type="hidden" name="source" defaultValue={source} />
        <input type="hidden" name="page_url" defaultValue="" />
        <button type="submit" className="btn btn-grad yb-lead-form__submit">
          {submitLabel}
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
            <line x1="5" y1="12" x2="19" y2="12" />
            <polyline points="12 5 19 12 12 19" />
          </svg>
        </button>
        <p className="yb-lead-form__status" hidden aria-live="polite" />
      </form>
      <Script src="/js/lead-form-config.js" strategy="afterInteractive" />
      <Script src="/js/lead-form.js" strategy="afterInteractive" />
    </>
  );
}
