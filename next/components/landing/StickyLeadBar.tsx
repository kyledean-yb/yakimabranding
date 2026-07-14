import { LeadCaptureForm } from "@/components/landing/LeadCaptureForm";
import { Container } from "@/components/ui/Container";

type StickyLeadBarProps = {
  ctaLabel: string;
  offerText: string;
  trustLine: string;
};

export function StickyLeadBar({ ctaLabel, offerText, trustLine }: StickyLeadBarProps) {
  return (
    <div id="top-cta" className="sticky-lead-bar sticky-lead-bar--bold border-b border-yb-blue/20 shadow-sm">
      <Container>
        <p className="mb-2 font-display text-sm font-bold text-white md:text-base">{offerText}</p>
        <LeadCaptureForm ctaLabel={ctaLabel} compact trustLine={trustLine} />
      </Container>
    </div>
  );
}
