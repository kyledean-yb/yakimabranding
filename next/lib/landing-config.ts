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
  topBar: {
    offerText: string;
    marketLabel: string;
    trustLine: string;
  };
  ctaLabel: string;
  pain: LandingSectionIntro & { points: LandingPainPoint[] };
  benefitsSection: LandingSectionIntro;
  benefits: LandingBenefit[];
  solutionSection: LandingSectionIntro;
  pricingPreviewIntro: string;
  pricingOptions: LandingPricingOption[];
  serviceCategories: ServiceCategory[];
  localProof: LandingLocalProof;
  finalCta: LandingSectionIntro;
};

export const phoenixConfig: LandingPageConfig = {
  cityName: "Phoenix",
  stateName: "AZ",
  radiusMiles: 20,
  mapImage: "/placeholders/map-phoenix-az-radius-20mi.jpg",
  mapAlt: "Phoenix, AZ 20-mile service radius map — full-service marketing coverage area",
  topBar: {
    offerText: "Get Your Free Marketing Plan",
    marketLabel: "Serving Phoenix, AZ",
    trustLine: "509-901-9735 · Local Team",
  },
  ctaLabel: "Get My Free Marketing Plan",
  pain: {
    eyebrow: "THE PROBLEM",
    headline: "Your Marketing Shouldn't Feel This Scattered",
    subheadline:
      "Three vendors, three messages, one confused customer. If your branding, ads, and content don't feel like they're coming from the same company, they probably aren't.",
    points: [
      {
        title: "Nobody's Actually in Charge",
        description:
          "Different agencies handling ads, SEO, and social — each optimizing for their own piece, nobody owning the whole picture.",
      },
      {
        title: "Spend Without a Story",
        description:
          "Money is going out the door across channels, but there's no clear line from ad spend to actual leads.",
      },
      {
        title: "You're the Marketing Department",
        description:
          "Between running the business and chasing vendors for updates, marketing becomes the thing that gets squeezed to the bottom of the list.",
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
    headline: "Build Your Full-Service Marketing Package",
    subheadline: "Pick the channels you need. One accountable team runs the whole plan.",
  },
  pricingPreviewIntro:
    "Pricing is based on what you're currently doing — not a one-size-fits-all rate.",
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
      ],
    },
  ],
  pricingOptions: [
    {
      id: "starter",
      label: "Tier 1 — Getting Started",
      description: "For businesses doing some marketing already but lacking cohesion.",
      pricePlaceholder: "[$X,XXX/mo]",
    },
    {
      id: "growth",
      label: "Tier 2 — Growth Package",
      description: "For businesses ready to consolidate vendors into one plan.",
      pricePlaceholder: "[$X,XXX/mo]",
    },
    {
      id: "scale",
      label: "Tier 3 — Full Scale",
      description: "For businesses investing heavily across multiple channels.",
      pricePlaceholder: "[$X,XXX/mo]",
    },
  ],
  localProof: {
    eyebrow: "LOCAL PROOF",
    body: "We know the Phoenix market — the competitive landscape, the local search behavior, and what actually moves the needle for businesses in this area.",
    proofPoints: [
      "Local market data folded into every strategy, not a generic national playbook.",
      "Direct experience managing full-service marketing for Phoenix-area businesses.",
      "One team covering your full 20-mile service radius — no city-by-city handoffs.",
    ],
  },
  finalCta: {
    eyebrow: "GET STARTED",
    headline: "Get Your Free Marketing Plan",
    subheadline:
      "Tell us about your business and we'll put together a marketing plan built for Phoenix — one team, one strategy, no scattered vendors.",
  },
};

export const triCitiesConfig: LandingPageConfig = {
  ...phoenixConfig,
  cityName: "Tri-Cities",
  stateName: "WA",
  mapImage: "/placeholders/map-tri-cities-wa-radius-20mi.jpg",
  mapAlt: "Tri-Cities, WA 20-mile service radius map — full-service marketing coverage area",
  topBar: {
    ...phoenixConfig.topBar,
    marketLabel: "Serving Tri-Cities, WA",
  },
  localProof: {
    eyebrow: "LOCAL PROOF",
    body: `We know the Tri-Cities market — the competitive landscape, the local search behavior, and what actually moves the needle for businesses in this area.`,
    proofPoints: [
      "Local market data folded into every strategy, not a generic national playbook.",
      "Direct experience managing full-service marketing for Tri-Cities-area businesses.",
      "One team covering your full 20-mile service radius — no city-by-city handoffs.",
    ],
  },
  finalCta: {
    ...phoenixConfig.finalCta,
    subheadline:
      "Tell us about your business and we'll put together a marketing plan built for the Tri-Cities — one team, one strategy, no scattered vendors.",
  },
};
