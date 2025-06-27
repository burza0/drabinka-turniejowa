import { createApp } from 'vue'
import './style.css'  // Przywracam import Tailwind CSS
import App from './App.vue'
import { pinia } from './stores'

// PWA Registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('🏁 SKATECROSS PWA: Service Worker registered', registration.scope)
      })
      .catch((error) => {
        console.log('❌ SKATECROSS PWA: Service Worker registration failed', error)
      })
  })
}

const app = createApp(App)
app.use(pinia)
app.mount('#app')
