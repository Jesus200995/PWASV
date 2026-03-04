# 🧪 GUÍA DE PRUEBAS — ASISTENCIAVIEW APPLE STYLE
## Verificación Completa del Rediseño

---

## ✅ CHECKLIST DE VERIFICACIÓN VISUAL

### 🎨 **1. Diseño Apple**

#### Header
- [ ] Glassmorphism aplicado (fondo translúcido con blur)
- [ ] Icono circular con gradiente azul
- [ ] Título grande con tipografía SF Pro Display
- [ ] Subtítulo con contador de registros
- [ ] Botón refresh circular en la derecha
- [ ] Sticky al hacer scroll

#### Stats Cards
- [ ] 3 cards con iconos de colores (azul, verde, púrpura)
- [ ] Hover eleva las cards 4px
- [ ] Sombras sutiles visibles
- [ ] Gradientes en iconos
- [ ] Valores numéricos grandes y pesados
- [ ] Labels en uppercase pequeños

#### Búsqueda
- [ ] Input grande (48px de altura)
- [ ] Icono de lupa dentro del input
- [ ] Placeholder gris claro
- [ ] Botón X circular para limpiar (cuando hay texto)
- [ ] Focus ring azul Apple al enfocar
- [ ] Fondo gris claro (#F5F5F7)

#### Quick Filters (Pills)
- [ ] Botones redondeados (border-radius: 20px)
- [ ] Fondo gris claro por defecto
- [ ] Fondo azul cuando está activo
- [ ] Transición suave al cambiar
- [ ] Texto blanco cuando activo

#### Tabla
- [ ] Fondo blanco limpio
- [ ] Headers con fondo gris claro
- [ ] Hover row con fondo azul transparente
- [ ] Avatares circulares con gradientes
- [ ] Badges coloridos para estados
- [ ] Botones de ubicación con iconos
- [ ] Fotos thumbnail clickeables

#### Paginación
- [ ] Botones circulares/redondeados
- [ ] Número activo con gradiente azul
- [ ] Flechas SVG limpias
- [ ] Disabled state visible

---

## ⚡ CHECKLIST DE PERFORMANCE

### Carga Inicial
- [ ] Primera carga < 1 segundo
- [ ] Spinner de carga suave
- [ ] Stats cards aparecen primero
- [ ] Tabla carga después

### Búsqueda y Filtros
- [ ] Búsqueda responde instantáneamente
- [ ] Filtros rápidos cambian sin lag
- [ ] No hay flash de contenido
- [ ] Smooth scrolling al cambiar página

### Animaciones
- [ ] Todas las animaciones a 60 FPS
- [ ] No hay jank al hacer hover
- [ ] Transiciones modales suaves
- [ ] Spinner gira perfectamente

---

## 🖱️ CHECKLIST DE INTERACCIONES

### Hover States
- [ ] Cards stats elevan al hover
- [ ] Botones cambian color al hover
- [ ] Filas de tabla destacan al hover
- [ ] Cursor pointer en elementos clickeables

### Click/Tap
- [ ] Botón refresh recarga datos
- [ ] Quick filters togglean correctamente
- [ ] Fotos abren modal al click
- [ ] Botón ubicación abre mapa
- [ ] Paginación funciona

### Focus/Keyboard
- [ ] Tab navega correctamente
- [ ] Enter activa botones enfocados
- [ ] Esc cierra modales
- [ ] Input búsqueda con focus ring azul

---

## 📱 CHECKLIST RESPONSIVE

### Desktop (>1024px)
- [ ] 3 stats cards en fila
- [ ] Tabla con todas las columnas visibles
- [ ] Sidebar visible
- [ ] Quick filters en una línea

### Tablet (768-1024px)
- [ ] Stats cards se adaptan
- [ ] Tabla aún visible completa
- [ ] Sidebar reducido
- [ ] Filtros wrap si es necesario

### Mobile (<768px)
- [ ] Stats cards en columna
- [ ] Tabla responsive (sin scroll horizontal)
- [ ] Sidebar oculto/colapsado
- [ ] Header compacto
- [ ] Botones táctiles (44x44px minimum)

---

## 🎨 CHECKLIST DE COLORES

Verifica que estos colores estén presentes:

### Azul Apple
- [ ] #007AFF en: botones primarios, links, focus rings
- [ ] Gradiente azul en stats card 1

### Verde Apple
- [ ] #34C759 en: badges "Completa", iconos éxito
- [ ] Gradiente verde en stats card 2

### Púrpura Apple
- [ ] #AF52DE en: stats card 3, acciones secundarias

### Grises
- [ ] #F5F5F7: fondos principales
- [ ] #E5E5EA: bordes sutiles
- [ ] #8E8E93: texto secundario
- [ ] #1D1D1F: texto principal

---

## 🧩 PRUEBAS FUNCIONALES

### Carga de Datos
```bash
# Abrir DevTools Console
# Buscar mensajes:
✅ Usuarios obtenidos del caché
✅ ## asistencias cargadas y cacheadas
⚡ Carga total de asistencias: ##ms
```

### Búsqueda
1. Escribir "Juan" → Debe filtrar instantáneamente
2. Borrar búsqueda → Debe restaurar todos los registros
3. Escribir caracteres especiales → No debe romper

### Filtros Rápidos
1. Click "Hoy" → Muestra solo asistencias de hoy
2. Click "Ayer" → Muestra solo de ayer
3. Click "Esta semana" → Filtra correctamente
4. Click mismo botón → Desactiva filtro

### Paginación
1. Navegar a página 2 → Smooth scroll al top
2. Click números directos → Cambia página
3. Flechas prev/next → Funcionan
4. Primera/última deshabilitadas correctamente

### Modales
1. Click en foto → Abre modal
2. Click fuera → Cierra modal
3. Botón X → Cierra modal
4. Esc key → Cierra modal

---

## 🔍 VERIFICACIÓN EN DEVTOOLS

### Performance Tab
```
Grabar 3 segundos de uso normal:
- Scripting: < 20%
- Rendering: < 30%
- Painting: < 10%
- FPS: estable en 60
```

### Network Tab
```
Verificar:
- Primera carga: 2-3 requests
- Caché funciona (no re-fetching)
- Requests con priority: high
- AbortController cancela correctos
```

### Console
```
No debe mostrar:
❌ Errores de JavaScript
❌ Warnings de Vue
❌ Errors 404 de imágenes
❌ CORS errors

Debe mostrar:
✅ Logs de caché
✅ Tiempos de carga
✅ Confirmaciones de operaciones
```

---

## 🎯 PRUEBAS DE RENDIMIENTO

### Lighthouse (Chrome DevTools)
Ejecutar Lighthouse en modo Desktop:

```
Targets:
- Performance:    > 95
- Accessibility:  > 95
- Best Practices: > 95
- SEO:           > 90
```

### Core Web Vitals
```
- LCP (Largest Contentful Paint):  < 1.2s
- FID (First Input Delay):         < 50ms
- CLS (Cumulative Layout Shift):   < 0.05
```

---

## 🐛 PROBLEMAS COMUNES Y SOLUCIONES

### "Los estilos no se aplican"
```bash
# Solución:
1. Verificar que AsistenciaView.vue fue reemplazado
2. Limpiar caché del navegador (Ctrl + Shift + R)
3. Verificar que vite está corriendo
4. Reiniciar servidor de desarrollo
```

### "Los datos no cargan"
```bash
# Solución:
1. Verificar que backend está corriendo
2. Check console para errores de CORS
3. Verificar token de autenticación
4. Revisar URL de API en config/api.js
```

### "Las animaciones van lentas"
```bash
# Solución:
1. Desactivar extensiones de navegador
2. Verificar GPU acceleration habilitado
3. Cerrar otras pestañas pesadas
4. Usar Chrome/Edge para mejor performance
```

### "Modal no se ve"
```bash
# Solución:
1. Verificar z-index del modal (debe ser 1000)
2. Check que body.style.overflow se setea a 'hidden'
3. Verificar que backdrop-filter es soportado
```

---

## 📸 SCREENSHOTS ESPERADOS

### Desktop
```
Tomar capturas de:
1. Vista general (header + stats + tabla)
2. Hover en stats card (elevación)
3. Focus en input búsqueda (ring azul)
4. Filter activo (pill azul)
5. Hover en fila de tabla
6. Modal de foto abierto
7. Paginación en página intermedia
```

### Mobile
```
Tomar capturas de:
1. Header compacto
2. Stats cards en columna
3. Tabla responsive
4. Filtros wrapeados
5. Modal de foto (full screen)
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

El rediseño se considera **exitoso** si:

1. ✅ **Visual**: Se ve indistinguible de una app Apple
2. ✅ **Performance**: Carga < 1s, 60 FPS constantes
3. ✅ **Responsivo**: Perfecto en todos los dispositivos
4. ✅ **Funcional**: Todas las features funcionan
5. ✅ **Caché**: Requests se cachean correctamente
6. ✅ **Accesible**: Navegación por teclado funciona
7. ✅ **Sin errores**: Console limpia
8. ✅ **Lighthouse**: Score > 95 en Performance

---

## 🚀 COMANDOS DE PRUEBA

### Iniciar Sistema
```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd admin-pwa
npm run dev
```

### Limpiar Caché
```javascript
// En DevTools Console:
AsistenciasService.limpiarCache()
location.reload()
```

### Ver Stats de Caché
```javascript
// En DevTools Console:
console.table(AsistenciasService.cache)
```

---

## 📊 MÉTRICAS OBJETIVO

| Métrica | Target | Actual |
|---------|--------|--------|
| Primera carga | < 1s | ___ |
| Búsqueda response | < 50ms | ___ |
| Cambio página | < 100ms | ___ |
| Apertura modal | < 200ms | ___ |
| FPS promedio | 60 | ___ |
| Lighthouse Performance | > 95 | ___ |
| Bundle size | < 500KB | ___ |

---

## 🎉 ¡PRUEBAS COMPLETADAS!

Una vez verificados todos los checkboxes, el rediseño Apple está **100% completo y funcional**.

---

**Última actualización**: 4 de marzo de 2026  
**Versión**: 2.0.0 Apple Style
