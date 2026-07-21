<template>
  <div class="login-page">

    <!-- ═══ PANEL IZQUIERDO — imagen de campo (solo desktop) ═══ -->
    <div class="image-panel" aria-hidden="true">
      <div class="image-overlay"></div>
      <div class="image-content">
        <div class="image-logo">
          <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" class="hero-leaf">
            <defs>
              <linearGradient id="lg1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#bbf7d0"/>
                <stop offset="100%" style="stop-color:#4ade80"/>
              </linearGradient>
            </defs>
            <path d="M50 12 C28 22, 16 46, 22 68 C28 86, 44 92, 50 92 C56 92, 72 86, 78 68 C84 46, 72 22, 50 12"
              fill="none" stroke="url(#lg1)" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M50 18 L50 84" stroke="url(#lg1)" stroke-width="1.8" fill="none" stroke-linecap="round"/>
            <path d="M50 30 L36 42 M50 46 L32 58 M50 60 L36 70" stroke="url(#lg1)" stroke-width="1.3" fill="none" stroke-linecap="round"/>
            <path d="M50 30 L64 42 M50 46 L68 58 M50 60 L64 70" stroke="url(#lg1)" stroke-width="1.3" fill="none" stroke-linecap="round"/>
          </svg>
        </div>
        <h1 class="hero-title">Sembrando Vida</h1>
        <p class="hero-subtitle">Subsecretaría de Inclusión Productiva<br>y Desarrollo Rural</p>
        <div class="hero-divider"></div>
        <p class="hero-tagline">Sistema de Seguimiento<br>y Monitoreo de Campo</p>
        <div class="hero-stats">
          <div class="stat">
            <span class="stat-icon">🌱</span>
            <span class="stat-label">Seguimiento en tiempo real</span>
          </div>
          <div class="stat">
            <span class="stat-icon">📍</span>
            <span class="stat-label">Geolocalización precisa</span>
          </div>
          <div class="stat">
            <span class="stat-icon">📊</span>
            <span class="stat-label">Reportes y estadísticas</span>
          </div>
        </div>
      </div>
      <!-- Decoraciones flotantes -->
      <div class="float-circle fc-1"></div>
      <div class="float-circle fc-2"></div>
      <div class="float-circle fc-3"></div>
    </div>

    <!-- ═══ PANEL DERECHO — formulario ═══ -->
    <div class="form-panel">
      <!-- Logo pequeño visible solo en móvil -->
      <div class="mobile-brand">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" class="mobile-leaf">
          <defs>
            <linearGradient id="lg2" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#15803d"/>
              <stop offset="100%" style="stop-color:#4ade80"/>
            </linearGradient>
          </defs>
          <path d="M50 12 C28 22, 16 46, 22 68 C28 86, 44 92, 50 92 C56 92, 72 86, 78 68 C84 46, 72 22, 50 12"
            fill="none" stroke="url(#lg2)" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M50 18 L50 84" stroke="url(#lg2)" stroke-width="1.8" fill="none" stroke-linecap="round"/>
          <path d="M50 30 L36 42 M50 46 L32 58 M50 60 L36 70" stroke="url(#lg2)" stroke-width="1.3" fill="none" stroke-linecap="round"/>
          <path d="M50 30 L64 42 M50 46 L68 58 M50 60 L64 70" stroke="url(#lg2)" stroke-width="1.3" fill="none" stroke-linecap="round"/>
        </svg>
        <span class="mobile-brand-name">Sembrando Vida</span>
      </div>

      <div class="form-box">
        <!-- Encabezado del formulario -->
        <div class="form-header">
          <h2 class="form-title">Iniciar sesión</h2>
          <p class="form-desc">Ingresa tus credenciales para acceder</p>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="login" class="login-form" novalidate>
          <!-- Usuario -->
          <div class="form-group">
            <label for="username" class="form-label">Correo electrónico</label>
            <div class="input-wrap">
              <span class="input-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
              </span>
              <input
                v-model="credentials.username"
                type="text"
                id="username"
                placeholder="usuario@ejemplo.com"
                autocomplete="username"
                required
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Contraseña -->
          <div class="form-group">
            <label for="password" class="form-label">Contraseña</label>
            <div class="input-wrap">
              <span class="input-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
              </span>
              <input
                v-model="credentials.password"
                :type="showPassword ? 'text' : 'password'"
                id="password"
                placeholder="••••••••"
                autocomplete="current-password"
                required
                :disabled="loading"
              />
              <button
                type="button"
                class="eye-btn"
                @click="showPassword = !showPassword"
                :disabled="loading"
                :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
              >
                <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Botón submit -->
          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading" class="btn-inner">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="btn-icon">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
                <polyline points="10 17 15 12 10 7"/>
                <line x1="15" y1="12" x2="3" y2="12"/>
              </svg>
              Iniciar Sesión
            </span>
            <span v-else class="btn-inner">
              <div class="spinner"></div>
              Verificando...
            </span>
          </button>

          <!-- Error -->
          <transition name="err">
            <div v-if="error" class="error-box" role="alert">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="err-icon">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {{ error }}
            </div>
          </transition>
        </form>

        <p class="footer-copy">© 2026 Sembrando Vida · Administración</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/authService'

const router = useRouter()

const credentials = reactive({ username: '', password: '' })
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

const login = async () => {
  if (!credentials.username || !credentials.password) {
    error.value = 'Por favor completa todos los campos'
    return
  }
  loading.value = true
  error.value = ''
  try {
    const result = await authService.login(credentials)
    if (result.success) {
      router.push('/visor-map')
    } else {
      error.value = 'Credenciales incorrectas'
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'No se pudo conectar con el servidor'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ── Reset / base ── */
*, *::before, *::after { box-sizing: border-box; }

.login-page {
  min-height: 100vh;
  width: 100%;
  display: flex;
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
  color-scheme: light only;
  background: #f0fdf4;
}

/* ════════════════════════════════════════
   PANEL IZQUIERDO — imagen de cosecha
   ════════════════════════════════════════ */
.image-panel {
  display: none; /* oculto en móvil */
  position: relative;
  overflow: hidden;
  background:
    url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=85')
    center/cover no-repeat;
}

/* Filtro verde sobre la imagen */
.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    160deg,
    rgba(5, 46, 22, 0.82) 0%,
    rgba(20, 83, 45, 0.75) 35%,
    rgba(21, 128, 61, 0.68) 65%,
    rgba(34, 197, 94, 0.55) 100%
  );
  z-index: 1;
}

/* Contenido sobre la imagen */
.image-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 48px 40px;
  text-align: center;
  color: #fff;
}

.hero-leaf {
  width: 72px;
  height: 72px;
  margin-bottom: 20px;
  filter: drop-shadow(0 0 12px rgba(74, 222, 128, 0.6));
  animation: leafSway 4s ease-in-out infinite;
}
@keyframes leafSway {
  0%, 100% { transform: rotate(-3deg); }
  50%       { transform: rotate(3deg); }
}

.hero-title {
  font-size: clamp(26px, 2.8vw, 38px);
  font-weight: 800;
  letter-spacing: -0.5px;
  margin: 0 0 10px;
  text-shadow: 0 2px 20px rgba(0,0,0,0.4);
  background: linear-gradient(135deg, #fff 40%, #bbf7d0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 13px;
  color: rgba(255,255,255,0.7);
  margin: 0 0 28px;
  line-height: 1.6;
}

.hero-divider {
  width: 48px;
  height: 3px;
  background: linear-gradient(90deg, #4ade80, #86efac);
  border-radius: 99px;
  margin: 0 auto 24px;
}

.hero-tagline {
  font-size: 15px;
  font-weight: 600;
  color: rgba(255,255,255,0.9);
  line-height: 1.5;
  margin: 0 0 36px;
}

.hero-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 260px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 12px;
  padding: 10px 16px;
  text-align: left;
}

.stat-icon { font-size: 18px; }
.stat-label { font-size: 13px; color: rgba(255,255,255,0.9); font-weight: 500; }

/* Círculos decorativos flotantes */
.float-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  z-index: 1;
}
.fc-1 { width: 280px; height: 280px; top: -80px;  left: -80px;  animation: floatA 18s ease-in-out infinite; }
.fc-2 { width: 180px; height: 180px; bottom: 60px; right: -60px; animation: floatB 14s ease-in-out infinite; }
.fc-3 { width: 120px; height: 120px; bottom: 30%;  left: 15%;    animation: floatA 20s ease-in-out infinite 3s; }

@keyframes floatA {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50%       { transform: translate(20px, -30px) scale(1.05); }
}
@keyframes floatB {
  0%, 100% { transform: translate(0, 0); }
  50%       { transform: translate(-15px, 20px); }
}

/* ════════════════════════════════════════
   PANEL DERECHO — formulario
   ════════════════════════════════════════ */
.form-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  background: #fff;
  min-height: 100vh;
}

/* Logo visible solo en móvil */
.mobile-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 32px;
}
.mobile-leaf { width: 36px; height: 36px; }
.mobile-brand-name {
  font-size: 18px;
  font-weight: 700;
  color: #15803d;
  letter-spacing: -0.3px;
}

