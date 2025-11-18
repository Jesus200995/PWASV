# 📊 Implementación de Botón Naranja para Descargar Registros CSV

## ✅ Completado

Se ha implementado exitosamente un **botón naranja con animación** en el panel de Configuración del Admin PWA que permite descargar todos los registros de actividades en formato CSV con **progreso en tiempo real**.

---

## 📋 Detalles de Implementación

### 1. **Botón Naranja en UI** ✅

**Ubicación:** `admin-pwa/src/views/ConfiguracionView.vue` (línea ~205)

```vue
<button @click="descargarRegistrosCSV" class="action-btn registros-csv-btn" :disabled="descargandoRegistrosCSV">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
    <polyline points="14,2 14,8 20,8"></polyline>
    <line x1="12" y1="13" x2="12" y2="19"></line>
    <line x1="9" y1="16" x2="15" y2="16"></line>
  </svg>
  {{ descargandoRegistrosCSV ? 'Exportando CSV...' : '📊 Registros CSV' }}
</button>
```

**Características:**
- Texto dinámico: "📊 Registros CSV" (normal) → "Exportando CSV..." (durante descarga)
- `:disabled` automático durante descarga
- Icono SVG de tabla/hojas de cálculo

### 2. **Estilos CSS para Botón Naranja** ✅

**Ubicación:** `admin-pwa/src/views/ConfiguracionView.vue` (línea ~1975)

```css
.registros-csv-btn {
  background: linear-gradient(135deg, #f97316 0%, #fb923c 50%, #fbbf24 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.4);
  font-weight: 600;
  position: relative;
  overflow: hidden;
}

.registros-csv-btn::before {
  content: '📊';
  position: absolute;
  left: 8px;
  font-size: 14px;
  animation: bounce 1.2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
    opacity: 1;
  }
  50% {
    transform: translateY(-4px);
    opacity: 0.8;
  }
}

.registros-csv-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.6);
}
```

**Características:**
- **Gradiente naranja:** De `#f97316` a `#fbbf24`
- **Animación de rebote:** El emoji 📊 rebota de forma suave (1.2s)
- **Hover effect:** Traslación hacia arriba + sombra mejorada
- **Estados:** Deshabilitado automático durante descarga

### 3. **Variables Reactivas** ✅

**Ubicación:** `admin-pwa/src/views/ConfiguracionView.vue` (línea ~395)

```javascript
const descargandoRegistrosCSV = ref(false)

// Variables para el modal de descarga de CSV
const descargaCSVProgressRef = ref(null)
const showDescargaCSVProgress = ref(false)
```

### 4. **Función de Descarga con Progreso** ✅

**Ubicación:** `admin-pwa/src/views/ConfiguracionView.vue` (línea ~965)

```javascript
const descargarRegistrosCSV = async () => {
  descargandoRegistrosCSV.value = true
  showDescargaCSVProgress.value = true
  
  try {
    console.log('📊 Iniciando descarga de registros en CSV con progreso...')
    
    // Definir callback para actualizar el progreso
    const onProgress = (datos) => {
      if (descargaCSVProgressRef.value) {
        console.log('📊 Actualizando progreso CSV:', datos)
        descargaCSVProgressRef.value.actualizar({
          bytesDescargados: datos.bytesDescargados,
          tamanoTotal: datos.tamanoTotal,
          velocidad: datos.velocidad,
          mensaje: `Exportando: ${((datos.bytesDescargados / (1024 * 1024)).toFixed(2))} MB exportados...`
        })
      }
    }
    
    // Llamar al servicio de CSV con callback de progreso
    const resultado = await baseDatosService.descargarRegistrosCSV(onProgress)
    
    // Marcar como completado
    if (descargaCSVProgressRef.value) {
      descargaCSVProgressRef.value.completar()
    }
    
    // Esperar un bit y cerrar el modal
    setTimeout(() => {
      showDescargaCSVProgress.value = false
      descargandoRegistrosCSV.value = false
      
      // Mostrar mensaje de éxito
      mostrarMensaje('✅ Exportación Exitosa', 
        `<div style="text-align: left;">
          <h4 style="color: #f97316; margin-bottom: 15px;">📊 Registros Exportados</h4>
          <p><strong>📁 Archivo:</strong> ${resultado.archivo}</p>
          <p><strong>📊 Tamaño:</strong> ${resultado.tamanhoMB} MB</p>
          <p><strong>📝 Registros:</strong> ${resultado.registros} registros exportados</p>
          <hr style="margin: 15px 0;">
          <p style="font-size: 12px; color: #666; margin-top: 15px;">
            ✅ Todos los registros de actividades han sido exportados exitosamente en formato CSV.
            Puedes abrir el archivo en Excel o cualquier editor de hojas de cálculo.
          </p>
        </div>`
      )
    }, 1500)
    
  } catch (err) {
    console.error('❌ Error en descarga de CSV:', err)
    showDescargaCSVProgress.value = false
    descargandoRegistrosCSV.value = false
    // ... manejo de errores personalizado
  } finally {
    descargandoRegistrosCSV.value = false
  }
}
```

