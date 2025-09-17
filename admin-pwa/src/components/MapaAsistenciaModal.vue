<template>
  <!-- Modal del mapa de asistencia -->
  <div v-if="visible" class="modal-overlay" @click="cerrarModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <div class="header-info">
          <h3 class="modal-title">Ubicación de {{ tipo }}</h3>
          <div v-if="asistencia" class="user-info">
            <span class="user-name">{{ asistencia.nombre_usuario }}</span>
            <span class="date-info">{{ formatearFecha(asistencia.fecha) }}</span>
          </div>
        </div>
        <button @click="cerrarModal" class="modal-close">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      
      <div class="modal-body">
        <div ref="mapContainer" class="map-container"></div>
      </div>
    </div>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  name: 'MapaAsistenciaModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    asistencia: {
      type: Object,
      default: null
    },
    tipo: {
      type: String,
      default: 'asistencia' // 'entrada', 'salida', 'asistencia'
    }
  },
  data() {
    return {
      map: null,
      markers: []
    }
  },
  watch: {
    visible(newVal) {
      if (newVal && this.asistencia) {
        this.$nextTick(() => {
          this.inicializarMapa()
        })
      } else if (!newVal && this.map) {
        this.destruirMapa()
      }
    }
  },
  beforeUnmount() {
    this.destruirMapa()
  },
  methods: {
    inicializarMapa() {
      if (this.map) {
        this.destruirMapa()
      }

      // Configurar íconos personalizados para Leaflet
      delete L.Icon.Default.prototype._getIconUrl
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'data:image/svg+xml;base64,' + btoa(this.getMarkerIcon('green')),
        iconUrl: 'data:image/svg+xml;base64,' + btoa(this.getMarkerIcon('green')),
        shadowUrl: '',
      })

      // Crear el mapa
      this.map = L.map(this.$refs.mapContainer, {
        zoomControl: true,
        attributionControl: true
      }).setView([0, 0], 13)

      // Agregar capa de mapa
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
      }).addTo(this.map)

      this.agregarMarcadores()
    },

    agregarMarcadores() {
      if (!this.asistencia) return

      const marcadores = []
      const coordenadas = []

      // Agregar marcador de entrada si existe
      if (this.asistencia.latitud_entrada && this.asistencia.longitud_entrada) {
        const latEntrada = parseFloat(this.asistencia.latitud_entrada)
        const lngEntrada = parseFloat(this.asistencia.longitud_entrada)
        
        if (!isNaN(latEntrada) && !isNaN(lngEntrada)) {
          const iconoEntrada = L.divIcon({
            className: 'custom-marker entrada-marker',
            html: this.getMarkerHtml('entrada'),
            iconSize: [40, 40],
            iconAnchor: [20, 40],
            popupAnchor: [0, -40]
          })

          const marcadorEntrada = L.marker([latEntrada, lngEntrada], { 
            icon: iconoEntrada 
          }).addTo(this.map)

          const horaEntrada = this.asistencia.hora_entrada ? this.formatearHora(this.asistencia.hora_entrada) : 'No registrada'
          const popupContentEntrada = `
            <div class="popup-content entrada">
              <div class="popup-header">
                <div class="popup-icon entrada-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 11l3 3L22 4"/>
                    <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9c1.67 0 3.22.46 4.56 1.26"/>
                  </svg>
                </div>
                <h4>Entrada</h4>
              </div>
              <div class="popup-body">
                <p><strong>Hora:</strong> ${horaEntrada}</p>
                <p><strong>Usuario:</strong> ${this.asistencia.nombre_usuario}</p>
                ${this.asistencia.descripcion_entrada ? `<p><strong>Observación:</strong> ${this.asistencia.descripcion_entrada}</p>` : ''}
              </div>
            </div>
          `
          
          marcadorEntrada.bindPopup(popupContentEntrada, {
            maxWidth: 300,
            className: 'custom-popup'
          })

          marcadores.push(marcadorEntrada)
          coordenadas.push([latEntrada, lngEntrada])
        }
      }

      // Agregar marcador de salida si existe
      if (this.asistencia.latitud_salida && this.asistencia.longitud_salida) {
        const latSalida = parseFloat(this.asistencia.latitud_salida)
        const lngSalida = parseFloat(this.asistencia.longitud_salida)
        
        if (!isNaN(latSalida) && !isNaN(lngSalida)) {
          const iconoSalida = L.divIcon({
            className: 'custom-marker salida-marker',
            html: this.getMarkerHtml('salida'),
            iconSize: [40, 40],
            iconAnchor: [20, 40],
            popupAnchor: [0, -40]
          })

          const marcadorSalida = L.marker([latSalida, lngSalida], { 
            icon: iconoSalida 
          }).addTo(this.map)

          const horaSalida = this.asistencia.hora_salida ? this.formatearHora(this.asistencia.hora_salida) : 'No registrada'
          const popupContentSalida = `
            <div class="popup-content salida">
              <div class="popup-header">
                <div class="popup-icon salida-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                    <polyline points="16,17 21,12 16,7"/>
                    <line x1="21" y1="12" x2="9" y2="12"/>
                  </svg>
                </div>
                <h4>Salida</h4>
              </div>
              <div class="popup-body">
                <p><strong>Hora:</strong> ${horaSalida}</p>
                <p><strong>Usuario:</strong> ${this.asistencia.nombre_usuario}</p>
                ${this.asistencia.descripcion_salida ? `<p><strong>Observación:</strong> ${this.asistencia.descripcion_salida}</p>` : ''}
              </div>
            </div>
          `
          
          marcadorSalida.bindPopup(popupContentSalida, {
            maxWidth: 300,
            className: 'custom-popup'
          })

          marcadores.push(marcadorSalida)
          coordenadas.push([latSalida, lngSalida])
        }
      }

      this.markers = marcadores

      // Ajustar la vista del mapa
      if (coordenadas.length > 1) {
        // Si hay múltiples puntos, ajustar para mostrar todos
        const group = new L.featureGroup(marcadores)
        this.map.fitBounds(group.getBounds().pad(0.1))
      } else if (coordenadas.length === 1) {
        // Si hay un solo punto, centrarlo
        this.map.setView(coordenadas[0], 16)
      }

      // Abrir popup automáticamente basado en el tipo
      setTimeout(() => {
        if (this.tipo === 'entrada' && marcadores[0]) {
          marcadores[0].openPopup()
        } else if (this.tipo === 'salida' && marcadores.length > 1) {
          marcadores[1].openPopup()
        } else if (this.tipo === 'salida' && marcadores.length === 1 && this.asistencia.latitud_salida) {
          marcadores[0].openPopup()
        }
      }, 500)
    },

    getMarkerHtml(tipo) {
      const color = tipo === 'entrada' ? '#4CAF50' : '#f44336'
      const icon = tipo === 'entrada' 
        ? `<path d="M9 11l3 3L22 4"/><path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9c1.67 0 3.22.46 4.56 1.26"/>`
        : `<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16,17 21,12 16,7"/><line x1="21" y1="12" x2="9" y2="12"/>`

      return `
        <div class="marker-container ${tipo}">
          <div class="marker-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              ${icon}
            </svg>
          </div>
          <div class="marker-pulse"></div>
        </div>
      `
    },

    getMarkerIcon(color) {
      return `<svg width="24" height="24" viewBox="0 0 24 24" fill="${color}" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
        <circle cx="12" cy="9" r="2.5" fill="white"/>
      </svg>`
    },

    destruirMapa() {
      if (this.map) {
        this.map.remove()
        this.map = null
        this.markers = []
      }
    },

    cerrarModal() {
      this.$emit('cerrar')
    },

    formatearFecha(fecha) {
      if (!fecha) return ''
      const date = new Date(fecha)
      return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },

    formatearHora(hora) {
      if (!hora) return 'No registrada'
      
      try {
        // Si la hora ya viene como string completo (ej: "2023-12-25T14:30:00")
        if (hora.includes('T')) {
          const date = new Date(hora)
          if (!isNaN(date.getTime())) {
            return date.toLocaleTimeString('es-ES', {
              hour: 'numeric',
              minute: '2-digit',
              hour12: true
            })
          }
        }
        
        // Si la hora viene solo como tiempo (ej: "14:30:00" o "14:30")
        const timePattern = /^(\d{1,2}):(\d{2})(?::(\d{2}))?$/
        const match = hora.match(timePattern)
        
        if (match) {
          const [, hours, minutes] = match
          const date = new Date()
          date.setHours(parseInt(hours), parseInt(minutes), 0, 0)
          
          return date.toLocaleTimeString('es-ES', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
          })
        }
        
        // Intentar crear una fecha con el formato original
        const date = new Date(`1970-01-01T${hora}`)
        if (!isNaN(date.getTime())) {
          return date.toLocaleTimeString('es-ES', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
          })
        }
        
        // Si todo falla, devolver la hora tal como viene
        return hora
      } catch (error) {
        console.warn('Error al formatear hora:', hora, error)
        return hora || 'No registrada'
      }
    }
  }
}
</script>

