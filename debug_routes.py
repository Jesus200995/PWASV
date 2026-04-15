import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

# Busca rutas con path patterns avanzados
_, o, _ = ssh.exec_command("grep -n '@app\\.' /var/www/PWASV/main.py | grep -i 'reportes' | head -30")
print(o.read().decode())

print('\n=== Todas las rutas de reportes (todos los métodos) ===')
_, o2, _ = ssh.exec_command("grep -n '@app\\.' /var/www/PWASV/main.py | grep reportes")
print(o2.read().decode())

# Intentar curl con verbose para ver qué pasa
_, o3, _ = ssh.exec_command("curl -v http://127.0.0.1:8000/reportes/facilitador/mis-reportes?admin_id=1 2>&1 | tail -20")
print('\ncurl verbose:')
print(o3.read().decode())

ssh.close()
