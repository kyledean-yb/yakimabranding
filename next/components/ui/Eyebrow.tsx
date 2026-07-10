import type { ReactNode } from "react";

type EyebrowProps = {
  children: ReactNode;
  className?: string;
};

export function Eyebrow({ children, className = "" }: EyebrowProps) {
  return <span className={`yb-eyebrow ${className}`}>{children}</span>;
}
