import paramiko

hostname = "31.97.8.51"
username = "root"
password = "Lab-TeamMar@3690"

commands = [
    # Check current DB password in main.py
    "grep -n 'DB_PASS\\|DB_HOST\\|DB_NAME\\|DB_USER' /var/www/PWASV/backend/main.py | head -10",
    # Try to connect to postgres to check user
    "sudo -u postgres psql -c \"SELECT usename FROM pg_catalog.pg_user WHERE usename='jesus';\" 2>&1",
    # Check pg_hba.conf for auth method
    "grep -v '^#' /etc/postgresql/*/main/pg_hba.conf | grep -v '^$' | head -15 2>&1",
]

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password, timeout=15)
    
    with open("vps_db_check.txt", "w", encoding="utf-8") as f:
        for cmd in commands:
            stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode('utf-8', errors='replace').strip()
            err = stderr.read().decode('utf-8', errors='replace').strip()
            f.write(f">>> {cmd}\n{out}\n")
            if err:
                f.write(f"STDERR: {err}\n")
            f.write(f"Exit: {exit_status}\n\n")
    
    client.close()
    
    with open("vps_db_check.txt", "r", encoding="utf-8") as f:
        print(f.read())
except Exception as e:
    print(f"Error: {e}")
