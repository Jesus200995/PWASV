/**
 * Script de prueba para verificar el API_URL y las peticiones del servicio de reportes
 * Este script replica exactamente lo que hace el frontend
 */

import axios from 'axios';

// Simulamos la función de detectar entorno igual que en network.js
function detectEnvironment() {
  console.log(`🔍 Detectando entorno...`);
  console.log(`   Hostname: ${typeof window !== 'undefined' ? window.location.hostname : 'Node.js'}`);
  
  if (typeof window === 'undefined') {
    // En Node.js, asumir localhost
    return 'development';
  }
  
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'development';
  }
  return 'production';
}

// Simulamos las URLs de API
const API_URLS = {
  development: ["http://localhost:8000", "http://localhost:8001"],
  production: "https://apipwa.sembrandodatos.com"
};

function getApiUrl() {
  const environment = detectEnvironment();
  console.log(`🌍 Entorno detectado: ${environment}`);
  
  const urls = API_URLS[environment];
  const apiUrl = Array.isArray(urls) ? urls[0] : urls;
  
  console.log(`🔗 API_URL configurada como: ${apiUrl}`);
  return apiUrl;
}

const API_URL = getApiUrl();

// Simulamos la función reportesService.obtenerActividadesMesEspecifico
async function testObtenerActividadesMesEspecifico(usuarioId, mes, anio) {
  try {
    console.log(`\n📊 Obteniendo actividades de ${mes + 1}/${anio} para usuario ${usuarioId}`);
    
    const inicioDeMes = new Date(anio, mes, 1);
    const finDelMes = new Date(anio, mes + 1, 0);
    
    const fechaInicio = inicioDeMes.toISOString().split('T')[0];
    const fechaFin = finDelMes.toISOString().split('T')[0];
    
    console.log(`📅 Rango calculado: ${fechaInicio} a ${fechaFin}`);
    console.log(`🔗 URL: ${API_URL}/historial/${usuarioId}`);
    
    const params = {
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin,
      limit: 1000
    };
    
    console.log(`📋 Parámetros:`, params);
    
    const response = await axios.get(`${API_URL}/historial/${usuarioId}`, {
      params: params,
      timeout: 10000
    });
    
    console.log(`✅ Respuesta del servidor:`, response.data);
    console.log(`📊 Total de actividades obtenidas: ${response.data.historial?.length || 0}`);
    
    return response.data;
  } catch (error) {
    console.error(`❌ Error obteniendo actividades:`, error.message);
    if (error.response) {
      console.error(`📋 Respuesta del servidor:`, error.response.data);
      console.error(`⚠️ Status code: ${error.response.status}`);
    } else if (error.request) {
      console.error(`📋 No hay respuesta del servidor`);
      console.error(`🔗 URL solicitada: ${error.config?.url}`);
    }
    throw error;
  }
}

// Función principal
async function runTests() {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`🧪 PRUEBAS DE API_URL Y REPORTES`);
  console.log(`${'='.repeat(60)}`);
  
  const usuarioId = 1; // Cambiar según sea necesario
  const mesActual = new Date().getMonth();
  const anioActual = new Date().getFullYear();
  
  // Prueba 1: Mes actual
  console.log(`\n📍 PRUEBA 1: Mes actual (${mesActual + 1}/${anioActual})`);
  try {
    await testObtenerActividadesMesEspecifico(usuarioId, mesActual, anioActual);
  } catch (error) {
    console.error(`❌ Prueba 1 falló`);
  }
  
  // Prueba 2: Enero 2026
  console.log(`\n📍 PRUEBA 2: Enero 2026`);
  try {
    await testObtenerActividadesMesEspecifico(usuarioId, 0, 2026);
  } catch (error) {
    console.error(`❌ Prueba 2 falló`);
  }
  
  // Prueba 3: Otro mes
  console.log(`\n📍 PRUEBA 3: Diciembre 2025`);
  try {
    await testObtenerActividadesMesEspecifico(usuarioId, 11, 2025);
  } catch (error) {
    console.error(`❌ Prueba 3 falló`);
  }
  
  console.log(`\n${'='.repeat(60)}`);
  console.log(`✅ Pruebas completadas`);
  console.log(`${'='.repeat(60)}`);
}

// Ejecutar pruebas
runTests().catch(console.error);
