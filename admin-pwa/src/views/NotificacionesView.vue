<template>
  <div class="notificaciones-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                <circle cx="12" cy="8" r="1" opacity="0.6"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Centro de Notificaciones</h1>
              <p class="header-subtitle">Administra y envía notificaciones a los usuarios</p>
            </div>
          </div>
          <div class="header-actions">
            <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
              <div class="status-indicator"></div>
              <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
            </div>
            <button @click="cargarNotificaciones" class="refresh-btn" :disabled="loading">
              <svg class="refresh-icon" :class="{ spinning: loading }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10"></polyline>
                <polyline points="1 20 1 14 7 14"></polyline>
                <path d="m3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
              </svg>
              {{ loading ? 'Cargando...' : 'Actualizar' }}
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Panel de filtros avanzados -->
        <div class="advanced-filters">
          <!-- Filtros principales -->
          <div class="filters-main">
            <!-- Contenedor izquierdo con filtros -->
            <div class="filters-left">
              <!-- Barra de búsqueda -->
              <div class="search-box">
                <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input 
                  v-model="filtros.search" 
                  type="text" 
                  placeholder="Buscar notificaciones..." 
                  class="search-input"
                  @input="cargarNotificaciones"
                >
                <button v-if="filtros.search" @click="limpiarBusqueda" class="clear-search-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
              
              <!-- Filtros por estado y tipo -->
              <div class="filter-selects">
                <select v-model="filtros.status" @change="cargarNotificaciones" class="filter-select">
                  <option value="">Todos los estados</option>
                  <option value="draft">📝 Borradores</option>
                  <option value="scheduled">⏰ Programadas</option>
                  <option value="sent">✅ Enviadas</option>
                  <option value="failed">❌ Fallidas</option>
                </select>
                
                <select v-model="filtros.type" @change="cargarNotificaciones" class="filter-select">
                  <option value="">Todos los tipos</option>
                  <option value="info">ℹ️ Informativas</option>
                  <option value="success">✅ Éxito</option>
                  <option value="warning">⚠️ Advertencias</option>
                  <option value="urgent">🚨 Urgentes</option>
                </select>
              </div>
            </div>
            
            <!-- Contadores de estadísticas en el lado derecho -->
            <div class="filters-right">
              <div class="visor-stats-compact">
                <div class="compact-stat-card">
                  <div class="compact-stat-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" fill="#4CAF50" opacity="0.8"/>
                      <circle cx="12" cy="8" r="4" fill="#66BB6A" opacity="0.5"/>
                    </svg>
                  </div>
                  <div class="compact-stat-info">
                    <div class="compact-stat-value">{{ estadisticas.general?.total_notifications || 0 }}</div>
                    <div class="compact-stat-label">Total</div>
                  </div>
                </div>
                
                <div class="compact-stat-card">
                  <div class="compact-stat-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M22 17H2a3 3 0 0 0 3-3V9a7 7 0 0 1 14 0v5a3 3 0 0 0 3 3z" fill="#4CAF50" opacity="0.7"/>
                      <path d="M19 17v2a3 3 0 0 1-3 3h-8a3 3 0 0 1-3-3v-2" stroke="#4CAF50" stroke-width="2"/>
                    </svg>
                  </div>
                  <div class="compact-stat-info">
                    <div class="compact-stat-value">{{ estadisticas.general?.sent_notifications || 0 }}</div>
                    <div class="compact-stat-label">Enviadas</div>
                  </div>
                </div>

                <div class="compact-stat-card">
                  <div class="compact-stat-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="#4CAF50" stroke-width="2" fill="none"/>
                      <circle cx="8.5" cy="7" r="4" fill="#66BB6A"/>
                      <circle cx="17" cy="11" r="6" fill="#4CAF50" opacity="0.5"/>
                    </svg>
                  </div>
                  <div class="compact-stat-info">
                    <div class="compact-stat-value">{{ estadisticas.general?.total_devices || 0 }}</div>
                    <div class="compact-stat-label">Dispositivos</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Contenido principal de notificaciones -->
        <div class="notificaciones-section">
          <!-- Estado de carga -->
          <div v-if="loading" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando notificaciones...</p>
          </div>
          
          <!-- Lista de notificaciones -->
          <div v-else-if="notificaciones.length > 0" class="notifications-list">
            <div class="list-header">
              <div class="list-title">
                <h3>Notificaciones ({{ totalNotificaciones }})</h3>
                <button @click="abrirModalCrear" class="create-btn-header">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="16"/>
                    <line x1="8" y1="12" x2="16" y2="12"/>
                  </svg>
                  Nueva
                </button>
              </div>
            </div>
            
            <div class="notifications-grid">
              <div 
                v-for="notificacion in notificaciones" 
                :key="notificacion.id"
                class="notification-card"
                :class="[`status-${notificacion.status}`, `type-${notificacion.type}`]"
              >
                <div class="notification-header">
                  <div class="notification-type">
                    <span class="type-badge" :class="notificacion.type">
                      {{ getTipoIcon(notificacion.type) }} {{ getTipoLabel(notificacion.type) }}
                    </span>
                  </div>
                  <div class="notification-actions">
                    <button 
                      v-if="notificacion.status === 'draft'" 
                      @click="enviarNotificacion(notificacion.id)"
                      class="action-btn send"
                      title="Enviar ahora"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22,2 15,22 11,13 2,9"></polygon>
                      </svg>
                    </button>
                    <button 
                      @click="verDetalles(notificacion)"
                      class="action-btn view"
                      title="Ver detalles"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </button>
                    <button 
                      @click="eliminarNotificacion(notificacion.id)"
                      class="action-btn delete"
                      title="Eliminar"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3,6 5,6 21,6"></polyline>
                        <path d="m19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"></path>
                      </svg>
                    </button>
                  </div>
                </div>
                
                <div class="notification-content">
                  <h4 class="notification-title">{{ notificacion.title }}</h4>
                  <p class="notification-body">{{ notificacion.body }}</p>
                </div>
                
                <div class="notification-meta">
                  <div class="meta-item">
                    <span class="meta-label">Audiencia:</span>
                    <span class="meta-value">{{ getAudienciaLabel(notificacion.audience) }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="meta-label">Estado:</span>
                    <span class="meta-value status" :class="notificacion.status">{{ getStatusLabel(notificacion.status) }}</span>
                  </div>
                </div>
                
                <div class="notification-stats">
                  <div class="stat-item">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                      <circle cx="8.5" cy="7" r="4"></circle>
                    </svg>
                    <span>{{ notificacion.stats?.total_recipients || 0 }} destinatarios</span>
                  </div>
                  <div class="stat-item">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                    </svg>
                    <span>{{ notificacion.stats?.total_reads || 0 }} leídas ({{ notificacion.stats?.read_rate || 0 }}%)</span>
                  </div>
                </div>
                
                <div class="notification-footer">
                  <div class="notification-date">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"></circle>
                      <polyline points="12,6 12,12 16,14"></polyline>
                    </svg>
                    {{ formatearFecha(notificacion.created_at) }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Paginación -->
            <div v-if="totalNotificaciones > filtros.limit" class="pagination">
              <button 
                @click="paginaAnterior" 
                :disabled="filtros.offset === 0"
                class="pagination-btn"
              >
                ← Anterior
              </button>
              <span class="pagination-info">
                {{ filtros.offset + 1 }}-{{ Math.min(filtros.offset + filtros.limit, totalNotificaciones) }} de {{ totalNotificaciones }}
              </span>
              <button 
                @click="paginaSiguiente" 
                :disabled="filtros.offset + filtros.limit >= totalNotificaciones"
                class="pagination-btn"
              >
                Siguiente →
              </button>
            </div>
          </div>
          
          <!-- Estado vacío -->
          <div v-else class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                <circle cx="12" cy="8" r="1" opacity="0.6"/>
              </svg>
            </div>
            <h3>{{ filtros.search ? 'No se encontraron notificaciones' : 'No hay notificaciones' }}</h3>
            <p>{{ filtros.search ? 'Intenta con otros términos de búsqueda' : 'Aún no se han configurado notificaciones en el sistema.' }}</p>
            <button @click="abrirModalCrear" class="create-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="16"/>
                <line x1="8" y1="12" x2="16" y2="12"/>
              </svg>
              Crear Nueva Notificación
            </button>
          </div>
        </div>
      </div>
    </main>
    
    <!-- Modal de creación/edición -->
    <NotificacionModal 
      :visible="mostrarModal"
      :notificacion="notificacionEditar"
      @close="cerrarModal"
      @saved="onNotificacionGuardada"
      @error="mostrarError"
    />
    
    <!-- Toast de mensajes -->
    <div v-if="mensaje.texto" class="toast" :class="mensaje.tipo">
      <div class="toast-content">
        <svg v-if="mensaje.tipo === 'success'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        <svg v-else-if="mensaje.tipo === 'error'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="15" y1="9" x2="9" y2="15"></line>
          <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
        <span>{{ mensaje.texto }}</span>
      </div>
      <button @click="ocultarMensaje" class="toast-close">×</button>
    </div>
  </div>
</template>

<script>
import Sidebar from '../components/Sidebar.vue'
import NotificacionModal from '../components/NotificacionModal.vue'
import notificacionesService from '../services/notificacionesService.js'

export default {
  name: 'NotificacionesView',
  components: {
    Sidebar,
    NotificacionModal
  },
  data() {
    return {
      loading: false,
      isOnline: navigator.onLine,
      notificaciones: [],
      totalNotificaciones: 0,
      estadisticas: {},
      mostrarModal: false,
      notificacionEditar: null,
      filtros: {
        search: '',
        status: '',
        type: '',
        limit: 10,
        offset: 0
      },
      mensaje: {
        texto: '',
        tipo: 'success' // success, error, info
      }
    }
  },
  mounted() {
    this.configurarEventosConexion()
    this.inicializar()
  },
  methods: {
    async inicializar() {
      await Promise.all([
        this.cargarEstadisticas(),
        this.cargarNotificaciones()
      ])
    },
    
    async cargarNotificaciones() {
      try {
        this.loading = true
        
        const response = await notificacionesService.obtenerNotificaciones(this.filtros)
        
        this.notificaciones = response.notifications || []
        this.totalNotificaciones = response.total || 0
        
      } catch (error) {
        console.error('Error cargando notificaciones:', error)
        this.mostrarError('Error al cargar las notificaciones')
        this.notificaciones = []
        this.totalNotificaciones = 0
      } finally {
        this.loading = false
      }
    },
    
    async cargarEstadisticas() {
      try {
        this.estadisticas = await notificacionesService.obtenerEstadisticas()
      } catch (error) {
        console.error('Error cargando estadísticas:', error)
        this.estadisticas = {
          general: {
            total_notifications: 0,
            sent_notifications: 0,
            total_devices: 0
          }
        }
      }
    },
    
    async enviarNotificacion(id) {
      try {
        await notificacionesService.enviarNotificacion(id)
        this.mostrarExito('Notificación enviada exitosamente')
        await this.cargarNotificaciones()
        await this.cargarEstadisticas()
      } catch (error) {
        console.error('Error enviando notificación:', error)
        this.mostrarError('Error al enviar la notificación')
      }
    },
    
    async eliminarNotificacion(id) {
      if (!confirm('¿Estás seguro de que deseas eliminar esta notificación?')) {
        return
      }
      
      try {
        await notificacionesService.eliminarNotificacion(id)
        this.mostrarExito('Notificación eliminada exitosamente')
        await this.cargarNotificaciones()
        await this.cargarEstadisticas()
      } catch (error) {
        console.error('Error eliminando notificación:', error)
        this.mostrarError('Error al eliminar la notificación')
      }
    },
    
    verDetalles(notificacion) {
      // TODO: Implementar modal de detalles
      console.log('Ver detalles:', notificacion)
      this.mostrarInfo('Funcionalidad de detalles próximamente')
    },
    
    abrirModalCrear() {
      this.notificacionEditar = null
      this.mostrarModal = true
    },
    
    abrirModalEditar(notificacion) {
      this.notificacionEditar = notificacion
      this.mostrarModal = true
    },
    
    cerrarModal() {
      this.mostrarModal = false
      this.notificacionEditar = null
    },
    
    async onNotificacionGuardada(resultado) {
      this.mostrarExito('Notificación guardada exitosamente')
      await this.cargarNotificaciones()
      await this.cargarEstadisticas()
    },
    
    limpiarBusqueda() {
      this.filtros.search = ''
      this.cargarNotificaciones()
    },
    
    paginaAnterior() {
      if (this.filtros.offset > 0) {
        this.filtros.offset -= this.filtros.limit
        this.cargarNotificaciones()
      }
    },
    
    paginaSiguiente() {
      if (this.filtros.offset + this.filtros.limit < this.totalNotificaciones) {
        this.filtros.offset += this.filtros.limit
        this.cargarNotificaciones()
      }
    },
    
    configurarEventosConexion() {
      window.addEventListener('online', () => {
        this.isOnline = true
        this.cargarNotificaciones()
      })
      
      window.addEventListener('offline', () => {
        this.isOnline = false
      })
    },
    
    // Métodos de utilidad
    getTipoIcon(type) {
      const icons = {
        info: 'ℹ️',
        success: '✅',
        warning: '⚠️',
        urgent: '🚨'
      }
      return icons[type] || 'ℹ️'
    },
    
    getTipoLabel(type) {
      const labels = {
        info: 'Informativa',
        success: 'Éxito',
        warning: 'Advertencia',
        urgent: 'Urgente'
      }
      return labels[type] || 'Informativa'
    },
    
    getStatusLabel(status) {
      const labels = {
        draft: 'Borrador',
        scheduled: 'Programada',
        sending: 'Enviando',
        sent: 'Enviada',
        failed: 'Fallida'
      }
      return labels[status] || 'Desconocido'
    },
    
    getAudienciaLabel(audience) {
      const labels = {
        all: 'Todos los usuarios',
        users: 'Usuarios específicos'
      }
      return labels[audience] || 'Desconocido'
    },
    
    formatearFecha(fechaISO) {
      if (!fechaISO) return 'Sin fecha'
      
      const fecha = new Date(fechaISO)
      const ahora = new Date()
      const diffMs = ahora - fecha
      const diffMinutos = Math.floor(diffMs / 60000)
      const diffHoras = Math.floor(diffMinutos / 60)
      const diffDias = Math.floor(diffHoras / 24)
      
      if (diffMinutos < 1) {
        return 'Hace un momento'
      } else if (diffMinutos < 60) {
        return `Hace ${diffMinutos} minuto${diffMinutos > 1 ? 's' : ''}`
      } else if (diffHoras < 24) {
        return `Hace ${diffHoras} hora${diffHoras > 1 ? 's' : ''}`
      } else if (diffDias < 7) {
        return `Hace ${diffDias} día${diffDias > 1 ? 's' : ''}`
      } else {
        return fecha.toLocaleDateString('es-ES', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      }
    },
    
    // Métodos de mensajes
    mostrarExito(texto) {
      this.mensaje = { texto, tipo: 'success' }
      setTimeout(() => this.ocultarMensaje(), 4000)
    },
    
    mostrarError(texto) {
      this.mensaje = { texto, tipo: 'error' }
      setTimeout(() => this.ocultarMensaje(), 6000)
    },
    
    mostrarInfo(texto) {
      this.mensaje = { texto, tipo: 'info' }
      setTimeout(() => this.ocultarMensaje(), 4000)
    },
    
    ocultarMensaje() {
      this.mensaje = { texto: '', tipo: 'success' }
    },
    
    logout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.notificaciones-container {
  display: flex;
  min-height: 100vh;
  background-color: #f9f9f9;
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw); /* Ajusta según el ancho del sidebar */
  padding: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-x: hidden;
}

.page-header {
  padding: 1.5rem 2rem;
  background: linear-gradient(to right, #ffffff, #f5f5f5);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.header-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.header-text {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  color: #2E7D32;
}

.header-subtitle {
  font-size: 0.95rem;
  color: #666;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.connection-status {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.connection-status.online {
  background-color: rgba(76, 175, 80, 0.1);
  color: #2E7D32;
}

.connection-status.offline {
  background-color: rgba(244, 67, 54, 0.1);
  color: #C62828;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
}

.online .status-indicator {
  background-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.3);
  animation: pulse 1.5s infinite;
}

.offline .status-indicator {
  background-color: #F44336;
  box-shadow: 0 0 0 2px rgba(244, 67, 54, 0.3);
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0.5rem 1rem;
  background: linear-gradient(to bottom, #ffffff, #f9f9f9);
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  color: #333;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background: linear-gradient(to bottom, #f9f9f9, #f0f0f0);
  border-color: #d0d0d0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.refresh-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.refresh-icon {
  transition: transform 0.5s ease;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4); }
  70% { box-shadow: 0 0 0 5px rgba(76, 175, 80, 0); }
  100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
}

.page-content {
  flex: 1;
  padding: 1.5rem 2rem;
  display: flex;
  flex-direction: column;
}

.advanced-filters {
  background: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
}

.filters-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.filters-left {
  flex: 1;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 280px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #4CAF50;
  background-color: #ffffff;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.clear-search-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  width: 20px;
  height: 20px;
}

.filter-selects {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.filter-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background-color: #f9f9f9;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 150px;
}

.filter-select:focus {
  outline: none;
  border-color: #4CAF50;
  background-color: #ffffff;
}

/* Lista de notificaciones */
.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.list-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.list-title h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.create-btn-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(to bottom, #4CAF50, #43A047);
  border: none;
  border-radius: 6px;
  color: white;
  font-weight: 500;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-btn-header:hover {
  background: linear-gradient(to bottom, #43A047, #388E3C);
  transform: translateY(-1px);
}

.notifications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.notification-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.notification-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.notification-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: #4CAF50;
}

.notification-card.type-warning::before {
  background: #FF9800;
}

.notification-card.type-urgent::before {
  background: #F44336;
}

.notification-card.type-success::before {
  background: #4CAF50;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.type-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.type-badge.info {
  background: rgba(33, 150, 243, 0.1);
  color: #1976D2;
}

.type-badge.success {
  background: rgba(76, 175, 80, 0.1);
  color: #2E7D32;
}

.type-badge.warning {
  background: rgba(255, 152, 0, 0.1);
  color: #F57C00;
}

.type-badge.urgent {
  background: rgba(244, 67, 54, 0.1);
  color: #C62828;
}

.notification-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.action-btn.send {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.action-btn.send:hover {
  background: rgba(76, 175, 80, 0.2);
}

.action-btn.view {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
}

.action-btn.view:hover {
  background: rgba(33, 150, 243, 0.2);
}

.action-btn.delete {
  background: rgba(244, 67, 54, 0.1);
  color: #F44336;
}

.action-btn.delete:hover {
  background: rgba(244, 67, 54, 0.2);
}

.notification-content {
  margin-bottom: 1rem;
}

.notification-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 0.5rem;
  line-height: 1.3;
}

.notification-body {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.notification-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f5f5f5;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.meta-label {
  font-size: 0.75rem;
  color: #999;
  text-transform: uppercase;
  font-weight: 500;
}

.meta-value {
  font-size: 0.85rem;
  color: #333;
  font-weight: 500;
}

.meta-value.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.meta-value.status.draft {
  background: rgba(158, 158, 158, 0.1);
  color: #666;
}

.meta-value.status.scheduled {
  background: rgba(255, 152, 0, 0.1);
  color: #F57C00;
}

.meta-value.status.sent {
  background: rgba(76, 175, 80, 0.1);
  color: #2E7D32;
}

.meta-value.status.failed {
  background: rgba(244, 67, 54, 0.1);
  color: #C62828;
}

.notification-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #666;
}

.stat-item svg {
  opacity: 0.7;
}

.notification-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #999;
}

/* Paginación */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 1rem;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background: #ffffff;
  color: #333;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: #f5f5f5;
  border-color: #4CAF50;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 0.9rem;
  color: #666;
}

/* Toast notifications */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1001;
  display: flex;
  align-items: center;
  gap: 1rem;
  max-width: 400px;
  animation: slideIn 0.3s ease;
}

.toast.success {
  background: #4CAF50;
  color: white;
}

.toast.error {
  background: #F44336;
  color: white;
}

.toast.info {
  background: #2196F3;
  color: white;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.toast-close {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@media (max-width: 1200px) {
  .notifications-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-selects {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .notification-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .notification-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .pagination {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .toast {
    left: 20px;
    right: 20px;
    max-width: none;
  }
}

.filters-right {
  display: flex;
  gap: 1rem;
}

.visor-stats-compact {
  display: flex;
  gap: 1rem;
}

.compact-stat-card {
  background: linear-gradient(to bottom, #ffffff, #f9f9f9);
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 160px;
}

.compact-stat-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #f5f5f5, #ffffff);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.compact-stat-info {
  display: flex;
  flex-direction: column;
}

.compact-stat-value {
  font-weight: 700;
  font-size: 1.2rem;
  color: #2E7D32;
}

.compact-stat-label {
  font-size: 0.75rem;
  color: #666;
}

.notificaciones-section {
  flex: 1;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.loading-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.spinner-large {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(76, 175, 80, 0.2);
  border-radius: 50%;
  border-top-color: #4CAF50;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.empty-icon {
  margin-bottom: 1.5rem;
  opacity: 0.8;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 0.5rem;
}

.empty-state p {
  color: #666;
  margin: 0 0 2rem;
  max-width: 400px;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(to bottom, #4CAF50, #43A047);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
  transition: all 0.2s ease;
}

.create-btn:hover {
  background: linear-gradient(to bottom, #43A047, #388E3C);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.create-btn:active {
  transform: translateY(-1px);
}

/* Responsive styles */
@media (max-width: 1200px) {
  .filters-main {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filters-right {
    width: 100%;
    margin-top: 1rem;
  }
  
  .visor-stats-compact {
    width: 100%;
    justify-content: space-between;
  }
  
  .compact-stat-card {
    min-width: 0;
    flex: 1;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 60px; /* Ajustar para sidebar colapsado */
  }
  
  .page-header {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .header-icon {
    width: 40px;
    height: 40px;
  }
  
  .header-icon svg {
    width: 20px;
    height: 20px;
  }
  
  .header-title {
    font-size: 1.5rem;
  }
  
  .page-content {
    padding: 1rem;
  }
  
  .advanced-filters {
    padding: 1rem;
  }
  
  .filters-left {
    width: 100%;
  }
  
  .search-box {
    width: 100%;
  }
  
  .visor-stats-compact {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .compact-stat-card {
    padding: 0.5rem;
    min-width: calc(50% - 0.5rem);
  }
  
  .notificaciones-section {
    padding: 1rem;
  }
  
  .empty-state {
    padding: 2rem 1rem;
  }
}

@media (max-width: 480px) {
  .compact-stat-card {
    min-width: 100%;
    margin-bottom: 0.5rem;
  }
  
  .header-main {
    width: 100%;
  }
  
  .header-title {
    font-size: 1.3rem;
  }
  
  .header-subtitle {
    font-size: 0.8rem;
  }
  
  .create-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
