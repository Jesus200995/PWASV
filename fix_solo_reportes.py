import paramiko, json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

script = """
import psycopg2, json

conn = psycopg2.connect(host='localhost', dbname='app_registros', user='jesus', password='2025')
cur = conn.cursor()

# Solo reportes: true, sin firmas
nuevos_permisos = json.dumps({"reportes": True})

cur.execute(
    "UPDATE admin_users SET permisos = %s::jsonb WHERE cargo = 'FACILITADOR' AND activo = TRUE",
    (nuevos_permisos,)
)
print(f"Actualizados: {cur.rowcount} facilitadores")
conn.commit()

cur.execute("SELECT COUNT(*), permisos::text FROM admin_users WHERE cargo='FACILITADOR' AND activo=TRUE GROUP BY permisos::text")
for row in cur.fetchall():
    print(f"  {row[0]} registros: {row[1]}")

conn.close()
"""

with ssh.open_sftp() as sftp:
    with sftp.open('/tmp/fix_perm.py', 'w') as f:
        f.write(script)

_, o, _ = ssh.exec_command('cd /var/www/PWASV/backend && source venv/bin/activate && python /tmp/fix_perm.py 2>&1', get_pty=True)
print(o.read().decode())
ssh.close()
