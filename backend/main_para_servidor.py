from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
import bcrypt
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext

app = FastAPI()

# Permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ¡ajusta esto en producción!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a PostgreSQL
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

try:
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cursor = conn.cursor()
    print("✅ Conexión a la base de datos exitosa")
except Exception as e:
    print(f"❌ Error conectando a la base de datos: {e}")
    conn = None
    cursor = None

# Carpeta para guardar fotos
FOTOS_DIR = "fotos"
os.makedirs(FOTOS_DIR, exist_ok=True)

# Modelos para autenticación
class UserCreate(BaseModel):
    correo: str
    nombre_completo: str
    cargo: str
    supervisor: str = None
    contrasena: str
    curp: str  # CURP obligatoria

class UserLogin(BaseModel):
    correo: str
    contrasena: str

class PasswordChange(BaseModel):
    usuario_id: int
    nueva_contrasena: str

# Montar carpeta de fotos para servir estáticamente
app.mount("/fotos", StaticFiles(directory="fotos"), name="fotos")

# Configuración para autenticación JWT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "cambia-esto-por-una-clave-muy-larga-y-unica-para-admin-2025"  # Cambia esto por seguridad

# Endpoints de autenticación
@app.post("/usuarios")
async def crear_usuario(usuario: UserCreate):
    try:
        # Validación de CURP obligatoria
        if not usuario.curp or not usuario.curp.strip():
            raise HTTPException(status_code=400, detail="La CURP es obligatoria")
        
        # Convertir CURP a mayúsculas y validar
        curp_upper = usuario.curp.upper().strip()
        if len(curp_upper) != 18:
            raise HTTPException(status_code=400, detail="La CURP debe tener exactamente 18 caracteres")
        
        # Validación básica de formato CURP
        import re
        if not re.match(r'^[A-Z0-9]{18}$', curp_upper):
            raise HTTPException(status_code=400, detail="La CURP debe contener solo letras mayúsculas y números")
        
        # Comprobar si el correo ya existe
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (usuario.correo,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        
        # Comprobar si la CURP ya existe
        cursor.execute("SELECT id FROM usuarios WHERE curp = %s", (curp_upper,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="La CURP ya está registrada")
        
        # Hash de la contraseña
        hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
        
        # Insertar usuario con CURP
        cursor.execute(
            "INSERT INTO usuarios (correo, nombre_completo, cargo, supervisor, contrasena, curp) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (usuario.correo, usuario.nombre_completo, usuario.cargo, usuario.supervisor, hashed_password.decode('utf-8'), curp_upper)
        )
        
        user_id = cursor.fetchone()[0]
        conn.commit()
        
        return {"id": user_id, "mensaje": "Usuario creado exitosamente", "curp": curp_upper}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error completo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@app.post("/login")
async def login(usuario: UserLogin):
    # Buscar usuario por correo
    cursor.execute("SELECT id, correo, nombre_completo, cargo, contrasena FROM usuarios WHERE correo = %s", (usuario.correo,))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Verificar contraseña
    if not bcrypt.checkpw(usuario.contrasena.encode('utf-8'), user[4].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
      # Devolver datos del usuario (sin la contraseña)
    return {
        "id": user[0],
        "correo": user[1],
        "nombre_completo": user[2],
        "cargo": user[3]
    }

@app.post("/cambiar_contrasena")
async def cambiar_contrasena(datos: PasswordChange):
    try:
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (datos.usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Validar que la nueva contraseña no esté vacía
        if not datos.nueva_contrasena or len(datos.nueva_contrasena.strip()) < 6:
            raise HTTPException(status_code=400, detail="La nueva contraseña debe tener al menos 6 caracteres")
        
        # Hash de la nueva contraseña
        hashed_password = bcrypt.hashpw(datos.nueva_contrasena.encode('utf-8'), bcrypt.gensalt())
        
        # Actualizar la contraseña en la base de datos
        cursor.execute(
            "UPDATE usuarios SET contrasena = %s WHERE id = %s",
            (hashed_password.decode('utf-8'), datos.usuario_id)
        )
        
        conn.commit()
        
        return {"success": True, "message": "Contraseña actualizada exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al cambiar contraseña: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cambiar contraseña: {str(e)}")

@app.post("/registro")
async def registrar(
    usuario_id: str = Form(...),
    latitud: float = Form(...),
    longitud: float = Form(...),
    descripcion: str = Form(""),
    foto: UploadFile = File(...)
):
    # Guardar la foto en disco
    ext = os.path.splitext(foto.filename)[1]
    nombre_archivo = f"{usuario_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{ext}"
    ruta_archivo = os.path.join(FOTOS_DIR, nombre_archivo)
    with open(ruta_archivo, "wb") as f:
        contenido = await foto.read()
        f.write(contenido)

    # Guardar registro en la base
    fecha_hora = datetime.utcnow()
    cursor.execute(
        "INSERT INTO registros (usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora) VALUES (%s, %s, %s, %s, %s, %s)",
        (usuario_id, latitud, longitud, descripcion, ruta_archivo, fecha_hora)
    )
    conn.commit()

    return {"status": "ok", "foto_url": ruta_archivo}

# ENDPOINT CORREGIDO - Esta es la parte importante que debe actualizarse
@app.get("/registros")
def obtener_registros(usuario_id: int = None):
    try:
        print(f"🔍 Obteniendo registros para usuario: {usuario_id}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Usar cursor directo - NO usar cursor_factory aquí
        if usuario_id:
            cursor.execute(
                "SELECT id, usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora FROM registros WHERE usuario_id = %s ORDER BY fecha_hora DESC LIMIT 50",
                (usuario_id,)
            )
        else:
            cursor.execute(
                "SELECT id, usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora FROM registros ORDER BY fecha_hora DESC LIMIT 50"
            )
        
        resultados = cursor.fetchall()
        print(f"📊 Encontrados {len(resultados)} registros")
        
        # Convertir tuplas a diccionarios manualmente
        registros = []
        for row in resultados:
            registro = {
                "id": row[0],
                "usuario_id": row[1],
                "latitud": float(row[2]) if row[2] else None,
                "longitud": float(row[3]) if row[3] else None,
                "descripcion": row[4],
                "foto_url": row[5],
                "fecha_hora": row[6].isoformat() if row[6] else None
            }
            registros.append(registro)
        
        print(f"✅ Registros procesados correctamente")
        return {"registros": registros}
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener registros: {str(e)}")

# Endpoint de autenticación para administradores
@app.post("/admin/login")
def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        username = form_data.username
        password = form_data.password
        
        # Buscar usuario administrador en la base de datos
        cursor.execute("SELECT password FROM admin_users WHERE username = %s", (username,))
        row = cursor.fetchone()
        
        if not row or not pwd_context.verify(password, row[0]):
            raise HTTPException(status_code=400, detail="Credenciales incorrectas")
        
        # Generar token JWT
        token = jwt.encode({"sub": username, "role": "admin"}, SECRET_KEY, algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}
        
    except Exception as e:
        print(f"❌ Error en admin login: {e}")
        raise HTTPException(status_code=500, detail=f"Error en autenticación: {str(e)}")

# Nuevo endpoint para obtener usuarios (para el panel de administración)
@app.get("/usuarios")
async def obtener_usuarios():
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Obtener todos los usuarios con CURP y contraseña
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp, contrasena FROM usuarios ORDER BY id DESC"
        )
        
        resultados = cursor.fetchall()
        print(f"📊 Encontrados {len(resultados)} usuarios")
        
        # Convertir tuplas a diccionarios manualmente
        usuarios = []
        for row in resultados:
            usuario = {
                "id": row[0],
                "correo": row[1],
                "nombre_completo": row[2],
                "cargo": row[3],
                "supervisor": row[4],
                "curp": row[5],
                "contrasena": row[6]  # Incluir contraseña
            }
            usuarios.append(usuario)
        
        print(f"✅ Usuarios procesados correctamente")
        return {"usuarios": usuarios}
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

# NUEVO ENDPOINT PARA EXPORTACIÓN COMPLETA CON CONTRASEÑAS
@app.get("/usuarios/exportacion-completa")
async def obtener_usuarios_exportacion_completa():
    """
    Endpoint especial para exportar usuarios con contraseñas incluidas.
    Solo para uso en exportación de base de datos completa.
    """
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Obtener TODOS los campos de usuarios incluyendo contraseñas
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, contrasena, curp FROM usuarios ORDER BY id DESC"
        )
        
        resultados = cursor.fetchall()
        print(f"📊 Exportación completa: {len(resultados)} usuarios con contraseñas")
        
        # Convertir tuplas a diccionarios manualmente
        usuarios = []
        for row in resultados:
            usuario = {
                "id": row[0],
                "correo": row[1],
                "nombre_completo": row[2],
                "cargo": row[3],
                "supervisor": row[4],
                "contrasena": row[5],  # INCLUIR LA CONTRASEÑA REAL
                "curp": row[6]
            }
            usuarios.append(usuario)
        
        print(f"✅ Exportación completa procesada correctamente")
        return {"usuarios": usuarios}
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios para exportación: {str(e)}")

# Endpoint para obtener un usuario específico
@app.get("/usuarios/{user_id}")
async def obtener_usuario(user_id: int):
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Obtener usuario específico con contraseña
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp, contrasena FROM usuarios WHERE id = %s",
            (user_id,)
        )
        
        resultado = cursor.fetchone()
        
        if not resultado:
            raise HTTPException(status_code=404, detail=f"Usuario {user_id} no encontrado")
        
        # Convertir tupla a diccionario
        usuario = {
            "id": resultado[0],
            "correo": resultado[1],
            "nombre_completo": resultado[2],
            "cargo": resultado[3],
            "supervisor": resultado[4],
            "curp": resultado[5],
            "contrasena": resultado[6]  # Incluir contraseña
        }
        
        print(f"✅ Usuario {user_id} obtenido correctamente")
        return usuario
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")

@app.put("/usuarios/{user_id}")
async def actualizar_usuario(user_id: int, usuario: UserCreate):
    """Actualiza los datos de un usuario específico"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"✏️ Actualizando usuario {user_id}...")
        
        # Validación de CURP si se proporciona
        if usuario.curp and usuario.curp.strip():
            curp_upper = usuario.curp.upper().strip()
            if len(curp_upper) != 18:
                raise HTTPException(status_code=400, detail="La CURP debe tener exactamente 18 caracteres")
            
            import re
            if not re.match(r'^[A-Z0-9]{18}$', curp_upper):
                raise HTTPException(status_code=400, detail="La CURP tiene un formato inválido")
            
            # Verificar que la CURP no esté en uso por otro usuario
            cursor.execute("SELECT id FROM usuarios WHERE curp = %s AND id != %s", (curp_upper, user_id))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Esta CURP ya está registrada por otro usuario")
        else:
            curp_upper = None
        
        # Verificar que el correo no esté en uso por otro usuario
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s AND id != %s", (usuario.correo, user_id))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Este correo ya está registrado por otro usuario")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Actualizar usuario (contraseña sin encriptar)
        cursor.execute(
            """UPDATE usuarios SET 
               correo = %s, 
               nombre_completo = %s, 
               cargo = %s, 
               supervisor = %s, 
               contrasena = %s, 
               curp = %s 
               WHERE id = %s""",
            (usuario.correo, usuario.nombre_completo, usuario.cargo, 
             usuario.supervisor, usuario.contrasena, curp_upper, user_id)
        )
        
        conn.commit()
        
        # Obtener el usuario actualizado
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp, contrasena FROM usuarios WHERE id = %s",
            (user_id,)
        )
        resultado = cursor.fetchone()
        
        usuario_actualizado = {
            "id": resultado[0],
            "correo": resultado[1],
            "nombre_completo": resultado[2],
            "cargo": resultado[3],
            "supervisor": resultado[4],
            "curp": resultado[5],
            "contrasena": resultado[6]
        }
        
        print(f"✅ Usuario {user_id} actualizado exitosamente")
        return {
            "success": True,
            "message": "Usuario actualizado exitosamente",
            "usuario": usuario_actualizado
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")

@app.delete("/usuarios/{user_id}")
async def eliminar_usuario(user_id: int):
    """Elimina completamente un usuario y todos sus datos asociados"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🗑️ Iniciando eliminación completa del usuario {user_id}...")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, correo, nombre_completo FROM usuarios WHERE id = %s", (user_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail=f"Usuario {user_id} no encontrado")
        
        usuario_info = {
            "id": usuario[0],
            "correo": usuario[1], 
            "nombre_completo": usuario[2]
        }
        
        print(f"👤 Usuario encontrado: {usuario_info}")
        
        # Contadores para el reporte
        registros_eliminados = 0
        asistencias_eliminadas = 0
        fotos_eliminadas = 0
        
        # 1. Obtener y eliminar fotos asociadas a registros del usuario
        try:
            cursor.execute("SELECT foto_url FROM registros WHERE usuario_id = %s AND foto_url IS NOT NULL", (user_id,))
            fotos_registros = cursor.fetchall()
            
            for foto_row in fotos_registros:
                foto_path = foto_row[0]
                if foto_path and os.path.exists(foto_path):
                    try:
                        os.remove(foto_path)
                        fotos_eliminadas += 1
                        print(f"📸 Foto eliminada: {foto_path}")
                    except Exception as e:
                        print(f"⚠️ Error eliminando foto {foto_path}: {e}")
                        
        except Exception as e:
            print(f"⚠️ Error obteniendo fotos de registros: {e}")
        
        # 2. Eliminar registros del usuario
        try:
            cursor.execute("DELETE FROM registros WHERE usuario_id = %s", (user_id,))
            registros_eliminados = cursor.rowcount
            print(f"📋 {registros_eliminados} registros eliminados")
        except Exception as e:
            print(f"⚠️ Error eliminando registros: {e}")
        
        # 3. Eliminar asistencias del usuario
        try:
            cursor.execute("DELETE FROM asistencias WHERE usuario_id = %s", (user_id,))
            asistencias_eliminadas = cursor.rowcount
            print(f"⏰ {asistencias_eliminadas} asistencias eliminadas")
        except Exception as e:
            print(f"⚠️ Error eliminando asistencias: {e}")
        
        # 4. Finalmente eliminar el usuario
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        
        conn.commit()
        
        reporte = {
            "success": True,
            "message": f"Usuario {user_id} eliminado completamente",
            "usuario_eliminado": usuario_info,
            "estadisticas": {
                "registros_eliminados": registros_eliminados,
                "asistencias_eliminadas": asistencias_eliminadas,
                "fotos_eliminadas": fotos_eliminadas
            }
        }
        
        print(f"✅ Usuario {user_id} eliminado exitosamente")
        print(f"📊 Estadísticas: {reporte['estadisticas']}")
        
        return reporte
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")

# Modelos para historial
class HistorialCreate(BaseModel):
    usuario_id: int
    tipo: str
    descripcion: str
    fecha: str = None
    hora: str = None
    detalles: str = None

# ENDPOINTS DE HISTORIAL
@app.post("/historial")
async def crear_historial(historial: HistorialCreate):
    """Crear un nuevo registro en el historial"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (historial.usuario_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Usar fecha y hora actuales si no se proporcionan
        fecha_actual = historial.fecha or datetime.now().date()
        hora_actual = historial.hora or datetime.now().time()
        
        cursor.execute("""
            INSERT INTO historial (usuario_id, tipo, descripcion, fecha, hora, detalles)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            historial.usuario_id,
            historial.tipo,
            historial.descripcion,
            fecha_actual,
            hora_actual,
            historial.detalles
        ))
        
        historial_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ Historial creado con ID: {historial_id}")
        return {"id": historial_id, "message": "Historial creado exitosamente"}
        
    except Exception as e:
        print(f"❌ Error creando historial: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error creando historial: {str(e)}")

