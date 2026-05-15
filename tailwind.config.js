/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'midnight': '#000000',
        'dark-slate': '#0a0a0a',
        'graphite': '#1a1a1a',
        'grey-900': '#1f1f1f',
        'grey-800': '#2a2a2a',
        'grey-700': '#3a3a3a',
        'grey-600': '#4a4a4a',
        'grey-500': '#666666',
        'grey-400': '#888888',
        'grey-300': '#aaaaaa',
        'grey-200': '#cccccc',
        'grey-100': '#dddddd',
        'white': '#ffffff',
        'off-white': '#f5f5f5',
        'royal': '#ffffff',
        'neon-cyan': '#cccccc',
        'neon-blue': '#888888',
        'premium-purple': '#666666',
        'emerald-accent': '#888888',
        'rose-accent': '#999999',
      },
      backdropBlur: {
        'xl': '32px',
      },
      boxShadow: {
        'glow': '0 0 20px rgba(255, 255, 255, 0.1)',
        'premium': '0 10px 30px rgba(0, 0, 0, 0.5)',
        'inner-glow': 'inset 0 0 20px rgba(255, 255, 255, 0.05)',
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 3s ease-in-out infinite',
        'shimmer': 'shimmer 2s infinite',
        'slide-up': 'slide-up 0.5s ease-out',
        'fade-in': 'fade-in 0.5s ease-out',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'shimmer': {
          '0%': { backgroundPosition: '-1000px 0' },
          '100%': { backgroundPosition: '1000px 0' },
        },
        'slide-up': {
          'from': { opacity: '0', transform: 'translateY(20px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in': {
          'from': { opacity: '0' },
          'to': { opacity: '1' },
        },
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
        'satoshi': ['Satoshi', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
