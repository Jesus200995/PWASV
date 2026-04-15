import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('31.97.8.51', username='root', password='Lab-312334062', timeout=20)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd, get_pty=True)
    return o.read().decode(errors='replace')

# Verificar cuántos facilitadores hay y cómo tienen sus permisos
check = run("""PGPASSWORD='2025' psql -U jesus -d app_registros -c "
SELECT COUNT(*), permisos::text
FROM admin_users
WHERE cargo = 'FACILITADOR' AND activo = TRUE
GROUP BY permisos::text
ORDER BY COUNT(*) DESC;
" """)
print("Estado actual de permisos:\n", check)

# Actualizar todos los facilitadores: firmas + reportes
update = run("""PGPASSWORD='2025' psql -U jesus -d app_registros -c "
UPDATE admin_users
SET permisos = '{\"firmas\": true, \"reportes\": true}'::jsonb
WHERE cargo = 'FACILITADOR' AND activo = TRUE;
" """)
print("\nResultado del UPDATE:\n", update)

# Verificar resultado
verify = run("""PGPASSWORD='2025' psql -U jesus -d app_registros -c "
SELECT COUNT(*) as total_actualizados, permisos::text
FROM admin_users
WHERE cargo = 'FACILITADOR' AND activo = TRUE
GROUP BY permisos::text;
" """)
print("\nPermisos después:\n", verify)

ssh.close()
