"use client";

import Script from "next/script";

export const LANDING_HS_PORTAL_ID = "243964841";
export const LANDING_HS_REGION = "na2";
/** Compact header form for HVAC landing page */
export const LANDING_HEADER_HS_FORM_ID = "a468be00-425a-426f-aac6-9930570f0374";
/** Same form as home / contact ("Send Us a Message") */
export const HOME_HS_FORM_ID = "c7a3c349-a4e9-4608-9771-9aa39c7f05e1";
export const LANDING_THANK_YOU_PATH = "/thank-you-landing-page";
export const LANDING_HS_EMBED_SCRIPT = `https://js-na2.hsforms.net/forms/embed/${LANDING_HS_PORTAL_ID}.js`;

type HubSpotLeadFormProps = {
  formId?: string;
  source?: string;
  /** Hard-coded thank-you path (data-redirect). */
  redirect?: string;
  theme?: "landing-header" | "default";
  className?: string;
};

export function HubSpotLeadForm({
  formId = LANDING_HEADER_HS_FORM_ID,
  source = "HVAC Landing Page",
  redirect = LANDING_THANK_YOU_PATH,
  theme = "default",
  className,
}: HubSpotLeadFormProps) {
  return (
    <>
      <div
        className={["yb-hs-form", className].filter(Boolean).join(" ")}
        data-source={source}
        data-redirect={redirect}
        data-yb-theme={theme}
      >
        <div
          className="hs-form-frame"
          data-region={LANDING_HS_REGION}
          data-form-id={formId}
          data-portal-id={LANDING_HS_PORTAL_ID}
        />
      </div>
      <Script src={LANDING_HS_EMBED_SCRIPT} strategy="afterInteractive" />
      <Script src="/js/hubspot-form.js?v=landing-header-3" strategy="afterInteractive" />
    </>
  );
}
