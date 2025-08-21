from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse
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
import json
from typing import List, Optional
import io
# Importaciones para Web Push
from pywebpush import webpush, WebPushException
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

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

# ==================== CONFIGURACIÓN VAPID PARA PUSH NOTIFICATIONS ====================

# Cargar claves VAPID
VAPID_KEYS = {
    "private_key": """-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQg9Vk9NeZ/wJxo7w2I
CY+Mbv9mi+f5xUZ+8vAN/ffNwiuhRANCAAQZSHdq8I6A9GuSaH5YIpWCV0qOfjlA
C5iOzzKAjFwnSWH5V/Xo8pvYFURmWienap6QZulsS0UdcQ2KuWyZe/3M
-----END PRIVATE KEY-----""",
    "public_key": "BBlId2rwjoD0a5JoflgilYJXSo5-OUALmI7PMoCMXCdJYflX9ejym9gVRGZaJ6dqnpBm6WxLRR1xDYq5bJl7_cw",
    "subject": "mailto:admin@sembrandodatos.com"
}

# Configuración para push notifications
PUSH_CONFIG = {
    "private_key": VAPID_KEYS["private_key"],
    "public_key": VAPID_KEYS["public_key"],
    "claims": {
        "sub": VAPID_KEYS["subject"]
    }
}

# Thread pool para operaciones de push asíncronas
push_executor = ThreadPoolExecutor(max_workers=10)

# Modelos para autenticación
class UserCreate(BaseModel):
    correo: str
    nombre_completo: str
    cargo: str
    supervisor: str = None
    contrasena: str
    curp: str  # CURP obligatoria
    telefono: str  # Teléfono obligatorio

class UserLogin(BaseModel):
    correo: str
    contrasena: str

class PasswordChange(BaseModel):
    usuario_id: int
    nueva_contrasena: str

# Modelo para actualizar información personal (sin contraseña)
class UserInfoUpdate(BaseModel):
    nombre_completo: str
    correo: str
    cargo: str
    supervisor: str = None
    curp: str = None
    telefono: str = None

class TerminosAceptados(BaseModel):
    usuario_id: int

# ==================== MODELOS PARA NOTIFICACIONES ====================

class NotificacionCreate(BaseModel):
    titulo: str
    subtitulo: Optional[str] = None
    descripcion: Optional[str] = None
    enlace_url: Optional[str] = None
    enviada_a_todos: bool = True
    usuario_ids: Optional[List[int]] = None  # Solo si enviada_a_todos = False

class NotificacionResponse(BaseModel):
    id: int
    titulo: str
    subtitulo: Optional[str] = None
    descripcion: Optional[str] = None
    enlace_url: Optional[str] = None
    archivo_nombre: Optional[str] = None
    archivo_tipo: Optional[str] = None
    enviada_a_todos: bool
    fecha_creacion: datetime
    fecha_envio: Optional[datetime] = None
    destinatarios: Optional[List[dict]] = None

# ==================== MODELOS PARA PUSH NOTIFICATIONS ====================

class PushSubscription(BaseModel):
    usuario_id: int
    endpoint: str
    p256dh: str
    auth: str
    user_agent: Optional[str] = None
    dispositivo: Optional[str] = None

class PushNotificationData(BaseModel):
    title: str
    body: Optional[str] = None
    icon: Optional[str] = "/pwa-192x192.png"
    badge: Optional[str] = "/pwa-192x192.png"
    tag: Optional[str] = None
    data: Optional[dict] = None
    vibrate: Optional[List[int]] = [200, 100, 200]
    requireInteraction: Optional[bool] = True

