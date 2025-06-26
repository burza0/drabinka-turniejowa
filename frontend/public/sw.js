// Service Worker dla SKATECROSS PWA v37.0
const CACHE_NAME = 'skatecross-pwa-v37-0'
const API_CACHE_NAME = 'skatecross-api-v37-0'
const OFFLINE_QUEUE_NAME = 'skatecross-offline-queue'

// Pliki do buforowania przy instalacji
const STATIC_CACHE_URLS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
]

// API endpoints do buforowania
const API_CACHE_PATTERNS = [
  /^\/api\/zawodnicy/,
  /^\/api\/rankings/,
  /^\/api\/kategorie/,
  /^\/api\/kluby/,
  /^\/api\/unified\/dashboard-data/
]

// API endpoints tylko online (skanowanie, check-in)
const ONLINE_ONLY_PATTERNS = [
  /^\/api\/unified\/scan-qr/,
  /^\/api\/unified\/register-athlete/,
  /^\/api\/qr\/manual-checkins/,
  /^\/api\/centrum-startu\/manual-checkin/
]

// === INSTALACJA SERVICE WORKER ===
self.addEventListener('install', (event) => {
  console.log('🔧 SKATECROSS PWA: Service Worker installing...')
  
  event.waitUntil(
    Promise.all([
      // Cache statycznych plików
      caches.open(CACHE_NAME).then((cache) => {
        console.log('📦 Caching static files')
        return cache.addAll(STATIC_CACHE_URLS)
      }),
      
      // Przygotuj offline queue
      caches.open(OFFLINE_QUEUE_NAME)
    ])
  )
  
  // Aktywuj nowy SW natychmiast
  self.skipWaiting()
})

// === AKTYWACJA SERVICE WORKER ===
self.addEventListener('activate', (event) => {
  console.log('🚀 SKATECROSS PWA: Service Worker activating...')
  
  event.waitUntil(
    Promise.all([
      // Usuń stare cache
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => 
              cacheName !== CACHE_NAME && 
              cacheName !== API_CACHE_NAME &&
              cacheName !== OFFLINE_QUEUE_NAME
            )
            .map((cacheName) => {
              console.log(`🗑️ Deleting old cache: ${cacheName}`)
              return caches.delete(cacheName)
            })
        )
      }),
      
      // Przejmij kontrolę nad wszystkimi klientami
      self.clients.claim()
    ])
  )
})

// === PRZECHWYTYWANIE ŻĄDAŃ ===
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)
  
  // Ignoruj żądania spoza naszej domeny
  if (!url.origin.includes(self.location.origin)) {
    return
  }
  
  // Strategia dla różnych typów żądań
  if (request.method === 'GET') {
    if (url.pathname.startsWith('/api/')) {
      event.respondWith(handleApiRequest(request))
    } else {
      event.respondWith(handleStaticRequest(request))
    }
  } else if (request.method === 'POST') {
    event.respondWith(handlePostRequest(request))
  }
})

