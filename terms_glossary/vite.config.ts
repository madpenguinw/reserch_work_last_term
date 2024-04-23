import { fileURLToPath, URL } from 'node:url'

import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],

  server: {
    host: '0.0.0.0',
    strictPort: true,
    port: 3080
  },
  preview: {
    host: true,
    strictPort: true,
    port: 3000
  },

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('src', import.meta.url))
    }
  }
})
