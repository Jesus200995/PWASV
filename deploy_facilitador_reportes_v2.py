import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

def run(cmd, timeout=200):
    _, stdout, _ = ssh.exec_command(cmd, get_pty=True)
    stdout.channel.settimeout(timeout)
    return stdout.read().decode()

print("=== git pull ===")
print(run("cd /var/www/PWASV && git stash && git pull origin main 2>&1"))

print("\n=== restart backend ===")
print(run("systemctl restart apipwa && sleep 2 && systemctl is-active apipwa"))

print("\n=== build pwasuper ===")
print(run("cd /var/www/PWASV/pwasuper && npm run build 2>&1", timeout=240))

print("\n=== deploy pwasuper ===")
print(run("cp -r /var/www/PWASV/pwasuper/dist/* /var/www/app.sembrandodatos.com/ && echo 'PWASUPER OK'"))

print("\n=== build admin-pwa ===")
print(run("cd /var/www/PWASV/admin-pwa && npm run build 2>&1", timeout=240))

print("\n=== deploy admin-pwa ===")
print(run("cp -r /var/www/PWASV/admin-pwa/dist/* /var/www/adminpwa.sembrandodatos.com/ && echo 'ADMIN OK'"))

ssh.close()
print("\n=== TERMINADO ===")
