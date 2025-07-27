from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
import bcrypt
import re
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext
import pytz
import uvicorn

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
        
        # Insertar usuario con CURP (contraseña sin encriptar)
        cursor.execute(
            "INSERT INTO usuarios (correo, nombre_completo, cargo, supervisor, contrasena, curp) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (usuario.correo, usuario.nombre_completo, usuario.cargo, usuario.supervisor, usuario.contrasena, curp_upper)
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
    
    # Verificar contraseña (comparación directa sin encriptación)
    if usuario.contrasena != user[4]:
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
    foto: UploadFile = File(...),
    timestamp_offline: str = Form(None)  # Nuevo campo opcional para registro offline
):
    print(f"🔍 REGISTRO - Datos recibidos:")
    print(f"   usuario_id: {usuario_id}")
    print(f"   latitud: {latitud}")
    print(f"   longitud: {longitud}")
    print(f"   descripcion: {descripcion}")
    print(f"   foto: {foto.filename}")
    print(f"   timestamp_offline: {timestamp_offline}")
    
    # Usar timestamp personalizado si viene de offline, sino usar tiempo actual
    if timestamp_offline:
        try:
            # Convertir string ISO a datetime
            fecha_hora = datetime.fromisoformat(timestamp_offline.replace('Z', '+00:00'))
            print(f"📅 ✅ Usando timestamp offline: {fecha_hora}")
            # Usar el timestamp offline también para el nombre del archivo
            timestamp_for_filename = fecha_hora.strftime('%Y%m%d%H%M%S')
        except Exception as e:
            print(f"⚠️ Error parseando timestamp offline: {e}, usando tiempo actual")
            fecha_hora = datetime.utcnow()
            timestamp_for_filename = fecha_hora.strftime('%Y%m%d%H%M%S')
    else:
        fecha_hora = datetime.utcnow()
        timestamp_for_filename = fecha_hora.strftime('%Y%m%d%H%M%S')
        print(f"📅 ⏰ Usando timestamp actual: {fecha_hora}")

    # Guardar la foto en disco usando el timestamp correcto
    ext = os.path.splitext(foto.filename)[1]
    nombre_archivo = f"{usuario_id}_{timestamp_for_filename}{ext}"
    ruta_archivo = os.path.join(FOTOS_DIR, nombre_archivo)
    print(f"📁 Guardando foto como: {nombre_archivo}")
    
    with open(ruta_archivo, "wb") as f:
        contenido = await foto.read()
        f.write(contenido)

    # Guardar registro en la base
    cursor.execute(
        "INSERT INTO registros (usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora) VALUES (%s, %s, %s, %s, %s, %s)",
        (usuario_id, latitud, longitud, descripcion, ruta_archivo, fecha_hora)
    )
    conn.commit()
    print(f"✅ Registro guardado en BD con fecha_hora: {fecha_hora}")

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

# Nuevo endpoint para obtener usuarios (para el panel de administración)
@app.get("/usuarios")
async def obtener_usuarios():
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Obtener todos los usuarios con CURP
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp FROM usuarios ORDER BY id DESC"
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
                "curp": row[5]
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

# Endpoint para obtener un usuario específico por ID
@app.get("/usuarios/{user_id}")
async def obtener_usuario(user_id: int):
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Buscar usuario por ID con CURP
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp FROM usuarios WHERE id = %s",
            (user_id,)
        )
        
        resultado = cursor.fetchone()        
        if not resultado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        usuario = {
            "id": resultado[0],
            "correo": resultado[1],
            "nombre_completo": resultado[2],
            "cargo": resultado[3],
            "supervisor": resultado[4],
            "curp": resultado[5]
        }
        
        print(f"✅ Usuario {user_id} encontrado correctamente")
        return usuario
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")