/* Caja del formulario */
.form-box {
  width: 100%;
  max-width: 400px;
  animation: slideUp 0.5s ease-out;
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

.form-header { margin-bottom: 32px; }

.form-title {
  font-size: 26px;
  font-weight: 800;
  color: #111827;
  margin: 0 0 6px;
  letter-spacing: -0.5px;
}

.form-desc {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

/* ── Campos ── */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  letter-spacing: 0.2px;
}

.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  color: #9ca3af;
  display: flex;
  align-items: center;
  pointer-events: none;
}
.input-icon svg { width: 18px; height: 18px; }

.input-wrap input {
  width: 100%;
  padding: 13px 44px;
  font-size: 15px;
  color: #111827;
  background: #f9fafb;
  border: 1.5px solid #e5e7eb;
  border-radius: 12px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
}
.input-wrap input::placeholder { color: #9ca3af; }
.input-wrap input:focus {
  background: #fff;
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.12);
}
.input-wrap input:disabled { opacity: 0.55; cursor: not-allowed; }

.eye-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  display: flex;
  align-items: center;
  padding: 4px;
  border-radius: 6px;
  transition: color 0.2s;
}
.eye-btn:hover:not(:disabled) { color: #16a34a; }
.eye-btn:disabled { cursor: not-allowed; opacity: 0.5; }
.eye-btn svg { width: 20px; height: 20px; }

/* ── Botón submit ── */
.submit-btn {
  width: 100%;
  padding: 14px 24px;
  margin-top: 4px;
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 14px rgba(21, 128, 61, 0.35);
  overflow: hidden;
  position: relative;
}
.submit-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0);
  transition: background 0.2s;
}
.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(21, 128, 61, 0.45);
}
.submit-btn:hover:not(:disabled)::after { background: rgba(255,255,255,0.08); }
.submit-btn:active:not(:disabled) { transform: translateY(0); }
.submit-btn:disabled {
  background: #d1d5db;
  box-shadow: none;
  cursor: not-allowed;
}

