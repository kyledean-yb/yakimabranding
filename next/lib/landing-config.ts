export type LandingPainPoint = {
  title: string;
  description: string;
};

export type LandingSectionIntro = {
  eyebrow: string;
  headline: string;
  subheadline: string;
};

export type BenefitIconId = "hub" | "spend" | "team" | "results";

export type LandingBenefit = {
  title: string;
  description: string;
  icon: BenefitIconId;
};

export type LandingPricingOption = {
  id: string;
  label: string;
  description: string;
  pricePlaceholder: string;
};

export type ServiceCategoryIconId = "search" | "paid" | "social";

export type ServiceCategoryOption = {
  id: string;
  label: string;
  description: string;
};

export type ServiceCategory = {
  id: string;
  label: string;
  icon: ServiceCategoryIconId;
  options: ServiceCategoryOption[];
};

export type LandingLocalProof = {
  eyebrow: string;
  body: string;
  proofPoints: string[];
};

export type LandingPageConfig = {
  cityName: string;
  stateName: string;
  radiusMiles: number;
  mapImage: string;
  mapAlt: string;
  /** Google Maps embed URL (preferred over static mapImage when set). */
  mapEmbedUrl?: string;
  localHeadline: string;
  topBar: {
    offerText: string;
    marketLabel: string;
    trustLine: string;
  };
  ctaLabel: string;
  onboardingCtaLabel: string;
  needMoreInfoLabel: string;
  serviceSelectHeader: string;
  customPricingMessage: string;
  packagePricingLabel: string;
  packagePrice: string;
  pain: LandingSectionIntro & { points: LandingPainPoint[] };
  benefitsSection: LandingSectionIntro;
  benefits: LandingBenefit[];
  solutionSection: LandingSectionIntro;
  pricingPreviewIntro: string;
  pricingOptions: LandingPricingOption[];
  serviceCategories: ServiceCategory[];
  localProof: LandingLocalProof;
  finalCta: LandingSectionIntro;
  visualHint: string;
};

const customOption = {
  id: "custom",
  label: "I want Custom!",
  description: "Tell us what you need — we'll tailor a plan and pricing around your HVAC business.",
};

