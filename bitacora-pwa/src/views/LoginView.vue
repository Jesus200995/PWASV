<template>
  <div class="login-wrap">
    <form class="login-card" @submit.prevent="doLogin">
      <div class="logo-area">
        <div class="logo-icon">📍</div>
        <h1>Sistema de Ubicación</h1>
        <p>Acceso restringido</p>
      </div>

      <div class="field">
        <label>Usuario</label>
        <input v-model="handle" type="text" autocomplete="username" required />
      </div>

      <div class="field">
        <label>Contraseña</label>
        <input v-model="secret" type="password" autocomplete="current-password" required />
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <button :disabled="loading" type="submit">
        <span v-if="loading">Verificando...</span>
        <span v-else>Entrar</span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { obsLogin } from '../services/api.js'

const router = useRouter()
const handle = ref('')
const secret = ref('')
const error = ref('')
const loading = ref(false)

async function doLogin() {
  error.value = ''
  loading.value = true
  try {
    await obsLogin(handle.value, secret.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.message || 'Error de acceso'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}
.login-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 2.5rem 2rem;
  width: 100%;
  max-width: 380px;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.logo-area { text-align: center; }
.logo-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
h1 { font-size: 1.3rem; color: #f1f5f9; font-weight: 700; }
p { color: #64748b; font-size: 0.85rem; margin-top: 0.25rem; }
.field { display: flex; flex-direction: column; gap: 0.4rem; }
label { font-size: 0.8rem; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }
input {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 0.65rem 0.9rem;
  color: #e2e8f0;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}
input:focus { border-color: #3b82f6; }
button {
  background: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.75rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 0.4rem;
}
button:hover:not(:disabled) { background: #2563eb; }
button:disabled { opacity: 0.6; cursor: not-allowed; }
.error { color: #f87171; font-size: 0.85rem; text-align: center; }
</style>
