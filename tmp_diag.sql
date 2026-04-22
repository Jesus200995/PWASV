-- Facilitador
SELECT 'admin:' as tipo, au.id as admin_id, au.usuario_id, au.nombre_completo, au.curp, au.cargo
FROM admin_users au WHERE au.curp='RIGJ020607HPLSMSA0';

-- Tecnico pwasuper
SELECT 'tecnico:' as tipo, u.id, u.nombre_completo, u.correo, u.cargo, u.supervisor
FROM usuarios u WHERE u.correo='jess@gmail.com';

-- Asignaciones del tecnico
SELECT 'asignacion:' as tipo, fta.*
FROM facilitador_tecnico_asignaciones fta
JOIN usuarios u ON u.id = fta.tecnico_usuario_id
WHERE u.correo='jess@gmail.com';
