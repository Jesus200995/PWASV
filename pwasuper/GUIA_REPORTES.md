# 📊 Guía de Uso - Módulo de Reportes

## Descripción General

El nuevo módulo de **Reportes** en PWA Super permite a los usuarios generar reportes mensuales de sus actividades registradas. Los reportes pueden incluir:

- ✅ Listado completo de actividades del período seleccionado
- ✅ Información del usuario (nombre, cargo, correo)
- ✅ Firma digital autenticada
- ✅ Descarga en formato PDF o CSV

## 🎯 Funcionalidades Principales

### 1. **Selección de Período**
- Selecciona el mes y año deseado mediante dropdowns
- Se carga automáticamente el historial de actividades del período
- Muestra estadísticas del período (total de registros, entradas, salidas)

### 2. **Tabla de Actividades**
- Visualización clara de todas las actividades registradas
- Incluye: Fecha, Hora, Tipo (Entrada/Salida/Actividad), Descripción
- Estilos diferenciados por tipo de actividad
- Tabla responsiva que se adapta a cualquier dispositivo

### 3. **Firma Digital**
- Canvas interactivo para firmar con ratón o pantalla táctil
- Botón para limpiar la firma
- Limpiar y volver a intentar sin límites
- La firma se incluye automáticamente en el PDF

### 4. **Generación de Reportes**

#### PDF
- Documento profesional con encabezado personalizado
- Incluye información del usuario
- Tabla formateada con todas las actividades
- Firma digital si está disponible
- Metadatos con fecha y hora de generación

#### CSV
- Formato Excel compatible
- Importable a hojas de cálculo
- Incluye todos los campos de actividades

### 5. **Historial de Reportes**
- Registro local de reportes generados recientemente
- Muestra nombre, fecha y tipo de formato
- Se almacena en localStorage del navegador

## 📱 Acceso al Módulo

### Desde el Menú Principal
1. Abre la aplicación PWA Super
2. Inicia sesión con tus credenciales
3. Abre el menú móvil (hamburguesa en la esquina superior derecha)
4. Selecciona **"Reportes"**

### Ruta Directa
```
/reportes
```

## 🚀 Flujo de Uso Típico

1. **Navega a Reportes**
   - Accede desde el menú principal

2. **Selecciona el Período**
   - Elige mes y año usando los selectores
   - El sistema carga automáticamente las actividades

3. **Revisa las Actividades**
   - Visualiza la tabla con todos los registros
   - Verifica que toda la información sea correcta

4. **Firma el Reporte (Opcional pero Recomendado)**
   - Dibuja tu firma en el canvas
   - Puedes limpiar y volver a intentar cuantas veces quieras

5. **Selecciona Formato de Descarga**
   - PDF: Para imprimir o compartir formalmente
   - CSV: Para análisis en Excel

6. **Descarga el Reporte**
   - Haz clic en "Descargar Reporte"
   - El archivo se guardará en tu dispositivo

## 📋 Información Mostrada en el Reporte

### Encabezado
- Título: "REPORTE DE ACTIVIDADES"
- Período: Mes y Año

### Sección de Usuario
- Nombre Completo
- Cargo
- Correo Electrónico
- Fecha de Generación

### Resumen
- Total de Registros
- Total de Entradas
- Total de Salidas

### Detalle de Actividades
Tabla con columnas:
- **Fecha**: Fecha del registro (formato local)
- **Hora**: Hora exacta del registro
- **Tipo**: Entrada, Salida o Actividad
- **Descripción**: Detalles adicionales del registro

### Firma Digital (si aplica)
- Imagen de la firma
- Nombre de quien firma
- Fecha y hora de firma

## 🛠️ Características Técnicas

### Dependencias Utilizadas
- **jsPDF**: Generación de documentos PDF
- **html2canvas**: Conversión de elementos HTML a imágenes
- **Axios**: Comunicación con el backend
- **Vue Router**: Enrutamiento

### API Utilizada
```
GET /historial/{usuario_id}?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD
```

### Almacenamiento Local
- Historial de reportes guardados en localStorage
- Persisten entre sesiones del navegador

## 📊 Estadísticas Mostradas

Las tarjetas de estadísticas en la parte superior muestran:

1. **Actividades del Mes**
   - Total de actividades registradas

2. **Período**
   - Mes y año seleccionados
   - Rango de fechas completo

3. **Estado del Reporte**
   - "Sin datos": No hay actividades
   - "Sin firmar": Hay actividades pero no está firmado
   - "Firmado": Reporte listo con firma

## 💡 Tips y Recomendaciones

1. **Firma Digital**: Aunque es opcional, se recomienda firmar los reportes para mayor autenticidad

2. **Formato PDF**: Ideal para:
   - Impresión
   - Envío por correo
   - Archivos de auditoría
   - Presentaciones formales

3. **Formato CSV**: Ideal para:
   - Análisis de datos
   - Importación a bases de datos
   - Procesamiento automatizado
   - Auditorías técnicas

4. **Navegación por Períodos**: Puedes generar reportes de meses anteriores seleccionando el mes y año deseado

5. **Actualización de Datos**: Los datos se cargan del servidor cuando cambias de período

## ⚠️ Limitaciones Conocidas

- La firma digital solo es válida en el navegador donde se creó
- El historial de reportes se borra si se limpian los datos del navegador
- El CSV no incluye las imágenes de actividades (solo datos)
- Se requiere conexión a internet para cargar las actividades del servidor

## 🐛 Solución de Problemas

### "No hay actividades para generar el reporte"
- **Causa**: No hay registros en el período seleccionado
- **Solución**: Selecciona otro mes con registros o verifica en el Historial

### La firma no se guarda
- **Causa**: Problemas con el canvas o navegador
- **Solución**: Intenta de nuevo, asegúrate de usar un navegador moderno

### Error de conexión al cargar actividades
- **Causa**: Problema de red o servidor no disponible
- **Solución**: Verifica tu conexión y recarga la página

### El PDF no se descarga
- **Causa**: Bloqueador de ventanas emergentes o problema de permisos
- **Solución**: Verifica la configuración de descargas del navegador

## 📞 Soporte

Para problemas o sugerencias relacionadas con el módulo de Reportes:
- Contacta al equipo de soporte
- Usa la burbuja de soporte en la app
- Envía un correo al equipo técnico

---

**Versión**: 1.0  
**Última actualización**: Enero 2026  
**Estado**: Activo y Funcional
