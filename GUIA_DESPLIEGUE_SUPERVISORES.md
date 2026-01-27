# ========================================
# GUÍA DE DESPLIEGUE MANUAL AL VPS
# ========================================

## PROBLEMA IDENTIFICADO
Los territorios con "/" en el nombre (Chihuahua / Sonora, Durango / Zacatecas, etc.) 
están generando ERROR HTTP 405 porque el endpoint del backend no maneja correctamente 
las barras en la ruta.

## SOLUCIÓN APLICADA LOCALMENTE
Se cambió el endpoint en backend/main.py línea 6888:
- ANTES: @app.get("/supervisor-territorio/{territorio}")
- AHORA: @app.get("/supervisor-territorio/{territorio:path}")

El modificador `:path` permite que FastAPI maneje correctamente las barras "/" en los parámetros de ruta.

## DESPLIEGUE AL VPS

### Opción 1: Usando SCP (Recomendado)
```powershell
# 1. Copiar archivo actualizado al VPS
scp backend/main.py root@31.97.8.51:/root/pwa-backend/

# 2. Conectarse al VPS
ssh root@31.97.8.51

# 3. Reiniciar servicio del backend
systemctl restart apipwa

# 4. Verificar que el servicio está corriendo
systemctl status apipwa

# 5. Ver logs en tiempo real (opcional)
journalctl -u apipwa -f
```

### Opción 2: Usando Python Script
```powershell
python desplegar_backend.py
```

### Opción 3: Manual con WinSCP o FileZilla
1. Conectarse al servidor: 31.97.8.51
2. Usuario: root
3. Navegar a: /root/pwa-backend/
4. Reemplazar main.py con la versión local de: backend/main.py
5. Ejecutar en terminal SSH: systemctl restart apipwa

## VERIFICACIÓN POST-DESPLIEGUE

### 1. Verificar que todos los territorios devuelven supervisores
```powershell
python verificar_supervisores_territoriales.py
```

Resultado esperado:
- ✅ 31/31 territorios CON supervisor
- ❌ 0/31 territorios SIN supervisor
- ⚠️ 0 errores HTTP 405

### 2. Ejecutar actualización masiva de supervisores
```powershell
python actualizar_supervisores_tecnicos.py
```

Este script:
- Busca TODOS los técnicos (TECNICO SOCIAL y TECNICO PRODUCTIVO)
- Les asigna automáticamente el supervisor según su territorio
- Muestra estadísticas de actualización

### 3. Verificar en PWA/Admin
- Entrar a admin-pwa
- Ver usuarios técnicos
- Verificar que tengan supervisor asignado
- Especialmente revisar usuarios de territorios:
  * Chihuahua / Sonora
  * Durango / Zacatecas
  * Nayarit / Jalisco
  * Tlaxcala / Estado de México
  * Tzucacab / Opb

## RESUMEN DE CAMBIOS REALIZADOS

### Backend (main.py)
✅ Línea 6888: Cambio de {territorio} a {territorio:path}
✅ Línea 6790: Endpoint POST /actualizar-supervisores-tecnicos

### Administradores Territoriales Creados (7)
✅ Acayucan - admin.acayucan@sembrandovida.gob.mx
✅ Chihuahua / Sonora - admin.chihuahuasonora@sembrandovida.gob.mx
✅ Durango / Zacatecas - admin.durangozacatecas@sembrandovida.gob.mx
✅ Nayarit / Jalisco - admin.nayaritjalisco@sembrandovida.gob.mx
✅ Tlaxcala / Estado de México - admin.tlaxcalaedomex@sembrandovida.gob.mx
✅ Tzucacab / Opb - admin.tzucacab@sembrandovida.gob.mx
✅ Oficinas Centrales - admin.centrales@sembrandovida.gob.mx

Contraseñas: Ver archivo crear_admins_faltantes.py líneas 13-55

### Scripts Creados
✅ crear_admins_faltantes.py - Crea los 7 admins territoriales
✅ verificar_supervisores_territoriales.py - Verifica todos los territorios
✅ actualizar_supervisores_tecnicos.py - Actualización masiva
✅ desplegar_backend.py - Automatiza despliegue al VPS

## NOTAS IMPORTANTES

1. Los cambios del backend están SOLO en local hasta que se desplieguen al VPS
2. Los 7 administradores territoriales YA ESTÁN creados en producción
3. Una vez desplegado el backend, los territorios con "/" funcionarán
4. Después del despliegue, ejecutar actualizar_supervisores_tecnicos.py

## CONTACTO SOPORTE
Si hay problemas con el despliegue:
- Verificar acceso SSH al VPS
- Verificar que el servicio apipwa existe: systemctl list-units | grep apipwa
- Verificar ruta del backend: ls -la /root/pwa-backend/
- Ver logs: journalctl -u apipwa --since "10 minutes ago"
