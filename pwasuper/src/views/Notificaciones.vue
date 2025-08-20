<template>
  <div class="fixed inset-0 bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 overflow-hidden" style="z-index: 0;">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-3" style="z-index: 1;">
      <div class="page-container w-full max-w-sm mx-auto relative z-10 p-3 sm:p-4 lg:p-5">
        <!-- Header de notificaciones -->
        <div class="glass-card mb-2">
          <div class="text-center mb-3">
            <div class="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-2 glass-avatar">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-3.5-3.5a.928.928 0 010-1.314L20 8.5h-5M9 17H4l3.5-3.5a.928.928 0 000-1.314L4 8.5h5M12 3v18M10.5 21.5a1.5 1.5 0 003 0" />
              </svg>
            </div>
            <h1 class="text-base font-bold text-gray-800 modern-title">Centro de Notificaciones</h1>
            <div class="green-line mx-auto mb-2"></div>
            <p class="text-xs text-gray-600">Mantente al día con todas las actualizaciones</p>
          </div>
        </div>

        <!-- Filtros de notificaciones -->
        <div class="glass-card mb-2">
          <div class="flex justify-between items-center mb-2">
            <h2 class="text-sm font-semibold text-gray-800 modern-title flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              Filtros
            </h2>
            <button @click="clearAllNotifications" class="text-xs text-red-500 hover:text-red-600 transition-colors" :disabled="notifications.length === 0">
              Limpiar todo
            </button>
          </div>
          <div class="green-line mb-2"></div>
          
          <!-- Toggle para mostrar solo no leídas -->
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-medium text-gray-700">Solo no leídas</span>
            <button 
              @click="toggleUnreadOnly" 
              :class="[
                'relative inline-flex h-4 w-7 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2',
                showUnreadOnly ? 'bg-green-500' : 'bg-gray-300'
              ]"
            >
              <span 
                :class="[
                  'inline-block h-3 w-3 transform rounded-full bg-white transition-transform',
                  showUnreadOnly ? 'translate-x-3.5' : 'translate-x-0.5'
                ]"
              />
            </button>
          </div>
          
          <!-- Estadísticas -->
          <div class="grid grid-cols-3 gap-2 text-center">
            <div class="bg-white/20 rounded-lg p-2">
              <div class="text-lg font-bold text-green-600">{{ totalNotifications }}</div>
              <div class="text-xs text-gray-600">Total</div>
            </div>
            <div class="bg-white/20 rounded-lg p-2">
              <div class="text-lg font-bold text-blue-600">{{ unreadCount }}</div>
              <div class="text-xs text-gray-600">No leídas</div>
            </div>
            <div class="bg-white/20 rounded-lg p-2">
              <div class="text-lg font-bold text-gray-600">{{ readCount }}</div>
              <div class="text-xs text-gray-600">Leídas</div>
            </div>
          </div>
        </div>

        <!-- Lista de notificaciones -->
        <div class="glass-card">
          <h2 class="text-sm font-semibold text-gray-800 mb-2 modern-title flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 2a3.5 3.5 0 013.5 3.5c0 .379-.061.744-.177 1.092l.177-.092a8.5 8.5 0 018.5 8.5v3a1.5 1.5 0 01-1.5 1.5H3a1.5 1.5 0 01-1.5-1.5v-3a8.5 8.5 0 018.5-8.5l.177.092A3.485 3.485 0 0110.5 5.5 3.5 3.5 0 0110 2zM9 21a2 2 0 002 2h2a2 2 0 002-2" />
            </svg>
            Notificaciones Recientes
          </h2>
          <div class="green-line mb-3"></div>
          
          <!-- Estado vacío -->
          <div v-if="filteredNotifications.length === 0" class="text-center py-8">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M15 17h5l-3.5-3.5a.928.928 0 010-1.314L20 8.5h-5M9 17H4l3.5-3.5a.928.928 0 000-1.314L4 8.5h5M12 3v18M10.5 21.5a1.5 1.5 0 003 0" />
            </svg>
            <h3 class="text-sm font-medium text-gray-600 mb-1">No hay notificaciones</h3>
            <p class="text-xs text-gray-400">
              {{ showUnreadOnly ? 'No tienes notificaciones sin leer' : 'Todas las notificaciones aparecerán aquí' }}
            </p>
          </div>

          <!-- Lista de notificaciones -->
          <div v-else class="space-y-3">
            <div 
              v-for="notification in filteredNotifications" 
              :key="notification.id"
              @click="markAsRead(notification.id)"
              :class="[
                'notification-item border-l-4 p-3 rounded-lg cursor-pointer transition-all duration-200 hover:bg-white/30',
                notification.read ? 'border-gray-300 bg-white/10' : 'border-blue-500 bg-blue-50/30'
              ]"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center mb-1">
                    <div :class="[
                      'w-2 h-2 rounded-full mr-2 flex-shrink-0',
                      notification.read ? 'bg-gray-400' : 'bg-blue-500'
                    ]"></div>
                    <h4 :class="[
                      'text-sm font-medium',
                      notification.read ? 'text-gray-600' : 'text-gray-800'
                    ]">{{ notification.title }}</h4>
                    <div :class="[
                      'ml-2 px-1.5 py-0.5 text-xs rounded-full font-medium',
                      getTypeStyle(notification.type)
                    ]">
                      {{ getTypeLabel(notification.type) }}
                    </div>
                  </div>
                  <p :class="[
                    'text-xs mb-2',
                    notification.read ? 'text-gray-500' : 'text-gray-700'
                  ]">{{ notification.message }}</p>
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-gray-400">{{ formatTime(notification.timestamp) }}</span>
                    <button 
                      v-if="!notification.read"
                      @click.stop="markAsRead(notification.id)"
                      class="text-xs text-blue-500 hover:text-blue-600 font-medium"
                    >
                      Marcar como leída
                    </button>
                  </div>
                </div>
                <button 
                  @click.stop="removeNotification(notification.id)"
                  class="ml-2 text-gray-400 hover:text-red-500 transition-colors"
                  title="Eliminar notificación"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Configuración de notificaciones -->
        <div class="glass-card mt-2">
          <h2 class="text-sm font-semibold text-gray-800 mb-2 modern-title flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Configuración
          </h2>
          <div class="green-line mb-2"></div>
          
          <div class="space-y-3">
            <!-- Notificaciones push -->
            <div class="flex items-center justify-between">
              <div>
                <span class="text-xs font-medium text-gray-700">Notificaciones Push</span>
                <p class="text-xs text-gray-500">Recibe notificaciones en el navegador</p>
              </div>
              <button 
                @click="togglePushNotifications" 
                :class="[
                  'relative inline-flex h-4 w-7 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2',
                  pushNotificationsEnabled ? 'bg-green-500' : 'bg-gray-300'
                ]"
              >
                <span 
                  :class="[
                    'inline-block h-3 w-3 transform rounded-full bg-white transition-transform',
                    pushNotificationsEnabled ? 'translate-x-3.5' : 'translate-x-0.5'
                  ]"
                />
              </button>
            </div>
            
            <!-- Sonido -->
            <div class="flex items-center justify-between">
              <div>
                <span class="text-xs font-medium text-gray-700">Sonido</span>
                <p class="text-xs text-gray-500">Reproducir sonido con las notificaciones</p>
              </div>
              <button 
                @click="toggleSoundEnabled" 
                :class="[
                  'relative inline-flex h-4 w-7 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2',
                  soundEnabled ? 'bg-green-500' : 'bg-gray-300'
                ]"
              >
                <span 
                  :class="[
                    'inline-block h-3 w-3 transform rounded-full bg-white transition-transform',
                    soundEnabled ? 'translate-x-3.5' : 'translate-x-0.5'
                  ]"
                />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Estados reactivos
