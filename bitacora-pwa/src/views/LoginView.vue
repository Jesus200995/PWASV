<template>
  <div class="page">
    <div class="card">
      <div class="brand">
        <div class="brand-icon" aria-hidden="true">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="10" fill="#1a6ef5"/>
            <path d="M16 7l7 4v10l-7 4-7-4V11l7-4z" stroke="#fff" stroke-width="1.6" stroke-linejoin="round" fill="none"/>
            <circle cx="16" cy="16" r="2.5" fill="#fff"/>
          </svg>
        </div>
        <div>
          <h1>Panel de control</h1>
          <p class="sub">Acceso privado · PWASV</p>
        </div>
      </div>

      <form @submit.prevent="doLogin" novalidate>
        <div class="field">
          <label for="handle">
            <i class="ti ti-user" aria-hidden="true"></i> Usuario
          </label>
          <input
            id="handle"
            v-model="handle"
            type="text"
            placeholder="Ingresa tu usuario"
            autocomplete="username"
            :class="{ error: !!errMsg }"
            required
          />
        </div>

        <div class="field">
          <label for="secret">
            <i class="ti ti-lock" aria-hidden="true"></i> Contraseña
          </label>
          <div class="pass-wrap">
            <input
              id="secret"
              v-model="secret"
              :type="showPass ? 'text' : 'password'"
              placeholder="••••••••"
              autocomplete="current-password"
              :class="{ error: !!errMsg }"
              required
            />
            <button type="button" class="eye-btn" @click="showPass = !showPass" :aria-label="showPass ? 'Ocultar' : 'Mostrar'">
              <i :class="showPass ? 'ti ti-eye-off' : 'ti ti-eye'" aria-hidden="true"></i>
            </button>
          </div>
        </div>

        <transition name="fade">
          <div v-if="errMsg" class="err-banner" role="alert">
            <i class="ti ti-alert-circle" aria-hidden="true"></i> {{ errMsg }}
          </div>
        </transition>

        <button type="submit" class="submit-btn" :disabled="loading || !handle || !secret">
          <span v-if="loading" class="spinner" aria-hidden="true"></span>
          <span>{{ loading ? 'Verificando...' : 'Iniciar sesión' }}</span>
        </button>
      </form>

      <p class="footer-note">Sistema restringido — uso exclusivo administrativo</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { obsLogin } from '../services/api.js'

const router = useRouter()
const handle = ref('')
const secret = ref('')
const showPass = ref(false)
const errMsg = ref('')
const loading = ref(false)

async function doLogin() {
  errMsg.value = ''
  loading.value = true
  try {
    await obsLogin(handle.value.trim(), secret.value)
    router.push('/dashboard')
  } catch (e) {
    errMsg.value = e.message || 'Credenciales inválidas'
    secret.value = ''
  } finally {
    loading.value = false
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', system-ui, sans-serif;
  background: #06090f;
  color: #e2e8f0;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

:root {
  --blue: #1a6ef5;
  --blue-hover: #1558d6;
  --surface: #0d1117;
  --surface2: #161b22;
  --border: rgba(255,255,255,0.08);
  --border-focus: rgba(26,110,245,0.6);
  --text: #e2e8f0;
  --muted: #8b949e;
  --danger: #f85149;
  --danger-bg: rgba(248,81,73,0.12);
  --radius: 10px;
  --radius-lg: 16px;
}
</style>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(26,110,245,0.12) 0%, transparent 70%), #06090f;
}

.card {
  width: 100%;
  max-width: 400px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 2.25rem 2rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.875rem;
}

.brand-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(26,110,245,0.12);
  border: 1px solid rgba(26,110,245,0.3);
}

h1 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text);
  line-height: 1.3;
}

.sub {
  font-size: 0.78rem;
  color: var(--muted);
  margin-top: 2px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

label {
  font-size: 0.78rem;
  font-weight: 500;
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 0.3rem;
  letter-spacing: 0.02em;
}

label i { font-size: 14px; }

input {
  width: 100%;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.65rem 0.875rem;
  font-size: 0.9rem;
  color: var(--text);
  font-family: inherit;
  outline: none;
  transition: border-color 0.18s;
}

input::placeholder { color: var(--muted); opacity: 0.6; }

input:focus {
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(26,110,245,0.12);
}

input.error { border-color: var(--danger); }

.pass-wrap { position: relative; }

.pass-wrap input { padding-right: 2.75rem; }

.eye-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--muted);
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  font-size: 16px;
  transition: color 0.15s;
}

.eye-btn:hover { color: var(--text); }

.err-banner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--danger-bg);
  border: 1px solid rgba(248,81,73,0.3);
  border-radius: var(--radius);
  padding: 0.55rem 0.875rem;
  font-size: 0.82rem;
  color: var(--danger);
}

.err-banner i { font-size: 15px; flex-shrink: 0; }

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: var(--blue);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  padding: 0.72rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.18s, opacity 0.18s, transform 0.1s;
  margin-top: 0.25rem;
}

.submit-btn:hover:not(:disabled) { background: var(--blue-hover); }
.submit-btn:active:not(:disabled) { transform: scale(0.98); }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.spinner {
  width: 15px;
  height: 15px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

@keyframes spin { to { transform: rotate(360deg); } }

.footer-note {
  font-size: 0.72rem;
  color: var(--muted);
  text-align: center;
  opacity: 0.6;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s, transform 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-4px); }

@media (max-width: 480px) {
  .card { padding: 1.75rem 1.25rem 1.5rem; }
}
</style>
