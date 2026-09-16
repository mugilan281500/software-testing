import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/mock-bank': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/tests': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/findings': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/flags': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/dashboard': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/reports': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
