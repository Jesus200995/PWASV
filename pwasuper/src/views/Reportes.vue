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

      // ===== ENCABEZADO OFICIAL =====
      // Franja guinda superior
      doc.setFillColor(105, 27, 63); // Color guinda oficial
      doc.rect(0, 0, pageWidth, 15, 'F');

      // Texto "SECRETARÍA DE BIENESTAR"
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(9);
      doc.setFont(undefined, 'bold');
      doc.text('SECRETARÍA DE BIENESTAR', pageWidth / 2, 7, { align: 'center' });
      doc.setFontSize(7);
      doc.setFont(undefined, 'normal');
      doc.text('Programa Sembrando Vida', pageWidth / 2, 11, { align: 'center' });

      currentY = 20;

      // Título del documento
      doc.setTextColor(105, 27, 63);
      doc.setFontSize(14);
      doc.setFont(undefined, 'bold');
      doc.text('INFORME DE ACTIVIDADES', pageWidth / 2, currentY, { align: 'center' });
      
      currentY += 8;
      doc.setFontSize(10);
      doc.setTextColor(0, 0, 0);
      doc.text(`${this.mesActual.toUpperCase()} ${this.anioSeleccionado}`, pageWidth / 2, currentY, { align: 'center' });

      // Línea divisoria
      currentY += 5;
      doc.setDrawColor(105, 27, 63);
      doc.setLineWidth(0.5);
      doc.line(15, currentY, pageWidth - 15, currentY);

      currentY += 8;

      // ===== DATOS DEL FACILITADOR =====
      doc.setFillColor(240, 240, 240);
      doc.rect(15, currentY - 3, pageWidth - 30, 30, 'F');
      
      doc.setTextColor(105, 27, 63);
      doc.setFontSize(10);
      doc.setFont(undefined, 'bold');
      doc.text('DATOS DEL FACILITADOR', 18, currentY + 2);
      
      currentY += 8;
      doc.setFontSize(8);
      doc.setTextColor(0, 0, 0);
      doc.setFont(undefined, 'normal');
      
      doc.text(`NOMBRE:`, 18, currentY);
      doc.setFont(undefined, 'bold');
      doc.text(this.usuarioInfo.nombre.toUpperCase(), 38, currentY);
      
      currentY += 5;
      doc.setFont(undefined, 'normal');
      doc.text(`CARGO:`, 18, currentY);
      doc.setFont(undefined, 'bold');
      doc.text((this.usuarioInfo.cargo || 'FACILITADOR COMUNITARIO').toUpperCase(), 38, currentY);
      
      currentY += 5;
      doc.setFont(undefined, 'normal');
      doc.text(`CURP:`, 18, currentY);
      doc.setFont(undefined, 'bold');
      doc.text((this.usuarioInfo.curp || 'NO REGISTRADO').toUpperCase(), 38, currentY);
      
      currentY += 5;
      doc.setFont(undefined, 'normal');
      doc.text(`CORREO:`, 18, currentY);
      doc.setFont(undefined, 'bold');
      doc.text(this.usuarioInfo.correo.toLowerCase(), 38, currentY);

      currentY += 10;

      // ===== RESUMEN DE ACTIVIDADES =====
      doc.setFillColor(105, 27, 63);
      doc.rect(15, currentY, pageWidth - 30, 7, 'F');
      
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(9);
      doc.setFont(undefined, 'bold');
      doc.text('RESUMEN DE ACTIVIDADES DESARROLLADAS', pageWidth / 2, currentY + 5, { align: 'center' });
      
      currentY += 12;

      const campo = this.actividades.filter(a => a.tipo_actividad === 'campo').length;
      const gabinete = this.actividades.filter(a => a.tipo_actividad === 'gabinete').length;

      doc.setTextColor(0, 0, 0);
      doc.setFontSize(8);
      doc.setFont(undefined, 'normal');
      doc.text(`Total de Actividades Registradas: ${this.actividades.length}`, 18, currentY);
      currentY += 5;
      doc.text(`Actividades de Campo: ${campo}`, 18, currentY);
      currentY += 5;
      doc.text(`Actividades de Gabinete: ${gabinete}`, 18, currentY);

      currentY += 10;

      // ===== TABLA DE ACTIVIDADES =====
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

      // ===== FIRMAS =====
      if (currentY > pageHeight - 60) {
        doc.addPage();
        currentY = 20;
      }

      // Línea divisoria antes de firmas
      doc.setDrawColor(105, 27, 63);
      doc.setLineWidth(0.5);
      doc.line(15, currentY, pageWidth - 15, currentY);
      currentY += 15;

      // Firma del Facilitador
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.setTextColor(0, 0, 0);
      
      if (this.$refs.firmaComponent?.hayFirma) {
        const firmaBase64 = this.$refs.firmaComponent.obtenerFirmaBase64();
        doc.addImage(firmaBase64, 'PNG', 25, currentY - 5, 50, 20);
        currentY += 18;
      } else {
        currentY += 15;
      }

      doc.line(25, currentY, 75, currentY);
      currentY += 5;
      doc.text('Elaboró', pageWidth / 4, currentY, { align: 'center' });
      currentY += 8;
      doc.setFontSize(7);
      doc.setFont(undefined, 'normal');
      doc.text('Facilitador Comunitario', pageWidth / 4, currentY, { align: 'center' });
      currentY += 4;
      doc.setFont(undefined, 'bold');
      doc.text(this.usuarioInfo.nombre.toUpperCase(), pageWidth / 4, currentY, { align: 'center' });

      // Firma del Coordinador (espacio vacío)
      const firmaY = currentY - 37;
      doc.line(pageWidth - 75, firmaY + 15, pageWidth - 25, firmaY + 15);
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.text('Aprobó', pageWidth * 3 / 4, firmaY + 20, { align: 'center' });
      doc.setFontSize(7);
      doc.setFont(undefined, 'normal');
      doc.text('Encargada de Despacho de la', pageWidth * 3 / 4, firmaY + 28, { align: 'center' });
      doc.text('Coordinación Territorial', pageWidth * 3 / 4, firmaY + 32, { align: 'center' });

      // Pie de página
      currentY = pageHeight - 15;
      doc.setFillColor(105, 27, 63);
      doc.rect(0, currentY, pageWidth, 15, 'F');
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(6);
      doc.text(`Generado el ${new Date().toLocaleDateString('es-MX', { day: '2-digit', month: 'long', year: 'numeric' })}`, pageWidth / 2, currentY + 8, { align: 'center' });

      // Descargar
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
