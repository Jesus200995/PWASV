<template>
  <div class="register-page">
    <!-- Modal de Éxito -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showSuccessModal" class="modal-overlay" @click.self="goToLogin">
          <div class="modal-card">
            <div class="modal-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="#10b981" stroke-width="2"/>
                <path d="M8 12l2.5 2.5L16 9" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h2 class="modal-title">¡Registro Exitoso!</h2>
            <p class="modal-text">Tu cuenta ha sido creada correctamente</p>
            <div class="modal-progress">
              <div class="modal-progress-bar"></div>
            </div>
            <p class="modal-redirect">Redirigiendo al login...</p>
            <button @click="goToLogin" class="modal-button">Ir al Login</button>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Contenido Principal con Scroll -->
    <div class="register-scroll">
      <!-- Header -->
      <header class="register-header">
        <router-link to="/login" class="back-link">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
          </svg>
          <span>Volver</span>
        </router-link>
      </header>

      <!-- Título -->
      <div class="register-title">
        <div class="title-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5">
            <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h1>Crear Cuenta</h1>
        <p>Completa tus datos para registrarte</p>
      </div>

      <!-- Error Banner -->
      <Transition name="slide">
        <div v-if="message.text && message.type === 'error'" class="error-banner">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          <span>{{ message.text }}</span>
        </div>
      </Transition>

      <!-- Formulario -->
      <form @submit.prevent="register" @keydown.enter="handleEnterKey" class="register-form">
        
        <!-- SECCIÓN: DATOS PERSONALES -->
        <section class="form-section">
          <h3 class="section-title">
            <span class="section-emoji">👤</span>
            Datos Personales
          </h3>

          <!-- Email -->
          <div class="field">
            <label for="email">Correo Electrónico</label>
            <div class="input-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/>
              </svg>
              <input v-model="form.email" id="email" type="email" autocomplete="email" required placeholder="ejemplo@correo.com"/>
            </div>
          </div>

          <!-- Nombre -->
          <div class="field">
            <label for="nombre">Nombre(s)</label>
            <div class="input-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              <input v-model="form.nombre" @input="formatNombre" id="nombre" type="text" required placeholder="Ej. JOSÉ MARÍA" class="uppercase"/>
            </div>
            <span class="hint">Ingresa tu nombre o nombres de pila</span>
          </div>

          <!-- Apellido Paterno -->
          <div class="field">
            <label for="primerApellido">Apellido Paterno</label>
            <div class="input-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              <input v-model="form.primerApellido" @input="formatPrimerApellido" id="primerApellido" type="text" required placeholder="Ej. GARCÍA" class="uppercase"/>
            </div>
          </div>

          <!-- Apellido Materno -->
          <div class="field">
            <label for="segundoApellido">Apellido Materno</label>
            <div class="input-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              <input v-model="form.segundoApellido" @input="formatSegundoApellido" id="segundoApellido" type="text" required placeholder="Ej. LÓPEZ" class="uppercase"/>
            </div>
          </div>

          <!-- CURP -->
          <div class="field">
            <label for="curp">CURP</label>
            <div class="input-box" :class="{ error: curpError, success: curpWarning }">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <input v-model="form.curp" @input="formatCurp" id="curp" type="text" required maxlength="18" placeholder="18 caracteres" class="uppercase tracking"/>
              <span v-if="form.curp" class="char-count">{{ form.curp.length }}/18</span>
            </div>
            <span v-if="curpError" class="hint error">{{ curpError }}</span>
            <span v-else-if="curpWarning" class="hint success">{{ curpWarning }}</span>
            <span v-else class="hint">La CURP debe contener exactamente 18 caracteres</span>
          </div>
        </section>

        <!-- SECCIÓN: INFORMACIÓN LABORAL -->
        <section class="form-section">
          <h3 class="section-title">
            <span class="section-emoji">💼</span>
            Información Laboral
          </h3>

          <!-- Territorio -->
          <div class="field">
            <label for="territorio">Territorio</label>
            <div class="select-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <select v-model="form.territorio" id="territorio" required>
                <option value="" disabled>Selecciona tu territorio</option>
                <option v-for="territorio in territoriosSembrandoVida" :key="territorio" :value="territorio">{{ territorio }}</option>
              </select>
              <svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
              </svg>
            </div>
            <span v-if="territorioError" class="hint error">{{ territorioError }}</span>
            <span v-else class="hint">Selecciona el territorio de tu área de trabajo</span>
          </div>

          <!-- Cargo -->
          <div class="field">
            <label for="cargo">Puesto de Trabajo</label>
            <div class="select-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              <select v-model="form.cargo" id="cargo" required>
                <option value="" disabled>Selecciona tu cargo</option>
                <option v-for="cargo in cargosDisponibles" :key="cargo" :value="cargo">{{ cargo }}</option>
              </select>
              <svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
              </svg>
            </div>
          </div>

          <!-- Campo OTRO cargo -->
          <Transition name="expand">
            <div v-if="form.cargo === 'OTRO'" class="field">
              <label for="cargoOtro">Especifica tu cargo</label>
              <div class="input-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
                <input v-model="form.cargoOtro" @input="formatCargoOtro" id="cargoOtro" type="text" required placeholder="Ej. COORDINADOR DE PROYECTO" class="uppercase"/>
              </div>
            </div>
          </Transition>

          <!-- Supervisor -->
          <div class="field">
            <label for="supervisor">Supervisor Inmediato</label>
            <div class="input-box" :class="{ disabled: esTecnico }">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
              <input v-model="form.supervisor" @input="formatSupervisor" id="supervisor" type="text" required :readonly="esTecnico" :placeholder="esTecnico && buscandoSupervisor ? 'Buscando supervisor...' : 'Ej. MARÍA GARCÍA LÓPEZ'" class="uppercase"/>
              <div v-if="buscandoSupervisor" class="spinner"></div>
            </div>
            <span v-if="esTecnico" class="hint success">✓ Supervisor asignado automáticamente</span>
            <span v-else class="hint">Nombre completo de tu jefe directo</span>
          </div>
        </section>

        <!-- SECCIÓN: CONTACTO -->
        <section class="form-section">
          <h3 class="section-title">
            <span class="section-emoji">📱</span>
            Contacto
          </h3>

          <!-- Teléfono -->
          <div class="field">
            <label for="telefono">Número de Teléfono</label>
            <div class="phone-container">
              <!-- Selector País -->
              <div class="country-selector">
                <button type="button" @click="showCountrySelector = !showCountrySelector" class="country-button">
                  <span class="flag">{{ paises.find(p => p.codigo === form.codigoPais)?.bandera || '🌎' }}</span>
                  <span class="code">{{ form.codigoPais }}</span>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
                  </svg>
                </button>
                
                <Transition name="dropdown">
                  <div v-if="showCountrySelector" class="country-dropdown">
                    <div class="country-search">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                      </svg>
                      <input type="text" v-model="countrySearch" placeholder="Buscar país..." @click.stop/>
                    </div>
                    <ul class="country-list">
                      <li v-for="pais in filteredCountries" :key="pais.codigo" @click="selectCountry(pais)" class="country-item">
                        <span class="flag">{{ pais.bandera }}</span>
                        <span class="name">{{ pais.nombre }}</span>
                        <span class="dial">{{ pais.codigo }}</span>
                      </li>
                      <li v-if="filteredCountries.length === 0" class="country-empty">No se encontraron países</li>
                    </ul>
                  </div>
                </Transition>
              </div>
              
              <!-- Input Teléfono -->
              <div class="input-box phone-input">
                <input v-model="form.telefono" id="telefono" type="tel" required maxlength="10" pattern="[0-9]{10}" placeholder="10 dígitos" @input="validatePhone"/>
              </div>
            </div>
            <span class="hint">Ingresa solo los 10 dígitos (sin lada)</span>
          </div>
        </section>

        <!-- SECCIÓN: SEGURIDAD -->
        <section class="form-section">
          <h3 class="section-title">
            <span class="section-emoji">🔐</span>
            Seguridad
          </h3>

          <!-- Contraseña -->
          <div class="field">
            <label for="password">Contraseña</label>
            <div class="input-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              <input v-model="form.password" id="password" :type="showPassword ? 'text' : 'password'" required minlength="6" placeholder="••••••••"/>
              <button type="button" @click="togglePasswordVisibility" class="toggle-pass">
                <svg v-if="showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
              </button>
            </div>
            <span class="hint">Mínimo 6 caracteres</span>
          </div>

          <!-- Confirmar Contraseña -->
          <div class="field">
            <label for="confirmPassword">Confirmar Contraseña</label>
            <div class="input-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <input v-model="form.confirmPassword" id="confirmPassword" :type="showConfirmPassword ? 'text' : 'password'" required minlength="6" placeholder="Confirmar contraseña"/>
              <button type="button" @click="toggleConfirmPasswordVisibility" class="toggle-pass">
                <svg v-if="showConfirmPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
              </button>
            </div>
          </div>
        </section>

        <!-- SECCIÓN: PRIVACIDAD -->
        <section class="form-section privacy-section">
          <div class="privacy-card">
            <div class="privacy-header">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
              <h4>Aviso de Privacidad</h4>
            </div>
            
            <div class="privacy-content">
              <p class="privacy-main">AVISO DE PRIVACIDAD PARA EL REGISTRO Y USO DE INFORMACIÓN DE LOS TÉCNICOS DEL PROGRAMA SEMBRANDO VIDA MEDIANTE APLICACIÓN MÓVIL OFICIAL</p>
              <p>En cumplimiento con lo dispuesto por la Ley General de Transparencia y Acceso a la Información pública y la Ley Federal de Transparencia y Acceso a la Información Pública, se informa a las y los Técnico(a)s del Programa Sembrando Vida que los datos personales recabados serán tratados conforme a los siguientes términos:</p>
              <p class="sub">1. Identidad y domicilio del responsable</p>
              <p>El responsable del tratamiento de los datos personales es la Secretaría de Bienestar, Subsecretaria de Inclusión Productiva y Desarrollo Rural con domicilio en: Av. P.º de la Reforma 116, Juárez, Cuauhtémoc, 06600 Ciudad de México, CDMX.</p>
              <p class="sub">2. Datos personales que se recaban</p>
              <p>Nombre completo, CURP, Número telefónico, Correo electrónico, Cargo y supervisor asignado, Datos de localización geográfica precisa, Actividades realizadas en campo y fotografías.</p>
              <p class="sub">3. Finalidades del tratamiento</p>
              <p>Los datos serán utilizados exclusivamente para registrar actividades de técnicos, documentar avances del programa y elaborar reportes internos.</p>
              <p class="date">Fecha de última actualización: 12 de agosto del 2025.</p>
              <p class="accept">Al proporcionar mis datos personales, acepto el tratamiento conforme al Aviso de Privacidad.</p>
            </div>
            
            <label class="checkbox-container">
              <input v-model="termsAccepted" @change="clearTermsError" type="checkbox" required/>
              <span class="checkmark">
                <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                </svg>
              </span>
              <span class="checkbox-label">He leído y acepto el Aviso de Privacidad y los Términos y Condiciones <span class="required">*</span></span>
            </label>
            <Transition name="fade">
              <span v-if="termsError" class="hint error terms-error">{{ termsError }}</span>
            </Transition>
          </div>
        </section>

        <!-- Botón Submit -->
        <button type="submit" :disabled="loading || !termsAccepted" class="submit-button" :class="{ disabled: loading || !termsAccepted }">
          <Transition name="fade" mode="out-in">
            <span v-if="loading" class="btn-content">
              <div class="btn-spinner"></div>
              <span>Creando cuenta...</span>
            </span>
            <span v-else-if="!termsAccepted" class="btn-content">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              <span>Acepta los términos</span>
            </span>
            <span v-else class="btn-content">
              <span>Crear mi cuenta</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
              </svg>
            </span>
          </Transition>
        </button>
      </form>

      <!-- Footer -->
      <footer class="register-footer">
        <p>¿Ya tienes cuenta? <router-link to="/login">Inicia sesión</router-link></p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, computed, watch, Teleport, Transition } from 'vue';
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
const countrySearch = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const form = reactive({
  email: '',
  nombre: '',
  primerApellido: '',
  segundoApellido: '',
  cargo: '',
  cargoOtro: '',
  curp: '',
  territorio: '',
  supervisor: '',
  codigoPais: '+52',
  telefono: '',
  password: '',
  confirmPassword: ''
});

