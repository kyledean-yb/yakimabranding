"use client";

import { useMemo, useState } from "react";
import { BenefitsSection } from "@/components/landing/BenefitsSection";
import { ElevateBrandCta } from "@/components/landing/ElevateBrandCta";
import { HeroConvergeVisual } from "@/components/landing/HeroConvergeVisual";
import { LeadCaptureForm } from "@/components/landing/LeadCaptureForm";
import { PackageSummaryCard } from "@/components/landing/PackageSummaryCard";
import { ReviewsSection } from "@/components/landing/ReviewsSection";
import { ServiceCategoryIcon } from "@/components/landing/ServiceCategoryIcon";
import { StickyLeadBar } from "@/components/landing/StickyLeadBar";
import { SiteFooter } from "@/components/layout/SiteFooter";
import { SiteHeader } from "@/components/layout/SiteHeader";
import { Button } from "@/components/ui/Button";
import { Container } from "@/components/ui/Container";
import { Eyebrow } from "@/components/ui/Eyebrow";
import type { LandingPageConfig } from "@/lib/landing-config";

type MarketingLandingPageProps = {
  config: LandingPageConfig;
};

export function MarketingLandingPage({ config }: MarketingLandingPageProps) {
  const [selections, setSelections] = useState<Record<string, string>>(() =>
    Object.fromEntries(
      config.serviceCategories.map((category) => [
        category.id,
        category.options[0]?.id ?? "",
      ]),
    ),
  );

  const hasCustomSelection = useMemo(
    () => Object.values(selections).some((value) => value === "custom"),
    [selections],
  );

  return (
    <>
      <div className="landing-top-chrome">
        <SiteHeader />

        <StickyLeadBar
          ctaLabel={config.ctaLabel}
          offerText={config.topBar.offerText}
          trustLine={config.topBar.trustLine}
        />
      </div>

      <main>
        <section className="hero" id="top">
          <div className="hero-mesh" />
          <div className="hero-logo-overlay hero-logo-overlay--light hero-logo-overlay--left" aria-hidden="true">
            <img src="/yb-logo-color.png" alt="" />
          </div>
          <Container>
            <div className="hero-head-row">
              <div>
                <Eyebrow className="mb-4">{config.pain.eyebrow}</Eyebrow>
                <h1 className="yb-display mb-5 text-[clamp(2rem,4vw,3.25rem)]">{config.pain.headline}</h1>
                <p className="yb-lead hero-lead mb-8">{config.pain.subheadline}</p>
                <Button href="#top-cta" size="lg">
                  {config.ctaLabel}
                </Button>
              </div>
              <div className="hero-visual-col">
                <HeroConvergeVisual />
                <p className="hero-visual-hint">{config.visualHint}</p>
              </div>
            </div>

            <div className="hero-pain-grid">
              {config.pain.points.map((point, index) => (
                <article key={point.title} className="hero-pain-card">
                  <div className="mb-2 flex items-center gap-2.5">
                    <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-wash-coral font-display text-xs font-bold text-yb-coral">
                      {index + 1}
                    </span>
                    <h2>{point.title}</h2>
                  </div>
                  <p>{point.description}</p>
                </article>
              ))}
            </div>
          </Container>
          <div className="hero-wave" aria-hidden="true">
            <svg viewBox="0 0 1440 60" preserveAspectRatio="none">
              <path d="M0,0 C360,60 1080,60 1440,0 L1440,60 L0,60 Z" fill="#F6F8FC" />
            </svg>
          </div>
        </section>

        <BenefitsSection section={config.benefitsSection} benefits={config.benefits} />

        <section id="solution" className="py-16 md:py-20">
          <Container>
            <div className="mx-auto mb-10 max-w-2xl text-center">
              <Eyebrow className="mb-3 justify-center">{config.solutionSection.eyebrow}</Eyebrow>
              <h2 className="yb-h2">{config.solutionSection.headline}</h2>
              <p className="mt-3 yb-lead">{config.solutionSection.subheadline}</p>
            </div>

            <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
              <div className="grid gap-5">
                <p className="service-select-header">{config.serviceSelectHeader}</p>
                {config.serviceCategories.map((category) => (
                  <div key={category.id} className="yb-card">
                    <h3 className="mb-4 flex items-center gap-2.5 font-display text-lg font-bold text-ink">
                      <ServiceCategoryIcon id={category.icon} />
                      {category.label}
                    </h3>
                    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
                      {category.options.map((option) => {
                        const active = selections[category.id] === option.id;
                        return (
                          <button
                            key={option.id}
                            type="button"
                            onClick={() =>
                              setSelections((prev) => ({
                                ...prev,
                                [category.id]: option.id,
                              }))
                            }
                            className={`rounded-md border px-4 py-3 text-left transition ${
                              active
                                ? "border-yb-blue bg-wash-blue shadow-sm"
                                : "border-line bg-white hover:border-line-strong"
                            }`}
                          >
                            <span className={`block text-sm font-semibold ${active ? "text-yb-blue" : "text-ink"}`}>
                              {option.label}
                            </span>
                            <span className="mt-1 block text-xs leading-relaxed text-fg2">{option.description}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>

              <aside className="flex flex-col gap-4">
                {!hasCustomSelection ? <PackageSummaryCard selections={selections} /> : null}
                <div className="yb-card h-fit">
                  <h3 className="mb-2 font-display text-lg font-bold text-ink">Pricing Preview</h3>
                  <p className="mb-5 text-sm text-fg2">{config.pricingPreviewIntro}</p>

                  {hasCustomSelection ? (
                    <div className="rounded-md border border-yb-blue bg-wash-blue p-5 text-center">
                      <p className="font-display text-lg font-bold text-ink">{config.customPricingMessage}</p>
                      <p className="mt-2 text-sm text-fg2">
                        You selected a custom option — we&apos;ll build a tailored HVAC plan and quote for you.
                      </p>
                    </div>
                  ) : (
                    <div className="rounded-md border border-yb-blue bg-wash-blue p-5">
                      <div className="mb-1 flex flex-wrap items-center justify-between gap-3">
                        <h4 className="font-display text-base font-bold text-ink">{config.packagePricingLabel}</h4>
                        <span className="text-lg font-bold text-yb-blue">{config.packagePrice}</span>
                      </div>
                      <p className="text-xs leading-relaxed text-fg2">
                        {config.pricingOptions[0]?.description}
                      </p>
                    </div>
                  )}

                  <Button href="#final-cta" className="mt-5 w-full justify-center">
                    {config.onboardingCtaLabel}
                  </Button>
                  <a href="#top-cta" className="need-more-info-link">
                    {config.needMoreInfoLabel}
                  </a>
                </div>
              </aside>
            </div>
          </Container>
        </section>

        <section className="bg-bg-soft py-16 md:py-20">
          <Container>
            <div className="grid items-center gap-8 lg:grid-cols-2">
              <div>
                <Eyebrow className="mb-3">{config.localProof.eyebrow}</Eyebrow>
                <h2 className="yb-h2 mb-4">{config.localHeadline}</h2>
                <p className="yb-lead mb-4">{config.localProof.body}</p>
                <ul className="grid gap-2 text-sm text-fg2">
                  {config.localProof.proofPoints.map((point) => (
                    <li key={point}>• {point}</li>
                  ))}
                </ul>
              </div>
              <div className="landing-map-wrap">
                <img
                  src={config.mapImage}
                  alt={config.mapAlt}
                  className="landing-map-img"
                  onError={(e) => {
                    const img = e.currentTarget;
                    img.style.display = "none";
                    img.nextElementSibling?.classList.remove("hidden");
                  }}
                />
                <div className="landing-map-fallback hidden" role="img" aria-label={config.mapAlt}>
                  <span>Static map — Greater Phoenix / Scottsdale</span>
                  <p className="mt-2 text-xs font-normal text-fg3">Add map asset: {config.mapImage}</p>
                </div>
              </div>
            </div>
          </Container>
        </section>

        <ReviewsSection />

        <ElevateBrandCta />

        <section id="final-cta" className="bg-[var(--grad-navy)] py-16 text-white md:py-20">
          <Container>
            <div className="mx-auto max-w-3xl text-center">
              <Eyebrow className="mb-3 justify-center text-yb-cyan before:bg-yb-cyan">{config.finalCta.eyebrow}</Eyebrow>
              <h2 className="mb-4 font-display text-[clamp(1.75rem,3vw,2.5rem)] font-bold leading-tight">
                {config.finalCta.headline}
              </h2>
              <p className="mx-auto mb-8 max-w-2xl text-fg2-on-dark">{config.finalCta.subheadline}</p>
            </div>
            <div className="mx-auto max-w-4xl rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm md:p-8">
              <LeadCaptureForm ctaLabel={config.ctaLabel} />
            </div>
          </Container>
        </section>
      </main>

      <SiteFooter />
    </>
  );
}
