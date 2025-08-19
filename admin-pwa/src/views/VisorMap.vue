<template>
  <div class="visor-map-container">
    <!-- Importar fuentes modernas -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Mapa Optimizado</h1>
              <p class="header-subtitle">Visualización de ubicaciones de forma eficiente</p>
            </div>
          </div>
          <div class="header-actions">
            <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
              <div class="status-indicator"></div>
              <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
            </div>
            
            <!-- Contador de puntos en el mapa con efecto de cristal líquido -->
            <div class="lcd-counter">
              <div class="lcd-display">
                <div class="lcd-label">PUNTOS EN MAPA</div>
                <div class="lcd-number">{{ totalPuntosEnMapa.toLocaleString() }}</div>
              </div>
            </div>
            
            <button @click="recargarMapa" class="refresh-btn-icon" :disabled="loading" title="Actualizar manualmente">
              <svg class="refresh-icon" :class="{ spinning: loading }" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10"></polyline>
                <polyline points="1 20 1 14 7 14"></polyline>
                <path d="m3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
              </svg>
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Panel de control lateral para el mapa -->
        <div class="controles-panel">
          <div class="panel-header">
            <h3>Controles del Mapa</h3>
            <button @click="recargarMapa" class="btn-refresh" :disabled="loading">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 2v6h-6"></path>
                <path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
                <path d="M3 22v-6h6"></path>
                <path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
              </svg>
              <span>Actualizar datos</span>
            </button>
          </div>
          
          <div class="panel-section">
            <h4>Estado</h4>
            <div v-if="error" class="error-message">
              <p>{{ error }}</p>
              <button @click="recargarMapa" class="retry-btn-small">Reintentar</button>
            </div>
            <div v-else class="status-message">
              <div class="status-badge" :class="loading ? 'loading' : 'success'">
                {{ loading ? 'Cargando...' : 'Mapa listo' }}
              </div>
              <p class="status-info">{{ totalPuntosEnMapa }} ubicaciones en el mapa</p>
            </div>
          </div>
          
          <div class="panel-section">
            <h4>Estadísticas</h4>
            <div class="stat-grid">
              <div class="stat-item">
                <span class="stat-label">Total</span>
                <span class="stat-value">{{ totalPuntosEnMapa }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Entradas</span>
                <span class="stat-value entrada">{{ clusterInfo.entradas }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Salidas</span>
                <span class="stat-value salida">{{ clusterInfo.salidas }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Hoy</span>
                <span class="stat-value hoy">{{ clusterInfo.registrosHoy }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Antiguos</span>
                <span class="stat-value antiguo">{{ clusterInfo.registrosAntiguos }}</span>
              </div>
            </div>
          </div>
          
          <div class="panel-section">
            <h4>Leyenda</h4>
            <div class="leyenda-grid">
              <div class="leyenda-item">
                <div class="color-marker entrada"></div>
                <span>Entrada</span>
              </div>
              <div class="leyenda-item">
                <div class="color-marker salida"></div>
                <span>Salida</span>
              </div>
              <div class="leyenda-item">
                <div class="color-marker registro-hoy"></div>
                <span>Registro hoy</span>
              </div>
              <div class="leyenda-item">
                <div class="color-marker registro-antiguo"></div>
                <span>Registro antiguo</span>
              </div>
            </div>
          </div>
          
          <div class="panel-section">
            <h4>Ayuda</h4>
            <div class="help-text">
              <p>• Haz clic en los grupos para expandir</p>
              <p>• Haz clic en los puntos para ver detalles</p>
              <p>• Usa los controles de zoom para acercar/alejar</p>
            </div>
          </div>
        </div>
        
        <!-- Contenedor del mapa con Mapbox -->
        <div class="mapa-container">
          <div v-if="loading" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando mapa optimizado...</p>
          </div>
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarDatos" class="retry-btn">Reintentar</button>
          </div>
          <div id="mapa-principal" class="mapa-area"></div>
          
          <!-- Popup personalizado -->
          <div v-show="showCustomPopup" 
               class="custom-popup" 
               :class="'popup-' + popupData.tipoClase" 
               :style="{ top: popupY + 'px', left: popupX + 'px' }">
            <div class="popup-header">
              <div class="popup-title">
                <!-- Iconos según el tipo de actividad -->
                <svg v-if="popupData.tipoClase === 'entrada'" class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
                  <polyline points="10 17 15 12 10 7"/>
                  <line x1="15" y1="12" x2="3" y2="12"/>
                </svg>
                <svg v-else-if="popupData.tipoClase === 'salida'" class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16 17 21 12 16 7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                <svg v-else-if="popupData.tipoClase === 'registro-hoy'" class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
                <svg v-else class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="8" x2="12" y2="12"/>
                  <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                <strong>{{ popupData.tipoActividad }}</strong>
              </div>
              
              <div class="popup-header-right">
                <span class="popup-fecha">{{ popupData.fecha }}</span>
                <button class="popup-close-btn" @click="cerrarPopup" title="Cerrar">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
            </div>
            <div class="popup-body">
              <div class="popup-row">
                <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                <div class="popup-usuario">{{ popupData.usuario }}</div>
              </div>
              <div class="popup-row">
                <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                <div class="popup-coordenadas">{{ popupData.coordenadasTexto }}</div>
              </div>
            </div>
            <div class="popup-footer">
              <button class="popup-btn" @click="verDetallesRegistro">
                <svg class="popup-btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"/>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                  <line x1="11" y1="8" x2="11" y2="14"/>
                  <line x1="8" y1="11" x2="14" y2="11"/>
                </svg>
                Ver detalles
              </button>
            </div>
            <!-- Flecha indicadora que apunta al punto en el mapa -->
            <div class="popup-arrow"></div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import axios from 'axios'
import mapboxgl from 'mapbox-gl'
import { usuariosService } from '../services/usuariosService.js'
import asistenciasService from '../services/asistenciasService.js'
import { estadisticasService } from '../services/estadisticasService.js'

// Token de acceso de Mapbox - En producción debe estar en variables de entorno
mapboxgl.accessToken = 'pk.eyJ1IjoibWFyaWVsMDgiLCJhIjoiY202emV3MDhhMDN6YjJscHVqaXExdGpjMyJ9.F_ACoKzS_4e280lD0XndEw';

const router = useRouter()
const API_URL = 'https://apipwa.sembrandodatos.com'

// Estado de conexión
const isOnline = ref(navigator.onLine)

// Estado del componente
const loading = ref(true)
const error = ref('')
const totalPuntosEnMapa = ref(0)

// Referencias al mapa y capas
let map = null
let puntosSource = null
let hasDatosUsuario = ref(false)

// Estado del popup personalizado
const showCustomPopup = ref(false)
const popupX = ref(0)
const popupY = ref(0)
const popupData = ref({
  coordinates: [],
  usuario: '',
  fecha: '',
  tipoActividad: '',
  tipoClase: '',
  coordenadasTexto: ''
})

// Registros y filtrado
const registros = ref([])
const asistencias = ref([])
const usuarios = ref([])

// Estado de los clusters y horario CDMX
const clusterInfo = reactive({
  total: 0,
  entradas: 0,
  salidas: 0,
  registrosHoy: 0,
  registrosAntiguos: 0
})

// Función para obtener la fecha actual en CDMX (tiempo real)
const obtenerFechaCDMX = () => {
  // Horario de Ciudad de México: UTC-6 (normal) o UTC-5 (horario de verano)
  // Para simplificar, usamos -6 como zona horaria fija para CDMX
  const fechaUTC = new Date();
  const offsetCDMX = -6 * 60; // -6 horas en minutos
  const utcOffset = fechaUTC.getTimezoneOffset(); // Offset local en minutos
  const totalOffset = offsetCDMX + utcOffset; // Diferencia entre local y CDMX
  
  const fechaCDMX = new Date(fechaUTC.getTime() + totalOffset * 60000);
  return fechaCDMX;
}

// Función para cargar datos
const cargarDatos = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const token = localStorage.getItem('admin_token')
    
    // Cargar registros, asistencias y usuarios en paralelo
    const [responseRegistros, asistenciasData, usuariosData] = await Promise.all([
      axios.get(`${API_URL}/registros`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }),
      asistenciasService.obtenerAsistenciasConUsuarios(),
      usuariosService.obtenerUsuarios()
    ])
    
    // La respuesta puede ser directamente un array o tener una propiedad específica
    const registrosRaw = Array.isArray(responseRegistros.data) ? responseRegistros.data : (responseRegistros.data.registros || [])
    
    // Enriquecer registros con información de usuarios
    const registrosEnriquecidos = await usuariosService.enriquecerRegistrosConUsuarios(registrosRaw)
    
    // Guardar datos
    registros.value = registrosEnriquecidos
    asistencias.value = asistenciasData
    usuarios.value = usuariosData
    
    // Calcular las últimas actividades por usuario
    const ultimasActividades = obtenerUltimasActividadesPorUsuario(registrosEnriquecidos, asistenciasData)
    
    // Si el mapa ya está cargado, actualizar puntos
    if (map) {
      actualizarPuntosMapa(ultimasActividades)
    } else {
      inicializarMapa(ultimasActividades)
    }
    
    hasDatosUsuario.value = true
    loading.value = false
    totalPuntosEnMapa.value = ultimasActividades.length
    
  } catch (err) {
    console.error('Error al cargar datos:', err)
    if (err.response?.status === 401) {
      logout()
    } else {
      error.value = 'Error al cargar los datos: ' + (err.response?.data?.detail || err.message)
      loading.value = false
    }
  }
}

// Obtener las últimas actividades por usuario (combinando registros y asistencias)
const obtenerUltimasActividadesPorUsuario = (registros, asistencias) => {
  const mapaUsuarios = new Map()
  
  // Procesar registros normales
  registros.forEach(registro => {
    if (!registro.latitud || !registro.longitud) return
    
    const usuarioId = registro.usuario_id
    const fechaHora = new Date(registro.fecha_hora)
    
    const actividad = {
      ...registro,
      tipo_actividad: 'registro',
      fecha_actividad: fechaHora,
      latitud: parseFloat(registro.latitud),
      longitud: parseFloat(registro.longitud)
    }
    
    if (!mapaUsuarios.has(usuarioId) || 
        fechaHora > mapaUsuarios.get(usuarioId).fecha_actividad) {
      mapaUsuarios.set(usuarioId, actividad)
    }
  })
  
  // Procesar asistencias (entrada y salida)
  asistencias.forEach(asistencia => {
    const usuarioId = asistencia.usuario_id
    
    // Procesar entrada si existe
    if (asistencia.hora_entrada && asistencia.latitud_entrada && asistencia.longitud_entrada) {
      const fechaEntrada = new Date(asistencia.hora_entrada)
      
      const actividadEntrada = {
        id: `entrada_${asistencia.id}`,
        usuario_id: usuarioId,
        usuario: {
          nombre_completo: asistencia.nombre_usuario,
          correo: asistencia.correo_usuario,
          cargo: asistencia.cargo_usuario
        },
        tipo_actividad: 'entrada',
        fecha_actividad: fechaEntrada,
        fecha_hora: asistencia.hora_entrada,
        latitud: parseFloat(asistencia.latitud_entrada),
        longitud: parseFloat(asistencia.longitud_entrada),
        foto_url: asistencia.foto_entrada_url,
        descripcion: asistencia.descripcion_entrada || 'Entrada registrada'
      }
      
      if (!mapaUsuarios.has(usuarioId) || 
          fechaEntrada > mapaUsuarios.get(usuarioId).fecha_actividad) {
        mapaUsuarios.set(usuarioId, actividadEntrada)
      }
    }
    
    // Procesar salida si existe
    if (asistencia.hora_salida && asistencia.latitud_salida && asistencia.longitud_salida) {
      const fechaSalida = new Date(asistencia.hora_salida)
      
      const actividadSalida = {
        id: `salida_${asistencia.id}`,
        usuario_id: usuarioId,
        usuario: {
          nombre_completo: asistencia.nombre_usuario,
          correo: asistencia.correo_usuario,
          cargo: asistencia.cargo_usuario
        },
        tipo_actividad: 'salida',
        fecha_actividad: fechaSalida,
        fecha_hora: asistencia.hora_salida,
        latitud: parseFloat(asistencia.latitud_salida),
        longitud: parseFloat(asistencia.longitud_salida),
        foto_url: asistencia.foto_salida_url,
        descripcion: asistencia.descripcion_salida || 'Salida registrada'
      }
      
      if (!mapaUsuarios.has(usuarioId) || 
          fechaSalida > mapaUsuarios.get(usuarioId).fecha_actividad) {
        mapaUsuarios.set(usuarioId, actividadSalida)
      }
    }
  })
  
  // Convertir el mapa de vuelta a un array
  return Array.from(mapaUsuarios.values()).filter(a => {
    // Verificar que las coordenadas sean válidas
    return !isNaN(a.latitud) && !isNaN(a.longitud) && 
           Math.abs(a.latitud) <= 90 && Math.abs(a.longitud) <= 180
  })
}

// Determinar el tipo de actividad para colores en el mapa usando horario CDMX
const determinarTipoActividad = (actividad) => {
  // Verificar si la actividad ocurrió hoy en horario CDMX
  const esActividadDeHoy = esUbicacionReciente(actividad.fecha_hora);
  
  // CASO 1: Si la actividad es de tipo entrada
  if (actividad.tipo_actividad === 'entrada') {
    // Si la entrada es de hoy (CDMX): Verde
    if (esActividadDeHoy) {
      return {
        tipo: 'entrada',
        clase: 'entrada',
        descripcion: 'Entrada de Hoy',
        color: '#32CD32' // Verde lima
      };
    } 
    // Si la entrada NO es de hoy (CDMX): Naranja (antigua)
    else {
      return {
        tipo: 'registro-antiguo',
        clase: 'antiguo',
        descripcion: 'Entrada Anterior',
        color: '#FF9800' // Naranja
      };
    }
  }
  
  // CASO 2: Si la actividad es de tipo salida
  else if (actividad.tipo_actividad === 'salida') {
    // Si la salida es de hoy (CDMX): Rojo
    if (esActividadDeHoy) {
      return {
        tipo: 'salida',
        clase: 'salida',
        descripcion: 'Salida de Hoy',
        color: '#DC2626' // Rojo
      };
    }
    // Si la salida NO es de hoy (CDMX): Naranja (antigua)
    else {
      return {
        tipo: 'registro-antiguo',
        clase: 'antiguo',
        descripcion: 'Salida Anterior',
        color: '#FF9800' // Naranja
      };
    }
  }
  
  // CASO 3: Si es un registro normal (ni entrada ni salida)
  else {
    // Si el registro es de hoy (CDMX): Azul
    if (esActividadDeHoy) {
      return {
        tipo: 'registro-hoy',
        clase: 'registro-hoy',
        descripcion: 'Registro de Hoy',
        color: '#1E3A8A' // Azul marino
      };
    }
    // Si el registro NO es de hoy (CDMX): Naranja (antiguo)
    else {
      return {
        tipo: 'registro-antiguo',
        clase: 'antiguo',
        descripcion: 'Registro Anterior',
        color: '#FF9800' // Naranja
      };
    }
  }
}

// Función para inicializar el mapa con Mapbox
const inicializarMapa = (datos) => {
  loading.value = true
  error.value = ''
  
  try {
    // Verificar que el token esté disponible
    if (!mapboxgl.accessToken) {
      console.error('No se ha proporcionado un token de Mapbox');
      error.value = 'Error: No se ha proporcionado un token de Mapbox';
      loading.value = false;
      return;
    }
    
    console.log('Inicializando mapa con token:', mapboxgl.accessToken.substring(0, 10) + '...');
    
    // Verificar validez del token (formato básico)
    if (!mapboxgl.accessToken.startsWith('pk.')) {
      console.error('El token de Mapbox no parece tener el formato correcto');
      error.value = 'Error: El token de Mapbox no tiene el formato correcto';
      loading.value = false;
      return;
    }
    
    // Verificar que el elemento del mapa exista
    const mapElement = document.getElementById('mapa-principal');
    if (!mapElement) {
      console.error('No se encuentra el elemento del mapa con ID "mapa-principal"');
      error.value = 'Error: No se encuentra el contenedor del mapa';
      loading.value = false;
      return;
    }
    
    console.log('Iniciando creación del mapa con token:', mapboxgl.accessToken);
    
    // Crear nuevo mapa de Mapbox con el estilo original
    map = new mapboxgl.Map({
      container: 'mapa-principal',
      style: 'mapbox://styles/mapbox/streets-v11', // Volvemos al estilo original con más detalle
      center: [-99.1332, 19.4326], // Centro inicial en Ciudad de México
      zoom: 5, // Zoom inicial más cercano
      maxZoom: 18,
      pitchWithRotate: false, // Limitar inclinación para mejor rendimiento
      attributionControl: false,
      cooperativeGestures: false, // Desactivamos para permitir scroll normal con el mouse
      scrollZoom: true, // Habilitamos zoom con rueda del mouse
      dragRotate: false, // Desactivamos rotación con arrastre para una experiencia más intuitiva
      fadeDuration: 300   // Transiciones suaves
    });
    
    // Añadir controles de navegación mejorados con zoom visible
    map.addControl(new mapboxgl.NavigationControl({
      showCompass: true, // Mostramos la brújula para orientación
      visualizePitch: false, // No mostrar el control de inclinación para simplificar
      showZoom: true // Asegurarnos que los botones de zoom sean visibles
    }), 'top-right'); // Movemos a la esquina superior derecha para mejor visibilidad
    
    // Añadir mensaje sobre el uso de la rueda del mouse
    const zoomHelpElement = document.createElement('div');
    zoomHelpElement.className = 'mapbox-zoom-help';
    zoomHelpElement.innerHTML = `
      <div class="zoom-help-tooltip">
        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M12 16v-4"></path>
          <path d="M12 8h.01"></path>
        </svg>
        <span>Use la rueda del ratón para acercar/alejar</span>
      </div>
    `;
    map.getContainer().appendChild(zoomHelpElement);
    
    // Añadir control de atribución en posición menos intrusiva
    map.addControl(new mapboxgl.AttributionControl({
      compact: true
    }), 'bottom-left');
    
    // Añadir control de escala
    map.addControl(new mapboxgl.ScaleControl({
      maxWidth: 100,
      unit: 'metric'
    }), 'bottom-left');
    
    // Añadir atajos de teclado para zoom
    map.getCanvas().tabIndex = 0; // Hacer que el canvas sea enfocable para eventos de teclado
    map.getCanvas().addEventListener('keydown', (e) => {
      if (e.key === '+' || e.key === '=') {
        map.zoomIn(); // Zoom in con tecla +
      } else if (e.key === '-') {
        map.zoomOut(); // Zoom out con tecla -
      }
    });
    
    // Configurar el comportamiento de zoom con la rueda del ratón para hacerlo más suave
    map.scrollZoom.setWheelZoomRate(1/450); // Velocidad de zoom más suave
    map.scrollZoom.setZoomRate(0.75); // Ajustar la intensidad del zoom
    
    // Esperar a que el mapa se cargue
    map.on('load', () => {
      // Añadir fuente de datos para puntos individuales (sin clustering)
      map.addSource('puntos', {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: []
        },
        cluster: false
      });
      
      // Modificar fuente de datos para deshabilitar clústeres completamente
      map.addSource('clusters', {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: []
        },
        cluster: false // Desactivamos el clustering para que no aparezcan círculos con números
      });
      
      // Guardar referencia a la fuente para actualizarla después
      puntosSource = map.getSource('puntos');
      
      // Eliminamos las capas de clústeres para que no aparezcan en el mapa
      
      // Añadir capa para los puntos individuales
      map.addLayer({
        id: 'unclustered-point',
        type: 'circle',
        source: 'puntos',
        filter: ['!', ['has', 'point_count']],
        paint: {
          'circle-color': [
            'match',
            ['get', 'tipo_actividad'],
            'entrada', '#32CD32', // Verde para entradas
            'salida', '#DC2626', // Rojo para salidas
            'registro-hoy', '#1E3A8A', // Azul para registros de hoy
            'registro-antiguo', '#FF9800', // Naranja para registros antiguos
            '#A9A9A9' // Gris por defecto (no debería llegar aquí)
          ],
          // Tamaño un poco más grande pero manteniendo proporción según nivel de zoom
          'circle-radius': [
            'interpolate', 
            ['linear'], 
            ['zoom'],
            // A niveles de zoom bajos, puntos más visibles
            3, 3.5,
            // A niveles de zoom medios, puntos de tamaño medio
            8, 5.5,
            // A niveles de zoom altos, puntos más grandes
            14, 7
          ],
          // Borde ligeramente más grueso para mejor definición
          'circle-stroke-width': 1.5,
          'circle-stroke-color': 'white',
          'circle-opacity': 0.9
        }
      });
      
      // Eliminamos los eventos relacionados con clústeres, ya que no los usamos más
      
      // Usaremos las variables del componente principal para el popup

      // Evento al hacer clic en un punto individual
      map.on('click', 'unclustered-point', (e) => {
        console.log('Click en punto individual', e.features[0]);
        const props = e.features[0].properties;
        const coordinates = e.features[0].geometry.coordinates.slice();
        
        // Asegurar que las coordenadas sean válidas
        if (!isNaN(coordinates[0]) && !isNaN(coordinates[1])) {
          // Obtener información del punto
          const usuario = props.nombre || `Usuario ${props.usuario_id}`;
          const fecha = new Date(props.fecha_hora).toLocaleString('es-ES');
          const tipoActividad = props.tipo_actividad === 'entrada' ? 'Entrada' : 
                               props.tipo_actividad === 'salida' ? 'Salida' : 
                               'Registro';
          
          // Convertir coordenadas geográficas a coordenadas de pantalla
          const point = map.project(coordinates);
          
          // Actualizar variables globales del popup
          popupData.value = {
            coordinates: coordinates,
            usuario: usuario,
            fecha: fecha,
            tipoActividad: tipoActividad,
            tipoClase: props.tipo_actividad,
            coordenadasTexto: `${coordinates[1].toFixed(6)}, ${coordinates[0].toFixed(6)}`
          };
          
          // Posicionar el popup justo encima del punto, con la flecha muy cerca
          popupX.value = point.x;
          popupY.value = point.y - 10; // Muy cercano al punto para que la flecha apunte directamente
          showCustomPopup.value = true;
          
          console.log('Mostrando popup en:', popupX.value, popupY.value);
          console.log('Datos del popup:', popupData.value);
          
          // Evitar que se propague el evento para no cerrar el popup inmediatamente
          e.originalEvent.stopPropagation();
        }
      });
      
      // Cerrar el popup al hacer clic en cualquier lugar del mapa
      map.on('click', (e) => {
        // Verificar si el clic fue directamente en el mapa (y no en un punto)
        const features = map.queryRenderedFeatures(e.point, { layers: ['unclustered-point'] });
        if (features.length === 0) {
          console.log('Cerrar popup - clic fuera de punto');
          showCustomPopup.value = false;
        }
      });
      
      // Cambiar cursor a puntero al pasar sobre los puntos
      map.on('mouseenter', 'unclustered-point', () => {
        map.getCanvas().style.cursor = 'pointer';
      });
      
      map.on('mouseleave', 'unclustered-point', () => {
        map.getCanvas().style.cursor = '';
      });
      
      // Actualizar la posición del popup cuando el mapa se mueve
      map.on('move', () => {
        // Si el popup está abierto y hay coordenadas, actualizar su posición
        if (showCustomPopup.value && popupData.value.coordinates && popupData.value.coordinates.length) {
          const point = map.project(popupData.value.coordinates);
          popupX.value = point.x;
          popupY.value = point.y - 10; // Mantener la misma distancia muy cercana al punto
          console.log('Actualizando posición del popup en move:', popupX.value, popupY.value);
        }
      });
      
      // Cerrar popup al hacer zoom
      map.on('zoom', () => {
        console.log('Cerrar popup - zoom');
        showCustomPopup.value = false;
      });
      
      // Actualizar puntos en el mapa
      if (datos && datos.length > 0) {
        actualizarPuntosMapa(datos);
      }
      
      loading.value = false;
    });
    
    // Manejar errores de carga del mapa
    map.on('error', (e) => {
      console.error('Error en el mapa:', e);
      const errorMsg = e.error ? 
        (e.error.message || e.error.toString()) : 
        (e.message || 'Error desconocido en la carga del mapa');
      
      console.log('Detalles del error:', errorMsg);
      error.value = 'Error al cargar el mapa: ' + errorMsg;
      
      // Intentar con estilos alternativos si el error es relacionado con el estilo
      if (errorMsg.includes('style') || errorMsg.includes('token')) {
        try {
          console.log('Intentando con estilos alternativos...');
          
          // Intentar primero con streets-v11 nuevamente (el estilo preferido)
          map.setStyle('mapbox://styles/mapbox/streets-v11');
          
          // Si aún hay problemas, establecer un temporizador para probar con estilos alternativos
          setTimeout(() => {
            if (error.value) {
              const estilosAlternativos = [
                'mapbox://styles/mapbox/outdoors-v11', 
                'mapbox://styles/mapbox/navigation-day-v1',
                'mapbox://styles/mapbox/light-v10'
              ];
              
              const estiloAleatorio = estilosAlternativos[Math.floor(Math.random() * estilosAlternativos.length)];
              console.log('Probando con estilo alternativo:', estiloAleatorio);
              map.setStyle(estiloAleatorio);
            }
          }, 2000);
          
        } catch (styleError) {
          console.error('Error al cambiar el estilo:', styleError);
        }
      }
      
      loading.value = false;
    });
    
    // Confirmar cuando el mapa está listo
    map.on('styledata', () => {
      console.log('Estilo del mapa cargado correctamente');
    });
    
  } catch (err) {
    console.error('Error al inicializar el mapa:', err);
    const errorMsg = err.message || err.toString() || 'Error desconocido';
    console.log('Detalles del error de inicialización:', errorMsg);
    error.value = 'Error al inicializar el mapa: ' + errorMsg;
    loading.value = false;
  }
}

