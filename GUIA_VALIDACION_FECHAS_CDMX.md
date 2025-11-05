# ✅ GUÍA DE VALIDACIÓN - Corrección de Fechas CDMX

## 📋 Checklist de Pruebas

### 1. ✅ Marcar Entrada
**Pasos**:
1. Abre la PWA en modo usuario
2. Ve a Home.vue
3. Haz clic en "Marcar Entrada"
4. Llena los campos (ubicación, foto, descripción)
5. Confirma

**Validación**:
- [ ] La hora que se guarda debe coincidir EXACTAMENTE con el reloj de la barra verde (ConnectivityStatus.vue)
- [ ] La fecha debe ser de HOY en CDMX (no anterior)
- [ ] En el modal de confirmación, debe mostrar hora correcta
- [ ] En Historial → Asistencias, debe aparecer con fecha/hora correcta

---

### 2. ✅ Registrar Actividad (Campo/Gabinete)
**Pasos**:
1. Marca tu Entrada primero
2. Ve a la sección "Actividades"
3. Selecciona tipo (Campo o Gabinete)
4. Obtén ubicación, foto, descripción
5. Guarda

**Validación**:
- [ ] La actividad se guarda con hora ACTUAL de CDMX
- [ ] En Historial → Actividades, aparece con fecha/hora correcta
- [ ] La fecha NO es de hace un día
- [ ] El tipo de actividad (Campo/Gabinete) se muestra correctamente

---

### 3. ✅ Marcar Salida
**Pasos**:
1. Después de registrar actividades
2. Haz clic en "Marcar Salida"
3. Llena los campos
4. Confirma

**Validación**:
- [ ] La salida se guarda con hora ACTUAL de CDMX
- [ ] En Historial → Asistencias, aparece con fecha/hora correcta
- [ ] La hora es DESPUÉS de la entrada
- [ ] Las actividades siguen visibles en el historial

---

### 4. ✅ Historial - Asistencias
**Pasos**:
1. Ve a Historial
2. Tab "Asistencias"
3. Busca el registro de hoy

**Validación**:
- [ ] Agrupa por fecha correcta (hoy, no ayer)
- [ ] Muestra "ENTRADA" y "SALIDA" por separado
- [ ] Las horas coinciden exactamente con las que registraste
- [ ] Botón "Ubicación" funciona correctamente

---

### 5. ✅ Historial - Actividades
**Pasos**:
1. Ve a Historial
2. Tab "Actividades"
3. Busca los registros de hoy

**Validación**:
- [ ] Se agrupa por fecha correcta (hoy, no ayer)
- [ ] Muestra tipo de actividad (🌾 Campo o 🏢 Gabinete)
- [ ] Las horas coinciden exactamente con las que registraste
- [ ] NO aparecen como entrada/salida

---

### 6. ✅ Modo Offline - Registrar Offline
**Pasos**:
1. Desactiva internet (modo avión o desconecta WiFi)
2. Registra una actividad completamente offline
3. Confirma que se guarda "pendiente"
4. Reactiva internet
5. Espera sincronización automática o toca "Sincronizar ahora"

**Validación**:
- [ ] El registro se guarda offline correctamente
- [ ] Al sincronizar, se envía al servidor
- [ ] En el Historial, aparece con fecha/hora CORRECTA de CDMX (NO actualizado a la hora actual)
- [ ] El timestamp guardado es el del momento offline, no del sincronización

---

### 7. ✅ Reloj de la Barra Verde
**Pasos**:
1. Abre Home.vue
2. Observa el reloj en la barra verde (ConnectivityStatus.vue)
3. Registra algo y verifica que la hora coincida

**Validación**:
- [ ] El reloj muestra CDMX correctamente
- [ ] Cuando registras algo, la hora en el modal coincide
- [ ] El reloj avanza en tiempo real (actualiza cada segundo)
- [ ] Es la fuente de verdad

---

### 8. ✅ Formato de Fechas
**Verificación en consola del navegador**:

```javascript
// Abre DevTools → Console
// Verifica que los ISO formats tengan zona horaria:

// Deberías ver:
"fecha_hora": "2025-11-05T14:30:45-06:00"  // ✅ Correcto (con -06:00)

// NO deberías ver:
"fecha_hora": "2025-11-05T14:30:45"  // ❌ Incorrecto (sin zona)
```

