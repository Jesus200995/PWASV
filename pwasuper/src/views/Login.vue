<template>
  <div class="root">

    <!-- ══════════════════════════════════════
         PANEL IZQUIERDO — naturaleza sin personas
         ══════════════════════════════════════ -->
    <aside class="left-panel" aria-hidden="true">
      <div class="left-overlay"></div>

      <!-- Contenido encima de la imagen -->
      <div class="left-body">
        <!-- Badge institucional -->
        <div class="badge">
          <span class="badge-dot"></span>
          Sistema Oficial de Seguimiento
        </div>

        <!-- Título grande -->
        <h1 class="left-heading">
          Sembrando<br>
          <span class="left-heading-accent">Vida</span>
        </h1>

        <p class="left-desc">
          Subsecretaría de Inclusión Productiva<br>y Desarrollo Rural
        </p>

        <!-- Separador -->
        <div class="left-sep"></div>

        <!-- Stats / pilares -->
        <div class="pillars">
          <div class="pillar">
            <span class="pillar-ico">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
            </span>
            <div class="pillar-text">Geolocalización<br>en tiempo real</div>
          </div>
          <div class="pillar">
            <span class="pillar-ico">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10 9 9 9 8 9"/>
              </svg>
            </span>
            <div class="pillar-text">Registro de<br>asistencias</div>
          </div>
          <div class="pillar">
            <span class="pillar-ico">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <line x1="1" y1="6" x2="23" y2="6"/>
                <line x1="1" y1="10" x2="17" y2="10"/>
                <line x1="1" y1="14" x2="11" y2="14"/>
                <line x1="1" y1="18" x2="7" y2="18"/>
              </svg>
            </span>
            <div class="pillar-text">Modo<br>sin conexión</div>
          </div>
        </div>
      </div>

      <!-- Círculos decorativos -->
      <div class="deco d1"></div>
      <div class="deco d2"></div>
      <div class="deco d3"></div>
    </aside>

    <!-- ══════════════════════════════════════
         PANEL DERECHO — formulario
         ══════════════════════════════════════ -->
    <main class="right-panel">
      <div class="form-card">

        <!-- Logo único -->
        <div class="brand">
          <img src="/images/logosv.png" alt="Sembrando Vida" class="brand-logo" />
        </div>

        <!-- Línea divisoria desvanecida -->
        <div class="brand-divider" aria-hidden="true"></div>

        <!-- Encabezado -->
        <div class="form-header">
          <h2 class="form-title" aria-label="App de Seguimiento">
            <span
              v-for="(char, i) in titleChars"
              :key="i"
              class="title-char"
              :style="{ animationDelay: `${i * 0.06}s` }"
            >{{ char === ' ' ? ' ' : char }}</span>
          </h2>
          <p class="form-sub">Ingresa tus credenciales para continuar</p>
        </div>

        <!-- Alerta error -->
        <transition name="slide-down">
          <div v-if="errorMessage" class="alert-error" role="alert">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="alert-ico">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            {{ errorMessage }}
          </div>
        </transition>

        <!-- Form -->
        <form @submit.prevent="login" novalidate class="form">

          <div class="field">
            <label for="email" class="label">Correo electrónico</label>
            <div class="inp-wrap">
              <span class="inp-ico">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
              </span>
              <input
                v-model="email"
                id="email"
                type="email"
                autocomplete="email"
                placeholder="nombre@ejemplo.com"
                required
                :disabled="loading"
                :class="{ 'inp-shake': formError }"
                class="inp"
              />
            </div>
          </div>

          <div class="field">
            <label for="password" class="label">Contraseña</label>
            <div class="inp-wrap">
              <span class="inp-ico">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
              </span>
              <input
                v-model="password"
                id="password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="current-password"
                placeholder="••••••••"
                required
                :disabled="loading"
                :class="{ 'inp-shake': formError }"
                class="inp"
              />
              <button type="button" class="eye" @click="togglePasswordVisibility" :disabled="loading" tabindex="-1">
                <svg v-if="showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
              </button>
            </div>
          </div>

          <button type="submit" class="btn-submit" :disabled="loading">
            <svg v-if="loading" class="spin" fill="none" viewBox="0 0 24 24">
              <circle style="opacity:.25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path style="opacity:.75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            <span>{{ loading ? 'Verificando...' : 'Iniciar sesión' }}</span>
          </button>

        </form>

        <!-- Links -->
        <div class="form-links">
          <p>¿No tienes cuenta? <router-link to="/register" class="flink">Crear cuenta</router-link></p>
          <router-link to="/forgot-password" class="flink flink-sm">¿Olvidaste tu contraseña?</router-link>
        </div>

        <p class="copy">© 2026 Sembrando Vida · Todos los derechos reservados</p>

      </div><!-- /form-card -->
    </main>

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
const MAX_RETRIES = 2;

