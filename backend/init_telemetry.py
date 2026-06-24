"""Script de inicialización del sistema de telemetría. Idempotente: se puede correr varias veces."""
import psycopg2
import bcrypt

DB_HOST = "localhost"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "sa2026"

conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS sys_telemetry (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    usr VARCHAR(120),
    usr_id INTEGER,
    action_type VARCHAR(60) NOT NULL,
    module VARCHAR(80),
    detail TEXT,
    target_id VARCHAR(120),
    target_label VARCHAR(255),
    ip_hint VARCHAR(60),
    ua TEXT,
    session_id VARCHAR(64),
    extra JSONB
);
""")

# Columnas adicionales para auditoría grado legal (idempotente)
extra_cols = [
    ("usr_nombre",    "VARCHAR(255)"),
    ("usr_rol",       "VARCHAR(50)"),
    ("usr_territorio","VARCHAR(120)"),
    ("usr_cargo",     "VARCHAR(255)"),
    ("http_method",   "VARCHAR(10)"),
    ("http_path",     "VARCHAR(400)"),
    ("http_status",   "INTEGER"),
    ("source",        "VARCHAR(20) DEFAULT 'frontend'"),
]
for name, ctype in extra_cols:
    cur.execute(f"ALTER TABLE sys_telemetry ADD COLUMN IF NOT EXISTS {name} {ctype};")

cur.execute("CREATE INDEX IF NOT EXISTS idx_sys_telemetry_ts ON sys_telemetry(ts DESC);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_sys_telemetry_usr ON sys_telemetry(usr);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_sys_telemetry_action ON sys_telemetry(action_type);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_sys_telemetry_module ON sys_telemetry(module);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_sys_telemetry_source ON sys_telemetry(source);")

cur.execute("""
CREATE TABLE IF NOT EXISTS sys_observers (
    id SERIAL PRIMARY KEY,
    handle VARCHAR(60) UNIQUE NOT NULL,
    secret_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
""")

pwd_hash = bcrypt.hashpw(b'sv2026', bcrypt.gensalt(12)).decode()
cur.execute(
    "INSERT INTO sys_observers (handle, secret_hash) VALUES (%s, %s) ON CONFLICT (handle) DO UPDATE SET secret_hash = EXCLUDED.secret_hash",
    ('adminsv', pwd_hash)
)

conn.commit()
cur.close()
conn.close()
print("✅ Telemetría inicializada/actualizada correctamente")
