import paramiko
import sys

hostname = "31.97.8.51"
username = "root"
password = "Lab-312334062"

commands = [
    "cd /var/www/PWASV/admin-pwa && npm run build",
    "cp -r /var/www/PWASV/admin-pwa/dist/* /var/www/adminpwa.sembrandodatos.com/",
    "systemctl restart nginx"
]

def execute_commands():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password, timeout=10)
        
        for cmd in commands:
            stdin, stdout, stderr = client.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode('utf-8', errors='replace')
            err = stderr.read().decode('utf-8', errors='replace')
            print(f"Command: {cmd} - Status: {exit_status}")
            
        client.close()
    except Exception as e:
        print(f"Error al conectar o ejecutar: {e}")

if __name__ == "__main__":
    execute_commands()
