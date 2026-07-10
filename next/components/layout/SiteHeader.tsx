"use client";

import { useState } from "react";
import { useSiteNav } from "@/hooks/useSiteNav";
import { NAV_SERVICES } from "@/lib/nav-services";
import { siteLinks } from "@/lib/site-links";

const phoneIcon = (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round">
    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z" />
  </svg>
);

const chevronIcon = (
  <svg className="nav-chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
    <polyline points="6 9 12 15 18 9" />
  </svg>
);

export function SiteHeader() {
  useSiteNav();
  const [mobileAboutOpen, setMobileAboutOpen] = useState(false);

  return (
    <div className="header top" id="header">
      <div className="container header-inner">
        <a className="logo" href={siteLinks.home}>
          <img src="/yb-logo-color.png" alt="YB Marketing logo" style={{ width: 44, height: 44 }} />
          <span className="logo-text">
            YB <span>Marketing</span>
          </span>
        </a>

        <nav className="nav">
          <a href={siteLinks.home} className="nav-a">
            Home
          </a>

          <div className="nav-about" id="navAbout">
            <button className="nav-svc-btn" type="button">
              About
              {chevronIcon}
            </button>
            <div className="nav-dd nav-dd-about">
              <div className="nav-dd-arrow" />
              <div className="nav-dd-about-inner">
                <div className="nav-dd-about-banner">
                  <span className="nav-dd-eyebrow">About YB Marketing</span>
                  <p className="nav-dd-banner-text">Pacific Northwest agency · Washington State</p>
                </div>
                <div className="nav-dd-about-grid">
                  <a href={siteLinks.about} className="dd-card">
                    <div className="dd-ic" style={{ background: "var(--wash-blue)", color: "var(--yb-blue)" }}>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                        <circle cx="9" cy="7" r="4" />
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                      </svg>
                    </div>
                    <div>
                      <span className="dd-name">About Us</span>
                      <span className="dd-desc">Meet our team &amp; our story</span>
                    </div>
                  </a>
                  <a href={siteLinks.caseStudies} className="dd-card">
                    <div className="dd-ic" style={{ background: "var(--wash-violet)", color: "var(--yb-violet)" }}>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
                        <line x1="8" y1="7" x2="16" y2="7" />
                        <line x1="8" y1="11" x2="14" y2="11" />
                      </svg>
                    </div>
                    <div>
                      <span className="dd-name">Case Studies</span>
                      <span className="dd-desc">Client results &amp; project highlights</span>
                    </div>
                  </a>
                  <a href={siteLinks.waTax} className="dd-card">
                    <div className="dd-ic" style={{ background: "#e8f5ee", color: "#2d9a5a" }}>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                        <polyline points="14 2 14 8 20 8" />
                        <line x1="16" y1="13" x2="8" y2="13" />
                        <line x1="16" y1="17" x2="8" y2="17" />
                      </svg>
                    </div>
                    <div>
                      <span className="dd-name">WA Sales Tax Notice</span>
                      <span className="dd-desc">Oct 2025 advertising &amp; software tax info</span>
                    </div>
                  </a>
                </div>
              </div>
            </div>
          </div>

          <div className="nav-services" id="navServices">
            <button className="nav-svc-btn" type="button">
              Services
              {chevronIcon}
            </button>
            <div className="nav-dd">
              <div className="nav-dd-arrow" />
              <div className="nav-dd-grid">
                {NAV_SERVICES.map((service) => (
                  <a key={service.href} href={service.href} className="dd-card">
                    <div className="dd-ic" style={{ background: service.wash, color: service.color }}>
                      {service.icon}
                    </div>
                    <div>
                      <span className="dd-name">{service.name}</span>
                      <span className="dd-desc">{service.desc}</span>
                    </div>
                  </a>
                ))}
              </div>
            </div>
          </div>

          <a href={siteLinks.insights} className="nav-a">
            Insights
          </a>
          <a href={siteLinks.contact} className="nav-a">
            Contact
          </a>
        </nav>

        <div className="btn-hdr" style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <a href={siteLinks.phone} className="btn btn-hdr-phone">
            {phoneIcon}
            509-901-9735
          </a>
          <a href={siteLinks.contact} className="btn btn-grad">
            Get Started
          </a>
        </div>

        <button className="hamburger" id="hamburger" type="button" aria-label="Open menu">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round">
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>
      </div>

      <div className="mobile-menu" id="mobileMenu">
        <a href={siteLinks.home}>Home</a>
        <a
          href="#"
          onClick={(e) => {
            e.preventDefault();
            setMobileAboutOpen((open) => !open);
          }}
          style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}
        >
          About <span>▾</span>
        </a>
        <div className={`mobile-svc-list${mobileAboutOpen ? " open" : ""}`} id="mobileAboutList">
          <a href={siteLinks.about} className="mobile-about-row">
            <strong>About Us</strong>
            <span>Meet our team &amp; our story</span>
          </a>
          <a href={siteLinks.caseStudies} className="mobile-about-row">
            <strong>Case Studies</strong>
            <span>Client results &amp; project highlights</span>
          </a>
          <a href={siteLinks.waTax} className="mobile-about-row">
            <strong>WA Sales Tax Notice</strong>
            <span>Oct 2025 tax updates</span>
          </a>
        </div>
        <a href={siteLinks.insights}>Insights</a>
        <a href={siteLinks.contact}>Contact</a>
      </div>
    </div>
  );
}
