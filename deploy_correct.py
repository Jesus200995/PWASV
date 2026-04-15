import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

sftp = ssh.open_sftp()
sftp.put('backend/main.py', '/var/www/PWASV/backend/main.py')
sftp.close()
print('main.py subido a /var/www/PWASV/backend/main.py')

_, o, e = ssh.exec_command('systemctl restart apipwa')
print('restart:', o.read().decode(), e.read().decode())
time.sleep(5)

_, o2, _ = ssh.exec_command('systemctl is-active apipwa')
print('estado:', o2.read().decode().strip())

time.sleep(2)
_, o3, _ = ssh.exec_command('curl -s http://127.0.0.1:8000/reportes/facilitador/mis-reportes?admin_id=1')
print('test endpoint:', o3.read().decode()[:300])

ssh.close()