// Función para actualizar los puntos en el mapa
const actualizarPuntosMapa = (datos) => {
  if (!map || !puntosSource) return;
  
  try {
    // Reiniciar contadores
    clusterInfo.total = 0;
    clusterInfo.entradas = 0;
    clusterInfo.salidas = 0;
    clusterInfo.registrosHoy = 0;
    clusterInfo.registrosAntiguos = 0;
    
    // Convertir datos a formato GeoJSON
    const features = datos.map(punto => {
      // Usar la función determinarTipoActividad para clasificar según horario CDMX
      const infoActividad = determinarTipoActividad(punto);
      const tipoActividad = infoActividad.tipo;
      
      // Verificar si la actividad es de hoy según el horario CDMX
      const esHoy = esUbicacionReciente(punto.fecha_hora);
      
      // Actualizar contadores para las estadísticas
      clusterInfo.total++;
      
      // Actualizar contadores basados en el tipo de actividad
      if (tipoActividad === 'entrada') {
        clusterInfo.entradas++;
      } else if (tipoActividad === 'salida') {
        clusterInfo.salidas++;
      } else if (tipoActividad === 'registro-hoy') {
        clusterInfo.registrosHoy++;
      } else if (tipoActividad === 'registro-antiguo') {
        clusterInfo.registrosAntiguos++;
      }
      
      return {
        type: 'Feature',
        properties: {
          id: punto.id,
          usuario_id: punto.usuario_id,
          nombre: punto.usuario?.nombre_completo || `Usuario ${punto.usuario_id}`,
          tipo_actividad: tipoActividad,
          fecha_hora: punto.fecha_hora,
          descripcion: punto.descripcion || ''
        },
        geometry: {
          type: 'Point',
          coordinates: [punto.longitud, punto.latitud]
        }
      };
    });
    
    // Actualizar solo la fuente de datos para puntos (sin clústeres)
    puntosSource.setData({
      type: 'FeatureCollection',
      features: features
    });
    
    totalPuntosEnMapa.value = features.length;
    
    // Ajustar mapa para mostrar todos los puntos
    if (features.length > 0) {
      // Crear límites para contener todos los puntos
      const bounds = new mapboxgl.LngLatBounds();
      features.forEach(feature => {
        bounds.extend(feature.geometry.coordinates);
      });
      
      // Ajustar vista a los límites calculados
      map.fitBounds(bounds, {
        padding: { top: 50, bottom: 50, left: 50, right: 50 },
        maxZoom: 15
      });
    }
    
  } catch (err) {
    console.error('Error al actualizar puntos en el mapa:', err);
  }
}

