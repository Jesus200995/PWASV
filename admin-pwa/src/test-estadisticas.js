// Script para probar las estadísticas desde el frontend
console.log('🧪 Iniciando prueba de estadísticas...')

// Simular una llamada al endpoint de estadísticas
async function probarEstadisticas() {
  try {
    const API_URL = 'http://localhost:8000' // Usar localhost para pruebas
    
    console.log('📡 Haciendo petición a:', `${API_URL}/estadisticas`)
    
    const response = await fetch(`${API_URL}/estadisticas`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    
    const data = await response.json()
    console.log('✅ Respuesta exitosa:', data)
    
    if (data.estadisticas) {
      const stats = data.estadisticas
      console.log('📊 ESTADÍSTICAS OBTENIDAS:')
      console.log(`  📋 Total Actividades: ${stats.total_registros}`)
      console.log(`  👥 Total Usuarios: ${stats.total_usuarios}`)
      console.log(`  📅 Actividades Hoy: ${stats.registros_hoy}`)
      console.log(`  ⏰ Total Asistencias: ${stats.total_asistencias}`)
      console.log(`  🕐 Asistencias Hoy: ${stats.asistencias_hoy}`)
      console.log(`  👤 Usuarios Presentes: ${stats.usuarios_presentes}`)
      
      // Verificar el problema específico de "Total Actividades"
      if (stats.total_registros > 50) {
        console.log(`🎯 PROBLEMA RESUELTO: El total real de actividades es ${stats.total_registros}, no 50!`)
      } else {
        console.log(`⚠️ El total sigue siendo bajo: ${stats.total_registros}`)
      }
    }
    
  } catch (error) {
    console.error('❌ Error en la prueba:', error)
    
    if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
      console.error('🌐 Error de red: ¿Está el backend corriendo en http://localhost:8000?')
    }
  }
}

// Ejecutar la prueba
probarEstadisticas()
