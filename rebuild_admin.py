import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=30)

def run(cmd, label=''):
    print(f'\n--- {label or cmd[:60]} ---')
    _, o, _ = ssh.exec_command(cmd, get_pty=True)
    out = o.read().decode(errors='replace')
    print(out[-1200:] if len(out) > 1200 else out)
    return out

# Verificar que el código nuevo está en el VPS
run("grep -n 'firmas' /var/www/PWASV/admin-pwa/src/router/index.js", 'verificar firmas en router')

# Rebuild admin-pwa
run('cd /var/www/PWASV/admin-pwa && npm run build 2>&1', 'npm build admin-pwa')

# Deploy
run('cp -r /var/www/PWASV/admin-pwa/dist/* /var/www/adminpwa.sembrandodatos.com/ && echo "DEPLOY OK"', 'deploy admin-pwa')

ssh.close()
print('\n✅ Admin-pwa redeployado')
