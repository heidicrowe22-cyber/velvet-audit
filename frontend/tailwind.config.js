/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        velvet: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#a855f7',
          600: '#9333ea',
          700: '#7e22ce',
          800: '#6b21a8',
          900: '#581c87',
          950: '#3b0764',
          primary: '#3A0CA3',
          secondary: '#7209B7',
        },
        gold: {
          400: '#facc15',
          500: '#eab308',
          600: '#ca8a04',
          accent: '#FFD700',
        },
        champagne: '#F3E5AB',
        slate: {
          deep: '#212529',
        },
        ghost: '#F8F9FA',
        success: '#2ECC71',
        alert: '#E63946',
      },
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Montserrat', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        gold: '0 4px 14px 0 rgba(255, 215, 0, 0.35)',
        premium: '0 4px 24px 0 rgba(58, 12, 163, 0.08)',
      },
    },
  },
  plugins: [],
}