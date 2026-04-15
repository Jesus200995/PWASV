import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

def run(cmd, timeout=120):
    _, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    stdout.channel.settimeout(timeout)
    out = stdout.read().decode()
    err = stderr.read().decode()
    return out + err

# 1) Git pull
print("=== git pull ===")
print(run("cd /var/www/PWASV && git stash && git pull origin main 2>&1"))

# 2) Build admin-pwa
print("\n=== npm build admin-pwa ===")
print(run("cd /var/www/PWASV/admin-pwa && npm run build 2>&1", timeout=180))

# 3) Deploy a carpeta nginx
print("\n=== deploy ===")
print(run("cp -r /var/www/PWASV/admin-pwa/dist/* /var/www/adminpwa.sembrandodatos.com/ && echo 'DEPLOY OK'"))

ssh.close()
print("\n=== TERMINADO ===")
