import type { Metadata } from "next";
import { MarketingLandingPage } from "@/components/landing/MarketingLandingPage";
import { phoenixConfig } from "@/lib/landing-config";

/**
 * /landing-page — wireframe landing page (Phoenix default market).
 *
 * To localize for another city/vertical, swap `phoenixConfig` with
 * `triCitiesConfig` or a new config object in lib/landing-config.ts.
 */
export const metadata: Metadata = {
  title: "HVAC Marketing for Phoenix & Scottsdale | YB Marketing | 509-901-9735",
  description:
    "More leads for HVAC companies with >$1M in sales. Full-service marketing for Greater Phoenix / Scottsdale — one agency, one plan. Call 509-901-9735.",
};

export default function LandingPage() {
  return <MarketingLandingPage config={phoenixConfig} />;
}