.btn-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  position: relative;
  z-index: 1;
}
.btn-icon { width: 20px; height: 20px; transition: transform 0.2s; }
.submit-btn:hover:not(:disabled) .btn-icon { transform: translateX(3px); }

.spinner {
  width: 20px; height: 20px;
  border: 2.5px solid rgba(255,255,255,0.35);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Error ── */
.error-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  color: #dc2626;
  font-size: 14px;
  font-weight: 500;
}
.err-icon { width: 18px; height: 18px; flex-shrink: 0; }

.err-enter-active, .err-leave-active { transition: all 0.25s ease; }
.err-enter-from, .err-leave-to { opacity: 0; transform: translateY(-6px); }

/* ── Footer ── */
.footer-copy {
  text-align: center;
  font-size: 12px;
  color: #9ca3af;
  margin: 28px 0 0;
}

/* ════════════════════════════════════════
   DESKTOP — layout split (≥ 1024px)
   ════════════════════════════════════════ */
@media (min-width: 1024px) {
  .image-panel {
    display: flex;
    width: 52%;
    flex-shrink: 0;
    min-height: 100vh;
  }
  .form-panel {
    width: 48%;
    padding: 60px 64px;
  }
  .mobile-brand { display: none; }
  .form-box { max-width: 420px; }
  .form-title { font-size: 30px; }
}

/* Pantallas grandes */
@media (min-width: 1440px) {
  .image-panel { width: 56%; }
  .form-panel  { width: 44%; padding: 60px 80px; }
}

/* ════════════════════════════════════════
   TABLET (768–1023px)
   ════════════════════════════════════════ */
@media (min-width: 768px) and (max-width: 1023px) {
  .form-panel { padding: 60px 80px; }
  .form-box   { max-width: 440px; }
}

/* ════════════════════════════════════════
   MÓVIL (< 768px) — fondo verde
   ════════════════════════════════════════ */
@media (max-width: 767px) {
  .login-page { background: linear-gradient(160deg, #14532d 0%, #15803d 50%, #16a34a 100%); }

  .form-panel {
    background: transparent;
    padding: 40px 20px;
  }

  .mobile-brand { display: flex; }
  .mobile-brand-name { color: #bbf7d0; }

  .form-box {
    background: #fff;
    border-radius: 24px;
    padding: 32px 24px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
  }

  .form-title { font-size: 22px; }
  .footer-copy { color: rgba(255,255,255,0.5); margin-top: 20px; }
}

/* Móvil pequeño */
@media (max-width: 380px) {
  .form-panel { padding: 32px 16px; }
  .form-box   { padding: 28px 20px; }
}

/* Altura baja (landscape móvil) */
@media (max-height: 600px) and (orientation: landscape) {
  .form-panel { padding: 24px 20px; justify-content: flex-start; }
  .mobile-brand { margin-bottom: 16px; }
  .login-form { gap: 14px; }
}
</style>
