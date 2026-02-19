# ⚡ ACCIÓN INMEDIATA - 3 PASOS SIMPLES

## 🎯 LO QUE DEBES HACER AHORA:

### 1️⃣ DESPLEGAR EL BACKEND (5 minutos)

```bash
cd backend
pip install paramiko
python desplegar_backend_auto.py
```

El script te pedirá:
- Contraseña del servidor (31.97.8.51)
- Confirmación para reiniciar

**Hace automáticamente**:
- ✅ Backup del archivo actual
- ✅ Sube el archivo arreglado
- ✅ Reinicia el servicio
- ✅ Verifica que esté corriendo

---

### 2️⃣ PROBAR QUE FUNCIONA (2 minutos)

```bash
cd admin-pwa
npm run dev
```

Luego en el navegador:
```
http://localhost:5173/#/debug-buscador
```

1. Ingresa: `ROCR820619MSLJSB05`
2. Click en "🔍 Buscar"
3. Observa el resultado

**Si funciona**: Verás usuarios y sus registros
**Si no funciona**: Verás exactamente qué salió mal en el log

---

### 3️⃣ VERIFICAR EN PRODUCCIÓN (1 minuto)

Ve a tu admin-pwa de producción y busca la CURP en `/registros` normal.

---

## 🚨 SI ALGO FALLA

### Script de despliegue falla:

```bash
# Despliegue manual:
ssh root@31.97.8.51

# Una vez conectado:
cd /root
find . -name "main.py" | grep -E "backend|pwa"

# Editar el archivo encontrado y cambiar línea ~6436:
# DE:   WHERE {' AND '.join(condiciones)}
# A:    WHERE {' OR '.join(condiciones)}

# Reiniciar:
pm2 restart all
# o
systemctl restart pwa-backend
```

### Debug muestra error:

Revisa el log en la parte inferior de la página de debug. Te dirá exactamente qué está mal.

---

## 📁 ARCHIVOS CREADOS (para tu referencia)

1. **DebugBuscadorView.vue** - Página de debugging
2. **desplegar_backend_auto.py** - Script de despliegue
3. **test_buscar_produccion.py** - Script de pruebas
4. **SOLUCION_COMPLETA_BUSCADOR.md** - Guía completa
5. **GUIA_DEBUG_BUSCADOR_COMPLETO.md** - Guía de uso

---

## ✅ RESUMEN

**PROBLEMA**: Backend usa AND en vez de OR para buscar usuarios

**SOLUCIÓN**: Ya está arreglado en local, solo falta desplegar

**ACCIÓN**: Ejecutar script de despliegue y probar

---

**Tiempo estimado total**: 8 minutos
**Dificultad**: Baja (todo automatizado)

¿Listo? Ejecuta el primer comando 👆
