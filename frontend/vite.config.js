import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

const frontendPort = process.env.FRONTEND_PORT;
const isDevelopment = process.env.NODE_ENV === 'development';

// https://vitejs.dev/config/
export default defineConfig(({command, mode}) => {

  const env = loadEnv(mode, process.cwd(), '');

  return {
    server: { https: true },
    plugins: [react()],
    server: {
      watch: {
        usePolling: isDevelopment,
      },
      host: true,
      strictPort: true,
      port: frontendPort,
    },
    define: {
      __APP_ENV__: JSON.stringify(env.APP_ENV),
    },
    build: {
      target: 'esnext' //browsers can handle the latest ES features
    },
  }
})