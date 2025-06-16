# Script para eliminar archivos obsoletos de la migración a Vue.js
# Ejecutar desde: c:\Users\Admin_1\Pictures\PWA\PWASV\admin-pwa\

Write-Host "🧹 Limpiando archivos obsoletos para migración a Vue.js..." -ForegroundColor Cyan
Write-Host ""

# Definir archivos a eliminar
$archivosAEliminar = @(
    "index.html",
    "dashboard.html", 
    "admin.js",
    "style.css"
)

# Mostrar archivos que se van a eliminar
Write-Host "📋 Archivos que serán eliminados:" -ForegroundColor Yellow
foreach ($archivo in $archivosAEliminar) {
    if (Test-Path $archivo) {
        Write-Host "   ❌ $archivo" -ForegroundColor Red
    } else {
        Write-Host "   ⚠️  $archivo (no existe)" -ForegroundColor Gray
    }
}

Write-Host ""

# Confirmar acción
$confirmacion = Read-Host "¿Deseas continuar con la eliminación? (s/N)"

if ($confirmacion -eq "s" -or $confirmacion -eq "S" -or $confirmacion -eq "si" -or $confirmacion -eq "Si") {
    Write-Host ""
    Write-Host "🗑️  Eliminando archivos..." -ForegroundColor Red
    
    foreach ($archivo in $archivosAEliminar) {
        if (Test-Path $archivo) {
            try {
                Remove-Item $archivo -Force
                Write-Host "   ✅ Eliminado: $archivo" -ForegroundColor Green
            }
            catch {
                Write-Host "   ❌ Error eliminando: $archivo - $($_.Exception.Message)" -ForegroundColor Red
            }
        } else {
            Write-Host "   ⚠️  No existe: $archivo" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    Write-Host "✨ Limpieza completada. Ahora puedes proceder con la instalación de Vue.js:" -ForegroundColor Green
    Write-Host "   1. npm install" -ForegroundColor Cyan
    Write-Host "   2. npm run dev" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Operación cancelada. No se eliminaron archivos." -ForegroundColor Yellow
    Write-Host ""
}

# Mostrar estado final
Write-Host "📁 Estado actual del directorio:" -ForegroundColor Cyan
Get-ChildItem -Name | Where-Object { $_ -notin @("node_modules", ".git", "cleanup.ps1") } | ForEach-Object {
    Write-Host "   📄 $_" -ForegroundColor White
}

Write-Host ""
Write-Host "🎯 Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
