#!/usr/bin/env python3
"""
Script para verificar la configuración de zona horaria
y probar que las fechas se guardan correctamente en CDMX
"""

import os
import sys
from datetime import datetime
import pytz

# Configurar zona horaria de Ciudad de México
CDMX_TZ = pytz.timezone("America/Mexico_City")

def verificar_zona_horaria():
    """Verifica que la zona horaria esté configurada correctamente"""
    print("=== VERIFICACIÓN DE ZONA HORARIA ===")
    
    # Fecha UTC actual
    fecha_utc = datetime.utcnow()
    print(f"Fecha UTC actual: {fecha_utc}")
    
    # Fecha en Ciudad de México
    fecha_cdmx = datetime.now(CDMX_TZ)
    print(f"Fecha CDMX actual: {fecha_cdmx}")
    
    # Conversión de UTC a CDMX
    fecha_utc_convertida = fecha_utc.replace(tzinfo=pytz.UTC).astimezone(CDMX_TZ)
    print(f"UTC convertida a CDMX: {fecha_utc_convertida}")
    
    # Verificar que la diferencia es la esperada (UTC-6 o UTC-5 dependiendo del horario de verano)
    offset = fecha_cdmx.utcoffset().total_seconds() / 3600
    print(f"Offset actual: UTC{offset:+.0f}")
    
    if offset in [-6, -5]:
        print("✅ Zona horaria configurada correctamente")
        return True
    else:
        print("❌ Error en la configuración de zona horaria")
        return False

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    print("\n=== VERIFICACIÓN DE DEPENDENCIAS ===")
    
    dependencias = [
        'fastapi',
        'uvicorn', 
        'psycopg2',
        'bcrypt',
        'pydantic',
        'pytz',
        'jose',
        'passlib'
    ]
    
    dependencias_faltantes = []
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NO INSTALADO")
            dependencias_faltantes.append(dep)
    
    if dependencias_faltantes:
        print(f"\n⚠️ Dependencias faltantes: {', '.join(dependencias_faltantes)}")
        print("Ejecuta: pip install " + " ".join(dependencias_faltantes))
        return False
    else:
        print("\n✅ Todas las dependencias están instaladas")
        return True

def simular_registro():
    """Simula la creación de un registro con fecha CDMX"""
    print("\n=== SIMULACIÓN DE REGISTRO ===")
    
    # Simular creación de registro
    fecha_registro = datetime.now(CDMX_TZ)
    print(f"Fecha del registro: {fecha_registro}")
    print(f"Formato ISO: {fecha_registro.isoformat()}")
    
    # Simular conversión para frontend
    fecha_iso = fecha_registro.isoformat()
    fecha_parseada = datetime.fromisoformat(fecha_iso.replace('Z', '+00:00') if fecha_iso.endswith('Z') else fecha_iso)
    
    if fecha_parseada.tzinfo:
        fecha_cdmx_convertida = fecha_parseada.astimezone(CDMX_TZ)
    else:
        fecha_cdmx_convertida = CDMX_TZ.localize(fecha_parseada)
    
    print(f"Fecha convertida para frontend: {fecha_cdmx_convertida}")
    print("✅ Simulación exitosa")

def main():
    """Función principal"""
    print("SCRIPT DE VERIFICACIÓN - FECHAS EN CDMX")
    print("=" * 50)
    
    # Verificaciones
    tz_ok = verificar_zona_horaria()
    deps_ok = verificar_dependencias()
    
    if tz_ok and deps_ok:
        simular_registro()
        print("\n🎉 ¡Todo configurado correctamente!")
        print("\nInstrucciones para el despliegue:")
        print("1. Asegúrate de que el servidor PostgreSQL tenga configurada la zona horaria America/Mexico_City")
        print("2. Si usas Docker, añade la variable de entorno TZ=America/Mexico_City")
        print("3. Reinicia el backend después de instalar las dependencias")
        print("4. Verifica en el frontend que las fechas se muestren correctamente")
    else:
        print("\n❌ Hay problemas en la configuración. Revisa los errores anteriores.")
        sys.exit(1)

if __name__ == "__main__":
    main()