const cargosDisponibles = [
  'TECNICO PRODUCTIVO',
  'TECNICO SOCIAL',
  'FACILITADOR COMUNITARIO',
  'COORDINACION TERRITORIAL C',
  'COORDINACION TERRITORIAL B',
  'COORDINACION TERRITORIAL A',
  'ESPECIALISTAS PRODUCTIVOS Y SOCIALES',
  'SEMBRADOR',
  'OTRO'
];

const buscandoSupervisor = ref(false);

const esTecnico = computed(() => {
  const cargoUpper = (form.cargo || '').toUpperCase();
  return cargoUpper === 'TECNICO SOCIAL' || cargoUpper === 'TECNICO PRODUCTIVO';
});

const territoriosSembrandoVida = [
  'Acapulco - Centro - Norte - Tierra Caliente',
  'Acayucan',
  'Balancán',
  'Chihuahua / Sonora',
  'Colima',
  'Comalcalco',
  'Córdoba',
  'Costa Chica - Montaña',
  'Costa Grande - Sierra',
  'Durango / Zacatecas',
  'Hidalgo',
  'Istmo',
  'Michoacán',
  'Mixteca',
  'Morelos',
  'Nayarit / Jalisco',
  'Ocosingo',
  'Palenque',
  'Papantla',
  'Pichucalco',
  'Puebla',
  'San Luis Potosí',
  'Sinaloa',
  'Tamaulipas',
  'Tantoyuca',
  'Tapachula',
  'Teapa',
  'Tlaxcala / Estado de México',
  'Tzucacab / Opb',
  'Xpujil',
  'Oficinas Centrales'
];