// Función auxiliar para determinar si una ubicación es reciente usando horario CDMX
const esUbicacionReciente = (fechaStr) => {
  try {
    // Convertir la cadena de fecha a objeto Date
    const fechaObj = new Date(fechaStr);
    
    // Obtener la fecha actual en CDMX
    const fechaCDMX = obtenerFechaCDMX();
    
    // Ajustar la fecha proporcionada al horario CDMX
    const offsetCDMX = -6 * 60; // -6 horas en minutos
    const utcOffset = fechaObj.getTimezoneOffset(); // Offset local en minutos
    const totalOffset = offsetCDMX + utcOffset; // Diferencia entre local y CDMX
    
    const fechaObjCDMX = new Date(fechaObj.getTime() + totalOffset * 60000);
    
    // Verificar si es del mismo día (hoy en CDMX)
    return (
      fechaCDMX.getFullYear() === fechaObjCDMX.getFullYear() &&
      fechaCDMX.getMonth() === fechaObjCDMX.getMonth() &&
      fechaCDMX.getDate() === fechaObjCDMX.getDate()
    );
  } catch (e) {
    console.error('Error al procesar fecha:', e);
    return false;
  }
}

// Función para manejar el clic en "Ver detalles" en el popup
const verDetallesRegistro = () => {
  // Obtiene los datos actuales del popup
  const registro = popupData.value;
  
  // Aquí puedes implementar lo que quieras hacer con los detalles del registro
  // Por ejemplo, abrir un modal con más información, navegar a una página de detalles, etc.
  console.log('Ver detalles del registro:', registro);
  
  // Por ahora, simplemente cerramos el popup
  showCustomPopup.value = false;
}

