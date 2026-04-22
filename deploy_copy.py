import paramiko

hostname = "31.97.8.51"
username = "root"
password = "Lab-312334062"

commands = [
    "ls -la /var/www/PWASV/admin-pwa/dist/assets/ | tail -5",
    "cp -r /var/www/PWASV/admin-pwa/dist/* /var/www/adminpwa.sembrandodatos.com/",
    "systemctl restart nginx",
    "cat /var/www/adminpwa.sembrandodatos.com/index.html | head -5"
]

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password, timeout=10)
    
    for cmd in commands:
        print(f">>> {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        out = stdout.read().decode('utf-8', errors='replace')
        if out:
            print(out.strip())
        print(f"  -> Exit: {exit_status}\n")
        
    client.close()
    print("Done!")
except Exception as e:
    print(f"Error: {e}")
