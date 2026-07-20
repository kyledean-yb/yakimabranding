"use client";

import type { FormEvent } from "react";
import { useState } from "react";
import { Button } from "@/components/ui/Button";
import {
  LANDING_HEADER_HS_FORM_ID,
  LANDING_HS_PORTAL_ID,
  LANDING_THANK_YOU_PATH,
} from "@/components/landing/HubSpotLeadForm";

type HorizontalLandingFormProps = {
  ctaLabel: string;
  trustLine?: string;
  source?: string;
  redirect?: string;
};

function getCookie(name: string): string | undefined {
  if (typeof document === "undefined") return undefined;
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : undefined;
}

async function submitToHubSpot(fields: { name: string; value: string }[], source: string) {
  const hutk = getCookie("hubspotutk");
  const allFields = [...fields];
  if (source) {
    allFields.push({
      name: "form_submission_page",
      value: `${typeof window !== "undefined" ? window.location.pathname : ""} (${source})`,
    });
  }

  const payload: Record<string, unknown> = {
    fields: allFields,
    context: {
      pageUri: typeof window !== "undefined" ? window.location.href : "",
      pageName: typeof document !== "undefined" ? document.title : "",
      ...(hutk ? { hutk } : {}),
    },
  };

  const url = `https://api.hsforms.com/submissions/v3/integration/submit/${LANDING_HS_PORTAL_ID}/${LANDING_HEADER_HS_FORM_ID}`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    // Retry without optional tracking field if HubSpot rejects unknown properties
    if (allFields.length > fields.length) {
      const retry = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...payload, fields }),
      });
      if (retry.ok) return;
      const err = await retry.json().catch(() => null);
      throw new Error(err?.message || `HubSpot submit failed (${retry.status})`);
    }
    const err = await res.json().catch(() => null);
    throw new Error(err?.message || `HubSpot submit failed (${res.status})`);
  }
}

export function HorizontalLandingForm({
  ctaLabel,
  trustLine,
  source = "HVAC Landing Page Header",
  redirect = LANDING_THANK_YOU_PATH,
}: HorizontalLandingFormProps) {
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    if (typeof form.checkValidity === "function" && !form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const data = new FormData(form);
    const fields = [
      { name: "firstname", value: String(data.get("firstname") || "").trim() },
      { name: "lastname", value: String(data.get("lastname") || "").trim() },
      { name: "email", value: String(data.get("email") || "").trim() },
      { name: "phone", value: String(data.get("phone") || "").trim() },
    ].filter((f) => f.value);

    setSubmitting(true);
    setError(null);
    try {
      await submitToHubSpot(fields, source);
      window.location.href = redirect;
    } catch (err) {
      setSubmitting(false);
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
    }
  }

  return (
    <form className="landing-form-compact" onSubmit={onSubmit} noValidate={false}>
      <label className="landing-form-compact-field">
        <span className="text-xs font-semibold uppercase tracking-wide text-fg3">First Name</span>
        <input
          className="yb-input landing-form-compact-input"
          type="text"
          name="firstname"
          placeholder="First name"
          autoComplete="given-name"
          required
        />
      </label>
      <label className="landing-form-compact-field">
        <span className="text-xs font-semibold uppercase tracking-wide text-fg3">Last Name</span>
        <input
          className="yb-input landing-form-compact-input"
          type="text"
          name="lastname"
          placeholder="Last name"
          autoComplete="family-name"
        />
      </label>
      <label className="landing-form-compact-field">
        <span className="text-xs font-semibold uppercase tracking-wide text-fg3">Email</span>
        <input
          className="yb-input landing-form-compact-input"
          type="email"
          name="email"
          placeholder="you@company.com"
          autoComplete="email"
          required
        />
      </label>
      <label className="landing-form-compact-field">
        <span className="text-xs font-semibold uppercase tracking-wide text-fg3">Phone</span>
        <input
          className="yb-input landing-form-compact-input"
          type="tel"
          name="phone"
          placeholder="(555) 555-5555"
          autoComplete="tel"
          required
        />
      </label>
      <div className="landing-form-compact-submit">
        <span className="text-xs font-semibold uppercase tracking-wide text-fg3 opacity-0" aria-hidden="true">
          Submit
        </span>
        <Button type="submit" className="btn-form-inline w-full" disabled={submitting}>
          {submitting ? "Sending…" : ctaLabel}
        </Button>
        {trustLine ? <p className="landing-form-compact-trust">{trustLine}</p> : null}
        {error ? <p className="landing-form-compact-error">{error}</p> : null}
      </div>
    </form>
  );
}
