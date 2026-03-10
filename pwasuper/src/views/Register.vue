<template>
  <div class="apple-register">
    <!-- Success Modal -->
    <Teleport to="body">
      <Transition name="modal-scale">
        <div v-if="showSuccessModal" class="modal-backdrop" @click.self="goToLogin">
          <div class="modal-container">
            <div class="modal-success-icon">
              <svg viewBox="0 0 56 56" fill="none">
                <circle cx="28" cy="28" r="26" stroke="#34C759" stroke-width="3"/>
                <path d="M17 28l7 7 15-15" stroke="#34C759" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h2 class="modal-heading">Registro Exitoso</h2>
            <p class="modal-description">Tu cuenta ha sido creada correctamente</p>
            <div class="modal-progress-track">
              <div class="modal-progress-fill"></div>
            </div>
            <p class="modal-redirect-text">Redirigiendo al inicio de sesión...</p>
            <button @click="goToLogin" class="modal-action-btn">Continuar</button>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Main Content -->
    <div class="register-content">
      <!-- Fixed Navigation Header -->
      <nav class="register-nav">
        <div class="nav-container">
          <router-link to="/login" class="nav-back-btn">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M15 19l-7-7 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Volver</span>
          </router-link>
          <h1 class="nav-title">Crear Cuenta</h1>
          <div class="nav-spacer"></div>
        </div>
      </nav>

      <!-- Header Section -->
      <header class="register-hero">
        <p class="hero-instruction">Completa el formulario con tus datos personales y laborales para crear tu cuenta en el sistema.</p>
      </header>

      <!-- Error Alert -->
      <Transition name="alert-slide">
        <div v-if="message.text && message.type === 'error'" class="error-alert">
          <div class="alert-icon">
            <svg viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M12 8v4m0 4h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <span class="alert-text">{{ message.text }}</span>
        </div>
      </Transition>

      <!-- Registration Form -->
      <form @submit.prevent="register" @keydown.enter="handleEnterKey" class="register-form">
        
        <!-- Personal Information -->
        <div class="form-group">
          <div class="group-header">
            <div class="group-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="2"/>
                <path d="M4 20c0-4.418 3.582-8 8-8s8 3.582 8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <h3 class="group-title">Datos Personales</h3>
          </div>

          <!-- Email -->
          <div class="form-field">
            <label class="field-label">Correo Electrónico</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <rect x="2" y="4" width="20" height="16" rx="3" stroke="currentColor" stroke-width="2"/>
                <path d="M2 7l10 6 10-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <input v-model="form.email" type="email" autocomplete="email" required placeholder="tu@email.com"/>
            </div>
          </div>

          <!-- Name -->
          <div class="form-field">
            <label class="field-label">Nombre(s)</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
              </svg>
              <input v-model="form.nombre" @input="formatNombre" type="text" required placeholder="NOMBRE COMPLETO" class="uppercase-input"/>
            </div>
            <span class="field-hint">Ingresa tu nombre o nombres de pila</span>
          </div>

          <!-- First Last Name -->
          <div class="form-field">
            <label class="field-label">Apellido Paterno</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
              </svg>
              <input v-model="form.primerApellido" @input="formatPrimerApellido" type="text" required placeholder="APELLIDO PATERNO" class="uppercase-input"/>
            </div>
          </div>

          <!-- Second Last Name -->
          <div class="form-field">
            <label class="field-label">Apellido Materno</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
              </svg>
              <input v-model="form.segundoApellido" @input="formatSegundoApellido" type="text" required placeholder="APELLIDO MATERNO" class="uppercase-input"/>
            </div>
          </div>

          <!-- CURP -->
          <div class="form-field">
            <label class="field-label">CURP</label>
            <div class="input-wrapper" :class="{ 'has-error': curpError, 'has-success': curpWarning }">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 8h10M7 12h6M7 16h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <input v-model="form.curp" @input="formatCurp" type="text" required maxlength="18" placeholder="CURP (18 CARACTERES)" class="uppercase-input letter-spaced"/>
              <span v-if="form.curp" class="char-counter">{{ form.curp.length }}/18</span>
            </div>
            <span v-if="curpError" class="field-hint error-hint">{{ curpError }}</span>
            <span v-else-if="curpWarning" class="field-hint success-hint">{{ curpWarning }}</span>
            <span v-else class="field-hint">Clave Única de Registro de Población</span>
          </div>
        </div>

        <!-- Work Information -->
        <div class="form-group">
          <div class="group-header">
            <div class="group-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <rect x="2" y="7" width="20" height="14" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2" stroke="currentColor" stroke-width="2"/>
                <path d="M12 12v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <h3 class="group-title">Información Laboral</h3>
          </div>

          <!-- Territory -->
          <div class="form-field">
            <label class="field-label">Territorio</label>
            <div class="select-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="9" r="2.5" stroke="currentColor" stroke-width="2"/>
              </svg>
              <select v-model="form.territorio" required>
                <option value="" disabled>Selecciona tu territorio</option>
                <option v-for="territorio in territoriosSembrandoVida" :key="territorio" :value="territorio">{{ territorio }}</option>
              </select>
              <svg class="select-arrow" viewBox="0 0 24 24" fill="none">
                <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <span v-if="territorioError" class="field-hint error-hint">{{ territorioError }}</span>
            <span v-else class="field-hint">Selecciona tu área de trabajo</span>
          </div>

          <!-- Position -->
          <div class="form-field">
            <label class="field-label">Puesto de Trabajo</label>
            <div class="select-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
              </svg>
              <select v-model="form.cargo" required>
                <option value="" disabled>Selecciona tu puesto</option>
                <option v-for="cargo in cargosDisponibles" :key="cargo" :value="cargo">{{ cargo }}</option>
              </select>
              <svg class="select-arrow" viewBox="0 0 24 24" fill="none">
                <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>

          <!-- Other Position -->
          <Transition name="field-expand">
            <div v-if="form.cargo === 'OTRO'" class="form-field">
              <label class="field-label">Especifica tu cargo</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                  <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M18.5 2.5a2.121 2.121 0 113 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <input v-model="form.cargoOtro" @input="formatCargoOtro" type="text" required placeholder="NOMBRE DEL CARGO" class="uppercase-input"/>
              </div>
            </div>
          </Transition>

          <!-- Supervisor -->
          <div class="form-field">
            <label class="field-label">Supervisor Inmediato</label>
            <div class="input-wrapper" :class="{ 'is-disabled': esTecnico }">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="9" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <input v-model="form.supervisor" @input="formatSupervisor" type="text" required :readonly="esTecnico" :placeholder="esTecnico && buscandoSupervisor ? 'Buscando...' : 'NOMBRE DEL SUPERVISOR'" class="uppercase-input"/>
              <div v-if="buscandoSupervisor" class="input-spinner"></div>
            </div>
            <span v-if="esTecnico" class="field-hint success-hint">
              <svg viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/>
                <path d="M5 8l2 2 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Supervisor asignado automáticamente
            </span>
            <span v-else class="field-hint">Nombre completo de tu jefe directo</span>
          </div>
        </div>

        <!-- Contact Information -->
        <div class="form-group">
          <div class="group-header">
            <div class="group-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <rect x="5" y="2" width="14" height="20" rx="3" stroke="currentColor" stroke-width="2"/>
                <path d="M12 18h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <h3 class="group-title">Contacto</h3>
          </div>

          <!-- Phone -->
          <div class="form-field">
            <label class="field-label">Número de Teléfono</label>
            <div class="phone-field">
              <!-- Country Code Selector -->
              <div class="country-code-selector">
                <button type="button" @click="showCountrySelector = !showCountrySelector" class="country-trigger">
                  <span class="country-code-text">{{ paises.find(p => p.codigo === form.codigoPais)?.abrev || 'MX' }}</span>
                  <span class="country-dial">{{ form.codigoPais }}</span>
                  <svg class="country-arrow" viewBox="0 0 24 24" fill="none">
                    <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                
                <Transition name="dropdown-fade">
                  <div v-if="showCountrySelector" class="country-panel">
                    <div class="country-search-box">
                      <svg viewBox="0 0 24 24" fill="none">
                        <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/>
                        <path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                      </svg>
                      <input type="text" v-model="countrySearch" placeholder="Buscar país..." @click.stop/>
                    </div>
                    <ul class="country-options">
                      <li v-for="pais in filteredCountries" :key="pais.codigo" @click="selectCountry(pais)" class="country-option">
                        <span class="country-abbr">{{ pais.abrev }}</span>
                        <span class="country-name">{{ pais.nombre }}</span>
                        <span class="country-dial-code">{{ pais.codigo }}</span>
                      </li>
                      <li v-if="filteredCountries.length === 0" class="country-empty">Sin resultados</li>
                    </ul>
                  </div>
                </Transition>
              </div>
              
              <!-- Phone Input -->
              <div class="input-wrapper phone-input-wrapper">
                <input v-model="form.telefono" type="tel" required maxlength="10" pattern="[0-9]{10}" placeholder="10 dígitos" @input="validatePhone"/>
              </div>
            </div>
            <span class="field-hint">Solo los 10 dígitos sin lada</span>
          </div>
        </div>

        <!-- Security -->
        <div class="form-group">
          <div class="group-header">
            <div class="group-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 11V7a5 5 0 0110 0v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <h3 class="group-title">Seguridad</h3>
          </div>

          <!-- Password -->
          <div class="form-field">
            <label class="field-label">Contraseña <span class="required-mark">*</span></label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 11V7a5 5 0 0110 0v4" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="16" r="1.5" fill="currentColor"/>
              </svg>
              <input v-model="form.password" @input="checkPasswordsMatch" :type="showPassword ? 'text' : 'password'" required minlength="6" placeholder="Mínimo 6 caracteres"/>
              <button type="button" @click="togglePasswordVisibility" class="visibility-toggle">
                <svg v-if="showPassword" viewBox="0 0 24 24" fill="none">
                  <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M1 1l22 22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2"/>
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
            <span class="field-hint">Usa al menos 6 caracteres</span>
          </div>

          <!-- Confirm Password -->
          <div class="form-field">
            <label class="field-label">Confirmar Contraseña <span class="required-mark">*</span></label>
            <div class="input-wrapper" :class="{ 'has-error': !passwordsMatch && form.confirmPassword.length > 0, 'has-success': passwordsMatch && form.confirmPassword.length >= 6 }">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              </svg>
              <input v-model="form.confirmPassword" @input="checkPasswordsMatch" :type="showConfirmPassword ? 'text' : 'password'" required minlength="6" placeholder="Repite tu contraseña"/>
              <button type="button" @click="toggleConfirmPasswordVisibility" class="visibility-toggle">
                <svg v-if="showConfirmPassword" viewBox="0 0 24 24" fill="none">
                  <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M1 1l22 22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2"/>
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
            <span v-if="!passwordsMatch && form.confirmPassword.length > 0" class="field-hint error-hint">Las contraseñas no coinciden</span>
            <span v-else-if="passwordsMatch && form.confirmPassword.length >= 6" class="field-hint success-hint">
              <svg viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/>
                <path d="M5 8l2 2 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Las contraseñas coinciden
            </span>
          </div>
        </div>

        <!-- Privacy Agreement -->
        <div class="form-group privacy-agreement">
          <div class="privacy-container">
            <div class="privacy-header">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <h4>Aviso de Privacidad</h4>
            </div>
            
            <div class="privacy-scroll-area">
              <p class="privacy-title-text">AVISO DE PRIVACIDAD PARA EL REGISTRO Y USO DE INFORMACIÓN DE LOS TÉCNICOS DEL PROGRAMA SEMBRANDO VIDA MEDIANTE APLICACIÓN MÓVIL OFICIAL</p>
              <p>En cumplimiento con lo dispuesto por la Ley General de Transparencia y Acceso a la Información pública y la Ley Federal de Transparencia y Acceso a la Información Pública, se informa a las y los Técnico(a)s del Programa Sembrando Vida que los datos personales recabados serán tratados conforme a los siguientes términos:</p>
              <p class="privacy-section-title">1. Identidad y domicilio del responsable</p>
              <p>El responsable del tratamiento de los datos personales es la Secretaría de Bienestar, Subsecretaria de Inclusión Productiva y Desarrollo Rural con domicilio en: Av. P.º de la Reforma 116, Juárez, Cuauhtémoc, 06600 Ciudad de México, CDMX.</p>
              <p class="privacy-section-title">2. Datos personales que se recaban</p>
              <p>Nombre completo, CURP, Número telefónico, Correo electrónico, Cargo y supervisor asignado, Datos de localización geográfica precisa, Actividades realizadas en campo y fotografías.</p>
              <p class="privacy-section-title">3. Finalidades del tratamiento</p>
              <p>Los datos serán utilizados exclusivamente para registrar actividades de técnicos, documentar avances del programa y elaborar reportes internos.</p>
              <p class="privacy-date">Fecha de última actualización: 12 de agosto del 2025.</p>
              <p class="privacy-accept-text">Al proporcionar mis datos personales, acepto el tratamiento conforme al Aviso de Privacidad.</p>
            </div>
            
            <label class="checkbox-field">
              <input v-model="termsAccepted" @change="clearTermsError" type="checkbox" required/>
              <span class="checkbox-indicator">
                <svg viewBox="0 0 16 16" fill="none">
                  <path d="M3.5 8l3 3 6-6" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <span class="checkbox-text">He leído y acepto el Aviso de Privacidad y los Términos y Condiciones <span class="required-mark">*</span></span>
            </label>
            <Transition name="hint-fade">
              <span v-if="termsError" class="field-hint error-hint terms-error-hint">{{ termsError }}</span>
            </Transition>
          </div>
        </div>

        <!-- Submit Button -->
        <button type="submit" :disabled="loading || !termsAccepted || !passwordsMatch || !isFormComplete" class="submit-btn" :class="{ 'is-loading': loading, 'is-disabled': !termsAccepted || !passwordsMatch || !isFormComplete }">
          <Transition name="btn-fade" mode="out-in">
            <span v-if="loading" key="loading" class="btn-inner">
              <div class="btn-loader"></div>
              <span>Creando cuenta...</span>
            </span>
            <span v-else-if="!isFormComplete" key="incomplete" class="btn-inner">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M12 8v4m0 4h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <span>Completa todos los campos</span>
            </span>
            <span v-else-if="!termsAccepted" key="locked" class="btn-inner">
              <svg viewBox="0 0 24 24" fill="none">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 11V7a5 5 0 0110 0v4" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>Acepta los términos</span>
            </span>
            <span v-else-if="!passwordsMatch" key="mismatch" class="btn-inner">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M15 9l-6 6m0-6l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <span>Las contraseñas deben coincidir</span>
            </span>
            <span v-else key="ready" class="btn-inner">
              <span>Crear mi cuenta</span>
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14m-6-6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
          </Transition>
        </button>
      </form>

      <!-- Footer -->
      <footer class="register-footer">
        <p>¿Ya tienes una cuenta? <router-link to="/login">Iniciar sesión</router-link></p>
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
const passwordsMatch = ref(true);

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

