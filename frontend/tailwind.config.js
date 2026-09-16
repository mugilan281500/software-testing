/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: "#0B0F17",
          card: "#111827",
          border: "#1E293B",
          hover: "#1F293D",
          input: "#0D131F"
        },
        risk: {
          low: "#10B981",       // Emerald
          medium: "#F59E0B",    // Amber
          high: "#F97316",      // Orange
          critical: "#EF4444"   // Crimson Red
        },
        brand: {
          cyan: "#06B6D4",
          blue: "#3B82F6",
          purple: "#8B5CF6",
          emerald: "#10B981"
        }
      }
    },
  },
  plugins: [],
}
