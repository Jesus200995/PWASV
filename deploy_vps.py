import paramiko, time

HOST = '31.97.8.51'
USER = 'root'
PASS = 'Lab-312334062'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=30)

def run(cmd, label=''):
    print(f'\n{"="*60}')
    print(f'>>> {label or cmd}')
    print('='*60)
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    out = stdout.read().decode(errors='replace')
    print(out)
    return out

# 1. Backend
run('cd /var/www/PWASV && git clean -fd 2>&1 | head -5', 'git clean untracked')
run('cd /var/www/PWASV/backend && git pull origin main 2>&1', 'git pull backend')
run('cd /var/www/PWASV/backend && source venv/bin/activate && pip install -r requirements.txt 2>&1 | tail -5', 'pip install')
run('systemctl restart apipwa && sleep 3 && systemctl is-active apipwa', 'restart backend')

# 2. pwasuper
run('cd /var/www/PWASV/pwasuper && git pull origin main 2>&1', 'git pull pwasuper')
run('cd /var/www/PWASV/pwasuper && npm install 2>&1 | tail -5', 'npm install pwasuper')
run('cd /var/www/PWASV/pwasuper && npm run build 2>&1 | tail -10', 'npm build pwasuper')
run('cp -r /var/www/PWASV/pwasuper/dist/* /var/www/app.sembrandodatos.com/ && echo "pwasuper deployed"', 'deploy pwasuper')

# 3. admin-pwa
run('cd /var/www/PWASV/admin-pwa && git pull origin main 2>&1', 'git pull admin-pwa')
run('cd /var/www/PWASV/admin-pwa && npm install 2>&1 | tail -5', 'npm install admin-pwa')
run('cd /var/www/PWASV/admin-pwa && npm run build 2>&1 | tail -10', 'npm build admin-pwa')
run('cp -r /var/www/PWASV/admin-pwa/dist/* /var/www/adminpwa.sembrandodatos.com/ && echo "admin-pwa deployed"', 'deploy admin-pwa')

ssh.close()
print('\n\n✅ Despliegue completo')
