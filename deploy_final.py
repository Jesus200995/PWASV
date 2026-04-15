import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=30)

def run(cmd, label=''):
    print(f'\n--- {label} ---')
    _, o, _ = ssh.exec_command(cmd, get_pty=True)
    out = o.read().decode(errors='replace')
    print(out[-800:] if len(out) > 800 else out)

run('cd /var/www/PWASV && git pull origin main 2>&1', 'git pull')
run('cd /var/www/PWASV/admin-pwa && npm run build 2>&1 | tail -8', 'npm build')
run('cp -r /var/www/PWASV/admin-pwa/dist/* /var/www/adminpwa.sembrandodatos.com/ && echo "DEPLOY OK"', 'deploy')

ssh.close()
