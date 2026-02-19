-- Script SQL para agregar campos de dispositivo a la tabla usuarios
-- Ejecutar con: psql -h 31.97.8.51 -U jesus -d app_registros -f agregar_dispositivo.sql

-- 1. Agregar columna dispositivo
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS dispositivo VARCHAR(50) DEFAULT 'desconocido';

-- 2. Agregar columna user_agent (opcional, para análisis detallado)
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS user_agent TEXT DEFAULT NULL;

-- 3. Agregar columna ultimo_acceso
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS ultimo_acceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- 4. Crear índice para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_usuarios_dispositivo ON usuarios(dispositivo);

-- 5. Ver estadísticas actuales
SELECT 
    dispositivo,
    COUNT(*) as cantidad,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM usuarios), 2) as porcentaje
FROM usuarios
GROUP BY dispositivo
ORDER BY cantidad DESC;

-- 6. Total de usuarios
SELECT 
    'Total de usuarios:' as descripcion,
    COUNT(*) as cantidad
FROM usuarios;
