-- Script para agregar columna 'activo' a la tabla 'usuarios'
-- Fecha: 2026-02-05
-- Propósito: Permitir desactivar cuentas de usuarios

-- Verificar si la columna ya existe antes de agregarla
DO $$ 
BEGIN
    -- Verificar si la columna 'activo' existe en la tabla 'usuarios'
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'usuarios' 
        AND column_name = 'activo'
    ) THEN
        -- Agregar la columna 'activo' con valor por defecto TRUE
        ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE;
        RAISE NOTICE 'Columna activo agregada a la tabla usuarios';
    ELSE
        RAISE NOTICE 'La columna activo ya existe en la tabla usuarios';
    END IF;
    
    -- Actualizar todos los registros existentes para que tengan activo = TRUE
    UPDATE usuarios SET activo = TRUE WHERE activo IS NULL;
    RAISE NOTICE 'Registros actualizados con activo = TRUE';
    
END $$;

-- Verificar el resultado
SELECT COUNT(*) as total_usuarios, 
       COUNT(*) FILTER (WHERE activo = TRUE) as usuarios_activos,
       COUNT(*) FILTER (WHERE activo = FALSE) as usuarios_inactivos
FROM usuarios;