const territorioError = ref('');

const paises = [
  { codigo: '+52', nombre: 'México', bandera: '🇲🇽' },
  { codigo: '+1', nombre: 'Estados Unidos', bandera: '🇺🇸' },
  { codigo: '+34', nombre: 'España', bandera: '🇪🇸' },
  { codigo: '+57', nombre: 'Colombia', bandera: '🇨🇴' },
  { codigo: '+56', nombre: 'Chile', bandera: '🇨🇱' },
  { codigo: '+54', nombre: 'Argentina', bandera: '🇦🇷' },
  { codigo: '+51', nombre: 'Perú', bandera: '🇵🇪' },
  { codigo: '+591', nombre: 'Bolivia', bandera: '🇧🇴' },
  { codigo: '+502', nombre: 'Guatemala', bandera: '🇬🇹' },
  { codigo: '+503', nombre: 'El Salvador', bandera: '🇸🇻' }
];

const showCountrySelector = ref(false);

const filteredCountries = computed(() => {
  if (!countrySearch.value) return paises;
  const searchTerm = countrySearch.value.toLowerCase();
  return paises.filter(pais => 
    pais.nombre.toLowerCase().includes(searchTerm) || 
    pais.codigo.includes(searchTerm)
  );
});

watch(() => form.territorio, async (nuevoTerritorio, viejoTerritorio) => {
  if (nuevoTerritorio && nuevoTerritorio !== viejoTerritorio && esTecnico.value) {
    await buscarSupervisorPorTerritorio(nuevoTerritorio);
  }
});

