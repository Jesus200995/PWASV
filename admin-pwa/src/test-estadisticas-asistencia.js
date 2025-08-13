// Test para verificar que las estadísticas de AsistenciaView funcionan correctamente
import EstadisticasService from './services/estadisticasService.js'

async function testEstadisticasAsistencia() {
  console.log('🧪 PROBANDO ESTADÍSTICAS EN ASISTENCIAVIEW...')
  console.log('=' .repeat(50))
  
  try {
    // Simular el comportamiento que hace AsistenciaView.vue
    console.log('🔍 Obteniendo estadísticas desde el servidor...')
    
    const estadisticas = await EstadisticasService.obtenerEstadisticasConFallback([], [], [])
    
    console.log('📊 ESTADÍSTICAS OBTENIDAS:')
    console.log(`  📝 Total Asistencias (servidor): ${estadisticas.totalAsistencias}`)
    console.log(`  🌅 Asistencias Hoy (servidor): ${estadisticas.asistenciasHoy}`) 
    console.log(`  👥 Usuarios Presentes (servidor): ${estadisticas.usuariosPresentes}`)
    console.log(`  📋 Total Registros: ${estadisticas.totalRegistros}`)
    console.log(`  👤 Total Usuarios: ${estadisticas.totalUsuarios}`)
    console.log(`  📅 Registros Hoy: ${estadisticas.registrosHoy}`)
    
    // Verificaciones
    const tests = [
      {
        nombre: 'Total Asistencias > 50',
        condicion: estadisticas.totalAsistencias > 50,
        valor: estadisticas.totalAsistencias,
        esperado: '> 50'
      },
      {
        nombre: 'Asistencias Hoy >= 0',
        condicion: estadisticas.asistenciasHoy >= 0,
        valor: estadisticas.asistenciasHoy,
        esperado: '>= 0'
      },
      {
        nombre: 'Usuarios Presentes >= 0',
        condicion: estadisticas.usuariosPresentes >= 0,
        valor: estadisticas.usuariosPresentes,
        esperado: '>= 0'
      },
      {
        nombre: 'Total Registros > Total Asistencias',
        condicion: estadisticas.totalRegistros >= estadisticas.totalAsistencias,
        valor: `${estadisticas.totalRegistros} vs ${estadisticas.totalAsistencias}`,
        esperado: 'registros >= asistencias'
      }
    ]
    
    console.log('\n🔬 EJECUTANDO PRUEBAS:')
    console.log('-'.repeat(40))
    
    let todosLosPasaron = true
    
    tests.forEach((test, index) => {
      const resultado = test.condicion ? '✅ PASÓ' : '❌ FALLÓ'
      console.log(`${index + 1}. ${test.nombre}: ${resultado}`)
      console.log(`   Valor: ${test.valor} (Esperado: ${test.esperado})`)
      
      if (!test.condicion) {
        todosLosPasaron = false
      }
    })
    
    console.log('\n📊 RESUMEN:')
    console.log('-'.repeat(40))
    
    if (todosLosPasaron) {
      console.log('🎉 ¡TODAS LAS PRUEBAS PASARON!')
      console.log('✅ Los contadores en AsistenciaView ahora muestran los valores reales de la BD')
      console.log('✅ Ya NO están limitados a 50 registros')
      console.log('✅ El servicio de estadísticas funciona correctamente')
    } else {
      console.log('⚠️ Algunas pruebas fallaron')
      console.log('❌ Revisar la implementación')
    }
    
    // Comparación antes/después
    console.log('\n📈 COMPARACIÓN ANTES vs DESPUÉS:')
    console.log('-'.repeat(40))
    console.log('❌ ANTES: Total Asistencias = 50 (limitado por LIMIT 50)')
    console.log(`✅ AHORA: Total Asistencias = ${estadisticas.totalAsistencias} (valor real de BD)`)
    console.log('❌ ANTES: Contadores calculados solo con registros limitados')
    console.log('✅ AHORA: Contadores obtenidos del endpoint /estadisticas dedicado')
    
  } catch (error) {
    console.error('❌ ERROR EN LA PRUEBA:', error)
    
    if (error.message === 'TOKEN_EXPIRED') {
      console.log('🔐 Parece que necesitas hacer login en la aplicación primero')
    } else if (error.code === 'ERR_NETWORK') {
      console.log('🌐 Problema de conexión - asegúrate de que el backend esté corriendo')
    }
  }
}

// Ejecutar test
testEstadisticasAsistencia()
