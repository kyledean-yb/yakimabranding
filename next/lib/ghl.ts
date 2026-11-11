/** GoHighLevel inbound webhook, shared with /js/lead-form-config.js on the static site. */
export const GHL_WEBHOOK_URL =
  "https://services.leadconnectorhq.com/hooks/0Pc2NnJAQkzYB3hhPi1b/webhook-trigger/1865a2f2-d6f5-48ec-a4a7-4d68fb92f329";

type GhlLead = {
  name: string;
  email: string;
  phone: string;
  source: string;
  company?: string;
  interest?: string;
  interestLabel?: string;
  message?: string;
};

/** Payload matches /js/lead-form.js so GHL workflows treat every form the same. */
export async function submitToGhl(lead: GhlLead): Promise<void> {
  const payload = {
    name: lead.name,
    email: lead.email,
    phone: lead.phone,
    company: lead.company || "",
    interest: lead.interest || "",
    interest_label: lead.interestLabel || "",
    message: lead.message || "",
    source: lead.source,
    site: "YB Marketing",
    site_domain: "yakimabranding.com",
    page_url: window.location.href,
    page_path: window.location.pathname + window.location.search,
    submitted_at: new Date().toISOString(),
  };
  try {
    await fetch(GHL_WEBHOOK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload),
      mode: "cors",
      keepalive: true,
    });
  } catch {
    // GHL often accepts the request even when the browser cannot read the CORS response.
  }
}
