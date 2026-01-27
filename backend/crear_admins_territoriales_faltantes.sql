-- Script SQL para crear administradores territoriales faltantes
-- Ejecutar en PostgreSQL del VPS: ssh root@31.97.8.51, luego psql -U postgres -d app_registros

-- IMPORTANTE: Reemplazar las contraseñas hash con las correctas

-- 1. Acayucan
INSERT INTO admin_users (correo, nombre_completo, territorio, es_territorial, activo, contrasena_hash)
VALUES (
    'admin.acayucan@sembrandovida.gob.mx',
    'ADMINISTRADOR TERRITORIAL ACAYUCAN',
    'Acayucan',
    TRUE,
    TRUE,
    '$2b$12$hashedpasswordhere'  -- Cambiar por hash real
) ON CONFLICT (correo) DO NOTHING;

-- 2. Chihuahua / Sonora
INSERT INTO admin_users (correo, nombre_completo, territorio, es_territorial, activo, contrasena_hash)
VALUES (
    'admin.chihuahuasonora@sembrandovida.gob.mx',
    'ADMINISTRADOR TERRITORIAL CHIHUAHUA SONORA',
    'Chihuahua / Sonora',
    TRUE,
    TRUE,
    '$2b$12$hashedpasswordhere'  -- Cambiar por hash real
) ON CONFLICT (correo) DO NOTHING;

-- 3. Durango / Zacatecas
INSERT INTO admin_users (correo, nombre_completo, territorio, es_territorial, activo, contrasena_hash)
VALUES (
    'admin.durangozacatecas@sembrandovida.gob.mx',
    'ADMINISTRADOR TERRITORIAL DURANGO ZACATECAS',
    'Durango / Zacatecas',
    TRUE,
    TRUE,
    '$2b$12$hashedpasswordhere'  -- Cambiar por hash real
) ON CONFLICT (correo) DO NOTHING;

-- 4. Nayarit / Jalisco
INSERT INTO admin_users (correo, nombre_completo, territorio, es_territorial, activo, contrasena_hash)
VALUES (
    'admin.nayaritjalisco@sembrandovida.gob.mx',
    'ADMINISTRADOR TERRITORIAL NAYARIT JALISCO',
    'Nayarit / Jalisco',
    TRUE,
    TRUE,
    '$2b$12$hashedpasswordhere'  -- Cambiar por hash real
) ON CONFLICT (correo) DO NOTHING;

-- 5. Tlaxcala / Estado de México
INSERT INTO admin_users (correo, nombre_completo, territorio, es_territorial, activo, contrasena_hash)
VALUES (
    'admin.tlaxcalaedomex@sembrandovida.gob.mx',
    'ADMINISTRADOR TERRITORIAL TLAXCALA ESTADO DE MEXICO',
    'Tlaxcala / Estado de México',
    TRUE,
    TRUE,
    '$2b$12$hashedpasswordhere'  -- Cambiar por hash real
) ON CONFLICT (correo) DO NOTHING;

-- 6. Tzucacab / Opb
INSERT INTO admin_users (correo, nombre_completo, territorio, es_territorial, activo, contrasena_hash)
VALUES (
    'admin.tzucacab@sembrandovida.gob.mx',
    'ADMINISTRADOR TERRITORIAL TZUCACAB OPB',
    'Tzucacab / Opb',
    TRUE,
    TRUE,
    '$2b$12$hashedpasswordhere'  -- Cambiar por hash real
) ON CONFLICT (correo) DO NOTHING;

-- 7. Oficinas Centrales
INSERT INTO admin_users (correo, nombre_completo, territorio, es_territorial, activo, contrasena_hash)
VALUES (
    'admin.centrales@sembrandovida.gob.mx',
    'ADMINISTRADOR TERRITORIAL OFICINAS CENTRALES',
    'Oficinas Centrales',
    TRUE,
    TRUE,
    '$2b$12$hashedpasswordhere'  -- Cambiar por hash real
) ON CONFLICT (correo) DO NOTHING;

-- Verificar que se crearon correctamente
SELECT 
    id,
    nombre_completo,
    territorio,
    es_territorial,
    activo
FROM admin_users
WHERE territorio IN (
    'Acayucan',
    'Chihuahua / Sonora',
    'Durango / Zacatecas',
    'Nayarit / Jalisco',
    'Tlaxcala / Estado de México',
    'Tzucacab / Opb',
    'Oficinas Centrales'
)
ORDER BY territorio;

-- Contar administradores territoriales
SELECT 
    COUNT(*) as total_territoriales
FROM admin_users
WHERE es_territorial = TRUE AND activo = TRUE;
