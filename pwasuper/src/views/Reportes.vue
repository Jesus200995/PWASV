<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 pt-24">
    <!-- Header -->
    <div class="fixed top-0 left-0 right-0 z-10 bg-white shadow-md border-b-4 border-blue-500">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
              <i class="fas fa-file-pdf text-white text-xl"></i>
            </div>
            <div>
              <h1 class="text-3xl font-bold text-gray-900">Mis Reportes</h1>
              <p class="text-sm text-gray-500">Genera y descarga tus reportes mensuales</p>
            </div>
          </div>
          <router-link
            to="/home"
            class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <i class="fas fa-times text-xl"></i>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Cards principales -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <!-- Card de Actividades -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow border-t-4 border-blue-500">
          <div class="bg-gradient-to-r from-blue-50 to-blue-100 px-6 py-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-600 text-sm font-medium">Actividades Mes</p>
                <p class="text-4xl font-bold text-blue-600 mt-2">{{ estadisticas.totalActividades }}</p>
              </div>
              <div class="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center text-white opacity-20">
                <i class="fas fa-tasks text-3xl"></i>
              </div>
            </div>
          </div>
        </div>

        <!-- Card de Rango de Fechas -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow border-t-4 border-green-500">
          <div class="bg-gradient-to-r from-green-50 to-green-100 px-6 py-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-600 text-sm font-medium">Período</p>
                <p class="text-lg font-bold text-green-600 mt-2">{{ mesActual }}</p>
                <p class="text-xs text-gray-500 mt-1">{{ dateRange }}</p>
              </div>
              <div class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center text-white opacity-20">
                <i class="fas fa-calendar text-3xl"></i>
              </div>
            </div>
          </div>
        </div>

        <!-- Card de Estado -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow border-t-4 border-purple-500">
          <div class="bg-gradient-to-r from-purple-50 to-purple-100 px-6 py-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-600 text-sm font-medium">Estado</p>
                <p class="text-xl font-bold text-purple-600 mt-2">{{ estadoReporte }}</p>
                <p class="text-xs text-gray-500 mt-1">Listo para generar</p>
              </div>
              <div class="w-16 h-16 bg-purple-500 rounded-full flex items-center justify-center text-white opacity-20">
                <i class="fas fa-check-circle text-3xl"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Selector de Mes -->
      <div class="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <i class="fas fa-calendar-alt text-blue-500"></i>
          Seleccionar Período
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Mes</label>
            <select
              v-model.number="mesSeleccionado"
              @change="cambiarPeriodo"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option v-for="(mes, index) in meses" :key="index" :value="index">
                {{ mes }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Año</label>
            <select
              v-model.number="anioSeleccionado"
              @change="cambiarPeriodo"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option v-for="year in anos" :key="year" :value="year">
                {{ year }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Sección de Actividades -->
      <div class="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <i class="fas fa-list text-indigo-500"></i>
          Actividades del Período
        </h2>

        <!-- Loading -->
        <div v-if="cargando" class="flex justify-center items-center py-12">
          <div class="text-center">
            <div class="inline-block">
              <svg class="animate-spin h-12 w-12 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
            <p class="mt-4 text-gray-600">Cargando actividades...</p>
          </div>
        </div>

        <!-- Tabla de Actividades -->
        <div v-else class="overflow-x-auto">
          <table v-if="actividades.length > 0" class="w-full">
            <thead>
              <tr class="bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
                <th class="px-4 py-3 text-left text-sm font-semibold">Fecha</th>
                <th class="px-4 py-3 text-left text-sm font-semibold">Hora</th>
                <th class="px-4 py-3 text-left text-sm font-semibold">Tipo</th>
                <th class="px-4 py-3 text-left text-sm font-semibold">Descripción</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(actividad, index) in actividades"
                :key="index"
                class="border-b border-gray-200 hover:bg-blue-50 transition-colors"
              >
                <td class="px-4 py-4 text-sm text-gray-900 font-medium">
                  {{ formatearFecha(actividad.fecha) }}
                </td>
                <td class="px-4 py-4 text-sm text-gray-700">
                  {{ formatearHora(actividad.hora) }}
                </td>
                <td class="px-4 py-4 text-sm">
                  <span
                    :class="[
                      'inline-flex items-center px-3 py-1 rounded-full text-xs font-medium',
                      actividad.tipo === 'entrada' 
                        ? 'bg-green-100 text-green-800'
                        : actividad.tipo === 'salida'
                        ? 'bg-orange-100 text-orange-800'
                        : 'bg-blue-100 text-blue-800'
                    ]"
                  >
                    <i :class="[
                      'fas mr-1.5',
                      actividad.tipo === 'entrada' ? 'fa-sign-in-alt' : 
                      actividad.tipo === 'salida' ? 'fa-sign-out-alt' : 'fa-clipboard'
                    ]"></i>
                    {{ capitalizar(actividad.tipo) }}
                  </span>
                </td>
                <td class="px-4 py-4 text-sm text-gray-600">
                  {{ actividad.descripcion || '-' }}
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="text-center py-12">
            <div class="w-16 h-16 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
              <i class="fas fa-inbox text-gray-400 text-2xl"></i>
            </div>
            <p class="text-gray-500 text-lg">No hay actividades registradas para este período</p>
          </div>
        </div>
      </div>

      <!-- Sección de Firma y Generación de PDF -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Firma -->
        <div class="bg-white rounded-2xl shadow-lg p-6">
          <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <i class="fas fa-pen-fancy text-purple-500"></i>
            Firma Digital
          </h2>
          <p class="text-sm text-gray-600 mb-4">
            Firma el reporte para autenticarlo. Esto será incluido en el PDF final.
          </p>
          <FirmaDigital
            ref="firmaComponent"
            label="Firmar aquí"
          />
        </div>

        <!-- Opciones de Descarga -->
        <div class="bg-white rounded-2xl shadow-lg p-6">
          <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <i class="fas fa-download text-green-500"></i>
            Generar Reporte
          </h2>

          <!-- Información de Usuario -->
          <div class="bg-gray-50 rounded-lg p-4 mb-6">
            <div class="mb-3">
              <p class="text-xs text-gray-500">Nombre Completo</p>
              <p class="text-lg font-semibold text-gray-900">{{ usuarioInfo.nombre }}</p>
            </div>
            <div class="mb-3">
              <p class="text-xs text-gray-500">Cargo</p>
              <p class="text-lg font-semibold text-gray-900">{{ usuarioInfo.cargo || 'No especificado' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Correo</p>
              <p class="text-lg font-semibold text-gray-900">{{ usuarioInfo.correo }}</p>
            </div>
          </div>

          <!-- Opciones de Formato -->
          <div class="space-y-3 mb-6">
            <label class="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors">
              <input
                type="radio"
                v-model="formatoSeleccionado"
                value="pdf"
                class="w-4 h-4 text-blue-600"
              />
              <span class="ml-3">
                <span class="text-sm font-medium text-gray-900">PDF Completo</span>
                <p class="text-xs text-gray-500">Incluye tabla de actividades y firma</p>
              </span>
            </label>
            <label class="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors">
              <input
                type="radio"
                v-model="formatoSeleccionado"
                value="csv"
                class="w-4 h-4 text-blue-600"
              />
              <span class="ml-3">
                <span class="text-sm font-medium text-gray-900">CSV (Excel)</span>
                <p class="text-xs text-gray-500">Importable a hojas de cálculo</p>
              </span>
            </label>
          </div>

          <!-- Botón de Descarga -->
          <button
            @click="generarReporte"
            :disabled="cargando || generandoReporte"
            class="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl"
          >
            <i v-if="!generandoReporte" class="fas fa-download"></i>
            <svg v-else class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ generandoReporte ? 'Generando...' : 'Descargar Reporte' }}
          </button>

          <!-- Información de Firma -->
          <div class="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div class="flex gap-3">
              <i class="fas fa-info-circle text-blue-500 mt-0.5"></i>
              <div class="text-sm text-blue-800">
                <p class="font-semibold">Nota sobre firmas</p>
                <p>La firma es opcional pero recomendada. Se incluirá en el PDF final si está presente.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Historial de Reportes Descargados -->
      <div class="bg-white rounded-2xl shadow-lg p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <i class="fas fa-history text-orange-500"></i>
          Reportes Generados Recientemente
        </h2>
        <div v-if="reportesGenerados.length > 0" class="space-y-3">
          <div
            v-for="reporte in reportesGenerados"
            :key="reporte.id"
            class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                <i class="fas fa-file text-orange-600"></i>
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ reporte.nombre }}</p>
                <p class="text-xs text-gray-500">{{ reporte.fecha }}</p>
              </div>
            </div>
            <span :class="[
              'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
              reporte.tipo === 'PDF' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
            ]">
              {{ reporte.tipo }}
            </span>
          </div>
        </div>
        <div v-else class="text-center py-8">
          <p class="text-gray-500">No hay reportes generados recientemente</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import FirmaDigital from '../components/FirmaDigital.vue';
