# 🔍 GUÍA DE DEBUGGING - BUSCADOR DE REGISTROS

## 🧪 Cómo Probar la Búsqueda

### Paso 1: Abrir la Consola del Navegador
1. Ir a `admin.sembrandodatos.com` (o `localhost:5173`)
2. Presionar `F12` para abrir Developer Tools
3. Ir a la pestaña **Console**
4. Ir a la sección **Registros**

### Paso 2: Realizar una Búsqueda

Escribe en el campo de búsqueda una **CURP completa o parcial**, por ejemplo:
```
ROCR820619MSLJSB05
```

### Paso 3: Ver los Logs en Consola

Deberías ver logs como estos:

```
⏳ Iniciando búsqueda en 500ms para: "ROCR820619MSLJSB05"

🚀 Ejecutando búsqueda para: "ROCR820619MSLJSB05"

🔍 ===== INICIANDO BÚSQUEDA =====
📝 Término de búsqueda: "ROCR820619MSLJSB05"
📊 Registros actuales en memoria: 200

   📋 Búsqueda por nombre: 0 resultados
   📋 Búsqueda por correo: 0 resultados
   📋 Búsqueda por CURP: 1 resultados

✅ Total usuarios únicos encontrados: 1
   👤 ID: 463 | Nombre: Rosa Cruz | CURP: ROCR820619MSLJSB05

📥 Cargando registros de 1 usuario(s)...
   ⬇️ Cargando registros del usuario 463 (Rosa Cruz)...
      🔍 Solicitando registros del usuario 463 al backend...
      📦 Backend respondió: 25 registros de 25 totales
      🔄 Enriqueciendo registros con información de usuarios...
      📊 Registros nuevos: 25 | Ya existentes: 0
      ✅ Total registros en memoria ahora: 225
      📋 Ejemplo de registro con CURP: Rosa Cruz - ROCR820619MSLJSB05

📊 Total de registros en memoria después de búsqueda: 225
===== FIN DE BÚSQUEDA =====

🔎 Aplicando filtro local...

🔍 ===== INICIANDO FILTRADO =====
📊 Total de registros en memoria: 225
🔎 Aplicando filtro de búsqueda: "rocr820619msljsb05"
   ✅ Registros después de búsqueda: 25 (filtrados: 200)
   📋 Registros encontrados:
      1. Rosa Cruz (ROCR820619MSLJSB05) - Visita domiciliaria zona norte
      2. Rosa Cruz (ROCR820619MSLJSB05) - Reunión con vecinos
      ... (hasta 5 registros)

📊 RESULTADO FINAL DEL FILTRADO:
   🗂️ Registros mostrados: 25
   🔢 Usuarios únicos: 1
===== FIN DE FILTRADO =====

✅ Búsqueda completada. Registros filtrados: 25
```

---

## ❌ Problemas Comunes y Soluciones

### Problema 1: "No hay registros"

**Síntomas:**
```
📋 Búsqueda por CURP: 0 resultados
❌ No se encontraron usuarios con ese criterio
```

**Causas posibles:**
1. La CURP no existe en la base de datos
2. La CURP está mal escrita
3. El backend no está respondiendo

**Solución:**
Prueba con otra CURP que sepas que existe. Verifica en la sección de Usuarios primero.

---

### Problema 2: "Usuario encontrado pero sin registros"

**Síntomas:**
```
✅ Total usuarios únicos encontrados: 1
📥 Cargando registros de 1 usuario(s)...
📦 Backend respondió: 0 registros de 0 totales
⚠️ No se encontraron registros para el usuario 463
```

**Causa:**
El usuario existe pero no tiene registros de actividades en la base de datos.

**Solución:**
Esto es normal. El usuario no ha registrado actividades aún.

---

### Problema 3: "Error al cargar registros"

**Síntomas:**
```
❌ Error cargando registros del usuario 463:
📛 Status: 500 | Message: Error de base de datos
```

**Causas posibles:**
1. Problema de conexión con el backend
2. Error en la base de datos
3. Timeout

**Solución:**
1. Verificar que el backend esté corriendo
2. Revisar los logs del backend (main.py)
3. Intentar de nuevo después de unos segundos

---

### Problema 4: "Registros cargados pero no se muestran"

**Síntomas:**
```
✅ Total registros en memoria ahora: 225
📊 RESULTADO FINAL DEL FILTRADO:
   🗂️ Registros mostrados: 0
⚠️ No se encontraron registros para "ROCR820619MSLJSB05"
```

**Causa:**
El filtro local no está encontrando coincidencias. Posiblemente los registros no tienen la información del usuario enriquecida.

**Solución:**
Verifica en los logs si aparece:
```
📋 Ejemplo de registro con CURP: Rosa Cruz - ROCR820619MSLJSB05
```

Si no aparece, el problema está en `usuariosService.enriquecerRegistrosConUsuarios()`.

