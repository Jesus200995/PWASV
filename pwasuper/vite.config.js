import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      injectRegister: 'auto',
      manifest: false,
      workbox: {
        clientsClaim: true,
        skipWaiting: true,
        cleanupOutdatedCaches: true,
        /*
         * Sin esto, cualquier navegación de ruta (ej. /historial, /profile)
         * que no coincida con un asset precacheado exacto cae al navegador
         * nativo "sin conexión" en vez de servir el app shell cacheado.
         * Es la causa de que la app no abra sin internet.
         */
        navigateFallback: '/index.html',
        navigateFallbackDenylist: [/^\/api\//],
        runtimeCaching: [
          {
            urlPattern: /\/api\//i,
            handler: 'NetworkOnly',
          },
          {
            urlPattern: /^https:\/\/app\.sembrandodatos\.com\/(?!api).*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'app-cache-v1.0.6',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24
              },
              networkTimeoutSeconds: 5
            }
          }
        ]
      }
    })
  ],
  server: {
    port: 5174,
  },
})