import reportesService from '../services/reportesService.js';

export default {
  name: 'Reportes',
  components: {
    FirmaDigital
  },
  data() {
    return {
      actividades: [],
      cargando: false,
      generandoReporte: false,
      mesSeleccionado: new Date().getMonth(),
      anioSeleccionado: new Date().getFullYear(),
      anos: [],
      formatoSeleccionado: 'pdf',
      usuarioInfo: {
        nombre: '',
        cargo: '',
        correo: ''
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
        const resultado = await reportesService.obtenerActividadesMesEspecifico(
          usuario.id,
          this.mesSeleccionado,
          this.anioSeleccionado
        );

        this.actividades = resultado.historial || [];
        console.log('✅ Actividades cargadas:', this.actividades);
      } catch (error) {
        console.error('❌ Error cargando actividades:', error);
        this.$notify?.({
          type: 'error',
          message: 'Error al cargar las actividades'
        });
      } finally {
        this.cargando = false;
      }
    },

    cambiarPeriodo() {
      this.cargarActividades();
    },

    formatearFecha(fecha) {
      if (!fecha) return '-';
      const date = new Date(fecha);
      return date.toLocaleDateString('es-MX', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    formatearHora(hora) {
      if (!hora) return '-';
      return hora;
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
      let currentY = 20;

      // Encabezado
      doc.setFillColor(59, 130, 246);
      doc.rect(0, 0, pageWidth, 30, 'F');

      doc.setTextColor(255, 255, 255);
      doc.setFontSize(24);
      doc.setFont(undefined, 'bold');
      doc.text('REPORTE DE ACTIVIDADES', pageWidth / 2, 15, { align: 'center' });

      doc.setFontSize(10);
      doc.setFont(undefined, 'normal');
      doc.text(`${this.mesActual} ${this.anioSeleccionado}`, pageWidth / 2, 25, { align: 'center' });

      currentY = 40;

      // Información del usuario
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(11);
      doc.setFont(undefined, 'bold');
      doc.text('INFORMACIÓN DEL USUARIO', 20, currentY);
      currentY += 8;

      doc.setFontSize(9);
      doc.setFont(undefined, 'normal');
      doc.text(`Nombre: ${this.usuarioInfo.nombre}`, 20, currentY);
      currentY += 6;
      doc.text(`Cargo: ${this.usuarioInfo.cargo || 'No especificado'}`, 20, currentY);
      currentY += 6;
      doc.text(`Correo: ${this.usuarioInfo.correo}`, 20, currentY);
      currentY += 6;
      doc.text(`Fecha de Generación: ${new Date().toLocaleString('es-MX')}`, 20, currentY);
      currentY += 8;

      // Resumen
      doc.setFont(undefined, 'bold');
      doc.setFontSize(11);
      doc.text('RESUMEN', 20, currentY);
      currentY += 8;

      doc.setFontSize(9);
      doc.setFont(undefined, 'normal');
      
      const entradas = this.actividades.filter(a => a.tipo === 'entrada').length;
      const salidas = this.actividades.filter(a => a.tipo === 'salida').length;
      
      doc.text(`Total de Registros: ${this.actividades.length}`, 20, currentY);
      currentY += 6;
      doc.text(`Entradas: ${entradas}`, 20, currentY);
      currentY += 6;
      doc.text(`Salidas: ${salidas}`, 20, currentY);
      currentY += 12;

      // Tabla de Actividades
      doc.setFont(undefined, 'bold');
      doc.setFontSize(11);
      doc.text('DETALLE DE ACTIVIDADES', 20, currentY);
      currentY += 8;

      // Headers
      doc.setFillColor(37, 99, 235);
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');

      const tableY = currentY;
      doc.rect(20, tableY - 4, 170, 6, 'F');
      doc.text('Fecha', 25, tableY);
      doc.text('Hora', 60, tableY);
      doc.text('Tipo', 90, tableY);
      doc.text('Descripción', 110, tableY);

      currentY += 8;
      doc.setTextColor(0, 0, 0);
      doc.setFont(undefined, 'normal');

      // Datos
      this.actividades.forEach((actividad, index) => {
        if (currentY > pageHeight - 30) {
          doc.addPage();
          currentY = 20;
        }

        const fecha = this.formatearFecha(actividad.fecha);
        const hora = this.formatearHora(actividad.hora);
        const tipo = this.capitalizar(actividad.tipo);
        const desc = (actividad.descripcion || '-').substring(0, 30);

        if (index % 2 === 0) {
          doc.setFillColor(240, 244, 255);
          doc.rect(20, currentY - 3, 170, 5, 'F');
        }

        doc.text(fecha, 25, currentY);
        doc.text(hora, 60, currentY);
        doc.text(tipo, 90, currentY);
        doc.text(desc, 110, currentY);

        currentY += 6;
      });

      currentY += 8;

      // Firma
      if (this.$refs.firmaComponent?.hayFirma) {
        if (currentY > pageHeight - 50) {
          doc.addPage();
          currentY = 20;
        }

        doc.setFont(undefined, 'bold');
        doc.setFontSize(10);
        doc.text('FIRMA DIGITAL', 20, currentY);
        currentY += 10;

        const firmaBase64 = this.$refs.firmaComponent.obtenerFirmaBase64();
        doc.addImage(firmaBase64, 'PNG', 20, currentY, 80, 30);
        currentY += 35;

        doc.setFontSize(8);
        doc.setFont(undefined, 'normal');
        doc.text(`Firmado por: ${this.usuarioInfo.nombre}`, 20, currentY);
        currentY += 4;
        doc.text(`Fecha de Firma: ${new Date().toLocaleString('es-MX')}`, 20, currentY);
      }

      // Descargar
      doc.save(`Reporte_${this.mesActual}_${this.anioSeleccionado}.pdf`);
    },

    generarCSV() {
      const headers = ['Fecha', 'Hora', 'Tipo', 'Descripción', 'Usuario', 'Cargo', 'Correo'];
      
      const rows = this.actividades.map(actividad => [
        this.formatearFecha(actividad.fecha),
        this.formatearHora(actividad.hora),
        this.capitalizar(actividad.tipo),
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
        correo: usuario.correo || ''
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
</style>
