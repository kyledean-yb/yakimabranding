import { LeadCaptureForm } from "@/components/landing/LeadCaptureForm";
import { Container } from "@/components/ui/Container";

type StickyLeadBarProps = {
  ctaLabel: string;
  offerText: string;
  trustLine: string;
};

export function StickyLeadBar({ ctaLabel, offerText, trustLine }: StickyLeadBarProps) {
  return (
    <div id="top-cta" className="sticky-lead-bar border-b border-line bg-white/95 shadow-sm backdrop-blur-md">
      <Container>
        <p className="mb-2 font-display text-sm font-bold text-ink md:text-base">{offerText}</p>
        <LeadCaptureForm ctaLabel={ctaLabel} compact trustLine={trustLine} />
      </Container>
    </div>
  );
}