const isFormComplete = computed(() => {
  // Validar campos básicos
  const basicFieldsFilled = 
    form.email.trim() !== '' &&
    form.nombre.trim() !== '' &&
    form.primerApellido.trim() !== '' &&
    form.segundoApellido.trim() !== '' &&
    form.cargo.trim() !== '' &&
    form.curp.trim() !== '' &&
    form.territorio.trim() !== '' &&
    form.supervisor.trim() !== '' &&
    form.telefono.trim() !== '' &&
    form.password.trim() !== '' &&
    form.confirmPassword.trim() !== '';
  
  // Si el cargo es "OTRO", también debe llenar cargoOtro
  const cargoOtroFilled = form.cargo.toUpperCase() === 'OTRO' 
    ? form.cargoOtro.trim() !== '' 
    : true;
  
  return basicFieldsFilled && cargoOtroFilled;
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
  { codigo: '+52', nombre: 'México', abrev: 'MX' },
  { codigo: '+1', nombre: 'Estados Unidos', abrev: 'US' },
  { codigo: '+34', nombre: 'España', abrev: 'ES' },
  { codigo: '+57', nombre: 'Colombia', abrev: 'CO' },
  { codigo: '+56', nombre: 'Chile', abrev: 'CL' },
  { codigo: '+54', nombre: 'Argentina', abrev: 'AR' },
  { codigo: '+51', nombre: 'Perú', abrev: 'PE' },
  { codigo: '+591', nombre: 'Bolivia', abrev: 'BO' },
  { codigo: '+502', nombre: 'Guatemala', abrev: 'GT' },
  { codigo: '+503', nombre: 'El Salvador', abrev: 'SV' }
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

function checkPasswordsMatch() {
  if (form.confirmPassword.length > 0) {
    passwordsMatch.value = form.password === form.confirmPassword;
  } else {
    passwordsMatch.value = true;
  }
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
      curpWarning.value = 'CURP válida';
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
  if (!e.target.closest('.country-code-selector')) {
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
/* ==========================================================================
   APPLE DESIGN SYSTEM - REGISTER PAGE
   Clean, Minimal, Professional
   ========================================================================== */

/* Base Reset */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Main Container */
.apple-register {
  position: fixed;
  inset: 0;
  background: #f5f5f7;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Scrollable Content */
.register-content {
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  padding: 0 20px env(safe-area-inset-bottom, 20px);
  padding-top: 0;
}

/* Fixed Navigation */
.register-nav {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(245, 245, 247, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 0 20px;
  margin: 0 -20px;
}

.nav-container {
  max-width: 500px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  gap: 16px;
}

.nav-back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 980px;
  color: #06c;
  font-size: 15px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.25, 0.1, 0.25, 1);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  flex-shrink: 0;
}

.nav-back-btn:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateX(-2px);
}

.nav-back-btn:active {
  transform: scale(0.97);
}

.nav-back-btn svg {
  width: 16px;
  height: 16px;
}

.nav-title {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
  letter-spacing: -0.4px;
  margin: 0;
  text-align: center;
  flex: 1;
}

.nav-spacer {
  width: 90px;
  flex-shrink: 0;
}

/* Hero Section */
.register-hero {
  text-align: center;
  padding: 24px 0 20px;
  max-width: 500px;
  margin: 0 auto;
}

.hero-instruction {
  font-size: 15px;
  line-height: 1.5;
  color: #86868b;
  font-weight: 400;
  margin: 0;
  text-align: center;
}

/* Error Alert */
.error-alert {
  max-width: 500px;
  margin: 0 auto 20px;
  padding: 16px;
  background: #fff2f2;
  border-radius: 12px;
  border: 1px solid rgba(255, 59, 48, 0.2);
  display: flex;
  align-items: center;
  gap: 12px;
}

.alert-icon {
  flex-shrink: 0;
}

.alert-icon svg {
  width: 22px;
  height: 22px;
  color: #ff3b30;
}

.alert-text {
  font-size: 14px;
  color: #ff3b30;
  font-weight: 500;
  line-height: 1.4;
}

/* Form Container */
.register-form {
  max-width: 500px;
  margin: 0 auto;
}

/* Form Groups */
.form-group {
  background: white;
  border-radius: 14px;
  padding: 18px;
  margin-bottom: 14px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.group-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f5f5f7;
}

.group-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(180deg, #34c759 0%, #30b350 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.group-icon svg {
  width: 16px;
  height: 16px;
  color: white;
}

.group-title {
  font-size: 15px;
  font-weight: 600;
  color: #1d1d1f;
  letter-spacing: -0.2px;
}

/* Form Fields */
.form-field {
  margin-bottom: 20px;
}

.form-field:last-child {
  margin-bottom: 0;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 8px;
  letter-spacing: -0.1px;
}

/* Input Wrapper */
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: #f5f5f7;
  border: 2px solid transparent;
  border-radius: 12px;
  transition: all 0.2s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.input-wrapper:focus-within {
  background: white;
  border-color: #34c759;
  box-shadow: 0 0 0 4px rgba(52, 199, 89, 0.1);
}

.input-wrapper.has-error {
  border-color: #ff3b30;
}

.input-wrapper.has-error:focus-within {
  box-shadow: 0 0 0 4px rgba(255, 59, 48, 0.1);
}

.input-wrapper.has-success {
  border-color: #34c759;
}

.input-wrapper.is-disabled {
  background: #e8e8ed;
  cursor: not-allowed;
}

.input-icon {
  position: absolute;
  left: 14px;
  width: 20px;
  height: 20px;
  color: #86868b;
  pointer-events: none;
  transition: color 0.2s ease;
}

.input-wrapper:focus-within .input-icon {
  color: #34c759;
}

.input-wrapper.has-error .input-icon {
  color: #ff3b30;
}

.input-wrapper input {
  flex: 1;
  width: 100%;
  padding: 14px 14px 14px 46px;
  border: none;
  background: transparent;
  font-size: 17px;
  color: #1d1d1f;
  outline: none;
  font-family: inherit;
}

.input-wrapper input::placeholder {
  color: #86868b;
}

.input-wrapper input.uppercase-input {
  text-transform: uppercase;
}

.input-wrapper input.letter-spaced {
  letter-spacing: 2px;
}

.input-wrapper input:read-only {
  cursor: default;
  color: #86868b;
}

.char-counter {
  position: absolute;
  right: 14px;
  font-size: 12px;
  color: #86868b;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
}

/* Field Hints */
.field-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #86868b;
  margin-top: 6px;
}

.field-hint svg {
  width: 14px;
  height: 14px;
}

.field-hint.error-hint {
  color: #ff3b30;
}

.field-hint.success-hint {
  color: #34c759;
}

/* Select Wrapper */
.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: #f5f5f7;
  border: 2px solid transparent;
  border-radius: 12px;
  transition: all 0.2s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.select-wrapper:focus-within {
  background: white;
  border-color: #34c759;
  box-shadow: 0 0 0 4px rgba(52, 199, 89, 0.1);
}

.select-wrapper select {
  flex: 1;
  width: 100%;
  padding: 14px 44px 14px 46px;
  border: none;
  background: transparent;
  font-size: 17px;
  color: #1d1d1f;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
  font-family: inherit;
}

.select-wrapper select option {
  color: #1d1d1f;
}

.select-arrow {
  position: absolute;
  right: 14px;
  width: 20px;
  height: 20px;
  color: #86868b;
  pointer-events: none;
}

/* Phone Field */
.phone-field {
  display: flex;
  gap: 10px;
}

.country-code-selector {
  position: relative;
  flex-shrink: 0;
}

.country-trigger {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 14px 12px;
  background: #f5f5f7;
  border: 2px solid transparent;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  color: #1d1d1f;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.country-trigger:hover {
  background: #e8e8ed;
}

.country-code-text {
  font-weight: 600;
  color: #34c759;
}

.country-dial {
  color: #86868b;
}

.country-arrow {
  width: 16px;
  height: 16px;
  color: #86868b;
}

.phone-input-wrapper {
  flex: 1;
}

.phone-input-wrapper input {
  padding-left: 14px;
}

/* Country Panel */
.country-panel {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  width: 280px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(0, 0, 0, 0.05);
  z-index: 100;
  overflow: hidden;
}

.country-search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px;
  border-bottom: 1px solid #f5f5f7;
}

.country-search-box svg {
  width: 18px;
  height: 18px;
  color: #86868b;
}

.country-search-box input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  font-family: inherit;
  color: #1d1d1f;
}

