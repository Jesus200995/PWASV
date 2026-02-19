# 🚀 DESPLIEGUE MANUAL - SUPER SIMPLE

## Ejecuta estos comandos UNO POR UNO:

### 1️⃣ Conectarse al servidor

```bash
ssh root@31.97.8.51
```

Ingresa la contraseña del VPS.

---

### 2️⃣ Encontrar el archivo main.py

```bash
find /root /home -name 'main.py' -type f 2>/dev/null | grep -v node_modules
```

Copia la ruta que te muestre (ejemplo: `/root/backend/main.py`)

---

### 3️⃣ Hacer backup

Reemplaza `/ruta/al/main.py` con la ruta que encontraste:

```bash
cp /ruta/al/main.py /ruta/al/main.py.backup_$(date +%Y%m%d_%H%M%S)
```

Ejemplo:
```bash
cp /root/backend/main.py /root/backend/main.py.backup_$(date +%Y%m%d_%H%M%S)
```

---

### 4️⃣ Ver la línea que vamos a cambiar

```bash
grep -n "join.*condiciones" /ruta/al/main.py
```

Deberías ver algo como:
```
6436:    WHERE {' AND '.join(condiciones)}
```

---

### 5️⃣ Hacer el cambio (AND → OR)

**OPCIÓN A: Con sed (automático)**

```bash
sed -i "s/WHERE {' AND '.join(condiciones)}/WHERE {' OR '.join(condiciones)}/g" /ruta/al/main.py
```

**OPCIÓN B: Con nano (manual)**

```bash
nano /ruta/al/main.py
```

Busca la línea (Ctrl+W): `WHERE {' AND '.join`
Cambia `AND` por `OR`
Guarda (Ctrl+O) y sal (Ctrl+X)

---

### 6️⃣ Verificar el cambio

```bash
grep -n "OR.*join.*condiciones" /ruta/al/main.py
```

Deberías ver:
```
6436:    WHERE {' OR '.join(condiciones)}
```

✅ Si ves `OR`, el cambio está correcto!

---

### 7️⃣ Reiniciar el servicio

Prueba estos comandos EN ORDEN hasta que uno funcione:

```bash
# Opción 1: PM2
pm2 restart all

# Opción 2: Systemctl
systemctl restart pwa-backend

# Opción 3: Systemctl alternativo
systemctl restart uvicorn

# Opción 4: Manual
# Primero ver el proceso actual
ps aux | grep -E '[u]vicorn|[p]ython.*main'

# Matar el proceso (reemplaza XXXX con el PID que viste arriba)
kill XXXX

# Iniciar de nuevo (ajusta la ruta)
cd /ruta/al/backend
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
```

---

### 8️⃣ Verificar que esté corriendo

```bash
ps aux | grep -E '[u]vicorn|[p]ython.*main'
```

Deberías ver el proceso activo.

---

## ✅ VERIFICACIÓN FINAL

Una vez completado, sal del servidor (`exit`) y:

### 1. Inicia el admin local

```bash
cd admin-pwa
npm run dev
```

### 2. Abre la página de debug

```
http://localhost:5173/#/debug-buscador
```

### 3. Prueba la búsqueda

1. Ingresa: `ROCR820619MSLJSB05`
2. Click en "🔍 Buscar"
3. Deberías ver:
   - ✅ Usuarios encontrados: 1 (o más)
   - ✅ Registros recibidos: X

---

## 🆘 SI ALGO FALLA

### No encuentra main.py

Busca más ampliamente:
```bash
find / -name 'main.py' 2>/dev/null | grep -E 'backend|pwa|api'
```

### No puede reiniciar el servicio

Ver qué servicios hay:
```bash
systemctl list-units --type=service | grep -E 'pwa|backend|uvicorn'
pm2 list
supervisorctl status
```

### El proceso no arranca

Ver logs:
```bash
# Si usa systemd:
journalctl -u pwa-backend -f

# Si usa PM2:
pm2 logs

# Si corre manual:
tail -f /ruta/al/nohup.out
```

---

## ⏱️ TIEMPO ESTIMADO: 5 MINUTOS

¡Todo listo! Ejecuta los comandos paso a paso 👆
