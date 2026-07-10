import Link from "next/link";
import { Container } from "@/components/ui/Container";

const CTA_HEADLINE = "Ready to elevate your brand?";
const CTA_BODY =
  "Let's discuss how our comprehensive solutions can transform your business and accelerate your growth.";
const CTA_BUTTON = "Start Your Project";

const arrowIcon = (
  <svg
    width="18"
    height="18"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2.5"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden
  >
    <line x1="5" y1="12" x2="19" y2="12" />
    <polyline points="12 5 19 12 12 19" />
  </svg>
);

type ElevateBrandCtaProps = {
  href?: string;
};

export function ElevateBrandCta({ href = "#final-cta" }: ElevateBrandCtaProps) {
  return (
    <section className="landing-elevate-cta-section py-16 md:py-20">
      <Container>
        <div className="landing-elevate-cta">
          <div className="landing-elevate-cta-mesh" aria-hidden="true" />
          <div className="landing-elevate-cta-copy">
            <h3>{CTA_HEADLINE}</h3>
            <p>{CTA_BODY}</p>
          </div>
          <Link href={href} className="btn btn-grad btn-lg landing-elevate-cta-btn">
            {CTA_BUTTON}
            {arrowIcon}
          </Link>
        </div>
      </Container>
    </section>
  );
}