.country-search-box input::placeholder {
  color: #86868b;
}

.country-options {
  list-style: none;
  max-height: 240px;
  overflow-y: auto;
  padding: 8px;
}

.country-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.country-option:hover {
  background: #f5f5f7;
}

.country-abbr {
  font-size: 13px;
  font-weight: 700;
  color: #34c759;
  min-width: 28px;
}

.country-name {
  flex: 1;
  font-size: 15px;
  color: #1d1d1f;
}

.country-dial-code {
  font-size: 14px;
  color: #86868b;
  font-variant-numeric: tabular-nums;
}

.country-empty {
  padding: 20px;
  text-align: center;
  color: #86868b;
  font-size: 14px;
}

/* Visibility Toggle */
.visibility-toggle {
  position: absolute;
  right: 8px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: 10px;
  transition: background 0.15s ease;
}

.visibility-toggle:hover {
  background: rgba(0, 0, 0, 0.04);
}

.visibility-toggle svg {
  width: 22px;
  height: 22px;
  color: #86868b;
}

/* Input Spinner */
.input-spinner {
  position: absolute;
  right: 14px;
  width: 20px;
  height: 20px;
  border: 2px solid #e8e8ed;
  border-top-color: #34c759;
  border-radius: 50%;
  animation: spinner-rotate 0.8s linear infinite;
}

