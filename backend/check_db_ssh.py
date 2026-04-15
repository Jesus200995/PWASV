"""
Script de diagnóstico: ejecuta SQL en VPS via SSH y devuelve resultados.
"""
import paramiko
import sys

HOST = "31.97.8.51"
USER = "root"
PASS = "Lab-312334062"

PG_PASS = "2025"

QUERIES = [
    ("Columnas admin_users", 
     f"PGPASSWORD='{PG_PASS}' psql -U jesus -d app_registros -c \"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='admin_users' ORDER BY ordinal_position\""),
    ("Muestra admin_users",
     f"PGPASSWORD='{PG_PASS}' psql -U jesus -d app_registros -c \"SELECT id, username, rol, activo, es_territorial, nombre_completo, curp, cargo FROM admin_users LIMIT 5\""),
    ("Tabla facilitador_tecnico_asignaciones existe",
     f"PGPASSWORD='{PG_PASS}' psql -U jesus -d app_registros -c \"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='facilitador_tecnico_asignaciones')\""),
    ("Columnas reportes_generados firma",
     f"PGPASSWORD='{PG_PASS}' psql -U jesus -d app_registros -c \"SELECT column_name FROM information_schema.columns WHERE table_name='reportes_generados' AND (column_name ILIKE '%supervisor%' OR column_name ILIKE '%facilitador%')\""),
    ("Facilitadores en usuarios pwasuper",
     f"PGPASSWORD='{PG_PASS}' psql -U jesus -d app_registros -c \"SELECT id, nombre_completo, cargo, curp FROM usuarios WHERE cargo ILIKE '%FACILITADOR%' LIMIT 5\""),
    ("Total usuarios con CURP",
     f"PGPASSWORD='{PG_PASS}' psql -U jesus -d app_registros -c \"SELECT COUNT(*) FROM usuarios WHERE curp IS NOT NULL AND curp != ''\""),
]

def run_ssh(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS, timeout=15)
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    client.close()
    return out, err

if __name__ == "__main__":
    for label, cmd in QUERIES:
        print(f"\n{'='*50}\n=== {label} ===")
        try:
            out, err = run_ssh(cmd)
            if out: print(out)
            if err: print("STDERR:", err[:300])
        except Exception as e:
            print(f"ERROR: {e}")
