<template>
  <div class="login-page">

    <!-- ═══ PANEL IZQUIERDO — imagen de cosecha (solo desktop) ═══ -->
    <div class="image-panel" aria-hidden="true">
      <div class="image-overlay"></div>
      <div class="image-content">
        <img src="/images/logosv.png" alt="Sembrando Vida" class="hero-logo" />
        <h1 class="hero-title">Sembrando Vida</h1>
        <p class="hero-sub">Subsecretaría de Inclusión Productiva<br>y Desarrollo Rural</p>
        <div class="hero-divider"></div>
        <p class="hero-tagline">Aplicación de Seguimiento<br>para Técnicos de Campo</p>
        <div class="hero-features">
          <div class="feat"><span class="feat-dot"></span>Registro de asistencias en tiempo real</div>
          <div class="feat"><span class="feat-dot"></span>Geolocalización y mapas</div>
          <div class="feat"><span class="feat-dot"></span>Funcionamiento sin conexión</div>
          <div class="feat"><span class="feat-dot"></span>Reportes y seguimiento</div>
        </div>
      </div>
      <div class="fc fc-1"></div>
      <div class="fc fc-2"></div>
      <div class="fc fc-3"></div>
    </div>

    <!-- ═══ PANEL DERECHO — formulario ═══ -->
    <div class="form-panel">
      <div class="form-box">

        <!-- Logo + branding arriba (siempre visible) -->
        <div class="form-head">
          <img src="/images/logosv.png" alt="Sembrando Vida" class="form-logo" />
          <h2 class="form-title">Aplicación de <span class="title-accent">Seguimiento</span></h2>
          <div class="title-line"></div>
          <p class="form-subtitle">Iniciar sesión</p>
          <p class="form-hint">Ingresa tus credenciales para acceder</p>
        </div>

        <!-- Error -->
        <transition name="bounce">
          <div v-if="errorMessage" class="error-box" role="alert">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="err-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            {{ errorMessage }}
          </div>
        </transition>

        <!-- Formulario -->
        <form @submit.prevent="login" novalidate>
          <div class="fields">
            <!-- Email -->
            <div class="field">
              <label for="email" class="field-label">Correo electrónico</label>
              <div class="input-wrap">
                <span class="ico">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                    <polyline points="22,6 12,13 2,6"/>
                  </svg>
                </span>
                <input
                  v-model="email"
                  id="email"
                  type="email"
                  autocomplete="email"
                  required
                  placeholder="nombre@ejemplo.com"
                  :class="{ shake: formError }"
                  :disabled="loading"
                />
              </div>
            </div>

            <!-- Contraseña -->
            <div class="field">
              <label for="password" class="field-label">Contraseña</label>
              <div class="input-wrap">
                <span class="ico">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                </span>
                <input
                  v-model="password"
                  id="password"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="current-password"
                  required
                  placeholder="••••••••"
                  :class="{ shake: formError }"
                  :disabled="loading"
                />
                <button type="button" class="eye-btn" @click="togglePasswordVisibility" :disabled="loading">
                  <svg v-if="showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Botón -->
          <button type="submit" class="submit-btn" :disabled="loading">
            <svg v-if="loading" class="spin-icon" fill="none" viewBox="0 0 24 24">
              <circle class="op25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="op75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            {{ loading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
          </button>
        </form>

        <!-- Links -->
        <div class="links">
          <p>¿No tienes cuenta? <router-link to="/register" class="link">Crear cuenta</router-link></p>
          <p><router-link to="/forgot-password" class="link">¿Olvidaste tu contraseña?</router-link></p>
        </div>
      </div>

        <p class="footer-copy">© 2025 Sembrando Vida</p>
      </div><!-- /form-box -->
    </div><!-- /form-panel -->

    <SupportBubbleLogin />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { API_URL } from '../utils/network.js';
import SupportBubbleLogin from '../components/SupportBubbleLogin.vue';
import { enviarInfoDispositivo } from '../services/dispositivoTrackingService.js';

const router = useRouter();
const email = ref('');
const password = ref('');
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref('');
const formError = ref(false);
const retryCount = ref(0);
const MAX_RETRIES = 2;

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}

async function intentarLogin(correo, contrasena) {
  const response = await axios.post(`${API_URL}/login`, {
    correo,
    contrasena
  }, {
    timeout: 30000,
    headers: { 'Content-Type': 'application/json' }
  });
  return response.data;
}

async function login() {
  if (!email.value || !password.value) {
    errorMessage.value = 'Por favor, completa todos los campos';
    formError.value = true;
    return;
  }

  loading.value = true;
  errorMessage.value = '';
  formError.value = false;
  retryCount.value = 0;

  let lastError = null;

  for (let intento = 0; intento <= MAX_RETRIES; intento++) {
    if (intento > 0) {
      errorMessage.value = `Reintentando conexión (${intento}/${MAX_RETRIES})...`;
      await new Promise(r => setTimeout(r, 3000 * intento));
    }

    try {
      const userData = await intentarLogin(email.value, password.value);
      localStorage.setItem('user', JSON.stringify(userData));
      enviarInfoDispositivo(userData.id).catch(() => {});
      sessionStorage.setItem('justLoggedIn', 'true');
      window.location.href = '/';
      return;
    } catch (error) {
      lastError = error;
      if (error.response) {
        const status = error.response.status;
        if (status === 401) {
          errorMessage.value = 'Credenciales incorrectas. Verifica tu email y contraseña.';
        } else if (status === 403) {
          errorMessage.value = error.response.data?.detail || 'Tu cuenta ha sido desactivada. Contacta al administrador.';
        } else if (status === 500) {
          errorMessage.value = 'Error del servidor. Inténtalo de nuevo en unos minutos.';
        } else {
          errorMessage.value = error.response.data?.detail || 'Error al iniciar sesión.';
        }
        formError.value = true;
        loading.value = false;
        return;
      }
      retryCount.value = intento + 1;
    }
  }

  formError.value = true;
  loading.value = false;
  errorMessage.value = !navigator.onLine
    ? 'Sin conexión a internet. Conéctate a una red y vuelve a intentar.'
    : 'No se pudo conectar con el servidor. La red puede ser lenta — intenta de nuevo en unos segundos.';
}
</script>

<style scoped>
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
   PANEL IZQUIERDO
   ════════════════════════════════════════ */
.image-panel {
  display: none;
  position: relative;
  overflow: hidden;
  background:
    url('https://images.unsplash.com/photo-1574943320219-553eb213f72d?auto=format&fit=crop&w=1200&q=85')
    center/cover no-repeat;
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    155deg,
    rgba(2, 44, 18, 0.88) 0%,
    rgba(14, 79, 34, 0.80) 30%,
    rgba(21, 128, 61, 0.72) 65%,
    rgba(22, 163, 74, 0.60) 100%
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
  padding: 56px 44px;
  text-align: center;
  color: #fff;
}

.hero-logo {
  width: 130px;
  height: 130px;
  object-fit: contain;
  margin-bottom: 20px;
  filter: drop-shadow(0 4px 20px rgba(0,0,0,0.35));
  animation: logoBob 4s ease-in-out infinite;
}
@keyframes logoBob {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-8px); }
}

