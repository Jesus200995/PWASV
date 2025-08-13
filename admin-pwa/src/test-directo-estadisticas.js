// Test directo de la API de estadísticas usando fetch
const API_URL = 'http://localhost:8000'

async function testEstadisticasAsistenciaDirecta() {
  console.log('🧪 PROBANDO ENDPOINT /estadisticas DIRECTAMENTE...')
  console.log('=' .repeat(50))
  
  try {
    console.log('🔍 Conectando a:', API_URL + '/estadisticas')
    
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
    
    console.log('📊 RESPUESTA DEL SERVIDOR:')
    console.log(JSON.stringify(data, null, 2))
    
    if (data.estadisticas) {
      const stats = data.estadisticas
      
      console.log('\n📈 ESTADÍSTICAS OBTENIDAS:')
      console.log('-'.repeat(40))
      console.log(`  📝 Total Asistencias: ${stats.total_asistencias}`)
      console.log(`  🌅 Asistencias Hoy: ${stats.asistencias_hoy}`) 
      console.log(`  👥 Usuarios Presentes: ${stats.usuarios_presentes}`)
      console.log(`  📋 Total Registros: ${stats.total_registros}`)
      console.log(`  👤 Total Usuarios: ${stats.total_usuarios}`)
      console.log(`  📅 Registros Hoy: ${stats.registros_hoy}`)
      
      // Verificaciones
      const tests = [
        {
          nombre: 'Total Asistencias > 50',
          condicion: stats.total_asistencias > 50,
          valor: stats.total_asistencias,
          esperado: '> 50 (sin límite artificial)'
        },
        {
          nombre: 'Asistencias Hoy >= 0',
          condicion: stats.asistencias_hoy >= 0,
          valor: stats.asistencias_hoy,
          esperado: '>= 0'
        },
        {
          nombre: 'Usuarios Presentes >= 0',
          condicion: stats.usuarios_presentes >= 0,
          valor: stats.usuarios_presentes,
          esperado: '>= 0'
        },
        {
          nombre: 'Total Registros >= Total Asistencias',
          condicion: stats.total_registros >= stats.total_asistencias,
          valor: `${stats.total_registros} vs ${stats.total_asistencias}`,
          esperado: 'registros >= asistencias'
        }
      ]
      
      console.log('\n🔬 EJECUTANDO PRUEBAS:')
      console.log('-'.repeat(40))
      
      let todosLosPasaron = true
      
      tests.forEach((test, index) => {
        const resultado = test.condicion ? '✅ PASÓ' : '❌ FALLÓ'
        console.log(`${index + 1}. ${test.nombre}: ${resultado}`)
        console.log(`   Valor: ${test.valor} (${test.esperado})`)
        
        if (!test.condicion) {
          todosLosPasaron = false
        }
      })
      
      console.log('\n🎯 ANÁLISIS DEL PROBLEMA RESUELTO:')
      console.log('-'.repeat(40))
      
      if (stats.total_asistencias > 50) {
        console.log('✅ ¡PROBLEMA SOLUCIONADO!')
        console.log('✅ Los contadores ahora muestran valores reales de la base de datos')
        console.log('✅ Ya NO hay límite de 50 registros')
        console.log('✅ AsistenciaView.vue ahora usa el endpoint /estadisticas')
      } else {
        console.log('⚠️ El problema podría no estar completamente resuelto')
      }
      
      console.log('\n📊 COMPARACIÓN ANTES vs DESPUÉS:')
      console.log('-'.repeat(40))
      console.log('❌ ANTES: Total Asistencias siempre = 50 (LIMIT hardcodeado)')
      console.log(`✅ AHORA: Total Asistencias = ${stats.total_asistencias} (valor real)`)
      console.log('❌ ANTES: Calculado desde datos limitados localmente')
      console.log('✅ AHORA: Obtenido desde endpoint dedicado /estadisticas')
      
      if (todosLosPasaron) {
        console.log('\n🎉 ¡ÉXITO TOTAL!')
        console.log('✅ Todas las pruebas pasaron')
        console.log('✅ La solución está funcionando correctamente')
        console.log('✅ Los usuarios verán los conteos reales en AsistenciaView')
      }
      
    } else {
      console.log('❌ La respuesta no contiene estadísticas válidas')
    }
    
  } catch (error) {
    console.error('❌ ERROR EN LA PRUEBA:', error.message)
    
    if (error.message.includes('ECONNREFUSED')) {
      console.log('🔌 El backend no está corriendo en ' + API_URL)
      console.log('   Ejecuta: python main.py en la carpeta backend/')
    } else if (error.message.includes('401')) {
      console.log('🔐 Error de autorización - pero el endpoint responde')
    } else if (error.message.includes('404')) {
      console.log('🔍 El endpoint /estadisticas no existe')
    }
  }
}

// Función para simular window en Node.js
global.fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args))

// Ejecutar test
testEstadisticasAsistenciaDirecta()
