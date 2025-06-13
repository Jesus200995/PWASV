<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-white py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <h1 class="text-4xl font-bold text-primary mb-2">Sembrando Vida</h1>
        <h2 class="text-2xl font-semibold text-gray-700">
          Iniciar sesión
        </h2>
        <p class="mt-2 text-gray-500">Ingresa tus credenciales para acceder</p>
      </div>
      
      <transition name="bounce">
        <div v-if="errorMessage" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg shadow-sm" role="alert">
          <p class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            {{ errorMessage }}
          </p>
        </div>
      </transition>

      <div class="bg-white py-8 px-6 shadow-xl rounded-xl transform transition-all hover:shadow-2xl">
        <form class="space-y-6" @submit.prevent="login">
          <div class="space-y-4">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Correo electrónico</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </div>
                <input v-model="email" id="email" name="email" type="email" autocomplete="email" required 
                  class="pl-10 appearance-none block w-full px-3 py-3 border border-gray-300 rounded-lg placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all duration-200 sm:text-sm" 
                  placeholder="nombre@ejemplo.com" 
                  :class="{ 'animate-shake': formError }" />
              </div>
            </div>
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input v-model="password" id="password" name="password" type="password" autocomplete="current-password" required 
                  class="pl-10 appearance-none block w-full px-3 py-3 border border-gray-300 rounded-lg placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all duration-200 sm:text-sm" 
                  placeholder="••••••••" 
                  :class="{ 'animate-shake': formError }" />
              </div>
            </div>
          </div>

          <div>
            <button type="submit" :disabled="loading" 
              class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-200 transform hover:scale-105 shadow-md hover:shadow-lg">
              <span v-if="loading" class="absolute left-0 inset-y-0 flex items-center pl-3">
                <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </span>
              {{ loading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
            </button>
          </div>
        </form>

        <div class="text-center mt-6">
          <p class="text-sm text-gray-600">
            ¿No tienes cuenta?
            <router-link to="/register" class="font-medium text-primary hover:text-primary-dark transition-colors duration-200">
              Crear cuenta
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { API_URL, checkInternetConnection, getOfflineMessage } from '../utils/network.js';

const router = useRouter();
const email = ref('');
const password = ref('');
const loading = ref(false);
const errorMessage = ref('');
const formError = ref(false);
const isOnline = ref(true);

// Verificar conexión a internet cuando carga el componente
onMounted(async () => {
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    errorMessage.value = getOfflineMessage();
  }
});

async function login() {
  loading.value = true;
  errorMessage.value = '';
  formError.value = false;
  
  // Verificar si hay campos vacíos
  if (!email.value || !password.value) {
    errorMessage.value = 'Por favor, completa todos los campos';
    formError.value = true;
    loading.value = false;
    return;
  }
  
  // Verificar conexión a internet
  const online = await checkInternetConnection();
  if (!online) {
    errorMessage.value = getOfflineMessage();
    formError.value = true;
    loading.value = false;
    return;
  }
  
  try {
    // Conectar con la API real
    const response = await axios.post(`${API_URL}/login`, {
      correo: email.value,
      contrasena: password.value
    });
    
    // Obtener datos del usuario desde la respuesta
    const userData = response.data;
    
    // Guardar datos del usuario en localStorage
    localStorage.setItem('user', JSON.stringify(userData));
    
    // Establecer bandera para mostrar mensaje de bienvenida
    sessionStorage.setItem('justLoggedIn', 'true');
    
    // Redirigir a la página principal
    router.push('/');
  } catch (error) {
    console.error('Error de inicio de sesión:', error);
    
    if (error.response) {
      // El servidor respondió con un estado de error
      errorMessage.value = error.response.data.detail || 'Error al iniciar sesión. Verifica tus credenciales.';
    } else if (error.request) {
      // La solicitud fue hecha pero no se recibió respuesta
      errorMessage.value = 'No se pudo conectar con el servidor. Verifica tu conexión.';
    } else {      // Algo ocurrió al configurar la solicitud
      errorMessage.value = 'Error al iniciar sesión: ' + error.message;
    }
    
    formError.value = true;
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.bounce-enter-active {
  animation: bounce-in 0.5s;
}
.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.5;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

.animate-shake {
  animation: shake 0.6s cubic-bezier(.36,.07,.19,.97) both;
}
</style>
