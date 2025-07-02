import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const config: any = {
    plugins: [
      vue(),
      VitePWA({
        registerType: 'autoUpdate',
        includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],
        manifest: {
          name: 'SKATECROSS PWA v37.0',
          short_name: 'SKATECROSS',
          description: 'System turniejowy SKATECROSS - skaner QR, rankingi, start control',
          theme_color: '#3b82f6',
          background_color: '#1f2937',
          display: 'standalone',
          scope: '/',
          start_url: '/',
          icons: [
            {
              src: 'icons/icon-192x192.png',
              sizes: '192x192',
              type: 'image/png'
            },
            {
              src: 'icons/icon-512x512.png',
              sizes: '512x512',
              type: 'image/png'
            }
          ]
        },
        workbox: {
          globPatterns: ['**/*.{js,css,html,ico,png,svg}']
          // USUNIĘTO runtimeCaching API - powodowało konflikty z proxy w development
        },
        devOptions: {
          enabled: false, // WYŁĄCZONE w development - eliminuje konflikty z proxy
          type: 'module'
        }
      })
    ],
    build: {
      // OPTYMALIZACJA BUNDLE SIZE - v30.5.4
      rollupOptions: {
        output: {
          manualChunks: {
            // Vendor chunks - oddzielne chunki dla dużych bibliotek
            'vue-vendor': ['vue'],
            'axios-vendor': ['axios'],
            'heroicons': ['@heroicons/vue/24/outline'],
            'qrcode': ['qrcode']
          }
        }
      },
      // Kompresja i minifikacja
      minify: true,
      terserOptions: {
        compress: {
          drop_console: mode === 'production', // Usuń console.log w produkcji
          drop_debugger: true
        }
      },
      // Zwiększ limity dla analizy bundle size
      chunkSizeWarningLimit: 500
    },
    // Optymalizacje dev server
    optimizeDeps: {
      include: [
        'vue',
        'axios',
        '@heroicons/vue/24/outline',
        'qrcode'
      ]
    }
  }

  // Dev server konfiguracja - UPROSZCZONA dla debugowania
  if (mode === 'development') {
    config.server = {
      port: 5173, // WYMUSZONY port 5173
      strictPort: true, // BRAK SKAKANIA PORTÓW!
      https: false, // HTTP dla debugowania połączenia
      host: '0.0.0.0', // Pozwala na dostęp z innych urządzeń w sieci
      headers: {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      },
      proxy: {
        '/api': {
          target: 'http://localhost:5001',
          changeOrigin: true,
          secure: false,
          ws: true,
          configure: (proxy, _options) => {
            proxy.on('error', (err, _req, _res) => {
              console.log('🔴 Proxy error:', err.message);
            });
            proxy.on('proxyReq', (proxyReq, req, _res) => {
              console.log('📤 Proxy request:', req.method, req.url);
            });
            proxy.on('proxyRes', (proxyRes, req, _res) => {
              console.log('📥 Proxy response:', proxyRes.statusCode, req.url);
            });
          }
        }
      }
    }
  }

  return config
}) 