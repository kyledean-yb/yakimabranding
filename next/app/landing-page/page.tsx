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
  title: "YB Marketing | 509-901-9735",
  description:
    "Full-spectrum branding and digital marketing for growing businesses. Call 509-901-9735 to get started.",
};

export default function LandingPage() {
  return <MarketingLandingPage config={phoenixConfig} />;
}
