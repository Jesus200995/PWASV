import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

# Busca el nuevo endpoint en el archivo en VPS
_, o, _ = ssh.exec_command("grep -n 'mis-reportes\\|mis-tecnicos\\|facilitador_tecnico_asig' /var/www/PWASV/main.py | head -20")
print(o.read().decode())

# Ver que rutas GET de reportes tienen el VPS
_, o2, _ = ssh.exec_command("grep -n '@app.get' /var/www/PWASV/main.py | grep reportes")
print('\nRutas GET reportes:')
print(o2.read().decode())

ssh.close()
