import Link from "next/link";
import type { ReactNode } from "react";

type ButtonProps = {
  children: ReactNode;
  href?: string;
  type?: "button" | "submit";
  className?: string;
  size?: "default" | "lg";
  onClick?: () => void;
};

export function Button({
  children,
  href,
  type = "button",
  className = "",
  size = "default",
  onClick,
}: ButtonProps) {
  const styles = ["btn", "btn-grad", size === "lg" ? "btn-lg" : "", className]
    .filter(Boolean)
    .join(" ");

  if (href) {
    return (
      <Link href={href} className={styles}>
        {children}
      </Link>
    );
  }

  return (
    <button type={type} onClick={onClick} className={styles}>
      {children}
    </button>
  );
}
