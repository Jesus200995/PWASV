# 📊 GUÍA COMPLETA: ESTADÍSTICAS DE USUARIOS POR PLATAFORMA (Android vs iOS)

## 🎯 Objetivo
Implementar un sistema de tracking que te permita ver en **tiempo real**:
- Cuántos usuarios usan **Android** 🤖
- Cuántos usuarios usan **iOS** 🍎
- Cuántos usuarios usan **Desktop** 💻
- Porcentajes y estadísticas detalladas

---

## 📋 PASO 1: Actualizar Base de Datos

### En el VPS, conectarte a PostgreSQL:
```bash
cd /var/www/PWASV/admin-pwa/backend
psql -h 31.97.8.51 -U jesus -d app_registros -f agregar_dispositivo.sql
```

**O ejecutar manualmente:**
```bash
psql -h 31.97.8.51 -U jesus -d app_registros
```

Luego copiar y pegar este SQL:
```sql
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS dispositivo VARCHAR(50) DEFAULT 'desconocido';

ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS user_agent TEXT DEFAULT NULL;

ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS ultimo_acceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE INDEX IF NOT EXISTS idx_usuarios_dispositivo ON usuarios(dispositivo);

-- Verificar que se crearon
\d usuarios
```

---

## 📋 PASO 2: Actualizar Backend (main.py)

### 2.1. Agregar el modelo DispositivoUpdate
Buscar la línea que dice `class NotificacionResponse(BaseModel):` (línea ~408)  
**DESPUÉS de esa clase**, agregar:

```python
class DispositivoUpdate(BaseModel):
    usuario_id: int
    dispositivo: str
    user_agent: Optional[str] = None
```

### 2.2. Agregar endpoints
Buscar el endpoint `@app.post("/login")` (línea ~642)  
**DESPUÉS del endpoint completo de login**, agregar estos dos nuevos endpoints:

