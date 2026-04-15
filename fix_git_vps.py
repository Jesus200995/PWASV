import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd, get_pty=True)
    out = o.read().decode(errors='replace')
    print(out)
    return out

print('=== Stash y git pull backend ===')
run('cd /var/www/PWASV && git stash && git pull origin main 2>&1')

print('=== Verificar backend ===')
run('systemctl is-active apipwa')

ssh.close()
print('Listo')
