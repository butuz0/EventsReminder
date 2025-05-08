import type {Config} from "tailwindcss";

const config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  prefix: "",
  theme: {
    extend: {
      colors: {
        seaBlue: "#155dfc",
        skyBlue: "#dff2fe",
        grayLight: "#f9fafb",
      },
      fontFamily: {
        sourceSerif: ["var(--font-sourceSerif)", "serif"],
        nunito: ["var(--font-nunito)", "sans-serif"],
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;

export default config;