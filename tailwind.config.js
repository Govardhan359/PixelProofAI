/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./detector/templates/**/*.html"
  ],
  theme: {
    extend: {
      colors: {
        background: '#0f172a', /* slate-900 */
        surface: '#1e293b', /* slate-800 */
        primary: '#0ea5e9', /* sky-500 */
        secondary: '#38bdf8', /* sky-400 */
      }
    },
  },
  plugins: [],
}
