"use client";

import type { FormEvent } from "react";
import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/Button";
import { HONEYPOT_NAME, checkLead } from "@/lib/lead-guard";
import { LANDING_THANK_YOU_PATH } from "@/components/landing/GhlLeadForm";
import { submitToGhl } from "@/lib/ghl";

type HorizontalLandingFormProps = {
  ctaLabel: string;
  trustLine?: string;
  source?: string;
  redirect?: string;
};

export function HorizontalLandingForm({
  ctaLabel,
  trustLine,
  source = "HVAC Landing Page Header",
  redirect = LANDING_THANK_YOU_PATH,
}: HorizontalLandingFormProps) {
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const startedAt = useRef(0);
  const interacted = useRef(false);

  useEffect(() => {
    startedAt.current = Date.now();
  }, []);

  function markInteracted() {
    interacted.current = true;
  }

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    if (typeof form.checkValidity === "function" && !form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const data = new FormData(form);
    const verdict = checkLead({
      honeypot: String(data.get(HONEYPOT_NAME) || ""),
      startedAt: startedAt.current,
      interacted: interacted.current,
      name: `${data.get("firstname") || ""} ${data.get("lastname") || ""}`,
      email: String(data.get("email") || ""),
      phone: String(data.get("phone") || ""),
    });
    if (verdict === "bot") {
      window.location.href = redirect;
      return;
    }
    if (verdict) {
      setError(verdict);
      return;
    }

    const firstName = String(data.get("firstname") || "").trim();
    const lastName = String(data.get("lastname") || "").trim();

    setSubmitting(true);
    setError(null);
    await submitToGhl({
      name: `${firstName} ${lastName}`.trim(),
      email: String(data.get("email") || "").trim(),
      phone: String(data.get("phone") || "").trim(),
      source,
    });
    window.location.href = redirect;
  }

  return (
    <form
      className="landing-form-compact"
      onSubmit={onSubmit}
      onFocus={markInteracted}
      onInput={markInteracted}
      noValidate={false}
    >
      <div aria-hidden="true" style={{ position: "absolute", left: "-10000px", width: 1, height: 1, overflow: "hidden" }}>
        <label>
          Company website
          <input type="text" name={HONEYPOT_NAME} defaultValue="" tabIndex={-1} autoComplete="off" />
        </label>
      </div>
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