@keyframes spinner-rotate {
  to { transform: rotate(360deg); }
}

/* Privacy Agreement */
.privacy-agreement {
  background: transparent;
  padding: 0;
  box-shadow: none;
}

.privacy-container {
  background: white;
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.privacy-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.privacy-header svg {
  width: 24px;
  height: 24px;
  color: #34c759;
}

.privacy-header h4 {
  font-size: 17px;
  font-weight: 600;
  color: #1d1d1f;
}

.privacy-scroll-area {
  background: #f5f5f7;
  border-radius: 12px;
  padding: 16px;
  max-height: 180px;
  overflow-y: auto;
  font-size: 13px;
  line-height: 1.6;
  color: #6e6e73;
  margin-bottom: 20px;
}

.privacy-scroll-area p {
  margin-bottom: 12px;
}

.privacy-scroll-area p:last-child {
  margin-bottom: 0;
}

.privacy-title-text {
  font-weight: 700;
  color: #1d1d1f;
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.5px;
}

.privacy-section-title {
  font-weight: 600;
  color: #1d1d1f;
  margin-top: 16px;
}

.privacy-date {
  font-style: italic;
  color: #86868b;
}

.privacy-accept-text {
  font-weight: 500;
  color: #34c759;
}

/* Checkbox */
.checkbox-field {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  cursor: pointer;
}

.checkbox-field input {
  display: none;
}

.checkbox-indicator {
  width: 24px;
  height: 24px;
  background: #f5f5f7;
  border: 2px solid #d2d2d7;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.checkbox-indicator svg {
  width: 14px;
  height: 14px;
  opacity: 0;
  transform: scale(0.5);
  transition: all 0.2s ease;
}

.checkbox-field input:checked + .checkbox-indicator {
  background: #34c759;
  border-color: #34c759;
}

.checkbox-field input:checked + .checkbox-indicator svg {
  opacity: 1;
  transform: scale(1);
}

.checkbox-text {
  font-size: 14px;
  color: #6e6e73;
  line-height: 1.5;
}

.required-mark {
  color: #ff3b30;
  font-weight: 600;
}

.terms-error-hint {
  margin-top: 12px;
}

/* Submit Button */
.submit-btn {
  width: 100%;
  padding: 18px 24px;
  background: linear-gradient(180deg, #34c759 0%, #30b350 100%);
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.25, 0.1, 0.25, 1);
  box-shadow: 0 4px 14px rgba(52, 199, 89, 0.35);
  font-family: inherit;
  margin-top: 10px;
}

.submit-btn:hover:not(.is-loading):not(.is-disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(52, 199, 89, 0.4);
}

.submit-btn:active:not(.is-loading):not(.is-disabled) {
  transform: translateY(0);
}

.submit-btn.is-disabled {
  background: linear-gradient(180deg, #8e8e93 0%, #7c7c80 100%);
  cursor: not-allowed;
  box-shadow: none;
}

.submit-btn.is-loading {
  cursor: wait;
}

.btn-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-inner svg {
  width: 20px;
  height: 20px;
}

.btn-loader {
  width: 20px;
  height: 20px;
  border: 2.5px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spinner-rotate 0.8s linear infinite;
}

/* Footer */
.register-footer {
  max-width: 500px;
  margin: 30px auto;
  text-align: center;
  padding-bottom: 30px;
}

.register-footer p {
  font-size: 15px;
  color: #86868b;
}

.register-footer a {
  color: #06c;
  font-weight: 600;
  text-decoration: none;
}

.register-footer a:hover {
  text-decoration: underline;
}

/* ==========================================================================
   MODAL
   ========================================================================== */

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  z-index: 1000;
}

.modal-container {
  background: white;
  border-radius: 24px;
  padding: 40px 32px;
  max-width: 380px;
  width: 100%;
  text-align: center;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.25);
}

