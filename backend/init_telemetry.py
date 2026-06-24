"""Script de inicialización del sistema de telemetría. Ejecutar una sola vez en el VPS."""
import psycopg2
import bcrypt

DB_HOST = "31.97.8.51"
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

cur.execute("CREATE INDEX IF NOT EXISTS idx_sys_telemetry_ts ON sys_telemetry(ts DESC);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_sys_telemetry_usr ON sys_telemetry(usr);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_sys_telemetry_action ON sys_telemetry(action_type);")

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
print("✅ Telemetría inicializada correctamente")
