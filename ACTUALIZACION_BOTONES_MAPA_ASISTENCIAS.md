# Actualización: Botones "Ver Ubicación" en Historial

## Resumen de Cambios

Se ha actualizado el texto de los botones en todo el historial:
- **Actividades**: "Mapa" → "Ubicación"
- **Asistencias (Entrada)**: "Ver en mapa" → "Ver ubicación"
- **Asistencias (Salida)**: "Ver en mapa" → "Ver ubicación"

Todos los botones ahora muestran el mismo diseño consistente con icono de ubicación y texto descriptivo.

## Cambios Realizados

### 1. **Botón en Actividades (Línea ~275)**

**Antes:**
```vue
<button @click="verEnMapa(registro)" ...>
  <svg>...</svg>
  Mapa
</button>
```

**Después:**
```vue
<button @click="verEnMapa(registro)" ...>
  <svg>...</svg>
  Ubicación
</button>
```

### 2. **Botón de Entrada (Línea ~419)**

**Antes:**
```vue
<span class="text-xs">Ver en mapa</span>
```

**Después:**
```vue
<span class="text-xs">Ver ubicación</span>
```

### 3. **Botón de Salida (Línea ~481)**

**Antes:**
```vue
<span class="text-xs">Ver en mapa</span>
```

**Después:**
```vue
<span class="text-xs">Ver ubicación</span>
```

## Características de los Botones

### Botones en Entrada (Azul)
- **Icono:** Ubicación (pin)
- **Texto:** "Ver ubicación" 
- **Fondo:** `bg-blue-100` con borde `border-blue-200`
- **Color:** `text-blue-700` en pequeño
- **Hover:** Fondo `bg-blue-200` con efecto escala `hover:scale-105`
- **Sombra:** `shadow-sm` para profundidad
- **Transición:** 300ms suave

### Botones en Salida (Rojo)
- **Icono:** Ubicación (pin)
- **Texto:** "Ver ubicación" 
- **Fondo:** `bg-red-100` con borde `border-red-200`
- **Color:** `text-red-700` en pequeño
- **Hover:** Fondo `bg-red-200` con efecto escala `hover:scale-105`
- **Sombra:** `shadow-sm` para profundidad
- **Transición:** 300ms suave

### Botón en Actividades
- **Icono:** Ubicación (pin)
- **Texto:** "Ubicación" 
- **Color dinámico según tipo de actividad:**
  - Campo: Verde (`bg-green-100`, `text-green-700`)
  - Gabinete: Naranja (`bg-orange-100`, `text-orange-700`)
  - Otros: Gris (`bg-gray-100`, `text-gray-700`)
- **Hover:** Color más oscuro con efecto escala
- **Sombra:** `shadow-sm` para profundidad
- **Transición:** 300ms suave

## Mejoras Visuales

1. ✅ **Texto Consistente:** Todos dicen "Ubicación" o "Ver ubicación"
2. ✅ **Mejor Legibilidad:** Texto completo en lugar de emojis
3. ✅ **Interactividad Mejorada:** Efecto hover con escala y transición suave
4. ✅ **Distinción Visual:** 
   - Actividades: Colores según tipo (Verde/Naranja/Gris)
   - Entrada: Azul
   - Salida: Rojo
5. ✅ **Icono Consistente:** Mismo SVG de ubicación en todos
6. ✅ **Tamaño Optimizado:** Texto pequeño (`text-xs`) pero legible

## Validación

- ✅ Sin errores de sintaxis
- ✅ Cambios aplicados correctamente
- ✅ Responsive y adaptable
- ✅ Consistencia visual mantenida

## Archivo Modificado

- `src/views/Historial.vue` (líneas ~275, ~419, ~481)

---
**Fecha:** 30 de Octubre de 2025
**Estado:** Completado ✅
