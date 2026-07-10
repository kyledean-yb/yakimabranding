import type { ReactNode } from "react";
import { siteLinks } from "@/lib/site-links";

export type NavService = {
  href: string;
  name: string;
  desc: string;
  wash: string;
  color: string;
  icon: ReactNode;
};

export const NAV_SERVICES: NavService[] = [
  {
    href: siteLinks.branding,
    name: "Branding & Design",
    desc: "Logos, systems & identity",
    wash: "var(--wash-violet)",
    color: "var(--yb-violet)",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="13.5" cy="6.5" r="0.5" fill="currentColor" />
        <circle cx="17.5" cy="10.5" r="0.5" fill="currentColor" />
        <circle cx="8.5" cy="7.5" r="0.5" fill="currentColor" />
        <circle cx="6.5" cy="12.5" r="0.5" fill="currentColor" />
        <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z" />
      </svg>
    ),
  },
  {
    href: siteLinks.webDesign,
    name: "Web Design",
    desc: "WordPress, Wix & custom sites",
    wash: "var(--wash-mint)",
    color: "#159468",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="3" width="18" height="18" rx="2" />
        <path d="M3 9h18" />
        <path d="M9 21V9" />
      </svg>
    ),
  },
  {
    href: siteLinks.socialMedia,
    name: "Social Media",
    desc: "Grow your following",
    wash: "var(--wash-amber)",
    color: "#c77f12",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="18" cy="5" r="3" />
        <circle cx="6" cy="12" r="3" />
        <circle cx="18" cy="19" r="3" />
      </svg>
    ),
  },
  {
    href: siteLinks.googleAds,
    name: "Google Ads",
    desc: "PPC that converts",
    wash: "var(--wash-coral)",
    color: "var(--yb-coral)",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="10" />
        <circle cx="12" cy="12" r="3" />
      </svg>
    ),
  },
  {
    href: siteLinks.seo,
    name: "SEO",
    desc: "Rank higher on Google",
    wash: "var(--wash-cyan)",
    color: "var(--yb-cyan)",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
    ),
  },
  {
    href: siteLinks.pressReleases,
    name: "Press Releases",
    desc: "Get published",
    wash: "var(--wash-pink)",
    color: "var(--yb-pink)",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2z" />
      </svg>
    ),
  },
  {
    href: siteLinks.contentMarketing,
    name: "Content & Blogging",
    desc: "Copy that converts",
    wash: "var(--wash-violet)",
    color: "var(--yb-violet)",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M12 20h9" />
        <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
      </svg>
    ),
  },
];
