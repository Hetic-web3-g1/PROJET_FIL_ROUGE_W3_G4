import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const frontendPort = process.env.FRONTEND_PORT;
const isDevelopment = process.env.NODE_ENV === 'development';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    watch: {
      usePolling: isDevelopment,
    },
    host: true,
    strictPort: true,
    port: frontendPort,
  },
})
