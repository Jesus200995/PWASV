// Script para obtener la documentación OpenAPI y ver todos los endpoints
import axios from 'axios'

const API_URL = 'https://apipwa.sembrandodatos.com'

async function obtenerDocumentacionAPI() {
  try {
    console.log('📖 Obteniendo documentación OpenAPI...')
    
    const response = await axios.get(`${API_URL}/openapi.json`)
    const openapi = response.data
    
    console.log('✅ Documentación obtenida')
    console.log('📋 Información de la API:')
    console.log(`   Título: ${openapi.info?.title || 'No especificado'}`)
    console.log(`   Versión: ${openapi.info?.version || 'No especificada'}`)
    console.log(`   Descripción: ${openapi.info?.description || 'No especificada'}`)
    
    console.log('\n🛣️  Endpoints disponibles:')
    
    if (openapi.paths) {
      for (const [path, methods] of Object.entries(openapi.paths)) {
        console.log(`\n📍 ${path}`)
        
        for (const [method, details] of Object.entries(methods)) {
          const summary = details.summary || 'Sin descripción'
          const tags = details.tags ? details.tags.join(', ') : 'Sin categoría'
          
          console.log(`   ${method.toUpperCase()}: ${summary} [${tags}]`)
          
          // Si hay parámetros, mostrarlos
          if (details.parameters && details.parameters.length > 0) {
            console.log(`   Parámetros:`)
            details.parameters.forEach(param => {
              console.log(`     - ${param.name} (${param.in}): ${param.description || 'Sin descripción'}`)
            })
          }
        }
      }
    }
    
    // Buscar específicamente endpoints relacionados con usuarios
    console.log('\n👥 Endpoints relacionados con usuarios:')
    
    if (openapi.paths) {
      const endpointsUsuarios = Object.keys(openapi.paths).filter(path => 
        path.toLowerCase().includes('usuario') || 
        path.toLowerCase().includes('user') ||
        path.toLowerCase().includes('admin')
      )
      
      if (endpointsUsuarios.length > 0) {
        endpointsUsuarios.forEach(path => {
          console.log(`   🔹 ${path}`)
          const methods = Object.keys(openapi.paths[path])
          console.log(`     Métodos: ${methods.join(', ').toUpperCase()}`)
        })
      } else {
        console.log('   ❌ No se encontraron endpoints específicos de usuarios')
      }
    }
    
  } catch (error) {
    console.error('💥 Error al obtener documentación:', error.message)
  }
}

// Ejecutar
obtenerDocumentacionAPI()
