import psycopg2
import sys

try:
    conn = psycopg2.connect(
        host='31.97.8.51',
        database='app_registros',
        user='jesus',
        password='2025',
        connect_timeout=10
    )
    cur = conn.cursor()

    print("=== Columnas admin_users ===")
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='admin_users' ORDER BY ordinal_position")
    for r in cur.fetchall():
        print(f"  {r[0]} ({r[1]})")

    print("\n=== Muestra de admin_users ===")
    cur.execute("SELECT id, username, rol, activo, es_territorial, territorio, nombre_completo, curp, cargo FROM admin_users LIMIT 5")
    for r in cur.fetchall():
        print(f"  {r}")

    print("\n=== Usuarios con CURP (muestra) ===")
    cur.execute("SELECT id, nombre_completo, cargo, curp, territorio FROM usuarios WHERE curp IS NOT NULL AND curp != '' AND cargo ILIKE '%FACILITADOR%' LIMIT 5")
    rows = cur.fetchall()
    print(f"  Facilitadores en pwasuper: {len(rows)}")
    for r in rows:
        print(f"  {r}")

    print("\n=== Tabla facilitador_tecnico_asignaciones existe? ===")
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='facilitador_tecnico_asignaciones')")
    print(f"  {cur.fetchone()[0]}")

    print("\n=== Columnas tabla reportes_generados (firma) ===")
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='reportes_generados' AND column_name IN ('firmado_supervisor','firma_supervisor_base64','supervisor_id','nombre_supervisor','facilitador_usuario_id') ORDER BY ordinal_position")
    for r in cur.fetchall():
        print(f"  {r[0]}")

    conn.close()
    print("\nConexion OK")
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
