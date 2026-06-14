/** @type {import('tailwindcss').Config} */
// Design system — frozen after Week 1 (see execution doc §5.3).
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
    },
  },
  plugins: [],
};
