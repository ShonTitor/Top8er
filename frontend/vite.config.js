import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import envCompatible from 'vite-plugin-env-compatible'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), envCompatible()],
  base: '/static/',
  envDir: resolve(__dirname, '..'), // Specify the parent directory
})
