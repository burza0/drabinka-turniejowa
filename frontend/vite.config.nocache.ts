import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 🔥 SKATECROSS NO-CACHE CONFIG - Port 5175
// Całkowicie wyłącza PWA i cache dla development
export default defineConfig({
  plugins: [
    vue()
    // BRAK PWA PLUGINU - całkowicie wyłączony w development
  ],
  server: {
    port: 5175, // NOWY PORT - omija cache przeglądarki
    strictPort: true,
    host: '0.0.0.0',
    // MAKSYMALNIE AGRESYWNE ANTI-CACHE HEADERS
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate, max-age=0, s-maxage=0',
      'Pragma': 'no-cache',
      'Expires': '0',
      'Surrogate-Control': 'no-store',
      'X-Accel-Expires': '0',
      'Last-Modified': new Date().toUTCString(),
      'ETag': `"${Date.now()}"` // Unikalny ETag dla każdego startu
    },
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        secure: false,
        ws: true,
        configure: (proxy) => {
          proxy.on('error', (err, _req, _res) => {
            console.log('🔴 Proxy error:', err.message);
          });
          proxy.on('proxyReq', (proxyReq, req, _res) => {
            // ANTI-CACHE HEADERS dla proxy
            proxyReq.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
            proxyReq.setHeader('Pragma', 'no-cache');
            proxyReq.setHeader('X-Timestamp', Date.now().toString());
            console.log('📤 Proxy (NO-CACHE):', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes, req, _res) => {
            // ANTI-CACHE HEADERS dla response
            proxyRes.headers['cache-control'] = 'no-cache, no-store, must-revalidate';
            proxyRes.headers['pragma'] = 'no-cache';
            proxyRes.headers['expires'] = '0';
            console.log('📥 Proxy response:', proxyRes.statusCode, req.url);
          });
        }
      }
    }
  },
  // WYMUŚ ODŚWIEŻENIE WSZYSTKICH DEPENDENCJI
  optimizeDeps: {
    force: true // Wymusza przebudowę dependency cache
  },
  // WYŁĄCZ WSZYSTKIE CACHE MECHANIZMY
  build: {
    // Wyłącz cache podczas buildu
    write: true,
    emptyOutDir: true
  },
  // DODAJ TIMESTAMP DO WSZYSTKICH ASSETÓW
  define: {
    __TIMESTAMP__: Date.now()
  }
}) 