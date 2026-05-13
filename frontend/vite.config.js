import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  // 👇 REQUIRED for FastAPI + Docker + Render
  build: {
    outDir: "dist",          // output folder
    assetsDir: "assets",     // matches FastAPI's /assets mount
    emptyOutDir: true,
  },

  // 👇 REQUIRED so Vite builds correct absolute URLs
  base: "/",                 // ensures paths like /assets/... work
})
