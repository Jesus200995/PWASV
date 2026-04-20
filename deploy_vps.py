import paramiko
import sys

hostname = "31.97.8.51"
username = "root"
password = "Lab-312334062"

commands = [
    "cd /var/www/PWASV/backend && git pull origin main && source venv/bin/activate && pip install -r requirements.txt && systemctl restart apipwa",
    "cd /var/www/PWASV/admin-pwa && git pull origin main",
    "cd /var/www/PWASV/admin-pwa && npm install",
    "cd /var/www/PWASV/admin-pwa && npm run build",
    "cp -r /var/www/PWASV/admin-pwa/dist/* /var/www/adminpwa.sembrandodatos.com/"
]

def execute_commands():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Conectando a {hostname}...")
        client.connect(hostname, username=username, password=password, timeout=10)
        print("Conexión exitosa. Ejecutando comandos...")
        
        for cmd in commands:
            print(f"\n> {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
            if out:
                print(out)
            if err:
                print(f"Error: {err}")
            print(f"Exit status: {exit_status}")
            
        client.close()
        print("\nDespliegue completado.")
    except Exception as e:
        print(f"Error al conectar o ejecutar: {e}")

if __name__ == "__main__":
    execute_commands()
