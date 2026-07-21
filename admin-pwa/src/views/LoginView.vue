<template>
  <div class="login-page">

    <!-- ═══ PANEL IZQUIERDO — imagen de campo (solo desktop) ═══ -->
    <aside class="image-panel" aria-hidden="true">
      <div class="image-overlay"></div>

      <div class="image-content">
        <!-- Marca desvanecida, pequeña: identifica el programa -->
        <p class="hero-brand">Sembrando Vida</p>

        <!-- Título principal del panel: más grande que la marca -->
        <h1 class="hero-title">Administrador</h1>

        <p class="hero-subtitle">Subsecretaría de Inclusión Productiva<br>y Desarrollo Rural</p>

        <div class="hero-divider"></div>

        <p class="hero-tagline">App de Seguimiento</p>

        <div class="hero-stats">
          <div class="stat">
            <span class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
              </svg>
            </span>
            <span class="stat-label">Seguimiento en tiempo real</span>
          </div>
          <div class="stat">
            <span class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
            </span>
            <span class="stat-label">Geolocalización precisa</span>
          </div>
          <div class="stat">
            <span class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
            </span>
            <span class="stat-label">Reportes y estadísticas</span>
          </div>
        </div>
      </div>

      <div class="float-circle fc-1"></div>
      <div class="float-circle fc-2"></div>
      <div class="float-circle fc-3"></div>
    </aside>

    <!-- ═══ PANEL DERECHO — formulario ═══ -->
    <main class="form-panel">
      <div class="form-box">

        <!-- Encabezado del formulario -->
        <div class="form-header">
          <h2 class="form-title">Iniciar sesión</h2>
          <p class="form-desc">Ingresa tus credenciales para acceder al panel</p>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="login" class="login-form" novalidate>
          <!-- Usuario -->
          <div class="form-group">
            <label for="username" class="form-label">Correo electrónico</label>
            <div class="input-wrap">
              <span class="input-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
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
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
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
                <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Botón submit -->
          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading" class="btn-inner">
              Iniciar sesión
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </span>
            <span v-else class="btn-inner">
              <span class="spinner"></span>
              Verificando
            </span>
          </button>

          <!-- Error -->
          <transition name="err">
            <div v-if="error" class="error-box" role="alert">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="err-icon">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {{ error }}
            </div>
          </transition>
        </form>

        <p class="footer-copy">© 2026 Sembrando Vida · Panel de Administración</p>
      </div>
    </main>

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

/*
 * Tipografía estilo Apple: system-ui prioriza San Francisco en macOS/iOS,
 * con pesos intermedios (500/590) y tracking negativo sutil en títulos.
 */
.login-page {
  height: 100vh;
  width: 100%;
  display: flex;
  overflow: hidden; /* sin scroll a ningún zoom: todo escala con vh/clamp */
  font-family: -apple-system, 'SF Pro Display', 'Inter', system-ui, 'Segoe UI', sans-serif;
  color-scheme: light only;
  background: #fff;
}

/* ════════════════════════════════════════
   PANEL IZQUIERDO — imagen de cosecha
   ════════════════════════════════════════ */
.image-panel {
  display: none;
  position: relative;
  overflow: hidden;
  background:
    url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=85')
    center/cover no-repeat;
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    160deg,
    rgba(5, 46, 22, 0.85) 0%,
    rgba(20, 83, 45, 0.78) 35%,
    rgba(21, 128, 61, 0.70) 65%,
    rgba(34, 197, 94, 0.56) 100%
  );
  z-index: 1;
}

.image-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: clamp(24px, 5vh, 48px) clamp(28px, 4vw, 44px);
  text-align: center;
  color: #fff;
  overflow: hidden;
}