watch(() => form.cargo, async (nuevoCargo, viejoCargo) => {
  if (nuevoCargo !== viejoCargo) {
    const cargoUpper = (nuevoCargo || '').toUpperCase();
    const esNuevoTecnico = cargoUpper === 'TECNICO SOCIAL' || cargoUpper === 'TECNICO PRODUCTIVO';
    
    if (viejoCargo === 'OTRO' && nuevoCargo !== 'OTRO') {
      form.cargoOtro = '';
    }
    
    if (esNuevoTecnico && form.territorio) {
      await buscarSupervisorPorTerritorio(form.territorio);
    } else if (!esNuevoTecnico) {
      form.supervisor = '';
    }
  }
});

onMounted(async () => {
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    message.text = getOfflineMessage();
    message.type = 'error';
  } else {
    try {
      await apiService.refreshApiUrl();
      currentApiUrl.value = apiService.getCurrentApiUrl();
    } catch (error) {
      console.warn('Error inicializando servicio API:', error);
    }
  }
  document.addEventListener('click', closeCountrySelector);
  document.addEventListener('keydown', handleEscKey);
});

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}

function toggleConfirmPasswordVisibility() {
  showConfirmPassword.value = !showConfirmPassword.value;
}

async function register() {
  if (!validateForm()) return;
  
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    message.text = getOfflineMessage();
    message.type = 'error';
    return;
  }
  
  if (loading.value) return;
  
  loading.value = true;
  message.text = '';
  
  try {
    const telefonoCompleto = `${form.codigoPais}${form.telefono.trim()}`;
    const nombreCompleto = `${form.nombre.trim()} ${form.primerApellido.trim()} ${form.segundoApellido.trim()}`.toUpperCase();
    const cargoFinal = form.cargo === 'OTRO' ? form.cargoOtro.trim().toUpperCase() : form.cargo.toUpperCase();
    
    const payload = {
      correo: form.email.trim(),
      nombre_completo: nombreCompleto,
      cargo: cargoFinal,
      supervisor: form.supervisor.trim().toUpperCase(),
      contrasena: form.password,
      curp: form.curp.toUpperCase().trim(),
      telefono: telefonoCompleto,
      territorio: form.territorio
    };
    
    const response = await apiService.createUser(payload);
    currentApiUrl.value = apiService.getCurrentApiUrl();
    showSuccessModal.value = true;
    
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
          message.text = 'El correo electrónico ya está registrado.';
        } else if (detail.includes('CURP')) {
          message.text = 'La CURP ya está registrada.';
        } else {
          message.text = detail || 'Los datos proporcionados son inválidos.';
        }
      } else if (status === 500) {
        message.text = 'Error del servidor. Inténtalo de nuevo.';
      } else {
        message.text = error.response.data.detail || 'Error al crear la cuenta.';
      }
    } else if (error.request) {
      message.text = 'No se pudo conectar con el servidor.';
    } else {
      message.text = 'Error al crear la cuenta: ' + error.message;
    }
    
    message.type = 'error';
  } finally {
    loading.value = false;
  }
}

