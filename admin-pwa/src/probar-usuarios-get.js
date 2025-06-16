// Script para probar los nuevos endpoints de usuarios
console.log('🧪 Probando endpoints de usuarios después de agregar GET...');

async function probarEndpoints() {
    const baseUrl = 'https://apipwa.sembrandodatos.com';
    
    console.log('\n1️⃣ Probando GET /usuarios (obtener todos los usuarios)...');
    try {
        const response = await fetch(`${baseUrl}/usuarios`);
        console.log(`Status: ${response.status} ${response.statusText}`);
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Respuesta exitosa:', data);
            console.log(`📊 Encontrados ${data.usuarios ? data.usuarios.length : 0} usuarios`);
            
            // Si hay usuarios, probar el endpoint individual
            if (data.usuarios && data.usuarios.length > 0) {
                const primerUsuario = data.usuarios[0];
                console.log(`\n2️⃣ Probando GET /usuarios/${primerUsuario.id} (obtener usuario específico)...`);
                
                const responseUsuario = await fetch(`${baseUrl}/usuarios/${primerUsuario.id}`);
                console.log(`Status: ${responseUsuario.status} ${responseUsuario.statusText}`);
                
                if (responseUsuario.ok) {
                    const usuario = await responseUsuario.json();
                    console.log('✅ Usuario específico obtenido:', usuario);
                } else {
                    console.error('❌ Error al obtener usuario específico');
                }
            } else {
                console.log('⚠️ No hay usuarios en la base de datos para probar endpoint individual');
            }
        } else {
            const errorText = await response.text();
            console.error('❌ Error en la respuesta:', errorText);
        }
    } catch (error) {
        console.error('❌ Error de red:', error.message);
    }
}

probarEndpoints().then(() => {
    console.log('\n✅ Pruebas completadas');
});
