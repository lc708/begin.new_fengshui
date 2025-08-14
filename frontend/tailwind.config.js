/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/features/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'traditional': {
          red: '#8B0000',
          gold: '#FFD700',
          black: '#000000',
          beige: '#FFF8DC',
          'dark-green': '#2F4F4F',
        }
      },
      fontFamily: {
        'serif-sc': ['Noto Serif SC', 'serif'],
        'sans-sc': ['Noto Sans SC', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