function validateForm() {
  curpError.value = '';
  curpWarning.value = '';
  termsError.value = '';
  territorioError.value = '';
  message.text = '';
  
  if (!termsAccepted.value) {
    termsError.value = 'Debes aceptar el Aviso de Privacidad';
    message.text = 'Debes aceptar el Aviso de Privacidad';
    message.type = 'error';
    return false;
  }

  if (!form.email || !form.email.trim()) {
    message.text = 'El correo electrónico es obligatorio';
    message.type = 'error';
    return false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(form.email.trim())) {
    message.text = 'Ingresa un correo electrónico válido';
    message.type = 'error';
    return false;
  }

  if (!form.nombre || !form.nombre.trim()) {
    message.text = 'El nombre es obligatorio';
    message.type = 'error';
    return false;
  }

  if (!form.primerApellido || !form.primerApellido.trim()) {
    message.text = 'El apellido paterno es obligatorio';
    message.type = 'error';
    return false;
  }

  if (!form.segundoApellido || !form.segundoApellido.trim()) {
    message.text = 'El apellido materno es obligatorio';
    message.type = 'error';
    return false;
  }

  if (!form.cargo || !form.cargo.trim()) {
    message.text = 'El puesto de trabajo es obligatorio';
    message.type = 'error';
    return false;
  }

  if (form.cargo === 'OTRO' && (!form.cargoOtro || !form.cargoOtro.trim())) {
    message.text = 'Especifica el puesto de trabajo';
    message.type = 'error';
    return false;
  }

  if (!esTecnico.value) {
    if (!form.supervisor || !form.supervisor.trim()) {
      message.text = 'El supervisor inmediato es obligatorio';
      message.type = 'error';
      return false;
    }
  }
  
  if (!form.curp || !form.curp.trim()) {
    curpError.value = 'La CURP es obligatoria';
    message.text = 'La CURP es obligatoria';
    message.type = 'error';
    return false;
  }
  
  if (!form.territorio || !form.territorio.trim()) {
    territorioError.value = 'El territorio es obligatorio';
    message.text = 'Selecciona el territorio';
    message.type = 'error';
    return false;
  }
  
  if (!form.telefono || !form.telefono.trim()) {
    message.text = 'El número de teléfono es obligatorio';
    message.type = 'error';
    return false;
  }
  
  if (!/^\d{10}$/.test(form.telefono.trim())) {
    message.text = 'El teléfono debe tener 10 dígitos';
    message.type = 'error';
    return false;
  }
  
  const curpClean = form.curp.toUpperCase().trim();
  if (curpClean.length !== 18) {
    curpError.value = 'La CURP debe tener 18 caracteres';
    message.text = 'La CURP debe tener 18 caracteres';
    message.type = 'error';
    return false;
  }
  
  const curpRegex = /^[A-Z0-9]{18}$/;
  if (!curpRegex.test(curpClean)) {
    curpError.value = 'Solo letras mayúsculas y números';
    message.text = 'CURP: solo letras mayúsculas y números';
    message.type = 'error';
    return false;
  }
  
  if (form.password !== form.confirmPassword) {
    message.text = 'Las contraseñas no coinciden';
    message.type = 'error';
    return false;
  }
  
  if (form.password.length < 6) {
    message.text = 'Contraseña: mínimo 6 caracteres';
    message.type = 'error';
    return false;
  }
  
  return true;
}

function formatCurp() {
  form.curp = form.curp.toUpperCase();
  curpError.value = '';
  curpWarning.value = '';
  termsError.value = '';
  
  if (form.curp.length > 0 && form.curp.length < 18) {
    curpError.value = `Faltan ${18 - form.curp.length} caracteres`;
  } else if (form.curp.length === 18) {
    const curpRegex = /^[A-Z0-9]{18}$/;
    if (!curpRegex.test(form.curp)) {
      curpError.value = 'Solo letras mayúsculas y números';
    } else {
      curpWarning.value = 'CURP válida ✓';
    }
  }
}

function formatNombre() {
  form.nombre = form.nombre.toUpperCase();
}

