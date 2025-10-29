# 🚀 Guía Rápida: Eliminar Imágenes

## ¿Qué hace?
Elimina todas las imágenes (fotos) del sistema:
- ✅ Fotos de registros de actividades
- ✅ Fotos de entrada/salida de asistencias
- ✅ Archivos físicos del servidor

## ¿Dónde está?
**Configuración → Sección "Acciones" → Botón Rosa "Eliminar Imágenes"**

## ¿Cómo usarlo?

### 1. Haz clic en el botón
![Button location]
Busca el botón rosa con icono de imagen en la sección de Acciones

### 2. Primera Confirmación (Modal)
Se abrirá un modal diciendo:
- ⚠️ "ELIMINAR TODAS LAS IMÁGENES"
- Descripción de qué se va a eliminar
- Botones: "Cancelar" o "Aceptar"

**Haz clic en "Aceptar"**

### 3. Segunda Confirmación (Prompt)
Aparecerá un cuadro de texto pidiendo:
```
Para confirmar, escribe exactamente: ELIMINAR IMÁGENES
```

**Copia y pega o escribe exactamente**: `ELIMINAR IMÁGENES`

### 4. Ver Progreso
Aparecerá el modal de progreso con:
- 📊 Barra de progreso animada
- 📈 Estadísticas en vivo:
  - Fotos en BD limpiadas
  - Archivos eliminados
  - Archivos no encontrados
  - Errores

### 5. Resultado Final
Cuando termine:
- ✅ Mostrará resumen con total eliminado
- 🎯 Botón "Aceptar" se activa
- 📢 Mensaje de éxito

---

## ⚙️ Características de Seguridad

✅ **Doble Confirmación**: Modal + Prompt de texto
✅ **Confirmación de Texto**: Evita errores
✅ **Progreso en Tiempo Real**: Ve qué está pasando
✅ **Estadísticas Detalladas**: Sabe qué se eliminó
✅ **Sin Backup**: Una vez eliminado, no se recupera ⚠️

---

## ⚠️ IMPORTANTE

🔴 **ESTA ACCIÓN ES IRREVERSIBLE**
- No hay papelera de reciclaje
- No hay backups automáticos
- Una vez eliminadas, las imágenes se pierden

💡 **RECOMENDACIÓN**: 
- Hacer backup de la BD antes de ejecutar
- Realizar en horario de bajo uso del sistema
- Confirmar con el administrador del sistema

---

## 🆘 Si Algo Sale Mal

### ❌ El botón no aparece
- Recarga la página (F5)
- Limpia el cache (Ctrl + Shift + R)
- Verifica que tengas permisos de administrador

### ❌ Error de conexión
- Verifica que el servidor está activo
- Comprueba tu conexión a internet
- Intenta de nuevo en unos minutos

### ❌ Las imágenes no se eliminan
- Verifica que el servidor tiene permisos en `/fotos/`
- Revisa el espacio disponible en el disco
- Consulta los logs del servidor

---

## 📊 Ejemplo de Resultado

```
✅ ELIMINACIÓN EXITOSA

Total eliminado: 142 imágenes
- Fotos de BD limpiadas: 142
- Archivos eliminados: 140
- Archivos no encontrados: 2
- Errores: 0

Operación completada en: 2.5 segundos
```

---

## 💾 Alternativa Segura

Si no estás seguro, puedes:

1. **Exportar Datos** primero:
   - Botón "Exportar Datos (JSON)" 
   - Botón "Descargar BD"
   - Botón "Exportar Usuarios"

2. **Luego Eliminar Imágenes**:
   - Ya tienes un backup
   - Procede con confianza

---

**¿Preguntas?** Revisa la documentación completa en:
`ELIMINADOR_IMAGENES_DOCUMENTACION.md`