const notifications = ref([])
const showUnreadOnly = ref(false)
const pushNotificationsEnabled = ref(false)
const soundEnabled = ref(true)

// Notificaciones de ejemplo
const sampleNotifications = [
  {
    id: 1,
    title: 'Asistencia registrada',
    message: 'Tu entrada del día de hoy ha sido registrada correctamente a las 08:30 AM.',
    type: 'success',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 horas atrás
    read: false
  },
  {
    id: 2,
    title: 'Recordatorio de salida',
    message: 'No olvides registrar tu salida al finalizar tu jornada laboral.',
    type: 'reminder',
    timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 horas atrás
    read: false
  },
  {
    id: 3,
    title: 'Actividad completada',
    message: 'La actividad "Mantenimiento de equipo" ha sido marcada como completada.',
    type: 'info',
    timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // 1 día atrás
    read: true
  },
  {
    id: 4,
    title: 'Actualización del sistema',
    message: 'Se ha actualizado la aplicación. Recarga la página para ver las mejoras.',
    type: 'warning',
    timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 días atrás
    read: true
  },
  {
    id: 5,
    title: 'Perfil actualizado',
    message: 'Tu información de perfil ha sido actualizada exitosamente.',
    type: 'success',
    timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 días atrás
    read: true
  }
]

