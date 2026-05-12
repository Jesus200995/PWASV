import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'prompt',
      injectRegister: 'auto',
      workbox: {
        clientsClaim: true,
        skipWaiting: true,
        cleanupOutdatedCaches: true,
        runtimeCaching: [
          {
            // API calls bypass the service worker completely — no caching, no timeout interference
            urlPattern: /\/api\//i,
            handler: 'NetworkOnly',
          },
          {
            // Static app assets only — exclude /api/ paths
            urlPattern: /^https:\/\/app\.sembrandodatos\.com\/(?!api).*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'app-cache-v1.0.4',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24 // 24 horas
              },
              networkTimeoutSeconds: 30
            }
          }
        ]
      },
      manifest: {
        name: 'Sembrando Datos',
        short_name: 'Sembrando Datos',
        description: 'Aplicación para registro de ubicaciones y reforestación',
        theme_color: '#4CAF50',
        background_color: '#FFFFFF',
        display: 'standalone',
        scope: '/',
        start_url: '/',
        icons: [
          {
            src: '/pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ],
  server: {
    port: 5174,
  },
})
