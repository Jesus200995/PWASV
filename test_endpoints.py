import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

cmds = [
    'curl -s -w "\\nHTTP_CODE:%{http_code}" http://127.0.0.1:8000/reportes/facilitador/mis-reportes?admin_id=1',
    'curl -s -w "\\nHTTP_CODE:%{http_code}" http://127.0.0.1:8000/facilitadores/mis-tecnicos?admin_id=1',
]

for cmd in cmds:
    _, o, _ = ssh.exec_command(cmd)
    print(o.read().decode()[:400])
    print('---')

ssh.close()
