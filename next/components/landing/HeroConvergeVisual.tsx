"use client";

import { useEffect, useRef } from "react";
import type { CSSProperties } from "react";

type BubbleId = "ads" | "brand" | "seo" | "social" | "email";

const BUBBLES: {
  id: BubbleId;
  label: string;
  color: string;
  wash: string;
  scatterTop: string;
  scatterLeft: string;
  driftDelay: string;
}[] = [
  { id: "ads", label: "Ads", color: "var(--yb-coral)", wash: "var(--wash-coral)", scatterTop: "4%", scatterLeft: "2%", driftDelay: "0s" },
  { id: "brand", label: "Brand", color: "var(--yb-violet)", wash: "var(--wash-violet)", scatterTop: "2%", scatterLeft: "54%", driftDelay: "-0.8s" },
  { id: "seo", label: "SEO", color: "var(--yb-cyan)", wash: "var(--wash-cyan)", scatterTop: "52%", scatterLeft: "2%", driftDelay: "-1.6s" },
  { id: "social", label: "Social", color: "var(--yb-amber)", wash: "var(--wash-amber)", scatterTop: "58%", scatterLeft: "48%", driftDelay: "-2.2s" },
  { id: "email", label: "Email", color: "var(--yb-mint)", wash: "var(--wash-mint)", scatterTop: "18%", scatterLeft: "30%", driftDelay: "-1.1s" },
];

function BubbleIcon({ id }: { id: BubbleId }) {
  const props = {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 2,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    "aria-hidden": true,
  };

  switch (id) {
    case "ads":
      return (
        <svg {...props}>
          <circle cx="12" cy="12" r="10" />
          <circle cx="12" cy="12" r="3" />
        </svg>
      );
    case "brand":
      return (
        <svg {...props}>
          <circle cx="13.5" cy="6.5" r="0.5" fill="currentColor" stroke="none" />
          <circle cx="17.5" cy="10.5" r="0.5" fill="currentColor" stroke="none" />
          <circle cx="8.5" cy="7.5" r="0.5" fill="currentColor" stroke="none" />
          <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z" />
        </svg>
      );
    case "seo":
      return (
        <svg {...props}>
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      );
    case "social":
      return (
        <svg {...props}>
          <circle cx="18" cy="5" r="3" />
          <circle cx="6" cy="12" r="3" />
          <circle cx="18" cy="19" r="3" />
        </svg>
      );
    case "email":
      return (
        <svg {...props}>
          <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
          <polyline points="22,6 12,13 2,6" />
        </svg>
      );
  }
}

function BubbleCard({
  id,
  label,
  color,
  wash,
  orbit = false,
}: {
  id: BubbleId;
  label: string;
  color: string;
  wash: string;
  orbit?: boolean;
}) {
  return (
    <div className={`hero-converge-bubble-card${orbit ? " hero-converge-bubble-card--orbit" : ""}`}>
      <span className="hero-converge-bubble-dot" style={{ background: wash, color }}>
        <BubbleIcon id={id} />
      </span>
      <span className="hero-converge-bubble-label">{label}</span>
    </div>
  );
}

function OrbitNode({
  bubble,
  index,
}: {
  bubble: (typeof BUBBLES)[number];
  index: number;
}) {
  return (
    <div className="hero-converge-node" style={{ "--i": index } as CSSProperties}>
      <div className="hero-converge-bubble-anchor">
        <div className="hero-converge-bubble-counter-static">
          <div className="hero-converge-bubble-counter-spin">
            <BubbleCard id={bubble.id} label={bubble.label} color={bubble.color} wash={bubble.wash} orbit />
          </div>
        </div>
      </div>
    </div>
  );
}

export function HeroConvergeVisual() {
  const convergeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const converge = convergeRef.current;
    if (!converge) return;

    let ticking = false;
    let connected = false;

    const update = () => {
      const scrollTop = window.scrollY;
      const shouldConnect = scrollTop > 32;
      if (shouldConnect !== connected) {
        connected = shouldConnect;
        converge.classList.toggle("hero-converge--connected", connected);
      }
      ticking = false;
    };

    const onScroll = () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    };

    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <div className="hero-visual">
      <div
        ref={convergeRef}
        className="hero-converge"
        tabIndex={0}
        role="img"
        aria-label="Scattered marketing channels that connect into one YB Marketing team"
      >
        <div className="hero-converge-ring" aria-hidden="true" />

        <div className="hero-converge-hub" aria-hidden="true">
          <div className="hero-converge-hub-mesh" />
          <img className="hero-converge-hub-logo" src="/yb-logo-white.png" alt="" />
        </div>

        <div className="hero-converge-scatter" aria-hidden="true">
          {BUBBLES.map((bubble) => (
            <div
              key={bubble.id}
              className="hero-converge-scatter-item"
              style={{
                top: bubble.scatterTop,
                left: bubble.scatterLeft,
                animationDelay: bubble.driftDelay,
              }}
            >
              <BubbleCard id={bubble.id} label={bubble.label} color={bubble.color} wash={bubble.wash} />
            </div>
          ))}
        </div>

        <div className="hero-converge-orbit" style={{ "--orbit-n": BUBBLES.length } as CSSProperties}>
          <div className="hero-converge-orbit-spin">
            <svg className="hero-converge-connectors" viewBox="0 0 460 460" aria-hidden="true">
              {BUBBLES.map((_, i) => {
                const angle = (i * 360) / BUBBLES.length - 90;
                const rad = (angle * Math.PI) / 180;
                const cx = 230;
                const cy = 230;
                const r = 148;
                const x2 = cx + Math.cos(rad) * r;
                const y2 = cy + Math.sin(rad) * r;
                return (
                  <line
                    key={i}
                    x1={cx}
                    y1={cy}
                    x2={x2}
                    y2={y2}
                    stroke="var(--yb-blue)"
                    strokeWidth="1.5"
                    strokeOpacity="0.35"
                  />
                );
              })}
            </svg>
            {BUBBLES.map((bubble, i) => (
              <OrbitNode key={bubble.id} bubble={bubble} index={i} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