<style scoped>
/* Modal overlay y animaciones */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: white;
  border-radius: 20px;
  max-width: 90vw;
  max-height: 90vh;
  width: 800px;
  height: 600px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
  animation: slideUp 0.3s ease;
  display: flex;
  flex-direction: column;
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(50px) scale(0.95);
  }
  to { 
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Header del modal */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  position: relative;
  z-index: 10;
}

.header-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.modal-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  background: linear-gradient(135deg, #4CAF50, #2196F3);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.user-name {
  font-weight: 600;
  color: #374151;
  font-size: 1rem;
}

.date-info {
  font-size: 0.875rem;
  color: #6b7280;
}

.modal-close {
  background: #f3f4f6;
  border: none;
  border-radius: 12px;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #6b7280;
  position: sticky;
  top: 1.5rem;
  right: 0;
  z-index: 20;
}

.modal-close:hover {
  background: #e5e7eb;
  color: #374151;
  transform: scale(1.05);
}

/* Cuerpo del modal */
.modal-body {
  flex: 1;
  padding: 0;
  position: relative;
}

.map-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
}

/* Responsive */
@media (max-width: 768px) {
  .modal-content {
    width: 95vw;
    height: 80vh;
    max-height: 80vh;
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .modal-title {
    font-size: 1.25rem;
  }
  
  .map-container {
    min-height: 300px;
  }
}

@media (max-width: 480px) {
  .modal-content {
    width: 98vw;
    height: 85vh;
    border-radius: 16px;
  }
  
  .header-info {
    gap: 0.25rem;
  }
  
  .user-name {
    font-size: 0.875rem;
  }
  
  .date-info {
    font-size: 0.75rem;
  }
}
</style>

<style>
/* Estilos globales para los marcadores y popups de Leaflet */
.custom-marker {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

.marker-container {
  position: relative;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: markerAppear 0.6s ease-out;
}

@keyframes markerAppear {
  0% {
    opacity: 0;
    transform: scale(0.3) translateY(-20px);
  }
  60% {
    opacity: 1;
    transform: scale(1.1) translateY(0);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.marker-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  position: relative;
  z-index: 2;
  animation: gentleGlow 3s ease-in-out infinite;
  transition: all 0.3s ease;
}

.marker-container.entrada .marker-icon {
  background: linear-gradient(135deg, #1e90ff, #1976d2);
  border: 2px solid rgba(30, 144, 255, 0.3);
}

.marker-container.entrada:hover .marker-icon {
  background: linear-gradient(135deg, #1976d2, #1565c0);
  border-color: rgba(30, 144, 255, 0.5);
  transform: scale(1.1);
}

.marker-container.salida .marker-icon {
  background: linear-gradient(135deg, #dc143c, #b71c1c);
  border: 2px solid rgba(220, 20, 60, 0.3);
}

.marker-container.salida:hover .marker-icon {
  background: linear-gradient(135deg, #b71c1c, #c62828);
  border-color: rgba(220, 20, 60, 0.5);
  transform: scale(1.1);
}

.marker-icon svg {
  width: 20px;
  height: 20px;
}

.marker-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  opacity: 0.7;
  animation: pulse 2.5s ease-out infinite;
}

.marker-container.entrada .marker-pulse {
  background: rgba(30, 144, 255, 0.6);
  animation: pulse 2.5s ease-out infinite;
}

.marker-container.salida .marker-pulse {
  background: rgba(220, 20, 60, 0.6);
  animation: pulse 2.5s ease-out infinite 0.3s;
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.7;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.3);
    opacity: 0.4;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.6);
    opacity: 0;
  }
}

@keyframes gentleGlow {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
  }
}

/* Estilos para los popups */
.leaflet-popup-content-wrapper {
  border-radius: 12px !important;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important;
  border: none !important;
}

.leaflet-popup-content {
  margin: 0 !important;
  padding: 0 !important;
}

.popup-content {
  padding: 1rem;
  min-width: 200px;
}

.popup-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
}

.popup-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.popup-icon.entrada-icon {
  background: linear-gradient(135deg, #1e90ff, #1976d2);
}

.popup-icon.salida-icon {
  background: linear-gradient(135deg, #dc143c, #b71c1c);
}

.popup-icon svg {
  width: 16px;
  height: 16px;
  color: white;
}

.popup-header h4 {
  margin: 0;
  color: #1f2937;
  font-weight: 600;
  font-size: 1rem;
}

.popup-body p {
  margin: 0.5rem 0;
  font-size: 0.875rem;
  color: #374151;
}

.popup-body p:first-child {
  margin-top: 0;
}

.popup-body p:last-child {
  margin-bottom: 0;
}

.popup-body strong {
  color: #1f2937;
  font-weight: 600;
}

.leaflet-popup-tip {
  background: white !important;
  border: none !important;
  box-shadow: 0 3px 14px rgba(0, 0, 0, 0.15) !important;
}

/* Ajustes para el control de zoom */
.leaflet-control-zoom {
  border: none !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

.leaflet-control-zoom a {
  border-radius: 0 !important;
  border: none !important;
  background: white !important;
  color: #374151 !important;
  font-weight: 600 !important;
  transition: all 0.2s ease !important;
}

.leaflet-control-zoom a:hover {
  background: #f3f4f6 !important;
  color: #1f2937 !important;
}

.leaflet-control-zoom-in {
  border-top-left-radius: 12px !important;
  border-top-right-radius: 12px !important;
}

.leaflet-control-zoom-out {
  border-bottom-left-radius: 12px !important;
  border-bottom-right-radius: 12px !important;
}

/* Ajustes para la atribución */
.leaflet-control-attribution {
  background: rgba(255, 255, 255, 0.8) !important;
  border-radius: 8px !important;
  font-size: 0.75rem !important;
}
</style>
