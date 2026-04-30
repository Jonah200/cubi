import path from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  base: '/static/',
  build: {
    outDir: 'dist/'
    },
  server: {
    proxy: {
      '/api/events/': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        headers: { 'X-Accel-Buffering': 'no' },
      },
      '/api': 'http://localhost:8000',
    },
  },
})
