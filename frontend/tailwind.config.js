/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Rubik', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        neo: {
          bg: '#121212',
          surface: '#1a1a1a',
          elevated: '#1e1e1e',
          accent: '#00a3ff',
          muted: '#8a8f98',
        },
      },
      borderRadius: {
        neo: '2rem',
        'neo-lg': '2.5rem',
      },
      boxShadow: {
        'neo-raised': '8px 8px 20px rgba(0, 0, 0, 0.55), -4px -4px 12px rgba(255, 255, 255, 0.04)',
        'neo-panel': '10px 10px 24px rgba(0, 0, 0, 0.55), -6px -6px 16px rgba(255, 255, 255, 0.04)',
        'neo-inset': 'inset 4px 4px 10px rgba(0, 0, 0, 0.55), inset -2px -2px 6px rgba(255, 255, 255, 0.04)',
        'neo-glow': '0 4px 20px rgba(0, 163, 255, 0.35)',
        'neo-glow-lg': '0 6px 28px rgba(0, 163, 255, 0.45)',
        'neo-hero': '8px 8px 20px rgba(0, 0, 0, 0.55), -4px -4px 12px rgba(255, 255, 255, 0.04), 0 4px 24px rgba(255, 255, 255, 0.08)',
      },
    },
  },
  plugins: [],
}
