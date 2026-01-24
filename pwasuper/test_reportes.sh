#!/bin/bash
# Script de prueba del módulo de Reportes
# Ejecutar desde: c:\Users\ASUS\Music\PWASV\PWASV\pwasuper

echo "🧪 Iniciando pruebas del módulo de Reportes..."
echo ""

# Verificar que las dependencias están instaladas
echo "✅ Verificando dependencias..."
npm list jspdf html2canvas 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: jspdf o html2canvas no instalados"
    echo "📦 Instalando dependencias..."
    npm install jspdf html2canvas
fi

# Verificar que los archivos existen
echo ""
echo "✅ Verificando archivos creados..."

FILES=(
    "src/services/reportesService.js"
    "src/components/FirmaDigital.vue"
    "src/views/Reportes.vue"
    "GUIA_REPORTES.md"
    "RESUMEN_TECNICO_REPORTES.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file - NO ENCONTRADO"
    fi
done

# Verificar rutas en router
echo ""
echo "✅ Verificando configuración del router..."
if grep -q "Reportes" "src/router/index.js"; then
    echo "   ✅ Ruta de Reportes configurada"
else
    echo "   ❌ Ruta de Reportes no encontrada en router"
fi

if grep -q "/reportes" "src/router/index.js"; then
    echo "   ✅ Path /reportes configurado"
else
    echo "   ❌ Path /reportes no encontrado"
fi

# Verificar menú en App.vue
echo ""
echo "✅ Verificando menú principal..."
if grep -q "/reportes" "src/App.vue"; then
    echo "   ✅ Enlace a reportes en App.vue"
else
    echo "   ❌ Enlace a reportes no encontrado en App.vue"
fi

echo ""
echo "🎉 Verificación completada"
echo ""
echo "📋 Próximos pasos:"
echo "1. Ejecutar: npm run dev"
echo "2. Abrir: http://localhost:3003"
echo "3. Iniciar sesión"
echo "4. Ir a: Menú > Reportes"
echo "5. Probar generación de PDF y CSV"
