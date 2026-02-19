

# ========== ENDPOINT DE BÚSQUEDA DE USUARIOS SIN CONFLICTO DE RUTAS ==========
@app.get("/api/buscar-usuarios")
async def buscar_usuarios_api(correo: Optional[str] = None, nombre: Optional[str] = None, 
                              curp: Optional[str] = None, cargo: Optional[str] = None):
    """Buscar usuarios por diferentes criterios con OR - Sin conflicto de rutas"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexion a la base de datos")
        
        condiciones = []
        parametros = []
        
        if correo:
            condiciones.append("correo ILIKE %s")
            parametros.append(f"%{correo}%")
        
        if nombre:
            condiciones.append("nombre_completo ILIKE %s")
            parametros.append(f"%{nombre}%")
        
        if curp:
            condiciones.append("curp ILIKE %s")
            parametros.append(f"%{curp.upper()}%")
        
        if cargo:
            condiciones.append("cargo ILIKE %s")
            parametros.append(f"%{cargo}%")
        
        if not condiciones:
            raise HTTPException(status_code=400, detail="Debe proporcionar al menos un criterio de busqueda")
        
        # Usar OR para buscar en cualquiera de los campos
        consulta = f"""
            SELECT id, correo, nombre_completo, cargo, supervisor, curp, telefono
            FROM usuarios 
            WHERE {' OR '.join(condiciones)}
            ORDER BY id DESC
            LIMIT 100
        """
        
        print(f"API buscar-usuarios: {consulta}")
        print(f"Parametros: {parametros}")
        
        cursor.execute(consulta, parametros)
        resultados = cursor.fetchall()
        
        usuarios = []
        for row in resultados:
            usuario = {
                "id": row[0],
                "correo": row[1],
                "nombre_completo": row[2],
                "cargo": row[3],
                "supervisor": row[4],
                "curp": row[5],
                "telefono": row[6],
                "rol": "user"
            }
            usuarios.append(usuario)
        
        print(f"Encontrados: {len(usuarios)} usuarios")
        return {"usuarios": usuarios}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en buscar-usuarios: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
