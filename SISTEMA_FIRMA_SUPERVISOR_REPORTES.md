# Sistema de Firma de Supervisor para Reportes

## 📋 Resumen

Se implementó un sistema completo que permite a los supervisores firmar reportes generados por los usuarios. Una vez firmado, el reporte no puede ser eliminado.

---

## 🗄️ Cambios en Base de Datos

### Nuevas Columnas en `reportes_generados`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `firmado_supervisor` | BOOLEAN | Indica si el reporte fue firmado |
| `fecha_firma_supervisor` | TIMESTAMP | Fecha/hora de la firma |
| `firma_supervisor_base64` | TEXT | Imagen de firma digital (opcional) |
| `nombre_supervisor` | VARCHAR(255) | Nombre de quien firmó |
| `supervisor_id` | INTEGER | ID del supervisor que firmó |

### Ejecutar Migración

```bash
# En el VPS (31.97.8.51)
cd /ruta/backend
python agregar_firma_supervisor_reportes.py
```

---

## 🔌 Nuevos Endpoints en Backend

### 1. Firmar Reporte
```
POST /reportes/firmar/{reporte_id}
```

**Body:**
```json
{
  "supervisor_id": 1,
  "nombre_supervisor": "Juan Pérez",
  "firma_base64": "data:image/png;base64,..." // Opcional
}
```

**Response exitosa:**
```json
{
  "success": true,
  "message": "Reporte firmado exitosamente por Juan Pérez",
  "data": {
    "reporte_id": 123,
    "firmado_supervisor": true,
    "fecha_firma": "2025-01-15T10:30:00-06:00",
    "nombre_supervisor": "Juan Pérez",
    "supervisor_id": 1
  }
}
```

### 2. Quitar Firma
```
DELETE /reportes/quitar-firma/{reporte_id}?supervisor_id=1
```

---

## 🖼️ Cambios en Frontend (pwasuper)

### Vista de Historial de Reportes

1. **Indicador visual de firma**
   - Los reportes firmados tienen borde verde
   - Badge "✓ Firmado" visible
   - Info del supervisor que firmó y fecha

2. **Botón de eliminar**
   - Se muestra normalmente si NO está firmado
   - Se reemplaza por icono de candado si ESTÁ firmado
   - Tooltip: "No se puede eliminar: Reporte firmado por supervisor"

3. **Línea informativa**
   - Cuando está firmado, muestra:
   - "Firmado por **Nombre Supervisor** • 15 ene 2025, 10:30"

---

## 🛡️ Protección en Backend

El endpoint de eliminación ahora verifica:
```python
# Si está firmado, no permite eliminar
if reporte[5]:  # firmado_supervisor
    raise HTTPException(
        status_code=403, 
        detail="No se puede eliminar un reporte que ya ha sido firmado por el supervisor"
    )
```

---

## 📝 Para Implementar Después (admin-pwa)

Cuando lo solicites, se implementará en admin-pwa:

1. **Listado de reportes sin firmar**
   - Filtro para ver solo reportes pendientes de firma
   
2. **Modal de firma**
   - Campo de firma digital (canvas)
   - Botón "Firmar Reporte"
   
3. **Indicadores visuales**
   - Reportes firmados vs pendientes
   - Historial de firmas

---

## ✅ Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `backend/main.py` | Endpoints de firma, historial actualizado, protección de eliminación |
| `backend/agregar_firma_supervisor_reportes.py` | Script de migración de BD |
| `pwasuper/src/views/Reportes.vue` | UI de historial con indicadores de firma |

---

## 🚀 Pasos para Despliegue

1. **Ejecutar migración de BD:**
   ```bash
   python agregar_firma_supervisor_reportes.py
   ```

2. **Reiniciar backend:**
   ```bash
   sudo systemctl restart pwa-backend
   ```

3. **Reconstruir pwasuper:**
   ```bash
   npm run build
   ```

---

*Implementado: Enero 2025*
