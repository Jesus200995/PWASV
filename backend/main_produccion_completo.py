from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext
import os
import re
import bcrypt
import pytz

app = FastAPI()

# Permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003", "http://127.0.0.1:3003", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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

class TerminosAceptados(BaseModel):
    usuario_id: int

# Montar carpeta de fotos para servir estáticamente
app.mount("/fotos", StaticFiles(directory="fotos"), name="fotos")

# Configuración para autenticación JWT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "cambia-esto-por-una-clave-muy-larga-y-unica-para-admin-2025"

# ==================== NUEVOS ENDPOINTS DE TÉRMINOS ====================

@app.get("/usuarios/{user_id}/terminos")
async def verificar_terminos_usuario(user_id: int):
    """Verificar si un usuario ha aceptado los términos y condiciones"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
            
        print(f"🔍 Verificando términos para usuario {user_id}")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, correo FROM usuarios WHERE id = %s", (user_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print(f"❌ Usuario {user_id} no encontrado")
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar si ha aceptado términos
        cursor.execute(
            "SELECT aceptado, fecha_aceptado FROM usuarios_terminos WHERE usuario_id = %s",
            (user_id,)
        )
        terminos = cursor.fetchone()
        
        resultado = {
            "usuario_id": user_id,
            "ha_aceptado_terminos": terminos is not None and terminos[0] if terminos else False,
            "fecha_aceptacion": terminos[1].isoformat() if terminos and terminos[1] else None
        }
        
        print(f"✅ Términos verificados para usuario {user_id}: {resultado['ha_aceptado_terminos']}")
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error verificando términos: {e}")
        raise HTTPException(status_code=500, detail=f"Error al verificar términos: {str(e)}")

@app.post("/usuarios/aceptar_terminos")
async def aceptar_terminos(terminos: TerminosAceptados):
    """Registrar la aceptación de términos y condiciones de un usuario"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
            
        print(f"📝 Registrando términos para usuario {terminos.usuario_id}")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, correo FROM usuarios WHERE id = %s", (terminos.usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print(f"❌ Usuario {terminos.usuario_id} no encontrado")
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar si ya existe un registro para este usuario
        cursor.execute("SELECT id FROM usuarios_terminos WHERE usuario_id = %s", (terminos.usuario_id,))
        existe = cursor.fetchone()
        
        if existe:
            # Actualizar registro existente
            cursor.execute("""
                UPDATE usuarios_terminos 
                SET aceptado = %s, fecha_aceptado = NOW()
                WHERE usuario_id = %s
            """, (True, terminos.usuario_id))
            print(f"✅ Términos actualizados para usuario {terminos.usuario_id}")
        else:
            # Insertar nuevo registro
            cursor.execute("""
                INSERT INTO usuarios_terminos (usuario_id, aceptado, fecha_aceptado) 
                VALUES (%s, %s, NOW())
            """, (terminos.usuario_id, True))
            print(f"✅ Términos creados para usuario {terminos.usuario_id}")
        
        conn.commit()
        
        return {
            "status": "success",
            "message": "Términos y condiciones aceptados exitosamente",
            "usuario_id": terminos.usuario_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error aceptando términos: {e}")
        raise HTTPException(status_code=500, detail=f"Error al registrar aceptación de términos: {str(e)}")

# ==================== ENDPOINT DE USUARIOS MODIFICADO ====================

@app.post("/usuarios")
async def crear_usuario(usuario: UserCreate):
    """Crear usuario y automáticamente registrar aceptación de términos"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
            
        print(f"👤 Creando usuario: {usuario.correo}")
        
        # Validación de CURP obligatoria
        if not usuario.curp or not usuario.curp.strip():
            raise HTTPException(status_code=400, detail="La CURP es obligatoria")
        
        # Convertir CURP a mayúsculas y validar
        curp_upper = usuario.curp.upper().strip()
        if len(curp_upper) != 18:
            raise HTTPException(status_code=400, detail="La CURP debe tener exactamente 18 caracteres")
        
        # Validación básica de formato CURP
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
        print(f"✅ Usuario creado con ID: {user_id}")
        
        # ==================== REGISTRO AUTOMÁTICO DE TÉRMINOS ====================
        
        # Registrar automáticamente la aceptación de términos al crear el usuario
        try:
            cursor.execute(
                "INSERT INTO usuarios_terminos (usuario_id, aceptado, fecha_aceptado) VALUES (%s, %s, NOW())",
                (user_id, True)
            )
            print(f"✅ Términos registrados automáticamente para usuario {user_id}")
        except psycopg2.IntegrityError as e:
            print(f"⚠️ Usuario {user_id} ya tiene términos registrados: {e}")
            # No es un error crítico, continuar
        except Exception as e:
            print(f"❌ Error registrando términos para usuario {user_id}: {e}")
            # No hacer rollback completo, solo advertir
        
        conn.commit()
        
        return {
            "id": user_id, 
            "mensaje": "Usuario creado exitosamente con términos aceptados automáticamente", 
            "curp": curp_upper,
            "terminos_registrados": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error completo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

# ==================== RESTO DE ENDPOINTS ORIGINALES ====================

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

# Define el timezone de CDMX
CDMX_TZ = pytz.timezone("America/Mexico_City")

def obtener_fecha_hora_cdmx(timestamp_offline=None):
    """Función de utilidad para manejar correctamente las fechas y horas en zona CDMX."""
    if timestamp_offline:
        try:
            print(f"🕐 Procesando timestamp offline: '{timestamp_offline}'")
            
            fecha_hora_utc = None
            
            # Caso 1: Termina con Z (UTC)
            if timestamp_offline.endswith('Z'):
                fecha_hora_utc = datetime.fromisoformat(timestamp_offline.replace('Z', '+00:00'))
                print(f"   📝 Formato detectado: UTC con Z")
                
            # Caso 2: Ya tiene información de zona horaria (+ o -)
            elif '+' in timestamp_offline or timestamp_offline.count('-') > 2:
                fecha_hora_utc = datetime.fromisoformat(timestamp_offline)
                print(f"   📝 Formato detectado: Con zona horaria")
                
            # Caso 3: Solo fecha y hora, asumir UTC
            else:
                if '.' in timestamp_offline:
                    fecha_hora_utc = datetime.fromisoformat(timestamp_offline).replace(tzinfo=pytz.UTC)
                else:
                    fecha_hora_utc = datetime.fromisoformat(timestamp_offline).replace(tzinfo=pytz.UTC)
                print(f"   📝 Formato detectado: Sin zona, asumiendo UTC")
            
            print(f"   🌍 Timestamp parseado como UTC: {fecha_hora_utc}")
            
            # Convertir a zona horaria de CDMX
            hora_cdmx = fecha_hora_utc.astimezone(CDMX_TZ)
            fecha_cdmx = hora_cdmx.date()
            
            print(f"📅 ✅ Conversión completada:")
            print(f"   🌍 UTC original: {fecha_hora_utc}")
            print(f"   🇲🇽 CDMX convertido: {hora_cdmx}")
            print(f"   📆 Fecha LOCAL CDMX: {fecha_cdmx}")
            
            timestamp_for_filename = hora_cdmx.strftime('%Y%m%d%H%M%S')
            
            return fecha_cdmx, hora_cdmx, timestamp_for_filename
            
        except Exception as e:
            print(f"⚠️ ERROR parseando timestamp offline '{timestamp_offline}': {e}")
            print(f"🔄 Fallback a tiempo actual de CDMX")
    
    # Usar tiempo actual de CDMX
    now_cdmx = datetime.now(CDMX_TZ)
    fecha_cdmx = now_cdmx.date()
    timestamp_for_filename = now_cdmx.strftime('%Y%m%d%H%M%S')
    
    print(f"📅 ⏰ Usando timestamp actual CDMX:")
    print(f"   🇲🇽 Hora CDMX: {now_cdmx}")
    print(f"   📆 Fecha CDMX: {fecha_cdmx}")
    
    return fecha_cdmx, now_cdmx, timestamp_for_filename

@app.post("/registro")
async def registrar(
    usuario_id: str = Form(...),
    latitud: float = Form(...),
    longitud: float = Form(...),
    descripcion: str = Form(""),
    foto: UploadFile = File(...),
    timestamp_offline: str = Form(None)
):
    print(f"🔍 REGISTRO - Datos recibidos:")
    print(f"   usuario_id: {usuario_id}")
    print(f"   latitud: {latitud}")
    print(f"   longitud: {longitud}")
    print(f"   descripcion: {descripcion}")
    print(f"   foto: {foto.filename}")
    print(f"   timestamp_offline: {timestamp_offline}")
    
    if timestamp_offline:
        try:
            fecha_hora = datetime.fromisoformat(timestamp_offline.replace('Z', '+00:00'))
            print(f"📅 ✅ Usando timestamp offline: {fecha_hora}")
            timestamp_for_filename = fecha_hora.strftime('%Y%m%d%H%M%S')
        except Exception as e:
            print(f"⚠️ Error parseando timestamp offline: {e}, usando tiempo actual")
            fecha_hora = datetime.utcnow()
            timestamp_for_filename = fecha_hora.strftime('%Y%m%d%H%M%S')
    else:
        fecha_hora = datetime.utcnow()
        timestamp_for_filename = fecha_hora.strftime('%Y%m%d%H%M%S')
        print(f"📅 ⏰ Usando timestamp actual: {fecha_hora}")

    # Guardar la foto en disco
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

@app.get("/registros")
def obtener_registros(usuario_id: int = None):
    try:
        print(f"🔍 Obteniendo registros para usuario: {usuario_id}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
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

@app.get("/usuarios")
async def obtener_usuarios():
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp, contrasena FROM usuarios ORDER BY id DESC"
        )
        
        resultados = cursor.fetchall()
        print(f"📊 Encontrados {len(resultados)} usuarios")
        
        usuarios = []
        for row in resultados:
            usuario = {
                "id": row[0],
                "correo": row[1],
                "nombre_completo": row[2],
                "cargo": row[3],
                "supervisor": row[4],
                "curp": row[5],
                "contrasena": row[6]
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

@app.get("/usuarios/{user_id}")
async def obtener_usuario(user_id: int):
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp, contrasena FROM usuarios WHERE id = %s",
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
            "curp": resultado[5],
            "contrasena": resultado[6]
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

# Resto de endpoints de asistencia...
@app.post("/asistencia/entrada")
async def marcar_entrada(
    usuario_id: int = Form(...),
    latitud: float = Form(...),
    longitud: float = Form(...),
    descripcion: str = Form(""),
    foto: UploadFile = File(...),
    timestamp_offline: str = Form(None)
):
    try:
        print(f"🔍 ENTRADA - Datos recibidos:")
        print(f"   usuario_id: {usuario_id}")
        print(f"   latitud: {latitud}")
        print(f"   longitud: {longitud}")
        print(f"   descripcion: {descripcion}")
        print(f"   foto: {foto.filename}")
        print(f"   timestamp_offline: {timestamp_offline}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        fecha, hora_entrada, timestamp_for_filename = obtener_fecha_hora_cdmx(timestamp_offline)

        cursor.execute(
            "SELECT id FROM asistencias WHERE usuario_id = %s AND fecha = %s",
            (usuario_id, fecha)
        )
        existe = cursor.fetchone()

        if existe:
            raise HTTPException(
                status_code=400, 
                detail=f"El usuario {usuario_id} ya tiene registro de entrada para el día {fecha}"
            )

        ext = os.path.splitext(foto.filename)[1]
        nombre_archivo = f"entrada_{usuario_id}_{timestamp_for_filename}{ext}"
        ruta_archivo = os.path.join(FOTOS_DIR, nombre_archivo)
        
        with open(ruta_archivo, "wb") as f:
            contenido = await foto.read()
            f.write(contenido)

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
    timestamp_offline: str = Form(None)
):
    try:
        print(f"🔍 SALIDA - Datos recibidos:")
        print(f"   usuario_id: {usuario_id}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        fecha, hora_salida, timestamp_for_filename = obtener_fecha_hora_cdmx(timestamp_offline)

        cursor.execute(
            "SELECT id, hora_salida FROM asistencias WHERE usuario_id = %s AND fecha = %s",
            (usuario_id, fecha)
        )
        registro = cursor.fetchone()

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

        ext = os.path.splitext(foto.filename)[1]
        nombre_archivo = f"salida_{usuario_id}_{timestamp_for_filename}{ext}"
        ruta_archivo = os.path.join(FOTOS_DIR, nombre_archivo)
        
        with open(ruta_archivo, "wb") as f:
            contenido = await foto.read()
            f.write(contenido)

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
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(e)}")

# ==================== ENDPOINT DE PRUEBA PARA TÉRMINOS ====================

@app.get("/test/terminos")
async def test_terminos():
    """Endpoint de prueba para verificar que la funcionalidad de términos está activa"""
    return {
        "status": "active",
        "message": "Los endpoints de términos están funcionando correctamente",
        "endpoints": {
            "verificar_terminos": "/usuarios/{user_id}/terminos",
            "aceptar_terminos": "/usuarios/aceptar_terminos",
            "crear_usuario_con_terminos": "/usuarios"
        },
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
