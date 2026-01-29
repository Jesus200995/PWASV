# 📋 RECORDATORIO: Proceso de Git para Cada Implementación

## ✅ PASOS OBLIGATORIOS DESPUÉS DE CADA CAMBIO

### 1. **Verificar Cambios Locales**
```powershell
git status
```

### 2. **Agregar Archivos Modificados**
```powershell
# Agregar archivos específicos
git add backend/main.py
git add admin-pwa/src/views/NombreArchivo.vue
git add pwasuper/src/views/OtroArchivo.vue

# O agregar todos los cambios (usar con cuidado)
git add .
```

### 3. **Hacer Commit con Mensaje Descriptivo**
```powershell
git commit -m "Tipo: Descripción clara del cambio

- Detalle 1
- Detalle 2
- Detalle 3"
```

**Tipos de commit:**
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bugs
- `chore:` Tareas de mantenimiento
- `refactor:` Refactorización de código
- `docs:` Documentación

### 4. **Pushear al Repositorio Remoto**
```powershell
git push origin main
```

### 5. **Actualizar Servidor de Producción**
```powershell
# Opción 1: Via Git (recomendado si hay .gitignore configurado)
ssh root@31.97.8.51 "cd /var/www/PWASV && git pull origin main"

# Opción 2: Via SCP (para archivos específicos)
scp ruta/local/archivo root@31.97.8.51:/var/www/PWASV/ruta/destino

# Opción 3: Reiniciar servicios si es necesario
ssh root@31.97.8.51 "sudo systemctl restart apipwa && sudo systemctl reload nginx"
```

---

## 🔄 FLUJO COMPLETO DE TRABAJO

```powershell
# 1. Hacer cambios en el código
# 2. Probar localmente
# 3. Agregar a Git
git add .

# 4. Commit
git commit -m "feat: descripción del cambio"

# 5. Push
git push origin main

# 6. Actualizar servidor
ssh root@31.97.8.51 "cd /var/www/PWASV && git reset --hard origin/main && git pull origin main"

# 7. Reiniciar servicios si es backend
ssh root@31.97.8.51 "sudo systemctl restart apipwa"

# 8. Deploy frontend si es necesario
cd admin-pwa
npm run build
scp -r dist/* root@31.97.8.51:/var/www/html/admin-pwa/

cd ../pwasuper
npm run build
scp -r dist/* root@31.97.8.51:/var/www/html/pwasuper/
```

---

## 📁 ARCHIVOS IGNORADOS (.gitignore)

Ya están configurados para ignorar:
- ✅ `backend/fotos/` - Fotos de usuarios
- ✅ `node_modules/` - Dependencias
- ✅ `dist/` - Builds compilados
- ✅ `venv/` - Entorno virtual Python
- ✅ `*.log` - Archivos de log
- ✅ `.vscode/` - Configuración del IDE

---

## ⚠️ IMPORTANTE

1. **SIEMPRE** hacer commit después de cambios funcionales
2. **SIEMPRE** pushear al repositorio remoto
3. **SIEMPRE** actualizar el servidor después del push
4. **NUNCA** modificar directamente en el servidor (excepto emergencias)
5. **VERIFICAR** que el servidor esté sincronizado antes de nuevos cambios

---

## 🚨 SOLUCIÓN A PROBLEMAS COMUNES

### Conflicto de merge en el servidor
```powershell
ssh root@31.97.8.51 "cd /var/www/PWASV && git reset --hard origin/main && git pull origin main"
```

### Archivos no trackeados masivamente
```powershell
# Ya resuelto con .gitignore
# Si persiste, agregar al .gitignore y hacer commit
```

### Servidor desactualizado
```powershell
ssh root@31.97.8.51 "cd /var/www/PWASV && git fetch origin && git reset --hard origin/main"
```

---

## 📊 VERIFICACIÓN POST-DEPLOYMENT

```powershell
# Ver últimos commits locales
git log --oneline -5

# Ver últimos commits en servidor
ssh root@31.97.8.51 "cd /var/www/PWASV && git log --oneline -5"

# Verificar que coincidan
# Verificar servicios activos
ssh root@31.97.8.51 "systemctl status apipwa"
```

---

**Última actualización:** 29 de enero de 2026
**Repositorio:** https://github.com/Jesus200995/PWASV
**Servidor:** 31.97.8.51
