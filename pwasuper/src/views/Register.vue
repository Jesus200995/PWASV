<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-6">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Crear cuenta
        </h2>
      </div>
      
      <transition name="fade">
        <div v-if="message.text" :class="['border-l-4 p-4 rounded', message.type === 'error' ? 'bg-red-100 border-red-500 text-red-700' : 'bg-green-100 border-green-500 text-green-700']" role="alert">
          <p>{{ message.text }}</p>
        </div>
      </transition>

      <form class="mt-8 space-y-4" @submit.prevent="register">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Correo electrónico</label>
          <input v-model="form.email" id="email" name="email" type="email" autocomplete="email" required 
            class="mt-1 form-input" />
        </div>
        
        <div>
          <label for="nombre" class="block text-sm font-medium text-gray-700">Nombre completo</label>
          <input v-model="form.nombre" id="nombre" name="nombre" type="text" required 
            class="mt-1 form-input" />
        </div>
        
        <div>
          <label for="cargo" class="block text-sm font-medium text-gray-700">Cargo</label>
          <input v-model="form.cargo" id="cargo" name="cargo" type="text" required 
            class="mt-1 form-input" />
        </div>
        
        <div>
          <label for="supervisor" class="block text-sm font-medium text-gray-700">Supervisor</label>
          <input v-model="form.supervisor" id="supervisor" name="supervisor" type="text" 
            class="mt-1 form-input" />
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <input v-model="form.password" id="password" name="password" type="password" required 
            class="mt-1 form-input" />
        </div>
        
        <div>
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirmar contraseña</label>
          <input v-model="form.confirmPassword" id="confirmPassword" name="confirmPassword" type="password" required 
            class="mt-1 form-input" />
        </div>

        <div>
          <button type="submit" :disabled="loading" 
            class="mt-4 w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
            <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Registrando...' : 'Registrarme' }}
          </button>
        </div>
      </form>

      <div class="text-center">
        <p class="text-sm text-gray-600">
          ¿Ya tienes cuenta?
          <router-link to="/login" class="font-medium text-primary hover:text-primary/80">
            Iniciar sesión
          </router-link>
        </p>      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { API_URL, checkInternetConnection, getOfflineMessage } from '../utils/network.js';

const router = useRouter();
const loading = ref(false);
const message = reactive({ text: '', type: '' });
const isOnline = ref(true);

const form = reactive({
  email: '',
  nombre: '',
  cargo: '',
  supervisor: '',
  password: '',
  confirmPassword: ''
});

onMounted(async () => {
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    message.text = getOfflineMessage();
    message.type = 'error';
  }
});

async function register() {
  // Validar datos
  if (!validateForm()) return;
  
  // Verificar conexión a internet
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    message.text = getOfflineMessage();
    message.type = 'error';
    return;
  }
  
  loading.value = true;
  message.text = '';
  
  try {
    // Conectar con la API real para crear el usuario
    const response = await axios.post(`${API_URL}/usuarios`, {
      correo: form.email,
      nombre_completo: form.nombre,
      cargo: form.cargo,
      supervisor: form.supervisor || null, // Enviar null si está vacío
      contrasena: form.password
    });    // Mostrar mensaje de éxito
    message.text = '¡Cuenta creada exitosamente! Redirigiendo...';
    message.type = 'success';
    
    // Redirigir después de un breve retraso
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (error) {
    console.error('Error de registro:', error);
    
    if (error.response) {
      // Error de respuesta del servidor
      message.text = error.response.data.detail || 'Error al crear la cuenta.';
    } else if (error.request) {
      // Error de conexión
      message.text = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
    } else {
      // Error general
      message.text = 'Error al crear la cuenta: ' + error.message;
    }
    
    message.type = 'error';
  } finally {
    loading.value = false;
  }
}

function validateForm() {
  // Verificar que las contraseñas coincidan
  if (form.password !== form.confirmPassword) {
    message.text = 'Las contraseñas no coinciden';
    message.type = 'error';
    return false;
  }
  
  // Verificar que la contraseña tenga al menos 6 caracteres
  if (form.password.length < 6) {
    message.text = 'La contraseña debe tener al menos 6 caracteres';
    message.type = 'error';
    return false;
  }
  
  // Verificar formato de correo electrónico
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(form.email)) {
    message.text = 'Por favor ingresa un correo electrónico válido';
    message.type = 'error';
    return false;
  }
  
  return true;
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
