<template>
  <div class="login-container">
    <div class="login-card">
      <div class="header">
        <div class="logo">🌱</div>
        <h1>Panel Administrativo</h1>
        <p>Sembrando Vida - Administración</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <label for="username">Usuario</label>
          <input
            v-model="form.username"
            type="text"
            id="username"
            placeholder="Ingresa tu usuario"
            required
            autocomplete="username"
            :disabled="loading"
          />
        </div>
        
        <div class="input-group">
          <label for="password">Contraseña</label>
          <input
            v-model="form.password"
            type="password"
            id="password"
            placeholder="Ingresa tu contraseña"
            required
            autocomplete="current-password"
            :disabled="loading"
          />
        </div>
        
        <button type="submit" :disabled="loading" class="btn-primary">
          <span v-if="!loading">Iniciar Sesión</span>
          <span v-else>
            <div class="spinner"></div>
            Iniciando sesión...
          </span>
        </button>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
      
      <div class="login-footer">
        <p class="login-info">
          <span class="info-icon">ℹ️</span>
          Acceso restringido solo para administradores
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)
const error = ref('')

const form = reactive({
  username: '',
  password: ''
})

const API_URL = 'https://apipwa.sembrandodatos.com'

const handleLogin = async () => {
  if (!form.username || !form.password) {
    error.value = 'Por favor completa todos los campos'
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    // Crear FormData para OAuth2PasswordRequestForm
    const formData = new URLSearchParams()
    formData.append('grant_type', '')
    formData.append('username', form.username)
    formData.append('password', form.password)
    formData.append('scope', '')
    formData.append('client_id', '')
    formData.append('client_secret', '')
    
    const response = await axios.post(`${API_URL}/admin/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    
    if (response.data.access_token) {
      // Login exitoso
      localStorage.setItem('admin_token', response.data.access_token)
      localStorage.setItem('admin_user', form.username)
      localStorage.setItem('login_time', new Date().toISOString())
      
      // Redirigir al dashboard
      router.push('/dashboard')
    }
  } catch (err) {
    console.error('Error de login:', err)
    
    if (err.response) {
      error.value = err.response.data.detail || 'Credenciales incorrectas. Verifica tu usuario y contraseña.'
    } else if (err.request) {
      error.value = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.'
    } else {
      error.value = 'Error al iniciar sesión: ' + err.message
    }
  } finally {
    loading.value = false
  }
}

// Auto-ocultar error después de 5 segundos
const clearError = () => {
  setTimeout(() => {
    error.value = ''
  }, 5000)
}

// Observar cambios en error para auto-ocultar
import { watch } from 'vue'
watch(error, (newValue) => {
  if (newValue) {
    clearError()
  }
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
  backdrop-filter: blur(10px);
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  font-size: 60px;
  margin-bottom: 20px;
}

.header h1 {
  color: #4CAF50;
  font-size: 28px;
  margin-bottom: 10px;
  font-weight: 700;
}

.header p {
  color: #666;
  font-size: 16px;
}

.login-form {
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 25px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 15px;
  border: 2px solid #e1e1e1;
  border-radius: 12px;
  font-size: 16px;
  transition: border-color 0.3s ease;
  background: #fafafa;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
  background: white;
}

input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  width: 100%;
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 15px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #45a049, #4CAF50);
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(76, 175, 80, 0.3);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  color: #e74c3c;
  background: #ffebee;
  border: 1px solid #ffcdd2;
  border-radius: 8px;
  padding: 12px;
  margin-top: 15px;
  font-size: 14px;
  text-align: center;
}

.login-footer {
  margin-top: 20px;
  text-align: center;
}

.login-info {
  color: #666;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.info-icon {
  font-size: 16px;
}
</style>