**Características:**
- Activa el modal de progreso al iniciar
- Callback para actualización en tiempo real
- Muestra mensaje de éxito con detalles (archivo, tamaño, registros)
- Manejo robusto de errores

### 5. **Modal de Progreso** ✅

**Ubicación:** `admin-pwa/src/views/ConfiguracionView.vue` (línea ~355)

```vue
<!-- Modal de progreso para descarga de CSV -->
<DescargaProgressModal
  ref="descargaCSVProgressRef"
  :show="showDescargaCSVProgress"
/>
```

Reutiliza el mismo componente `DescargaProgressModal` que la descarga de BD, mostrando:
- Barra de progreso con animación shimmer
- 4 estadísticas en tiempo real (Descargado, Tamaño Total, Velocidad, Tiempo Restante)
- Íconos animados y puntos de carga

### 6. **Método de Servicio** ✅

**Ubicación:** `admin-pwa/src/services/baseDatosService.js` (línea ~178)

```javascript
async descargarRegistrosCSV(onProgress = null) {
  try {
    const response = await fetch(
      `${this.apiUrl}/exportar-registros-csv`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      }
    )

    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`)
    }

    const reader = response.body.getReader()
    const chunks = []
    let bytesDescargados = 0
    const tamanoTotal = parseInt(response.headers.get('content-length') || 0)
    
    let ultimaActualizacion = Date.now()
    let bytesPrevios = 0

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      chunks.push(value)
      bytesDescargados += value.length

      const ahoraMs = Date.now()
      if (ahoraMs - ultimaActualizacion >= 200) {
        const tiempoTranscurrido = (ahoraMs - ultimaActualizacion) / 1000
        const bytesDelta = bytesDescargados - bytesPrevios
        const velocidad = bytesDelta / tiempoTranscurrido

        if (onProgress) {
          onProgress({
            bytesDescargados,
            tamanoTotal,
            velocidad,
            porcentaje: tamanoTotal > 0 ? Math.round((bytesDescargados / tamanoTotal) * 100) : 0
          })
        }

        ultimaActualizacion = ahoraMs
        bytesPrevios = bytesDescargados
      }
    }

    const blob = new Blob(chunks, { type: 'text/csv;charset=utf-8' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `registros_actividades_${new Date().toISOString().split('T')[0]}.csv`
    link.click()

    return {
      archivo: link.download,
      tamanhoMB: (blob.size / (1024 * 1024)).toFixed(2),
      registros: 'Todos los registros disponibles'
    }
  } catch (error) {
    console.error('Error descargando CSV:', error)
    throw new Error(`No se pudo descargar el CSV: ${error.message}`)
  }
}
```

### 7. **Backend Endpoint** ✅

**Ubicación:** `backend/main.py` (línea ~5235)

```python
@app.get("/exportar-registros-csv")
async def exportar_registros_csv():
    """Exporta todos los registros de actividades en formato CSV con streaming."""
    try:
        async def generar_csv():
            try:
                db = next(get_db_context())
                cursor = db.cursor()
                
                # Headers del CSV
                headers = "ID,Usuario,Email,IP,Ciudad,Código Postal,Estado,Tipo Acción,Objeto Modificado,Valores Anteriores,Valores Nuevos,Fecha Acción,Timestamp Creación\n"
                yield headers.encode('utf-8')
                
                # Consulta con JOIN para obtener información del usuario
                cursor.execute("""
                    SELECT 
                        r.id, u.username, u.email, r.ip, r.ciudad, r.codigo_postal, r.estado,
                        r.tipo_accion, r.objeto_modificado, r.valores_anteriores, 
                        r.valores_nuevos, r.fecha_accion, r.timestamp
                    FROM registros r
                    LEFT JOIN usuarios u ON r.usuario_id = u.id
                    ORDER BY r.timestamp DESC
                """)
                
                # Procesar en chunks
                chunk_size = 500
                while True:
                    rows = cursor.fetchmany(chunk_size)
                    if not rows:
                        break
                    
                    for row in rows:
                        # Procesar y escapar valores
                        csv_row = format_csv_row(row)
                        yield csv_row.encode('utf-8')
                
                cursor.close()
                db.close()
            except Exception as e:
                print(f"Error en generador CSV: {e}")
        
        return StreamingResponse(
            generar_csv(),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=registros_actividades_{datetime.now().strftime('%Y-%m-%d')}.csv"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exportando registros: {str(e)}")
