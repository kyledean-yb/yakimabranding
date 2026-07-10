"use client";

import { GOOGLE_RATING, GOOGLE_REVIEW_COUNT, GOOGLE_REVIEWS, type Review } from "@/lib/reviews";
import { Eyebrow } from "@/components/ui/Eyebrow";

function StarRow({ size = 15 }: { size?: number }) {
  return (
    <div className="flex gap-0.5 text-yb-amber" style={{ marginBottom: 12 }}>
      {Array.from({ length: 5 }).map((_, i) => (
        <svg key={i} style={{ width: size, height: size }} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
        </svg>
      ))}
    </div>
  );
}

function ReviewCard({ review }: { review: Review }) {
  return (
    <div className="rv-scroll-card">
      <StarRow />
      <p className="rv-scroll-quote">&ldquo;{review.quote}&rdquo;</p>
      <div className="rv-scroll-footer">
        <div className="flex items-center gap-2.5">
          <div className="rv-scroll-avatar" style={{ background: review.avatarBackground }}>
            {review.initials}
          </div>
          <span className="text-[13px] font-bold text-ink">{review.name}</span>
        </div>
        <span className="rv-scroll-source">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
          Google
        </span>
      </div>
    </div>
  );
}

function ReviewSet({ reviews, ariaHidden }: { reviews: Review[]; ariaHidden?: boolean }) {
  return (
    <div className="reviews-scroll-set" aria-hidden={ariaHidden}>
      {reviews.map((review) => (
        <ReviewCard key={`${review.name}-${review.initials}`} review={review} />
      ))}
    </div>
  );
}

export function ReviewsSection() {
  return (
    <section className="reviews-bg overflow-hidden pb-0 pt-16 md:pt-[88px]">
      <div className="container mx-auto mb-10 max-w-container px-7">
        <div className="mx-auto max-w-[640px] text-center">
          <Eyebrow className="justify-center text-yb-coral before:bg-yb-coral">Client Love</Eyebrow>
          <h2 className="yb-h2 mt-3.5 mb-4">What Our Clients Say</h2>
          <div className="reviews-rating-pill">
            <StarRow size={18} />
            <span className="text-base font-extrabold text-ink">{GOOGLE_RATING}</span>
            <span className="text-[13px] font-semibold text-fg3">· {GOOGLE_REVIEW_COUNT} Google Reviews</span>
          </div>
        </div>
      </div>
      <div className="overflow-hidden pb-16 md:pb-[88px]">
        <div className="reviews-scroll-track">
          <ReviewSet reviews={GOOGLE_REVIEWS} />
          <ReviewSet reviews={GOOGLE_REVIEWS} ariaHidden />
        </div>
      </div>
    </section>
  );
}
