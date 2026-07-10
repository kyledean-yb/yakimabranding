"use client";

import type { CSSProperties } from "react";
import { BenefitIcon } from "@/components/landing/BenefitIcon";
import { Container } from "@/components/ui/Container";
import { Eyebrow } from "@/components/ui/Eyebrow";
import type { LandingBenefit, LandingSectionIntro } from "@/lib/landing-config";

type BenefitsSectionProps = {
  section: LandingSectionIntro;
  benefits: LandingBenefit[];
};

export function BenefitsSection({ section, benefits }: BenefitsSectionProps) {
  return (
    <section className="bg-bg-soft py-16 md:py-20">
      <Container>
        <div className="mx-auto mb-10 max-w-2xl text-center">
          <Eyebrow className="mb-3 justify-center">{section.eyebrow}</Eyebrow>
          <h2 className="yb-h2">{section.headline}</h2>
          <p className="mt-3 yb-lead">{section.subheadline}</p>
        </div>

        <div className="benefits-flow">
          <svg className="benefits-flow-svg" viewBox="0 0 1000 48" preserveAspectRatio="none" aria-hidden="true">
            <line x1="125" y1="24" x2="875" y2="24" className="benefits-flow-track" />
            <line x1="125" y1="24" x2="875" y2="24" className="benefits-flow-animated" />
            {benefits.map((_, i) => {
              const x = 125 + i * 250;
              return <circle key={i} cx={x} cy="24" r="5" className="benefits-flow-node" />;
            })}
          </svg>

          <div className="benefits-flow-grid">
            {benefits.map((benefit, index) => (
              <article
                key={benefit.title}
                className="benefits-flow-card yb-card"
                style={{ "--benefit-i": index } as CSSProperties}
              >
                <div className="benefits-flow-icon">
                  <BenefitIcon id={benefit.icon} />
                </div>
                <h3 className="mb-2 font-display text-lg font-bold text-ink">{benefit.title}</h3>
                <p className="text-sm leading-relaxed text-fg2">{benefit.description}</p>
              </article>
            ))}
          </div>
        </div>
      </Container>
    </section>
  );
}
