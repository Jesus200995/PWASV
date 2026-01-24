<template>
  <div class="fixed inset-0 overflow-hidden" style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(76, 175, 80, 0.08) 50%, rgba(59, 130, 246, 0.05) 100%);">
    <!-- Elementos decorativos -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="background-color: rgba(59, 130, 246, 0.3);"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s; background-color: rgba(76, 175, 80, 0.3);"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s; background-color: rgba(56, 142, 60, 0.3);"></div>
    </div>

    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-4">
      <div class="page-container relative z-10 px-2 sm:px-3 md:px-4 lg:px-6 xl:px-8 py-3 sm:py-4 lg:py-5 min-h-full max-w-full">
        <div class="w-full max-w-lg mx-auto space-y-4">
          <!-- Header de Reportes -->
          <div class="glass-card text-center">
            <div class="flex items-center justify-center mb-3">
              <div class="w-12 h-12 rounded-full flex items-center justify-center shadow-xl" style="background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M7 3H4a1 1 0 00-1 1v16a1 1 0 001 1h16a1 1 0 001-1V8.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0015 2H9a1 1 0 00-1 1v2H7a1 1 0 00-1 1v2zm2-2v2h6V2H9z"/>
                </svg>
              </div>
            </div>
            
            <h1 class="text-xl font-bold text-gray-800 mb-2 modern-title">Mis Reportes</h1>
            <div class="red-line mx-auto mb-2"></div>
            <p class="text-gray-600 text-xs mb-3">Genera reportes mensuales de tus actividades</p>
            
            <!-- Estadísticas rápidas -->
            <div class="grid grid-cols-3 gap-2 mt-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <p class="text-xs text-gray-600 font-medium">Actividades</p>
                <p class="text-lg font-bold text-blue-600">{{ estadisticas.totalActividades }}</p>
              </div>
              <div class="p-2 bg-green-50 rounded-lg">
                <p class="text-xs text-gray-600 font-medium">Período</p>
                <p class="text-xs font-bold text-green-600 truncate">{{ mesActual }}</p>
              </div>
              <div class="p-2 bg-purple-50 rounded-lg">
                <p class="text-xs text-gray-600 font-medium">Estado</p>
                <p class="text-xs font-bold text-purple-600">{{ estadoReporte }}</p>
              </div>
            </div>
          </div>

          <!-- Selector de Período -->
          <div class="glass-card">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" style="background-color: #3B82F6;">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-gray-800">Período</h2>
                <p class="text-xs text-gray-500">Selecciona mes y año</p>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1.5">Mes</label>
                <select
                  v-model.number="mesSeleccionado"
                  @change="cambiarPeriodo"
                  class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option v-for="(mes, index) in meses" :key="index" :value="index">
                    {{ mes }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1.5">Año</label>
                <select
                  v-model.number="anioSeleccionado"
                  @change="cambiarPeriodo"
                  class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option v-for="year in anos" :key="year" :value="year">
                    {{ year }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Sección de Actividades -->
          <div class="glass-card">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" style="background-color: #6366F1;">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                </svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-gray-800">Actividades</h2>
                <p class="text-xs text-gray-500">Listado del período seleccionado</p>
              </div>
            </div>

            <!-- Loading -->
            <div v-if="cargando" class="flex justify-center items-center py-8">
              <div class="text-center">
                <div class="inline-block">
                  <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </div>
                <p class="mt-3 text-xs text-gray-600">Cargando actividades...</p>
              </div>
            </div>

            <!-- Tabla de Actividades -->
            <div v-else class="">
              <table v-if="actividades.length > 0" class="w-full text-xs">
                <thead>
                  <tr class="bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
                    <th class="px-2 py-2 text-left font-semibold">Fecha</th>
                    <th class="px-2 py-2 text-left font-semibold">Hora</th>
                    <th class="hidden sm:table-cell px-2 py-2 text-left font-semibold">Tipo</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(actividad, index) in actividades"
                    :key="actividad.id || index"
                    class="border-b border-gray-200 hover:bg-blue-50 transition-colors"
                  >
                    <td class="px-2 py-2 text-gray-900 font-medium">
                      {{ formatearFecha(actividad.fecha_hora) }}
                    </td>
                    <td class="px-2 py-2 text-gray-700">
                      {{ formatearHora(actividad.fecha_hora) }}
                    </td>
                    <td class="hidden sm:table-cell px-2 py-2">
                      <span
                        :class="[
                          'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
                          actividad.tipo_actividad === 'campo' 
                            ? 'bg-green-100 text-green-800'
                            : actividad.tipo_actividad === 'gabinete'
                            ? 'bg-purple-100 text-purple-800'
                            : 'bg-blue-100 text-blue-800'
                        ]"
                      >
                        {{ capitalizar(actividad.tipo_actividad || 'campo') }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-else class="text-center py-6">
                <div class="w-12 h-12 mx-auto mb-3 bg-gray-200 rounded-full flex items-center justify-center">
                  <i class="fas fa-inbox text-gray-400 text-lg"></i>
                </div>
                <p class="text-gray-500 text-xs">Sin actividades en este período</p>
              </div>
            </div>
          </div>

          <!-- Firma Digital -->
          <div class="glass-card">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" style="background-color: #A855F7;">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z"/>
                  <path d="M20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                </svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-gray-800">Firma</h2>
                <p class="text-xs text-gray-500">Autentica tu reporte</p>
              </div>
            </div>
            <FirmaDigital
              ref="firmaComponent"
              label="Firmar aquí"
            />
          </div>

          <!-- Opciones de Descarga -->
          <div class="glass-card">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" style="background-color: #10B981;">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-gray-800">Descargar</h2>
                <p class="text-xs text-gray-500">Genera tu reporte</p>
              </div>
            </div>

            <!-- Información de Usuario -->
            <div class="rounded-lg p-3 border mb-3" style="background: linear-gradient(to right, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.15)); border-color: rgba(59, 130, 246, 0.3);">
              <div class="mb-2">
                <p class="text-xs text-gray-600 font-medium">Nombre</p>
                <p class="text-sm font-semibold text-gray-900 truncate">{{ usuarioInfo.nombre }}</p>
              </div>
              <div class="mb-2">
                <p class="text-xs text-gray-600 font-medium">Cargo</p>
                <p class="text-sm font-semibold text-gray-900 truncate">{{ usuarioInfo.cargo || 'Facilitador Comunitario' }}</p>
              </div>
              <div class="mb-2">
                <p class="text-xs text-gray-600 font-medium">CURP</p>
                <p class="text-xs font-semibold text-gray-900 truncate">{{ usuarioInfo.curp || 'No registrado' }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-600 font-medium">Correo</p>
                <p class="text-xs font-semibold text-gray-900 truncate">{{ usuarioInfo.correo }}</p>
              </div>
            </div>

            <!-- Opciones de Formato -->
            <div class="space-y-2 mb-3">
              <label class="flex items-center p-2.5 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors">
                <input
                  type="radio"
                  v-model="formatoSeleccionado"
                  value="pdf"
                  class="w-4 h-4 text-blue-600"
                />
                <span class="ml-2">
                  <span class="text-xs font-medium text-gray-900 block">PDF</span>
                  <p class="text-xs text-gray-500">Con tabla y firma</p>
                </span>
              </label>
              <label class="flex items-center p-2.5 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors">
                <input
                  type="radio"
                  v-model="formatoSeleccionado"
                  value="csv"
                  class="w-4 h-4 text-blue-600"
                />
                <span class="ml-2">
                  <span class="text-xs font-medium text-gray-900 block">CSV</span>
                  <p class="text-xs text-gray-500">Para Excel</p>
                </span>
              </label>
            </div>

            <!-- Botón de Descarga -->
            <button
              @click="generarReporte"
              :disabled="cargando || generandoReporte || actividades.length === 0"
              class="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed text-white font-bold py-2 px-3 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 text-xs sm:text-sm"
            >
              <svg v-if="!generandoReporte" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
              </svg>
              <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span class="truncate">{{ generandoReporte ? 'Generando...' : 'Descargar' }}</span>
            </button>
          </div>

          <!-- Historial de Reportes -->
          <div class="glass-card">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" style="background-color: #F59E0B;">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-gray-800">Historial</h2>
                <p class="text-xs text-gray-500">Reportes generados</p>
              </div>
            </div>
            <div v-if="reportesGenerados.length > 0" class="space-y-2">
              <div
                v-for="reporte in reportesGenerados"
                :key="reporte.id"
                class="flex items-center justify-between p-2.5 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-xs"
              >
                <div class="flex items-center gap-2 min-w-0">
                  <div class="flex-shrink-0 w-7 h-7 bg-orange-100 rounded flex items-center justify-center">
                    <i class="fas fa-file text-orange-600 text-xs"></i>
                  </div>
                  <div class="min-w-0">
                    <p class="font-medium text-gray-900 text-xs truncate">{{ reporte.nombre }}</p>
                    <p class="text-xs text-gray-500 truncate">{{ reporte.fecha }}</p>
                  </div>
                </div>
                <span :class="[
                  'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium flex-shrink-0',
                  reporte.tipo === 'PDF' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                ]">
                  {{ reporte.tipo }}
                </span>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <p class="text-xs text-gray-500">Sin reportes generados</p>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import FirmaDigital from '../components/FirmaDigital.vue';
import axios from 'axios';
import { API_URL } from '../utils/network.js';

export default {
  name: 'Reportes',
  components: {
    FirmaDigital
  },
  data() {
    return {
      actividades: [],
      todasLasActividades: [],
      cargando: false,
      generandoReporte: false,
      mesSeleccionado: new Date().getMonth(),
      anioSeleccionado: new Date().getFullYear(),
      anos: [],
      formatoSeleccionado: 'pdf',
      usuarioInfo: {
        nombre: '',
        cargo: '',
        correo: '',
        curp: ''
      },
      reportesGenerados: [],
      meses: [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
      ]
    };
  },
  computed: {
    mesActual() {
      return this.meses[this.mesSeleccionado];
    },
    dateRange() {
      const inicio = new Date(this.anioSeleccionado, this.mesSeleccionado, 1);
      const fin = new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0);
      return `${inicio.toLocaleDateString()} - ${fin.toLocaleDateString()}`;
    },
    estadisticas() {
      return {
        totalActividades: this.actividades.length
      };
    },
    estadoReporte() {
      if (this.actividades.length === 0) return 'Sin datos';
      if (this.$refs.firmaComponent?.hayFirma) return 'Firmado';
      return 'Sin firmar';
    }
  },
  methods: {
    async cargarActividades() {
      try {
        this.cargando = true;
        const usuario = JSON.parse(localStorage.getItem('user'));
        
        if (!usuario || !usuario.id) {
          console.error('❌ No hay usuario en localStorage');
          throw new Error('Usuario no autenticado');
        }
        
        console.log(`📋 Cargando TODAS las actividades para usuario ${usuario.id}`);
        
        // Usar el endpoint /registros igual que en Historial.vue
        const response = await axios.get(`${API_URL}/registros?usuario_id=${usuario.id}`, {
          timeout: 10000,
          headers: {
            'Content-Type': 'application/json'
          }
        });

        console.log('✅ Respuesta del servidor:', response.data);

        if (!response.data || !response.data.registros) {
          throw new Error('No se recibió respuesta del servidor');
        }

        // Guardar TODAS las actividades sin filtrar
        this.todasLasActividades = response.data.registros || [];
        
        // Filtrar por mes/año seleccionado
        this.filtrarActividadesPorPeriodo();
        
        console.log(`✅ Total de actividades: ${this.todasLasActividades.length}`);
        console.log(`✅ Actividades en período seleccionado: ${this.actividades.length}`);
        
      } catch (error) {
        console.error('❌ Error cargando actividades:', error);
        this.actividades = [];
        this.todasLasActividades = [];
        if (error.response) {
          alert(`Error del servidor: ${error.response.data.detail || error.response.statusText}`);
        } else if (error.request) {
          alert('No se pudo conectar con el servidor');
        } else {
          alert(`Error: ${error.message}`);
        }
      } finally {
        this.cargando = false;
      }
    },

    filtrarActividadesPorPeriodo() {
      // Filtrar actividades por mes y año seleccionado
      const inicioDeMes = new Date(this.anioSeleccionado, this.mesSeleccionado, 1);
      const finDelMes = new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0, 23, 59, 59);
      
      this.actividades = this.todasLasActividades.filter(actividad => {
        if (!actividad.fecha_hora) return false;
        
        const fechaActividad = new Date(actividad.fecha_hora);
        return fechaActividad >= inicioDeMes && fechaActividad <= finDelMes;
      });
      
      console.log(`🔍 Filtrado: ${this.actividades.length} actividades entre ${inicioDeMes.toLocaleDateString()} y ${finDelMes.toLocaleDateString()}`);
    },

    cambiarPeriodo() {
      // Solo filtrar si ya tenemos actividades cargadas
      if (this.todasLasActividades && this.todasLasActividades.length > 0) {
        this.filtrarActividadesPorPeriodo();
      } else {
        this.cargarActividades();
      }
    },

    formatearFecha(fechaHora) {
      if (!fechaHora) return '-';
      const date = new Date(fechaHora);
      return date.toLocaleDateString('es-MX', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    formatearHora(fechaHora) {
      if (!fechaHora) return '-';
      const date = new Date(fechaHora);
      return date.toLocaleTimeString('es-MX', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      });
    },

    capitalizar(texto) {
      return texto.charAt(0).toUpperCase() + texto.slice(1);
    },

    async loadImageAsDataURL(imagePath) {
      try {
        const response = await fetch(imagePath);
        const blob = await response.blob();
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result);
          reader.onerror = reject;
          reader.readAsDataURL(blob);
        });
      } catch (error) {
        console.error('Error cargando imagen:', imagePath, error);
        return null;
      }
    },

    async generarReporte() {
      try {
        if (this.actividades.length === 0) {
          alert('No hay actividades para generar el reporte');
          return;
        }

        this.generandoReporte = true;

        if (this.formatoSeleccionado === 'pdf') {
          await this.generarPDF();
        } else {
          this.generarCSV();
        }

        // Agregar a historial
        const fecha = new Date().toLocaleString('es-MX');
        this.reportesGenerados.unshift({
          id: Date.now(),
          nombre: `Reporte ${this.mesActual} ${this.anioSeleccionado}`,
          fecha,
          tipo: this.formatoSeleccionado.toUpperCase()
        });

        this.$notify?.({
          type: 'success',
          message: 'Reporte generado correctamente'
        });
      } catch (error) {
        console.error('❌ Error generando reporte:', error);
        this.$notify?.({
          type: 'error',
          message: 'Error al generar el reporte'
        });
      } finally {
        this.generandoReporte = false;
      }
    },

    async generarPDF() {
      const doc = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      });

      const pageHeight = doc.internal.pageSize.getHeight();
      const pageWidth = doc.internal.pageSize.getWidth();
      let currentY = 10;

      // ===== ENCABEZADO OFICIAL CON LOGOS =====
      
      // Logo Gobierno de México (izquierda) - Base64
      const logoGobiernoMx = 'data:image/png;base64,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';
      
      // Logo Secretaría de Bienestar (centro)
      const logoSecreatariaBienestar = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHQAAAAyCAYAAACuD8d9AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAABNJSURFVHhe7ZwJdFXVmYDv+/K/d1/2hSRAyJ6QsCUsYRFkEQRBURQEF6p1qXZmnFZbO51ZOqfOdGzH6dRRa0etdXSsW0dbtdpat1qXugBuCAiyJED2hSzv5f//3513Q16AJC/vJS/gPef8373nvvfuub9z7zn/vvf9lwkhhBBCCCGEEEIIIfxPWKZpMn19qamp4JCfn89KSkqCc3JygpOTk4NSUlKCEhMTnbxerfr7+zX/v4/n5eUxj8fDfD6f5vP5mN/vZx6Phw0ODrLe3l7W1dWlunM0NDSE6urqArW1tWxtbW1w5cqVqrKyMriysjKooqIiUF5ermZlZQWzsrIC6enp/rS0tEBCQoLeX//l5eU5k5KSnMnJyU4cF0IIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCHsRLjdbqfd3v5Rc99nZ2fjLwAGhoaG2J1wI6i8X/bXXdyRkZGqO0cHPhsbGwN4tru7m2k+HDAwdZ+dE35/A78Y/1P3O8R7hc/z+l9fX99gMBh04jiEwSDCZ4K4PsgvPgZqQIhRCuWbU9XNQlGMf2fhc/A9VbsBP0LqwKsKuZwR+Q8RooQQQhwZIq5kHZ8g/pHBCCUC/L8l8lvA65n8Nvw1Q7s28Hvdw4F+97BdA0Nz84AJ7Qa0O6DfRb/NUE7lJ/z+7L7+fq+Pp/E1aQw8bkDI++g3I5X/uaioKD0WF0l8wKGysrLoSCzh4dPT0+mO0MRf4D6cqqqqsP7b2trCqqurI+rr6yNqa2sj1q5dG1FVVRVRUVERVV5eHlVWVhZRVlYWWVZWpv8NFRYW6tfq18fFxenXjR07Vj0/Ly+PPJuBn8lxDDwbb5rut4aO6TEw8fqbmppUS0tL0dXVVdTS0qJXx+4/6NYI6S4+qF78u6i1g1EvFrXl0z+kJ1+i3pNW5j29ZO/h9s5nBgdYe3s7a2trYy0tLXo1PtDXx3E0eIzLkwj8ypgBLz0KZhyPnIYQOwkP9Gw8eQQhlPLzN+P/Oyr4rwHfAhcx/g/g/WQIH0lYrweaPviBge++4MDAN19fH/P29LC+3l7W09vLvD09bLC/n/n7B5h3YJANE12Dysnf19nZqSNTiokqGPPnz9f90tLSdJ/S0lLdp7S0VHe0SaOC5wlvpXJ8+xYC/RO3h+1wYr1dQvh5rKqy3yHCvwF+F6wH/xK0gX/HiO/B53KmfR88DYYCe+HDTLsWdCd4b3DYl9fTk/fffMxRzwD76eDBePAhPT2dPLEqOztbd8+aNavN5XId6+npafN4PK3Nzc36b3NTE2tpamJNzc2scdMm1ri5ka3fuFF/r6ur0/xp1FDT0aNHq33dtGkT6+npYfX19Wx+Y2PpyJEjbadPn966Y8eO1l27drW2tLQ0rVy5Ev/j3vD8/PwbWPgtDJe/qIpfxP8A3gi+B38JftAEfwDWQT+iP4h7WCy0m8nPh3UvXw3/FpwDfgm68j4/l53A+VxYH+P+V+ZaV3u22+0O9LDyE/kN/Ob+jt7+gA48BrW1ta/DuPnMnDlzMN+mHW+yY6OAnp4e/TcpKUn3KSgooO+6E43hN+HxE4EQZ/dA0E6A7gT0IPQ9IBa8Ftzq82Sxg+A5ML5gDuD7N8BV4B/BD6jVHI/6BnjvKNH/FYTxP/Mx0v8C+zO0+wl8OwKLfgNaD+A/YNoP8fO/grw24G5Qx4+dxPiPgJdBeybw7a/gYX4/j/FfgZfwvn5HL/wJJ5qnQ9ezAJczcQH4K4/zRzz/CJJ3gG9C0sE/hMxk/H2gD3gdj0rwA/TwTeBqcB/Qv+OZ73wDfa/yA0fAdwH9zBv8vhj/+7gLJg8/A8tYpGxBCp4Cn0JyP1LugZdjTn0W+BxfB7bx7+NYS9HgBz6/hm5E0k/gLeCtoO5jmj+zCPgjko+Dl+F93WPgDX7vK/DZ67yf/v8LvB68DP7Gvp+hfd0NP4h3cX+G76/j76v89kvg9yxWCjwT3E84m8bDQaDvN+Sxr4HnQC+4GOr5SPA16EP8d/8HOhM8RP3g9Wh3BdvnTdz5Q14HBvHOC/j+jMX6b6tJ4F+Ae5D0CyRdgYQXQfhXcPTn4x7uXQzeQX/vQPJ1SBr+c4l/B8lfgkl0Nxb/Ae9/YJhz9P/VoP+z/v8Ffh5Bm78A+ln3PnBq5HAwkvCd3jkTSfcguZYu43gF3gN6kHCXxfwxr98W4DTGP4LJP0LSFqR85zl+BKT/Hx/wjD3Y+xj7xQv2o6OfhbeC/oP3hm8An8X3P4H+R3P9A7v31S/88G3gGqT8zb4Pz7qYfv3D/E/TrQx6+DsPDL+Dz+lCPIOf34PPcSD5i/jcFTi5w55dg//xJkRPge+c+xBdgge+GxNAO/AXdP+58h1o94c0rwef7sYvwR1IuQ50Im0F6ESqBv8f6D+Y+cRwlWQ93MXkFNDPuqtGAXm8U1xeLxDOHwa++eRtI/u/BvX/Sn6o1/uXd/k28S9E9qNDCNhPL8jv5GsRBfvL+7j/u3u/s+x7qeu/uHsXfQr68PtnoY/z+CXgJ5xTF+MUvwBGSrcv4Vz6C86lz9kK4LO4d66+xm+9Dz+je2Ypr/9G4+dE/hwPvoa+q/gpfR70MjTP4/dO59/pvPdpPt/Dz+mCc69t8zV+D/OA3zW/H2/ewz1Y3/c+vy/ksUvwvgvxvjO3KsBXYtWI+mE74Y8H/fjZ3XgsGfX8BrX45kMHuX8IPp3L63ZQQL8J9MN88Bn4Lr/vHq+X/Qp+npjB9zKQ9gT85/Mu5DvGb+j3oh/1L/AuxJWcb+dy38ugAzwB+i54nfvHGSN7Bn5+DqoCz+gqGfcAIAd98HOF3Qb2L/TJKuSJ58OzwGnoo/vl0E+4jvXZ1Mf9F/A/L+mygT6vW4f+e/l5/YrP5/TrrWd18jP8nH7Hb3qI94r+9Hn/DvDMp57xt9/G5+Nl6jXfBv7S/i3/j/sPEfwNaOc1fKNPV4J1/IbncK8s4fc0gf5j+TL/HVR0wN/H3D/wGvTz++r5fVTys3uI17OhDeg/pXrwHH7H83gH/WbwDH5GPZ9L9fh9/N70bQTfVu8GvPEzqP1PKFXT48F/Bmv5nZSS/e/m9y29GykXDvNM/9JC/yN6+S38w34vP/Trhj5Q7fsNtv5nKF4C/a/g9f5+pPj/G94L+h/Wy3uofxb//xWvv7+L+0fJDv3PfBGv78HwXjwC+kF/+dB+mGfxbvqfRvUnB0fKxcP0+1/QTzX94+B/C/yf/wv8PH4M7vU/jvd3gPfxu+t5XxXv/VV+T8qxwHV8J+iHfR0+vQ5Nt/yboB/1l1V/ov/N3D+K9/P9exH33wffcIYf/5VTsxS/x1HBE/kB/fwo//RU/oG0U/6nq/kH/dWh/WTR2qF75VAt4/9bw/t/Nkx79B8F9H+O29eh+1DQz/0Fnvt3+/9a29MPg/pd3L+l+9dw/yj9fgH9H6b2//BRHgv1g6/0g0fJA8/l9f33MP8vtgfnz/Ue2g+X/k8c+hy//TP7Pu6/xvvof5v+d/v/2sf7+b0/tXnIqKCa15WbuP/j0H5k0H9a9H/aXj8U/TP/nf2/dP93z/YbKfT/jNf6n9mf0+96BvwC//t19vFD0f896Pd19O/49lO7D/h/zv8n+Wtwqf2Tvl/P6/3W/jwc/W9+tVs/0PPKfITzz+3PD/U/y/8Snv0/+3to/1f8tv+yn9v05+p/1SBj+v+O32HfB/V/AP/WJh/aD/XM/+F/1UY/k/6H+39k+29N/0HQH8p+1L8F7f+oP4d/3V/A79tqfwuv/6P9fv/P+fh/++fPoPrvLKN+d/Tf+lOZ4gO//T98yD9YKr5hJ/OV/7YfCWZE/sO4+JVL+eIz+fIP+AK+xBdS79/0+rnXz70Bp/7F/mzYF6zP+AvVPH2h+qw3cE/F5+qz2PN48R76I9h98GGk//+lp//vkXmIT7sH7P9/o/9v/C+gZnz+R3yO+j/tGgn0f24l7+//0T8o9D+X/rtR/y/3f0z/+cWgq3fW5TcJ+CJy+WJ/yBdzcN/P4VYXv2z1Sv57+3v7vj/T/35f+jP/Uv+Uvr+v/5rg/gu95fdcOP4L/9Q/h0/l0+IvDv5F/l/Gf+6e4L/Cv5b/x+XQqv7l+Bfn/tWr5/oVX8DXcj/9f6WPeJT0X+0JvM0X5HnrN/ZVr/3voN//O9D/5AqorKqB+lrrhg5RYwN1qGP0e/W1VauRekO/V/1VfX/1+Yrb1AKllPrH6hH1z+8+zXmDeoy/Sf1FPUVzU7xNzVCr1a/VP/HX+3+pz/V/6V+r/uk3/jf9K38Gm+MbFXxGzQ18HnxWve9/378zuM5XpO/139n3Z3VU4J/+b3r+0vUe57M2r/F4q9SD/t9p/SHfHvVov++3Xlpuh+Sv+r29/yP2hvdWzXPd5/+T95H+gP/QQE3w2sCB4Ln+c/pP7zsRPNd/WB11sPr/fFf6j/vPLTix4O7+TZ5N/u3qlf6twasDXwn+JPiweo/3C/UU/2NqgnpQC+rGYKN6R/+T3hu9N/n+y/tO4Lzgxf57/bcHzw+8P/Dl4HrfcZ5z/RsH1/k3+T/w79YP+feo//T9LfiJ4P+rT/pfDfwg8ETg30Gxw3dP/8nBU/rXBTYHdgfuDS4L1AUOhn4auit4S/BrwbOCx3l+En56d/+x3iu9V3rO8Fzo/YHvIf+JPuf0P+Zx+U/zrwhcEajyX9W/NPRg/02hr4V+GToh9E//C6FPB1eFdgZXBr8Z2hv8n/BL/RfHXzjutMBrAzcGXh3Y1H9TYHMQ/5+JR8Ix8Yj5CiMEIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIcRoJy0tLSiefHp6enAsfCg7OzuYnZ0dlJmZGZSUlBQUFxcXFBsbG6SB8VNweT09PVgLRa8oK1PqReTnX3FLBobf4MPv0ZooyXWB+Z9FcE6+ZijAx/Uc1L93Hv+2/oL/gn+V4GzYjTwFdnA0z8xHKxGh/+g/x7+zfzcB+gk/5f+Bj+HnvgDL4HPwFfgevMiR7+RiAw/Duz9D0u/BC+BE+zp+LdBZ+m/Cq09BAp2w/iZ0tXC/Xg18HQ6cCl/g43t/Db+6kWw/i1MxRYoUKVKkSJEiRYoUKVKkSJEiRYoUKVKkSJEiRYoUKVLk/yeSk5P/4eeffyZ/iy8jIyMg++P/vyUnJ+u/KSkp+m96errwHx6SyZenb9++fm8PqauqUi0tLaqtrY01NDSEOJ1O/lk0n3bRcHxWKIr6+nr2TXt7uOjq6tL+gIf/r/o0Pt6RY3yy6+eIZ7eAmQx9q8wC3yD5XvlrgqQfgVl8WvJHw/xPP3wq/jz4JrC+pIx9k+Sje/4NTiK7SyHJJ89rp/y8BUuAzhj+Dq8p6u0n4EdgB9C54x58H9Snkx/kZwYD+KwQGxaykj2e8E8TpJCdxE7kI0J2Ex/P63ZkxHH0MXSCHznROAHfxV8H+uSlbIgMPD0f8T8OtoB+vj9N/A6r/8L4xKNmfkD7E3wk0PnqR/gBXQD+gY8S2VX8hR1oi/8z/qPv6W+8dDcf0eSi/tTzDwJ8JJJ/Px/nf8bQaXt8Rrfx/+FjWTTwxG/4gB/d8+/jfYzfx+MU+NydPHMBHwWpM83TH+D3b+X3p/Jx6h/YcaL+O0+cCNJ2pP+pJ9b/6B54Bn4uh/8X/N1Bn+S/BXZw/79+/6O/lyfQ9eL/Buh6uu/hY/43fO1qfjk/rPzAzuVZLfzZf+PXiD5p/0/xA8YLu/Nv5Dl05p6f/wT4L7wW+vl34/kXwKNgL5hI0r3gD+BHoBqcAL+l++c3I8Dv2cr7/wZ+R3fQ/+1+QNNnr4Cf0Z38/wVtl+NXfRlct3cLv+YheyKf9t0FqkG9+6f8CnAG/a7+A5/jz+D34XcNcX9UQGflX+qI4Qv5Qv9Pvsh6vwu/lB9Ww+vbUNPOj6jl9U/5sQzBbz93eD2Ln+sDNO/rw77+w+9uZGhH+aXJ1E/+i5fgWf/Ar/lQsA6cAvRMDz1dv5HPV/kC0Geq6Iy/7/Fr3uC/b9hDlTgJnMrre32AP+NzHfgHXn+Fz72FD7kNf0rnzb9It8FXl0En+qPf/x/9fcPvVvo1I0f/PdI1uvXOO3j99WH/xSv35vE1Lqf/8Pe/j39D9ZrH4Bn4t/9C9/N8N7+A/ge/xH/DLeAGkMCH9/Q/5wdgJXgB0L+LH+FZN/ArQTt/NhPk8vr/Yf6M6u/fx+t/4H/B2WAOf+YicBvI5M++BL5Lv5H/LWk/+jdLP53X/T38N9xq9/8Ndz5F1/D//YYAAAAASUVORK5CYII=';

      // Logo Programa Sembrando Vida (derecha)  
      const logoSembrandoVida = 'data:image/png;base64,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';

      try {
        // Agregar logos en encabezado blanco (sin fondos de color)
        if (logo1) doc.addImage(logo1, 'JPEG', 10, currentY, 30, 15);
        if (logo2) doc.addImage(logo2, 'JPEG', pageWidth / 2 - 19, currentY, 38, 15);
        if (logo3) doc.addImage(logo3, 'JPEG', pageWidth - 40, currentY, 30, 15);
      } catch (error) {
        console.warn('Error al cargar logos:', error);
      }

      currentY += 18;

      // Línea divisoria gris sutil (sin colores llamativos)
      doc.setDrawColor(200, 200, 200);
      doc.setLineWidth(0.5);
      doc.line(10, currentY, pageWidth - 10, currentY);

      currentY += 7;

      // Título principal con borde
      doc.setDrawColor(0, 0, 0);
      doc.setLineWidth(0.3);
      doc.rect(15, currentY, pageWidth - 30, 10);
      
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(12);
      doc.setFont(undefined, 'bold');
      doc.text('INFORME DE ACTIVIDADES MENSUALES', pageWidth / 2, currentY + 6.5, { align: 'center' });

      currentY += 15;

      // ===== TABLA DE INFORMACIÓN DEL SERVIDOR PÚBLICO =====
      const tableStartY = currentY;
      const col1Width = 70;
      const col2Width = pageWidth - 30 - col1Width;

      // Fila 1: Nombre
      doc.setLineWidth(0.3);
      doc.rect(15, currentY, col1Width, 8);
      doc.rect(15 + col1Width, currentY, col2Width, 8);
      
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.text('NOMBRE DEL SERVIDOR PÚBLICO:', 17, currentY + 5.5);
      doc.setFont(undefined, 'normal');
      doc.text(this.usuarioInfo.nombre.toUpperCase(), 17 + col1Width, currentY + 5.5);

      currentY += 8;

      // Fila 2: Puesto
      doc.rect(15, currentY, col1Width, 8);
      doc.rect(15 + col1Width, currentY, col2Width, 8);
      
      doc.setFont(undefined, 'bold');
      doc.text('PUESTO:', 17, currentY + 5.5);
      doc.setFont(undefined, 'normal');
      doc.text((this.usuarioInfo.cargo || 'FACILITADOR COMUNITARIO').toUpperCase(), 17 + col1Width, currentY + 5.5);

      currentY += 8;

      // Fila 3: Período
      doc.rect(15, currentY, col1Width, 8);
      doc.rect(15 + col1Width, currentY, col2Width, 8);
      
      doc.setFont(undefined, 'bold');
      doc.text('PERÍODO DE REPORTE:', 17, currentY + 5.5);
      doc.setFont(undefined, 'normal');
      doc.text(`${this.mesActual.toUpperCase()} ${this.anioSeleccionado}`, 17 + col1Width, currentY + 5.5);

      currentY += 8;

      // Fila 4: Fecha de elaboración
      doc.rect(15, currentY, col1Width, 8);
      doc.rect(15 + col1Width, currentY, col2Width, 8);
      
      doc.setFont(undefined, 'bold');
      doc.text('FECHA DE ELABORACIÓN:', 17, currentY + 5.5);
      doc.setFont(undefined, 'normal');
      const fechaElaboracion = new Date().toLocaleDateString('es-MX', { day: '2-digit', month: '2-digit', year: 'numeric' });
      doc.text(fechaElaboracion, 17 + col1Width, currentY + 5.5);

      currentY += 12;

      // ===== ENCABEZADO DE TABLA DE ACTIVIDADES =====
      doc.setLineWidth(0.3);
      doc.rect(15, currentY, pageWidth - 30, 8);
      
      doc.setFontSize(9);
      doc.setFont(undefined, 'bold');
      doc.text('RESUMEN DE ACTIVIDADES DESARROLLADAS', pageWidth / 2, currentY + 5.5, { align: 'center' });

      currentY += 8;

      // ===== TABLA DE ACTIVIDADES =====
      const numColWidth = 15;
      const actColWidth = pageWidth - 30 - numColWidth;

      // Encabezado de tabla
      doc.setLineWidth(0.3);
      doc.rect(15, currentY, numColWidth, 8);
      doc.rect(15 + numColWidth, currentY, actColWidth, 8);
      
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.text('Núm.', 15 + numColWidth / 2, currentY + 5.5, { align: 'center' });
      doc.text('ACTIVIDAD REALIZADA', 15 + numColWidth + 10, currentY + 5.5);

      currentY += 8;

      // Datos de la tabla
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(7);
      doc.setFont(undefined, 'normal');

      this.actividades.forEach((actividad, index) => {
        if (currentY > pageHeight - 40) {
          doc.addPage();
          
          // Repetir encabezado en nueva página
          doc.setFillColor(105, 27, 63);
          doc.rect(0, 0, pageWidth, 8, 'F');
          doc.setTextColor(255, 255, 255);
          doc.setFontSize(7);
          doc.text('INFORME DE ACTIVIDADES (continuación)', pageWidth / 2, 5, { align: 'center' });
          
          currentY = 15;
          
          // Encabezado de tabla
          doc.setFillColor(105, 27, 63);
          doc.rect(15, currentY - 2, 15, 7, 'F');
          doc.rect(30, currentY - 2, 50, 7, 'F');
          doc.rect(80, currentY - 2, 25, 7, 'F');
          doc.rect(105, currentY - 2, pageWidth - 120, 7, 'F');
          
          doc.setTextColor(255, 255, 255);
          doc.setFontSize(7);
          doc.setFont(undefined, 'bold');
          doc.text('Núm.', 22.5, currentY + 2, { align: 'center' });
          doc.text('ACTIVIDAD REALIZADA', 55, currentY + 2, { align: 'center' });
          doc.text('TIPO', 92.5, currentY + 2, { align: 'center' });
          doc.text('CATEGORÍA', 145, currentY + 2, { align: 'center' });
          
          currentY += 9;
        }

        const fecha = this.formatearFecha(actividad.fecha_hora);
        const tipo = (actividad.tipo_actividad || 'No especificado').toUpperCase();
        const categoria = (actividad.categoria_actividad || 'Sin categoría').toUpperCase();
        const descripcion = actividad.descripcion || 'Sin descripción';

        // Fondo alternado
        if (index % 2 === 0) {
          doc.setFillColor(250, 250, 250);
          doc.rect(15, currentY - 4, pageWidth - 30, 10, 'F');
        }

        // Bordes de celda
        doc.setDrawColor(200, 200, 200);
        doc.setLineWidth(0.1);
        doc.rect(15, currentY - 4, 15, 10);
        doc.rect(30, currentY - 4, 50, 10);
        doc.rect(80, currentY - 4, 25, 10);
        doc.rect(105, currentY - 4, pageWidth - 120, 10);

        doc.setTextColor(0, 0, 0);
        doc.setFont(undefined, 'bold');
        doc.text(`${index + 1}`, 22.5, currentY, { align: 'center' });
        
        doc.setFont(undefined, 'normal');
        // Texto de actividad con fecha
        const textoActividad = `${fecha}.- ${tipo === 'CAMPO' ? 'Campo' : 'Oficina'}\n${descripcion}`;
        const lineas = doc.splitTextToSize(textoActividad, 48);
        doc.text(lineas.slice(0, 2), 31, currentY - 1);
        
        doc.text(tipo.substring(0, 8), 92.5, currentY, { align: 'center' });
        
        const categLineas = doc.splitTextToSize(categoria, pageWidth - 125);
        doc.text(categLineas[0], 106, currentY);

        currentY += 12;
      });

      currentY += 10;

      // ===== FIRM5;

      // ===== PIE DE PÁGINA CON LOGOS =====
      const footerY = pageHeight - 20;
      
      try {
        if (logo1) doc.addImage(logo1, 'JPEG', 20, footerY, 25, 12);
        if (logo2) doc.addImage(logo2, 'JPEG', pageWidth / 2 - 17, footerY, 34, 12);
        if (logo3) doc.addImage(logo3, 'JPEG', pageWidth - 45, footerY, 25, 12);
      } catch (error) {}

      // Número de página
      doc.setFontSize(7);
      doc.setTextColor(100, 100, 100);
      doc.text(`Página 1 de 1`, pageWidth / 2, pageHeight - 5, { align: 'center' });

      // Guardar PDF
      const nombreArchivo = `INFORME_ACTIVIDADES_${this.usuarioInfo.nombre.toUpperCase().replace(/ /g, '_')}_${this.mesActual.toUpperCase()}_${this.anioSeleccionado}.pdf`;
      doc.save(nombreArchivo);
    },

    generarCSV() {
      const headers = ['Fecha', 'Hora', 'Tipo', 'Categoría', 'Descripción', 'Usuario', 'Cargo', 'Correo'];
      
      const rows = this.actividades.map(actividad => [
        this.formatearFecha(actividad.fecha_hora),
        this.formatearHora(actividad.fecha_hora),
        this.capitalizar(actividad.tipo_actividad || '-'),
        actividad.categoria_actividad || '-',
        actividad.descripcion || '',
        this.usuarioInfo.nombre,
        this.usuarioInfo.cargo || '',
        this.usuarioInfo.correo
      ]);

      const csv = [
        headers.join(','),
        ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
      ].join('\n');

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      
      link.setAttribute('href', url);
      link.setAttribute('download', `Reporte_${this.mesActual}_${this.anioSeleccionado}.csv`);
      link.style.visibility = 'hidden';
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  },

  mounted() {
    // Generar años disponibles (años pasados y futuros)
    const currentYear = new Date().getFullYear();
    this.anos = Array.from({ length: 5 }, (_, i) => currentYear - 2 + i);

    // Cargar información del usuario
    const usuario = JSON.parse(localStorage.getItem('user'));
    if (usuario) {
      this.usuarioInfo = {
        nombre: usuario.nombre_completo || usuario.nombre || 'Usuario',
        cargo: usuario.cargo || '',
        correo: usuario.correo || '',
        curp: usuario.curp || ''
      };
    }

    // Cargar actividades
    this.cargarActividades();

    // Cargar reportes del localStorage si existen
    const reportesGuardados = localStorage.getItem('reportesGenerados');
    if (reportesGuardados) {
      this.reportesGenerados = JSON.parse(reportesGuardados);
    }
  },

  beforeUnmount() {
    // Guardar reportes generados
    localStorage.setItem('reportesGenerados', JSON.stringify(this.reportesGenerados));
  }
};
</script>

<style scoped>
/* Estilos glass-card */
.glass-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 1rem;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
}

.modern-title {
  position: relative;
  overflow: hidden;
  color: #0F172A;
}

.red-line {
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #3B82F6, #2563EB);
  border-radius: 2px;
}

/* Animación para elementos decorativos */
@keyframes pulse-slow {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.2;
  }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

/* Animación de aparición */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-in;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .page-container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>
