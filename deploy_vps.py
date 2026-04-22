import paramiko
import sys

hostname = "31.97.8.51"
username = "root"
password = "Lab-312334062"

commands = [
    "cd /var/www/PWASV && git pull origin main",
    "cd /var/www/PWASV/backend && source venv/bin/activate && systemctl restart apipwa",
    "cd /var/www/PWASV/admin-pwa && npm run build 2>&1",
    "cp -r /var/www/PWASV/admin-pwa/dist/* /var/www/adminpwa.sembrandodatos.com/",
    "systemctl restart nginx"
]

def execute_commands():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Conectando a {hostname}...")
        client.connect(hostname, username=username, password=password, timeout=10)
        print("Conexion exitosa.\n")
        
        for cmd in commands:
            print(f">>> {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd, timeout=120)
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode('utf-8', errors='replace')
            err = stderr.read().decode('utf-8', errors='replace')
            if out:
                # Print last 5 lines of output only
                lines = out.strip().split('\n')
                for line in lines[-5:]:
                    print(f"  {line}")
            if err and exit_status != 0:
                err_lines = err.strip().split('\n')
                for line in err_lines[-5:]:
                    print(f"  [ERR] {line}")
            print(f"  -> Exit: {exit_status}\n")
            
        client.close()
        print("Despliegue completado exitosamente!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    execute_commands()
