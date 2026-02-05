# Sistema de Desactivación de Cuentas de Usuarios

## 📋 Resumen

Se implementó la funcionalidad para desactivar/activar cuentas de usuarios desde el panel administrativo. Los usuarios desactivados no podrán iniciar sesión en la aplicación.

## ✨ Características Implementadas

### Frontend (admin-pwa)

1. **Nuevo botón en UsuariosView.vue**
   - Ubicación: Columna "Acciones" en la tabla de usuarios
   - Funcionalidad: Toggle entre activar/desactivar cuenta
   - Estilos:
     - Botón gris con icono de "prohibido" para desactivar
     - Botón verde con icono de "check" para activar
     - Animaciones y efectos hover

2. **Servicio actualizado (usuariosService.js)**
   - Nuevo método: `cambiarEstadoUsuario(id, activo)`
   - Endpoint: `PATCH /admin/usuarios/{id}/estado`
   - Manejo de cache actualizado

### Backend (main.py)

1. **Nuevo endpoint**
   ```python
   @app.patch("/admin/usuarios/{user_id}/estado")
   async def cambiar_estado_usuario(user_id: int, datos: dict)
   ```
   - Parámetros: `{ "activo": true/false }`
   - Validaciones: Verifica que el usuario exista
   - Respuesta: Estado actualizado

2. **Columna en base de datos**
   - Tabla: `usuarios`
   - Columna: `activo BOOLEAN DEFAULT TRUE`
   - Ya existe en tabla `admin_users`

## 🗄️ Migración de Base de Datos

### Opción 1: Usando script Python (Recomendado)

```bash
cd backend
python agregar_columna_activo_usuarios.py
```

El script:
- Verifica si la columna ya existe
- Agrega la columna si no existe
- Actualiza registros existentes a `activo = TRUE`
- Muestra estadísticas de usuarios

### Opción 2: Usando script SQL directo

```bash
# Conectar a la base de datos
psql -h 31.97.8.51 -U jesus -d app_registros

# Ejecutar el script
\i backend/agregar_columna_activo_usuarios.sql
```

### Opción 3: Comando SQL manual

```sql
-- Agregar columna
ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE;

-- Actualizar registros existentes
UPDATE usuarios SET activo = TRUE WHERE activo IS NULL;

-- Verificar
SELECT COUNT(*) FILTER (WHERE activo = TRUE) as activos,
       COUNT(*) FILTER (WHERE activo = FALSE) as inactivos
FROM usuarios;
```

## 📝 Uso en el Panel Administrativo

1. Ir a **Gestión de Usuarios**
2. En la columna "Acciones", buscar el nuevo botón:
   - **Gris** = Usuario activo → Click para desactivar
   - **Verde** = Usuario inactivo → Click para activar

3. Al hacer click:
   - Se muestra confirmación
   - Se actualiza el estado en la base de datos
   - Se actualiza la interfaz automáticamente

## 🔒 Comportamiento de Usuarios Desactivados

- ❌ **No pueden iniciar sesión** en la aplicación
- ✅ **Se mantienen en la base de datos** (no se eliminan)
- ✅ **Se pueden reactivar** en cualquier momento
- ✅ **Mantienen todos sus datos** (registros, asistencias, reportes)

## 🎨 Estilos CSS Añadidos

```css
.btn-toggle { /* Botón base */ }
.btn-desactivar { /* Botón gris para desactivar */ }
.btn-activar { /* Botón verde para activar */ }
.btn-label-desactivar { /* Texto "Desactivar" */ }
.btn-label-activar { /* Texto "Activar" */ }
```

## 📁 Archivos Modificados

### Frontend
- `admin-pwa/src/views/UsuariosView.vue`
  - Línea ~220: Nuevo botón en HTML
  - Línea ~1685: Nueva función `toggleEstadoUsuario()`
  - Línea ~3100: Nuevos estilos CSS

- `admin-pwa/src/services/usuariosService.js`
  - Línea ~330: Nuevo método `cambiarEstadoUsuario()`

### Backend
- `backend/main.py`
  - Línea ~6870: Nuevo endpoint `@app.patch("/admin/usuarios/{user_id}/estado")`

### Nuevos Archivos
- `backend/agregar_columna_activo_usuarios.sql`
- `backend/agregar_columna_activo_usuarios.py`

## 🚀 Pasos para Despliegue

1. **Ejecutar migración de base de datos**
   ```bash
   python backend/agregar_columna_activo_usuarios.py
   ```

2. **Reiniciar backend**
   ```bash
   cd backend
   # Matar proceso actual
   pkill -f "python.*main.py"
   # Iniciar nuevo proceso
   nohup python main.py > backend.log 2>&1 &
   ```

3. **Reconstruir frontend**
   ```bash
   cd admin-pwa
   npm run build
   ```

4. **Verificar funcionalidad**
   - Acceder al panel administrativo
   - Ir a Gestión de Usuarios
   - Probar desactivar/activar un usuario de prueba

## ⚠️ Notas Importantes

- La columna `activo` ya existe en la tabla `admin_users` (usuarios administrativos)
- Esta implementación añade la misma columna a la tabla `usuarios` (usuarios regulares)
- El valor por defecto es `TRUE` (activo) para mantener compatibilidad
- Los usuarios existentes se marcan como activos automáticamente

## 🔍 Debugging

### Verificar estado en la base de datos
```sql
-- Ver todos los usuarios con su estado
SELECT id, nombre_completo, correo, activo 
FROM usuarios 
ORDER BY id DESC 
LIMIT 10;

-- Contar usuarios por estado
SELECT 
  activo,
  COUNT(*) as cantidad
FROM usuarios
GROUP BY activo;
```

### Verificar logs del backend
```bash
tail -f backend.log | grep "estado"
```

## ✅ Checklist de Implementación

- [x] Endpoint backend creado
- [x] Servicio frontend actualizado
- [x] Botón en interfaz añadido
- [x] Estilos CSS implementados
- [x] Scripts de migración creados
- [x] Documentación generada
- [ ] Migración de BD ejecutada en VPS
- [ ] Pruebas funcionales realizadas
- [ ] Backend reiniciado
- [ ] Frontend reconstruido

## 📞 Soporte

Si encuentras algún problema:
1. Verifica que la columna `activo` existe en la tabla `usuarios`
2. Revisa los logs del backend para errores
3. Verifica la consola del navegador para errores del frontend