function formatPrimerApellido() {
  form.primerApellido = form.primerApellido.toUpperCase();
}

function formatSegundoApellido() {
  form.segundoApellido = form.segundoApellido.toUpperCase();
}

function formatSupervisor() {
  if (!esTecnico.value) {
    form.supervisor = form.supervisor.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }
}

function formatCargoOtro() {
  form.cargoOtro = form.cargoOtro.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

async function buscarSupervisorPorTerritorio(territorio) {
  if (!territorio || !esTecnico.value) return;
  
  buscandoSupervisor.value = true;
  try {
    const response = await apiService.obtenerSupervisorTerritorio(territorio);
    if (response.success && response.supervisor) {
      form.supervisor = response.supervisor;
    } else {
      form.supervisor = '';
    }
  } catch (error) {
    console.error('Error buscando supervisor:', error);
    form.supervisor = '';
  } finally {
    buscandoSupervisor.value = false;
  }
}

function validatePhone() {
  form.telefono = form.telefono.replace(/\D/g, '');
  if (form.telefono.length > 10) {
    form.telefono = form.telefono.slice(0, 10);
  }
}

function selectCountry(pais) {
  form.codigoPais = pais.codigo;
  showCountrySelector.value = false;
}

function closeCountrySelector(e) {
  if (!e.target.closest('.country-selector')) {
    showCountrySelector.value = false;
  }
}

function handleEscKey(event) {
  if (event.key === 'Escape' && showCountrySelector.value) {
    showCountrySelector.value = false;
  }
}

function clearTermsError() {
  termsError.value = '';
  if (message.text && message.text.includes('Aviso de Privacidad')) {
    message.text = '';
  }
}

function handleEnterKey(event) {
  if (!termsAccepted.value) {
    event.preventDefault();
    termsError.value = 'Debes aceptar el Aviso de Privacidad';
    message.text = 'Debes aceptar el Aviso de Privacidad';
    message.type = 'error';
  }
}

function goToLogin() {
  showSuccessModal.value = false;
  router.push('/login');
}
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════════
   REGISTER PAGE - APPLE STYLE CLEAN
   ═══════════════════════════════════════════════════════════════ */

* {
  box-sizing: border-box;
}

.register-page {
  position: fixed;
  inset: 0;
  background: linear-gradient(160deg, #ecfdf5 0%, #d1fae5 50%, #a7f3d0 100%);
  overflow: hidden;
}

.register-scroll {
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  padding: 20px 16px env(safe-area-inset-bottom, 20px);
}

/* Header */
.register-header {
  max-width: 460px;
  margin: 0 auto 20px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50px;
  color: #059669;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.back-link:active {
  transform: scale(0.97);
}

.back-link svg {
  width: 16px;
  height: 16px;
}

/* Title */
.register-title {
  text-align: center;
  margin-bottom: 24px;
}

.title-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
}

.title-icon svg {
  width: 32px;
  height: 32px;
}

.register-title h1 {
  font-size: 28px;
  font-weight: 700;
  color: #064e3b;
  margin: 0 0 6px;
  letter-spacing: -0.5px;
}

.register-title p {
  font-size: 15px;
  color: #6b7280;
  margin: 0;
}

/* Error Banner */
.error-banner {
  max-width: 460px;
  margin: 0 auto 16px;
  padding: 14px 16px;
  background: linear-gradient(135deg, #fef2f2, #fee2e2);
  border-radius: 14px;
  border: 1px solid rgba(239, 68, 68, 0.2);
  display: flex;
  align-items: center;
  gap: 10px;
  color: #dc2626;
  font-size: 14px;
  font-weight: 500;
}

.error-banner svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* Form */
.register-form {
  max-width: 460px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 24px 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.6);
}

/* Section */
.form-section {
  padding: 16px 0;
  border-bottom: 1px solid rgba(16, 185, 129, 0.1);
}

.form-section:last-of-type {
  border-bottom: none;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #064e3b;
  margin: 0 0 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid rgba(16, 185, 129, 0.15);
}

.section-emoji {
  font-size: 16px;
}

/* Field */
.field {
  margin-bottom: 14px;
}

.field:last-child {
  margin-bottom: 0;
}

.field label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}

