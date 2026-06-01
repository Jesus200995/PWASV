import paramiko
import sys
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

hostname = "31.97.8.51"
username = "root"
password = "Lab-TeamMar@3690"

commands = [
    "systemctl is-active apipwa 2>&1",
    "systemctl is-active nginx 2>&1",
    "ss -tlnp | grep -E '8000|80|443'",
    "journalctl -u apipwa --no-pager -n 30 2>&1 | tail -30",
    "df -h / | tail -1",
    "free -h | head -2",
    "ps aux | grep -E 'uvicorn|python|node' | grep -v grep | head -10",
    "tail -20 /var/log/nginx/error.log 2>&1",
    "ls -la /var/www/PWASV/backend/main.py 2>&1",
    "cd /var/www/PWASV && git log -1 --oneline 2>&1",
    "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/ 2>&1 || echo 'API_NO_RESPONDE'",
    "cat /etc/systemd/system/apipwa.service 2>&1",
    "nginx -t 2>&1",
]

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password, timeout=15)
    
    for cmd in commands:
        sep = "=" * 60
        stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
        exit_status = stdout.channel.recv_exit_status()
        out = stdout.read().decode('utf-8', errors='replace').strip()
        err = stderr.read().decode('utf-8', errors='replace').strip()
        
        result = f"{sep}\n>>> {cmd}\n{sep}\n"
        if out:
            result += out + "\n"
        if err:
            result += f"STDERR: {err}\n"
        result += f"Exit: {exit_status}\n"
        
        # Write to file instead of print to avoid encoding issues
        with open("vps_diag.txt", "a", encoding="utf-8") as f:
            f.write(result + "\n")
        
    client.close()
    
    with open("vps_diag.txt", "r", encoding="utf-8") as f:
        print(f.read())
        
except Exception as e:
    print(f"Error: {e}")
