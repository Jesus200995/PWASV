<template>
  <div class="debug-buscador">
    <h1>🔍 Debug del Buscador de Registros</h1>
    
    <div class="section">
      <h2>1️⃣ Autenticación</h2>
      <div v-if="!token" class="alert alert-error">
        ❌ No hay token. Debes iniciar sesión primero.
      </div>
      <div v-else class="alert alert-success">
        ✅ Token encontrado: {{ token.substring(0, 20) }}...
      </div>
    </div>

    <div class="section">
      <h2>2️⃣ Buscar Usuario</h2>
      <div class="input-group">
        <input 
          v-model="curpBuscar" 
          type="text" 
          placeholder="Ingresa CURP, nombre o correo"
          @keyup.enter="paso1BuscarUsuario"
        >
        <button @click="paso1BuscarUsuario" :disabled="loading">
          {{ loading ? '⏳ Buscando...' : '🔍 Buscar' }}
        </button>
      </div>

      <div v-if="resultado1" class="resultado">
        <h3>📊 Resultado:</h3>
        <pre>{{ JSON.stringify(resultado1, null, 2) }}</pre>
        
        <div v-if="resultado1.usuarios && resultado1.usuarios.length > 0" class="usuarios-encontrados">
          <h4>👥 Usuarios encontrados: {{ resultado1.usuarios.length }}</h4>
          <div v-for="(usuario, i) in resultado1.usuarios" :key="i" class="usuario-card">
            <p><strong>ID:</strong> {{ usuario.id }}</p>
            <p><strong>Nombre:</strong> {{ usuario.nombre_completo }}</p>
            <p><strong>CURP:</strong> {{ usuario.curp || 'N/A' }}</p>
            <p><strong>Correo:</strong> {{ usuario.correo }}</p>
            <button @click="paso2CargarRegistros(usuario.id)">
              📥 Cargar registros de este usuario
            </button>
          </div>
        </div>
      </div>

      <div v-if="error1" class="alert alert-error">
        ❌ Error: {{ error1 }}
      </div>
    </div>

    <div class="section" v-if="usuarioSeleccionado">
      <h2>3️⃣ Cargar Registros del Usuario {{ usuarioSeleccionado }}</h2>
      <button @click="paso2CargarRegistros(usuarioSeleccionado)" :disabled="loading">
        {{ loading ? '⏳ Cargando...' : '📥 Cargar Registros' }}
      </button>

      <div v-if="resultado2" class="resultado">
        <h3>📊 Resultado:</h3>
        <p><strong>Total de registros:</strong> {{ resultado2.total }}</p>
        <p><strong>Registros recibidos:</strong> {{ resultado2.registros?.length || 0 }}</p>
        
        <div v-if="resultado2.registros && resultado2.registros.length > 0">
          <h4>📋 Primeros 5 registros:</h4>
          <div v-for="(registro, i) in resultado2.registros.slice(0, 5)" :key="i" class="registro-card">
            <p><strong>ID:</strong> {{ registro.id }}</p>
            <p><strong>Usuario ID:</strong> {{ registro.usuario_id }}</p>
            <p><strong>Descripción:</strong> {{ registro.descripcion?.substring(0, 100) || 'N/A' }}</p>
            <p><strong>Fecha:</strong> {{ registro.fecha_hora }}</p>
            <p><strong>Foto:</strong> {{ registro.foto_url ? '✅ Sí' : '❌ No' }}</p>
          </div>
        </div>
        <div v-else class="alert alert-warning">
          ⚠️ El usuario no tiene registros
        </div>
      </div>

      <div v-if="error2" class="alert alert-error">
        ❌ Error: {{ error2 }}
      </div>
    </div>

    <div class="section">
      <h2>4️⃣ Verificar Backend</h2>
      <button @click="verificarBackend" :disabled="loading">
        {{ loading ? '⏳ Verificando...' : '🔍 Verificar Endpoint OR' }}
      </button>

      <div v-if="resultadoVerificacion" class="resultado">
        <h3>📊 Verificación del Backend:</h3>
        <pre>{{ resultadoVerificacion }}</pre>
      </div>
    </div>

    <div class="section">
      <h2>📝 Registro de Actividad</h2>
      <div class="log">
        <div v-for="(log, i) in logs" :key="i" :class="`log-${log.tipo}`">
          <span class="log-time">{{ log.tiempo }}</span>
          <span class="log-message">{{ log.mensaje }}</span>
        </div>
      </div>
      <button @click="logs = []" v-if="logs.length > 0">🗑️ Limpiar Log</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const API_URL = 'https://apipwa.sembrandodatos.com'
