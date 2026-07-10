"use client";

import { useMemo } from "react";

const SUMMARY_LOOKUP: Record<string, string> = {
  "seo|google-ads|social-ads":
    "You're building long-term organic authority while driving immediate leads through paid search and social — visibility now, with growth that compounds over time, all under one accountable team.",
  "seo|google-ads|social-email":
    "You're pairing steady organic growth and high-intent paid search with ongoing content and email nurture — built to grow your visibility and keep customers engaged between purchases.",
  "seo|geofencing|social-ads":
    "You're combining long-term organic growth with hyper-local paid targeting and lead-driven social ads — built to capture nearby customers right when they're ready to buy, while building lasting search authority.",
  "seo|geofencing|social-email":
    "You're building organic authority and local visibility together, backed by ongoing social content and email nurture — a steady, locally-focused plan that builds trust over time.",
  "aseo|google-ads|social-ads":
    "You're positioning for how customers search now with AI-driven optimization, backed by high-intent paid search and lead-focused social ads — fast, modern visibility across every channel.",
  "aseo|google-ads|social-email":
    "You're pairing next-gen search optimization with targeted paid search and consistent social and email presence — visible in new search behavior, and top of mind between purchases.",
  "aseo|geofencing|social-ads":
    "You're combining AI-driven search readiness with hyper-local targeting and lead-generating social ads — built to capture nearby, ready-to-buy customers through the newest search and ad channels.",
  "aseo|geofencing|social-email":
    "You're building visibility for how people search now, reaching nearby customers with geofencing, and staying present through ongoing content and email — a modern, locally-focused full-funnel plan.",
};

const DEFAULT_MESSAGE =
  "Pick one option from each category to see how your plan comes together.";

type PackageSummaryCardProps = {
  selections: Record<string, string>;
};

function getSummaryText(selections: Record<string, string>): string {
  const search = selections.search;
  const paid = selections.paid;
  const social = selections.social;

  if (!search || !paid || !social) {
    return DEFAULT_MESSAGE;
  }

  const key = `${search}|${paid}|${social}`;
  return SUMMARY_LOOKUP[key] ?? DEFAULT_MESSAGE;
}

export function PackageSummaryCard({ selections }: PackageSummaryCardProps) {
  const summaryText = useMemo(() => getSummaryText(selections), [selections]);
  const summaryKey = useMemo(() => {
    const search = selections.search ?? "";
    const paid = selections.paid ?? "";
    const social = selections.social ?? "";
    return `${search}|${paid}|${social}`;
  }, [selections]);

  return (
    <div className="package-summary-card" aria-live="polite">
      <p key={summaryKey} className="package-summary-text text-sm leading-relaxed text-fg2">
        {summaryText}
      </p>
    </div>
  );
}
