<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">🌱</div>
        <h1>Panel Administrativo</h1>
        <p>Sembrando Vida - Administración</p>
      </div>
      
      <form @submit.prevent="login" class="login-form">
        <div class="input-group">
          <label for="username">Usuario</label>
          <input 
            v-model="credentials.username"
            type="text" 
            id="username" 
            placeholder="Ingresa tu usuario" 
            required
            :disabled="loading"
          >
        </div>
        
        <div class="input-group">
          <label for="password">Contraseña</label>
          <input 
            v-model="credentials.password"
            type="password" 
            id="password" 
            placeholder="Ingresa tu contraseña" 
            required
            :disabled="loading"
          >
        </div>
        
        <button type="submit" class="login-btn" :disabled="loading">
          <span v-if="!loading">Iniciar Sesión</span>
          <span v-else class="loading-text">
            <div class="spinner"></div>
            Iniciando sesión...
          </span>
        </button>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const credentials = reactive({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const API_URL = 'https://apipwa.sembrandodatos.com'

const login = async () => {
  if (!credentials.username || !credentials.password) {
    error.value = 'Por favor completa todos los campos'
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    const formData = new URLSearchParams()
    formData.append('grant_type', '')
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)
    formData.append('scope', '')
    formData.append('client_id', '')
    formData.append('client_secret', '')
    
    const response = await axios.post(`${API_URL}/admin/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    
    if (response.data.access_token) {
      // Guardar token y usuario
      localStorage.setItem('admin_token', response.data.access_token)
      localStorage.setItem('admin_user', credentials.username)
      
      // Redirigir al dashboard
      router.push('/dashboard')
    } else {
      error.value = 'Credenciales incorrectas'
    }
  } catch (err) {
    console.error('Error de login:', err)
    if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  font-size: 48px;
  margin-bottom: 16px;
}

.login-header h1 {
  color: #333;
  margin-bottom: 8px;
  font-size: 24px;
}

.login-header p {
  color: #666;
  font-size: 14px;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  color: #555;
  margin-bottom: 8px;
  font-weight: 500;
}

.input-group input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.input-group input:focus {
  outline: none;
  border-color: #4CAF50;
}

.input-group input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.login-btn {
  width: 100%;
  background: #4CAF50;
  color: white;
  border: none;
  padding: 14px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-btn:hover:not(:disabled) {
  background: #45a049;
}

.login-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

.spinner {
  width: 16px;
  height: 16px;
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
  background: #fee;
  color: #c33;
  padding: 12px;
  border-radius: 8px;
  margin-top: 16px;
  text-align: center;
  border: 1px solid #fcc;
}
</style>
