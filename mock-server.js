#!/usr/bin/env node

/**
 * Servidor Mock para pruebas de la API de Reportes
 * Simula el endpoint /historial/{usuario_id} con datos de prueba
 * 
 * Uso: node mock-server.js
 * Luego accede a: http://localhost:8000/historial/1
 */

const express = require('express');
const cors = require('cors');
const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Datos de prueba
const usuariosPrueba = {
    1: {
        id: 1,
        nombre_completo: 'Juan Pérez García',
        correo: 'juan.perez@ejemplo.com',
        cargo: 'Asistente Administrativo',
        curp: 'PEGJ820315HDFRRN09'
    },
    2: {
        id: 2,
        nombre_completo: 'María López Martínez',
        correo: 'maria.lopez@ejemplo.com',
        cargo: 'Coordinadora',
        curp: 'LOXM900520HDFNRR03'
    }
};

// Función para generar actividades de prueba
function generarActividadesPrueba(usuarioId, fechaInicio, fechaFin) {
    const actividades = [];
    const tipos = ['entrada', 'salida', 'entrada', 'salida'];
    
    const inicio = new Date(fechaInicio);
    const fin = new Date(fechaFin);
    
    let fecha = new Date(inicio);
    let id = 1;
    
    while (fecha <= fin) {
        // Solo añadir actividades en días de semana (lunes a viernes)
        if (fecha.getDay() !== 0 && fecha.getDay() !== 6) {
            const fechaStr = fecha.toISOString().split('T')[0];
            
            // Entrada matutina
            actividades.push({
                id: id++,
                usuario_id: usuarioId,
                tipo: 'entrada',
                descripcion: 'Registro de entrada',
                fecha: fechaStr,
                hora: '08:' + String(Math.floor(Math.random() * 60)).padStart(2, '0'),
                detalles: 'Entrada normal',
                creado_en: fechaStr + 'T08:00:00',
                usuario_nombre: usuariosPrueba[usuarioId]?.nombre_completo,
                usuario_correo: usuariosPrueba[usuarioId]?.correo,
                usuario_curp: usuariosPrueba[usuarioId]?.curp,
                usuario_cargo: usuariosPrueba[usuarioId]?.cargo
            });
            
            // Salida vespertina
            actividades.push({
                id: id++,
                usuario_id: usuarioId,
                tipo: 'salida',
                descripcion: 'Registro de salida',
                fecha: fechaStr,
                hora: '17:' + String(Math.floor(Math.random() * 60)).padStart(2, '0'),
                detalles: 'Salida normal',
                creado_en: fechaStr + 'T17:00:00',
                usuario_nombre: usuariosPrueba[usuarioId]?.nombre_completo,
                usuario_correo: usuariosPrueba[usuarioId]?.correo,
                usuario_curp: usuariosPrueba[usuarioId]?.curp,
                usuario_cargo: usuariosPrueba[usuarioId]?.cargo
            });
        }
        
        fecha.setDate(fecha.getDate() + 1);
    }
    
    return actividades.reverse();
}

// Endpoints

// 1. Debug: Estructura de usuarios
app.get('/debug/usuarios-estructura', (req, res) => {
    res.json({
        total_usuarios: Object.keys(usuariosPrueba).length,
        usuarios: Object.values(usuariosPrueba).map(u => ({
            id: u.id,
            nombre: u.nombre_completo,
            correo: u.correo
        }))
    });
});

// 2. Obtener usuario específico
app.get('/usuario/:id', (req, res) => {
    const usuarioId = parseInt(req.params.id);
    const usuario = usuariosPrueba[usuarioId];
    
    if (usuario) {
        res.json(usuario);
    } else {
        res.status(404).json({ 
            error: 'Usuario no encontrado',
            mensaje: `No existe usuario con ID ${usuarioId}`
        });
    }
});

// 3. Obtener historial con filtros
app.get('/historial/:id', (req, res) => {
    const usuarioId = parseInt(req.params.id);
    const usuario = usuariosPrueba[usuarioId];
    
    if (!usuario) {
        return res.status(404).json({ 
            error: 'Usuario no encontrado',
            detail: `No existe usuario con ID ${usuarioId}`
        });
    }
    
    // Parámetros de filtro
    const fechaInicio = req.query.fecha_inicio || '2026-01-01';
    const fechaFin = req.query.fecha_fin || '2026-01-31';
    const tipo = req.query.tipo; // 'entrada', 'salida', etc.
    const limit = parseInt(req.query.limit) || 100;
    
    console.log(`📊 Historial solicitado para usuario ${usuarioId}`);
    console.log(`   Período: ${fechaInicio} a ${fechaFin}`);
    if (tipo) console.log(`   Filtro tipo: ${tipo}`);
    console.log(`   Límite: ${limit}`);
    
    // Generar actividades
    let actividades = generarActividadesPrueba(usuarioId, fechaInicio, fechaFin);
    
    // Aplicar filtro de tipo si existe
    if (tipo) {
        actividades = actividades.filter(a => a.tipo === tipo);
    }
    
    // Aplicar límite
    actividades = actividades.slice(0, limit);
    
    console.log(`   ✅ Retornando ${actividades.length} actividades\n`);
    
    res.json({
        historial: actividades,
        total: actividades.length,
        usuario: {
            id: usuario.id,
            nombre: usuario.nombre_completo
        }
    });
});

// 4. Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Iniciar servidor
const PORT = 8000;
const HOST = '0.0.0.0';

app.listen(PORT, HOST, () => {
    console.log('\n' + '='.repeat(70));
    console.log('🟢 SERVIDOR MOCK INICIADO');
    console.log('='.repeat(70));
    console.log(`\n📍 Escuchando en: http://localhost:${PORT}`);
    console.log(`\n📋 Endpoints disponibles:\n`);
    console.log(`   GET /debug/usuarios-estructura`);
    console.log(`       Retorna lista de usuarios disponibles\n`);
    console.log(`   GET /usuario/:id`);
    console.log(`       Obtiene datos de usuario específico\n`);
    console.log(`   GET /historial/:id`);
    console.log(`       Obtiene historial con filtros opcionales:`);
    console.log(`       - fecha_inicio (YYYY-MM-DD)`);
    console.log(`       - fecha_fin (YYYY-MM-DD)`);
    console.log(`       - tipo (entrada/salida)`);
    console.log(`       - limit (defecto 100)\n`);
    console.log(`   GET /health`);
    console.log(`       Health check\n`);
    console.log('🧪 Ejemplos de prueba:\n');
    console.log(`   http://localhost:${PORT}/historial/1`);
    console.log(`   http://localhost:${PORT}/historial/1?fecha_inicio=2026-01-01&fecha_fin=2026-01-31`);
    console.log(`   http://localhost:${PORT}/historial/1?tipo=entrada`);
    console.log(`   http://localhost:${PORT}/historial/1?fecha_inicio=2026-01-01&fecha_fin=2026-01-31&tipo=salida\n`);
    console.log('⏹️  Presiona Ctrl+C para detener el servidor\n');
    console.log('='.repeat(70) + '\n');
});

// Manejo de errores
app.use((err, req, res, next) => {
    console.error('❌ Error:', err);
    res.status(500).json({ 
        error: 'Error interno del servidor',
        mensaje: err.message 
    });
});
