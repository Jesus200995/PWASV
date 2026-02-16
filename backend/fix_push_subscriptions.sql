-- Script para corregir/recrear la tabla push_subscriptions
-- EJECUTAR EN EL SERVIDOR: psql -U jesus -d app_registros -f fix_push_subscriptions.sql

-- Mostrar estructura actual primero
\echo '=== ESTRUCTURA ACTUAL ==='
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'push_subscriptions';

-- Agregar columnas faltantes si la tabla existe
DO $$
BEGIN
    -- Verificar si la tabla existe
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'push_subscriptions') THEN
        -- Agregar columna p256dh si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'push_subscriptions' AND column_name = 'p256dh') THEN
            ALTER TABLE push_subscriptions ADD COLUMN p256dh TEXT NOT NULL DEFAULT '';
            RAISE NOTICE 'Columna p256dh agregada';
        END IF;
        
        -- Agregar columna auth si no existe  
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'push_subscriptions' AND column_name = 'auth') THEN
            ALTER TABLE push_subscriptions ADD COLUMN auth TEXT NOT NULL DEFAULT '';
            RAISE NOTICE 'Columna auth agregada';
        END IF;
        
        -- Agregar columna activa si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'push_subscriptions' AND column_name = 'activa') THEN
            ALTER TABLE push_subscriptions ADD COLUMN activa BOOLEAN DEFAULT TRUE;
            RAISE NOTICE 'Columna activa agregada';
        END IF;
        
        -- Agregar columna device_info si no existe  
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'push_subscriptions' AND column_name = 'device_info') THEN
            ALTER TABLE push_subscriptions ADD COLUMN device_info JSONB;
            RAISE NOTICE 'Columna device_info agregada';
        END IF;
        
        -- Agregar columna fecha_creacion si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'push_subscriptions' AND column_name = 'fecha_creacion') THEN
            ALTER TABLE push_subscriptions ADD COLUMN fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            RAISE NOTICE 'Columna fecha_creacion agregada';
        END IF;
        
        -- Agregar columna fecha_actualizacion si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'push_subscriptions' AND column_name = 'fecha_actualizacion') THEN
            ALTER TABLE push_subscriptions ADD COLUMN fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            RAISE NOTICE 'Columna fecha_actualizacion agregada';
        END IF;
        
        -- Agregar columna ultimo_uso si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'push_subscriptions' AND column_name = 'ultimo_uso') THEN
            ALTER TABLE push_subscriptions ADD COLUMN ultimo_uso TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            RAISE NOTICE 'Columna ultimo_uso agregada';
        END IF;
        
        -- Agregar columna usuario_id si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'push_subscriptions' AND column_name = 'usuario_id') THEN
            ALTER TABLE push_subscriptions ADD COLUMN usuario_id INTEGER;
            RAISE NOTICE 'Columna usuario_id agregada';
        END IF;
        
        -- Agregar columna endpoint si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'push_subscriptions' AND column_name = 'endpoint') THEN
            ALTER TABLE push_subscriptions ADD COLUMN endpoint TEXT NOT NULL DEFAULT '';
            RAISE NOTICE 'Columna endpoint agregada';
        END IF;
        
    ELSE
        -- Si no existe la tabla, crearla completa
        CREATE TABLE push_subscriptions (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            endpoint TEXT NOT NULL UNIQUE,
            p256dh TEXT NOT NULL,
            auth TEXT NOT NULL,
            device_info JSONB,
            activa BOOLEAN DEFAULT TRUE,
            fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            ultimo_uso TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Crear índices
        CREATE INDEX IF NOT EXISTS idx_push_subscriptions_usuario ON push_subscriptions(usuario_id);
        CREATE INDEX IF NOT EXISTS idx_push_subscriptions_activa ON push_subscriptions(activa);
        CREATE INDEX IF NOT EXISTS idx_push_subscriptions_endpoint ON push_subscriptions(endpoint);
        
        RAISE NOTICE 'Tabla push_subscriptions creada desde cero';
    END IF;
END $$;

-- Quitar constraint DEFAULT de columnas que no lo necesitan
ALTER TABLE push_subscriptions ALTER COLUMN p256dh DROP DEFAULT;
ALTER TABLE push_subscriptions ALTER COLUMN auth DROP DEFAULT;
ALTER TABLE push_subscriptions ALTER COLUMN endpoint DROP DEFAULT;

\echo '=== ESTRUCTURA FINAL ==='
SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'push_subscriptions' ORDER BY ordinal_position;

\echo '=== TABLA LISTA ==='
