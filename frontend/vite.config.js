import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Permite que o Docker exponha a porta
    port: 5173,
    watch: {
      usePolling: true, // Força o Hot Reload a funcionar mapeado via Volume
    }
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.js',
  }
})