/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      height: {
        'main': 'calc(100vh - 80px)'
      }
    },
  },
  plugins: [],
}

