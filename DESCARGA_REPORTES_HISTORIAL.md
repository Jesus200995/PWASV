# Implementación de Descarga de Reportes desde Historial

## Resumen
Se implementó la funcionalidad para que los usuarios puedan volver a descargar reportes PDF previamente generados desde el historial.

## Cambios Realizados

### Backend (main.py)

1. **Endpoint `/reportes/guardar`** - Modificado para recibir y almacenar el PDF en base64:
   - Nuevo parámetro `pdf_base64`: recibe el PDF completo codificado
   - Se guarda en la nueva columna de la tabla

2. **Endpoint `/reportes/historial/{usuario_id}`** - Modificado para indicar si tiene PDF:
   - Nuevo campo `tiene_pdf`: boolean que indica si el reporte tiene PDF disponible

3. **Nuevo endpoint `/reportes/descargar/{reporte_id}`**:
   - Obtiene el PDF guardado de un reporte específico
   - Retorna el PDF en base64 para su descarga

### Frontend (Reportes.vue)

1. **UI del Historial**:
   - Iconos SVG diferentes para PDF y CSV
   - Botón de descarga azul para reportes con PDF disponible
   - Indicador de "no disponible" para reportes sin PDF
   - Animación de loading durante la descarga

2. **Nuevo método `descargarReporteHistorial(reporte)`**:
   - Obtiene el PDF del servidor
   - Convierte base64 a blob
   - Descarga automáticamente el archivo

3. **Generación de PDF**:
   - El método `generarPDF()` ahora retorna el PDF en base64
   - Se envía el PDF al guardar el reporte en la BD

### Base de Datos

Nueva columna en la tabla `reportes_generados`:
- `pdf_base64` (TEXT): Almacena el PDF completo en formato base64

## Instrucciones de Despliegue

### 1. Actualizar la Base de Datos

Ejecutar el script en el servidor de producción:

```bash
# En el servidor (VPS)
cd /ruta/al/backend
python agregar_columna_pdf_reportes.py --local
```

O ejecutar directamente este SQL:

```sql
ALTER TABLE reportes_generados ADD COLUMN IF NOT EXISTS pdf_base64 TEXT;
```

### 2. Actualizar el Backend

Copiar el archivo `main.py` actualizado al servidor y reiniciar el servicio.

### 3. Actualizar el Frontend

Compilar y desplegar la PWA con los cambios en `Reportes.vue`.

## Consideraciones

1. **Tamaño del PDF**: Los PDFs se almacenan completos en base64, lo que puede ocupar espacio considerable. Un PDF típico de 2-3 páginas ocupa ~100-300KB en base64.

2. **Reportes Antiguos**: Los reportes generados antes de esta actualización no tendrán el PDF disponible (mostrarán el indicador de "no disponible").

3. **Solo PDF**: Los reportes CSV no se guardan para descarga posterior, solo se generan en el momento.

## Fecha de Implementación
26 de enero de 2026
