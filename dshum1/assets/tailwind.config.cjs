const defaultTheme = require('tailwindcss/defaultTheme')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "../templates/**/*.html",
    "../**/templates/**/*.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Source Sans Pro', ...defaultTheme.fontFamily.sans],
      },
    },
    container: {
      center: true,
      padding: {
        DEFAULT: '1rem',
        sm: '2rem',
        lg: '4rem',
        xl: '5rem',
        '2xl': '6rem',
      },
    },
    fontSize: {
      sm: '1rem',
      base: '1.25rem',
      xl: '1.563rem',
      '2xl': '1.953rem',
      '3xl': '2.441rem',
      '4xl': '3.052rem',
      '5xl': '3.815rem',
    }
  },
  plugins: [require("@tailwindcss/forms")],
}