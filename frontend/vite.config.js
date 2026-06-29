import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import envCompatible from 'vite-plugin-env-compatible'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig(({ command }) => ({
  plugins: [react(), envCompatible()],
  base: command === 'serve' ? '/' : '/static/',
  envDir: resolve(__dirname, '..'), // Specify the parent directory
  optimizeDeps: {
    include: [
      '@emotion/react',
      '@emotion/styled',
      '@mui/material',
      '@mui/material/styles',
      '@mui/system',
      '@mui/icons-material',
    ],
  },
  build: {
    rollupOptions: {},
  },
}))
