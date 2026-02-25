#!/bin/bash
# Script para actualizar la base de datos con columnas de dispositivo

PGPASSWORD='2025' psql -h 31.97.8.51 -U jesus -d app_registros << 'EOF'
-- Agregar columnas de dispositivo
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS dispositivo VARCHAR(50) DEFAULT 'desconocido';
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS user_agent TEXT DEFAULT NULL;
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS ultimo_acceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
CREATE INDEX IF NOT EXISTS idx_usuarios_dispositivo ON usuarios(dispositivo);

-- Verificar columnas creadas
\echo '✅ Columnas agregadas exitosamente'
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name='usuarios' 
  AND column_name IN ('dispositivo', 'user_agent', 'ultimo_acceso');

\echo ''
\echo '📊 Estadísticas actuales:'
SELECT COUNT(*) as total_usuarios FROM usuarios;

SELECT 
    COALESCE(dispositivo, 'Sin datos') as dispositivo,
    COUNT(*) as cantidad
FROM usuarios
GROUP BY dispositivo
ORDER BY cantidad DESC;
EOF
