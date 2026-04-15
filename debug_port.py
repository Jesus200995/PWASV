import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

# Ver qué proceso está escuchando en puerto 8000
_, o, _ = ssh.exec_command("ss -tlnp | grep 8000")
print("Puerto 8000:", o.read().decode())

# Ver el servicio systemd para saber cómo inicia
_, o2, _ = ssh.exec_command("cat /etc/systemd/system/apipwa.service")
print("\nServicio:", o2.read().decode())

# Ver el archivo que está usando el proceso
_, o3, _ = ssh.exec_command("ls -la /proc/$(pgrep -f 'uvicorn main' | head -1)/exe 2>/dev/null; ls /var/www/PWASV/ | head -10")
print("\nArchivos:", o3.read().decode())

ssh.close()
