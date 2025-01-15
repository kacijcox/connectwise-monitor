import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://connectwise-monitor-ategh4fmh7cmfsdu.centralus-01.azurewebsites.net/',  
        changeOrigin: true,
        secure: false,
      }
    }
  },
  base: '/',
})