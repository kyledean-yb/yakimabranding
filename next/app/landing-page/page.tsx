import { MarketingLandingPage } from "@/components/landing/MarketingLandingPage";
import { phoenixConfig } from "@/lib/landing-config";

/**
 * /landing-page — wireframe landing page (Phoenix default market).
 *
 * To localize for another city/vertical, swap `phoenixConfig` with
 * `triCitiesConfig` or a new config object in lib/landing-config.ts.
 */
export default function LandingPage() {
  return <MarketingLandingPage config={phoenixConfig} />;
}
