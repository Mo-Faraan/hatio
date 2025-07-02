/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      backgroundColor: {
        'custom-color': '#4f46e5', // Example: Indigo-600
      },
    },
  },
  plugins: [],
}

