/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'surface': {
          DEFAULT: '#0B0F1A',
          light: '#F0F2F5',
        },
        'card': {
          DEFAULT: '#131929',
          light: '#FFFFFF',
        },
        'text-primary': {
          DEFAULT: '#E8EAF0',
          light: '#1A1D2E',
        },
        'accent-red': {
          DEFAULT: '#FF3B3B',
          light: '#D62828',
        },
        'accent-amber': {
          DEFAULT: '#F59E0B',
          light: '#D97706',
        },
        'accent-green': {
          DEFAULT: '#10B981',
          light: '#059669',
        },
        'accent-blue': {
          DEFAULT: '#3B82F6',
          light: '#2563EB',
        },
        'border-color': {
          DEFAULT: 'rgba(255,255,255,0.06)',
          light: 'rgba(0,0,0,0.08)',
        }
      },
      fontFamily: {
        'heading': ['Inter', 'sans-serif'],
        'body': ['Inter', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'scanline': 'scanline 2s linear infinite',
        'pulse-ring': 'pulse-ring 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite',
        'fade-in': 'fadeIn 0.3s ease-out',
      },
      keyframes: {
        scanline: {
          '0%': { transform: 'translateY(0%)' },
          '100%': { transform: 'translateY(100%)' },
        },
        'pulse-ring': {
          '0%': { transform: 'scale(0.8)', opacity: '0.5' },
          '100%': { transform: 'scale(1.5)', opacity: '0' },
        },
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
}