export const phoenixConfig: LandingPageConfig = {
  cityName: "Phoenix",
  stateName: "AZ",
  radiusMiles: 20,
  mapImage: "/placeholders/map-phoenix-az-radius-20mi.jpg",
  mapAlt: "Map of Scottsdale and Greater Phoenix, Arizona",
  mapEmbedUrl:
    "https://maps.google.com/maps?q=Scottsdale%2C%20AZ&hl=en&z=11&output=embed",
  localHeadline: "Serving HVAC Companies in the Greater Phoenix / Scottsdale area!",
  topBar: {
    offerText: "Get More Information",
    marketLabel: "Serving Phoenix & Scottsdale, AZ",
    trustLine: "509-901-9735 · All fields required",
  },
  ctaLabel: "Get More Information",
  onboardingCtaLabel: "Start Onboarding with YB",
  needMoreInfoLabel: "Need More info?",
  serviceSelectHeader: "Select Your Service in each Row",
  customPricingMessage: "Discover Your Solution and Pricing",
  packagePricingLabel: "HVAC Package Pricing",
  packagePrice: "$3,500 / month",
  pain: {
    eyebrow: "THE PROBLEM",
    headline: "More Leads for HVAC Companies, Spend Less Time!",
    subheadline:
      "Comprehensive marketing services and support for HVAC companies with > $1M in Sales and looking to grow. We can do it all for you.",
    points: [
      {
        title: "Deal with One Agency",
        description:
          "Stop juggling vendors for ads, SEO, and social. One HVAC-focused team owns the full plan — so nothing falls through the cracks.",
      },
      {
        title: "Consistent Branding and Communication",
        description:
          "Your trucks, ads, website, and follow-up emails should sound like the same company. We keep every touchpoint on-message.",
      },
      {
        title: "Single Dashboard Management",
        description:
          "See leads, spend, and channel performance in one place — not scattered reports from three different agencies.",
      },
    ],
  },
  benefitsSection: {
    eyebrow: "THE BENEFITS",
    headline: "What Changes When Marketing Works as One System",
    subheadline:
      "One team, one plan, one point of accountability — here's what that actually gets you.",
  },
  benefits: [
    {
      icon: "hub",
      title: "One Place for Branding, Ads, SEO, and Social",
      description:
        "Consistent messaging everywhere your customers find you — no more guessing which version of your brand they're seeing.",
    },
    {
      icon: "spend",
      title: "Spend That's Actually Working",
      description:
        "Every dollar tied to a channel, a campaign, and a result — so you know what's working before you spend more on what isn't.",
    },
    {
      icon: "team",
      title: "A Dedicated Strategy Team",
      description:
        "One point of contact who knows your business, not a rotating cast of account managers relearning it every quarter.",
    },
    {
      icon: "results",
      title: "Results You Can See",
      description:
        "Clear, regular reporting on what's moving — rankings, leads, and revenue — not a dashboard full of vanity metrics.",
    },
  ],
  solutionSection: {
    eyebrow: "THE SOLUTION",
    headline: "Full Service HVAC Marketing Solutions With Options",
    subheadline:
      "If you are managing individual parts of your >$1M HVAC Marketing services and happy with the results, our Standard Plan can be customized to suit your needs.",
  },
  pricingPreviewIntro:
    "One clear package for HVAC companies ready to grow — or choose Custom on any row for a tailored quote.",
  serviceCategories: [
    {
      id: "search",
      label: "Search Visibility",
      icon: "search",
      options: [
        {
          id: "seo",
          label: "SEO",
          description:
            "Long-term organic growth — rankings, content, and technical health built to compound over time.",
        },
        {
          id: "aseo",
          label: "ASEO",
          description:
            "AI-driven search optimization — positioning your business for how customers are starting to search now.",
        },
        customOption,
      ],
    },
    {
      id: "paid",
      label: "Paid Media",
      icon: "paid",
      options: [
        {
          id: "google-ads",
          label: "Google Ads Mgt",
          description:
            "Managed search and display campaigns built around your highest-intent keywords.",
        },
        {
          id: "geofencing",
          label: "Geofencing",
          description:
            "Hyper-local targeting that reaches customers the moment they're near your service area or a competitor's location.",
        },
        customOption,
      ],
    },
    {
      id: "social",
      label: "Social & Email",
      icon: "social",
      options: [
        {
          id: "social-ads",
          label: "Social Ads",
          description: "Paid campaigns built to drive leads, not just likes.",
        },
        {
          id: "social-email",
          label: "Social Media Mgt / Email",
          description:
            "Ongoing content, posting, and email nurture that keeps your brand top of mind between purchases.",
        },
        customOption,
      ],
    },
  ],
  pricingOptions: [
    {
      id: "hvac-package",
      label: "HVAC Package Pricing",
      description: "Full-service marketing package for growing HVAC companies.",
      pricePlaceholder: "$3,500 / month",
    },
  ],
  localProof: {
    eyebrow: "LOCAL PROOF",
    body: "We know the Greater Phoenix / Scottsdale HVAC market — the competitive landscape, seasonal demand, and what actually moves the needle for companies in this area.",
    proofPoints: [
      "Local market data folded into every strategy, not a generic national playbook.",
      "Direct experience managing full-service marketing for Phoenix-area service businesses.",
      "One team covering Greater Phoenix / Scottsdale — no city-by-city handoffs.",
    ],
  },
  finalCta: {
    eyebrow: "GET STARTED",
    headline: "Get More Information!",
    subheadline:
      "Tell us about your HVAC business and we'll put together a marketing plan built for Greater Phoenix / Scottsdale — one team, one strategy, more leads.",
  },
  visualHint: "Mouse over the diagram to see what can happen!",
};

export const triCitiesConfig: LandingPageConfig = {
  ...phoenixConfig,
  cityName: "Tri-Cities",
  stateName: "WA",
  mapImage: "/placeholders/map-tri-cities-wa-radius-20mi.jpg",
  mapAlt: "Tri-Cities, WA HVAC service area map",
  localHeadline: "Serving HVAC Companies in the Tri-Cities area!",
  topBar: {
    ...phoenixConfig.topBar,
    marketLabel: "Serving Tri-Cities, WA",
  },
  localProof: {
    eyebrow: "LOCAL PROOF",
    body: "We know the Tri-Cities HVAC market — the competitive landscape, seasonal demand, and what actually moves the needle for companies in this area.",
    proofPoints: [
      "Local market data folded into every strategy, not a generic national playbook.",
      "Direct experience managing full-service marketing for Tri-Cities-area service businesses.",
      "One team covering the Tri-Cities — no city-by-city handoffs.",
    ],
  },
  finalCta: {
    ...phoenixConfig.finalCta,
    subheadline:
      "Tell us about your HVAC business and we'll put together a marketing plan built for the Tri-Cities — one team, one strategy, more leads.",
  },
};
