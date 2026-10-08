import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        warm: {
          bg: "#f7f6f3",
          card: "#fdfcfb",
          sunken: "#f1efeb",
          hover: "#ebe8e3",
          primary: "#0f0f0e",
          body: "#3f3d3a",
          secondary: "#6b6660",
          muted: "#8a847d",
          border: "#e7e3dd",
          borderHover: "#d6d1c9",
          inverse: "#fdfcfb",
        },
        accent: {
          indigo: "#6366f1",
          violet: "#8b5cf6",
          cyan: "#0891b2",
          emerald: "#059669",
          amber: "#d97706",
          rose: "#e11d48",
        },
        category: {
          politics: { text: "#e11d48", bg: "#fff1f2", border: "#fecdd3" },
          sports: { text: "#059669", bg: "#ecfdf5", border: "#a7f3d0" },
          technology: { text: "#0891b2", bg: "#ecfeff", border: "#a5f3fc" },
          business: { text: "#d97706", bg: "#fffbeb", border: "#fde68a" },
          entertainment: { text: "#db2777", bg: "#fdf2f8", border: "#fbcfe8" },
          health: { text: "#65a30d", bg: "#f7fee7", border: "#d9f99d" },
        },
      },
      boxShadow: {
        sm: "0 1px 2px rgba(28, 27, 26, 0.04)",
        md: "0 4px 12px rgba(28, 27, 26, 0.06)",
        lg: "0 12px 32px rgba(28, 27, 26, 0.08)",
        xl: "0 24px 48px rgba(28, 27, 26, 0.10)",
        cta: "0 4px 12px rgba(99, 102, 241, 0.25)",
      },
      borderRadius: {
        lg: "0.75rem",
        xl: "1rem",
        "2xl": "1.25rem",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "-apple-system", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"],
        heading: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