.modal-success-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
}

.modal-success-icon svg {
  width: 100%;
  height: 100%;
}

.modal-heading {
  font-size: 24px;
  font-weight: 700;
  color: #1d1d1f;
  margin-bottom: 8px;
  letter-spacing: -0.3px;
}

.modal-description {
  font-size: 16px;
  color: #86868b;
  margin-bottom: 24px;
}

.modal-progress-track {
  height: 4px;
  background: #f5f5f7;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 8px;
}

.modal-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #34c759, #30d158);
  border-radius: 2px;
  animation: progress-fill 3s linear forwards;
}

@keyframes progress-fill {
  from { width: 0%; }
  to { width: 100%; }
}

.modal-redirect-text {
  font-size: 13px;
  color: #34c759;
  font-weight: 500;
  margin-bottom: 24px;
}

.modal-action-btn {
  padding: 14px 32px;
  background: linear-gradient(180deg, #34c759 0%, #30b350 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.modal-action-btn:hover {
  transform: scale(1.03);
}

.modal-action-btn:active {
  transform: scale(0.98);
}

/* ==========================================================================
   TRANSITIONS
   ========================================================================== */

/* Modal Scale */
.modal-scale-enter-active,
.modal-scale-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.modal-scale-enter-from,
.modal-scale-leave-to {
  opacity: 0;
}

.modal-scale-enter-from .modal-container,
.modal-scale-leave-to .modal-container {
  transform: scale(0.92) translateY(20px);
  opacity: 0;
}

/* Alert Slide */
.alert-slide-enter-active,
.alert-slide-leave-active {
  transition: all 0.3s ease;
}

.alert-slide-enter-from {
  opacity: 0;
  transform: translateY(-12px);
}

.alert-slide-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

/* Field Expand */
.field-expand-enter-active,
.field-expand-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.field-expand-enter-from,
.field-expand-leave-to {
  opacity: 0;
  max-height: 0;
  margin-bottom: 0;
}

/* Dropdown Fade */
.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: all 0.2s ease;
  transform-origin: top left;
}

