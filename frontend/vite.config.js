import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/Rem/',
  build: {
    outDir: '../docs'
  },
  server: {
    allowedHosts: ['scarlette-frogeyed-melvina.ngrok-free.dev']
  }
})
