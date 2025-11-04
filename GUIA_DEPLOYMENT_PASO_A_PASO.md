# 🚀 Guía de Deployment - Sistema Anti-Fraude CDMX

**Fecha:** 4 de Noviembre 2025  
**Ambiente:** Producción  
**Riesgo:** BAJO (sin cambios en BD)  
**Tiempo Estimado:** 15-30 minutos

---

## 📋 Pre-Deployment

### 1. Backup de Base de Datos
```bash
# En el servidor VPS (Linux/Ubuntu)
pg_dump -U postgres -d asistencias > backup_$(date +%Y%m%d_%H%M%S).sql
ls -lh backup_*.sql
```

### 2. Backup del Código Actual
```bash
# Backend
cd /ruta/backend
cp -r . ../backup_backend_$(date +%Y%m%d)

# Frontend
cd /ruta/pwasuper
cp -r . ../backup_pwasuper_$(date +%Y%m%d)
```

### 3. Verificar Servicios Activos
```bash
# Ver estado del servidor
ps aux | grep python
ps aux | grep npm

# Ver puertos
lsof -i :8000  # Backend
lsof -i :5173  # Frontend dev
lsof -i :80    # Nginx
```

---

## 🔧 Deployment del Backend

### Paso 1: Actualizar main.py
```bash
# En VS Code: Copiar el main.py actualizado

# En servidor: Reemplazar archivo
cd /ruta/backend
cp main.py main.py.backup
# Pegar el contenido nuevo
```

### Paso 2: Verificar Sintaxis Python
```bash
# En servidor
cd /ruta/backend
python3 -m py_compile main.py
# No debe mostrar errores
```

### Paso 3: Instalar Dependencias
```bash
# Si fastapi o pytz no están instaladas
pip install fastapi pytz
pip install -r requirements.txt
```

### Paso 4: Reiniciar Servidor Backend
```bash
# Opción A: Si usa supervisord
sudo supervisorctl restart pwasuper_backend

# Opción B: Si usa systemd
sudo systemctl restart pwasuper

# Opción C: Manual (kill y restart)
pkill -f "python.*main.py"
cd /ruta/backend
nohup python3 main.py > backend.log 2>&1 &
```

### Paso 5: Verificar Backend Activo
```bash
# Verificar puerto
lsof -i :8000

# Hacer request de prueba
curl http://localhost:8000/health

# O desde otra máquina
curl http://IP_SERVIDOR:8000/health

# Verificar nuevo endpoint
curl http://localhost:8000/validar/sincronizacion-reloj
# Debe retornar JSON con timestamps
```

---

## 🎨 Deployment del Frontend

### Paso 1: Actualizar Archivos Vue
```bash
# En VS Code: 
# 1. Actualizar Home.vue
# 2. Actualizar offlineService.js
# 3. Actualizar syncService.js

# Copiar a servidor o usar git
```

### Paso 2: Build del Frontend
```bash
# En servidor (carpeta pwasuper)
cd /ruta/pwasuper
npm run build
# Debe completar sin errores
# Genera carpeta dist/
```

### Paso 3: Verificar Build
```bash
# Verificar que se creó dist/
ls -la dist/

# Verificar tamaño
du -sh dist/

# Verificar archivos clave
ls -la dist/index.html
ls -la dist/js/
```

### Paso 4: Desplegar Frontend
```bash
# Opción A: Si usa Apache
cp -r dist/* /var/www/html/pwasuper/

# Opción B: Si usa Nginx
cp -r dist/* /usr/share/nginx/html/pwasuper/

# Opción C: Si usa otro servidor
cp -r dist/* /ruta/servidor/public/
```

### Paso 5: Verificar Permisos
```bash
# Asegurar permisos correctos
sudo chown -R www-data:www-data /ruta/destino
sudo chmod -R 755 /ruta/destino
```

---

## ✅ Validación Post-Deployment

### Test 1: Frontend Carga Correctamente
```bash
# En navegador
http://IP_SERVIDOR/pwasuper
# Debe cargar sin errores
# Consola: F12 → No debe haber errores rojos
```

### Test 2: Endpoint Anti-Fraude Funciona
```bash
# Desde terminal o Postman
curl -X GET http://localhost:8000/validar/sincronizacion-reloj

# Respuesta esperada:
{
  "servidor_timestamp_cdmx": "2025-11-04T14:30:45.123-06:00",
  "servidor_timestamp_utc": "2025-11-04T20:30:45.123Z",
  "servidor_hora_legible": "14:30:45",
  "servidor_fecha": "2025-11-04",
  "zona_horaria": "America/Mexico_City"
}
```

### Test 3: Marca de Entrada (Online)
```bash
# En navegador
1. Abrir PWA
2. Hacer login
3. Click en botón "Marcar Entrada"
4. Seleccionar entrada (Oficina)
5. Tomar foto
6. Click "Confirmar"
7. Ver respuesta en servidor
```

**En servidor verificar:**
```bash
# Ver logs del backend
tail -f backend.log | grep "Enviando timestamp CDMX"
# Debe mostrar: ✅ timestamp procesado
```

