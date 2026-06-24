import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import Sidebar from './components/Sidebar.vue'

// ── Propagación de identidad para auditoría ───────────────────────────────────
// Inyecta el token de administrador y un id de sesión en TODAS las llamadas al
// API (fetch y XMLHttpRequest/axios). Esto permite que el backend identifique con
// certeza quién realiza cada acción, sin tocar cada servicio individualmente.
;(function setupAuditPropagation() {
  const API_HOST = 'apipwa.sembrandodatos.com'

  // Id de sesión estable por pestaña
  let sid = sessionStorage.getItem('_asid')
  if (!sid) {
    sid = Math.random().toString(36).slice(2) + Date.now().toString(36)
    sessionStorage.setItem('_asid', sid)
  }

  const isApi = (url) => {
    try { return typeof url === 'string' && url.indexOf(API_HOST) !== -1 } catch (e) { return false }
  }

  // fetch
  if (window.fetch) {
    const origFetch = window.fetch.bind(window)
    window.fetch = function (input, init) {
      try {
        const url = typeof input === 'string' ? input : (input && input.url) || ''
        if (isApi(url)) {
          const token = localStorage.getItem('admin_token')
          init = init || {}
          const h = new Headers(init.headers || (typeof input !== 'string' && input.headers) || {})
          if (token && !h.has('Authorization')) h.set('Authorization', 'Bearer ' + token)
          if (!h.has('X-Session-Id')) h.set('X-Session-Id', sid)
          init.headers = h
        }
      } catch (e) { /* noop */ }
      return origFetch(input, init)
    }
  }

  // XMLHttpRequest (usado por axios)
  const origOpen = XMLHttpRequest.prototype.open
  const origSend = XMLHttpRequest.prototype.send
  const origSetHeader = XMLHttpRequest.prototype.setRequestHeader

  XMLHttpRequest.prototype.setRequestHeader = function (name, value) {
    try {
      this.__sentHeaders = this.__sentHeaders || {}
      this.__sentHeaders[String(name).toLowerCase()] = true
    } catch (e) { /* noop */ }
    return origSetHeader.call(this, name, value)
  }

  XMLHttpRequest.prototype.open = function (method, url) {
    this.__auditUrl = url
    return origOpen.apply(this, arguments)
  }

  XMLHttpRequest.prototype.send = function (body) {
    try {
      if (isApi(this.__auditUrl)) {
        const hs = this.__sentHeaders || {}
        const token = localStorage.getItem('admin_token')
        if (token && !hs['authorization']) {
          try { origSetHeader.call(this, 'Authorization', 'Bearer ' + token) } catch (e) {}
        }
        if (!hs['x-session-id']) {
          try { origSetHeader.call(this, 'X-Session-Id', sid) } catch (e) {}
        }
      }
    } catch (e) { /* noop */ }
    return origSend.call(this, body)
  }
})()

const app = createApp(App)

// Registrar Sidebar globalmente
app.component('Sidebar', Sidebar)

app.use(router)
app.mount('#app')
