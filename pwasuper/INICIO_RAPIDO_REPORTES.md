# 🚀 GUÍA RÁPIDA DE INICIO - MÓDULO DE REPORTES

## ⚡ En 5 Minutos

### 1. Verificar Instalación ✅
```bash
cd c:\Users\ASUS\Music\PWASV\PWASV\pwasuper
npm list jspdf html2canvas
```

Si no está instalado:
```bash
npm install jspdf html2canvas
```

### 2. Iniciar Desarrollo 🔄
```bash
npm run dev
```

La app estará disponible en: `http://localhost:3003`

### 3. Acceder a Reportes 📊
1. Abre la app en el navegador
2. Inicia sesión
3. Abre el menú (hamburguesa ☰)
4. Selecciona **"Reportes"**

---

## 🧪 Prueba Rápida

### Generar tu Primer Reporte

1. **Navega a Reportes**
   - Desde el menú principal

2. **Observa los datos**
   - Verifica que cargue actividades
   - Revisa las estadísticas

3. **Firma (Opcional)**
   - Dibuja tu firma en el canvas
   - O deja en blanco

4. **Descarga**
   - Selecciona formato (PDF o CSV)
   - Haz clic en "Descargar Reporte"

5. **Verifica**
   - Abre el archivo descargado
   - Confirma que contiene tus datos

---

## 📂 Estructura de Archivos

```
pwasuper/
├── src/
│   ├── services/
│   │   ├── reportesService.js ← NUEVO
│   │   └── ...
│   ├── components/
│   │   ├── FirmaDigital.vue ← NUEVO
│   │   └── ...
│   ├── views/
│   │   ├── Reportes.vue ← NUEVO
│   │   └── ...
│   └── router/
│       └── index.js ← MODIFICADO
├── package.json ← MODIFICADO
├── GUIA_REPORTES.md ← DOCUMENTACIÓN
├── RESUMEN_TECNICO_REPORTES.md ← DOCUMENTACIÓN
└── ...
```

---

## 🔍 Verificación Rápida

### Verificar que todo está instalado
```bash
# 1. Dependencias
npm list jspdf html2canvas

# 2. Archivos
ls -la src/services/reportesService.js
ls -la src/components/FirmaDigital.vue
ls -la src/views/Reportes.vue

# 3. Rutas
grep -n "Reportes" src/router/index.js
grep -n "/reportes" src/router/index.js
```

---

## 🎯 Funcionalidades Principales

### Dashboard
- Tarjetas con estadísticas
- Selector de mes/año
- Indicador de estado

### Tabla de Actividades
- Listado de registros
- Filtrado por período
- Estilos por tipo

### Firma Digital
- Canvas interactivo
- Soporte táctil
- Exportación a imagen

### Descarga
- Formato PDF profesional
- Formato CSV para Excel
- Historial de descargas

---

## 🐛 Si Algo No Funciona

### Error: "Módulo no encontrado"
```bash
npm install jspdf html2canvas
npm run dev
```

### Error: "Ruta /reportes no existe"
- Verifica que router/index.js tenga la ruta
- Recarga la página Ctrl+Shift+R

### Error: "No se carga tabla de actividades"
- Verifica que estés autenticado
- Comprueba conexión a internet
- Abre consola: F12 → Busca errores

### Error: "No se descarga PDF"
- Verifica permisos de descarga
- Desactiva bloqueador de pop-ups
- Intenta otro navegador

---

## 📊 Datos de Prueba

Para probar con datos reales:

1. Asegúrate de tener actividades registradas
2. Ve a la vista de Reportes
3. Selecciona un mes con registros
4. La tabla debe mostrar tus actividades

---

## 💡 Tips Útiles

### Tip 1: Cambiar Mes Rápido
- Usa los dropdowns de Mes/Año
- Los datos se cargan automáticamente

### Tip 2: Firma Bonita
- Dibuja lentamente
- Usa movimientos naturales
- Practica en el canvas varias veces

### Tip 3: Compartir Reportes
- PDF: Ideal para correo y WhatsApp
- CSV: Ideal para compartir datos
- Ambos se pueden imprimir

### Tip 4: Revisar Descargadas
- Scrollea hasta "Reportes Generados Recientemente"
- Veras historial de descargas locales
- Borrar datos del navegador = borra historial

---

## 🔗 Rutas Disponibles

```
/reportes          → Vista principal de reportes
                     (protegida por autenticación)
```

---

## 📱 Compatibilidad

✅ **Navegadores Soportados**
- Chrome/Chromium 80+
- Firefox 75+
- Safari 13+
- Edge 80+

✅ **Dispositivos**
- Móviles (320px+)
- Tablets (768px+)
- Desktops (1024px+)

---

## 🎓 Documentación

Para más detalles, lee:

1. **GUIA_REPORTES.md**
   - Guía de usuario completa
   - Explicación de todas las funciones
   - Solución de problemas

2. **RESUMEN_TECNICO_REPORTES.md**
   - Documentación técnica
   - Arquitectura del sistema
   - API endpoints

3. **RESUMEN_VISUAL_REPORTES.md**
   - Interfaz visual
   - Flujos de datos
   - Casos de uso

4. **CHECKLIST_IMPLEMENTACION_REPORTES.md**
   - Estado de implementación
   - Checklist de features
   - Información de deployment

---

## 🚀 Próximos Pasos (Opcional)

### Fase 1: Verificación
- [ ] Ejecutar en desarrollo
- [ ] Probar todas las funciones
- [ ] Verificar en múltiples navegadores

### Fase 2: Testing
- [ ] Pruebas de carga
- [ ] Pruebas con muchos datos
- [ ] Pruebas de compatibilidad

### Fase 3: Deployment
- [ ] Compilar para producción
- [ ] Desplegar en servidor
- [ ] Verificar funcionamiento

### Fase 4: Monitoreo
- [ ] Monitorear uso
- [ ] Recopilar feedback
- [ ] Realizar mejoras

---

## ❓ Preguntas Frecuentes

**P: ¿La firma se envía al servidor?**  
R: No, la firma se genera y guarda solo en el PDF localmente.

**P: ¿Dónde se guardan los reportes descargados?**  
R: En tu carpeta de Descargas del dispositivo.

**P: ¿Puedo generar reportes de meses pasados?**  
R: Sí, usa el selector de mes/año para elegir cualquier período.

**P: ¿Qué pasa si pierdo mi firma?**  
R: Puedes dibujar de nuevo en el canvas, es ilimitado.

**P: ¿Es seguro el PDF?**  
R: Sí, los PDF se generan en tu navegador sin pasar por servidor.

---

## 📞 Soporte

Si necesitas ayuda:

1. Revisa la documentación completa
2. Verifica la consola del navegador (F12)
3. Contacta al equipo técnico
4. Abre un ticket de soporte

---

## ✨ ¡Listo para Usar!

Ahora ya sabes cómo:
- ✅ Acceder al módulo de reportes
- ✅ Generar un reporte
- ✅ Firmar digitalmente
- ✅ Descargar en PDF/CSV
- ✅ Ver el historial

**¡Disfruta generando tus reportes!** 🎉

---

**Última actualización**: 24 de Enero de 2026  
**Versión**: 1.0  
**Estado**: Activo