### Test 4: Marca Offline + Sync
```bash
# En navegador
1. Desconectar internet (o usar DevTools)
2. Marcar entrada offline
3. Verificar que se guardó
4. Reconectar internet
5. Sincronizar
6. Verificar que se registró correctamente
```

**En servidor verificar:**
```bash
# Ver logs de sincronización
tail -f backend.log | grep "timestamp_cdmx"
# Debe usar timestamp original, no actual
```

### Test 5: Anti-Fraude
```bash
# Simular timestamp sospechoso
# (Requiere acceso a cliente para modificar DateTimeFormat)

# O verificar en logs:
tail -f backend.log | grep "ALERTA"
tail -f backend.log | grep "RECHAZO"
```

---

## 🔍 Verificación de Logs

### Backend Logs
```bash
# Ver últimas líneas
tail -20 /ruta/backend/backend.log

# Ver stream en vivo
tail -f /ruta/backend/backend.log

# Filtrar por anti-fraude
grep "ALERTA" /ruta/backend/backend.log
grep "RECHAZO" /ruta/backend/backend.log
grep "Validación anti-fraude" /ruta/backend/backend.log

# Ver errores
grep "ERROR" /ruta/backend/backend.log
grep "Exception" /ruta/backend/backend.log
```

### Frontend Logs
```bash
# En navegador: F12 → Console
# Buscar mensajes con 📌
# "📌 Enviando timestamp CDMX: ..."
# "📌 Timestamp CDMX para offline: ..."
```

---

## 🆘 Rollback en Caso de Error

### Si el backend falla
```bash
# Restaurar backup
cd /ruta/backend
cp main.py.backup main.py

# Reiniciar
sudo systemctl restart pwasuper
```

### Si el frontend falla
```bash
# Restaurar build anterior
cp -r ../backup_pwasuper_YYYYMMDD/dist/* /ruta/destino/

# O reconstruir desde backup
cd ../backup_pwasuper_YYYYMMDD
npm run build
cp -r dist/* /ruta/destino/
```

### Si hay problemas con BD
```bash
# Restaurar backup
psql -U postgres -d asistencias < backup_YYYYMMDD_HHMMSS.sql
```

---

## 📊 Monitoreo Post-Deploy

### Dashboard de Monitoreo
```bash
# Ver procesamiento en vivo
watch -n 5 'tail -20 /ruta/backend/backend.log'

# Contar intentos de fraude
grep "RECHAZO" /ruta/backend/backend.log | wc -l

# Ver promedio de validaciones/hora
grep "Validación anti-fraude" /ruta/backend/backend.log | wc -l
```

### Alertas Automáticas
```bash
# Crear script de alerta
cat > /ruta/check_fraud.sh << 'EOF'
#!/bin/bash

FRAUD_COUNT=$(grep "RECHAZO" /ruta/backend/backend.log | tail -100 | wc -l)

if [ $FRAUD_COUNT -gt 5 ]; then
  echo "ALERTA: $FRAUD_COUNT intentos de fraude detectados en últimas 2 horas"
  # Enviar email o notificación
  # mail -s "Alerta Fraude PWA" admin@domain.com
fi
EOF

chmod +x /ruta/check_fraud.sh

# Ejecutar cada 30 minutos
*/30 * * * * /ruta/check_fraud.sh
```

---

## 📝 Comandos Rápidos de Referencia

### Ver estado general
```bash
# Sistema operativo
uname -a

# Espacio disco
df -h

# Memoria
free -h

# Procesos Python
ps aux | grep python

# Conexiones activas
netstat -tulpn | grep LISTEN
```

### Reiniciar servicios
```bash
# Nginx
sudo systemctl restart nginx

# Backend
sudo systemctl restart pwasuper

# Ambos
sudo systemctl restart nginx pwasuper
```

### Ver logs integrados
```bash
# Todos los logs
journalctl -u pwasuper -f

# Nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# Syslog
tail -f /var/log/syslog
```

---

## ✅ Checklist Final Deployment

- [ ] Backup de BD realizado
- [ ] Backup de código realizado
- [ ] main.py actualizado
- [ ] Verificación sintaxis Python OK
- [ ] Backend reiniciado
- [ ] Frontend build exitoso
- [ ] Frontend desplegado
- [ ] Endpoint validación responde
- [ ] Test marca entrada OK
- [ ] Test marca offline OK
- [ ] Logs sin errores
- [ ] Anti-fraude funciona
- [ ] Performance normal
- [ ] Monitores configurados

---

## 📞 Soporte

Si hay problemas:

1. **Verificar logs:** `tail -f backend.log`
2. **Revisar validación:** `curl localhost:8000/validar/sincronizacion-reloj`
3. **Test endpoint:** `curl localhost:8000/health`
4. **Rollback si necesario:** `cp main.py.backup main.py`

---

**Status Deployment:** ✅ LISTO  
**Riesgo:** BAJO  
**Rollback:** FÁCIL (< 5 minutos)