# Endpoint para eliminar un usuario específico con todos sus datos
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
        
        # 2. Obtener y eliminar fotos asociadas a asistencias del usuario
        try:
            cursor.execute(
                "SELECT foto_entrada_url, foto_salida_url FROM asistencias WHERE usuario_id = %s", 
                (user_id,)
            )
            fotos_asistencias = cursor.fetchall()
            
            for foto_row in fotos_asistencias:
                # Foto de entrada
                if foto_row[0] and os.path.exists(foto_row[0]):
                    try:
                        os.remove(foto_row[0])
                        fotos_eliminadas += 1
                        print(f"📸 Foto de entrada eliminada: {foto_row[0]}")
                    except Exception as e:
                        print(f"⚠️ Error eliminando foto de entrada {foto_row[0]}: {e}")
                
                # Foto de salida
                if foto_row[1] and os.path.exists(foto_row[1]):
                    try:
                        os.remove(foto_row[1])
                        fotos_eliminadas += 1
                        print(f"📸 Foto de salida eliminada: {foto_row[1]}")
                    except Exception as e:
                        print(f"⚠️ Error eliminando foto de salida {foto_row[1]}: {e}")
                        
        except Exception as e:
            print(f"⚠️ Error obteniendo fotos de asistencias: {e}")
        
        # 3. Eliminar registros del usuario
        try:
            cursor.execute("SELECT COUNT(*) FROM registros WHERE usuario_id = %s", (user_id,))
            registros_eliminados = cursor.fetchone()[0]
            
            cursor.execute("DELETE FROM registros WHERE usuario_id = %s", (user_id,))
            print(f"📋 {registros_eliminados} registros eliminados")
            
        except Exception as e:
            print(f"❌ Error eliminando registros: {e}")
            raise HTTPException(status_code=500, detail=f"Error eliminando registros: {str(e)}")
        
        # 4. Eliminar asistencias del usuario
        try:
            cursor.execute("SELECT COUNT(*) FROM asistencias WHERE usuario_id = %s", (user_id,))
            asistencias_eliminadas = cursor.fetchone()[0]
            
            cursor.execute("DELETE FROM asistencias WHERE usuario_id = %s", (user_id,))
            print(f"⏰ {asistencias_eliminadas} asistencias eliminadas")
            
        except Exception as e:
            print(f"❌ Error eliminando asistencias: {e}")
            raise HTTPException(status_code=500, detail=f"Error eliminando asistencias: {str(e)}")
        
        # 5. Finalmente, eliminar el usuario
        try:
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            print(f"👤 Usuario {user_id} eliminado")
            
        except Exception as e:
            print(f"❌ Error eliminando usuario: {e}")
            raise HTTPException(status_code=500, detail=f"Error eliminando usuario: {str(e)}")
        
        # Confirmar todos los cambios
        conn.commit()
        
        # Resumen de eliminación
        resultado = {
            "status": "success",
            "message": f"Usuario {user_id} eliminado completamente",
            "usuario_eliminado": usuario_info,
            "datos_eliminados": {
                "registros": registros_eliminados,
                "asistencias": asistencias_eliminadas,
                "fotos": fotos_eliminadas
            }
        }
        
        print(f"✅ ELIMINACIÓN COMPLETA EXITOSA:")
        print(f"   👤 Usuario: {usuario_info['correo']}")
        print(f"   📋 Registros: {registros_eliminados}")
        print(f"   ⏰ Asistencias: {asistencias_eliminadas}")
        print(f"   📸 Fotos: {fotos_eliminadas}")
        
        return resultado
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL al eliminar usuario {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general al eliminar usuario {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")

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

# Define el timezone de CDMX
CDMX_TZ = pytz.timezone("America/Mexico_City")

@app.post("/asistencia/entrada")
async def marcar_entrada(
    usuario_id: int = Form(...),
    latitud: float = Form(...),
    longitud: float = Form(...),
    descripcion: str = Form(""),
    foto: UploadFile = File(...),
    timestamp_offline: str = Form(None),  # Timestamp de registro offline
    timestamp_registro: str = Form(None),  # Timestamp de registro online
    fecha_original: str = Form(None)  # Fecha original del registro
):
    try:
        print(f"🔍 ENTRADA - Datos recibidos:")
        print(f"   usuario_id: {usuario_id} (tipo: {type(usuario_id)})")
        print(f"   latitud: {latitud}")
        print(f"   longitud: {longitud}")
        print(f"   descripcion: {descripcion}")
        print(f"   foto: {foto.filename}")
        print(f"   timestamp_offline: {timestamp_offline}")
        print(f"   timestamp_registro: {timestamp_registro}")
        print(f"   fecha_original: {fecha_original}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Función para parsear timestamp ISO
        def parse_iso_timestamp(timestamp_str):
            try:
                if timestamp_str:
                    # Convertir string ISO a datetime y ajustar a zona horaria de CDMX
                    if timestamp_str.endswith('Z'):
                        fecha_hora_utc = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    else:
                        fecha_hora_utc = datetime.fromisoformat(timestamp_str)
                    return fecha_hora_utc.astimezone(CDMX_TZ)
                return None
            except Exception as e:
                print(f"⚠️ Error parseando timestamp {timestamp_str}: {e}")
                return None
        
        # Determinar el timestamp correcto a usar (prioridad: offline > registro > actual)
        hora_entrada = None
        timestamp_origen = "servidor"
        
        if timestamp_offline:
            # Registro offline - usar hora original de cuando se registró sin conexión
            hora_entrada = parse_iso_timestamp(timestamp_offline)
            timestamp_origen = "offline"
            print(f"📅 Usando timestamp OFFLINE: {hora_entrada}")
        elif timestamp_registro:
            # Registro online - usar hora específica del dispositivo
            hora_entrada = parse_iso_timestamp(timestamp_registro)
            timestamp_origen = "registro"
            print(f"📅 Usando timestamp REGISTRO: {hora_entrada}")
        
        # Fallback - usar tiempo actual del servidor
        if not hora_entrada:
            hora_entrada = datetime.now(CDMX_TZ)
            timestamp_origen = "servidor"
            print(f"📅 Usando timestamp SERVIDOR: {hora_entrada}")
        
        fecha = hora_entrada.date()
        timestamp_for_filename = hora_entrada.strftime('%Y%m%d%H%M%S')
        
        print(f"✅ Timestamp final para entrada: {hora_entrada} (origen: {timestamp_origen})")

        # Revisa si ya existe asistencia para hoy para este usuario específico
        cursor.execute(
            "SELECT id FROM asistencias WHERE usuario_id = %s AND fecha = %s",
            (usuario_id, fecha)
        )
        existe = cursor.fetchone()

        print(f"🔍 Verificando entrada para usuario {usuario_id} en fecha {fecha}")
        print(f"📊 Resultado de consulta: {existe}")

        if existe:
            raise HTTPException(
                status_code=400, 
                detail=f"El usuario {usuario_id} ya tiene registro de entrada para el día {fecha}"
            )

        # Guardar la foto en disco usando el timestamp correcto
        ext = os.path.splitext(foto.filename)[1]
        nombre_archivo = f"entrada_{usuario_id}_{timestamp_for_filename}{ext}"
        ruta_archivo = os.path.join(FOTOS_DIR, nombre_archivo)
        
        with open(ruta_archivo, "wb") as f:
            contenido = await foto.read()
            f.write(contenido)

        # Insertar registro de asistencia con ubicación y foto
        cursor.execute(
            "INSERT INTO asistencias (usuario_id, fecha, hora_entrada, latitud_entrada, longitud_entrada, foto_entrada_url, descripcion_entrada) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (usuario_id, fecha, hora_entrada, latitud, longitud, ruta_archivo, descripcion)
        )
        conn.commit()
        print(f"✅ Entrada registrada para usuario {usuario_id} a las {hora_entrada}")
        
        return {
            "status": "ok", 
            "mensaje": "Entrada registrada exitosamente", 
            "hora_entrada": str(hora_entrada),
            "latitud": latitud,
            "longitud": longitud,
            "foto_url": ruta_archivo,
            "descripcion": descripcion
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL en entrada: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general en entrada: {e}")
        raise HTTPException(status_code=500, detail=f"Error al registrar entrada: {str(e)}")

@app.post("/asistencia/salida")
async def marcar_salida(
    usuario_id: int = Form(...),
    latitud: float = Form(...),
    longitud: float = Form(...),
    descripcion: str = Form(""),
    foto: UploadFile = File(...),
    timestamp_offline: str = Form(None),  # Timestamp de registro offline
    timestamp_registro: str = Form(None),  # Timestamp de registro online
    fecha_original: str = Form(None)  # Fecha original del registro
):
    try:
        print(f"🔍 SALIDA - Datos recibidos:")
        print(f"   usuario_id: {usuario_id} (tipo: {type(usuario_id)})")
        print(f"   latitud: {latitud}")
        print(f"   longitud: {longitud}")
        print(f"   descripcion: {descripcion}")
        print(f"   foto: {foto.filename}")
        print(f"   timestamp_offline: {timestamp_offline}")
        print(f"   timestamp_registro: {timestamp_registro}")
        print(f"   fecha_original: {fecha_original}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Función para parsear timestamp ISO (reutilizada del endpoint de entrada)
        def parse_iso_timestamp(timestamp_str):
            try:
                if timestamp_str:
                    # Convertir string ISO a datetime y ajustar a zona horaria de CDMX
                    if timestamp_str.endswith('Z'):
                        fecha_hora_utc = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    else:
                        fecha_hora_utc = datetime.fromisoformat(timestamp_str)
                    return fecha_hora_utc.astimezone(CDMX_TZ)
                return None
            except Exception as e:
                print(f"⚠️ Error parseando timestamp {timestamp_str}: {e}")
                return None
        
        # Determinar el timestamp correcto a usar (prioridad: offline > registro > actual)
        hora_salida = None
        timestamp_origen = "servidor"
        
        if timestamp_offline:
            # Registro offline - usar hora original de cuando se registró sin conexión
            hora_salida = parse_iso_timestamp(timestamp_offline)
            timestamp_origen = "offline"
            print(f"📅 Usando timestamp OFFLINE para salida: {hora_salida}")
        elif timestamp_registro:
            # Registro online - usar hora específica del dispositivo
            hora_salida = parse_iso_timestamp(timestamp_registro)
            timestamp_origen = "registro"
            print(f"📅 Usando timestamp REGISTRO para salida: {hora_salida}")
        
        # Fallback - usar tiempo actual del servidor
        if not hora_salida:
            hora_salida = datetime.now(CDMX_TZ)
            timestamp_origen = "servidor"
            print(f"📅 Usando timestamp SERVIDOR para salida: {hora_salida}")
        
        fecha = hora_salida.date()
        timestamp_for_filename = hora_salida.strftime('%Y%m%d%H%M%S')
        
        print(f"✅ Timestamp final para salida: {hora_salida} (origen: {timestamp_origen})")

        # Busca el registro de asistencia de hoy para este usuario específico
        cursor.execute(
            "SELECT id, hora_salida FROM asistencias WHERE usuario_id = %s AND fecha = %s",
            (usuario_id, fecha)
        )
        registro = cursor.fetchone()

        print(f"🔍 Verificando salida para usuario {usuario_id} en fecha {fecha}")
        print(f"📊 Resultado de consulta: {registro}")

        if not registro:
            raise HTTPException(
                status_code=400, 
                detail=f"El usuario {usuario_id} no tiene registro de entrada para el día {fecha}"
            )
        if registro[1] is not None:
            raise HTTPException(
                status_code=400, 
                detail=f"El usuario {usuario_id} ya registró la salida para el día {fecha}"
            )

        # Guardar la foto en disco usando el timestamp correcto
        ext = os.path.splitext(foto.filename)[1]
        nombre_archivo = f"salida_{usuario_id}_{timestamp_for_filename}{ext}"
        ruta_archivo = os.path.join(FOTOS_DIR, nombre_archivo)
        
        with open(ruta_archivo, "wb") as f:
            contenido = await foto.read()
            f.write(contenido)

        # Actualizar registro con salida, ubicación y foto
        cursor.execute(
            "UPDATE asistencias SET hora_salida = %s, latitud_salida = %s, longitud_salida = %s, foto_salida_url = %s, descripcion_salida = %s WHERE usuario_id = %s AND fecha = %s",
            (hora_salida, latitud, longitud, ruta_archivo, descripcion, usuario_id, fecha)
        )
        conn.commit()
        print(f"✅ Salida registrada para usuario {usuario_id} a las {hora_salida}")
        
        return {
            "status": "ok", 
            "mensaje": "Salida registrada exitosamente", 
            "hora_salida": str(hora_salida),
            "latitud": latitud,
            "longitud": longitud,
            "foto_url": ruta_archivo,
            "descripcion": descripcion
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL en salida: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general en salida: {e}")
        raise HTTPException(status_code=500, detail=f"Error al registrar salida: {str(e)}")

@app.get("/asistencias")
async def obtener_historial_asistencias(usuario_id: int = None):
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🔍 Obteniendo historial de asistencias para usuario: {usuario_id}")
        
        if usuario_id:
            cursor.execute(
                """SELECT id, usuario_id, fecha, hora_entrada, hora_salida, 
                          latitud_entrada, longitud_entrada, latitud_salida, longitud_salida,
                          foto_entrada_url, foto_salida_url, descripcion_entrada, descripcion_salida
                   FROM asistencias 
                   WHERE usuario_id = %s 
                   ORDER BY fecha DESC, hora_entrada DESC 
                   LIMIT 50""",
                (usuario_id,)
            )
        else:
            cursor.execute(
                """SELECT id, usuario_id, fecha, hora_entrada, hora_salida, 
                          latitud_entrada, longitud_entrada, latitud_salida, longitud_salida,
                          foto_entrada_url, foto_salida_url, descripcion_entrada, descripcion_salida
                   FROM asistencias 
                   ORDER BY fecha DESC, hora_entrada DESC 
                   LIMIT 50"""
            )
        
        resultados = cursor.fetchall()
        print(f"📊 Encontradas {len(resultados)} asistencias")
        
        # Convertir tuplas a diccionarios manualmente
        asistencias = []
        for row in resultados:
            asistencia = {
                "id": row[0],
                "usuario_id": row[1],
                "fecha": row[2].isoformat() if row[2] else None,
                "hora_entrada": row[3].isoformat() if row[3] else None,
                "hora_salida": row[4].isoformat() if row[4] else None,
                "latitud_entrada": float(row[5]) if row[5] else None,
                "longitud_entrada": float(row[6]) if row[6] else None,
                "latitud_salida": float(row[7]) if row[7] else None,
                "longitud_salida": float(row[8]) if row[8] else None,
                "foto_entrada_url": row[9],
                "foto_salida_url": row[10],
                "descripcion_entrada": row[11],
                "descripcion_salida": row[12]
            }
            asistencias.append(asistencia)
        
        print(f"✅ Historial de asistencias procesado correctamente")
        return {"asistencias": asistencias}
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(e)}")

# Endpoint temporal para verificar la estructura de la tabla asistencias
@app.get("/debug/asistencias-estructura")
async def verificar_estructura_asistencias():
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Verificar si la tabla existe
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'asistencias'
        """)
        tabla_existe = cursor.fetchone()
        
        if not tabla_existe:
            return {"error": "La tabla 'asistencias' no existe"}
        
        # Obtener la estructura de la tabla
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'asistencias' 
            ORDER BY ordinal_position
        """)
        columnas = cursor.fetchall()
        
        # Obtener algunos registros de ejemplo
        cursor.execute("SELECT * FROM asistencias LIMIT 3")
        registros_ejemplo = cursor.fetchall()
        
        return {
            "tabla_existe": True,
            "columnas": [{"nombre": col[0], "tipo": col[1], "nullable": col[2]} for col in columnas],
            "total_registros": len(registros_ejemplo),
            "registros_ejemplo": registros_ejemplo
        }
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        raise HTTPException(status_code=500, detail=f"Error verificando estructura: {str(e)}")

# Endpoints para eliminación masiva (ADMIN ONLY)
@app.delete("/admin/usuarios/all")
async def eliminar_todos_usuarios():
    """Elimina TODOS los usuarios de la base de datos. ¡USO EXTREMO!"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Contar usuarios antes de eliminar
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        if total_usuarios == 0:
            return {
                "status": "info",
                "message": "No hay usuarios para eliminar",
                "usuarios_eliminados": 0
            }
        
        # Eliminar todos los usuarios
        cursor.execute("DELETE FROM usuarios")
        conn.commit()
        
        print(f"🗑️ ELIMINACIÓN MASIVA: {total_usuarios} usuarios eliminados")
        
        return {
            "status": "success",
            "message": f"Todos los usuarios han sido eliminados exitosamente",
            "usuarios_eliminados": total_usuarios
        }
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL al eliminar usuarios: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general al eliminar usuarios: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuarios: {str(e)}")

@app.delete("/admin/registros/all")
async def eliminar_todos_registros():
    """Elimina TODOS los registros de la base de datos. ¡USO EXTREMO!"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Contar registros antes de eliminar
        cursor.execute("SELECT COUNT(*) FROM registros")
        total_registros = cursor.fetchone()[0]
        
        if total_registros == 0:
            return {
                "status": "info",
                "message": "No hay registros para eliminar",
                "registros_eliminados": 0
            }
        
        # Eliminar todos los registros
        cursor.execute("DELETE FROM registros")
        conn.commit()
        
        print(f"🗑️ ELIMINACIÓN MASIVA: {total_registros} registros eliminados")
        
        return {
            "status": "success",
            "message": f"Todos los registros han sido eliminados exitosamente",
            "registros_eliminados": total_registros
        }
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL al eliminar registros: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general al eliminar registros: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar registros: {str(e)}")

@app.delete("/admin/asistencias/all")
async def eliminar_todas_asistencias():
    """Elimina TODAS las asistencias de la base de datos. ¡USO EXTREMO!"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print("🚀 Iniciando eliminación masiva de asistencias...")
        
        # Contar asistencias antes de eliminar (RÁPIDO)
        cursor.execute("SELECT COUNT(*) FROM asistencias")
        total_asistencias = cursor.fetchone()[0]
        
        if total_asistencias == 0:
            return {
                "status": "info",
                "message": "No hay asistencias para eliminar",
                "asistencias_eliminadas": 0
            }
        
        print(f"📊 Eliminando {total_asistencias} asistencias...")
        
        # OPTIMIZACIÓN: Eliminar primero las asistencias (RÁPIDO)
        cursor.execute("DELETE FROM asistencias")
        conn.commit()
        
        print(f"🗑️ ELIMINACIÓN MASIVA COMPLETADA: {total_asistencias} asistencias eliminadas")
        
        # OPTIMIZACIÓN: Eliminar fotos en segundo plano (no bloquear la respuesta)
        try:
            # Obtener lista de archivos en el directorio fotos para eliminar en lote
            fotos_dir = os.path.join(os.getcwd(), "fotos")
            fotos_eliminadas = 0
            
            if os.path.exists(fotos_dir):
                archivos = os.listdir(fotos_dir)
                for archivo in archivos:
                    if archivo.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        try:
                            os.remove(os.path.join(fotos_dir, archivo))
                            fotos_eliminadas += 1
                        except:
                            pass  # Ignorar errores de archivos individuales
                            
                print(f"📸 {fotos_eliminadas} fotos eliminadas del directorio")
        except Exception as e:
            print(f"⚠️ Error al limpiar fotos (no crítico): {e}")
            fotos_eliminadas = 0
        
        return {
            "status": "success",
            "message": f"Todas las asistencias han sido eliminadas exitosamente",
            "asistencias_eliminadas": total_asistencias,
            "fotos_eliminadas": fotos_eliminadas
        }
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL al eliminar asistencias: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general al eliminar asistencias: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar asistencias: {str(e)}")

# Endpoint para verificar estructura de tabla usuarios y CURP
@app.get("/debug/usuarios-estructura")
async def verificar_estructura_usuarios():
    """Endpoint para verificar que la tabla usuarios tenga la columna CURP"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Verificar si la tabla existe
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'usuarios'
        """)
        tabla_existe = cursor.fetchone()
        
        if not tabla_existe:
            return {"error": "La tabla 'usuarios' no existe"}
        
        # Obtener la estructura de la tabla
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            ORDER BY ordinal_position
        """)
        columnas = cursor.fetchall()
        
        # Verificar específicamente si existe la columna CURP
        cursor.execute("""
            SELECT 1 
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            AND column_name = 'curp'
        """)
        curp_existe = cursor.fetchone() is not None
        
        # Obtener algunos registros de ejemplo (sin contraseñas)
        cursor.execute("SELECT id, correo, nombre_completo, curp FROM usuarios LIMIT 3")
        registros_ejemplo = cursor.fetchall()
        
        return {
            "tabla_existe": True,
            "curp_columna_existe": curp_existe,
            "columnas": [{"nombre": col[0], "tipo": col[1], "nullable": col[2], "default": col[3]} for col in columnas],
            "total_registros": len(registros_ejemplo),
            "registros_ejemplo": registros_ejemplo
        }
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        raise HTTPException(status_code=500, detail=f"Error verificando estructura: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
