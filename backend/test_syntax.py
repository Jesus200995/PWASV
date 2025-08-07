#!/usr/bin/env python3
"""
Script para verificar que la sintaxis del backend está correcta
"""

try:
    import main
    print("✅ Sintaxis del backend correcta")
    print("✅ Modelos definidos correctamente")
    
    # Verificar que los endpoints están definidos
    app = main.app
    routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append(f"{route.methods} {route.path}")
    
    print(f"✅ {len(routes)} endpoints encontrados")
    
    # Buscar endpoints específicos que acabamos de agregar
    terminos_endpoints = [r for r in routes if 'terminos' in r]
    if terminos_endpoints:
        print("✅ Endpoints de términos encontrados:")
        for endpoint in terminos_endpoints:
            print(f"  - {endpoint}")
    else:
        print("⚠️  No se encontraron endpoints de términos")
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except SyntaxError as e:
    print(f"❌ Error de sintaxis: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
