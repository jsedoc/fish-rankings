import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Food Safety Platform Brand Colors
        'primary': {
          50: '#e6f7f7',
          100: '#b3e6e6',
          200: '#80d5d5',
          300: '#4dc4c4',
          400: '#1ab3b3',
          500: '#0D7377', // Main teal
          600: '#0a5c5f',
          700: '#084547',
          800: '#052e2f',
          900: '#031717',
        },
        'accent': {
          50: '#fef6ed',
          100: '#fce8d1',
          200: '#fadbb5',
          300: '#f8cd99',
          400: '#f6c07d',
          500: '#F4A259', // Warm amber
          600: '#c38247',
          700: '#926135',
          800: '#614123',
          900: '#302011',
        },
        'success': '#2D6A4F',
        'warning': '#F4A259',
        'danger': '#E63946',
        'ocean-dark': '#0a1e2e',
      },
    },
  },
  plugins: [],
}
export default config
