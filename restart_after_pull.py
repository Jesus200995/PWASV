import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

def run(cmd, label=''):
    print(f'\n--- {label or cmd} ---')
    _, o, _ = ssh.exec_command(cmd, get_pty=True)
    out = o.read().decode(errors='replace')
    print(out)
    return out

# Reiniciar backend con el main.py del git pull
run('systemctl restart apipwa', 'restart apipwa')
time.sleep(4)
run('systemctl is-active apipwa', 'estado')

# Verificar endpoints nuevos
run('curl -s http://127.0.0.1:8000/reportes/facilitador/mis-reportes?admin_id=1', 'test endpoint facilitador')
run('curl -s http://127.0.0.1:8000/facilitadores/mis-tecnicos?admin_id=1', 'test endpoint tecnicos')

ssh.close()