/* Marca "Sembrando Vida" — pequeña, desvanecida, estática (sin animación) */
.hero-brand {
  font-size: clamp(12px, 1.7vh, 15px);
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin: 0 0 clamp(4px, 1vh, 10px);
  flex-shrink: 0;
  background: linear-gradient(90deg, rgba(187,247,208,0.55) 0%, rgba(74,222,128,0.85) 50%, rgba(187,247,208,0.55) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Título principal "Administrador" — más grande que la marca */
.hero-title {
  font-size: clamp(30px, 5.6vh, 48px);
  font-weight: 800;
  letter-spacing: -1.2px;
  margin: 0 0 clamp(6px, 1.2vh, 10px);
  flex-shrink: 0;
  line-height: 1.05;
  color: #fff;
  text-shadow: 0 2px 20px rgba(0,0,0,0.35);
}

.hero-subtitle {
  font-size: clamp(11px, 1.6vh, 13px);
  font-weight: 400;
  color: rgba(255,255,255,0.68);
  margin: 0 0 clamp(14px, 2.6vh, 28px);
  line-height: 1.55;
  flex-shrink: 0;
}

.hero-divider {
  width: 44px;
  height: 2.5px;
  background: linear-gradient(90deg, #4ade80, #86efac);
  border-radius: 99px;
  margin: 0 auto clamp(12px, 2.2vh, 24px);
  flex-shrink: 0;
}

.hero-tagline {
  font-size: clamp(13px, 1.9vh, 15.5px);
  font-weight: 590;
  letter-spacing: -0.2px;
  color: rgba(255,255,255,0.92);
  line-height: 1.5;
  margin: 0 0 clamp(18px, 3.4vh, 36px);
  flex-shrink: 0;
}

.hero-stats {
  display: flex;
  flex-direction: column;
  gap: clamp(6px, 1.2vh, 12px);
  width: 100%;
  max-width: 270px;
  flex-shrink: 0;
}

.stat {
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.4vw, 12px);
  background: rgba(255,255,255,0.09);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.16);
  border-radius: clamp(10px, 1.4vh, 13px);
  padding: clamp(8px, 1.4vh, 11px) clamp(12px, 1.8vw, 16px);
  text-align: left;
  transition: background 0.25s ease, transform 0.25s ease;
}
.stat:hover {
  background: rgba(255,255,255,0.14);
  transform: translateX(3px);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: clamp(26px, 4vh, 32px);
  height: clamp(26px, 4vh, 32px);
  flex-shrink: 0;
  background: rgba(74,222,128,0.16);
  border-radius: 8px;
  color: #86efac;
}
.stat-icon svg { width: 55%; height: 55%; }
.stat-label {
  font-size: clamp(11px, 1.5vh, 13px);
  color: rgba(255,255,255,0.92);
  font-weight: 500;
  letter-spacing: -0.1px;
}

/* Círculos decorativos flotantes */
.float-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255,255,255,0.055);
  border: 1px solid rgba(255,255,255,0.1);
  z-index: 1;
  pointer-events: none;
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
   PANEL DERECHO — formulario, sin scroll
   ════════════════════════════════════════ */
/*
 * Fondo "canvas fluido": dos manchas radiales verdes que se
 * desplazan y respiran en bucle, evocando hojas/campo en movimiento
 * sin ser literales — un fondo vivo y moderno detrás de la tarjeta.
 */
.form-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  overflow: hidden;
  padding: clamp(12px, 3vw, 40px);
  /* Degradado verde oscuro — continúa la paleta del panel izquierdo,
     así ambos lados se sienten como una sola escena, no dos fondos distintos */
  background: linear-gradient(200deg, #0a2e1a 0%, #0f3d22 45%, #12472a 100%);
  position: relative;
}

.form-panel::before,
.form-panel::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  pointer-events: none;
  z-index: 0;
}
.form-panel::before {
  width: 55vw;
  height: 55vw;
  max-width: 640px;
  max-height: 640px;
  top: -18%;
  right: -14%;
  background: radial-gradient(circle, rgba(74,222,128,0.22) 0%, rgba(74,222,128,0) 70%);
  animation: canvasDrift1 16s ease-in-out infinite;
}
.form-panel::after {
  width: 46vw;
  height: 46vw;
  max-width: 520px;
  max-height: 520px;
  bottom: -16%;
  left: -12%;
  background: radial-gradient(circle, rgba(21,128,61,0.30) 0%, rgba(21,128,61,0) 70%);
  animation: canvasDrift2 20s ease-in-out infinite;
}
@keyframes canvasDrift1 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50%       { transform: translate(-30px, 40px) scale(1.12); }
}
@keyframes canvasDrift2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50%       { transform: translate(25px, -35px) scale(1.08); }
}

