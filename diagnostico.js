#!/usr/bin/env node

/**
 * Script de diagnóstico para verificar el estado del sistema completo
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

console.log('\n' + '='.repeat(70));
console.log('🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA PWASV');
console.log('='.repeat(70) + '\n');

const diagnostics = [];

// 1. Verificar Node.js
console.log('1️⃣  Verificando Node.js...');
const nodeVersion = process.version;
console.log(`   ✅ Node.js: ${nodeVersion}\n`);
diagnostics.push({ check: 'Node.js', status: 'OK', version: nodeVersion });

// 2. Verificar npm
console.log('2️⃣  Verificando npm...');
try {
    const npmVersion = require('child_process').execSync('npm --version', { encoding: 'utf-8' }).trim();
    console.log(`   ✅ npm: ${npmVersion}\n`);
    diagnostics.push({ check: 'npm', status: 'OK', version: npmVersion });
} catch (error) {
    console.log('   ❌ npm no encontrado\n');
    diagnostics.push({ check: 'npm', status: 'ERROR' });
}

// 3. Verificar estructura de carpetas
console.log('3️⃣  Verificando estructura de carpetas...');
const requiredDirs = [
    'c:\\Users\\ASUS\\Music\\PWASV\\PWASV\\backend',
    'c:\\Users\\ASUS\\Music\\PWASV\\PWASV\\pwasuper',
    'c:\\Users\\ASUS\\Music\\PWASV\\PWASV\\admin-pwa'
];

requiredDirs.forEach(dir => {
    if (fs.existsSync(dir)) {
        console.log(`   ✅ ${path.basename(dir)}`);
        diagnostics.push({ check: `Carpeta ${path.basename(dir)}`, status: 'OK' });
    } else {
        console.log(`   ❌ ${path.basename(dir)}`);
        diagnostics.push({ check: `Carpeta ${path.basename(dir)}`, status: 'MISSING' });
    }
});
console.log();

// 4. Verificar main.py
console.log('4️⃣  Verificando backend/main.py...');
if (fs.existsSync('c:\\Users\\ASUS\\Music\\PWASV\\PWASV\\backend\\main.py')) {
    const size = fs.statSync('c:\\Users\\ASUS\\Music\\PWASV\\PWASV\\backend\\main.py').size;
    console.log(`   ✅ main.py (${size} bytes)\n`);
    diagnostics.push({ check: 'Backend main.py', status: 'OK', size });
} else {
    console.log('   ❌ main.py no encontrado\n');
    diagnostics.push({ check: 'Backend main.py', status: 'MISSING' });
}

// 5. Verificar pwasuper/package.json
console.log('5️⃣  Verificando pwasuper/package.json...');
const packageJsonPath = 'c:\\Users\\ASUS\\Music\\PWASV\\PWASV\\pwasuper\\package.json';
if (fs.existsSync(packageJsonPath)) {
    const pkg = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
    console.log(`   ✅ Proyecto: ${pkg.name}`);
    console.log(`   ✅ Versión: ${pkg.version}\n`);
    diagnostics.push({ check: 'PWA Super package.json', status: 'OK', project: pkg.name });
} else {
    console.log('   ❌ package.json no encontrado\n');
    diagnostics.push({ check: 'PWA Super package.json', status: 'MISSING' });
}

// 6. Verificar servicios key
console.log('6️⃣  Verificando archivos clave del frontend...');
const keyFiles = [
    'c:\\Users\\ASUS\\Music\\PWASV\\PWASV\\pwasuper\\src\\services\\reportesService.js',
    'c:\\Users\\ASUS\\Music\\PWASV\\PWASV\\pwasuper\\src\\utils\\network.js',
    'c:\\Users\\ASUS\\Music\\PWASV\\PWASV\\pwasuper\\src\\views\\Reportes.vue'
];

keyFiles.forEach(file => {
    if (fs.existsSync(file)) {
        const name = path.basename(file);
        console.log(`   ✅ ${name}`);
        diagnostics.push({ check: `Archivo ${name}`, status: 'OK' });
    } else {
        const name = path.basename(file);
        console.log(`   ❌ ${name}`);
        diagnostics.push({ check: `Archivo ${name}`, status: 'MISSING' });
    }
});
console.log();

// 7. Verificar puerto 8000
console.log('7️⃣  Verificando puerto 8000...');
const net = require('net');
const server = net.createServer();
server.once('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.log('   ⚠️  Puerto 8000 EN USO (Backend está corriendo)');
        diagnostics.push({ check: 'Puerto 8000', status: 'IN_USE' });
    } else {
        console.log('   ❌ Error: ' + err.message);
        diagnostics.push({ check: 'Puerto 8000', status: 'ERROR' });
    }
    console.log();
});

server.once('listening', () => {
    server.close();
    console.log('   ✅ Puerto 8000 disponible (Backend NO está corriendo)');
    console.log('   ⚠️  El backend debe iniciarse manualmente\n');
    diagnostics.push({ check: 'Puerto 8000', status: 'AVAILABLE' });
});

server.listen(8000, '127.0.0.1');

// 8. Verificar puerto 5173
console.log('8️⃣  Verificando puerto 5173...');
const server5173 = net.createServer();
server5173.once('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.log('   ✅ Puerto 5173 EN USO (Frontend está corriendo)');
        diagnostics.push({ check: 'Puerto 5173', status: 'IN_USE' });
    } else {
        console.log('   ❌ Error: ' + err.message);
        diagnostics.push({ check: 'Puerto 5173', status: 'ERROR' });
    }
    printSummary();
});

server5173.once('listening', () => {
    server5173.close();
    console.log('   ⚠️  Puerto 5173 disponible (Frontend NO está corriendo)');
    console.log('   ℹ️  Ejecuta: cd pwasuper && npm run dev\n');
    diagnostics.push({ check: 'Puerto 5173', status: 'AVAILABLE' });
    printSummary();
});

server5173.listen(5173, '127.0.0.1');

function printSummary() {
    console.log('\n' + '='.repeat(70));
    console.log('📊 RESUMEN DE DIAGNÓSTICO');
    console.log('='.repeat(70) + '\n');

    const states = {
        OK: '✅',
        AVAILABLE: '✅',
        IN_USE: '🟢',
        ERROR: '❌',
        MISSING: '❌'
    };

    const grouped = {};
    diagnostics.forEach(d => {
        const category = d.check.split(' ')[0];
        if (!grouped[category]) grouped[category] = [];
        grouped[category].push(d);
    });

    Object.entries(grouped).forEach(([category, items]) => {
        console.log(`${category}:`);
        items.forEach(item => {
            console.log(`  ${states[item.status] || '⚠️ '} ${item.check}: ${item.status}`);
        });
        console.log();
    });

    console.log('='.repeat(70));
    console.log('\n📋 PRÓXIMOS PASOS:\n');
    console.log('1. Inicia el backend (en una terminal nueva):');
    console.log('   cd c:\\Users\\ASUS\\Music\\PWASV\\PWASV\\backend');
    console.log('   python main.py\n');
    console.log('2. El frontend debe estar corriendo en: http://localhost:5173\n');
    console.log('3. Accede a Reportes para probar el filtrador\n');
    console.log('4. Si sigue sin funcionar, abre: http://localhost:5173/test-api-directo.html\n');
}
