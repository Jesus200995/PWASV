-- Script para agregar columnas de firma de supervisor
ALTER TABLE reportes_generados ADD COLUMN IF NOT EXISTS firmado_supervisor BOOLEAN DEFAULT FALSE;
ALTER TABLE reportes_generados ADD COLUMN IF NOT EXISTS fecha_firma_supervisor TIMESTAMP;
ALTER TABLE reportes_generados ADD COLUMN IF NOT EXISTS firma_supervisor_base64 TEXT;
ALTER TABLE reportes_generados ADD COLUMN IF NOT EXISTS nombre_supervisor VARCHAR(255);
ALTER TABLE reportes_generados ADD COLUMN IF NOT EXISTS supervisor_id INTEGER;

-- Verificar columnas
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'reportes_generados' AND column_name LIKE '%supervisor%' OR column_name = 'firmado_supervisor';
