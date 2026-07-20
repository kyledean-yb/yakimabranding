"use client";

import type { FormEvent } from "react";
import { Button } from "@/components/ui/Button";

const THANK_YOU_PATH = "/thank-you-landing-page";

type LeadCaptureFormProps = {
  id?: string;
  ctaLabel: string;
  compact?: boolean;
  trustLine?: string;
};

function handleLeadSubmit(e: FormEvent<HTMLFormElement>) {
  e.preventDefault();
  const form = e.currentTarget;
  if (typeof form.checkValidity === "function" && !form.checkValidity()) {
    form.reportValidity();
    return;
  }
  window.location.href = THANK_YOU_PATH;
}

export function LeadCaptureForm({
  id,
  ctaLabel,
  compact = false,
  trustLine,
}: LeadCaptureFormProps) {
  if (compact) {
    return (
      <form id={id} className="landing-form-compact" onSubmit={handleLeadSubmit}>
        <label className="landing-form-compact-field">
          <span className="text-xs font-semibold uppercase tracking-wide text-fg3">Name</span>
          <input
            className="yb-input landing-form-compact-input"
            type="text"
            name="name"
            placeholder="Your name"
            autoComplete="name"
            required
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
        <label className="landing-form-compact-field">
          <span className="text-xs font-semibold uppercase tracking-wide text-fg3">Company</span>
          <input
            className="yb-input landing-form-compact-input"
            type="text"
            name="company"
            placeholder="Company name"
            autoComplete="organization"
            required
          />
        </label>
        <div className="landing-form-compact-submit">
          <span className="text-xs font-semibold uppercase tracking-wide text-fg3 opacity-0" aria-hidden="true">
            Submit
          </span>
          <Button type="submit" className="btn-form-inline w-full">
            {ctaLabel}
          </Button>
          {trustLine ? <p className="landing-form-compact-trust">{trustLine}</p> : null}
        </div>
      </form>
    );
  }

  return (
    <form id={id} className="grid gap-3 md:grid-cols-2" onSubmit={handleLeadSubmit}>
      <label className="grid gap-1.5">
        <span className="text-xs font-semibold uppercase tracking-wide text-fg3">Name</span>
        <input className="yb-input" type="text" name="name" placeholder="Your name" autoComplete="name" required />
      </label>
      <label className="grid gap-1.5">
        <span className="text-xs font-semibold uppercase tracking-wide text-fg3">Email</span>
        <input
          className="yb-input"
          type="email"
          name="email"
          placeholder="you@company.com"
          autoComplete="email"
          required
        />
      </label>
      <label className="grid gap-1.5">
        <span className="text-xs font-semibold uppercase tracking-wide text-fg3">Phone</span>
        <input
          className="yb-input"
          type="tel"
          name="phone"
          placeholder="(555) 555-5555"
          autoComplete="tel"
          required
        />
      </label>
      <label className="grid gap-1.5">
        <span className="text-xs font-semibold uppercase tracking-wide text-fg3">Company</span>
        <input
          className="yb-input"
          type="text"
          name="company"
          placeholder="Company name"
          autoComplete="organization"
          required
        />
      </label>
      <div className="md:col-span-2">
        <Button type="submit" className="w-full">
          {ctaLabel}
        </Button>
      </div>
    </form>
  );
}