const token = ref(localStorage.getItem('admin_token'))

const curpBuscar = ref('ROCR820619MSLJSB05')
const loading = ref(false)
const resultado1 = ref(null)
const error1 = ref('')
const resultado2 = ref(null)
const error2 = ref('')
const usuarioSeleccionado = ref(null)
const resultadoVerificacion = ref('')
const logs = ref([])

const addLog = (mensaje, tipo = 'info') => {
  const tiempo = new Date().toLocaleTimeString()
  logs.value.push({ tiempo, mensaje, tipo })
}

const paso1BuscarUsuario = async () => {
  if (!curpBuscar.value || curpBuscar.value.length < 3) {
    error1.value = 'Ingresa al menos 3 caracteres'
    return
  }

  loading.value = true
  error1.value = ''
  resultado1.value = null
  addLog(`🔍 Buscando: "${curpBuscar.value}"`, 'info')

  try {
    addLog(`📡 GET ${API_URL}/usuarios/buscar`, 'info')
    addLog(`   Params: nombre=${curpBuscar.value}, correo=${curpBuscar.value}, curp=${curpBuscar.value}`, 'info')

    const response = await axios.get(`${API_URL}/usuarios/buscar`, {
      headers: {
        'Authorization': `Bearer ${token.value}`,
        'Content-Type': 'application/json'
      },
      params: {
        nombre: curpBuscar.value.trim(),
        correo: curpBuscar.value.trim(),
        curp: curpBuscar.value.trim()
      },
      timeout: 15000
    })

    resultado1.value = response.data
    addLog(`✅ Respuesta recibida: ${response.data.usuarios?.length || 0} usuarios`, 'success')

    if (response.data.usuarios && response.data.usuarios.length > 0) {
      usuarioSeleccionado.value = response.data.usuarios[0].id
      addLog(`👤 Usuario seleccionado: ID ${usuarioSeleccionado.value}`, 'success')
    } else {
      addLog(`⚠️ No se encontraron usuarios`, 'warning')
    }

  } catch (err) {
    error1.value = err.response?.data?.detail || err.message
    addLog(`❌ Error: ${error1.value}`, 'error')
    console.error('Error completo:', err)
  } finally {
    loading.value = false
  }
}

const paso2CargarRegistros = async (usuarioId) => {
  if (!usuarioId) return

  loading.value = true
  error2.value = ''
  resultado2.value = null
  usuarioSeleccionado.value = usuarioId
  addLog(`📥 Cargando registros del usuario ${usuarioId}`, 'info')

  try {
    addLog(`📡 GET ${API_URL}/admin/registros`, 'info')
    addLog(`   Params: usuario_id=${usuarioId}, page=1, page_size=5000`, 'info')

    const response = await axios.get(`${API_URL}/admin/registros`, {
      headers: {
        'Authorization': `Bearer ${token.value}`,
        'Content-Type': 'application/json'
      },
      params: {
        usuario_id: usuarioId,
        page: 1,
        page_size: 5000
      },
      timeout: 30000
    })

    resultado2.value = response.data
    addLog(`✅ Registros recibidos: ${response.data.registros?.length || 0} de ${response.data.total || 0}`, 'success')

    if (!response.data.registros || response.data.registros.length === 0) {
      addLog(`⚠️ El usuario no tiene registros en la base de datos`, 'warning')
    }

  } catch (err) {
    error2.value = err.response?.data?.detail || err.message
    addLog(`❌ Error: ${error2.value}`, 'error')
    console.error('Error completo:', err)
  } finally {
    loading.value = false
  }
}