/* Input Box */
.input-box {
  position: relative;
  display: flex;
  align-items: center;
  background: #f9fafb;
  border: 1.5px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.input-box:focus-within {
  border-color: #10b981;
  background: white;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.input-box.error {
  border-color: #ef4444;
}

.input-box.error:focus-within {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.input-box.success {
  border-color: #10b981;
}

.input-box.disabled {
  background: #f3f4f6;
  opacity: 0.7;
}

.input-box > svg {
  position: absolute;
  left: 12px;
  width: 18px;
  height: 18px;
  color: #9ca3af;
  pointer-events: none;
}

.input-box input {
  flex: 1;
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: none;
  background: transparent;
  font-size: 16px;
  color: #1f2937;
  outline: none;
}

.input-box input::placeholder {
  color: #9ca3af;
}

.input-box input.uppercase {
  text-transform: uppercase;
}

.input-box input.tracking {
  letter-spacing: 1px;
}

.input-box input:read-only {
  cursor: default;
}

.char-count {
  position: absolute;
  right: 12px;
  font-size: 11px;
  color: #9ca3af;
  font-weight: 500;
}

/* Hint */
.hint {
  display: block;
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

.hint.error {
  color: #ef4444;
}

.hint.success {
  color: #10b981;
}

/* Select Box */
.select-box {
  position: relative;
  display: flex;
  align-items: center;
  background: #f9fafb;
  border: 1.5px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.select-box:focus-within {
  border-color: #10b981;
  background: white;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.select-box > svg:first-child {
  position: absolute;
  left: 12px;
  width: 18px;
  height: 18px;
  color: #9ca3af;
  pointer-events: none;
}

.select-box select {
  flex: 1;
  width: 100%;
  padding: 12px 36px 12px 40px;
  border: none;
  background: transparent;
  font-size: 16px;
  color: #1f2937;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
}

.select-box .arrow {
  position: absolute;
  right: 12px;
  width: 16px;
  height: 16px;
  color: #9ca3af;
  pointer-events: none;
}

/* Phone Container */
.phone-container {
  display: flex;
  gap: 8px;
}

.country-selector {
  position: relative;
}

.country-button {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px;
  background: #f9fafb;
  border: 1.5px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.country-button:hover {
  background: white;
  border-color: #10b981;
}

.country-button .flag {
  font-size: 18px;
}

.country-button .code {
  font-weight: 500;
  color: #374151;
}

.country-button svg {
  width: 14px;
  height: 14px;
  color: #9ca3af;
}

.phone-input {
  flex: 1;
}

.phone-input input {
  padding-left: 12px;
}

/* Country Dropdown */
.country-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  width: 240px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(0, 0, 0, 0.05);
  z-index: 100;
  overflow: hidden;
}

.country-search {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-bottom: 1px solid #f3f4f6;
}

.country-search svg {
  width: 16px;
  height: 16px;
  color: #9ca3af;
}

.country-search input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
}

.country-list {
  list-style: none;
  margin: 0;
  padding: 6px;
  max-height: 200px;
  overflow-y: auto;
}

.country-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.country-item:hover {
  background: #f0fdf4;
}

.country-item .flag {
  font-size: 18px;
}

.country-item .name {
  flex: 1;
  font-size: 14px;
  color: #374151;
}

.country-item .dial {
  font-size: 13px;
  color: #9ca3af;
}

.country-empty {
  padding: 16px;
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
}

/* Toggle Password */
.toggle-pass {
  position: absolute;
  right: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.15s ease;
}

.toggle-pass:hover {
  background: rgba(0, 0, 0, 0.04);
}

.toggle-pass svg {
  width: 20px;
  height: 20px;
  color: #9ca3af;
}

/* Spinner */
.spinner {
  position: absolute;
  right: 12px;
  width: 18px;
  height: 18px;
  border: 2px solid #e5e7eb;
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Privacy Section */
.privacy-section {
  padding-bottom: 0;
}

.privacy-card {
  background: #f9fafb;
  border-radius: 14px;
  padding: 16px;
}

.privacy-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.privacy-header svg {
  width: 20px;
  height: 20px;
  color: #10b981;
}

.privacy-header h4 {
  font-size: 14px;
  font-weight: 600;
  color: #064e3b;
  margin: 0;
}

.privacy-content {
  background: white;
  border-radius: 10px;
  padding: 14px;
  max-height: 160px;
  overflow-y: auto;
  font-size: 12px;
  line-height: 1.5;
  color: #6b7280;
  margin-bottom: 14px;
}

.privacy-content p {
  margin: 0 0 10px;
}

.privacy-content .privacy-main {
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  font-size: 11px;
}

.privacy-content .sub {
  font-weight: 600;
  color: #374151;
}

.privacy-content .date {
  font-style: italic;
  color: #9ca3af;
}

.privacy-content .accept {
  font-weight: 500;
  color: #10b981;
}

/* Checkbox */
.checkbox-container {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
}

.checkbox-container input {
  display: none;
}

.checkmark {
  width: 22px;
  height: 22px;
  background: white;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.checkmark svg {
  width: 14px;
  height: 14px;
  opacity: 0;
  transform: scale(0.5);
  transition: all 0.2s ease;
}

.checkbox-container input:checked + .checkmark {
  background: #10b981;
  border-color: #10b981;
}

.checkbox-container input:checked + .checkmark svg {
  opacity: 1;
  transform: scale(1);
}

.checkbox-label {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.4;
}

.checkbox-label .required {
  color: #ef4444;
}

.terms-error {
  margin-top: 8px;
}

/* Submit Button */
.submit-button {
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
  margin-top: 20px;
}

.submit-button:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.submit-button:active:not(.disabled) {
  transform: translateY(0);
}

.submit-button.disabled {
  background: linear-gradient(135deg, #9ca3af, #6b7280);
  cursor: not-allowed;
  box-shadow: none;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-content svg {
  width: 18px;
  height: 18px;
}

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Footer */
.register-footer {
  max-width: 460px;
  margin: 24px auto 0;
  text-align: center;
  padding-bottom: 20px;
}

.register-footer p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.register-footer a {
  color: #059669;
  font-weight: 600;
  text-decoration: none;
}

/* ═══════════════════════════════════════════════════════════════
   MODAL
   ═══════════════════════════════════════════════════════════════ */

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 1000;
}

.modal-card {
  background: white;
  border-radius: 24px;
  padding: 32px 28px;
  max-width: 340px;
  width: 100%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.modal-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 20px;
}

.modal-icon svg {
  width: 100%;
  height: 100%;
}

.modal-title {
  font-size: 22px;
  font-weight: 700;
  color: #064e3b;
  margin: 0 0 8px;
}

.modal-text {
  font-size: 15px;
  color: #6b7280;
  margin: 0 0 20px;
}

.modal-progress {
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 8px;
}

.modal-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #34d399);
  border-radius: 2px;
  animation: progress 3s linear forwards;
}

@keyframes progress {
  from { width: 0%; }
  to { width: 100%; }
}

.modal-redirect {
  font-size: 13px;
  color: #10b981;
  margin: 0 0 20px;
}

.modal-button {
  padding: 12px 24px;
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-button:hover {
  transform: scale(1.03);
}

/* ═══════════════════════════════════════════════════════════════
   TRANSITIONS
   ═══════════════════════════════════════════════════════════════ */

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-card,
.modal-leave-to .modal-card {
  transform: scale(0.9) translateY(20px);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  margin-bottom: 0;
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
  transform-origin: top left;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-8px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ═══════════════════════════════════════════════════════════════
   RESPONSIVE
   ═══════════════════════════════════════════════════════════════ */

@media (max-width: 480px) {
  .register-scroll {
    padding: 16px 12px env(safe-area-inset-bottom, 16px);
  }
  
  .register-title h1 {
    font-size: 24px;
  }
  
  .register-form {
    padding: 20px 16px;
    border-radius: 20px;
  }
  
  .input-box input,
  .select-box select {
    font-size: 16px; /* Prevents iOS zoom */
  }
  
  .country-dropdown {
    width: 220px;
    left: -10px;
  }
}

@media (min-width: 768px) {
  .register-scroll {
    padding: 40px 20px;
  }
  
  .register-title h1 {
    font-size: 32px;
  }
  
  .register-form {
    padding: 32px 28px;
  }
}

/* ═══════════════════════════════════════════════════════════════
   SCROLLBAR
   ═══════════════════════════════════════════════════════════════ */

.register-scroll::-webkit-scrollbar {
  width: 6px;
}

.register-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.register-scroll::-webkit-scrollbar-thumb {
  background: rgba(16, 185, 129, 0.3);
  border-radius: 3px;
}

.register-scroll::-webkit-scrollbar-thumb:hover {
  background: rgba(16, 185, 129, 0.5);
}

.privacy-content::-webkit-scrollbar {
  width: 4px;
}

.privacy-content::-webkit-scrollbar-track {
  background: #f3f4f6;
  border-radius: 2px;
}

.privacy-content::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 2px;
}

/* ═══════════════════════════════════════════════════════════════
   REDUCED MOTION
   ═══════════════════════════════════════════════════════════════ */

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* ═══════════════════════════════════════════════════════════════
   FALLBACK SIN BACKDROP-FILTER
   ═══════════════════════════════════════════════════════════════ */

@supports not (backdrop-filter: blur(20px)) {
  .register-form {
    background: rgba(255, 255, 255, 0.98);
  }
  
  .modal-overlay {
    background: rgba(0, 0, 0, 0.7);
  }
}
</style>
