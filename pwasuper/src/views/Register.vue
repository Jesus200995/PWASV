<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-6">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Crear cuenta
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Servidor: <span class="font-mono text-xs" :class="currentApiUrl.includes('localhost') ? 'text-blue-600' : 'text-green-600'">
            {{ currentApiUrl }}
          </span>
        </p>
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
          <label for="curp" class="block text-sm font-medium text-gray-700">CURP *</label>
          <input v-model="form.curp" @input="formatCurp" id="curp" name="curp" type="text" required
            maxlength="18" placeholder="18 caracteres en mayúsculas"
            class="mt-1 form-input uppercase tracking-wide" />
          <p v-if="curpError" class="mt-1 text-sm text-red-600">{{ curpError }}</p>
          <p class="mt-1 text-xs text-gray-500">La CURP debe contener exactamente 18 caracteres en mayúsculas</p>
          <p v-if="curpWarning" class="mt-1 text-xs text-yellow-600">{{ curpWarning }}</p>
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
import { apiService } from '../services/apiService.js';
import { checkInternetConnection, getOfflineMessage } from '../utils/network.js';

const router = useRouter();
const loading = ref(false);
const message = reactive({ text: '', type: '' });
const isOnline = ref(true);
const curpError = ref('');
const curpWarning = ref('');
const currentApiUrl = ref('');

const form = reactive({
  email: '',
  nombre: '',
  cargo: '',
  curp: '',
  supervisor: '',
  password: '',
  confirmPassword: ''
});

onMounted(async () => {
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    message.text = getOfflineMessage();
    message.type = 'error';
  } else {
    // Obtener la URL actual del servicio API
    try {
      await apiService.refreshApiUrl();
      currentApiUrl.value = apiService.getCurrentApiUrl();
      console.log(`🌐 Usando servidor: ${currentApiUrl.value}`);
    } catch (error) {
      console.warn('Error inicializando servicio API:', error);
    }
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
    // Crear payload con CURP obligatoria
    const payload = {
      correo: form.email,
      nombre_completo: form.nombre,
      cargo: form.cargo,
      supervisor: form.supervisor || null,
      contrasena: form.password,
      curp: form.curp.toUpperCase().trim()
    };
    
    console.log('📤 Enviando payload:', payload);
    
    // Usar el servicio API que maneja automáticamente la mejor URL
    const response = await apiService.createUser(payload);
    
    console.log('✅ Respuesta del servidor:', response);
    
    // Actualizar la URL mostrada
    currentApiUrl.value = apiService.getCurrentApiUrl();
    
    message.text = `¡Cuenta creada exitosamente con CURP! (Servidor: ${currentApiUrl.value.replace('https://', '').replace('http://', '')}) Redirigiendo...`;
    message.type = 'success';
    
    setTimeout(() => {
      router.push('/login');
    }, 2000);
    
    
  } catch (error) {
    console.error('Error de registro:', error);
    
    if (error.response) {
      const status = error.response.status;
      if (status === 400) {
        message.text = error.response.data.detail || 'El correo ya está registrado o los datos son inválidos.';
      } else if (status === 500) {
        message.text = 'Error del servidor. Inténtalo de nuevo en unos minutos.';
      } else {
        message.text = error.response.data.detail || 'Error al crear la cuenta.';
      }
    } else if (error.request) {
      message.text = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
    } else if (error.code === 'ECONNABORTED') {
      message.text = 'La conexión tardó demasiado. Verifica tu conexión a internet.';
    } else {
      message.text = 'Error al crear la cuenta: ' + error.message;
    }
    
    message.type = 'error';
  } finally {
    loading.value = false;
  }
}

function validateForm() {
  // Limpiar errores previos
  curpError.value = '';
  curpWarning.value = '';
  message.text = '';
  
  // Verificar CURP obligatoria
  if (!form.curp || !form.curp.trim()) {
    curpError.value = 'La CURP es obligatoria';
    message.text = 'Por favor completa todos los campos obligatorios';
    message.type = 'error';
    return false;
  }
  
  const curpClean = form.curp.toUpperCase().trim();
  if (curpClean.length !== 18) {
    curpError.value = 'La CURP debe contener exactamente 18 caracteres';
    message.text = 'La CURP debe contener exactamente 18 caracteres en mayúsculas';
    message.type = 'error';
    return false;
  }
  
  // Validación básica de formato CURP (solo letras y números)
  const curpRegex = /^[A-Z0-9]{18}$/;
  if (!curpRegex.test(curpClean)) {
    curpError.value = 'La CURP solo debe contener letras mayúsculas y números';
    message.text = 'La CURP debe contener solo letras mayúsculas y números';
    message.type = 'error';
    return false;
  }
  
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

function formatCurp() {
  // Convertir a mayúsculas automáticamente
  form.curp = form.curp.toUpperCase();
  
  // Limpiar errores cuando el usuario empiece a escribir
  if (curpError.value) {
    curpError.value = '';
  }
  if (curpWarning.value) {
    curpWarning.value = '';
  }
  
  // Validación en tiempo real
  if (form.curp.length > 0 && form.curp.length < 18) {
    curpError.value = `Faltan ${18 - form.curp.length} caracteres`;
  } else if (form.curp.length === 18) {
    const curpRegex = /^[A-Z0-9]{18}$/;
    if (!curpRegex.test(form.curp)) {
      curpError.value = 'La CURP solo debe contener letras mayúsculas y números';
    } else {
      curpError.value = '';
      curpWarning.value = 'CURP válida ✓';
    }
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

.uppercase {
  text-transform: uppercase;
}

.tracking-wide {
  letter-spacing: 0.025em;
}
</style>
