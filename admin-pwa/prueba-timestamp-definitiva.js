// PRUEBA DEFINITIVA DE TIMESTAMPS OFFLINE
// Script para validar que los timestamps offline se preserven correctamente

import axios from 'axios';
import FormData from 'form-data';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const BASE_URL = 'http://localhost:8000';

// Simular una imagen de prueba
function crearImagenPrueba() {
    const imagePath = path.join(__dirname, 'test-image.jpg');
    
    // Crear un archivo simple para la prueba si no existe
    if (!fs.existsSync(imagePath)) {
        const buffer = Buffer.from('JPEG_TEST_DATA', 'utf-8');
        fs.writeFileSync(imagePath, buffer);
    }
    
    return imagePath;
}

async function probarTimestampOffline() {
    console.log('🧪 INICIANDO PRUEBA DEFINITIVA DE TIMESTAMPS OFFLINE');
    console.log('=' .repeat(60));
    
    try {
        // Crear imagen de prueba
        const imagePath = crearImagenPrueba();
        
        // TIMESTAMP OFFLINE SIMULADO (hace 2 horas)
        const fechaOffline = new Date();
        fechaOffline.setHours(fechaOffline.getHours() - 2);
        const timestampOffline = fechaOffline.toISOString();
        
        console.log('📅 DATOS DE PRUEBA:');
        console.log(`   Timestamp offline: ${timestampOffline}`);
        console.log(`   Fecha offline: ${fechaOffline.toLocaleString()}`);
        console.log(`   Hora actual: ${new Date().toLocaleString()}`);
        console.log(`   Diferencia: 2 horas atrás`);
        console.log('');
        
        // PROBAR REGISTRO NORMAL
        console.log('🔬 PROBANDO REGISTRO NORMAL CON TIMESTAMP OFFLINE...');
        
        const formDataRegistro = new FormData();
        formDataRegistro.append('usuario_id', '1');
        formDataRegistro.append('actividad', 'PRUEBA TIMESTAMP OFFLINE');
        formDataRegistro.append('latitud', '19.4326');
        formDataRegistro.append('longitud', '-99.1332');
        formDataRegistro.append('foto', fs.createReadStream(imagePath));
        formDataRegistro.append('timestamp_offline', timestampOffline);
        
        console.log('📤 Enviando registro con timestamp offline...');
        console.log(`   timestamp_offline: ${timestampOffline}`);
        
        const responseRegistro = await axios.post(`${BASE_URL}/registro`, formDataRegistro, {
            headers: {
                ...formDataRegistro.getHeaders(),
            },
        });
        
        console.log('✅ RESPUESTA DEL SERVIDOR (Registro):');
        console.log(JSON.stringify(responseRegistro.data, null, 2));
        console.log('');
        
        // PROBAR ENTRADA DE ASISTENCIA
        console.log('🔬 PROBANDO ENTRADA DE ASISTENCIA CON TIMESTAMP OFFLINE...');
        
        const fechaEntrada = new Date();
        fechaEntrada.setHours(fechaEntrada.getHours() - 1);
        const timestampEntrada = fechaEntrada.toISOString();
        
        const formDataEntrada = new FormData();
        formDataEntrada.append('usuario_id', '2');
        formDataEntrada.append('latitud', '19.4326');
        formDataEntrada.append('longitud', '-99.1332');
        formDataEntrada.append('descripcion', 'ENTRADA OFFLINE HACE 1 HORA');
        formDataEntrada.append('foto', fs.createReadStream(imagePath));
        formDataEntrada.append('timestamp_offline', timestampEntrada);
        
        console.log('📤 Enviando entrada con timestamp offline...');
        console.log(`   timestamp_offline: ${timestampEntrada}`);
        
        const responseEntrada = await axios.post(`${BASE_URL}/asistencia/entrada`, formDataEntrada, {
            headers: {
                ...formDataEntrada.getHeaders(),
            },
        });
        
        console.log('✅ RESPUESTA DEL SERVIDOR (Entrada):');
        console.log(JSON.stringify(responseEntrada.data, null, 2));
        console.log('');
        
        // VERIFICAR RESULTADOS
        console.log('🔍 VERIFICACIÓN DE RESULTADOS:');
        console.log('=' .repeat(40));
        
        // Verificar registro
        if (responseRegistro.data.timestamp) {
            const timestampGuardado = new Date(responseRegistro.data.timestamp);
            const diferencia = Math.abs(timestampGuardado - fechaOffline);
            const diferenciaMinutos = diferencia / (1000 * 60);
            
            console.log(`📊 REGISTRO:`);
            console.log(`   Timestamp enviado: ${timestampOffline}`);
            console.log(`   Timestamp guardado: ${responseRegistro.data.timestamp}`);
            console.log(`   Diferencia: ${diferenciaMinutos.toFixed(2)} minutos`);
            
            if (diferenciaMinutos < 5) {
                console.log('   ✅ CORRECTO: Timestamp offline preservado');
            } else {
                console.log('   ❌ ERROR: Timestamp no preservado correctamente');
            }
        }
        
        // Verificar entrada
        if (responseEntrada.data.hora_entrada) {
            const horaEntradaGuardada = new Date(responseEntrada.data.hora_entrada);
            const diferencia = Math.abs(horaEntradaGuardada - fechaEntrada);
            const diferenciaMinutos = diferencia / (1000 * 60);
            
            console.log(`📊 ENTRADA:`);
            console.log(`   Timestamp enviado: ${timestampEntrada}`);
            console.log(`   Hora entrada guardada: ${responseEntrada.data.hora_entrada}`);
            console.log(`   Diferencia: ${diferenciaMinutos.toFixed(2)} minutos`);
            
            if (diferenciaMinutos < 5) {
                console.log('   ✅ CORRECTO: Timestamp offline preservado');
            } else {
                console.log('   ❌ ERROR: Timestamp no preservado correctamente');
            }
        }
        
        console.log('');
        console.log('🏁 PRUEBA COMPLETADA');
        
        // Limpiar archivo de prueba
        if (fs.existsSync(imagePath)) {
            fs.unlinkSync(imagePath);
        }
        
    } catch (error) {
        console.error('❌ ERROR EN LA PRUEBA:');
        console.error('Error:', error.message);
        
        if (error.response) {
            console.error('Status:', error.response.status);
            console.error('Data:', error.response.data);
        }
        
        // Revisar logs del backend
        console.log('');
        console.log('💡 RECOMENDACIÓN: Revisar los logs del backend para más detalles');
        console.log('   Los logs mostrarán exactamente cómo se procesan los timestamps');
    }
}

// Ejecutar la prueba
probarTimestampOffline();