const titleChars = 'App de Seguimiento'.split('');

function togglePasswordVisibility() { showPassword.value = !showPassword.value; }

async function intentarLogin(correo, contrasena) {
  const r = await axios.post(`${API_URL}/login`, { correo, contrasena }, {
    timeout: 30000, headers: { 'Content-Type': 'application/json' }
  });
  return r.data;
}

async function login() {
  if (!email.value || !password.value) {
    errorMessage.value = 'Por favor completa todos los campos';
    formError.value = true;
    return;
  }
  loading.value = true;
  errorMessage.value = '';
  formError.value = false;

  for (let i = 0; i <= MAX_RETRIES; i++) {
    if (i > 0) {
      errorMessage.value = `Reintentando conexión (${i}/${MAX_RETRIES})...`;
      await new Promise(r => setTimeout(r, 3000 * i));
    }
    try {
      const data = await intentarLogin(email.value, password.value);
      localStorage.setItem('user', JSON.stringify(data));
      enviarInfoDispositivo(data.id).catch(() => {});
      sessionStorage.setItem('justLoggedIn', 'true');
      window.location.href = '/';
      return;
    } catch (err) {
      if (err.response) {
        const s = err.response.status;
        errorMessage.value = s === 401 ? 'Credenciales incorrectas. Verifica tu email y contraseña.'
          : s === 403 ? (err.response.data?.detail || 'Cuenta desactivada. Contacta al administrador.')
          : s === 500 ? 'Error del servidor. Inténtalo en unos minutos.'
          : (err.response.data?.detail || 'Error al iniciar sesión.');
        formError.value = true;
        loading.value = false;
        return;
      }
    }
  }
  formError.value = true;
  loading.value = false;
  errorMessage.value = !navigator.onLine
    ? 'Sin conexión a internet.'
    : 'No se pudo conectar con el servidor. Intenta de nuevo.';
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600&display=swap');

/* ── reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ════════════════════════════════════════
   RAÍZ — flex horizontal
   ════════════════════════════════════════ */
.root {
  display: flex;
  align-items: stretch;   /* paneles estiran al alto real del contenido */
  min-height: 100vh;
  width: 100%;
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
  color-scheme: light only;
}

/* ════════════════════════════════════════
   PANEL IZQUIERDO
   ════════════════════════════════════════ */
.left-panel {
  display: none; /* oculto en móvil */
  position: relative;
  overflow: hidden;
  background:
    url('https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?auto=format&fit=crop&w=1400&q=90')
    center/cover no-repeat;
}

/* Filtro verde profundo + degradado lateral */
.left-overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(to right, rgba(2,44,18,0.15) 0%, rgba(2,44,18,0.08) 100%),
    linear-gradient(170deg,
      rgba(2,44,18,0.93)   0%,
      rgba(10,68,30,0.86) 30%,
      rgba(20,100,50,0.78) 60%,
      rgba(34,160,74,0.62) 100%
    );
  z-index: 1;
}

