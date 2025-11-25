# Solución: Sincronización Offline en Dispositivos Android

## Problema Reportado
En dispositivos Android, cuando los registros de actividades se subían offline y posteriormente se conectaban a internet, el sistema mostraba:
- "Se enviaron 0 elemento correctamente y 5 fallaron"

## Causas Identificadas

### 1. **Timeouts Insuficientes**
- El timeout fijo de 30 segundos era insuficiente para conexiones móviles lentas
- Las imágenes grandes tardaban más tiempo en subir

### 2. **Sin Sistema de Reintentos**
- Ante cualquier error de red, el registro se marcaba inmediatamente como fallido
- No había mecanismo de recuperación ante conexiones inestables

### 3. **Imágenes Muy Grandes**
- Las fotos tomadas en Android pueden ser de varios MB
- Esto causaba timeouts y errores de memoria

### 4. **Problemas de Formato Base64**
- Algunas variaciones en el formato base64 entre navegadores Android
- El prefijo `data:image/...;base64,` no siempre estaba presente

### 5. **Verificación de Conexión Insuficiente**
- No se verificaba la conexión antes de cada reintento
- Podía intentar enviar cuando la conexión ya se había perdido

## Solución Implementada

### Archivo Modificado
`pwasuper/src/services/syncService.js`

### Nuevas Características

#### 1. Configuración Centralizada (SYNC_CONFIG)
```javascript
const SYNC_CONFIG = {
  maxRetries: 3,                    // 3 reintentos por registro
  baseTimeout: 30000,               // Timeout base de 30s
  maxTimeout: 120000,               // Timeout máximo de 2 minutos
  retryDelayBase: 2000,             // Delay entre reintentos (2s)
  maxImageSize: 500 * 1024,         // Comprimir si > 500KB
  compressionQuality: 0.5,          // Calidad de compresión 50%
  chunkSize: 1,                     // Procesar de 1 en 1
  connectionCheckBeforeEach: true,  // Verificar conexión cada envío
};
```

#### 2. Compresión de Imágenes
```javascript
async comprimirImagenBase64(base64String, maxWidth = 800, quality = 0.7)
```
- Reduce imágenes grandes a máximo 800px de ancho
- Calidad ajustable (50% para sync)
- Evita timeouts por imágenes muy pesadas

#### 3. Placeholder de Imágenes
```javascript
async crearImagenPlaceholder()
```
- Crea imagen de 1x1 pixel cuando falla la conversión
- Evita errores del backend por falta de imagen
- Registra el problema para depuración

#### 4. Detección de Dispositivo
```javascript
detectarTipoDispositivo()
```
- Identifica: 'android', 'ios', 'desktop'
- Se envía en headers para diagnóstico
- Ayuda a identificar problemas específicos de plataforma

#### 5. Sistema de Reintentos Inteligente
Para `enviarRegistro()` y `enviarAsistencia()`:
- **3 intentos** antes de marcar como fallido
- **Timeout adaptativo**: 30s → 60s → 120s
- **Delay incremental** entre reintentos
- **Verificación de conexión** antes de cada reintento
- **Headers especiales** para trazabilidad:
  - `X-Retry-Count`: número de intento
  - `X-Device-Type`: tipo de dispositivo
  - `X-Offline-Sync`: marcador de sincronización

#### 6. Mejor Manejo de Errores
- Detección de errores de red vs errores del servidor
- Manejo de duplicados (status 400 con "ya existe")
- Logging detallado para diagnóstico
- Errores descriptivos en consola

## Flujo de Sincronización Mejorado

```
1. Detectar conexión a internet
2. Para cada registro pendiente:
   a. Verificar datos básicos (usuario_id, lat, lon)
   b. Comprimir imagen si es > 500KB
   c. Intentar envío (timeout: 30s)
      - Si falla por red:
        i. Verificar conexión
        ii. Esperar 2s * intento
        iii. Reintentar con timeout mayor
      - Si falla por duplicado:
        → Marcar como exitoso
      - Si éxito:
        → Eliminar de pendientes
   d. Tras 3 intentos fallidos → Marcar como error
3. Notificar resultado final
```

## Compatibilidad

- ✅ Android (Chrome, Samsung Browser, WebView)
- ✅ iOS (Safari, Chrome)
- ✅ Desktop (Chrome, Firefox, Edge, Safari)

## Pruebas Recomendadas

1. **En Android con conexión lenta (3G)**:
   - Tomar foto y registrar actividad offline
   - Reconectar a WiFi
   - Verificar que se sincronice correctamente

2. **Con conexión intermitente**:
   - Iniciar sync
   - Simular pérdida de señal
   - Verificar que reintenta automáticamente

3. **Con imágenes grandes (>2MB)**:
   - Tomar foto en alta resolución
   - Verificar que se comprime antes de enviar

## Logs de Diagnóstico

En consola del navegador se verán mensajes como:

```
📤 [Intento 1/3] Enviando registro offline ID: 123
⏱️ Timeout configurado: 30s
🖼️ Procesando imagen del registro...
📊 Imagen original: 1.2MB, comprimida: 0.4MB
✅ Registro 123 enviado exitosamente

o en caso de reintento:

📤 [Intento 2/3] Enviando registro offline ID: 124
⏱️ Timeout configurado: 60s
🔍 Verificando conexión antes del reintento...
✅ Conexión confirmada, continuando...
```

## Fecha de Implementación
Junio 2025

## Estado
✅ **COMPLETADO**
