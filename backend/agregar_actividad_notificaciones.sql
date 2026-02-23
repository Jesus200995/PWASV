-- Script para agregar campos de vinculación de notificaciones con actividades
-- Fecha: 23 de febrero de 2026

-- 1. Agregar campo para vincular notificación con reporte/actividad
ALTER TABLE notificaciones 
ADD COLUMN IF NOT EXISTS actividad_id INTEGER REFERENCES reportes_generados(id) ON DELETE SET NULL;

-- 2. Agregar campo para motivos de atención (array de strings)
ALTER TABLE notificaciones 
ADD COLUMN IF NOT EXISTS motivos_atencion TEXT[];

-- 3. Crear índice para mejorar consultas por actividad
CREATE INDEX IF NOT EXISTS idx_notificaciones_actividad 
ON notificaciones(actividad_id) 
WHERE actividad_id IS NOT NULL;

-- 4. Comentarios para documentación
COMMENT ON COLUMN notificaciones.actividad_id IS 'ID del reporte/actividad vinculado a esta notificación (para notificaciones contextuales)';
COMMENT ON COLUMN notificaciones.motivos_atencion IS 'Array de motivos por los que se envía la notificación (ej: ["Llamar atención", "Corrección requerida"])';

-- Verificar estructura actualizada
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'notificaciones' 
ORDER BY ordinal_position;