/* Contenido izquierdo — flex column, distribuye el espacio disponible */
.left-body {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  /* Padding escala con vh igual que el panel derecho */
  padding: clamp(28px, 5vh, 64px) clamp(24px, 4vw, 56px);
  color: #fff;
  overflow: hidden;
}

/* Badge */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.2);
  backdrop-filter: blur(8px);
  border-radius: 100px;
  padding: clamp(4px, 0.7vh, 6px) clamp(10px, 1.5vw, 16px);
  font-size: clamp(10px, 1.3vh, 12px);
  font-weight: 600;
  letter-spacing: 0.4px;
  color: rgba(255,255,255,0.9);
  width: fit-content;
  margin-bottom: clamp(14px, 3vh, 36px);
  flex-shrink: 0;
}
.badge-dot {
  width: clamp(5px, 0.8vh, 7px);
  height: clamp(5px, 0.8vh, 7px);
  background: #4ade80;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(74,222,128,0.8);
  animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* Título — escala con vh */
.left-heading {
  font-size: clamp(28px, 6.5vh, 68px);
  font-weight: 900;
  line-height: 1.0;
  letter-spacing: clamp(-1px, -0.2vw, -2px);
  color: #fff;
  margin-bottom: clamp(8px, 1.8vh, 20px);
  text-shadow: 0 4px 30px rgba(0,0,0,0.25);
  flex-shrink: 0;
}
.left-heading-accent {
  background: linear-gradient(135deg, #4ade80 0%, #bbf7d0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.left-desc {
  font-size: clamp(11px, 1.5vh, 14px);
  color: rgba(255,255,255,0.65);
  line-height: 1.6;
  margin-bottom: clamp(12px, 2.5vh, 36px);
  flex-shrink: 0;
}

/* Separador */
.left-sep {
  width: 48px;
  height: 3px;
  background: linear-gradient(90deg, #4ade80, transparent);
  border-radius: 99px;
  margin-bottom: clamp(12px, 2.5vh, 36px);
  flex-shrink: 0;
}

/* Pilares */
.pillars {
  display: flex;
  flex-direction: column;
  gap: clamp(8px, 1.4vh, 16px);
  flex-shrink: 0;
}
.pillar {
  display: flex;
  align-items: center;
  gap: clamp(10px, 1.5vw, 16px);
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.12);
  backdrop-filter: blur(6px);
  border-radius: clamp(10px, 1.5vh, 14px);
  padding: clamp(8px, 1.5vh, 14px) clamp(12px, 1.8vw, 18px);
  transition: background 0.2s;
}
.pillar:hover { background: rgba(255,255,255,0.12); }
.pillar-ico {
  display: flex; align-items: center; justify-content: center;
  width: clamp(28px, 4.5vh, 38px);
  height: clamp(28px, 4.5vh, 38px);
  flex-shrink: 0;
  background: rgba(74,222,128,0.15);
  border: 1px solid rgba(74,222,128,0.25);
  border-radius: clamp(7px, 1.2vh, 10px);
  color: #4ade80;
}
.pillar-ico svg { width: clamp(14px, 2.2vh, 18px); height: clamp(14px, 2.2vh, 18px); }
.pillar-text {
  font-size: clamp(10px, 1.4vh, 13px);
  color: rgba(255,255,255,0.88);
  font-weight: 500;
  line-height: 1.4;
}

/* Círculos decorativos */
.deco {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.07);
  z-index: 1;
  pointer-events: none;
}
.d1 { width: 380px; height: 380px; top: -120px; right: -120px; background: rgba(255,255,255,0.03); animation: spin-slow 40s linear infinite; }
.d2 { width: 240px; height: 240px; bottom: -60px; left: -60px;  background: rgba(74,222,128,0.04); animation: spin-slow 30s linear infinite reverse; }
.d3 { width: 140px; height: 140px; bottom: 20%;  right: 8%;     background: rgba(255,255,255,0.04); animation: spin-slow 25s linear infinite; }
@keyframes spin-slow { to { transform: rotate(360deg); } }

/* ════════════════════════════════════════
   PANEL DERECHO — sin scroll, todo encaja
   ════════════════════════════════════════ */
.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  overflow: hidden;
  padding: clamp(10px, 2.5vw, 36px);
  position: relative;
  background: linear-gradient(145deg, #052e16 0%, #14532d 40%, #166534 70%, #15803d 100%);
}

.right-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 50% at 20% 20%, rgba(74,222,128,0.15) 0%, transparent 60%),
    radial-gradient(ellipse 50% 60% at 85% 80%, rgba(21,128,61,0.22) 0%, transparent 55%);
  pointer-events: none;
  z-index: 0;
}

