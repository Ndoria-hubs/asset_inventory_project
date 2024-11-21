import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  optimizeDeps: {
    exclude: ['problematic-dependency'], // Add the name of the dependency that causes the issue
  },
  plugins: [react()],
})