.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-6px);
}

/* Hint Fade */
.hint-fade-enter-active,
.hint-fade-leave-active {
  transition: opacity 0.2s ease;
}

.hint-fade-enter-from,
.hint-fade-leave-to {
  opacity: 0;
}

/* Button Fade */
.btn-fade-enter-active,
.btn-fade-leave-active {
  transition: all 0.2s ease;
}

.btn-fade-enter-from,
.btn-fade-leave-to {
  opacity: 0;
  transform: translateY(4px);
}

/* ==========================================================================
   RESPONSIVE
   ========================================================================== */

@media (max-width: 480px) {
  .register-content {
    padding: 0 16px env(safe-area-inset-bottom, 16px);
    padding-top: 0;
  }
  
  .register-nav {
    padding: 0 16px;
    margin: 0 -16px;
  }
  
  .nav-container {
    height: 52px;
  }
  
  .nav-title {
    font-size: 18px;
  }
  
  .nav-back-btn {
    padding: 7px 12px;
    font-size: 14px;
  }
  
  .nav-back-btn svg {
    width: 14px;
    height: 14px;
  }
  
  .nav-spacer {
    width: 80px;
  }
  
  .hero-instruction {
    font-size: 14px;
  }
  
  .form-group {
    padding: 20px;
    border-radius: 16px;
  }
  
  .group-title {
    font-size: 18px;
  }
  
  .input-wrapper input,
  .select-wrapper select {
    font-size: 16px; /* Prevents iOS zoom */
    padding: 13px 13px 13px 44px;
  }
  
  .country-panel {
    width: 260px;
    left: -8px;
  }
}

