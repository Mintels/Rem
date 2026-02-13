import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

   // https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/Rem/',  // Your repo name
  build: {
    outDir: '../docs'  // Goes up one level and creates 'docs' folder
  }
})