/* ── TARJETA LIQUID GLASS — blanco translúcido con blur ── */
.form-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 440px;
  /* La tarjeta nunca supera el espacio disponible */
  max-height: calc(100vh - clamp(20px, 5vh, 72px));

  /* Blanco semitransparente + desenfoque de fondo = efecto vidrio líquido */
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(24px) saturate(1.4);
  -webkit-backdrop-filter: blur(24px) saturate(1.4);

  border-radius: clamp(14px, 2vw, 28px);
  /* Padding vertical escala con vh: achica al aumentar zoom */
  padding: clamp(14px, 2.8vh, 48px) clamp(18px, 3vw, 44px);

  /* Borde luminoso sutil — remata el efecto glass */
  border: 1px solid rgba(255,255,255,0.55);
  outline: 1px solid rgba(255,255,255,0.15);
  outline-offset: -1px;

  /* Flex para distribuir hijos uniformemente */
  display: flex;
  flex-direction: column;

  box-shadow:
    0 1px 0 0 rgba(255,255,255,0.6) inset,
    0 24px 56px rgba(0,0,0,0.32),
    0 6px 20px rgba(0,0,0,0.18),
    0 0 0 1px rgba(0,0,0,0.05);

  animation: cardIn 0.5s cubic-bezier(0.22,1,0.36,1);
}
@keyframes cardIn {
  from { opacity:0; transform: translateY(20px) scale(0.97); }
  to   { opacity:1; transform: translateY(0) scale(1); }
}

/* Logo — grande, se reduce con vh, menos margen inferior */
/*
 * El PNG del logo trae espacio en blanco/transparente incorporado
 * debajo del arte. line-height:0 no puede quitar ESO porque es parte
 * de la imagen, no un margen CSS. Solución: recortar visualmente con
 * un contenedor de altura menor + overflow hidden + object-position:top,
 * mostrando solo la parte superior (donde está el logo real).
 */
.brand {
  text-align: center;
  line-height: 0;
  overflow: hidden;
  height: clamp(96px, 17vh, 182px); /* ~65% de la altura real de la imagen */
  margin-bottom: 0;
  flex-shrink: 0;
}
.brand-logo {
  height: clamp(150px, 26vh, 280px);
  width: auto;
  max-width: 100%;
  object-fit: cover;
  object-position: top;
  display: block;
  margin: 0 auto;
  filter: drop-shadow(0 3px 10px rgba(21,128,61,0.20));
}

/* Línea divisoria desvanecida verde entre logo y título */
.brand-divider {
  width: min(70%, 220px);
  height: 2px;
  margin: clamp(4px, 1vh, 12px) auto;
  flex-shrink: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(22,163,74,0.55) 25%,
    rgba(74,222,128,0.85) 50%,
    rgba(22,163,74,0.55) 75%,
    transparent 100%
  );
}

/* Encabezado */
.form-header {
  text-align: center;
  margin-bottom: clamp(6px, 1.4vh, 20px);
  flex-shrink: 0;
}

