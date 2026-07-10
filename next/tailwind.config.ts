import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        yb: {
          blue: "#3F6FD6",
          "blue-600": "#2F5AC0",
          navy: "#1B2A4A",
          cyan: "#2BC4F0",
          violet: "#7B5BE6",
          coral: "#FF6B57",
          amber: "#FFB23E",
          mint: "#25C28A",
          pink: "#FF5C9D",
        },
        ink: "#16203A",
        fg2: "#4A5673",
        fg3: "#7C879E",
        "fg2-on-dark": "#B8C4DE",
        "bg-soft": "#F6F8FC",
        line: "#E3E9F2",
        "line-strong": "#CFD8E8",
        wash: {
          blue: "#EDF2FD",
          cyan: "#E4F7FE",
          violet: "#F0ECFD",
          coral: "#FFEDE9",
          amber: "#FFF4E2",
          mint: "#E3F8F1",
          pink: "#FFEAF2",
        },
      },
      fontFamily: {
        display: ["var(--font-sora)", "system-ui", "sans-serif"],
        body: ["var(--font-jakarta)", "system-ui", "sans-serif"],
      },
      borderRadius: {
        sm: "10px",
        md: "16px",
        lg: "22px",
        xl: "32px",
        pill: "999px",
      },
      boxShadow: {
        sm: "0 2px 8px rgba(22,32,58,.07)",
        md: "0 10px 28px -8px rgba(22,32,58,.16)",
        lg: "0 24px 56px -16px rgba(22,32,58,.22)",
        blue: "0 14px 30px -10px rgba(63,111,214,.45)",
      },
      maxWidth: {
        container: "1200px",
      },
    },
  },
  plugins: [],
};

export default config;
