/**
 * Script de Demostración para Reportes
 * 
 * Copia y pega esto en la consola del navegador (F12) en la página de Reportes
 * para ver en tiempo real cómo se cargan las actividades
 */

console.log(`
╔════════════════════════════════════════════════════════════════╗
║         🧪 DEMOSTRACIÓN DE CARGA DE ACTIVIDADES              ║
╚════════════════════════════════════════════════════════════════╝
`);

// 1. Verificar usuario
console.group('👤 INFORMACIÓN DEL USUARIO');
const usuario = JSON.parse(localStorage.getItem('user'));
console.log('Usuario en localStorage:', usuario);
console.groupEnd();

// 2. Verificar API_URL
console.group('🔗 CONFIGURACIÓN DE API');
console.log('API_URL debe ser http://localhost:8000 en desarrollo');
console.log('O https://apipwa.sembrandodatos.com en producción');
console.groupEnd();

// 3. Hacer petición manual a la API
console.group('📡 PETICIÓN A LA API');
const usuarioId = usuario?.id || 1;
const mes = new Date().getMonth();
const anio = new Date().getFullYear();
const inicioDeMes = new Date(anio, mes, 1);
const finDelMes = new Date(anio, mes + 1, 0);

const fechaInicio = inicioDeMes.toISOString().split('T')[0];
const fechaFin = finDelMes.toISOString().split('T')[0];

console.log(`Usuario ID: ${usuarioId}`);
console.log(`Mes: ${mes + 1}/${anio}`);
console.log(`Rango: ${fechaInicio} a ${fechaFin}`);

// Detectar API URL
const apiUrl = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000' 
  : 'https://apipwa.sembrandodatos.com';

console.log(`API URL: ${apiUrl}`);
console.groupEnd();

// 4. Realizar petición
console.group('⏳ ESPERANDO RESPUESTA...');

fetch(`${apiUrl}/historial/${usuarioId}?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}&limit=1000`)
  .then(response => {
    console.log(`Status: ${response.status}`);
    return response.json();
  })
  .then(data => {
    console.groupEnd();
    console.group('✅ RESPUESTA RECIBIDA');
    console.log(`Total de registros: ${data.total}`);
    console.log(`Cantidad en array: ${data.historial?.length || 0}`);
    console.log('Primeros 3 registros:', data.historial?.slice(0, 3));
    console.groupEnd();
    
    // 5. Mostrar estadísticas
    console.group('📊 ESTADÍSTICAS');
    const entradas = data.historial?.filter(a => a.tipo === 'entrada').length || 0;
    const salidas = data.historial?.filter(a => a.tipo === 'salida').length || 0;
    console.log(`Entradas: ${entradas}`);
    console.log(`Salidas: ${salidas}`);
    console.log(`Otros: ${(data.historial?.length || 0) - entradas - salidas}`);
    console.groupEnd();
  })
  .catch(error => {
    console.groupEnd();
    console.error('❌ ERROR EN LA PETICIÓN:', error);
    console.group('💡 SUGERENCIAS');
    console.log('1. Verifica que el backend está corriendo (python main.py)');
    console.log('2. Verifica que la URL sea correcta');
    console.log('3. Abre la pestaña Network en DevTools para ver más detalles');
    console.groupEnd();
  });

console.log(`
╔════════════════════════════════════════════════════════════════╗
║  ✅ Script ejecutado. Revisa los logs arriba para resultados  ║
╚════════════════════════════════════════════════════════════════╝
`);