/* Título con fuente circular delgada */
.form-title {
  font-family: 'Nunito', 'Segoe UI', system-ui, sans-serif;
  font-size: clamp(13px, 2vh, 18px);
  font-weight: 500;
  letter-spacing: 0.4px;
  margin-bottom: clamp(2px, 0.5vh, 6px);
  line-height: 1.3;
  white-space: nowrap;
}

/* Cada letra: animación de pulso de luz de izquierda a derecha */
.title-char {
  display: inline-block;
  color: #14532d;
  animation: letterShine 2.4s ease-in-out infinite;
  animation-fill-mode: both;
}
@keyframes letterShine {
  0%, 55%, 100% { color: #14532d; }
  27%            { color: #4ade80; }
}

.form-sub {
  font-size: clamp(10px, 1.4vh, 13.5px);
  color: #4b7a5a;
}

/* Error */
.alert-error {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  background: #fff1f2;
  border: 1px solid #fecdd3;
  border-left: 3px solid #f43f5e;
  border-radius: 10px;
  color: #be123c;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 20px;
  line-height: 1.4;
}
.alert-ico { width: 16px; height: 16px; flex-shrink: 0; margin-top: 1px; }

.slide-down-enter-active, .slide-down-leave-active { transition: all 0.25s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-8px); }

/* Form */
.form { display: flex; flex-direction: column; gap: clamp(8px, 1.6vh, 18px); flex-shrink: 0; }

.field { display: flex; flex-direction: column; gap: clamp(3px, 0.7vh, 6px); }

.label {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  letter-spacing: 0.1px;
}

.inp-wrap { position: relative; display: flex; align-items: center; }

.inp-ico {
  position: absolute;
  left: 14px;
  color: #94a3b8;
  pointer-events: none;
  display: flex;
  align-items: center;
}
.inp-ico svg { width: 17px; height: 17px; }

.inp {
  width: 100%;
  padding: clamp(8px, 1.5vh, 13px) 42px;
  font-size: clamp(12px, 1.7vh, 14.5px);
  color: #0f172a;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
  font-family: inherit;
}
.inp::placeholder { color: #cbd5e1; }
.inp:focus {
  background: #fff;
  border-color: #16a34a;
  box-shadow: 0 0 0 3.5px rgba(22,163,74,0.12);
}
.inp:disabled { opacity: 0.5; cursor: not-allowed; }

/* Shake */
@keyframes shake {
  0%,100%{transform:translateX(0)}
  20%,60%{transform:translateX(-5px)}
  40%,80%{transform:translateX(5px)}
}
.inp-shake { animation: shake 0.5s ease; }

/* Ojo */
.eye {
  position: absolute;
  right: 12px;
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  background: none; border: none; cursor: pointer;
  color: #94a3b8; border-radius: 8px;
  transition: color 0.15s, background 0.15s;
}
.eye:hover:not(:disabled) { color: #16a34a; background: rgba(22,163,74,0.06); }
.eye:disabled { opacity: 0.4; cursor: not-allowed; }
.eye svg { width: 18px; height: 18px; }

/* Botón submit */
.btn-submit {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: clamp(9px, 1.6vh, 14px) 24px;
  margin-top: clamp(2px, 0.5vh, 4px);
  font-size: clamp(13px, 1.8vh, 15px);
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(21,128,61,0.35), inset 0 1px 0 rgba(255,255,255,0.15);
  transition: all 0.2s ease;
  font-family: inherit;
  letter-spacing: 0.1px;
}
.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(21,128,61,0.42), inset 0 1px 0 rgba(255,255,255,0.2);
}
.btn-submit:active:not(:disabled) { transform: translateY(0); }
.btn-submit:disabled { opacity: 0.55; cursor: not-allowed; transform: none; }

.spin { width: 18px; height: 18px; animation: rot 0.75s linear infinite; }
@keyframes rot { to { transform: rotate(360deg); } }

/* Links */
.form-links {
  text-align: center;
  margin-top: clamp(8px, 1.5vh, 22px);
  display: flex;
  flex-direction: column;
  gap: clamp(3px, 0.7vh, 8px);
  flex-shrink: 0;
}
.form-links p { font-size: clamp(10px, 1.4vh, 13px); color: #3f5f4c; }

.flink {
  color: #16a34a;
  font-weight: 600;
  text-decoration: none;
  font-size: clamp(10px, 1.4vh, 13px);
  position: relative;
  transition: color 0.15s;
}
.flink::after {
  content: '';
  position: absolute; bottom: -1px; left: 0;
  width: 0; height: 1.5px;
  background: #16a34a;
  transition: width 0.2s;
  border-radius: 2px;
}
.flink:hover { color: #15803d; }
.flink:hover::after { width: 100%; }
.flink-sm { font-size: 12.5px; color: #2f5540; font-weight: 600; }
.flink-sm:hover { color: #16a34a; }

.copy {
  text-align: center;
  font-size: clamp(9px, 1.1vh, 11px);
  color: #5a7a68;
  margin-top: clamp(6px, 1.2vh, 28px);
  letter-spacing: 0.2px;
  flex-shrink: 0;
}

/* ════════════════════════════════════════
   DESKTOP ≥ 1024px — split-screen
   ════════════════════════════════════════ */
@media (min-width: 1024px) {
  .root { height: 100vh; overflow: hidden; }

  .left-panel {
    display: flex;
    width: 54%;
    flex-shrink: 0;
    height: 100vh;
    overflow: hidden;
  }

  .right-panel { width: 46%; }
}

@media (min-width: 1280px) {
  .left-panel { width: 56%; }
  .right-panel { width: 44%; }
}

/* ════════════════════════════════════════
   TABLET 768–1023px
   ════════════════════════════════════════ */
@media (min-width: 768px) and (max-width: 1023px) {
  .root { height: 100vh; overflow: hidden; }
}

/* ════════════════════════════════════════
   MÓVIL < 768px — diseño dedicado
   ════════════════════════════════════════ */
@media (max-width: 767px) {
  .root { height: 100vh; overflow: hidden; }

  /* Fondo con imagen de campo + overlay verde oscuro */
  .right-panel {
    background:
      linear-gradient(160deg, rgba(2,44,18,0.92) 0%, rgba(10,68,30,0.85) 45%, rgba(21,128,61,0.80) 100%),
      url('https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?auto=format&fit=crop&w=800&q=80') center/cover no-repeat;
    padding: clamp(16px, 5vw, 28px);
    justify-content: center;
  }

  /* Tarjeta: blanca, con sombra generosa y borde sutil */
  .form-card {
    border-radius: 24px;
    padding: clamp(20px, 5vw, 32px) clamp(18px, 5vw, 28px);
    box-shadow:
      0 0 0 1px rgba(255,255,255,0.12),
      0 8px 32px rgba(0,0,0,0.45),
      0 32px 64px rgba(0,0,0,0.30);
    max-width: 380px;
  }

  /* Logo grande en móvil */
  .brand-logo { height: clamp(120px, 32vw, 180px); }
  .brand { height: clamp(78px, 21vw, 118px); margin-bottom: 0; }

  .form-title { font-size: clamp(13px, 4vw, 17px); font-weight: 500; }
  .form-sub   { font-size: clamp(11px, 3.2vw, 13px); }
  .brand-divider { margin: 3px auto 8px; }

  /* Inputs: font-size mínimo 16px evita zoom automático en iOS */
  .inp { font-size: 16px; }

  /* Labels y links */
  .label       { font-size: clamp(12px, 3.5vw, 13px); }
  .form-links p, .flink, .flink-sm { font-size: clamp(11px, 3.2vw, 13px); }
  .copy        { font-size: clamp(9px, 2.5vw, 11px); }

  /* Botón con más presencia táctil */
  .btn-submit { padding: 14px 24px; font-size: 15px; border-radius: 14px; }
}
</style>