// === OBSŁUGA ŻĄDAŃ STATYCZNYCH ===
async function handleStaticRequest(request) {
  try {
    // Network First dla HTML (zawsze świeże)
    if (request.url.includes('.html') || request.url.endsWith('/')) {
      try {
        const networkResponse = await fetch(request)
        if (networkResponse.ok) {
          const cache = await caches.open(CACHE_NAME)
          cache.put(request, networkResponse.clone())
          return networkResponse
        }
      } catch (error) {
        console.log('📡 Network failed, falling back to cache')
      }
      
      // Fallback do cache
      const cachedResponse = await caches.match(request)
      if (cachedResponse) {
        return cachedResponse
      }
      
      // Ultimate fallback - offline page
      return new Response(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>SKATECROSS - Offline</title>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            body { 
              font-family: system-ui; 
              text-align: center; 
              padding: 2rem;
              background: linear-gradient(135deg, #1f2937 0%, #3b82f6 100%);
              color: white;
              min-height: 100vh;
              margin: 0;
              display: flex;
              align-items: center;
              justify-content: center;
              flex-direction: column;
            }
            .logo { font-size: 2rem; margin-bottom: 1rem; }
            .message { font-size: 1.2rem; margin-bottom: 2rem; }
            .retry { 
              background: #3b82f6; 
              color: white; 
              border: none; 
              padding: 1rem 2rem; 
              border-radius: 8px; 
              cursor: pointer; 
              font-size: 1rem;
            }
          </style>
        </head>
        <body>
          <div class="logo">🏁 SKATECROSS PWA</div>
          <div class="message">Tryb Offline</div>
          <button class="retry" onclick="window.location.reload()">Spróbuj ponownie</button>
        </body>
        </html>
      `, {
        headers: { 'Content-Type': 'text/html' }
      })
    }
    
    // Cache First dla zasobów statycznych
    const cachedResponse = await caches.match(request)
    if (cachedResponse) {
      return cachedResponse
    }
    
    // Fetch i cache nowych zasobów
    const networkResponse = await fetch(request)
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME)
      cache.put(request, networkResponse.clone())
    }
    return networkResponse
    
  } catch (error) {
    console.error('❌ Error handling static request:', error)
    return new Response('Offline', { status: 503 })
  }
}

// === OBSŁUGA ŻĄDAŃ API ===
async function handleApiRequest(request) {
  const url = new URL(request.url)
  
  // Sprawdź czy to endpoint tylko online
  const isOnlineOnly = ONLINE_ONLY_PATTERNS.some(pattern => 
    pattern.test(url.pathname)
  )
  
  if (isOnlineOnly) {
    try {
      return await fetch(request)
    } catch (error) {
      console.log('📡 Online-only API failed:', url.pathname)
      return new Response(
        JSON.stringify({ 
          error: 'Endpoint wymaga połączenia internetowego',
          offline: true,
          endpoint: url.pathname
        }),
        { 
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        }
      )
    }
  }
  
  // Cache strategia dla API
  const shouldCache = API_CACHE_PATTERNS.some(pattern => 
    pattern.test(url.pathname)
  )
  
  if (!shouldCache) {
    return fetch(request)
  }
  
  try {
    // Network First dla API
    const networkResponse = await fetch(request)
    
    if (networkResponse.ok) {
      const cache = await caches.open(API_CACHE_NAME)
      cache.put(request, networkResponse.clone())
      return networkResponse
    }
  } catch (error) {
    console.log('📡 API Network failed, trying cache:', url.pathname)
  }
  
  // Fallback do cache
  const cachedResponse = await caches.match(request, {
    cacheName: API_CACHE_NAME
  })
  
  if (cachedResponse) {
    console.log('💾 Serving API from cache:', url.pathname)
    // Dodaj header oznaczający cache
    const response = cachedResponse.clone()
    response.headers.set('X-Served-From', 'cache')
    return response
  }
  
  // Brak cache - zwróć błąd offline
  return new Response(
    JSON.stringify({ 
      error: 'Brak danych offline dla tego endpoint',
      offline: true,
      endpoint: url.pathname
    }),
    { 
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    }
  )
}

// === OBSŁUGA ŻĄDAŃ POST (OFFLINE QUEUE) ===
async function handlePostRequest(request) {
  try {
    // Spróbuj normalnego wysłania
    const networkResponse = await fetch(request)
    if (networkResponse.ok) {
      return networkResponse
    }
  } catch (error) {
    console.log('📡 POST request failed, queuing for later...')
  }
  
  // Dodaj do offline queue
  await addToOfflineQueue(request)
  
  return new Response(
    JSON.stringify({ 
      success: true,
      message: 'Żądanie dodane do kolejki offline',
      queued: true
    }),
    { 
      status: 202,
      headers: { 'Content-Type': 'application/json' }
    }
  )
}

// === OFFLINE QUEUE ===
async function addToOfflineQueue(request) {
  const cache = await caches.open(OFFLINE_QUEUE_NAME)
  const queueKey = `offline-${Date.now()}-${Math.random()}`
  
  // Sklonuj request z body
  const body = await request.text()
  const queuedRequest = new Request(request.url, {
    method: request.method,
    headers: request.headers,
    body: body
  })
  
  await cache.put(queueKey, new Response(body, {
    headers: {
      'X-Original-URL': request.url,
      'X-Original-Method': request.method,
      'X-Timestamp': Date.now().toString()
    }
  }))
  
  console.log('📥 Added to offline queue:', queueKey)
}

// === BACKGROUND SYNC ===
self.addEventListener('sync', (event) => {
  if (event.tag === 'offline-queue') {
    console.log('🔄 Background sync: processing offline queue')
    event.waitUntil(processOfflineQueue())
  }
})

async function processOfflineQueue() {
  const cache = await caches.open(OFFLINE_QUEUE_NAME)
  const requests = await cache.keys()
  
  for (const request of requests) {
    try {
      const response = await cache.match(request)
      if (!response) continue
      
      const originalURL = response.headers.get('X-Original-URL')
      const originalMethod = response.headers.get('X-Original-Method')
      const body = await response.text()
      
      // Wyślij oryginalny request
      const result = await fetch(originalURL, {
        method: originalMethod,
        body: body,
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      if (result.ok) {
        // Usuń z queue po sukcesie
        await cache.delete(request)
        console.log('✅ Offline queue item processed:', originalURL)
      }
      
    } catch (error) {
      console.log('❌ Failed to process queue item:', error)
    }
  }
}

// === PUSH NOTIFICATIONS ===
self.addEventListener('push', (event) => {
  if (!event.data) return
  
  try {
    const data = event.data.json()
    
    const options = {
      body: data.body || 'Nowe powiadomienie z SKATECROSS',
      icon: '/icons/icon-192x192.png',
      badge: '/icons/icon-72x72.png',
      data: data.data || {},
      actions: [
        {
          action: 'view',
          title: 'Zobacz'
        },
        {
          action: 'dismiss',
          title: 'Zamknij'
        }
      ]
    }
    
    event.waitUntil(
      self.registration.showNotification(
        data.title || 'SKATECROSS PWA',
        options
      )
    )
  } catch (error) {
    console.error('❌ Push notification error:', error)
  }
})

// === NOTIFICATION CLICK ===
self.addEventListener('notificationclick', (event) => {
  event.notification.close()
  
  if (event.action === 'view') {
    event.waitUntil(
      clients.openWindow(event.notification.data.url || '/')
    )
  }
})

console.log('🏁 SKATECROSS PWA v37.0 Service Worker loaded!') 