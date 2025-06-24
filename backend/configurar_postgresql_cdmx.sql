-- Script SQL para configurar PostgreSQL para zona horaria America/Mexico_City
-- Ejecutar como administrador de la base de datos

-- 1. Configurar timezone global del servidor (requiere reinicio de PostgreSQL)
-- En postgresql.conf, cambiar: timezone = 'America/Mexico_City'

-- 2. Configurar timezone para la base de datos actual
SET timezone = 'America/Mexico_City';

-- 3. Verificar timezone actual
SHOW timezone;

-- 4. Actualizar la columna fecha_hora para usar timestamp WITH time zone
-- IMPORTANTE: Esto debe ejecutarse como propietario de la tabla
ALTER TABLE registros 
ALTER COLUMN fecha_hora TYPE TIMESTAMP WITH TIME ZONE 
USING fecha_hora AT TIME ZONE 'America/Mexico_City';

-- 5. Verificar el cambio
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'registros' AND column_name = 'fecha_hora';

-- 6. Probar inserción con zona horaria
INSERT INTO registros (usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora) 
VALUES (999, 19.4326, -99.1332, 'Prueba de zona horaria', 'test.jpg', NOW());

-- 7. Verificar que la fecha se guardó correctamente
SELECT id, fecha_hora, 
       fecha_hora AT TIME ZONE 'UTC' as fecha_utc,
       fecha_hora AT TIME ZONE 'America/Mexico_City' as fecha_cdmx
FROM registros 
WHERE usuario_id = 999 
ORDER BY id DESC LIMIT 1;

-- 8. Limpiar registro de prueba
DELETE FROM registros WHERE usuario_id = 999;

-- Comandos adicionales para verificación:

-- Verificar todas las fechas existentes
SELECT COUNT(*), 
       MIN(fecha_hora) as fecha_minima, 
       MAX(fecha_hora) as fecha_maxima,
       EXTRACT(timezone_hour FROM fecha_hora) as offset_horas
FROM registros;

-- Si hay fechas con timezone incorrecto, actualizarlas:
-- UPDATE registros 
-- SET fecha_hora = fecha_hora AT TIME ZONE 'UTC' AT TIME ZONE 'America/Mexico_City'
-- WHERE EXTRACT(timezone_hour FROM fecha_hora) != -6 AND EXTRACT(timezone_hour FROM fecha_hora) != -5;

COMMIT;