const verificarBackend = async () => {
  loading.value = true
  resultadoVerificacion.value = ''
  addLog(`🔍 Verificando lógica del backend...`, 'info')

  try {
    // Buscar con una CURP que no existe pero con parámetros diferentes
    // para ver si el backend usa OR o AND
    addLog(`📡 Prueba 1: Buscar con CURP existente`, 'info')
    
    const response1 = await axios.get(`${API_URL}/usuarios/buscar`, {
      headers: { 'Authorization': `Bearer ${token.value}` },
      params: { curp: curpBuscar.value },
      timeout: 10000
    })

    const usuarios1 = response1.data?.usuarios || []
    addLog(`   Resultado: ${usuarios1.length} usuarios`, usuarios1.length > 0 ? 'success' : 'warning')

    addLog(`📡 Prueba 2: Buscar con parámetros múltiples (debe usar OR)`, 'info')
    
    const response2 = await axios.get(`${API_URL}/usuarios/buscar`, {
      headers: { 'Authorization': `Bearer ${token.value}` },
      params: {
        nombre: curpBuscar.value,
        correo: curpBuscar.value,
        curp: curpBuscar.value
      },
      timeout: 10000
    })

    const usuarios2 = response2.data?.usuarios || []
    addLog(`   Resultado: ${usuarios2.length} usuarios`, usuarios2.length > 0 ? 'success' : 'warning')

    if (usuarios1.length === usuarios2.length && usuarios1.length > 0) {
      resultadoVerificacion.value = '✅ El backend parece usar OR correctamente (mismo resultado con 1 o 3 parámetros)'
      addLog(resultadoVerificacion.value, 'success')
    } else if (usuarios1.length > 0 && usuarios2.length === 0) {
      resultadoVerificacion.value = '❌ PROBLEMA: El backend parece usar AND (encontró con 1 parámetro pero no con 3)'
      addLog(resultadoVerificacion.value, 'error')
    } else if (usuarios1.length === 0) {
      resultadoVerificacion.value = '⚠️ No se encontraron usuarios con esa CURP. Prueba con otra CURP que sepas que existe.'
      addLog(resultadoVerificacion.value, 'warning')
    } else {
      resultadoVerificacion.value = `ℹ️ Prueba 1: ${usuarios1.length} usuarios | Prueba 2: ${usuarios2.length} usuarios`
      addLog(resultadoVerificacion.value, 'info')
    }

  } catch (err) {
    resultadoVerificacion.value = `❌ Error: ${err.response?.data?.detail || err.message}`
    addLog(resultadoVerificacion.value, 'error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.debug-buscador {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

h1 {
  color: #2c3e50;
  margin-bottom: 30px;
}

.section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.section h2 {
  color: #34495e;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.2em;
}

.input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.input-group input {
  flex: 1;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.input-group input:focus {
  outline: none;
  border-color: #3498db;
}

button {
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.3s;
}

button:hover:not(:disabled) {
  background: #2980b9;
}

button:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.alert {
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.alert-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert-warning {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.resultado {
  margin-top: 15px;
}

.resultado h3, .resultado h4 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.resultado pre {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.usuarios-encontrados,
.registros-lista {
  margin-top: 15px;
}

.usuario-card,
.registro-card {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 10px;
}

.usuario-card p,
.registro-card p {
  margin: 5px 0;
  font-size: 14px;
}

.usuario-card button {
  margin-top: 10px;
}

.log {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 15px;
  border-radius: 4px;
  max-height: 400px;
  overflow-y: auto;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  margin-bottom: 10px;
}

.log > div {
  padding: 4px 0;
  border-bottom: 1px solid #333;
}

.log > div:last-child {
  border-bottom: none;
}

.log-time {
  color: #858585;
  margin-right: 10px;
}

.log-info .log-message {
  color: #4fc3f7;
}

.log-success .log-message {
  color: #81c784;
}

.log-warning .log-message {
  color: #ffb74d;
}

.log-error .log-message {
  color: #e57373;
}
</style>
