import type { BenefitIconId } from "@/lib/landing-config";

const iconClass = "h-6 w-6 text-yb-blue";

export function BenefitIcon({ id }: { id: BenefitIconId }) {
  switch (id) {
    case "hub":
      return (
        <svg className={iconClass} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="3" />
          <circle cx="5" cy="7" r="2" />
          <circle cx="19" cy="7" r="2" />
          <circle cx="5" cy="17" r="2" />
          <circle cx="19" cy="17" r="2" />
          <line x1="9.5" y1="10" x2="6.8" y2="8.5" />
          <line x1="14.5" y1="10" x2="17.2" y2="8.5" />
          <line x1="9.5" y1="14" x2="6.8" y2="15.5" />
          <line x1="14.5" y1="14" x2="17.2" y2="15.5" />
        </svg>
      );
    case "spend":
      return (
        <svg className={iconClass} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="9" />
          <circle cx="12" cy="12" r="4" />
          <line x1="12" y1="3" x2="12" y2="7" />
          <line x1="12" y1="17" x2="12" y2="21" />
          <line x1="3" y1="12" x2="7" y2="12" />
          <line x1="17" y1="12" x2="21" y2="12" />
        </svg>
      );
    case "team":
      return (
        <svg className={iconClass} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M3 11v3a2 2 0 0 0 2 2h1" />
          <path d="M21 11v3a2 2 0 0 1-2 2h-1" />
          <path d="M7 11h10" />
          <path d="M12 11v6" />
          <path d="M9 7a3 3 0 1 1 6 0v4H9V7z" />
        </svg>
      );
    case "results":
      return (
        <svg className={iconClass} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <polyline points="4 16 9 11 13 15 20 8" />
          <polyline points="17 8 20 8 20 11" />
          <line x1="4" y1="20" x2="20" y2="20" />
        </svg>
      );
  }
}
