-- Crear tabla push_notification_logs
CREATE TABLE IF NOT EXISTS push_notification_logs (
    id SERIAL PRIMARY KEY,
    notificacion_id INTEGER NOT NULL,
    usuario_id INTEGER,
    estado VARCHAR(50) NOT NULL,
    endpoint TEXT,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear índices
CREATE INDEX IF NOT EXISTS idx_push_logs_notificacion ON push_notification_logs(notificacion_id);
CREATE INDEX IF NOT EXISTS idx_push_logs_usuario ON push_notification_logs(usuario_id);
CREATE INDEX IF NOT EXISTS idx_push_logs_created ON push_notification_logs(created_at);

-- Verificar
SELECT 'Tabla push_notification_logs creada correctamente' as resultado;