// Función para cerrar el popup cuando se hace clic en el botón X
const cerrarPopup = () => {
  console.log('Cerrando popup mediante botón X');
  showCustomPopup.value = false;
}

// Recargar mapa y datos
const recargarMapa = async () => {
  // Si hay un error grave, reiniciar completamente el mapa
  if (error.value && error.value.includes('token')) {
    // Destruir el mapa actual si existe
    if (map) {
      try {
        map.remove();
        map = null;
        puntosSource = null;
        clusterSource = null;
      } catch (e) {
        console.error('Error al destruir el mapa:', e);
      }
    }
    
    // Limpiar el error y reiniciar
    error.value = '';
    console.log('Reiniciando el mapa con token proporcionado');
    
    // Asegurar que estamos usando el token proporcionado
    mapboxgl.accessToken = 'pk.eyJ1IjoibWFyaWVsMDgiLCJhIjoiY202emV3MDhhMDN6YjJscHVqaXExdGpjMyJ9.F_ACoKzS_4e280lD0XndEw';
  }
  
  // Cargar los datos nuevamente
  await cargarDatos();
}

// Función de cierre de sesión
const logout = () => {
  localStorage.removeItem('admin_token');
  localStorage.removeItem('admin_user');
  router.push('/login');
}

// Ciclo de vida del componente
onMounted(() => {
  // Asegurar que el CSS de Mapbox esté cargado (por si falla la importación en el estilo)
  const addMapboxCSS = () => {
    if (!document.getElementById('mapbox-gl-css')) {
      const link = document.createElement('link');
      link.id = 'mapbox-gl-css';
      link.rel = 'stylesheet';
      link.href = 'https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.css';
      document.head.appendChild(link);
      console.log('CSS de Mapbox cargado dinámicamente');
    }
  };
  
  addMapboxCSS();
  
  // Cargar datos y mapa
  cargarDatos();
  
  // Escuchar cambios de conexión
  window.addEventListener('online', () => {
    isOnline.value = true;
  });
  
  window.addEventListener('offline', () => {
    isOnline.value = false;
  });
});