---

### 9. ✅ Backend - Logs
**Cómo verificar**:

```bash
# En la terminal del backend, deberías ver:

# ✅ Cuando se registra entrada/salida:
"📅 ✅ Conversión de timestamp completada:"
"   🌍 UTC original: 2025-11-05T20:30:45+00:00"
"   🇲🇽 CDMX convertido: 2025-11-05 14:30:45-06:00"
"   📆 Fecha LOCAL CDMX: 2025-11-05"

# ✅ Cuando se devuelven registros:
"📅 Fecha con zona CDMX: 2025-11-05T14:30:45-06:00"
```

---

### 10. ✅ Casos Edge
**Fecha a medianoche**:
- Registra algo a las 23:59 (CDMX)
- Luego registra a las 00:01 del día siguiente
- Verifica que Historial agrupe correctamente por fecha

**Cambio de zona horaria**:
- Si el servidor tiene zona horaria UTC, pero devuelve con -06:00, es correcto

---

## 🐛 Problemas Esperados (SI los ves, significa que NO está bien)

❌ **La fecha es un día anterior**
- → Significa que no se agregó "-06:00" al ISO format
- → Verifica backend main.py líneas 672 y 2200

❌ **La hora es incorrecta**
- → Significa que el timestamp_offline no se está enviando
- → Verifica Home.vue línea ~1291 y ~1859

❌ **Las actividades aparecen como entrada/salida**
- → Significa que se están guardando en la tabla asistencias
- → Verifica que /registro sea POST diferente a /asistencia/entrada

❌ **Historial no agrupa correctamente**
- → Significa que obtenerFechaCDMX() no está formateando bien
- → Verifica Historial.vue línea ~892

---

## 📊 Tabla de Comparación - Antes vs Después

| Aspecto | Antes (❌) | Después (✅) |
|---------|-----------|-----------|
| Fecha en Historial | Ayer | Hoy |
| Hora vs Reloj Verde | No coincide | Coincide exactamente |
| Entrada vs Actividad | Se mezclan | Independientes |
| Formato Backend | `2025-11-05T14:30` | `2025-11-05T14:30-06:00` |
| Offline → Online | Fecha incorrecta | Fecha correcta |
| Consistencia | Errática | Perfecta |

---

## 🎯 Resultado Final Esperado

Cuando todo esté correcto, **DEBERÍAS VER**:

1. **Panel de entrada/salida**: Horas coinciden con reloj verde
2. **Historial - Asistencias**: 
   - Agrupa por "hoy" (no ayer)
   - Entrada y Salida con horas correctas
3. **Historial - Actividades**:
   - Agrupa por "hoy"
   - Cada actividad muestra tipo (Campo/Gabinete)
   - Horas exactas de cuando se registraron
4. **Sincronización**: Si registras offline, al sincronizar muestra fecha correcta
5. **Consistencia Total**: Todos los registros coinciden en fecha/hora

---

## 💡 Tips de Debugging

Si algo no funciona:

1. **Abre DevTools (F12) → Console**
   - Busca errores en JavaScript
   - Busca logs relacionados con timestamps

2. **Abre DevTools → Network**
   - Verifica que los requests incluyan `timestamp_offline`
   - Verifica que las respuestas tengan `-06:00` en las fechas

3. **Backend Console**
   - Busca el log de "Conversión de timestamp completada"
   - Verifica que la fecha LOCAL CDMX sea correcta

4. **Base de datos**
   ```sql
   SELECT id, fecha, hora_entrada FROM asistencias ORDER BY id DESC LIMIT 5;
   ```
   - Las fechas deben ser de CDMX (no UTC)

---

## 🎉 Confirmación Final

Cuando hayas validado todos los puntos, marca como completado y reporta:
- [ ] Entrada: Fecha/hora correcta
- [ ] Salida: Fecha/hora correcta
- [ ] Actividades: Fecha/hora correcta
- [ ] Historial: Todas las fechas son de HOY
- [ ] Offline → Online: Sincroniza con fecha correcta
- [ ] Todo coincide con el reloj de la barra verde

¡PERFECTO! 🚀