// Computed properties
const filteredNotifications = computed(() => {
  if (showUnreadOnly.value) {
    return notifications.value.filter(n => !n.read)
  }
  return notifications.value
})

const totalNotifications = computed(() => notifications.value.length)
const unreadCount = computed(() => notifications.value.filter(n => !n.read).length)
const readCount = computed(() => notifications.value.filter(n => n.read).length)

// Funciones
const markAsRead = (id) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification && !notification.read) {
    notification.read = true
    saveNotificationsToStorage()
  }
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
    saveNotificationsToStorage()
  }
}

const clearAllNotifications = () => {
  if (confirm('¿Estás seguro de que quieres eliminar todas las notificaciones?')) {
    notifications.value = []
    saveNotificationsToStorage()
  }
}

const toggleUnreadOnly = () => {
  showUnreadOnly.value = !showUnreadOnly.value
  localStorage.setItem('showUnreadOnly', showUnreadOnly.value.toString())
}

const togglePushNotifications = async () => {
  if (!pushNotificationsEnabled.value) {
    // Solicitar permiso para notificaciones
    if ('Notification' in window) {
      const permission = await Notification.requestPermission()
      if (permission === 'granted') {
        pushNotificationsEnabled.value = true
        localStorage.setItem('pushNotificationsEnabled', 'true')
        
        // Mostrar notificación de confirmación
        new Notification('Notificaciones activadas', {
          body: 'Ahora recibirás notificaciones de Sembrando Vida',
          icon: '/pwa-192x192.png'
        })
      }
    }
  } else {
    pushNotificationsEnabled.value = false
    localStorage.setItem('pushNotificationsEnabled', 'false')
  }
}

const toggleSoundEnabled = () => {
  soundEnabled.value = !soundEnabled.value
  localStorage.setItem('soundEnabled', soundEnabled.value.toString())
}

const getTypeStyle = (type) => {
  const styles = {
    success: 'bg-green-100 text-green-800',
    info: 'bg-blue-100 text-blue-800',
    warning: 'bg-yellow-100 text-yellow-800',
    error: 'bg-red-100 text-red-800',
    reminder: 'bg-purple-100 text-purple-800'
  }
  return styles[type] || styles.info
}

const getTypeLabel = (type) => {
  const labels = {
    success: 'Éxito',
    info: 'Info',
    warning: 'Aviso',
    error: 'Error',
    reminder: 'Recordatorio'
  }
  return labels[type] || 'Info'
}

const formatTime = (timestamp) => {
  const now = new Date()
  const diff = now - timestamp
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor(diff / (1000 * 60))
  
  if (days > 0) {
    return `Hace ${days} día${days > 1 ? 's' : ''}`
  } else if (hours > 0) {
    return `Hace ${hours} hora${hours > 1 ? 's' : ''}`
  } else if (minutes > 0) {
    return `Hace ${minutes} minuto${minutes > 1 ? 's' : ''}`
  } else {
    return 'Ahora'
  }
}

const saveNotificationsToStorage = () => {
  localStorage.setItem('notifications', JSON.stringify(notifications.value))
}

const loadNotificationsFromStorage = () => {
  try {
    const saved = localStorage.getItem('notifications')
    if (saved) {
      const parsed = JSON.parse(saved)
      // Convertir timestamps de string a Date
      notifications.value = parsed.map(n => ({
        ...n,
        timestamp: new Date(n.timestamp)
      }))
    } else {
      // Si no hay notificaciones guardadas, usar las de ejemplo
      notifications.value = sampleNotifications
      saveNotificationsToStorage()
    }
  } catch (error) {
    console.error('Error loading notifications:', error)
    notifications.value = sampleNotifications
  }
}

const loadSettings = () => {
  // Cargar configuración de mostrar solo no leídas
  const savedShowUnreadOnly = localStorage.getItem('showUnreadOnly')
  if (savedShowUnreadOnly !== null) {
    showUnreadOnly.value = savedShowUnreadOnly === 'true'
  }
  
  // Cargar configuración de notificaciones push
  const savedPushEnabled = localStorage.getItem('pushNotificationsEnabled')
  if (savedPushEnabled !== null) {
    pushNotificationsEnabled.value = savedPushEnabled === 'true'
  }
  
  // Cargar configuración de sonido
  const savedSoundEnabled = localStorage.getItem('soundEnabled')
  if (savedSoundEnabled !== null) {
    soundEnabled.value = savedSoundEnabled === 'true'
  }
}

