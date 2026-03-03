#!/usr/bin/env python3
"""
Script de prueba para diagnosticar el endpoint estadisticas-pdf cuando se filtra por territorio
"""

import psycopg2
import sys

def conectar():
    return psycopg2.connect(
        host='31.97.8.51',
        database='app_registros',
        user='jesus',
        password='2025'
    )

def main():
    territorio = sys.argv[1] if len(sys.argv) > 1 else 'Ocosingo'
    mes = sys.argv[2] if len(sys.argv) > 2 else None
    anio = int(sys.argv[3]) if len(sys.argv) > 3 else 2026
    
    print(f"📊 Probando estadísticas para territorio: {territorio}")
    print(f"   Mes: {mes}, Año: {anio}")
    
    conn = conectar()
    cursor = conn.cursor()
    
    # Query 1: Obtener territorios con técnicos
    print("\n1️⃣ Query de territorios:")
    query_territorios = """
        SELECT 
            u.territorio,
            COUNT(DISTINCT CASE WHEN UPPER(COALESCE(u.cargo, '')) LIKE '%SOCIAL%' THEN u.id END) as tecnicos_social,
            COUNT(DISTINCT CASE WHEN UPPER(COALESCE(u.cargo, '')) LIKE '%PRODUCTIVO%' THEN u.id END) as tecnicos_productivo,
            COUNT(DISTINCT u.id) as total_tecnicos
        FROM usuarios u
        WHERE u.territorio IS NOT NULL 
        AND u.territorio != ''
        AND COALESCE(u.activo, true) = TRUE
        AND u.territorio = %s
        GROUP BY u.territorio 
        ORDER BY u.territorio
    """
    
    try:
        cursor.execute(query_territorios, (territorio,))
        territorios_data = cursor.fetchall()
        print(f"   Resultado: {territorios_data}")
        
        if not territorios_data:
            print("   ⚠️ No se encontraron datos para este territorio")
            
            # Verificar si el territorio existe
            cursor.execute("SELECT DISTINCT territorio FROM usuarios WHERE territorio ILIKE %s LIMIT 10", (f'%{territorio}%',))
            similares = cursor.fetchall()
            print(f"   Territorios similares: {similares}")
            return
        
        # Query 2: Obtener reportes del territorio
        t = territorios_data[0]
        territorio_nombre = t[0]
        
        print(f"\n2️⃣ Query de reportes para {territorio_nombre}:")
        reportes_query = """
            SELECT 
                COUNT(r.id) as total_reportes,
                COUNT(CASE WHEN COALESCE(r.firmado_supervisor, false) = true THEN 1 END) as firmados,
                COUNT(CASE WHEN COALESCE(r.firmado_supervisor, false) = false THEN 1 END) as pendientes
            FROM reportes_generados r
            INNER JOIN usuarios u ON r.usuario_id = u.id
            WHERE u.territorio = %s
        """
        reportes_params = [territorio_nombre]
        
        if mes:
            reportes_query += " AND r.mes = %s"
            reportes_params.append(mes)
        if anio:
            reportes_query += " AND r.anio = %s"
            reportes_params.append(anio)
        
        print(f"   Params: {reportes_params}")
        cursor.execute(reportes_query, tuple(reportes_params))
        reportes_stats = cursor.fetchone()
        print(f"   Resultado: {reportes_stats}")
        
        print("\n✅ Todo funcionó correctamente")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