```python
@app.post("/actualizar_dispositivo")
async def actualizar_dispositivo(datos: DispositivoUpdate):
    """Actualiza el dispositivo del usuario al hacer login"""
    try:
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="Error de conexión a base de datos")
        
        cursor.execute("""
            UPDATE usuarios 
            SET dispositivo = %s, 
                user_agent = %s,
                ultimo_acceso = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (datos.dispositivo, datos.user_agent, datos.usuario_id))
        
        conn.commit()
        
        return {"success": True, "message": "Dispositivo actualizado"}
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al actualizar dispositivo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/estadisticas/dispositivos")
async def estadisticas_dispositivos():
    """Obtiene estadísticas de dispositivos en tiempo real"""
    try:
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="Error de conexión a base de datos")
        
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT 
                COALESCE(dispositivo, 'desconocido') as dispositivo,
                COUNT(*) as cantidad,
                ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM usuarios), 0), 2) as porcentaje
            FROM usuarios
            GROUP BY dispositivo
            ORDER BY cantidad DESC
        """)
        dispositivos = cursor.fetchall()
        
        cursor.execute("""
            SELECT 
                rol,
                COALESCE(dispositivo, 'desconocido') as dispositivo,
                COUNT(*) as cantidad
            FROM usuarios
            GROUP BY rol, dispositivo
            ORDER BY rol, cantidad DESC
        """)
        por_rol = cursor.fetchall()
        
        return {
            "total_usuarios": total,
            "por_dispositivo": [
                {"dispositivo": d[0], "cantidad": d[1], "porcentaje": float(d[2])}
                for d in dispositivos
            ],
            "por_rol": [
                {"rol": r[0], "dispositivo": r[1], "cantidad": r[2]}
                for r in por_rol
            ]
        }
    except Exception as e:
        print(f"❌ Error al obtener estadísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### 2.3. Modificar endpoint de login
Dentro del endpoint `@app.post("/login")`, buscar la línea del `return` (línea ~670)  
**ANTES del return**, agregar:

```python
    # Actualizar último acceso
    try:
        cursor.execute("""
            UPDATE usuarios 
            SET ultimo_acceso = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (user[0],))
        conn.commit()
    except Exception as e:
        print(f"⚠️ Error al actualizar último acceso: {e}")
```

---

## 📋 PASO 3: Actualizar Frontend (Login.vue)

Abrir: `pwasuper/src/views/Login.vue`

### 3.1. Agregar funciones de detección
Después de los imports y antes de las variables (alrededor línea 50), agregar:

```javascript
/**
 * Detecta el tipo de dispositivo del usuario
 */
function detectarDispositivo() {
  const userAgent = navigator.userAgent || navigator.vendor || window.opera;
  
  if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
    return 'iOS';
  }
  
  if (/android/i.test(userAgent)) {
    return 'Android';
  }
  
  if (/Windows|Macintosh|Linux/.test(userAgent)) {
    return 'Desktop';
  }
  
  return 'Desconocido';
}

/**
 * Envía información del dispositivo al backend
 */
async function enviarInfoDispositivo(usuarioId) {
  try {
    const dispositivo = detectarDispositivo();
    const userAgent = navigator.userAgent;
    
    await axios.post(`${currentApiUrl.value}/actualizar_dispositivo`, {
      usuario_id: usuarioId,
      dispositivo: dispositivo,
      user_agent: userAgent
    });
    
    console.log(`📱 Dispositivo registrado: ${dispositivo}`);
  } catch (error) {
    console.warn('⚠️ No se pudo actualizar el dispositivo:', error);
  }
}
```

### 3.2. Modificar handleLogin
Buscar dentro de `async function handleLogin` donde dice:  
`localStorage.setItem('user', JSON.stringify(userData));`

**JUSTO DESPUÉS de esa línea**, agregar:

```javascript
    // Enviar información del dispositivo
    enviarInfoDispositivo(userData.id).catch(err => 
      console.warn('No se pudo registrar dispositivo:', err)
    );
```

---

## 📋 PASO 4: Desplegar Cambios

### 4.1. Backend
```bash
cd /var/www/PWASV/admin-pwa
git add backend/main.py
git commit -m "Agregar tracking de dispositivos"
git push origin main

# Reiniciar backend
sudo systemctl restart fastapi-backend  # o el servicio que uses
```

### 4.2. Frontend (pwasuper)
```bash
cd /var/www/PWASV/pwasuper
git add src/views/Login.vue
git commit -m "Agregar detección de dispositivo en login"
git push origin main

npm run build
sudo cp -r dist/* /var/www/app.sembrandodatos.com/
```

---

## 📊 PASO 5: Ver Estadísticas

### Opción 1: Script de Python

```bash
cd /var/www/PWASV/admin-pwa/backend
python3 estadisticas_tiempo_real.py
```

**Modo monitor (actualización continua):**
```bash
python3 estadisticas_tiempo_real.py --monitor
# o cada 10 segundos:
python3 estadisticas_tiempo_real.py --monitor 10
```

### Opción 2: API REST

```bash
curl https://apipwa.sembrandodatos.com/estadisticas/dispositivos
```

### Opción 3: SQL directo

```bash
psql -h 31.97.8.51 -U jesus -d app_registros
```

```sql
-- Ver distribución por dispositivo
SELECT 
    COALESCE(dispositivo, 'Desconocido') as dispositivo,
    COUNT(*) as cantidad,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM usuarios), 2) as porcentaje
FROM usuarios
GROUP BY dispositivo
ORDER BY cantidad DESC;

-- Ver por rol
SELECT rol, dispositivo, COUNT(*) 
FROM usuarios 
GROUP BY rol, dispositivo 
ORDER BY rol, COUNT(*) DESC;

-- Últimos accesos
SELECT nombre_completo, dispositivo, ultimo_acceso 
FROM usuarios 
WHERE ultimo_acceso IS NOT NULL 
ORDER BY ultimo_acceso DESC 
LIMIT 20;
```

---

## 🎯 Resultado Esperado

Una vez implementado, verás algo como:

```
📊 ESTADÍSTICAS DE USUARIOS POR PLATAFORMA
=================================================================

📱 TOTAL DE USUARIOS REGISTRADOS: 1247

DISTRIBUCIÓN POR DISPOSITIVO:
-----------------------------------------------------------------
🤖 Android         856 usuarios ( 68.64%) ████████████████████████████████
🍎 iOS             289 usuarios ( 23.17%) ███████████
💻 Desktop          87 usuarios (  6.98%) ███
❓ Desconocido      15 usuarios (  1.20%) 

DISTRIBUCIÓN POR ROL Y DISPOSITIVO:
-----------------------------------------------------------------
📋 TÉCNICO:
  🤖 Android      748 usuarios
  🍎 iOS          198 usuarios
  💻 Desktop       45 usuarios
```

---

## ✅ Checklist de Verificación

- [ ] Base de datos actualizada con nuevas columnas
- [ ] Backend con nuevo modelo y endpoints
- [ ] Frontend enviando info de dispositivo en login
- [ ] Cambios desplegados en producción
- [ ] Script de estadísticas funcionando
- [ ] Datos apareciendo en las consultas

---

## 🚨 Troubleshooting

### "Column 'dispositivo' does not exist"
- Ejecutar nuevamente el SQL del Paso 1

### "No se actualiza el dispositivo"
- Verificar que el endpoint `/actualizar_dispositivo` existe en el backend
- Revisar la consola del navegador para ver si hay errores
- Verificar que el frontend esté llamando a la función

### "Todos aparecen como 'desconocido'"
- Los usuarios necesitan volver a hacer login para que se registre su dispositivo
- O puedes forzar una actualización ejecutando un script de migración

---

## 📝 Notas

- La info del dispositivo se actualiza **cada vez que el usuario hace login**
- Los usuarios existentes aparecerán como "desconocido" hasta su próximo login
- El campo `ultimo_acceso` te permite ver usuarios activos vs inactivos
- El `user_agent` completo se guarda para análisis más detallados si lo necesitas

---

## 🔗 Archivos Creados

1. `backend/agregar_dispositivo.sql` - SQL para actualizar BD
2. `backend/CODIGO_DISPOSITIVOS_BACKEND.py` - Código del backend
3. `pwasuper/CODIGO_DISPOSITIVOS_FRONTEND.js` - Código del frontend
4. `backend/estadisticas_tiempo_real.py` - Script de estadísticas
5. `GUIA_ESTADISTICAS_DISPOSITIVOS.md` - Esta guía

---

¿Necesitas ayuda con algún paso? 🚀
