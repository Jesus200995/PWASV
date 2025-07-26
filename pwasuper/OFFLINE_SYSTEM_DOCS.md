# Sistema Offline/Online PWA Super

## 📱 Funcionalidad Implementada

### 1. Almacenamiento Offline
- **IndexedDB**: Utilizado para guardar registros complejos (fotos, ubicación, datos de usuario)
- **LocalStorage**: Para datos de sesión y estado de asistencia
- **Fotos**: Convertidas a Base64 para almacenamiento local

### 2. Detección de Conectividad
- Escucha eventos `online`/`offline` del navegador
- Verificación activa de conexión a internet
- Indicadores visuales de estado de conectividad

### 3. Sincronización Automática
- **Al recuperar conexión**: Envío automático de todos los datos pendientes
- **Reintentos inteligentes**: No duplica registros ya existentes
- **Notificaciones**: Informa al usuario sobre el progreso de sincronización

### 4. Interfaz de Usuario
- **Banner superior**: Muestra estado de conectividad y registros pendientes
- **Modal informativo**: Detalles de sincronización y progreso
- **Indicadores visuales**: Registros offline marcados en el historial

## 🔧 Componentes Principales

### OfflineService (`src/services/offlineService.js`)
```javascript
// Funciones principales:
- guardarRegistroOffline()     // Guarda registros generales
- guardarAsistenciaOffline()   // Guarda entrada/salida
- obtenerRegistrosPendientes() // Lista registros por enviar
- contarPendientes()          // Cuenta elementos pendientes
```

### SyncService (`src/services/syncService.js`)
```javascript
// Funciones principales:
- sincronizarTodo()           // Envía todos los datos pendientes
- addListener()               // Escucha cambios de conectividad
- sincronizarManual()         // Sincronización manual por el usuario
```

### ConnectivityStatus (`src/components/ConnectivityStatus.vue`)
```vue
<!-- Características -->
- Banner superior responsivo
- Modal con progreso de sincronización
- Notificación flotante simple
- Botón de sincronización manual
```

## 📱 Flujo de Uso

### Modo Online (Con Conexión)
1. Usuario completa formulario
2. Se verifica conexión
3. Datos se envían directamente al servidor
4. Respuesta inmediata al usuario

### Modo Offline (Sin Conexión)
1. Usuario completa formulario
2. Se detecta falta de conexión
3. Datos se guardan en IndexedDB
4. Se muestra mensaje: "Guardado offline, se enviará al recuperar conexión"
5. Banner indica registros pendientes

### Recuperación de Conexión
1. Evento `online` detectado
2. SyncService inicia sincronización automática
3. Banner muestra progreso
4. Registros exitosos se eliminan del almacenamiento local
5. Usuario recibe confirmación de sincronización

## 🛠️ Archivos Modificados/Creados

### Nuevos Archivos
- `src/services/offlineService.js` - Gestión de almacenamiento offline
- `src/services/syncService.js` - Sincronización automática
- `public/sw.js` - Service Worker para PWA
- `public/offline.html` - Página offline
- `public/manifest.json` - Manifiesto PWA

### Archivos Modificados
- `src/components/ConnectivityStatus.vue` - Reemplazado completamente
- `src/views/Home.vue` - Lógica offline en registros y asistencias
- `src/main.js` - Registro de Service Worker
- `index.html` - Meta tags y referencias PWA

## 🔄 Mensajes al Usuario

### Estados de Conectividad
- **Sin conexión**: "Sin conexión" (banner rojo)
- **Sincronizando**: "Sincronizando..." (banner azul)
- **Pendientes**: "X registros pendientes" (banner amarillo)
- **Conectado**: "Conectado" (banner verde - se oculta automáticamente)

### Mensajes de Registro
- **Offline**: "Registro guardado offline! Se enviará automáticamente cuando recuperes la conexión."
- **Online**: "¡Registro enviado y guardado correctamente!"
- **Sincronización**: "Se enviaron X registros correctamente"

## 📊 Indicadores Visuales

### Banner Superior
- 🔴 **Rojo**: Sin conexión + registros pendientes
- 🔵 **Azul**: Sincronizando en progreso
- 🟡 **Amarillo**: Registros pendientes (con conexión)
- 🟢 **Verde**: Todo sincronizado (se oculta automáticamente)

### Historial
- **Registros offline**: Borde naranja y texto "⏳ Se enviará al recuperar conexión"
- **Registros online**: Apariencia normal

### Modal de Progreso
- Barra de progreso durante sincronización
- Contador de exitosos/fallidos
- Botón de sincronización manual

## 🚀 Service Worker

### Funcionalidades
- **Cache**: Archivos estáticos para funcionamiento offline
- **Fetch**: Intercepta solicitudes de red
- **Push**: Notificaciones (preparado para futuro)
- **Sync**: Sincronización en segundo plano

### Archivos Cacheados
- Página principal
- CSS y JavaScript esenciales
- Página offline personalizada

## 🔒 Consideraciones de Seguridad

### Datos Locales
- **Tiempo de vida**: Se limpian automáticamente tras envío exitoso
- **Validación**: Verificación de integridad antes del envío
- **Errores**: Reintentos inteligentes sin duplicar

### Sincronización
- **No duplicados**: Detecta registros existentes en el servidor
- **Timeouts**: 30 segundos por solicitud
- **Reintentos**: Solo para errores de conexión, no errores de servidor

## 📱 PWA Features

### Manifiesto
- Instalable como app nativa
- Iconos personalizados
- Atajos rápidos para entrada/salida
- Modo standalone

### Service Worker
- Funcionamiento offline
- Cache inteligente
- Actualizaciones automáticas

## 🧪 Testing

### Casos de Prueba
1. **Registro offline**: Desconectar red, completar registro, verificar almacenamiento
2. **Sincronización**: Reconectar y verificar envío automático
3. **Duplicados**: Verificar que no se envían registros duplicados
4. **UI States**: Comprobar todos los estados visuales
5. **Persistencia**: Verificar que datos offline persisten tras cerrar app

### Comandos útiles
```javascript
// En DevTools Console:
localStorage.clear()           // Limpiar datos locales
indexedDB.deleteDatabase('PWAOfflineDB') // Limpiar IndexedDB
navigator.serviceWorker.unregister() // Desregistrar SW
```

## 📞 Soporte

### Logs de Debug
- Todos los servicios incluyen logs detallados
- Prefijos emoji para fácil identificación
- Niveles: ✅ Éxito, ❌ Error, 🔄 Proceso, ℹ️ Info

### Navegadores Soportados
- Chrome/Edge: ✅ Completo
- Firefox: ✅ Completo  
- Safari: ✅ Completo (con limitaciones PWA)
- Opera: ✅ Completo
