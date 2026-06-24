-- Tabla de telemetría del sistema (uso interno)
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

CREATE INDEX IF NOT EXISTS idx_sys_telemetry_ts ON sys_telemetry(ts DESC);
CREATE INDEX IF NOT EXISTS idx_sys_telemetry_usr ON sys_telemetry(usr);
CREATE INDEX IF NOT EXISTS idx_sys_telemetry_action ON sys_telemetry(action_type);

-- Usuario de acceso a bitacora (hash bcrypt de 'sv2026')
CREATE TABLE IF NOT EXISTS sys_observers (
    id SERIAL PRIMARY KEY,
    handle VARCHAR(60) UNIQUE NOT NULL,
    secret_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO sys_observers (handle, secret_hash)
VALUES ('adminsv', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TugBjte0mJKH3x3TJWjGPrXgBnpC')
ON CONFLICT (handle) DO NOTHING;