/* Caja del formulario — tarjeta verde fuerte */
.form-box {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  max-height: calc(100vh - clamp(16px, 4vh, 60px));
  display: flex;
  flex-direction: column;

  background: linear-gradient(155deg, #1b7a3d 0%, #166534 55%, #124d29 100%);
  border-radius: clamp(18px, 2.4vw, 28px);
  padding: clamp(22px, 3.6vh, 44px) clamp(20px, 3.2vw, 40px);
  border: 1px solid rgba(255,255,255,0.12);

  box-shadow:
    0 1px 0 0 rgba(255,255,255,0.16) inset,
    0 0 0 1px rgba(74,222,128,0.08),
    0 30px 70px rgba(0,0,0,0.5),
    0 10px 28px rgba(0,0,0,0.35),
    0 0 60px rgba(34,197,94,0.10);

  animation: slideUp 0.55s cubic-bezier(0.22, 1, 0.36, 1);
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.form-header {
  margin-bottom: clamp(14px, 2.8vh, 30px);
  flex-shrink: 0;
}

.form-title {
  font-size: clamp(19px, 3.2vh, 28px);
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 clamp(3px, 0.6vh, 7px);
  letter-spacing: -0.6px;
}

.form-desc {
  font-size: clamp(11px, 1.5vh, 14px);
  font-weight: 400;
  color: #bcdec9;
  margin: 0;
  letter-spacing: -0.1px;
}

/* ── Campos ── */
.login-form {
  display: flex;
  flex-direction: column;
  gap: clamp(10px, 1.8vh, 20px);
  flex-shrink: 0;
}

.form-group { display: flex; flex-direction: column; gap: clamp(3px, 0.7vh, 6px); }

.form-label {
  font-size: clamp(11px, 1.5vh, 13px);
  font-weight: 600;
  color: #d7ecdf;
  letter-spacing: 0.1px;
}

.input-wrap { position: relative; display: flex; align-items: center; }

.input-icon {
  position: absolute;
  left: 14px;
  color: #7fae8e;
  display: flex;
  align-items: center;
  pointer-events: none;
  transition: color 0.2s ease;
}
.input-icon svg { width: 17px; height: 17px; }

.input-wrap input {
  width: 100%;
  padding: clamp(9px, 1.6vh, 13px) 44px;
  font-size: clamp(13px, 1.7vh, 15px);
  font-family: inherit;
  color: #0b1120;
  background: rgba(255,255,255,0.92);
  border: 1.5px solid rgba(255,255,255,0.15);
  border-radius: 13px;
  outline: none;
  transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
}
.input-wrap input::placeholder { color: #9aa8a1; }
.input-wrap input:focus {
  background: #fff;
  border-color: #4ade80;
  box-shadow: 0 0 0 4px rgba(74, 222, 128, 0.22);
}
.input-wrap input:focus ~ .input-icon,
.input-wrap:focus-within .input-icon { color: #16a34a; }
.input-wrap input:disabled { opacity: 0.55; cursor: not-allowed; }

.eye-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #7fae8e;
  display: flex;
  align-items: center;
  padding: 4px;
  border-radius: 7px;
  transition: color 0.2s ease, background 0.2s ease;
}
.eye-btn:hover:not(:disabled) { color: #16a34a; background: rgba(22,163,74,0.1); }
.eye-btn:disabled { cursor: not-allowed; opacity: 0.5; }
.eye-btn svg { width: 18px; height: 18px; }

/* ── Botón submit — blanco sólido, contraste máximo sobre la tarjeta verde ── */
.submit-btn {
  width: 100%;
  padding: clamp(10px, 1.8vh, 14px) 24px;
  margin-top: clamp(2px, 0.5vh, 6px);
  font-size: clamp(13px, 1.8vh, 15px);
  font-weight: 700;
  font-family: inherit;
  letter-spacing: -0.1px;
  color: #14532d;
  background: #ffffff;
  border: none;
  border-radius: 13px;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1), 0 10px 24px rgba(0,0,0,0.22);
  position: relative;
  overflow: hidden;
}
.submit-btn:hover:not(:disabled) {
  background: #f0fdf4;
  transform: translateY(-1px);
  box-shadow: 0 1px 2px rgba(0,0,0,0.12), 0 14px 30px rgba(0,0,0,0.28);
}
.submit-btn:active:not(:disabled) { transform: translateY(0) scale(0.99); }
.submit-btn:disabled {
  background: rgba(255,255,255,0.35);
  color: rgba(20,83,45,0.5);
  box-shadow: none;
  cursor: not-allowed;
}

.btn-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  z-index: 1;
}
.btn-icon { width: 17px; height: 17px; transition: transform 0.2s ease; }
.submit-btn:hover:not(:disabled) .btn-icon { transform: translateX(3px); }

.spinner {
  width: 15px; height: 15px;
  border: 2px solid rgba(255,255,255,0.35);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Error ── */
.error-box {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 11px 14px;
  background: rgba(254,242,242,0.95);
  border: 1px solid #fecaca;
  border-radius: 11px;
  color: #dc2626;
  font-size: clamp(11px, 1.5vh, 13.5px);
  font-weight: 500;
}
.err-icon { width: 16px; height: 16px; flex-shrink: 0; }

.err-enter-active, .err-leave-active { transition: all 0.25s ease; }
.err-enter-from, .err-leave-to { opacity: 0; transform: translateY(-6px); }

/* ── Footer ── */
.footer-copy {
  text-align: center;
  font-size: clamp(9.5px, 1.2vh, 11.5px);
  color: #8fbb9e;
  margin: clamp(14px, 2.4vh, 26px) 0 0;
  flex-shrink: 0;
}

/* ════════════════════════════════════════
   DESKTOP — layout split (≥ 1024px)
   ════════════════════════════════════════ */
@media (min-width: 1024px) {
  .image-panel {
    display: flex;
    width: 52%;
    flex-shrink: 0;
    height: 100vh;
    overflow: hidden;
  }
  .form-panel { width: 48%; }
}

@media (min-width: 1440px) {
  .image-panel { width: 56%; }
  .form-panel  { width: 44%; }
}

/* ════════════════════════════════════════
   MÓVIL (< 1024px) — tarjeta sobre fondo de campo
   ════════════════════════════════════════ */
@media (max-width: 1023px) {
  .login-page {
    background:
      linear-gradient(160deg, rgba(5,46,22,0.93) 0%, rgba(20,83,45,0.88) 45%, rgba(21,128,61,0.82) 100%),
      url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=900&q=80') center/cover no-repeat;
  }
  .form-panel { background: transparent; }
  .form-panel::before,
  .form-panel::after { display: none; }

  .form-box {
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    border-radius: clamp(18px, 3vw, 26px);
    padding: clamp(22px, 4.5vw, 36px) clamp(20px, 4vw, 30px);
    box-shadow: 0 24px 64px rgba(0,0,0,0.4), 0 1px 0 0 rgba(255,255,255,0.15) inset;
  }

  /* Input font-size mínimo 16px evita zoom automático de iOS */
  .input-wrap input { font-size: max(16px, clamp(13px, 1.7vh, 15px)); }
}

@media (max-width: 380px) {
  .form-box { padding: 20px 16px; }
}

/* Landscape móvil */
@media (max-height: 560px) and (orientation: landscape) {
  .form-header { margin-bottom: 12px; }
  .login-form { gap: 10px; }
  .footer-copy { margin-top: 12px; }
}
</style>
