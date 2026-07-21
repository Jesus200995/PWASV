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
        runtimeCaching: [
          {
            urlPattern: /\/api\//i,
            handler: 'NetworkOnly',
          },
          {
            urlPattern: /^https:\/\/app\.sembrandodatos\.com\/(?!api).*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'app-cache-v1.0.5',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24
              },
              networkTimeoutSeconds: 30
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
