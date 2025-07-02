#!/bin/bash

# 🧹 SKATECROSS Development Cache Cleaner v37.0
# Rozwiązuje problemy z PWA + Cache + Proxy w development

echo "🧹 SKATECROSS Development Cache Cleaner v37.0"
echo "============================================="

# Kill existing processes
echo "🛑 Zatrzymuję stare procesy..."
pkill -f "vite.*5173" 2>/dev/null || true
pkill -f "python3.*api_server" 2>/dev/null || true
sleep 2

# Clear Vite cache
echo "🗑️ Czyszczę cache Vite..."
rm -rf node_modules/.vite 2>/dev/null || true
rm -rf dist 2>/dev/null || true

# Clear npm cache
echo "🗑️ Czyszczę cache npm..."
npm cache clean --force 2>/dev/null || true

# Chrome cache clear instruction
echo "🌐 Instrukcje czyszczenia przeglądarki:"
echo "   Chrome: F12 → Application → Storage → Clear site data"
echo "   Safari: F12 → Storage → Clear All"
echo "   Firefox: F12 → Storage → Clear All"

echo ""
echo "🔄 URUCHAMIAM CLEAN DEVELOPMENT..."

# Start backend
echo "🚀 Backend na porcie 5001..."
cd backend
source venv/bin/activate 2>/dev/null || true
python3 api_server.py &
BACKEND_PID=$!
cd ..

# Wait for backend
sleep 3

# Start frontend with special dev settings
echo "🚀 Frontend na porcie 5173 (development mode)..."
cd frontend

# Create temporary vite config for clean development
cat > vite.config.dev.ts << 'EOF'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      // CAŁKOWITE WYŁĄCZENIE PWA W DEVELOPMENT
      devOptions: {
        enabled: false
      },
      // Minimalna konfiguracja - tylko dla production build
      registerType: 'autoUpdate',
      workbox: {
        cleanupOutdatedCaches: true
      }
    })
  ],
  server: {
    port: 5173,
    strictPort: true,
    host: '0.0.0.0',
    // AGRESYWNE WYŁĄCZENIE CACHE
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate, max-age=0',
      'Pragma': 'no-cache',
      'Expires': '0',
      'Surrogate-Control': 'no-store'
    },
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        secure: false,
        ws: true,
        // DODATKOWE PROXY HEADERS
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
            proxyReq.setHeader('Cache-Control', 'no-cache')
          })
        }
      }
    }
  },
  // WYŁĄCZ WSZYSTKIE CACHE OPTIMIZATIONS
  optimizeDeps: {
    force: true
  }
})
EOF

# Use clean config
npx vite --config vite.config.dev.ts &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ CLEAN DEVELOPMENT URUCHOMIONY!"
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:5001"
echo ""
echo "🎯 ROZWIĄZANIE PROBLEMU:"
echo "   - PWA całkowicie wyłączone w development"
echo "   - Cache headers ustawione na no-cache"
echo "   - Proxy z dodatkowymi headers"
echo ""
echo "⚠️  W przeglądarce:"
echo "   1. Otwórz http://localhost:5173"
echo "   2. F12 → Application → Storage → Clear site data"
echo "   3. Odśwież stronę (Cmd+R)"
echo ""
echo "🎉 Teraz PWA Scanner i Backend powinny działać razem!"

# Monitor
while true; do
  sleep 30
  if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend zatrzymany!"
    break
  fi
  if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Frontend zatrzymany!"
    break
  fi
  echo "✅ $(date '+%H:%M:%S') - Development działa poprawnie"
done

# Cleanup on exit
cleanup() {
  echo "🛑 Zatrzymuję development..."
  kill $BACKEND_PID 2>/dev/null || true
  kill $FRONTEND_PID 2>/dev/null || true
  rm -f frontend/vite.config.dev.ts
  exit 0
}

trap cleanup EXIT INT TERM 