@media (min-width: 768px) {
  .register-content {
    padding: 0 24px 40px;
    padding-top: 0;
  }
  
  .register-nav {
    padding: 0 24px;
    margin: 0 -24px;
  }
  
  .nav-container {
    height: 60px;
  }
  
  .nav-title {
    font-size: 22px;
  }
  
  .form-group {
    padding: 22px;
  }
}

/* ==========================================================================
   SCROLLBAR
   ========================================================================== */

.register-content::-webkit-scrollbar {
  width: 8px;
}

.register-content::-webkit-scrollbar-track {
  background: transparent;
}

.register-content::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.15);
  border-radius: 4px;
}

.register-content::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.25);
}

.privacy-scroll-area::-webkit-scrollbar {
  width: 4px;
}

.privacy-scroll-area::-webkit-scrollbar-track {
  background: #e8e8ed;
  border-radius: 2px;
}

.privacy-scroll-area::-webkit-scrollbar-thumb {
  background: #c7c7cc;
  border-radius: 2px;
}

.country-options::-webkit-scrollbar {
  width: 6px;
}

.country-options::-webkit-scrollbar-track {
  background: transparent;
}

.country-options::-webkit-scrollbar-thumb {
  background: #d2d2d7;
  border-radius: 3px;
}

/* ==========================================================================
   REDUCED MOTION
   ========================================================================== */

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* ==========================================================================
   BACKDROP FILTER FALLBACK
   ========================================================================== */

@supports not (backdrop-filter: blur(20px)) {
  .register-nav {
    background: rgba(245, 245, 247, 0.98);
  }
  
  .modal-backdrop {
    background: rgba(0, 0, 0, 0.8);
  }
}
</style>