// Función para agregar notificaciones (puede ser llamada desde otros componentes)
const addNotification = (notification) => {
  const newNotification = {
    id: Date.now(),
    timestamp: new Date(),
    read: false,
    ...notification
  }
  notifications.value.unshift(newNotification)
  saveNotificationsToStorage()
  
  // Mostrar notificación push si está habilitada
  if (pushNotificationsEnabled.value && 'Notification' in window && Notification.permission === 'granted') {
    new Notification(newNotification.title, {
      body: newNotification.message,
      icon: '/pwa-192x192.png'
    })
  }
  
  // Reproducir sonido si está habilitado
  if (soundEnabled.value) {
    // Aquí puedes agregar el código para reproducir un sonido
    console.log('🔔 Reproduciendo sonido de notificación')
  }
}

onMounted(() => {
  loadNotificationsFromStorage()
  loadSettings()
  
  // Hacer la función addNotification disponible globalmente
  window.addNotification = addNotification
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Efecto de vidrio realista - Glassmorphism */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 6px 25px 0 rgba(31, 38, 135, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  padding: 0.875rem;
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -50%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: skewX(-25deg);
  transition: all 0.6s;
}

.glass-card:hover::before {
  left: 150%;
}

.glass-avatar {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px 0 rgba(59, 130, 246, 0.3),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.modern-title {
  background: linear-gradient(
    90deg, 
    #166534 0%, 
    #15803d 25%, 
    #86efac 50%, 
    #15803d 75%, 
    #166534 100%
  );
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: gradient-wave 3s ease-in-out infinite;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.015em;
  font-weight: 500;
  position: relative;
}

.green-line {
  width: 40px;
  height: 1.5px;
  background: linear-gradient(90deg, #16a34a, #22c55e, #16a34a);
  border-radius: 1px;
  animation: line-glow 2s ease-in-out infinite alternate;
}

@keyframes gradient-wave {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes line-glow {
  0% {
    box-shadow: 0 0 5px rgba(34, 197, 94, 0.3);
    opacity: 0.8;
  }
  100% {
    box-shadow: 0 0 15px rgba(34, 197, 94, 0.6);
    opacity: 1;
  }
}

/* Animación para elementos decorativos */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

/* Respaldo para navegadores que no soportan background-clip: text */
@supports not (-webkit-background-clip: text) {
  .modern-title {
    color: #166534;
    animation: none;
  }
}

/* Estilos para notificaciones */
.notification-item {
  transition: all 0.2s ease;
}

.notification-item:hover {
  transform: translateX(2px);
}

/* Mejoras de responsividad para pantallas móviles */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }
  
  .glass-card {
    padding: 0.625rem;
    margin-bottom: 0.375rem;
    border-radius: 12px;
  }
  
  .text-base {
    font-size: 0.8rem;
  }
  
  .text-sm {
    font-size: 0.75rem;
  }
  
  .w-12, .h-12 {
    width: 2.75rem;
    height: 2.75rem;
  }
  
  .h-6, .w-6 {
    height: 1.25rem;
    width: 1.25rem;
  }
  
  .mb-2 {
    margin-bottom: 0.375rem;
  }
  
  .mb-3 {
    margin-bottom: 0.5rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.5rem;
  }
}

@media (max-width: 375px) {
  .page-container {
    padding-left: 0.375rem;
    padding-right: 0.375rem;
    max-width: calc(100vw - 0.75rem);
  }
  
  .glass-card {
    padding: 0.5rem;
    margin-bottom: 0.25rem;
    border-radius: 10px;
  }
  
  .text-base {
    font-size: 0.75rem;
  }
  
  .text-sm {
    font-size: 0.7rem;
  }
  
  .text-xs {
    font-size: 0.65rem;
  }
}

@media (max-height: 700px) {
  .page-container {
    padding-top: 0.375rem;
    padding-bottom: 0.375rem;
  }
  
  .glass-card {
    margin-bottom: 0.25rem;
    padding: 0.5rem;
  }
  
  .mb-2 {
    margin-bottom: 0.25rem;
  }
  
  .mb-3 {
    margin-bottom: 0.375rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.375rem;
  }
}

/* Para pantallas grandes */
@media (min-width: 768px) {
  .page-container {
    max-width: 350px;
    padding: 0.75rem;
  }
  
  .glass-card {
    padding: 1rem;
    margin-bottom: 0.75rem;
  }
}

/* Soporte adicional para navegadores que no soportan backdrop-filter */
@supports not (backdrop-filter: blur(20px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.85);
  }
}
</style>