---

## 🔬 Tests Detallados

### Test 1: Búsqueda por CURP Completa

**Input:**
```
ROCR820619MSLJSB05
```

**Resultado esperado:**
- ✅ Encuentra 1 usuario
- ✅ Carga sus registros (X registros)
- ✅ Muestra X registros en la tabla

---

### Test 2: Búsqueda por CURP Parcial

**Input:**
```
ROCR82
```

**Resultado esperado:**
- ✅ Encuentra todos los usuarios cuya CURP contenga "ROCR82"
- ✅ Carga registros de todos
- ✅ Muestra todos los registros en la tabla

---

### Test 3: Búsqueda por Nombre

**Input:**
```
Rosa
```

**Resultado esperado:**
- ✅ Encuentra todos los usuarios con "Rosa" en el nombre
- ✅ Carga registros de todos
- ✅ Muestra todos los registros

---

### Test 4: Búsqueda por Correo

**Input:**
```
rosa@
```

**Resultado esperado:**
- ✅ Encuentra usuarios con ese correo
- ✅ Carga sus registros
- ✅ Muestra los registros

---

### Test 5: Búsqueda Corta (< 3 caracteres)

**Input:**
```
RO
```

**Resultado esperado:**
```
📝 Búsqueda corta (2 caracteres), solo filtro local
```
- ✅ NO busca en el backend
- ✅ Solo filtra en los registros ya cargados

---

## 📊 Verificar Estado de los Datos

### Comando para ver registros en memoria:
Abre la consola y ejecuta:
```javascript
console.table(registros.value.slice(0, 5).map(r => ({
  id: r.id,
  usuario: r.usuario?.nombre_completo,
  curp: r.usuario?.curp,
  descripcion: r.descripcion?.substring(0, 30)
})))
```

### Comando para ver registros filtrados:
```javascript
console.table(registrosFiltrados.value.slice(0, 5).map(r => ({
  id: r.id,
  usuario: r.usuario?.nombre_completo,
  curp: r.usuario?.curp,
  descripcion: r.descripcion?.substring(0, 30)
})))
```

### Comando para ver si un usuario específico está en memoria:
```javascript
const usuarioId = 463
const registrosDeUsuario = registros.value.filter(r => r.usuario_id === usuarioId)
console.log(`Registros del usuario ${usuarioId}: ${registrosDeUsuario.length}`)
console.table(registrosDeUsuario.map(r => ({
  id: r.id,
  descripcion: r.descripcion,
  fecha: r.fecha_hora
})))
```

---

## 🐛 Debugging Avanzado

### Ver todas las variables de estado:
```javascript
console.log({
  totalRegistros: registros.value.length,
  registrosFiltrados: registrosFiltrados.value.length,
  searchTerm: searchTerm.value,
  buscandoUsuario: buscandoUsuario.value,
  filtroUsuario: filtroUsuario.value
})
```

### Forzar recarga de registros de un usuario:
```javascript
await cargarRegistrosParaUsuario(463)
```

### Limpiar todo y empezar de nuevo:
```javascript
searchTerm.value = ''
registros.value = []
registrosFiltrados.value = []
await cargarRegistros()
```

---

## ✅ Checklist de Verificación

Antes de reportar un error, verifica:

- [ ] El backend está corriendo (`http://localhost:8000` o producción)
- [ ] El admin-pwa está corriendo (`http://localhost:5173` o producción)
- [ ] La consola del navegador está abierta (F12)
- [ ] El término de búsqueda tiene al menos 3 caracteres
- [ ] El usuario que buscas existe en la base de datos
- [ ] El usuario tiene registros de actividades
- [ ] No hay errores en rojo en la consola
- [ ] El token de autenticación es válido

---

## 🔗 Endpoints del Backend a Verificar

### 1. Búsqueda de usuarios:
```bash
curl -X GET "http://localhost:8000/usuarios/buscar?curp=ROCR820619" \
  -H "Authorization: Bearer TU_TOKEN"
```

### 2. Registros de un usuario:
```bash
curl -X GET "http://localhost:8000/admin/registros?usuario_id=463&page_size=5000" \
  -H "Authorization: Bearer TU_TOKEN"
```

### 3. Info de un usuario:
```bash
curl -X GET "http://localhost:8000/usuarios/463" \
  -H "Authorization: Bearer TU_TOKEN"
```

---

## 📝 Información para Reportar

Si encuentras un problema, incluye:

1. **Término de búsqueda usado:** (ej: ROCR820619MSLJSB05)
2. **Logs completos de la consola** (copiar todo el output)
3. **Screenshot de la pantalla**
4. **Respuesta de los endpoints** (si es posible)
5. **Estado de las variables** (ejecutar los comandos de debugging)

---

¡Con estos logs detallados podemos diagnosticar exactamente qué está pasando! 🚀
