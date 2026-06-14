/** @type {import('tailwindcss').Config} */
// Design system — brand palette frozen after Week 1 (see execution doc §5.3).
// Depth / motion tokens added in the premium UI pass (brand colors unchanged).
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          navy: "#0F1E3D", // primary
          orange: "#E07B00", // accent / CTAs
          teal: "#0D6E73", // info
        },
        risk: {
          low: "#10803F", // green
          mid: "#B45309", // amber
          high: "#B91C1C", // red
        },
        surface: {
          DEFAULT: "#FFFFFF",
          muted: "#F4F5F7",
          border: "#D1D5DB",
        },
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui"],
        mono: ["JetBrains Mono", "monospace"],
      },
      // Soft, consistent elevation scale (tinted with brand navy, not pure black).
      boxShadow: {
        card: "0 1px 2px rgba(15,30,61,0.04), 0 4px 16px rgba(15,30,61,0.06)",
        "card-hover":
          "0 2px 4px rgba(15,30,61,0.06), 0 16px 40px rgba(15,30,61,0.12)",
        glow: "0 8px 30px rgba(224,123,0,0.35)",
      },
      backgroundImage: {
        "grad-navy": "linear-gradient(135deg, #0F1E3D 0%, #1B335F 100%)",
        "grad-orange": "linear-gradient(135deg, #E07B00 0%, #F2A33C 100%)",
        "grad-teal": "linear-gradient(135deg, #0D6E73 0%, #1AA0A6 100%)",
        // Subtle page mesh built from brand hues at low alpha.
        "grad-mesh":
          "radial-gradient(60% 60% at 15% 0%, rgba(224,123,0,0.10) 0%, rgba(224,123,0,0) 60%), radial-gradient(55% 55% at 100% 10%, rgba(13,110,115,0.10) 0%, rgba(13,110,115,0) 55%), radial-gradient(80% 80% at 50% 120%, rgba(15,30,61,0.06) 0%, rgba(15,30,61,0) 60%)",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "fade-in": { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-14px)" },
        },
        shimmer: { "100%": { transform: "translateX(100%)" } },
      },
      animation: {
        "fade-up": "fade-up 0.5s cubic-bezier(0.16,1,0.3,1) both",
        "fade-in": "fade-in 0.4s ease-out both",
        float: "float 7s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
