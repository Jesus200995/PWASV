-- ==================== SISTEMA DE PUSH NOTIFICATIONS ====================
-- Script para crear las tablas necesarias para Web Push Notifications
-- Ejecutar con: psql -U usuario -d basedatos -f push_notifications_setup.sql

-- Tabla para almacenar suscripciones push de dispositivos
CREATE TABLE IF NOT EXISTS push_subscriptions (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    endpoint TEXT NOT NULL UNIQUE,
    p256dh TEXT NOT NULL,  -- Clave pública para encriptación
    auth TEXT NOT NULL,     -- Secreto de autenticación
    device_info JSONB,      -- Info del dispositivo (navegador, OS, etc.)
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ultimo_uso TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para búsquedas eficientes
CREATE INDEX IF NOT EXISTS idx_push_subscriptions_usuario ON push_subscriptions(usuario_id);
CREATE INDEX IF NOT EXISTS idx_push_subscriptions_activa ON push_subscriptions(activa);
CREATE INDEX IF NOT EXISTS idx_push_subscriptions_endpoint ON push_subscriptions(endpoint);

-- Tabla para logs de push notifications enviadas
CREATE TABLE IF NOT EXISTS push_notification_logs (
    id SERIAL PRIMARY KEY,
    notificacion_id INTEGER REFERENCES notificaciones(id) ON DELETE SET NULL,
    subscription_id INTEGER REFERENCES push_subscriptions(id) ON DELETE SET NULL,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    estado VARCHAR(50) NOT NULL, -- 'enviado', 'fallido', 'expirado'
    error_mensaje TEXT,
    fecha_envio TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_push_logs_notificacion ON push_notification_logs(notificacion_id);
CREATE INDEX IF NOT EXISTS idx_push_logs_estado ON push_notification_logs(estado);

-- Añadir columnas de estilo a la tabla de notificaciones si no existen
DO $$
BEGIN
    -- Columna para configuración de estilo JSON
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'notificaciones' AND column_name = 'estilo_config') THEN
        ALTER TABLE notificaciones ADD COLUMN estilo_config JSONB DEFAULT '{}';
    END IF;
    
    -- Columna para prioridad de la notificación
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'notificaciones' AND column_name = 'prioridad') THEN
        ALTER TABLE notificaciones ADD COLUMN prioridad VARCHAR(20) DEFAULT 'normal';
    END IF;
    
    -- Columna para tipo/categoría de notificación
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'notificaciones' AND column_name = 'tipo') THEN
        ALTER TABLE notificaciones ADD COLUMN tipo VARCHAR(50) DEFAULT 'general';
    END IF;
    
    -- Columna para icono personalizado
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'notificaciones' AND column_name = 'icono') THEN
        ALTER TABLE notificaciones ADD COLUMN icono VARCHAR(100);
    END IF;
    
    -- Columna para color de acento
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'notificaciones' AND column_name = 'color_acento') THEN
        ALTER TABLE notificaciones ADD COLUMN color_acento VARCHAR(20);
    END IF;
    
    -- Columna para activar/desactivar push
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'notificaciones' AND column_name = 'enviar_push') THEN
        ALTER TABLE notificaciones ADD COLUMN enviar_push BOOLEAN DEFAULT TRUE;
    END IF;
    
    -- Columna para programar envío
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'notificaciones' AND column_name = 'fecha_programada') THEN
        ALTER TABLE notificaciones ADD COLUMN fecha_programada TIMESTAMP WITH TIME ZONE;
    END IF;
    
END $$;

-- Tabla de configuración de VAPID keys (solo una fila)
CREATE TABLE IF NOT EXISTS push_vapid_config (
    id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    public_key TEXT NOT NULL,
    private_key TEXT NOT NULL,
    email_contacto VARCHAR(255) DEFAULT 'admin@sembrandodatos.com',
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Comentarios para documentación
COMMENT ON TABLE push_subscriptions IS 'Almacena las suscripciones de Push Notifications por dispositivo/usuario';
COMMENT ON TABLE push_notification_logs IS 'Registro de todas las push notifications enviadas';
COMMENT ON TABLE push_vapid_config IS 'Configuración VAPID para Push Notifications (solo una fila)';
COMMENT ON COLUMN notificaciones.estilo_config IS 'Configuración de estilo JSON: fontFamily, fontSize, bold, italic, etc.';
COMMENT ON COLUMN notificaciones.prioridad IS 'Prioridad: low, normal, high, urgent';
COMMENT ON COLUMN notificaciones.tipo IS 'Tipo: general, alerta, recordatorio, actualizacion, urgente';

-- ==================== FIN SETUP ====================