# ==================== FIN MODELOS NOTIFICACIONES ====================

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
        
        # Validación de teléfono obligatorio
        if not usuario.telefono or not usuario.telefono.strip():
            raise HTTPException(status_code=400, detail="El número de teléfono es obligatorio")
        
        # Validación básica de formato de teléfono (permitir números, +, espacios y -)
        if not re.match(r'^[0-9\+\s\-]+$', usuario.telefono):
            raise HTTPException(status_code=400, detail="El número de teléfono contiene caracteres no válidos")
            
        # Validar que el formato general sea correcto (al menos debe tener un + y números)
        if not re.match(r'^\+[0-9]+\s*[0-9]+$', usuario.telefono.strip()):
            raise HTTPException(status_code=400, detail="El formato del teléfono debe incluir código de país con + y números")
        
        # Comprobar si el correo ya existe
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (usuario.correo,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        
        # Comprobar si la CURP ya existe
        cursor.execute("SELECT id FROM usuarios WHERE curp = %s", (curp_upper,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="La CURP ya está registrada")
        
        # Insertar usuario con CURP y teléfono (contraseña sin encriptar)
        cursor.execute(
            "INSERT INTO usuarios (correo, nombre_completo, cargo, supervisor, contrasena, curp, telefono) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (usuario.correo, usuario.nombre_completo, usuario.cargo, usuario.supervisor, usuario.contrasena, curp_upper, usuario.telefono)
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
def obtener_registros(usuario_id: int = None, limit: int = None):
    try:
        print(f"🔍 Obteniendo registros para usuario: {usuario_id}, límite: {limit if limit else 'Sin límite'}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Usar cursor directo - NO usar cursor_factory aquí
        if usuario_id:
            if limit:
                cursor.execute(
                    "SELECT id, usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora FROM registros WHERE usuario_id = %s ORDER BY fecha_hora DESC LIMIT %s",
                    (usuario_id, limit)
                )
            else:
                cursor.execute(
                    "SELECT id, usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora FROM registros WHERE usuario_id = %s ORDER BY fecha_hora DESC",
                    (usuario_id,)
                )
        else:
            if limit:
                cursor.execute(
                    "SELECT id, usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora FROM registros ORDER BY fecha_hora DESC LIMIT %s",
                    (limit,)
                )
            else:
                cursor.execute(
                    "SELECT id, usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora FROM registros ORDER BY fecha_hora DESC"
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

# NUEVO ENDPOINT PARA ESTADÍSTICAS COMPLETAS (SIN LÍMITES)
@app.get("/estadisticas")
def obtener_estadisticas():
    """Obtener estadísticas completas del sistema sin límites"""
    try:
        print("🔍 Obteniendo estadísticas completas del sistema")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Obtener total real de registros (actividades)
        cursor.execute("SELECT COUNT(*) FROM registros")
        total_registros = cursor.fetchone()[0]
        
        # Obtener total de usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        # Obtener registros de hoy
        cursor.execute("SELECT COUNT(*) FROM registros WHERE DATE(fecha_hora) = CURRENT_DATE")
        registros_hoy = cursor.fetchone()[0]
        
        # Obtener total de asistencias
        cursor.execute("SELECT COUNT(*) FROM asistencias")
        total_asistencias = cursor.fetchone()[0]
        
        # Obtener asistencias de hoy
        cursor.execute("SELECT COUNT(*) FROM asistencias WHERE fecha = CURRENT_DATE")
        asistencias_hoy = cursor.fetchone()[0]
        
        # Obtener usuarios presentes hoy (que han marcado entrada)
        cursor.execute("""
            SELECT COUNT(DISTINCT usuario_id) FROM asistencias 
            WHERE fecha = CURRENT_DATE AND hora_entrada IS NOT NULL
        """)
        usuarios_presentes = cursor.fetchone()[0]
        
        estadisticas = {
            "total_registros": total_registros,
            "total_usuarios": total_usuarios,
            "registros_hoy": registros_hoy,
            "total_asistencias": total_asistencias,
            "asistencias_hoy": asistencias_hoy,
            "usuarios_presentes": usuarios_presentes
        }
        
        print(f"✅ Estadísticas obtenidas: {estadisticas}")
        return {"estadisticas": estadisticas}
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

# Nuevo endpoint para obtener usuarios (para el panel de administración)
@app.get("/usuarios")
async def obtener_usuarios():
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Obtener todos los usuarios con CURP, teléfono y contraseña
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp, contrasena, telefono FROM usuarios ORDER BY id DESC"
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
                "contrasena": row[6],  # Incluir contraseña
                "telefono": row[7] if len(row) > 7 else None  # Incluir teléfono si existe
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
        
        # Obtener TODOS los campos de usuarios incluyendo contraseñas y teléfono
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, contrasena, curp, telefono FROM usuarios ORDER BY id DESC"
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
                "curp": row[6],
                "telefono": row[7] if len(row) > 7 else None  # Incluir teléfono si existe
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

# Endpoint para obtener un usuario específico por ID
@app.get("/usuarios/{user_id}")
async def obtener_usuario(user_id: int):
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Buscar usuario por ID con CURP, teléfono y contraseña
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp, contrasena, telefono FROM usuarios WHERE id = %s",
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
            "contrasena": resultado[6],  # Incluir contraseña
            "telefono": resultado[7] if len(resultado) > 7 else None  # Incluir teléfono si existe
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

# Endpoint para actualizar un usuario específico
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
            """UPDATE usuarios 
               SET correo = %s, nombre_completo = %s, cargo = %s, 
                   supervisor = %s, contrasena = %s, curp = %s, telefono = %s 
               WHERE id = %s""",
            (usuario.correo, usuario.nombre_completo, usuario.cargo, 
             usuario.supervisor, usuario.contrasena, curp_upper, usuario.telefono, user_id)
        )
        
        conn.commit()
        
        # Obtener usuario actualizado
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, contrasena, curp, telefono FROM usuarios WHERE id = %s",
            (user_id,)
        )
        
        resultado = cursor.fetchone()
        usuario_actualizado = {
            "id": resultado[0],
            "correo": resultado[1],
            "nombre_completo": resultado[2],
            "cargo": resultado[3],
            "supervisor": resultado[4],
            "contrasena": resultado[5],
            "curp": resultado[6],
            "telefono": resultado[7] if len(resultado) > 7 else None
        }
        
        print(f"✅ Usuario {user_id} actualizado exitosamente")
        return {"mensaje": "Usuario actualizado exitosamente", "usuario": usuario_actualizado}
        
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

# Endpoint para actualizar solo información personal de un usuario (sin contraseña)
@app.patch("/usuarios/{user_id}/info")
async def actualizar_info_usuario(user_id: int, info: UserInfoUpdate):
    """Actualiza solo la información personal de un usuario (sin modificar contraseña)"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"✏️ Actualizando información personal del usuario {user_id}...")
        
        # Validación de CURP si se proporciona
        curp_upper = None
        if info.curp and info.curp.strip():
            curp_upper = info.curp.upper().strip()
            if len(curp_upper) != 18:
                raise HTTPException(status_code=400, detail="La CURP debe tener exactamente 18 caracteres")
            
            if not re.match(r'^[A-Z0-9]{18}$', curp_upper):
                raise HTTPException(status_code=400, detail="La CURP tiene un formato inválido")
            
            # Verificar que la CURP no esté en uso por otro usuario
            cursor.execute("SELECT id FROM usuarios WHERE curp = %s AND id != %s", (curp_upper, user_id))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Esta CURP ya está registrada por otro usuario")
        
        # Verificar que el correo no esté en uso por otro usuario
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s AND id != %s", (info.correo, user_id))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Este correo ya está registrado por otro usuario")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Actualizar solo información personal (sin modificar contraseña)
        cursor.execute(
            """UPDATE usuarios 
               SET correo = %s, nombre_completo = %s, cargo = %s, 
                   supervisor = %s, curp = %s, telefono = %s 
               WHERE id = %s""",
            (info.correo, info.nombre_completo, info.cargo, 
             info.supervisor, curp_upper, info.telefono, user_id)
        )
        
        conn.commit()
        
        # Obtener usuario actualizado
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp, telefono FROM usuarios WHERE id = %s",
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
            "telefono": resultado[6]
        }
        
        print(f"✅ Información personal del usuario {user_id} actualizada exitosamente")
        return {"success": True, "mensaje": "Información personal actualizada exitosamente", "usuario": usuario_actualizado}
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar información personal: {str(e)}")

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

def obtener_fecha_hora_cdmx(timestamp_offline=None):
    """
    Función de utilidad para manejar correctamente las fechas y horas en zona CDMX.
    
    Args:
        timestamp_offline (str): Timestamp ISO string opcional desde el cliente
        
    Returns:
        tuple: (fecha_cdmx, hora_cdmx, timestamp_for_filename)
    """
    if timestamp_offline:
        try:
            print(f"🕐 Procesando timestamp offline: '{timestamp_offline}'")
            
            # NUEVA LÓGICA MÁS ROBUSTA PARA PARSEAR TIMESTAMPS
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
                # Verificar si tiene microsegundos
                if '.' in timestamp_offline:
                    # Formato: 2025-07-27T23:30:45.123
                    fecha_hora_utc = datetime.fromisoformat(timestamp_offline).replace(tzinfo=pytz.UTC)
                else:
                    # Formato: 2025-07-27T23:30:45
                    fecha_hora_utc = datetime.fromisoformat(timestamp_offline).replace(tzinfo=pytz.UTC)
                print(f"   📝 Formato detectado: Sin zona, asumiendo UTC")
            
            print(f"   🌍 Timestamp parseado como UTC: {fecha_hora_utc}")
            
            # CLAVE: Convertir a zona horaria de CDMX PRIMERO
            hora_cdmx = fecha_hora_utc.astimezone(CDMX_TZ)
            
            # LUEGO extraer la fecha LOCAL de CDMX (no UTC)
            fecha_cdmx = hora_cdmx.date()
            
            print(f"📅 ✅ Conversión de timestamp completada:")
            print(f"   🌍 UTC original: {fecha_hora_utc}")
            print(f"   🇲🇽 CDMX convertido: {hora_cdmx}")
            print(f"   📆 Fecha LOCAL CDMX: {fecha_cdmx}")
            print(f"   📊 Día de la semana: {fecha_cdmx.strftime('%A')}")
            
            timestamp_for_filename = hora_cdmx.strftime('%Y%m%d%H%M%S')
            
            return fecha_cdmx, hora_cdmx, timestamp_for_filename
            
        except Exception as e:
            print(f"⚠️ ERROR parseando timestamp offline '{timestamp_offline}': {e}")
            print(f"🔄 Fallback a tiempo actual de CDMX")
            # Fallback a tiempo actual
            pass
    
    # Usar tiempo actual de CDMX
    now_cdmx = datetime.now(CDMX_TZ)
    fecha_cdmx = now_cdmx.date()
    timestamp_for_filename = now_cdmx.strftime('%Y%m%d%H%M%S')
    
    print(f"📅 ⏰ Usando timestamp actual CDMX:")
    print(f"   🇲🇽 Hora CDMX: {now_cdmx}")
    print(f"   📆 Fecha CDMX: {fecha_cdmx}")
    print(f"   📊 Día de la semana: {fecha_cdmx.strftime('%A')}")
    
    return fecha_cdmx, now_cdmx, timestamp_for_filename

@app.post("/asistencia/entrada")
async def marcar_entrada(
    usuario_id: int = Form(...),
    latitud: float = Form(...),
    longitud: float = Form(...),
    descripcion: str = Form(""),
    foto: UploadFile = File(...),
    timestamp_offline: str = Form(None)  # Nuevo campo opcional para registro offline
):
    try:
        print(f"🔍 ENTRADA - Datos recibidos:")
        print(f"   usuario_id: {usuario_id} (tipo: {type(usuario_id)})")
        print(f"   latitud: {latitud}")
        print(f"   longitud: {longitud}")
        print(f"   descripcion: {descripcion}")
        print(f"   foto: {foto.filename}")
        print(f"   timestamp_offline: {timestamp_offline}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Usar timestamp personalizado si viene de offline, sino usar tiempo actual
        fecha, hora_entrada, timestamp_for_filename = obtener_fecha_hora_cdmx(timestamp_offline)

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
    timestamp_offline: str = Form(None)  # Nuevo campo opcional para registro offline
):
    try:
        print(f"🔍 SALIDA - Datos recibidos:")
        print(f"   usuario_id: {usuario_id} (tipo: {type(usuario_id)})")
        print(f"   latitud: {latitud}")
        print(f"   longitud: {longitud}")
        print(f"   descripcion: {descripcion}")
        print(f"   foto: {foto.filename}")
        print(f"   timestamp_offline: {timestamp_offline}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Usar timestamp personalizado si viene de offline, sino usar tiempo actual
        fecha, hora_salida, timestamp_for_filename = obtener_fecha_hora_cdmx(timestamp_offline)

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

@app.get("/asistencia/hoy/{usuario_id}")
async def consultar_asistencia_hoy(usuario_id: int):
    """
    Consulta la asistencia del día actual para un usuario específico.
    Usa la zona horaria de CDMX para determinar correctamente qué es 'hoy'.
    """
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🔍 Consultando asistencia del día actual para usuario {usuario_id}")
        
        # CRUCIAL: Usar la fecha actual en zona horaria CDMX
        now_cdmx = datetime.now(CDMX_TZ)
        fecha_hoy_cdmx = now_cdmx.date()
        
        print(f"📅 Fecha actual en CDMX: {fecha_hoy_cdmx}")
        print(f"⏰ Hora actual en CDMX: {now_cdmx.strftime('%H:%M:%S')}")
        
        # Consultar asistencia para la fecha actual en CDMX
        cursor.execute(
            """SELECT id, usuario_id, fecha, hora_entrada, hora_salida, 
                      latitud_entrada, longitud_entrada, latitud_salida, longitud_salida,
                      foto_entrada_url, foto_salida_url, descripcion_entrada, descripcion_salida
               FROM asistencias 
               WHERE usuario_id = %s AND fecha = %s""",
            (usuario_id, fecha_hoy_cdmx)
        )
        
        registro = cursor.fetchone()
        
        print(f"📊 Registro encontrado: {registro is not None}")
        
        if registro:
            # Construir respuesta con datos encontrados
            resultado = {
                "id": registro[0],
                "usuario_id": registro[1],
                "fecha": registro[2].isoformat() if registro[2] else None,
                "entrada": registro[3].isoformat() if registro[3] else None,
                "salida": registro[4].isoformat() if registro[4] else None,
                "latitud_entrada": float(registro[5]) if registro[5] else None,
                "longitud_entrada": float(registro[6]) if registro[6] else None,
                "latitud_salida": float(registro[7]) if registro[7] else None,
                "longitud_salida": float(registro[8]) if registro[8] else None,
                "foto_entrada_url": registro[9],
                "foto_salida_url": registro[10],
                "descripcion_entrada": registro[11],
                "descripcion_salida": registro[12]
            }
        else:
            # No hay registro para hoy, devolver estructura vacía
            resultado = {
                "id": None,
                "usuario_id": usuario_id,
                "fecha": fecha_hoy_cdmx.isoformat(),
                "entrada": None,
                "salida": None,
                "latitud_entrada": None,
                "longitud_entrada": None,
                "latitud_salida": None,
                "longitud_salida": None,
                "foto_entrada_url": None,
                "foto_salida_url": None,
                "descripcion_entrada": None,
                "descripcion_salida": None
            }
        
        print(f"✅ Consulta de asistencia hoy completada: {resultado['entrada'] is not None}, {resultado['salida'] is not None}")
        return resultado
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL en consulta hoy: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general en consulta hoy: {e}")
        raise HTTPException(status_code=500, detail=f"Error al consultar asistencia de hoy: {str(e)}")

@app.get("/debug/tiempo-actual")
async def debug_tiempo_actual():
    """Endpoint para verificar la hora y fecha actual en diferentes zonas horarias"""
    try:
        import pytz
        from datetime import datetime
        
        # Hora UTC
        utc_now = datetime.utcnow()
        
        # Hora en CDMX
        cdmx_tz = pytz.timezone("America/Mexico_City")
        cdmx_now = datetime.now(cdmx_tz)
        
        # Fecha en CDMX (que es lo que usamos para comparar asistencias)
        fecha_cdmx = cdmx_now.date()
        
        resultado = {
            "utc": {
                "datetime": utc_now.isoformat(),
                "fecha": utc_now.date().isoformat(),
                "hora": utc_now.strftime("%H:%M:%S"),
                "timestamp_filename": utc_now.strftime('%Y%m%d%H%M%S')
            },
            "cdmx": {
                "datetime": cdmx_now.isoformat(),
                "fecha": fecha_cdmx.isoformat(),
                "hora": cdmx_now.strftime("%H:%M:%S"),
                "timestamp_filename": cdmx_now.strftime('%Y%m%d%H%M%S'),
                "timezone_name": str(cdmx_now.tzinfo),
                "timezone_offset": cdmx_now.strftime('%z')
            },
            "comparacion": {
                "misma_fecha": utc_now.date() == fecha_cdmx,
                "diferencia_horas": int((cdmx_now - utc_now.replace(tzinfo=pytz.UTC)).total_seconds() / 3600)
            },
            "mensaje": f"En CDMX son las {cdmx_now.strftime('%H:%M:%S')} del {fecha_cdmx.strftime('%Y-%m-%d')}"
        }
        
        return resultado
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/asistencias")
async def obtener_historial_asistencias(usuario_id: int = None, limit: int = None):
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🔍 Obteniendo historial de asistencias para usuario: {usuario_id}, límite: {limit if limit else 'Sin límite'}")
        
        if usuario_id:
            if limit:
                cursor.execute(
                    """SELECT id, usuario_id, fecha, hora_entrada, hora_salida, 
                              latitud_entrada, longitud_entrada, latitud_salida, longitud_salida,
                              foto_entrada_url, foto_salida_url, descripcion_entrada, descripcion_salida
                       FROM asistencias 
                       WHERE usuario_id = %s 
                       ORDER BY fecha DESC, hora_entrada DESC 
                       LIMIT %s""",
                    (usuario_id, limit)
                )
            else:
                cursor.execute(
                    """SELECT id, usuario_id, fecha, hora_entrada, hora_salida, 
                              latitud_entrada, longitud_entrada, latitud_salida, longitud_salida,
                              foto_entrada_url, foto_salida_url, descripcion_entrada, descripcion_salida
                       FROM asistencias 
                       WHERE usuario_id = %s 
                       ORDER BY fecha DESC, hora_entrada DESC""",
                    (usuario_id,)
                )
        else:
            if limit:
                cursor.execute(
                    """SELECT id, usuario_id, fecha, hora_entrada, hora_salida, 
                              latitud_entrada, longitud_entrada, latitud_salida, longitud_salida,
                              foto_entrada_url, foto_salida_url, descripcion_entrada, descripcion_salida
                       FROM asistencias 
                       ORDER BY fecha DESC, hora_entrada DESC 
                       LIMIT %s""",
                    (limit,)
                )
            else:
                cursor.execute(
                    """SELECT id, usuario_id, fecha, hora_entrada, hora_salida, 
                              latitud_entrada, longitud_entrada, latitud_salida, longitud_salida,
                              foto_entrada_url, foto_salida_url, descripcion_entrada, descripcion_salida
                       FROM asistencias 
                       ORDER BY fecha DESC, hora_entrada DESC"""
                )
        
        resultados = cursor.fetchall()
        print(f"📊 Encontradas {len(resultados)} asistencias totales sin límite")
        
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
        
        print(f"✅ Historial completo de {len(asistencias)} asistencias procesado correctamente")
        return {"asistencias": asistencias}
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(e)}")

# Endpoint de test para simular registro de asistencia
@app.post("/debug/test-asistencia-fecha")
async def test_asistencia_fecha(
    timestamp_offline: str = Form(None)
):
    """Test para verificar exactamente cómo se procesa una fecha en asistencia"""
    try:
        print(f"🧪 TEST ASISTENCIA - Timestamp recibido: {timestamp_offline}")
        
        # Usar la misma función que usan las asistencias reales
        fecha, hora, filename = obtener_fecha_hora_cdmx(timestamp_offline)
        
        # Simular lo que haría la base de datos
        registro_simulado = {
            "usuario_id": 999,  # ID de test
            "fecha": fecha.isoformat(),
            "hora_entrada": hora.isoformat(),
            "timestamp_filename": filename
        }
        
        # Información actual para comparar
        ahora_cdmx = datetime.now(CDMX_TZ)
        
        result = {
            "test_resultado": {
                "timestamp_input": timestamp_offline,
                "fecha_procesada": fecha.isoformat(),
                "dia_procesado": fecha.strftime('%A, %d de %B %Y'),
                "hora_procesada": hora.isoformat(),
                "filename_generado": filename
            },
            
            "comparacion_fecha": {
                "fecha_hoy_real": ahora_cdmx.date().isoformat(),
                "dia_hoy_real": ahora_cdmx.strftime('%A, %d de %B %Y'),
                "coincide_con_hoy": fecha == ahora_cdmx.date(),
                "diferencia_dias": (fecha - ahora_cdmx.date()).days
            },
            
            "registro_que_se_guardaria": registro_simulado,
            
            "diagnostico_final": {
                "problema_detectado": fecha != ahora_cdmx.date(),
                "mensaje": "FECHA CORRECTA ✅" if fecha == ahora_cdmx.date() else f"FECHA INCORRECTA ❌ - Diferencia: {(fecha - ahora_cdmx.date()).days} días"
            }
        }
        
        print(f"🧪 RESULTADO TEST ASISTENCIA:")
        print(f"   📅 Fecha que se guardará: {fecha} ({fecha.strftime('%A')})")
        print(f"   ✅ ¿Es correcto?: {fecha == ahora_cdmx.date()}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error en test asistencia: {e}")
        return {"error": f"Error en test: {e}"}

# Endpoint de debugging ESPECÍFICO para el problema de fechas
@app.get("/debug/problema-fecha-actual")
async def debug_problema_fecha():
    """Debugging específico para entender por qué se guarda un día antes"""
    try:
        import pytz
        from datetime import datetime
        
        # Hora actual real
        ahora_utc = datetime.utcnow()
        ahora_cdmx = datetime.now(CDMX_TZ)
        
        # Simular un timestamp que podría venir del frontend
        timestamp_simulado = ahora_cdmx.isoformat()
        
        # Probar nuestra función
        fecha_resultado, hora_resultado, filename_resultado = obtener_fecha_hora_cdmx(timestamp_simulado)
        
        # También probar sin timestamp (tiempo actual)
        fecha_actual, hora_actual, filename_actual = obtener_fecha_hora_cdmx(None)
        
        return {
            "analisis_completo": {
                "fecha_esperada_hoy": ahora_cdmx.date().isoformat(),
                "dia_esperado": ahora_cdmx.strftime('%A, %d de %B %Y'),
                
                "con_timestamp_simulado": {
                    "timestamp_input": timestamp_simulado,
                    "fecha_obtenida": fecha_resultado.isoformat(),
                    "dia_obtenido": fecha_resultado.strftime('%A, %d de %B %Y'),
                    "es_correcto": fecha_resultado == ahora_cdmx.date(),
                    "diferencia_dias": (fecha_resultado - ahora_cdmx.date()).days
                },
                
                "sin_timestamp_actual": {
                    "fecha_obtenida": fecha_actual.isoformat(), 
                    "dia_obtenido": fecha_actual.strftime('%A, %d de %B %Y'),
                    "es_correcto": fecha_actual == ahora_cdmx.date(),
                    "diferencia_dias": (fecha_actual - ahora_cdmx.date()).days
                },
                
                "referencias_tiempo": {
                    "utc_ahora": ahora_utc.isoformat(),
                    "cdmx_ahora": ahora_cdmx.isoformat(),
                    "diferencia_horas": (ahora_cdmx - ahora_utc.replace(tzinfo=pytz.UTC)).total_seconds() / 3600
                }
            },
            
            "diagnostico": {
                "problema_detectado": fecha_resultado != ahora_cdmx.date() or fecha_actual != ahora_cdmx.date(),
                "causa_probable": "Conversión de zona horaria incorrecta" if fecha_resultado != ahora_cdmx.date() else "Función trabajando correctamente",
                "accion_recomendada": "Revisar lógica de conversión de timestamps" if fecha_resultado != ahora_cdmx.date() else "No hay problema"
            }
        }
        
    except Exception as e:
        return {"error": f"Error en debugging: {e}"}

# Endpoint de debugging para fechas y zonas horarias
@app.get("/debug/fecha-zona-horaria")
async def debug_fecha_zona_horaria():
    """Endpoint para debugging de zonas horarias y fechas"""
    try:
        # Tiempo actual en diferentes zonas
        utc_now = datetime.utcnow()
        cdmx_now = datetime.now(CDMX_TZ)
        
        # Probar la función de utilidad
        fecha_util, hora_util, filename_util = obtener_fecha_hora_cdmx()
        
        return {
            "debug_info": {
                "utc_actual": {
                    "datetime": utc_now.isoformat(),
                    "fecha": utc_now.date().isoformat(),
                    "dia_semana": utc_now.strftime('%A')
                },
                "cdmx_actual": {
                    "datetime": cdmx_now.isoformat(),
                    "fecha": cdmx_now.date().isoformat(),
                    "dia_semana": cdmx_now.strftime('%A')
                },
                "funcion_utilidad": {
                    "fecha": fecha_util.isoformat(),
                    "hora": hora_util.isoformat(),
                    "filename": filename_util,
                    "dia_semana": fecha_util.strftime('%A')
                }
            },
            "problema_detectado": {
                "diferencia_fechas": utc_now.date() != cdmx_now.date(),
                "diferencia_horas": abs((cdmx_now - utc_now.replace(tzinfo=pytz.UTC)).total_seconds() / 3600),
                "recomendacion": "Siempre usar la fecha de CDMX para registros"
            }
        }
        
    except Exception as e:
        return {"error": f"Error en debug: {e}"}

# Endpoint de test para debugging de asistencias
@app.post("/debug/test-fecha-asistencia")
async def test_fecha_asistencia(
    timestamp_offline: str = Form(None)
):
    """Test para verificar cómo se procesan las fechas en asistencias"""
    try:
        print(f"🧪 TEST - Timestamp recibido: {timestamp_offline}")
        
        # Probar la función de utilidad
        fecha, hora, filename = obtener_fecha_hora_cdmx(timestamp_offline)
        
        # Información detallada
        result = {
            "test_info": {
                "timestamp_input": timestamp_offline,
                "fecha_procesada": fecha.isoformat(),
                "hora_procesada": hora.isoformat(),
                "filename_generado": filename,
                "dia_semana": fecha.strftime('%A, %d de %B %Y'),
                "zona_horaria": str(hora.tzinfo)
            },
            "verificaciones": {
                "es_hoy": fecha == datetime.now(CDMX_TZ).date(),
                "timestamp_valido": timestamp_offline is not None,
                "zona_correcta": str(hora.tzinfo) == "America/Mexico_City"
            }
        }
        
        print(f"🧪 RESULTADO DEL TEST:")
        print(f"   📅 Fecha: {fecha} ({fecha.strftime('%A')})")
        print(f"   🕐 Hora: {hora}")
        print(f"   ✅ Es hoy: {result['verificaciones']['es_hoy']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return {"error": f"Error en test: {e}"}

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

# ================== ENDPOINTS PARA HISTORIAL ==================

class HistorialCreate(BaseModel):
    usuario_id: int
    tipo: str  # 'entrada', 'salida', 'actividad'
    descripcion: str
    fecha: str = None  # Si no se proporciona, usa la fecha actual
    hora: str = None   # Si no se proporciona, usa la hora actual
    detalles: dict = None  # Para guardar ubicación, foto_url, etc.

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
        print(f"❌ Error obteniendo resumen de historial: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo resumen: {str(e)}")

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

# ==================== ENDPOINTS DE NOTIFICACIONES ====================

# Define el timezone de CDMX para notificaciones
CDMX_TZ = pytz.timezone("America/Mexico_City")

def obtener_fecha_hora_cdmx_notificaciones():
    """Función de utilidad para obtener fecha y hora actual en zona CDMX para notificaciones"""
    return datetime.now(CDMX_TZ)

# ==================== FUNCIONES PARA PUSH NOTIFICATIONS ====================

def send_push_notification(subscription_info, notification_data):
    """Enviar push notification individual (función síncrona)"""
    try:
        # Preparar los datos de la notificación
        payload = {
            "title": notification_data["title"],
            "body": notification_data.get("body", ""),
            "icon": notification_data.get("icon", "/pwa-192x192.png"),
            "badge": notification_data.get("badge", "/pwa-192x192.png"),
            "tag": notification_data.get("tag", f"notification-{datetime.now().timestamp()}"),
            "data": notification_data.get("data", {}),
            "vibrate": notification_data.get("vibrate", [200, 100, 200]),
            "requireInteraction": notification_data.get("requireInteraction", True)
        }
        
        # Configurar suscripción
        subscription = {
            "endpoint": subscription_info["endpoint"],
            "keys": {
                "p256dh": subscription_info["p256dh"],
                "auth": subscription_info["auth"]
            }
        }
        
        # Enviar push notification
        response = webpush(
            subscription_info=subscription,
            data=json.dumps(payload),
            vapid_private_key=PUSH_CONFIG["private_key"],
            vapid_claims=PUSH_CONFIG["claims"]
        )
        
        print(f"✅ Push notification enviada exitosamente (status: {response.status_code})")
        return {"success": True, "status_code": response.status_code}
        
    except WebPushException as e:
        print(f"❌ Error enviando push notification: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"❌ Error inesperado enviando push: {e}")
        return {"success": False, "error": str(e)}

async def send_push_to_users(user_ids, notification_data):
    """Enviar push notifications a una lista de usuarios (función asíncrona)"""
    if not user_ids:
        return {"sent": 0, "failed": 0, "results": []}
    
    try:
        # Obtener suscripciones activas de los usuarios
        cursor.execute("""
            SELECT ps.usuario_id, ps.endpoint, ps.p256dh, ps.auth, u.nombre_completo
            FROM push_subscriptions ps
            JOIN usuarios u ON ps.usuario_id = u.id
            WHERE ps.usuario_id = ANY(%s) AND ps.activa = TRUE
        """, (user_ids,))
        
        subscriptions = cursor.fetchall()
        
        if not subscriptions:
            print(f"⚠️ No se encontraron suscripciones activas para usuarios: {user_ids}")
            return {"sent": 0, "failed": 0, "results": [], "message": "No hay dispositivos suscritos"}
        
        print(f"📱 Enviando push notifications a {len(subscriptions)} dispositivos...")
        
        # Enviar notificaciones en paralelo usando ThreadPoolExecutor
        loop = asyncio.get_event_loop()
        tasks = []
        
        for sub in subscriptions:
            subscription_info = {
                "endpoint": sub[1],
                "p256dh": sub[2], 
                "auth": sub[3]
            }
            
            # Ejecutar en thread pool para evitar bloqueo
            task = loop.run_in_executor(
                push_executor,
                send_push_notification,
                subscription_info,
                notification_data
            )
            tasks.append((sub[0], sub[4], task))  # (user_id, nombre, task)
        
        # Esperar todos los resultados
        results = []
        sent_count = 0
        failed_count = 0
        
        for user_id, nombre, task in tasks:
            try:
                result = await task
                if result["success"]:
                    sent_count += 1
                    results.append({
                        "user_id": user_id,
                        "nombre": nombre,
                        "status": "sent",
                        "message": "Enviado exitosamente"
                    })
                else:
                    failed_count += 1
                    results.append({
                        "user_id": user_id,
                        "nombre": nombre,
                        "status": "failed",
                        "error": result["error"]
                    })
            except Exception as e:
                failed_count += 1
                results.append({
                    "user_id": user_id,
                    "nombre": nombre,
                    "status": "failed",
                    "error": str(e)
                })
        
        print(f"📊 Push notifications: {sent_count} enviadas, {failed_count} fallidas")
        
        return {
            "sent": sent_count,
            "failed": failed_count,
            "total_devices": len(subscriptions),
            "results": results
        }
        
    except Exception as e:
        print(f"❌ Error enviando push notifications: {e}")
        return {"sent": 0, "failed": 0, "results": [], "error": str(e)}

async def send_push_to_all_users(notification_data):
    """Enviar push notification a todos los usuarios con suscripciones activas"""
    try:
        # Obtener todas las suscripciones activas
        cursor.execute("""
            SELECT DISTINCT ps.usuario_id
            FROM push_subscriptions ps
            WHERE ps.activa = TRUE
        """)
        
        user_ids = [row[0] for row in cursor.fetchall()]
        
        if not user_ids:
            print("⚠️ No hay usuarios con suscripciones activas")
            return {"sent": 0, "failed": 0, "results": [], "message": "No hay dispositivos suscritos"}
        
        print(f"📢 Enviando push notification a todos los usuarios ({len(user_ids)} usuarios)")
        
        return await send_push_to_users(user_ids, notification_data)
        
    except Exception as e:
        print(f"❌ Error enviando push a todos: {e}")
        return {"sent": 0, "failed": 0, "results": [], "error": str(e)}

@app.post("/notificaciones")
async def crear_notificacion(
    titulo: str = Form(...),
    subtitulo: str = Form(None),
    descripcion: str = Form(None),
    enlace_url: str = Form(None),
    enviada_a_todos: bool = Form(True),
    usuario_ids: str = Form(None),  # JSON string con lista de IDs
    archivo: UploadFile = File(None)
):
    """Crear una nueva notificación"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🔔 Creando notificación: {titulo}")
        
        # Validaciones básicas
        if len(titulo.strip()) == 0:
            raise HTTPException(status_code=400, detail="El título es obligatorio")
        
        if len(titulo) > 150:
            raise HTTPException(status_code=400, detail="El título no puede exceder 150 caracteres")
        
        if subtitulo and len(subtitulo) > 200:
            raise HTTPException(status_code=400, detail="El subtítulo no puede exceder 200 caracteres")
        
        # Validar usuarios si no es para todos
        usuarios_seleccionados = []
        if not enviada_a_todos:
            if not usuario_ids:
                raise HTTPException(status_code=400, detail="Debe especificar usuarios si no se envía a todos")
            
            try:
                usuarios_seleccionados = json.loads(usuario_ids)
                if not isinstance(usuarios_seleccionados, list) or len(usuarios_seleccionados) == 0:
                    raise HTTPException(status_code=400, detail="Debe seleccionar al menos un usuario")
                
                # Verificar que todos los usuarios existen
                cursor.execute("SELECT id FROM usuarios WHERE id = ANY(%s)", (usuarios_seleccionados,))
                usuarios_existentes = [row[0] for row in cursor.fetchall()]
                
                usuarios_inexistentes = set(usuarios_seleccionados) - set(usuarios_existentes)
                if usuarios_inexistentes:
                    raise HTTPException(status_code=400, detail=f"Usuarios no encontrados: {list(usuarios_inexistentes)}")
                
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Formato de usuarios inválido")
        
        # Procesar archivo si se proporciona
        archivo_bytes = None
        archivo_tipo = None
        archivo_nombre = None
        
        if archivo and archivo.filename:
            print(f"📎 Procesando archivo: {archivo.filename}")
            
            # Validar tipo de archivo
            ext = os.path.splitext(archivo.filename)[1].lower()
            tipos_permitidos = {
                '.jpg': 'imagen', '.jpeg': 'imagen', '.png': 'imagen', '.gif': 'imagen',
                '.pdf': 'pdf',
                '.mp4': 'video', '.avi': 'video', '.mov': 'video', '.wmv': 'video'
            }
            
            if ext not in tipos_permitidos:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Tipo de archivo no permitido. Formatos válidos: {', '.join(tipos_permitidos.keys())}"
                )
            
            # Leer archivo
            archivo_bytes = await archivo.read()
            archivo_tipo = tipos_permitidos[ext]
            archivo_nombre = archivo.filename
            
            # Validar tamaño (50MB máximo)
            if len(archivo_bytes) > 50 * 1024 * 1024:
                raise HTTPException(status_code=400, detail="El archivo no debe exceder 50MB")
            
            print(f"📎 Archivo procesado: {archivo_nombre} ({archivo_tipo}, {len(archivo_bytes)} bytes)")
        
        # Obtener fecha y hora actual en CDMX
        fecha_creacion = obtener_fecha_hora_cdmx_notificaciones()
        fecha_envio = fecha_creacion  # Se considera enviada inmediatamente
        
        # Insertar notificación
        cursor.execute("""
            INSERT INTO notificaciones (
                titulo, subtitulo, descripcion, enlace_url,
                archivo, archivo_tipo, archivo_nombre,
                enviada_a_todos, fecha_creacion, fecha_envio
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            titulo, subtitulo, descripcion, enlace_url,
            archivo_bytes, archivo_tipo, archivo_nombre,
            enviada_a_todos, fecha_creacion, fecha_envio
        ))
        
        notificacion_id = cursor.fetchone()[0]
        
        # Si no es para todos, insertar relaciones con usuarios
        if not enviada_a_todos and usuarios_seleccionados:
            for usuario_id in usuarios_seleccionados:
                cursor.execute(
                    "INSERT INTO notificacion_usuarios (notificacion_id, usuario_id) VALUES (%s, %s)",
                    (notificacion_id, usuario_id)
                )
            print(f"👥 Notificación asignada a {len(usuarios_seleccionados)} usuarios específicos")
        
        conn.commit()
        
        print(f"✅ Notificación creada exitosamente con ID: {notificacion_id}")
        
        # ==================== ENVIAR PUSH NOTIFICATIONS ====================
        
        # Preparar datos para push notification
        push_notification_data = {
            "title": titulo,
            "body": subtitulo or descripcion or "Nueva notificación disponible",
            "icon": "/pwa-192x192.png",
            "badge": "/pwa-192x192.png", 
            "tag": f"notification-{notificacion_id}",
            "data": {
                "notificacionId": notificacion_id,
                "url": "/notificaciones",
                "timestamp": fecha_creacion.timestamp()
            },
            "vibrate": [200, 100, 200],
            "requireInteraction": True
        }
        
        # Enviar push notifications según el tipo
        push_results = {"sent": 0, "failed": 0, "results": []}
        
        try:
            if enviada_a_todos:
                print("📢 Enviando push notification a todos los usuarios...")
                push_results = await send_push_to_all_users(push_notification_data)
            else:
                print(f"📱 Enviando push notification a {len(usuarios_seleccionados)} usuarios específicos...")
                push_results = await send_push_to_users(usuarios_seleccionados, push_notification_data)
            
            print(f"📊 Push notifications: {push_results['sent']} enviadas, {push_results['failed']} fallidas")
            
        except Exception as e:
            print(f"⚠️ Error enviando push notifications (la notificación se creó correctamente): {e}")
            push_results = {"sent": 0, "failed": 0, "results": [], "error": str(e)}
        
        # ==================== FIN PUSH NOTIFICATIONS ====================
        
        return {
            "id": notificacion_id,
            "status": "success",
            "message": "Notificación creada exitosamente",
            "titulo": titulo,
            "enviada_a_todos": enviada_a_todos,
            "usuarios_destinatarios": len(usuarios_seleccionados) if not enviada_a_todos else "todos",
            "tiene_archivo": archivo_nombre is not None,
            "fecha_envio": fecha_envio.isoformat(),
            # Información de push notifications
            "push_notifications": {
                "sent": push_results.get("sent", 0),
                "failed": push_results.get("failed", 0),
                "total_devices": push_results.get("total_devices", 0),
                "error": push_results.get("error", None)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error creando notificación: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear notificación: {str(e)}")

@app.get("/notificaciones")
async def listar_notificaciones(limit: int = 50, offset: int = 0):
    """Listar todas las notificaciones"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"📋 Listando notificaciones (limit: {limit}, offset: {offset})")
        
        # Obtener notificaciones con información de destinatarios
        cursor.execute("""
            SELECT 
                n.id, n.titulo, n.subtitulo, n.descripcion, n.enlace_url,
                n.archivo_nombre, n.archivo_tipo, n.enviada_a_todos,
                n.fecha_creacion, n.fecha_envio,
                CASE 
                    WHEN n.enviada_a_todos THEN 'Todos los usuarios'
                    ELSE (
                        SELECT COUNT(*)::text || ' usuarios seleccionados'
                        FROM notificacion_usuarios nu 
                        WHERE nu.notificacion_id = n.id
                    )
                END as destinatarios_texto
            FROM notificaciones n
            ORDER BY n.fecha_creacion DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))
        
        resultados = cursor.fetchall()
        
        # Obtener total de notificaciones
        cursor.execute("SELECT COUNT(*) FROM notificaciones")
        total = cursor.fetchone()[0]
        
        notificaciones = []
        for row in resultados:
            notificacion = {
                "id": row[0],
                "titulo": row[1],
                "subtitulo": row[2],
                "descripcion": row[3],
                "enlace_url": row[4],
                "archivo_nombre": row[5],
                "archivo_tipo": row[6],
                "enviada_a_todos": row[7],
                "fecha_creacion": row[8].isoformat() if row[8] else None,
                "fecha_envio": row[9].isoformat() if row[9] else None,
                "destinatarios_texto": row[10]
            }
            notificaciones.append(notificacion)
        
        print(f"📋 {len(notificaciones)} notificaciones listadas de {total} totales")
        
        return {
            "notificaciones": notificaciones,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }
        
    except Exception as e:
        print(f"❌ Error listando notificaciones: {e}")
        raise HTTPException(status_code=500, detail=f"Error al listar notificaciones: {str(e)}")

@app.get("/notificaciones/{notificacion_id}")
async def obtener_notificacion(notificacion_id: int):
    """Obtener detalles de una notificación específica"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🔍 Obteniendo notificación {notificacion_id}")
        
        # Obtener notificación
        cursor.execute("""
            SELECT id, titulo, subtitulo, descripcion, enlace_url,
                   archivo_nombre, archivo_tipo, enviada_a_todos,
                   fecha_creacion, fecha_envio
            FROM notificaciones
            WHERE id = %s
        """, (notificacion_id,))
        
        resultado = cursor.fetchone()
        
        if not resultado:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        notificacion = {
            "id": resultado[0],
            "titulo": resultado[1],
            "subtitulo": resultado[2],
            "descripcion": resultado[3],
            "enlace_url": resultado[4],
            "archivo_nombre": resultado[5],
            "archivo_tipo": resultado[6],
            "enviada_a_todos": resultado[7],
            "fecha_creacion": resultado[8].isoformat() if resultado[8] else None,
            "fecha_envio": resultado[9].isoformat() if resultado[9] else None
        }
        
        # Si no es para todos, obtener usuarios específicos
        destinatarios = []
        if not resultado[7]:  # Si enviada_a_todos es False
            cursor.execute("""
                SELECT u.id, u.nombre_completo, u.correo
                FROM notificacion_usuarios nu
                JOIN usuarios u ON nu.usuario_id = u.id
                WHERE nu.notificacion_id = %s
                ORDER BY u.nombre_completo
            """, (notificacion_id,))
            
            usuarios = cursor.fetchall()
            destinatarios = [
                {
                    "id": usuario[0],
                    "nombre_completo": usuario[1],
                    "correo": usuario[2]
                }
                for usuario in usuarios
            ]
        
        notificacion["destinatarios"] = destinatarios
        
        print(f"✅ Notificación {notificacion_id} obtenida exitosamente")
        return notificacion
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error obteniendo notificación: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener notificación: {str(e)}")

@app.get("/notificaciones/{notificacion_id}/archivo")
async def descargar_archivo_notificacion(notificacion_id: int):
    """Descargar o ver el archivo adjunto de una notificación"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"📎 Descargando archivo de notificación {notificacion_id}")
        
        # Obtener archivo de la notificación
        cursor.execute("""
            SELECT archivo, archivo_tipo, archivo_nombre
            FROM notificaciones
            WHERE id = %s AND archivo IS NOT NULL
        """, (notificacion_id,))
        
        resultado = cursor.fetchone()
        
        if not resultado:
            raise HTTPException(status_code=404, detail="Notificación no encontrada o sin archivo adjunto")
        
        archivo_bytes = resultado[0]
        archivo_tipo = resultado[1]
        archivo_nombre = resultado[2]
        
        # Definir Content-Type según el tipo de archivo
        content_types = {
            'imagen': 'image/jpeg',
            'pdf': 'application/pdf',
            'video': 'video/mp4'
        }
        
        content_type = content_types.get(archivo_tipo, 'application/octet-stream')
        
        print(f"📎 Enviando archivo: {archivo_nombre} ({archivo_tipo}, {len(archivo_bytes)} bytes)")
        
        # Crear stream del archivo
        archivo_stream = io.BytesIO(archivo_bytes)
        
        return StreamingResponse(
            io.BytesIO(archivo_bytes),
            media_type=content_type,
            headers={
                "Content-Disposition": f"inline; filename=\"{archivo_nombre}\"",
                "Content-Length": str(len(archivo_bytes))
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error descargando archivo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al descargar archivo: {str(e)}")

@app.delete("/notificaciones/{notificacion_id}")
async def eliminar_notificacion(notificacion_id: int):
    """Eliminar una notificación"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🗑️ Eliminando notificación {notificacion_id}")
        
        # Verificar que la notificación existe
        cursor.execute("SELECT id, titulo FROM notificaciones WHERE id = %s", (notificacion_id,))
        notificacion = cursor.fetchone()
        
        if not notificacion:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        # Eliminar notificación (las relaciones se eliminan automáticamente por CASCADE)
        cursor.execute("DELETE FROM notificaciones WHERE id = %s", (notificacion_id,))
        
        conn.commit()
        
        print(f"✅ Notificación {notificacion_id} eliminada exitosamente")
        
        return {
            "status": "success",
            "message": f"Notificación '{notificacion[1]}' eliminada exitosamente",
            "id": notificacion_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error eliminando notificación: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar notificación: {str(e)}")

@app.get("/notificaciones/usuario/{usuario_id}")
async def obtener_notificaciones_usuario(usuario_id: int, limit: int = 20, offset: int = 0):
    """Obtener notificaciones específicas de un usuario (para PWASUPER)"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"📱 Obteniendo notificaciones para usuario {usuario_id} (limit: {limit}, offset: {offset})")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, nombre_completo FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Obtener notificaciones del usuario (enviadas a todos + específicas del usuario)
        cursor.execute("""
            SELECT DISTINCT n.id, n.titulo, n.subtitulo, n.descripcion, n.enlace_url,
                   n.archivo_nombre, n.archivo_tipo, n.enviada_a_todos,
                   n.fecha_creacion, n.fecha_envio
            FROM notificaciones n
            LEFT JOIN notificacion_usuarios nu ON n.id = nu.notificacion_id
            WHERE n.enviada_a_todos = TRUE 
               OR nu.usuario_id = %s
            ORDER BY n.fecha_creacion DESC
            LIMIT %s OFFSET %s
        """, (usuario_id, limit, offset))
        
        resultados = cursor.fetchall()
        
        # Obtener total de notificaciones del usuario
        cursor.execute("""
            SELECT COUNT(DISTINCT n.id)
            FROM notificaciones n
            LEFT JOIN notificacion_usuarios nu ON n.id = nu.notificacion_id
            WHERE n.enviada_a_todos = TRUE 
               OR nu.usuario_id = %s
        """, (usuario_id,))
        
        total = cursor.fetchone()[0]
        
        notificaciones = []
        for resultado in resultados:
            notificacion = {
                "id": resultado[0],
                "titulo": resultado[1],
                "subtitulo": resultado[2],
                "descripcion": resultado[3],
                "enlace_url": resultado[4],
                "archivo_nombre": resultado[5],
                "archivo_tipo": resultado[6],
                "enviada_a_todos": resultado[7],
                "fecha_creacion": resultado[8].isoformat() if resultado[8] else None,
                "fecha_envio": resultado[9].isoformat() if resultado[9] else None,
                "tiene_archivo": bool(resultado[5])
            }
            notificaciones.append(notificacion)
        
        print(f"✅ {len(notificaciones)} notificaciones obtenidas para usuario {usuario[1]}")
        
        return {
            "usuario": {
                "id": usuario[0],
                "nombre_completo": usuario[1]
            },
            "notificaciones": notificaciones,
            "total": total,
            "limit": limit,
            "offset": offset
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error obteniendo notificaciones del usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener notificaciones del usuario: {str(e)}")

# ==================== FIN ENDPOINTS DE NOTIFICACIONES ====================

# ==================== ENDPOINTS PARA PUSH NOTIFICATIONS ====================

@app.get("/vapid/public-key")
async def get_vapid_public_key():
    """Obtener la clave pública VAPID para suscripciones push"""
    return {
        "public_key": VAPID_KEYS["public_key"]
    }

@app.post("/push/subscribe")
async def subscribe_to_push(subscription: PushSubscription):
    """Suscribir un usuario a push notifications"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"📱 Suscribiendo usuario {subscription.usuario_id} a push notifications...")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT nombre_completo FROM usuarios WHERE id = %s", (subscription.usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar si ya existe una suscripción con el mismo endpoint
        cursor.execute("SELECT id FROM push_subscriptions WHERE endpoint = %s", (subscription.endpoint,))
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar suscripción existente
            cursor.execute("""
                UPDATE push_subscriptions 
                SET usuario_id = %s, p256dh = %s, auth = %s, user_agent = %s, 
                    dispositivo = %s, activa = TRUE, fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE endpoint = %s
                RETURNING id
            """, (
                subscription.usuario_id, subscription.p256dh, subscription.auth,
                subscription.user_agent, subscription.dispositivo, subscription.endpoint
            ))
            subscription_id = cursor.fetchone()[0]
            action = "actualizada"
        else:
            # Crear nueva suscripción
            cursor.execute("""
                INSERT INTO push_subscriptions (
                    usuario_id, endpoint, p256dh, auth, user_agent, dispositivo, activa
                ) VALUES (%s, %s, %s, %s, %s, %s, TRUE)
                RETURNING id
            """, (
                subscription.usuario_id, subscription.endpoint, subscription.p256dh,
                subscription.auth, subscription.user_agent, subscription.dispositivo
            ))
            subscription_id = cursor.fetchone()[0]
            action = "creada"
        
        conn.commit()
        
        print(f"✅ Suscripción {action} exitosamente para {usuario[0]} (ID: {subscription_id})")
        
        return {
            "id": subscription_id,
            "status": "success",
            "message": f"Suscripción {action} exitosamente",
            "usuario": usuario[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error en suscripción push: {e}")
        raise HTTPException(status_code=500, detail=f"Error en suscripción: {str(e)}")

@app.delete("/push/unsubscribe/{usuario_id}")
async def unsubscribe_from_push(usuario_id: int, endpoint: str = None):
    """Cancelar suscripción a push notifications"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🔕 Cancelando suscripciones push para usuario {usuario_id}")
        
        if endpoint:
            # Cancelar suscripción específica por endpoint
            cursor.execute("""
                UPDATE push_subscriptions 
                SET activa = FALSE, fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE usuario_id = %s AND endpoint = %s
                RETURNING id
            """, (usuario_id, endpoint))
        else:
            # Cancelar todas las suscripciones del usuario
            cursor.execute("""
                UPDATE push_subscriptions 
                SET activa = FALSE, fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE usuario_id = %s
                RETURNING id
            """, (usuario_id,))
        
        canceled = cursor.fetchall()
        conn.commit()
        
        if canceled:
            print(f"✅ {len(canceled)} suscripciones canceladas")
            return {
                "status": "success",
                "message": f"{len(canceled)} suscripciones canceladas",
                "canceled_count": len(canceled)
            }
        else:
            raise HTTPException(status_code=404, detail="No se encontraron suscripciones activas")
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error cancelando suscripciones: {e}")
        raise HTTPException(status_code=500, detail=f"Error cancelando suscripciones: {str(e)}")

@app.get("/push/subscriptions/{usuario_id}")
async def get_user_subscriptions(usuario_id: int):
    """Obtener suscripciones activas de un usuario"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        cursor.execute("""
            SELECT id, endpoint, dispositivo, user_agent, fecha_creacion, fecha_actualizacion
            FROM push_subscriptions
            WHERE usuario_id = %s AND activa = TRUE
            ORDER BY fecha_actualizacion DESC
        """, (usuario_id,))
        
        suscripciones = []
        for row in cursor.fetchall():
            suscripciones.append({
                "id": row[0],
                "endpoint": row[1][-50:] + "..." if len(row[1]) > 50 else row[1],  # Truncar para mostrar
                "dispositivo": row[2],
                "user_agent": row[3],
                "fecha_creacion": row[4].isoformat() if row[4] else None,
                "fecha_actualizacion": row[5].isoformat() if row[5] else None
            })
        
        return {
            "usuario_id": usuario_id,
            "suscripciones": suscripciones,
            "total": len(suscripciones)
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo suscripciones: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo suscripciones: {str(e)}")

@app.post("/push/test/{usuario_id}")
async def test_push_notification(usuario_id: int, notification_data: PushNotificationData):
    """Enviar push notification de prueba a un usuario específico"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🧪 Enviando push notification de prueba a usuario {usuario_id}")
        
        # Preparar datos de notificación
        push_data = {
            "title": notification_data.title,
            "body": notification_data.body or "Mensaje de prueba",
            "icon": notification_data.icon or "/pwa-192x192.png",
            "badge": notification_data.badge or "/pwa-192x192.png",
            "tag": notification_data.tag or f"test-{datetime.now().timestamp()}",
            "data": notification_data.data or {"test": True, "timestamp": datetime.now().timestamp()},
            "vibrate": notification_data.vibrate or [200, 100, 200],
            "requireInteraction": notification_data.requireInteraction
        }
        
        # Enviar push notification
        result = await send_push_to_users([usuario_id], push_data)
        
        return {
            "status": "success",
            "message": "Push notification de prueba enviada",
            "result": result
        }
        
    except Exception as e:
        print(f"❌ Error enviando push de prueba: {e}")
        raise HTTPException(status_code=500, detail=f"Error enviando push de prueba: {str(e)}")

# ==================== FIN ENDPOINTS PUSH NOTIFICATIONS ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