.hero-title {
  font-size: clamp(24px, 2.5vw, 36px);
  font-weight: 800;
  letter-spacing: -0.5px;
  margin: 0 0 8px;
  background: linear-gradient(135deg, #fff 40%, #bbf7d0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: none;
}

.hero-sub {
  font-size: 12.5px;
  color: rgba(255,255,255,0.65);
  margin: 0 0 24px;
  line-height: 1.6;
}

.hero-divider {
  width: 44px; height: 3px;
  background: linear-gradient(90deg, #4ade80, #86efac);
  border-radius: 99px;
  margin: 0 auto 20px;
}

.hero-tagline {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255,255,255,0.88);
  line-height: 1.5;
  margin: 0 0 32px;
}

.hero-features {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  max-width: 250px;
  text-align: left;
}
.feat {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: rgba(255,255,255,0.85);
  font-weight: 500;
}
.feat-dot {
  width: 7px; height: 7px;
  background: #4ade80;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 6px rgba(74, 222, 128, 0.6);
}

/* Círculos decorativos */
.fc {
  position: absolute;
  border-radius: 50%;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.09);
  z-index: 1;
}
.fc-1 { width: 300px; height: 300px; top: -80px; left: -80px; animation: fa 18s ease-in-out infinite; }
.fc-2 { width: 200px; height: 200px; bottom: 40px; right: -60px; animation: fb 15s ease-in-out infinite; }
.fc-3 { width: 130px; height: 130px; bottom: 28%; left: 10%; animation: fa 22s ease-in-out infinite 3s; }
@keyframes fa { 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(16px,-24px) scale(1.04)} }
@keyframes fb { 0%,100%{transform:translate(0,0)} 50%{transform:translate(-12px,18px)} }

