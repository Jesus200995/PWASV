# Script para probar el endpoint /historial
Write-Host "🧪 Probando API de Historial" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# URLs a probar
$urls = @(
    "http://localhost:8000",
    "http://127.0.0.1:8000"
)

# ID de usuario para probar (cambiar según sea necesario)
$usuarioId = 1

Write-Host "`n1️⃣  TESTANDO CONEXIÓN AL SERVIDOR" -ForegroundColor Yellow

foreach ($baseUrl in $urls) {
    Write-Host "`nIntentando: $baseUrl"
    
    try {
        $healthResponse = Invoke-WebRequest -Uri "$baseUrl/debug/usuarios-estructura" -Method GET -TimeoutSec 5
        Write-Host "✅ Servidor responde en: $baseUrl" -ForegroundColor Green
        $workingUrl = $baseUrl
        break
    }
    catch {
        Write-Host "❌ No hay conexión en: $baseUrl" -ForegroundColor Red
    }
}

if (-not $workingUrl) {
    Write-Host "`n❌ No se encontró servidor activo" -ForegroundColor Red
    Write-Host "Por favor, asegúrate de que el backend está corriendo:" -ForegroundColor Yellow
    Write-Host "  cd c:\Users\ASUS\Music\PWASV\PWASV\backend"
    Write-Host "  python main.py"
    exit
}

Write-Host "`n2️⃣  OBTENIENDO DATOS DEL USUARIO" -ForegroundColor Yellow

try {
    $usuarioResponse = Invoke-WebRequest -Uri "$workingUrl/usuario/$usuarioId" -Method GET -TimeoutSec 5
    $usuario = $usuarioResponse.Content | ConvertFrom-Json
    Write-Host "✅ Usuario encontrado:" -ForegroundColor Green
    Write-Host "   ID: $($usuario.id)"
    Write-Host "   Nombre: $($usuario.nombre_completo)"
    Write-Host "   Correo: $($usuario.correo)"
}
catch {
    Write-Host "⚠️  No se encontró usuario con ID $usuarioId" -ForegroundColor Yellow
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n3️⃣  OBTENIENDO HISTORIAL SIN FILTROS" -ForegroundColor Yellow

try {
    $historialResponse = Invoke-WebRequest -Uri "$workingUrl/historial/$usuarioId" -Method GET -TimeoutSec 5
    $historial = $historialResponse.Content | ConvertFrom-Json
    
    Write-Host "✅ Historial obtenido:" -ForegroundColor Green
    Write-Host "   Total de registros: $($historial.total)"
    Write-Host "   Usuario ID: $($historial.usuario.id)"
    Write-Host "   Nombre: $($historial.usuario.nombre)"
    
    if ($historial.historial.Count -gt 0) {
        Write-Host "`n   Primeros 3 registros:" -ForegroundColor Cyan
        for ($i = 0; $i -lt [Math]::Min(3, $historial.historial.Count); $i++) {
            $registro = $historial.historial[$i]
            Write-Host "   [$($i+1)] Fecha: $($registro.fecha) | Hora: $($registro.hora) | Tipo: $($registro.tipo)"
        }
    }
}
catch {
    Write-Host "❌ Error obteniendo historial:" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n4️⃣  OBTENIENDO HISTORIAL CON FILTROS DE FECHA" -ForegroundColor Yellow

$fechaInicio = "2026-01-01"
$fechaFin = "2026-01-31"

try {
    $uri = "$workingUrl/historial/$usuarioId`?fecha_inicio=$fechaInicio&fecha_fin=$fechaFin&limit=100"
    Write-Host "   URI: $uri" -ForegroundColor DarkGray
    $historialFiltrado = Invoke-WebRequest -Uri $uri -Method GET -TimeoutSec 5
    $historialData = $historialFiltrado.Content | ConvertFrom-Json
    
    Write-Host "✅ Historial con filtro obtenido:" -ForegroundColor Green
    Write-Host "   Período: $fechaInicio a $fechaFin" -ForegroundColor Cyan
    Write-Host "   Total de registros: $($historialData.total)" -ForegroundColor Cyan
    
    if ($historialData.historial.Count -gt 0) {
        Write-Host "`n   Registros encontrados:" -ForegroundColor Green
        for ($i = 0; $i -lt [Math]::Min(5, $historialData.historial.Count); $i++) {
            $registro = $historialData.historial[$i]
            Write-Host "   [$($i+1)] $($registro.fecha) $($registro.hora) - $($registro.tipo)" -ForegroundColor Green
        }
    }
    else {
        Write-Host "   ⚠️  No hay registros en este período" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "❌ Error con filtro de fecha:" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n5️⃣  RESUMÉN DE LA CONFIGURACIÓN" -ForegroundColor Yellow
Write-Host "   Servidor: $workingUrl" -ForegroundColor Cyan
Write-Host "   Usuario ID: $usuarioId" -ForegroundColor Cyan
Write-Host "   Frontend debe usar: $workingUrl" -ForegroundColor Cyan
Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "✅ Pruebas completadas" -ForegroundColor Green
