/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        blush: {
          light: '#F2E6E6',
          DEFAULT: '#C89F9F',
          dark: '#B08080',
        },
        gold: {
          DEFAULT: '#D4A84B',
        },
        background: '#FAFAF8',
        card: '#FFFFFF',
        border: '#E8E4DE',
        text: {
          primary: '#2D2A26',
          muted: '#8A8580',
        },
        success: '#8CBD8C',
        alert: '#D17A7A',
      },
      fontFamily: {
        display: ['"Cormorant Garamond"', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      letterSpacing: {
        widest: '0.25em',
        luxury: '0.36em',
      },
    },
  },
  plugins: [],
}
