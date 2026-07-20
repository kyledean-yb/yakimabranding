import type { Metadata } from "next";
import { MarketingLandingPage } from "@/components/landing/MarketingLandingPage";
import { phoenixConfig } from "@/lib/landing-config";

/**
 * /phx-hvac — HVAC marketing page for Phoenix / Scottsdale.
 *
 * To localize for another city/vertical, swap `phoenixConfig` with
 * `triCitiesConfig` or a new config object in lib/landing-config.ts.
 */
export const metadata: Metadata = {
  title: "HVAC Marketing for Phoenix & Scottsdale | YB Marketing | 509-901-9735",
  description:
    "YB Marketing delivers full-service marketing for HVAC companies with >$1M in sales across Greater Phoenix and Scottsdale — SEO, ads, social, and more under one plan. Call 509-901-9735.",
  icons: {
    icon: "/favicon.png",
    apple: "/favicon.png",
  },
};

export default function LandingPage() {
  return <MarketingLandingPage config={phoenixConfig} />;
}
