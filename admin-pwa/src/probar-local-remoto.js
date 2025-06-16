// Script para probar endpoints locales y remotos
console.log('🧪 Probando endpoints locales y remotos...');

async function probarEndpoint(baseUrl, descripcion) {
    console.log(`\n🔍 Probando ${descripcion}: ${baseUrl}`);
    
    try {
        // Probar GET /usuarios
        console.log('  📡 GET /usuarios...');
        const response = await fetch(`${baseUrl}/usuarios`);
        console.log(`  Status: ${response.status} ${response.statusText}`);
        
        if (response.ok) {
            const data = await response.json();
            console.log('  ✅ Respuesta exitosa:', data);
        } else {
            const errorText = await response.text();
            console.log('  ❌ Error:', errorText);
        }
    } catch (error) {
        console.log(`  ❌ Error de conexión: ${error.message}`);
    }
}

async function probarAmbos() {
    await probarEndpoint('http://localhost:8000', 'Servidor Local');
    await probarEndpoint('https://apipwa.sembrandodatos.com', 'Servidor Remoto');
}

probarAmbos().then(() => {
    console.log('\n✅ Pruebas completadas');
});
