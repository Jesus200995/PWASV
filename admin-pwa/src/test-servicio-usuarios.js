// Script de prueba para verificar el servicio de usuarios desde el frontend
import usuariosService from './usuariosService.js';

console.log('🧪 Probando servicio de usuarios desde frontend...');

async function probarServicio() {
    try {
        console.log('\n1️⃣ Probando obtener todos los usuarios...');
        const usuarios = await usuariosService.obtenerUsuarios();
        console.log('✅ Usuarios obtenidos:', usuarios);
        console.log(`📊 Total usuarios: ${usuarios.length}`);
        
        if (usuarios.length > 0) {
            console.log('\n2️⃣ Probando obtener usuario específico...');
            const primerUsuario = usuarios[0];
            const usuario = await usuariosService.obtenerUsuario(primerUsuario.id);
            console.log('✅ Usuario específico:', usuario);
            
            console.log('\n3️⃣ Probando obtener múltiples usuarios por IDs...');
            const ids = usuarios.slice(0, 3).map(u => u.id);
            const usuariosMultiples = await usuariosService.obtenerUsuariosPorIds(ids);
            console.log('✅ Usuarios múltiples:', usuariosMultiples);
        }
        
    } catch (error) {
        console.error('❌ Error en pruebas:', error);
    }
}

probarServicio().then(() => {
    console.log('\n✅ Pruebas del servicio completadas');
});
