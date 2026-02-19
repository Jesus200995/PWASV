Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "DESPLIEGUE AUTOMATICO AL VPS" -ForegroundColor Cyan  
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Subiendo script de despliegue..." -ForegroundColor Yellow
scp desplegar_vps.sh root@31.97.8.51:/tmp/

Write-Host ""
Write-Host "2. Ejecutando script en el servidor..." -ForegroundColor Yellow
ssh root@31.97.8.51 "bash /tmp/desplegar_vps.sh"

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "COMPLETADO" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ahora prueba:" -ForegroundColor Yellow
Write-Host "  cd admin-pwa" -ForegroundColor White
Write-Host "  npm run dev" -ForegroundColor White
Write-Host "  Abre: http://localhost:5173/#/debug-buscador" -ForegroundColor White
Write-Host ""