@app.get("/historial/{usuario_id}")
async def obtener_historial_usuario(
    usuario_id: int,
    fecha_inicio: str = None,
    fecha_fin: str = None,
    tipo: str = None,
    limit: int = 100
):
    """Obtener historial de un usuario con filtros opcionales"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, nombre_completo FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Construir consulta con filtros
        query = """
            SELECT h.id, h.usuario_id, h.tipo, h.descripcion, h.fecha, h.hora, h.detalles, h.creado_en,
                   u.nombre_completo, u.correo
            FROM historial h
            JOIN usuarios u ON h.usuario_id = u.id
            WHERE h.usuario_id = %s
        """
        params = [usuario_id]
        
        if fecha_inicio:
            query += " AND h.fecha >= %s"
            params.append(fecha_inicio)
        
        if fecha_fin:
            query += " AND h.fecha <= %s"
            params.append(fecha_fin)
        
        if tipo:
            query += " AND h.tipo = %s"
            params.append(tipo)
        
        query += " ORDER BY h.fecha DESC, h.hora DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        historial = []
        for row in resultados:
            registro = {
                "id": row[0],
                "usuario_id": row[1],
                "tipo": row[2],
                "descripcion": row[3],
                "fecha": row[4].isoformat() if row[4] else None,
                "hora": str(row[5]) if row[5] else None,
                "detalles": row[6],
                "creado_en": row[7].isoformat() if row[7] else None,
                "usuario_nombre": row[8],
                "usuario_correo": row[9]
            }
            historial.append(registro)
        
        return {
            "historial": historial,
            "total": len(historial),
            "usuario": {
                "id": usuario[0],
                "nombre": usuario[1]
            }
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo historial: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo historial: {str(e)}")

@app.get("/historial")
async def obtener_todos_historiales():
    """Obtener todos los historiales para propósitos de depuración"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        cursor.execute("""
            SELECT h.id, h.usuario_id, h.tipo, h.descripcion, h.fecha, h.hora, h.detalles, h.creado_en,
                   u.nombre_completo, u.correo
            FROM historial h
            JOIN usuarios u ON h.usuario_id = u.id
            ORDER BY h.fecha DESC, h.hora DESC 
            LIMIT 50
        """)
        resultados = cursor.fetchall()
        
        historial = []
        for row in resultados:
            registro = {
                "id": row[0],
                "usuario_id": row[1],
                "tipo": row[2],
                "descripcion": row[3],
                "fecha": row[4].isoformat() if row[4] else None,
                "hora": str(row[5]) if row[5] else None,
                "detalles": row[6],
                "creado_en": row[7].isoformat() if row[7] else None,
                "usuario_nombre": row[8],
                "usuario_correo": row[9]
            }
            historial.append(registro)
        
        return {
            "historial": historial,
            "total": len(historial)
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo todos los historiales: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo historiales: {str(e)}")

@app.get("/historial/resumen/{usuario_id}")
async def obtener_resumen_historial(usuario_id: int):
    """Obtener resumen del historial de un usuario (estadísticas)"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT nombre_completo FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Obtener estadísticas
        cursor.execute("""
            SELECT 
                COUNT(*) as total_registros,
                COUNT(CASE WHEN tipo = 'entrada' THEN 1 END) as entradas,
                COUNT(CASE WHEN tipo = 'salida' THEN 1 END) as salidas,
                COUNT(CASE WHEN tipo = 'actividad' THEN 1 END) as actividades,
                MIN(fecha) as primera_fecha,
                MAX(fecha) as ultima_fecha
            FROM historial 
            WHERE usuario_id = %s
        """, (usuario_id,))
        
        stats = cursor.fetchone()
        
        # Obtener actividad por mes (últimos 12 meses)
        cursor.execute("""
            SELECT 
                DATE_TRUNC('month', fecha) as mes,
                COUNT(*) as cantidad
            FROM historial 
            WHERE usuario_id = %s 
            AND fecha >= CURRENT_DATE - INTERVAL '12 months'
            GROUP BY DATE_TRUNC('month', fecha)
            ORDER BY mes DESC
        """, (usuario_id,))
        
        actividad_mensual = cursor.fetchall()
        
        return {
            "usuario_nombre": usuario[0],
            "estadisticas": {
                "total_registros": stats[0] or 0,
                "entradas": stats[1] or 0,
                "salidas": stats[2] or 0,
                "actividades": stats[3] or 0,
                "primera_fecha": stats[4].isoformat() if stats[4] else None,
                "ultima_fecha": stats[5].isoformat() if stats[5] else None
            },
            "actividad_mensual": [
                {
                    "mes": row[0].isoformat() if row[0] else None,
                    "cantidad": row[1]
                }
                for row in actividad_mensual
            ]
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo resumen: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo resumen: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
