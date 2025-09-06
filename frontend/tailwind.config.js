/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}",
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "primary-black": "#000000",
        "primary-white": "#FFFFFF",
        "brand-hot-pink": "#FF0088",
      },
      boxShadow: {
        "neon-glow": "0 0 20px rgba(255, 0, 136, 0.6)",
      },
    },
  },
  plugins: [],
};
