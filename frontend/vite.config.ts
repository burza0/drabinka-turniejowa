import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const config = {
    plugins: [vue()],
  }

  // Proxy tylko w developmencie
  if (mode === 'development') {
    config.server = {
      proxy: {
        '/api': {
          target: 'http://localhost:5000',
          changeOrigin: true
        }
      }
    }
  }

  return config
}) 