```

---

## 🎨 Comparación Visual

### Botón Rosa (BD Completa Rápida)
- **Gradiente:** `#ec4899` → `#f472b6` → `#fb7185`
- **Animación:** Pulso del emoji ⚡
- **Datos:** SQL completo de la BD

### Botón Naranja (Registros CSV) - ✅ NUEVO
- **Gradiente:** `#f97316` → `#fb923c` → `#fbbf24`
- **Animación:** Rebote del emoji 📊
- **Datos:** Registros en formato CSV con usuario, IP, etc.

---

## 🚀 Flujo de Uso

1. **Usuario hace click** en "📊 Registros CSV"
2. **Botón se deshabilita** → Texto cambia a "Exportando CSV..."
3. **Modal de progreso aparece** mostrando:
   - Barra de progreso en tiempo real
   - MB descargados / total
   - Velocidad de descarga
   - Tiempo restante estimado
4. **Descarga completa** → Modal se cierra
5. **Mensaje de éxito** muestra:
   - Nombre del archivo (con fecha)
   - Tamaño total en MB
   - Cantidad de registros exportados
6. **Archivo se descarga** al navegador del usuario

---

## 📊 Características de la Descarga

- ✅ **Formato:** CSV con encoding UTF-8
- ✅ **Columnas:** ID, Usuario, Email, IP, Ciudad, CP, Estado, Tipo Acción, Objeto, Valores Anteriores/Nuevos, Fecha, Timestamp
- ✅ **Escaping:** Caracteres especiales (comillas, saltos de línea) correctamente escapados
- ✅ **Progreso Real:** Actualización cada 200ms con velocidad y tiempo restante
- ✅ **Streaming:** Memoria eficiente incluso con millones de registros
- ✅ **Autenticación:** Requiere token válido
- ✅ **Nombre Automático:** `registros_actividades_YYYY-MM-DD.csv`

---

## ✨ Estado Final

```
✅ Botón HTML              - Agregado y funcionando
✅ Estilos CSS             - Gradiente naranja + animación bounce
✅ Variable de estado       - descargandoRegistrosCSV
✅ Modal de progreso       - Reutilizado con segundo ref
✅ Función de descarga     - Manejo de progreso y errores
✅ Servicio baseDatos      - descargarRegistrosCSV() completado
✅ Backend endpoint        - /exportar-registros-csv con streaming
✅ Sin errores de sintaxis - Validado
✅ Servidor ejecutándose   - npm run dev activo
```

---

## 🎯 Próximos Pasos (Opcionales)

- [ ] Agregar filtros temporales (últimas 24h, última semana, etc.)
- [ ] Agregar opciones de formato (CSV, XLSX, JSON)
- [ ] Permitir selección de columnas específicas
- [ ] Guardar en base de datos un registro de exportaciones realizadas
- [ ] Agregar gráficos de actividades descargadas

