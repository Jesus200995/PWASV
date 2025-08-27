// Test manual de push notifications desde consola del navegador
// Copiar y pegar en DevTools > Console de PWA Super

console.log('🧪 INICIANDO TEST MANUAL DE PUSH NOTIFICATIONS');

async function testPushNotifications() {
  try {
    console.log('1️⃣ Verificando soporte...');
    
    // Verificar soporte básico
    if (!('serviceWorker' in navigator)) {
      throw new Error('Service Workers no soportados');
    }
    
    if (!('PushManager' in window)) {
      throw new Error('Push Manager no soportado');
    }
    
    if (!('Notification' in window)) {
      throw new Error('Notifications API no soportada');
    }
    
    console.log('✅ Soporte verificado');
    
    console.log('2️⃣ Obteniendo Service Worker...');
    
    // Obtener service worker registration
    const registration = await navigator.serviceWorker.ready;
    console.log('✅ Service Worker listo:', registration);
    
    console.log('3️⃣ Verificando permisos...');
    
    // Verificar y solicitar permisos
    let permission = Notification.permission;
    console.log('   Permiso actual:', permission);
    
    if (permission === 'default') {
      console.log('   Solicitando permisos...');
      permission = await Notification.requestPermission();
      console.log('   Permiso obtenido:', permission);
    }
    
    if (permission !== 'granted') {
      throw new Error('Permisos denegados');
    }
    
    console.log('✅ Permisos concedidos');
    
    console.log('4️⃣ Obteniendo clave VAPID...');
    
    // Obtener clave VAPID del servidor
    let vapidKey;
    try {
      const response = await fetch('http://localhost:8000/api/vapid-public-key');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      vapidKey = data.publicKey;
      console.log('✅ Clave VAPID obtenida:', vapidKey.substring(0, 20) + '...');
    } catch (err) {
      console.warn('⚠️ Error obteniendo VAPID del servidor:', err.message);
      // Usar clave de desarrollo como fallback
      vapidKey = 'BK2xdNLfyiFTLYObswC7XFi2ZFqU_VDqkteuiVxiPpJP6vzI6bvwL5xGB0ovqVpvngpQ8SdX1kF_eR3QsblHeN4';
      console.log('🔧 Usando clave VAPID de fallback');
    }
    
    console.log('5️⃣ Convertir clave VAPID...');
    
    // Convertir clave VAPID
    function urlBase64ToUint8Array(base64String) {
      const padding = '='.repeat((4 - base64String.length % 4) % 4);
      const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');
      
      const rawData = window.atob(base64);
      const outputArray = new Uint8Array(rawData.length);
      
      for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
      }
      return outputArray;
    }
    
    const applicationServerKey = urlBase64ToUint8Array(vapidKey);
    console.log('✅ Clave VAPID convertida');
    
    console.log('6️⃣ Verificando suscripción existente...');
    
    // Verificar suscripción existente
    let subscription = await registration.pushManager.getSubscription();
    
    if (subscription) {
      console.log('🔍 Suscripción existente encontrada:');
      console.log('   Endpoint:', subscription.endpoint);
      console.log('   Endpoint válido:', subscription.endpoint && subscription.endpoint.length > 50);
      
      if (!subscription.endpoint || subscription.endpoint.length < 50) {
        console.log('❌ Suscripción existente inválida, eliminando...');
        await subscription.unsubscribe();
        subscription = null;
      }
    }
    
    console.log('7️⃣ Creando nueva suscripción...');
    
    // Crear nueva suscripción
    if (!subscription) {
      subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: applicationServerKey
      });
      
      console.log('✅ Nueva suscripción creada');
    }
    
    console.log('8️⃣ Verificando datos de suscripción...');
    
    // Verificar datos críticos
    console.log('🔍 DATOS DE SUSCRIPCIÓN:');
    console.log('   Endpoint:', subscription.endpoint);
    console.log('   Endpoint length:', subscription.endpoint ? subscription.endpoint.length : 0);
    console.log('   Endpoint válido:', subscription.endpoint && subscription.endpoint.startsWith('https://'));
    console.log('   Tiene P256DH:', !!subscription.getKey('p256dh'));
    console.log('   Tiene AUTH:', !!subscription.getKey('auth'));
    
    if (!subscription.endpoint) {
      throw new Error('❌ CRÍTICO: Endpoint está vacío después de crear suscripción');
    }
    
    if (subscription.endpoint.length < 50) {
      throw new Error('❌ CRÍTICO: Endpoint es demasiado corto');
    }
    
    if (!subscription.endpoint.startsWith('https://')) {
      throw new Error('❌ CRÍTICO: Endpoint no es HTTPS');
    }
    
    console.log('9️⃣ Preparando datos para servidor...');
    
    // Preparar datos para enviar al servidor
    const subscriptionData = {
      usuario_id: 2390, // ID de usuario test
      endpoint: subscription.endpoint,
      keys: {
        p256dh: btoa(String.fromCharCode.apply(null, new Uint8Array(subscription.getKey('p256dh')))),
        auth: btoa(String.fromCharCode.apply(null, new Uint8Array(subscription.getKey('auth'))))
      },
      userAgent: navigator.userAgent,
      deviceInfo: {
        type: 'mobile',
        platform: navigator.platform + '-MANUAL-TEST'
      }
    };
    
    console.log('📤 DATOS PARA ENVIAR:');
    console.log('   Usuario ID:', subscriptionData.usuario_id);
    console.log('   Endpoint preview:', subscriptionData.endpoint.substring(0, 50) + '...');
    console.log('   P256DH preview:', subscriptionData.keys.p256dh.substring(0, 20) + '...');
    console.log('   Auth preview:', subscriptionData.keys.auth.substring(0, 20) + '...');
    
    console.log('🔟 Enviando al servidor...');
    
    // Enviar al servidor
    const response = await fetch('http://localhost:8000/api/push/subscribe', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(subscriptionData)
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Error del servidor (${response.status}): ${errorText}`);
    }
    
    const result = await response.json();
    console.log('✅ SUSCRIPCIÓN ENVIADA AL SERVIDOR:');
    console.log('   Respuesta:', result);
    
    console.log('1️⃣1️⃣ Test de push inmediato...');
    
    // Test de push inmediato
    const testResponse = await fetch('http://localhost:8000/api/push/test/2390', {
      method: 'POST'
    });
    
    if (testResponse.ok) {
      const testResult = await testResponse.json();
      console.log('🚀 TEST PUSH RESULTADO:');
      console.log('   Success:', testResult.success);
      console.log('   Dispositivos:', testResult.dispositivos);
      
      if (testResult.dispositivos > 0) {
        console.log('🎉 ¡ÉXITO TOTAL! Push notification enviada');
        console.log('📱 Revisa tu dispositivo/navegador para ver la notificación');
      } else {
        console.log('⚠️ Push enviado pero sin dispositivos alcanzados');
      }
    } else {
      console.log('❌ Error en test push:', testResponse.status);
    }
    
    console.log('🎊 TEST MANUAL COMPLETADO');
    console.log('Si llegaste hasta aquí, el sistema debería estar funcionando');
    
    return subscription;
    
  } catch (error) {
    console.error('💥 ERROR EN TEST MANUAL:', error);
    console.error('Stack:', error.stack);
    throw error;
  }
}

// Ejecutar el test
testPushNotifications()
  .then(subscription => {
    console.log('🏁 Test completado exitosamente');
    console.log('✅ Suscripción final:', subscription ? 'Válida' : 'Inválida');
    
    // Mostrar instrucciones
    console.log('\n📋 PRÓXIMOS PASOS:');
    console.log('1. Cerrar completamente la PWA (todas las pestañas)');
    console.log('2. El sistema debería seguir enviando notificaciones');
    console.log('3. Verificar que aparezcan en la bandeja del sistema');
  })
  .catch(error => {
    console.error('❌ Test falló:', error.message);
  });

console.log('\n💡 INSTRUCCIONES:');
console.log('1. Copia todo este código');
console.log('2. Pégalo en DevTools > Console');
console.log('3. Presiona Enter');
console.log('4. Sigue los logs detallados para ver dónde falla');
