🔧 INSTRUCCIONES PARA HACER FUNCIONAR LA ELIMINACIÓN DE IMÁGENES
═══════════════════════════════════════════════════════════════════

⚠️ IMPORTANTE: El servidor backend DEBE estar corriendo para que funcione

PASO 1: VERIFICAR QUE EL ENDPOINT EXISTE
═════════════════════════════════════════

✅ El endpoint está agregado en: backend/main.py (línea 4895)
✅ Se modificó la vista: admin-pwa/src/views/ConfiguracionView.vue
✅ Se creó el servicio: admin-pwa/src/services/imagenesService.js
✅ Se creó el componente: admin-pwa/src/components/ProgressModal.vue

PASO 2: REINICIAR EL BACKEND (MUY IMPORTANTE)
═════════════════════════════════════════════

Opción A - Línea de comando (PowerShell):
──────────────────────────────────────────

1. Abre PowerShell en Windows
2. Navega a la carpeta del backend:
   
   cd "C:\Users\Admin_1\Pictures\PWA\PWASV\backend"

3. Verifica si hay un proceso Python corriendo:
   
   Get-Process python -ErrorAction SilentlyContinue

4. Si hay uno ejecutando, termínalo:
   
   Stop-Process -Name python -Force

5. Espera 2-3 segundos

6. Inicia el servidor:
   
   python main.py

   ✅ Deberías ver: "INFO:     Uvicorn running on http://0.0.0.0:8000"

7. Mantén la terminal abierta mientras uses la aplicación

Opción B - Con entorno virtual:
────────────────────────────────

Si tienes un entorno virtual (venv):

1. Activa el entorno:
   
   venv\Scripts\Activate

2. Navega al backend:
   
   cd backend

3. Inicia el servidor:
   
   python main.py

PASO 3: VERIFICAR QUE EL SERVIDOR ESTÁ CORRIENDO
═════════════════════════════════════════════════

Abre en tu navegador y ve a:

  https://apipwa.sembrandodatos.com/health

O si es local:

  http://localhost:8000/health

Deberías ver una respuesta JSON como:
{
  "status": "healthy",
  "database": "connected",
  "message": "API y base de datos funcionando correctamente"
}

PASO 4: RECARGAR LA APLICACIÓN FRONTEND
════════════════════════════════════════

1. Abre la aplicación web: https://apipwa.sembrandodatos.com

2. Recarga la página: F5 (o Ctrl+F5 para limpiar cache)

3. Inicia sesión como administrador si no lo estás

PASO 5: PROBAR LA ELIMINACIÓN DE IMÁGENES
══════════════════════════════════════════

1. Ve a: CONFIGURACIÓN DEL SISTEMA

2. Busca la sección: ACCIONES

3. Haz clic en: "Eliminar Imágenes" (botón rosa)

4. Sigue el flujo:
   ✓ Lee la advertencia
   ✓ Haz clic "Aceptar"
   ✓ Escribe "ELIMINAR IMÁGENES" en el prompt
   ✓ Observa el progreso
   ✓ Verifica el resultado

SOLUCIÓN DE PROBLEMAS
═════════════════════

❌ ERROR: "Failed to load resource: net::ERR_FAILED"
─────────────────────────────────────────────────

SOLUCIÓN:
1. El servidor backend NO está corriendo
2. O el endpoint no está disponible

CÓMO ARREGLARLO:
1. Verifica que Python está corriendo (PASO 2)
2. Reinicia el servidor
3. Espera a ver el mensaje de "Uvicorn running"
4. Recarga la página del navegador (F5)

❌ ERROR: "Sesión expirada. Por favor inicia sesión nuevamente."
───────────────────────────────────────────────────────────────

SOLUCIÓN:
1. Tu token JWT expiró
2. O no tienes permiso de administrador

CÓMO ARREGLARLO:
1. Haz logout del sistema
2. Vuelve a iniciar sesión como administrador
3. Intenta de nuevo

❌ ERROR: "Error de conexión. Verifica tu conexión a internet."
──────────────────────────────────────────────────────────────

SOLUCIÓN:
1. El servidor no responde

CÓMO ARREGLARLO:
1. Verifica que apipwa.sembrandodatos.com está disponible
2. O verifica que localhost:8000 está disponible (si es desarrollo)
3. Reinicia el servidor backend
4. Recarga la página

VERIFICAR EN LA CONSOLA DEL NAVEGADOR (F12)
═════════════════════════════════════════════

1. Abre las herramientas de desarrollador: F12

2. Ve a la pestaña "CONSOLE"

3. Cuando hagas clic en "Eliminar Imágenes", verás logs como:

   📸 Iniciando eliminación de imágenes...
   🔗 URL del endpoint: https://apipwa.sembrandodatos.com/imagenes/eliminar-todas
   🔐 Token presente: true
   📞 Llamando al servicio...

4. Si ves errores, lee el mensaje exacto para diagnosticar

VERIFICAR EN TERMINAL DEL BACKEND
══════════════════════════════════

Cuando hagas clic en "Eliminar Imágenes", en la terminal de Python verás:

   🗑️ INICIANDO ELIMINACIÓN DE TODAS LAS IMÁGENES...
   📸 Se encontraron 5 fotos en registros
   📸 Se encontraron 3 fotos en asistencias
   ✅ ELIMINACIÓN COMPLETADA:
      📸 Fotos en BD limpiadas: 8
      🗑️ Archivos eliminados: 8
      ⚠️ Archivos no encontrados: 0
      ❌ Errores: 0

CAMBIOS RECIENTES (29 Octubre 2025)
═══════════════════════════════════

✅ CORREGIDO: Modal de confirmación ahora muestra texto plano (sin HTML)
✅ MEJORADO: Mejor manejo de errores en el servicio
✅ MEJORADO: Mensajes de error más descriptivos
✅ AGREGADO: Logging detallado en consola
✅ AGREGADO: Timeout de 60 segundos para la eliminación
✅ AGREGADO: Tipo "danger" en modal de confirmación

RESUMEN DEL FLUJO FUNCIONAL
═══════════════════════════

1. Usuario hace clic en "Eliminar Imágenes"
   ↓
2. Modal de confirmación (tipo "danger") aparece con texto limpio
   ↓
3. Usuario hace clic "Aceptar"
   ↓
4. Prompt pide escribir "ELIMINAR IMÁGENES"
   ↓
5. Frontend llama a imagenesService.eliminarTodasLasImagenes()
   ↓
6. Servicio hace DELETE a: /imagenes/eliminar-todas
   ↓
7. Backend:
   - Obtiene todas las fotos de registros
   - Obtiene todas las fotos de asistencias
   - Elimina archivos del servidor
   - Actualiza BD (URLs → NULL)
   - Retorna estadísticas
   ↓
8. Modal de progreso muestra resultado
   ↓
9. Usuario ve el resumen con total de imágenes eliminadas
   ↓
10. Haz clic "Aceptar" para cerrar

═══════════════════════════════════════════════════════════════════

🎯 CHECKLIST ANTES DE USAR
════════════════════════════

☑️ Backend reiniciado (python main.py corriendo)
☑️ Base de datos conectada
☑️ Token JWT válido (estás logueado como admin)
☑️ Tienes permisos de administrador
☑️ Hay imágenes para eliminar
☑️ Conexión a internet funciona
☑️ Frontend cargado correctamente

═══════════════════════════════════════════════════════════════════

¡LISTO! Ahora deberías poder eliminar imágenes correctamente. 🚀
