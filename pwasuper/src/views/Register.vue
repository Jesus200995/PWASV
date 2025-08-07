<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-6">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Crear cuenta
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600" style="display: none;">
          Servidor: <span class="font-mono text-xs" :class="currentApiUrl.includes('localhost') ? 'text-blue-600' : 'text-green-600'">
            {{ currentApiUrl }}
          </span>
        </p>
      </div>
      
      <!-- Modal de éxito -->
      <transition name="modal">
        <div v-if="showSuccessModal" class="fixed inset-0 z-50 flex items-center justify-center p-4" style="background-color: rgba(0, 0, 0, 0.5);">
          <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 transform transition-all">
            <div class="p-6 text-center">
              <!-- Icono de éxito animado -->
              <div class="mx-auto mb-4 w-16 h-16 bg-green-100 rounded-full flex items-center justify-center animate-bounce">
                <svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </div>
              
              <!-- Título -->
              <h3 class="text-lg font-semibold text-gray-900 mb-2">¡Registro Exitoso!</h3>
              
              <!-- Mensaje -->
              <p class="text-gray-600 mb-4">Tu cuenta ha sido creada correctamente. Serás redirigido al login en unos segundos.</p>
              
              <!-- Barra de progreso -->
              <div class="w-full bg-gray-200 rounded-full h-2 mb-4">
                <div class="bg-green-500 h-2 rounded-full animate-progress" style="animation-duration: 3s;"></div>
              </div>
              
              <!-- Botón opcional -->
              <button @click="goToLogin" class="bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                Ir al Login
              </button>
            </div>
          </div>
        </div>
      </transition>

      <!-- Mensajes de error (solo errores ahora) -->
      <transition name="fade">
        <div v-if="message.text && message.type === 'error'" class="border-l-4 p-4 rounded bg-red-100 border-red-500 text-red-700" role="alert">
          <p>{{ message.text }}</p>
        </div>
      </transition>

      <form class="mt-8 space-y-4" @submit.prevent="register" @keydown.enter="handleEnterKey">
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

        <!-- AVISO DE PRIVACIDAD -->
        <div class="mt-6 mb-4">
          <div class="border border-gray-300 rounded-md bg-gray-50">
            <div class="p-4">
              <h3 class="font-bold text-orange-600 mb-2 text-lg bg-gradient-to-r from-yellow-200 to-yellow-100 px-3 py-2 rounded-lg shadow-sm border border-yellow-300">
                Aviso de Privacidad
              </h3>
              <div class="max-h-64 overflow-y-auto text-sm text-gray-700 space-y-2 pr-2">
                <div class="font-semibold">AVISO DE PRIVACIDAD PARA EL REGISTRO Y USO DE INFORMACIÓN DE LOS TÉCNICOS DEL PROGRAMA SEMBRANDO VIDA</div>
                
                <p>En cumplimiento con lo dispuesto por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP), se informa a los Técnicos del Programa Sembrando Vida que los datos personales recabados serán tratados conforme a los siguientes términos:</p>
                
                <div class="font-semibold">1. Identidad y domicilio del responsable</div>
                <p>El responsable del tratamiento de los datos personales es la Secretaría de Bienestar, Subsecretaria de Inclusión Productiva y Desarrollo Rural con domicilio en: Av. P.º de la Reforma 116, Juárez, Cuauhtémoc, 06600 Ciudad de México, CDMX.</p>
                <p>Los datos personales mencionados serán recabados y registrados a través de una Aplicación Móvil oficial</p>
                
                <div class="font-semibold">2. Datos personales que se recaban</div>
                <ul class="list-disc pl-4 space-y-1">
                  <li>Nombre completo</li>
                  <li>CURP</li>
                  <li>Correo electrónico</li>
                  <li>Cargo y supervisor asignado</li>
                  <li>Datos de localización geográfica precisa, capturados a través de coordenadas (latitud y longitud), correspondientes a los sitios donde el titular realiza actividades dentro del Programa.</li>
                  <li>Actividades realizadas en campo dentro del Programa</li>
                  <li>Fotografías de las actividades realizadas</li>
                </ul>
                
                <div class="font-semibold">3. Finalidades del tratamiento</div>
                <p>Los datos personales mencionados serán recabados y registrados a través de la Aplicación Móvil oficial del Programa Sembrando Vida y serán utilizados exclusivamente para:</p>
                <ul class="list-disc pl-4 space-y-1">
                  <li>Registrar las actividades de los técnicos en campo.</li>
                  <li>Documentar el avance, seguimiento y diagnóstico de la implementación del Programa Sembrando Vida.</li>
                  <li>Elaborar reportes y análisis internos sobre el desempeño operativo del programa.</li>
                </ul>
                <p>Los datos no serán utilizados con fines publicitarios, comerciales ni compartidos con terceros sin el consentimiento previo del titular, salvo las excepciones previstas en la ley.</p>
                
                <div class="font-semibold">4. Transferencias de datos personales</div>
                <p>Los datos recabados no serán transferidos a terceros sin el consentimiento del titular, salvo en los casos expresamente autorizados por la ley.</p>
                
                <div class="font-semibold">5. Medios para ejercer derechos ARCO</div>
                <p>Usted tiene derecho a Acceder, Rectificar, Cancelar u Oponerse (ARCO) al tratamiento de sus datos personales. Para ejercer estos derechos, puede presentar una solicitud al correo electrónico: [correo de contacto], o acudir al domicilio mencionado en el punto 1.</p>
                
                <div class="font-semibold">6. Medidas de seguridad</div>
                <p>Se informa que los datos personales serán tratados bajo estrictas medidas de seguridad administrativas, técnicas y físicas que garanticen su confidencialidad e integridad.</p>
                
                <div class="font-semibold">7. Cambios al aviso de privacidad</div>
                <p>Este Aviso de Privacidad puede ser modificado. Las actualizaciones estarán disponibles en https://app.sembrandodatos.com.</p>
                
                <div class="font-semibold">Fecha de última actualización: 05 de agosto del 2025.</div>
                
                <p class="font-semibold text-blue-800">Al proporcionar mis datos personales, acepto el tratamiento conforme al Aviso de Privacidad.</p>
              </div>
            </div>
          </div>
          
          <!-- CHECKBOX OBLIGATORIO -->
          <div class="mt-4">
            <div class="flex items-start">
              <div class="flex items-center h-5">
                <input 
                  v-model="termsAccepted" 
                  @change="clearTermsError"
                  id="terms" 
                  name="terms" 
                  type="checkbox" 
                  class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                  required
                />
              </div>
              <div class="ml-3 text-sm">
                <label for="terms" class="font-medium text-gray-700">
                  He leído y acepto el Aviso de Privacidad y los Términos y Condiciones. <span class="text-red-500">*</span>
                </label>
              </div>
            </div>
            <p v-if="termsError" class="mt-1 text-sm text-red-600">{{ termsError }}</p>
          </div>
        </div>

        <div>
          <button type="submit" :disabled="loading || !termsAccepted" 
            class="mt-4 w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white"
            :class="loading || !termsAccepted ? 'bg-gray-400 cursor-not-allowed' : 'bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary'">
            <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Registrando...' : termsAccepted ? 'Registrarme' : 'Debes aceptar los términos' }}
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
const termsAccepted = ref(false);
const termsError = ref('');
const showSuccessModal = ref(false);

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
  // Validar datos incluyendo términos
  if (!validateForm()) return;
  
  // Verificar conexión a internet
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    message.text = getOfflineMessage();
    message.type = 'error';
    return;
  }
  
  // Prevenir múltiples envíos
  if (loading.value) return;
  
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
    
    // Mostrar modal de éxito en lugar del mensaje
    showSuccessModal.value = true;
    
    // Redirigir después de 3 segundos
    setTimeout(() => {
      router.push('/login');
    }, 3000);
    
    
  } catch (error) {
    console.error('Error de registro:', error);
    
    if (error.response) {
      const status = error.response.status;
      if (status === 400) {
        const detail = error.response.data.detail || '';
        if (detail.includes('correo')) {
          message.text = 'El correo electrónico ya está registrado. Por favor, utiliza otro correo.';
        } else if (detail.includes('CURP')) {
          message.text = 'La CURP ya está registrada. Si ya tienes una cuenta, inicia sesión.';
        } else {
          message.text = detail || 'Los datos proporcionados son inválidos. Verifica la información.';
        }
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
  termsError.value = '';
  message.text = '';
  
  // Verificar aceptación de términos
  if (!termsAccepted.value) {
    termsError.value = 'Debes aceptar el Aviso de Privacidad para continuar';
    message.text = 'Debes aceptar el Aviso de Privacidad para continuar';
    message.type = 'error';
    return false;
  }
  
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
  if (termsError.value) {
    termsError.value = '';
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

function clearTermsError() {
  if (termsError.value) {
    termsError.value = '';
  }
  if (message.text && message.text.includes('Aviso de Privacidad')) {
    message.text = '';
  }
}

function handleEnterKey(event) {
  // Prevenir envío del formulario si no se han aceptado los términos
  if (!termsAccepted.value) {
    event.preventDefault();
    termsError.value = 'Debes aceptar el Aviso de Privacidad para continuar';
    message.text = 'Debes aceptar el Aviso de Privacidad para continuar';
    message.type = 'error';
  }
}

function goToLogin() {
  showSuccessModal.value = false;
  router.push('/login');
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

/* Estilos para el scroll del aviso de privacidad */
.max-h-64.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.max-h-64.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.max-h-64.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.max-h-64.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Mejoras visuales para el checkbox */
input[type="checkbox"]:checked {
  background-color: #2563eb;
  border-color: #2563eb;
}

/* Transiciones para botón deshabilitado */
button {
  transition: all 0.2s ease-in-out;
}

/* Animaciones para el modal */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-active .bg-white, .modal-leave-active .bg-white {
  transition: all 0.3s ease;
}
.modal-enter-from .bg-white, .modal-leave-to .bg-white {
  transform: scale(0.8) translateY(-50px);
  opacity: 0;
}

/* Animación de la barra de progreso */
@keyframes progress {
  0% { width: 0%; }
  100% { width: 100%; }
}

.animate-progress {
  animation: progress 3s linear forwards;
}

/* Animación del bounce mejorada */
.animate-bounce {
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0,0,0);
  }
  40%, 43% {
    transform: translate3d(0, -15px, 0);
  }
  70% {
    transform: translate3d(0, -7px, 0);
  }
  90% {
    transform: translate3d(0, -2px, 0);
  }
}
</style>
