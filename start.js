#!/usr/bin/env node

/**
 * Script de inicio automático para PWASV
 * Inicia Mock Server + Frontend en la configuración correcta
 * 
 * Uso: node start.js
 */

const { spawn } = require('child_process');
const path = require('path');
const os = require('os');

console.clear();

console.log(`
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║         🚀 PWA SUPER - SISTEMA DE INICIACIÓN AUTOMÁTICA    ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

📋 Este script iniciará automáticamente:
   1. Mock Server (Puerto 8000)
   2. Frontend Dev (Puerto 5173)

`);

// Detectar SO
const isWindows = os.platform() === 'win32';

// Rutas
const workspaceRoot = __dirname;
const backendDir = path.join(workspaceRoot);
const frontendDir = path.join(workspaceRoot, 'pwasuper');

console.log(`📂 Workspace: ${workspaceRoot}\n`);

// Funciones para iniciar procesos
function startMockServer() {
    return new Promise((resolve, reject) => {
        console.log('🔄 Iniciando Mock Server...\n');
        
        const mockProcess = spawn('node', ['mock-server.js'], {
            cwd: backendDir,
            stdio: 'inherit'
        });

        mockProcess.on('error', (err) => {
            console.error('❌ Error iniciando Mock Server:', err);
            reject(err);
        });

        // Dar tiempo para que inicie
        setTimeout(() => {
            console.log('\n✅ Mock Server iniciado en puerto 8000\n');
            resolve(mockProcess);
        }, 2000);
    });
}

function startFrontend() {
    return new Promise((resolve, reject) => {
        console.log('🔄 Iniciando Frontend...\n');
        
        const cmd = isWindows ? 'npm.cmd' : 'npm';
        const frontendProcess = spawn(cmd, ['run', 'dev'], {
            cwd: frontendDir,
            stdio: 'inherit'
        });

        frontendProcess.on('error', (err) => {
            console.error('❌ Error iniciando Frontend:', err);
            reject(err);
        });

        // Dar tiempo para que inicie
        setTimeout(() => {
            console.log('\n✅ Frontend iniciado en puerto 5173\n');
            resolve(frontendProcess);
        }, 3000);
    });
}

// Función principal
async function start() {
    try {
        // Iniciar en paralelo
        const [mockProcess, frontendProcess] = await Promise.all([
            startMockServer(),
            startFrontend()
        ]);

        console.log(`
╔════════════════════════════════════════════════════════════╗
║                   ✅ SISTEMA INICIADO                     ║
╚════════════════════════════════════════════════════════════╝

🎯 Servicios disponibles:

   📱 Frontend:      http://localhost:5173
   🔗 API Mock:      http://localhost:8000
   🧪 Test API:      http://localhost:5173/test-api-directo.html

📋 Próximos pasos:

   1. Abre http://localhost:5173 en tu navegador
   2. Login si es necesario
   3. Navega a Reportes
   4. Cambia el mes/año para probar el filtrador
   5. Abre DevTools (F12) → Console para ver logs

🔍 Para debugging:

   • Console de navegador (F12)
   • Network tab para ver peticiones
   • Test Page: http://localhost:5173/test-api-directo.html

⏹️  Para detener: Presiona Ctrl+C en esta ventana

════════════════════════════════════════════════════════════

`);

        // Mantener procesos activos
        process.on('SIGINT', () => {
            console.log('\n\n🛑 Deteniendo servicios...\n');
            mockProcess.kill();
            frontendProcess.kill();
            process.exit(0);
        });

    } catch (error) {
        console.error('\n❌ Error fatal:', error.message);
        console.log('\n📝 Verifica que:');
        console.log('   1. Node.js esté instalado');
        console.log('   2. npm esté disponible');
        console.log('   3. Estés en el directorio correcto');
        console.log('   4. Los puertos 8000 y 5173 no estén en uso');
        process.exit(1);
    }
}

// Iniciar
start();
