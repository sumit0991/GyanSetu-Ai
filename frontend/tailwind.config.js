/** @type {import('tailwindcss').Config} */
export default {
  // 1. Path Scanning: Ensures Tailwind finds classes in your React components
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],

  // 2. Dark Mode: Set to 'class' so our toggle switch in App.tsx works
  darkMode: 'class',

  theme: {
    extend: {
      // 3. Custom Transitions: Ensures smooth theme switching
      transitionProperty: {
        'colors': 'background-color, border-color, color, fill, stroke',
      },
      // 4. Animation: For the 'Synthesizing' loading state
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },

  // 5. Plugins: Recommended for AI-generated text (Notes area)
  plugins: [],
}