# ============================================================================
# CÓDIGO PARA AGREGAR A backend/main.py - TRACKING DE DISPOSITIVOS
# ============================================================================

# 1. AGREGAR ESTE MODELO después de la línea 408 (después de NotificacionResponse)

class DispositivoUpdate(BaseModel):
    usuario_id: int
    dispositivo: str  # 'Android', 'iOS', 'Desktop', 'Desconocido'
    user_agent: Optional[str] = None


# 2. AGREGAR ESTE ENDPOINT después del endpoint de login (después de la línea 675)

@app.post("/actualizar_dispositivo")
async def actualizar_dispositivo(datos: DispositivoUpdate):
    """Actualiza el dispositivo del usuario al hacer login"""
    try:
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="Error de conexión a base de datos")
        
        cursor.execute("""
            UPDATE usuarios 
            SET dispositivo = %s, 
                user_agent = %s,
                ultimo_acceso = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (datos.dispositivo, datos.user_agent, datos.usuario_id))
        
        conn.commit()
        
        return {"success": True, "message": "Dispositivo actualizado"}
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al actualizar dispositivo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/estadisticas/dispositivos")
async def estadisticas_dispositivos():
    """Obtiene estadísticas de dispositivos en tiempo real"""
    try:
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="Error de conexión a base de datos")
        
        # Total de usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]
        
        # Por dispositivo
        cursor.execute("""
            SELECT 
                COALESCE(dispositivo, 'desconocido') as dispositivo,
                COUNT(*) as cantidad,
                ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM usuarios), 0), 2) as porcentaje
            FROM usuarios
            GROUP BY dispositivo
            ORDER BY cantidad DESC
        """)
        dispositivos = cursor.fetchall()
        
        # Por rol
        cursor.execute("""
            SELECT 
                rol,
                COALESCE(dispositivo, 'desconocido') as dispositivo,
                COUNT(*) as cantidad
            FROM usuarios
            GROUP BY rol, dispositivo
            ORDER BY rol, cantidad DESC
        """)
        por_rol = cursor.fetchall()
        
        # Usuarios activos (último acceso en últimos 30 días)
        cursor.execute("""
            SELECT 
                COALESCE(dispositivo, 'desconocido') as dispositivo,
                COUNT(*) as cantidad
            FROM usuarios
            WHERE ultimo_acceso >= NOW() - INTERVAL '30 days'
            GROUP BY dispositivo
            ORDER BY cantidad DESC
        """)
        activos = cursor.fetchall()
        
        return {
            "total_usuarios": total,
            "por_dispositivo": [
                {
                    "dispositivo": d[0],
                    "cantidad": d[1],
                    "porcentaje": float(d[2])
                }
                for d in dispositivos
            ],
            "por_rol": [
                {
                    "rol": r[0],
                    "dispositivo": r[1],
                    "cantidad": r[2]
                }
                for r in por_rol
            ],
            "activos_30_dias": [
                {
                    "dispositivo": a[0],
                    "cantidad": a[1]
                }
                for a in activos
            ]
        }
    except Exception as e:
        print(f"❌ Error al obtener estadísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# 3. MODIFICAR EL ENDPOINT DE LOGIN para actualizar último acceso
# Agregar estas líneas ANTES del return en el endpoint @app.post("/login")
# (alrededor de la línea 665, antes del return):

    # Actualizar último acceso
    try:
        cursor.execute("""
            UPDATE usuarios 
            SET ultimo_acceso = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (user[0],))
        conn.commit()
    except Exception as e:
        print(f"⚠️ Error al actualizar último acceso: {e}")


# ============================================================================
# FIN DEL CÓDIGO PARA AGREGAR
# ============================================================================
