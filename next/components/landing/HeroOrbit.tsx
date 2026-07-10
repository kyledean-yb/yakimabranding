"use client";

import type { CSSProperties } from "react";
import Script from "next/script";
import { siteLinks } from "@/lib/site-links";

const ORBIT_SERVICES = [
  {
    href: siteLinks.webDesign,
    label: "Web Design",
    wash: "var(--wash-mint)",
    color: "#159468",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" />
        <path d="M3 9h18" />
        <path d="M9 21V9" />
      </svg>
    ),
  },
  {
    href: siteLinks.seo,
    label: "SEO",
    wash: "var(--wash-cyan)",
    color: "var(--yb-cyan)",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
    ),
  },
  {
    href: siteLinks.googleAds,
    label: "Google Ads",
    wash: "var(--wash-coral)",
    color: "var(--yb-coral)",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <circle cx="12" cy="12" r="3" />
      </svg>
    ),
  },
  {
    href: siteLinks.socialMedia,
    label: "Social Media",
    wash: "var(--wash-amber)",
    color: "#c77f12",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="18" cy="5" r="3" />
        <circle cx="6" cy="12" r="3" />
        <circle cx="18" cy="19" r="3" />
        <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
        <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
      </svg>
    ),
  },
  {
    href: siteLinks.pressReleases,
    label: "Press Releases",
    wash: "var(--wash-blue)",
    color: "var(--yb-blue)",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
      </svg>
    ),
  },
  {
    href: siteLinks.contentMarketing,
    label: "Content & Blogging",
    wash: "var(--wash-pink)",
    color: "var(--yb-pink)",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="18" y1="2" x2="22" y2="6" />
        <path d="M7.5 20.5 19 9l-4-4L3.5 16.5 2 22z" />
      </svg>
    ),
  },
  {
    href: siteLinks.branding,
    label: "Branding & Design",
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
] as const;

export function HeroOrbit() {
  return (
    <>
      <div className="hero-visual">
        <div className="hero-orbit hero-orbit--pause-hover">
          <div className="hero-orbit-bg" aria-hidden="true">
            <div className="hero-orbit-ring hero-orbit-ring--track" />
            <div className="hero-orbit-hub">
              <div className="hero-orbit-hub-mesh" />
              <img className="hero-orbit-hub-logo" src="/yb-logo-white.png" alt="YB Marketing" />
            </div>
          </div>
          <div className="hero-orbit-spin">
            {ORBIT_SERVICES.map((service, index) => (
              <div key={service.href} className="hero-orbit-node" style={{ "--i": index } as CSSProperties}>
                <a href={service.href} className="hero-orbit-icon" aria-label={service.label}>
                  <span className="hero-orbit-pill">
                    <span className="hero-orbit-pill-ic" style={{ background: service.wash, color: service.color }}>
                      {service.icon}
                    </span>
                    <span className="hero-orbit-pill-label">{service.label}</span>
                  </span>
                </a>
              </div>
            ))}
          </div>
        </div>
      </div>
      <Script src="/js/hero-orbit.js" strategy="afterInteractive" />
    </>
  );
}