onUnmounted(() => {
  // Destruir el mapa para liberar recursos
  if (map) {
    map.remove();
    map = null;
  }
  
  // Limpiar listeners
  window.removeEventListener('online', () => {});
  window.removeEventListener('offline', () => {});
});
</script>

<style scoped>
/* Importación de fuentes */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

/* Estilos principales */
.visor-map-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #f0f2f5 0%, #e8f5e8 100%);
  font-family: 'Inter', 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  overflow: hidden;
}

.main-content {
  flex: 1;
  margin-left: clamp(180px, 18vw, 240px);
  width: calc(100vw - clamp(180px, 18vw, 240px));
  background: transparent;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 100vh;
  padding: 0;
  box-sizing: border-box;
  position: relative;
  z-index: 1;
}

/* Header con diseño moderno y verde */
.page-header {
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  border-bottom: none;
  padding: clamp(0.4rem, 1.2vw, 0.7rem);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  box-sizing: border-box;
  color: white;
  box-shadow: 0 4px 20px rgba(46, 204, 113, 0.15);
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
  z-index: 1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 100%;
  margin: 0;
  gap: clamp(0.3rem, 1.2vw, 0.6rem);
  flex-wrap: wrap;
  width: 100%;
  position: relative;
  z-index: 2;
}

.header-main {
  display: flex;
  align-items: center;
  gap: clamp(0.3rem, 1.2vw, 0.6rem);
  flex: 1;
  min-width: 150px;
}