/* ════════════════════════════════════════
   PANEL DERECHO
   ════════════════════════════════════════ */
.form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  background: #fff;
  min-height: 100vh;
}

/* Caja del formulario — centrada y compacta */
.form-box {
  width: 100%;
  max-width: 360px;
  animation: up 0.45s ease-out;
}
@keyframes up {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Cabecera con logo ── */
.form-head {
  text-align: center;
  margin-bottom: 28px;
}

.form-logo {
  width: 88px;
  height: 88px;
  object-fit: contain;
  margin: 0 auto 14px;
  display: block;
  filter: drop-shadow(0 4px 12px rgba(21,128,61,0.2));
}

.form-title {
  font-size: 21px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 8px;
  letter-spacing: -0.3px;
  line-height: 1.3;
}
.title-accent {
  color: #16a34a;
  font-weight: 800;
}

.title-line {
  width: 44px;
  height: 2.5px;
  background: linear-gradient(90deg, #16a34a, #4ade80, #16a34a);
  border-radius: 99px;
  margin: 0 auto 14px;
  animation: glow 2s ease-in-out infinite alternate;
}
@keyframes glow {
  from { box-shadow: 0 0 4px rgba(34,197,94,0.3); }
  to   { box-shadow: 0 0 10px rgba(34,197,94,0.5); }
}

.form-subtitle {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 4px;
}
.form-hint {
  font-size: 12.5px;
  color: #9ca3af;
  margin: 0;
}

/* Error */
.error-box {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  background: #fef2f2;
  border-left: 4px solid #ef4444;
  border-radius: 10px;
  color: #b91c1c;
  font-size: 13.5px;
  font-weight: 500;
  margin-bottom: 18px;
}
.err-icon { width: 18px; height: 18px; flex-shrink: 0; margin-top: 1px; }

/* Campos */
.fields { display: flex; flex-direction: column; gap: 18px; }
.field  { display: flex; flex-direction: column; gap: 5px; }
.field-label { font-size: 12.5px; font-weight: 600; color: #374151; }

.input-wrap { position: relative; display: flex; align-items: center; }
.ico {
  position: absolute; left: 13px;
  color: #9ca3af; display: flex; align-items: center; pointer-events: none;
}
.ico svg { width: 16px; height: 16px; }

.input-wrap input {
  width: 100%;
  padding: 12px 44px;
  font-size: 15px;
  color: #111827;
  background: rgba(249, 250, 251, 0.9);
  backdrop-filter: blur(10px);
  border: 1.5px solid rgba(255,255,255,0.3);
  border-radius: 12px;
  outline: none;
  transition: all 0.25s ease;
  box-shadow: 0 4px 16px rgba(31,38,135,0.08), inset 0 1px 0 rgba(255,255,255,0.2);
}
.input-wrap input::placeholder { color: rgba(107,114,128,0.6); }
.input-wrap input:focus {
  border-color: rgba(76,175,80,0.5);
  background: rgba(255,255,255,0.95);
  box-shadow: 0 0 0 3px rgba(76,175,80,0.12), 0 8px 25px rgba(31,38,135,0.1), inset 0 1px 0 rgba(255,255,255,0.3);
  transform: translateY(-1px);
}
.input-wrap input:disabled { opacity: 0.55; cursor: not-allowed; }

.eye-btn {
  position: absolute; right: 10px;
  background: none; border: none; cursor: pointer;
  color: #9ca3af; display: flex; align-items: center;
  padding: 6px; border-radius: 6px;
  transition: color 0.2s;
}
.eye-btn:hover:not(:disabled) { color: #16a34a; }
.eye-btn:disabled { cursor: not-allowed; opacity: 0.5; }
.eye-btn svg { width: 18px; height: 18px; }

/* Shake */
@keyframes shake {
  0%,100% { transform: translateX(0); }
  15%,45%,75% { transform: translateX(-5px); }
  30%,60%,90% { transform: translateX(5px); }
}
.shake { animation: shake 0.6s cubic-bezier(.36,.07,.19,.97) both; }

/* Botón submit */
.submit-btn {
  width: 100%;
  margin-top: 22px;
  padding: 13px 24px;
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, rgba(76,175,80,0.9) 0%, rgba(56,142,60,0.9) 100%);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(76,175,80,0.3);
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.25s ease;
  box-shadow: 0 4px 20px rgba(76,175,80,0.35), inset 0 1px 0 rgba(255,255,255,0.2);
  position: relative;
  overflow: hidden;
}
.submit-btn::before {
  content: '';
  position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
  transition: left 0.45s;
}
.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(76,175,80,0.45), inset 0 1px 0 rgba(255,255,255,0.3);
}
.submit-btn:hover:not(:disabled)::before { left: 100%; }
.submit-btn:active:not(:disabled) { transform: translateY(0); }
.submit-btn:disabled { opacity: 0.55; cursor: not-allowed; transform: none; box-shadow: none; }

.spin-icon { width: 18px; height: 18px; animation: spin 0.75s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.op25 { opacity: 0.25; }
.op75 { opacity: 0.75; }

/* Links */
.links {
  text-align: center;
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.links p { margin: 0; font-size: 12.5px; color: #6b7280; }
.link {
  font-weight: 600;
  color: #16a34a;
  text-decoration: none;
  position: relative;
  transition: color 0.2s;
}
.link::after {
  content: '';
  position: absolute; bottom: -1px; left: 0;
  width: 0; height: 1.5px;
  background: linear-gradient(90deg, #16a34a, #4ade80);
  border-radius: 99px;
  transition: width 0.25s ease;
}
.link:hover { color: #15803d; }
.link:hover::after { width: 100%; }

.footer-copy {
  margin-top: 32px;
  font-size: 12px;
  color: #9ca3af;
}

/* Bounce transition */
.bounce-enter-active { animation: bounceIn 0.4s; }
.bounce-leave-active { animation: bounceIn 0.3s reverse; }
@keyframes bounceIn {
  0%   { transform: scale(0.8); opacity: 0; }
  60%  { transform: scale(1.03); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
}

/* ════════════════════════════════════════
   DESKTOP ≥ 1024px — split screen
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
    padding: 48px 56px;
  }
  .form-logo  { width: 80px; height: 80px; }
  .form-title { font-size: 20px; }
}

@media (min-width: 1440px) {
  .image-panel { width: 55%; }
  .form-panel  { width: 45%; padding: 48px 72px; }
  .form-logo   { width: 88px; height: 88px; }
}

/* ════════════════════════════════════════
   TABLET 768–1023px
   ════════════════════════════════════════ */
@media (min-width: 768px) and (max-width: 1023px) {
  .form-panel { padding: 48px 64px; }
  .form-box   { max-width: 380px; }
}

/* ════════════════════════════════════════
   MÓVIL — fondo verde, tarjeta blanca
   ════════════════════════════════════════ */
@media (max-width: 767px) {
  .login-page {
    background: linear-gradient(155deg, #052e16 0%, #14532d 30%, #15803d 70%, #16a34a 100%);
  }
  .form-panel {
    background: transparent;
    padding: 32px 18px;
    align-items: center;
    justify-content: center;
  }
  .form-box {
    background: rgba(255,255,255,0.97);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 24px;
    padding: 28px 22px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.4);
  }
  .footer-copy { color: #9ca3af; }
  .input-wrap input { font-size: 16px; } /* evita zoom iOS */
}

@media (max-width: 380px) {
  .form-panel { padding: 24px 14px; }
  .form-box   { padding: 24px 18px; border-radius: 20px; }
  .form-logo  { width: 72px; height: 72px; }
}

/* Landscape móvil */
@media (max-height: 600px) and (orientation: landscape) {
  .form-panel { padding: 16px 18px; }
  .form-logo  { width: 56px; height: 56px; margin-bottom: 8px; }
  .fields { gap: 12px; }
  .form-head { margin-bottom: 14px; }
  .submit-btn { margin-top: 14px; }
}

/* Fallback sin backdrop-filter */
@supports not (backdrop-filter: blur(20px)) {
  .form-box { background: #fff; }
}
</style>
