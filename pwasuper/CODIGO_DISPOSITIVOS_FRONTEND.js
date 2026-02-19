/* ============================================================================
 * CÓDIGO PARA AGREGAR A pwasuper/src/views/Login.vue
 * ============================================================================
 */

// 1. AGREGAR ESTA FUNCIÓN al principio de la sección <script setup>
// (después de las importaciones, alrededor de la línea 50)

/**
 * Detecta el tipo de dispositivo del usuario
 * @returns {string} 'Android', 'iOS', 'Desktop', o 'Desconocido'
 */
function detectarDispositivo() {
  const userAgent = navigator.userAgent || navigator.vendor || window.opera;
  
  // Detectar iOS
  if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
    return 'iOS';
  }
  
  // Detectar Android
  if (/android/i.test(userAgent)) {
    return 'Android';
  }
  
  // Detectar Desktop (Windows, Mac, Linux)
  if (/Windows|Macintosh|Linux/.test(userAgent)) {
    return 'Desktop';
  }
  
  return 'Desconocido';
}

/**
 * Envía información del dispositivo al backend
 */
async function enviarInfoDispositivo(usuarioId) {
  try {
    const dispositivo = detectarDispositivo();
    const userAgent = navigator.userAgent;
    
    await axios.post(`${currentApiUrl.value}/actualizar_dispositivo`, {
      usuario_id: usuarioId,
      dispositivo: dispositivo,
      user_agent: userAgent
    });
    
    console.log(`📱 Dispositivo registrado: ${dispositivo}`);
  } catch (error) {
    console.warn('⚠️ No se pudo actualizar el dispositivo:', error);
    // No mostrar error al usuario, es información estadística
  }
}


// 2. MODIFICAR LA FUNCIÓN handleLogin
// Agregar esta línea DESPUÉS de guardar el usuario en localStorage
// (alrededor de la línea 220, después de localStorage.setItem('user', ...))

    // Enviar información del dispositivo al backend (no esperar respuesta)
    enviarInfoDispositivo(userData.id).catch(err => 
      console.warn('No se pudo registrar dispositivo:', err)
    );


// 3. La modificación completa sería algo así (sección relevante de handleLogin):

async function handleLogin(event) {
  event.preventDefault();
  
  // ... código existente de validación ...
  
  try {
    const response = await axios.post(`${currentApiUrl.value}/login`, {
      correo: email.value,
      contrasena: password.value
    }, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    const userData = response.data;
    
    // Guardar datos del usuario en localStorage
    localStorage.setItem('user', JSON.stringify(userData));
    
    // 🆕 AGREGAR ESTA LÍNEA:
    enviarInfoDispositivo(userData.id).catch(err => 
      console.warn('No se pudo registrar dispositivo:', err)
    );
    
    // ... resto del código existente ...
    
  } catch (error) {
    // ... manejo de errores existente ...
  }
}


/* ============================================================================
 * FIN DEL CÓDIGO PARA AGREGAR
 * ============================================================================
 */