.header-icon {
  width: clamp(28px, 4vw, 36px);
  height: clamp(28px, 4vw, 36px);
  background: rgba(255, 255, 255, 0.15);
  border-radius: clamp(6px, 1vw, 8px);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
  animation: float 3s ease-in-out infinite;
}

.header-icon svg {
  width: clamp(14px, 2.5vw, 18px);
  height: clamp(14px, 2.5vw, 18px);
  color: white;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-4px); }
}

.header-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.header-title {
  margin: 0;
  font-size: clamp(14px, 1.5vw, 20px);
  font-weight: 600;
  color: white;
  line-height: 1.2;
}

.header-subtitle {
  margin: 0;
  font-size: clamp(10px, 0.9vw, 14px);
  font-weight: 400;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.4;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: clamp(8px, 1vw, 16px);
}

/* Estado de conexión */
.connection-status {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.online {
  color: rgba(255, 255, 255, 0.95);
}

.offline {
  color: rgba(255, 192, 203, 0.95);
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.online .status-indicator {
  background-color: #4ade80;
  box-shadow: 0 0 8px rgba(74, 222, 128, 0.6);
}

.offline .status-indicator {
  background-color: #f87171;
  box-shadow: 0 0 8px rgba(248, 113, 113, 0.6);
}

/* Contador LCD */
.lcd-counter {
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0.4) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 6px 10px;
  box-shadow: 
    inset 0 1px 3px rgba(0, 0, 0, 0.3),
    0 1px 0 rgba(255, 255, 255, 0.1);
}

.lcd-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.lcd-label {
  font-size: 8px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.lcd-number {
  font-family: 'Digital-7', 'Courier New', monospace;
  font-size: 16px;
  font-weight: 500;
  color: #4ade80;
  letter-spacing: 0.05em;
  text-shadow: 0 0 10px rgba(74, 222, 128, 0.8);
}

/* Botón de actualización */
.refresh-btn-icon {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.refresh-btn-icon:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(15deg);
}

.refresh-icon {
  color: white;
  transition: all 0.3s ease;
}

.refresh-btn-icon:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinning {
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Contenido principal */
.page-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background: transparent;
  position: relative;
  z-index: 1;
  display: flex;
  gap: 16px;
  height: calc(100vh - 60px); /* Altura completa menos el header */
}

/* Panel de control lateral */
.controles-panel {
  width: 260px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  flex-shrink: 0;
  overflow-y: auto;
  max-height: calc(100vh - 92px);
}

.panel-header {
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding-bottom: 12px;
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.btn-refresh {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: #2ecc71;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-refresh:hover {
  background: #27ae60;
}

.btn-refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.panel-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.panel-section h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

/* Estado del mapa */
.error-message {
  background-color: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 10px;
}

.error-message p {
  color: #dc2626;
  font-size: 12px;
  margin: 0 0 8px 0;
}

.retry-btn-small {
  background-color: #dc2626;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s;
}

.retry-btn-small:hover {
  background-color: #b91c1c;
}

.status-message {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  max-width: fit-content;
}

.status-badge.loading {
  background-color: #dbeafe;
  color: #1e40af;
}

.status-badge.success {
  background-color: #dcfce7;
  color: #15803d;
}

.status-info {
  font-size: 12px;
  color: #6b7280;
  margin: 0;
}

/* Estadísticas */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.stat-item {
  background: #f9fafb;
  padding: 8px 12px;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.stat-value.entrada {
  color: #2ecc71;
}

.stat-value.salida {
  color: #e53e3e;
}

.stat-value.hoy {
  color: #1e40af;
}

.stat-value.antiguo {
  color: #f59e0b;
}

/* Leyenda del mapa */
.leyenda-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.leyenda-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.color-marker {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.color-marker.entrada {
  background-color: #32CD32;
}

.color-marker.salida {
  background-color: #DC2626;
}

.color-marker.registro-hoy {
  background-color: #1E3A8A;
}

.color-marker.registro-antiguo {
  background-color: #FF9800;
}

/* Ayuda */
.help-text {
  font-size: 12px;
  color: #6b7280;
}

.help-text p {
  margin: 4px 0;
}

/* Contenedor del mapa */
.mapa-container {
  flex: 1;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  position: relative;
  min-height: 600px;
  height: 100%;
}

.mapa-area {
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 1;
}

/* Indicadores de carga y error */
.loading-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(4px);
  z-index: 2;
}

.spinner-large {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(46, 204, 113, 0.2);
  border-radius: 50%;
  border-top-color: #2ecc71;
  animation: spin 1s linear infinite;
  margin-bottom: 12px;
}

.error-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  z-index: 2;
  padding: 20px;
  text-align: center;
}

.error-container p {
  color: #e53e3e;
  margin-bottom: 16px;
  max-width: 400px;
}

.retry-btn {
  padding: 8px 16px;
  background: #2ecc71;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: #27ae60;
  transform: translateY(-2px);
}

/* Estilos específicos para Mapbox */
@import url('https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.css');

/* Personalización de popups personalizados */
.custom-popup {
  position: absolute;
  width: 280px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  z-index: 10;
  transform: translate(-50%, -100%);
  pointer-events: auto;
  font-family: 'Inter', 'Poppins', sans-serif;
  overflow: visible; /* Permite que la flecha sea visible */
  opacity: 1;
  transition: opacity 0.2s ease-in-out;
}

/* Colores dinámicos según tipo de registro */
.custom-popup.popup-entrada {
  background-color: #f0fdf4;
  border: 1px solid rgba(50, 205, 50, 0.3);
}

.custom-popup.popup-salida {
  background-color: #fef2f2;
  border: 1px solid rgba(220, 38, 38, 0.3);
}

.custom-popup.popup-registro-hoy {
  background-color: #eff6ff;
  border: 1px solid rgba(30, 58, 138, 0.3);
}

.custom-popup.popup-registro-antiguo, 
.custom-popup.popup-antiguo {
  background-color: #fff7ed;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

/* Estilos para la flecha indicadora */
.popup-arrow {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 8px;
  overflow: hidden;
}

.popup-arrow::after {
  content: '';
  position: absolute;
  width: 12px;
  height: 12px;
  transform: translateY(-50%) rotate(45deg);
  top: 0;
  left: 2px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

/* Colores de la flecha según el tipo */
.popup-entrada .popup-arrow::after {
  background-color: #f0fdf4;
  border-right: 1px solid rgba(50, 205, 50, 0.3);
  border-bottom: 1px solid rgba(50, 205, 50, 0.3);
}

.popup-salida .popup-arrow::after {
  background-color: #fef2f2;
  border-right: 1px solid rgba(220, 38, 38, 0.3);
  border-bottom: 1px solid rgba(220, 38, 38, 0.3);
}

.popup-registro-hoy .popup-arrow::after {
  background-color: #eff6ff;
  border-right: 1px solid rgba(30, 58, 138, 0.3);
  border-bottom: 1px solid rgba(30, 58, 138, 0.3);
}

.popup-registro-antiguo .popup-arrow::after,
.popup-antiguo .popup-arrow::after {
  background-color: #fff7ed;
  border-right: 1px solid rgba(255, 152, 0, 0.3);
  border-bottom: 1px solid rgba(255, 152, 0, 0.3);
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.popup-header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.popup-title {
  display: flex;
  align-items: center;
  gap: 6px;
}

.popup-close-btn {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.05);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  padding: 0;
  transition: background-color 0.2s;
}

.popup-close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

.popup-close-btn svg {
  width: 14px;
  height: 14px;
  color: rgba(0, 0, 0, 0.5);
}

/* Estilos específicos para el botón X en cada tipo de popup */
.popup-entrada .popup-close-btn:hover svg {
  color: #22c55e;
}

.popup-salida .popup-close-btn:hover svg {
  color: #ef4444;
}

.popup-registro-hoy .popup-close-btn:hover svg {
  color: #1e40af;
}

.popup-registro-antiguo .popup-close-btn:hover svg,
.popup-antiguo .popup-close-btn:hover svg {
  color: #f59e0b;
}

.popup-icon {
  width: 18px;
  height: 18px;
}

.popup-icon-small {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* Colores de iconos y texto según tipo */
.popup-entrada .popup-icon,
.popup-entrada .popup-icon-small,
.popup-entrada strong {
  color: #22c55e;
}

.popup-salida .popup-icon,
.popup-salida .popup-icon-small,
.popup-salida strong {
  color: #ef4444;
}

.popup-registro-hoy .popup-icon,
.popup-registro-hoy .popup-icon-small,
.popup-registro-hoy strong {
  color: #1e40af;
}

.popup-registro-antiguo .popup-icon,
.popup-registro-antiguo .popup-icon-small,
.popup-antiguo .popup-icon,
.popup-antiguo .popup-icon-small,
.popup-registro-antiguo strong,
.popup-antiguo strong {
  color: #f59e0b;
}

.popup-header strong {
  font-size: 14px;
  font-weight: 600;
}

.popup-fecha {
  font-size: 11px;
  font-weight: 500;
  color: rgba(107, 114, 128, 0.8);
  background-color: rgba(0, 0, 0, 0.04);
  padding: 2px 8px;
  border-radius: 12px;
}

.popup-body {
  padding: 12px 14px;
}

.popup-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.popup-row:last-child {
  margin-bottom: 0;
}

.popup-usuario {
  font-weight: 500;
  font-size: 14px;
  color: #111827;
}

.popup-coordenadas {
  font-size: 11px;
  font-family: monospace;
  color: #6b7280;
}

.popup-footer {
  padding: 12px 14px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.popup-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background-color: rgba(0, 0, 0, 0.04);
  border: none;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: background-color 0.2s;
}

.popup-btn:hover {
  background-color: rgba(0, 0, 0, 0.08);
}

.popup-btn-icon {
  width: 16px;
  height: 16px;
}

/* Adaptación para modo móvil */
@media (max-width: 640px) {
  .custom-popup {
    width: 240px;
  }
}

/* Estilos para el tooltip de ayuda de zoom */
.mapbox-zoom-help {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
  pointer-events: none;
  animation: fadeInOut 5s forwards;
}

.zoom-help-tooltip {
  background-color: rgba(0, 0, 0, 0.75);
  color: white;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

@keyframes fadeInOut {
  0% { opacity: 0; }
  10% { opacity: 1; }
  80% { opacity: 1; }
  100% { opacity: 0; }
}

.popup-header {
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.popup-header.entrada {
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  color: white;
}

.popup-header.salida {
  background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
  color: white;
}

.popup-header.registro-hoy {
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
}

.popup-header.registro-antiguo {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.popup-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.popup-fecha {
  font-size: 12px;
  opacity: 0.9;
}

.popup-body {
  padding: 12px 15px;
  background: white;
}

.popup-usuario {
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 5px;
  color: #1f2937;
}

.popup-coordenadas {
  font-size: 11px;
  color: #4b5563;
  font-family: monospace;
}

/* Animación para los puntos del mapa */
@keyframes pulse {
  0% {
    transform: scale(0.8);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
  }
  100% {
    transform: scale(0.8);
    opacity: 0.8;
  }
}

.mapboxgl-ctrl-top-right {
  top: 60px !important;
}

.mapboxgl-ctrl-logo {
  opacity: 0.7;
}

/* Responsive design */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }
  
  .lcd-counter {
    display: none;
  }
}

@media (max-width: 640px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
