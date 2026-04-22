import paramiko

hostname = "31.97.8.51"
username = "root"
password = "Lab-312334062"

sql_script = """
cd /var/www/PWASV/backend && source venv/bin/activate && python3 -c "
import psycopg2

conn = psycopg2.connect(host='31.97.8.51', database='app_registros', user='jesus', password='2025')
cur = conn.cursor()

cur.execute('SELECT COUNT(*) FROM notificaciones WHERE enviada_a_todos = FALSE')
count = cur.fetchone()[0]
print(f'Notificaciones individuales encontradas: {count}')

cur.execute('DELETE FROM notificacion_usuarios WHERE notificacion_id IN (SELECT id FROM notificaciones WHERE enviada_a_todos = FALSE)')
print(f'Registros notificacion_usuarios eliminados: {cur.rowcount}')

cur.execute('DELETE FROM notificaciones WHERE enviada_a_todos = FALSE')
print(f'Notificaciones individuales eliminadas: {cur.rowcount}')

conn.commit()
cur.close()
conn.close()
print('Listo!')
"
"""

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password, timeout=10)
    
    print("Conectado. Eliminando notificaciones individuales...")
    stdin, stdout, stderr = client.exec_command(sql_script, timeout=30)
    exit_status = stdout.channel.recv_exit_status()
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out:
        print(out.strip())
    if err and exit_status != 0:
        print(f"Error: {err.strip()}")
    print(f"Exit: {exit_status}")
    
    client.close()
except Exception as e:
    print(f"Error: {e}")
