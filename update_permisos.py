import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

# Verificar estado actual
cmd_check = (
    "PGPASSWORD=2025 psql -U jesus -d app_registros "
    "-c \"SELECT COUNT(*), permisos::text FROM admin_users "
    "WHERE cargo='FACILITADOR' AND activo=TRUE GROUP BY permisos::text;\""
)
_, o, _ = ssh.exec_command(cmd_check)
print("Antes:\n", o.read().decode())

# Actualizar permisos - firmas + reportes
cmd_update = (
    "PGPASSWORD=2025 psql -U jesus -d app_registros "
    '-c "UPDATE admin_users '
    "SET permisos = '{\"firmas\": true, \"reportes\": true}'::jsonb "
    "WHERE cargo='FACILITADOR' AND activo=TRUE;\""
)
_, o, _ = ssh.exec_command(cmd_update)
print("UPDATE:", o.read().decode())

# Verificar resultado
_, o, _ = ssh.exec_command(cmd_check)
print("Después:\n", o.read().decode())

ssh.close()
