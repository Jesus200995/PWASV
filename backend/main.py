from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext
import os
import re
import bcrypt
import pytz
from typing import Optional, List, Dict, Any
import json
from pywebpush import webpush, WebPushException

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

# Modelos para notificaciones
class NotificationCreate(BaseModel):
    title: str
    body: str
    type: str = "info"  # info | warning | success | urgent
    audience: str       # all | segment | users
    users: Optional[List[int]] = None  # Para audience="users"
    scheduled_at: Optional[str] = None  # ISO timestamp
    metadata: Optional[Dict[str, Any]] = None

class NotificationRead(BaseModel):
    user_id: int
    notification_id: int

class DeviceSubscription(BaseModel):
    user_id: int
    endpoint: str
    keys: Dict[str, str]  # p256dh y auth
    ua: Optional[str] = None

# Montar carpeta de fotos para servir estáticamente
app.mount("/fotos", StaticFiles(directory="fotos"), name="fotos")

# ==================== FUNCIONES DE UTILIDAD PARA NOTIFICACIONES ====================

def crear_tablas_notificaciones():
    """Crear las tablas necesarias para el sistema de notificaciones"""
    try:
        if not conn:
            print("❌ No hay conexión a la base de datos para crear tablas")
            return
        
        # Tabla maestro de notificaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id               SERIAL PRIMARY KEY,
                title            VARCHAR(150) NOT NULL,
                body             TEXT NOT NULL,
                type             VARCHAR(30) DEFAULT 'info',
                audience         VARCHAR(30) NOT NULL,
                metadata         JSONB DEFAULT '{}'::jsonb,
                status           VARCHAR(20) NOT NULL DEFAULT 'draft',
                created_by       INTEGER,
                created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                scheduled_at     TIMESTAMPTZ,
                sent_at          TIMESTAMPTZ
            )
        """)
        
        # Índices para notificaciones
        cursor.execute("CREATE INDEX IF NOT EXISTS notifications_status_idx ON notifications(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS notifications_sched_idx ON notifications(scheduled_at)")
        
        # Tabla de destinatarios específicos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notification_targets (
                id               SERIAL PRIMARY KEY,
                notification_id  INTEGER NOT NULL REFERENCES notifications(id) ON DELETE CASCADE,
                user_id          INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        
        # Índices para targets
        cursor.execute("CREATE INDEX IF NOT EXISTS notification_targets_notif_idx ON notification_targets(notification_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS notification_targets_user_idx ON notification_targets(user_id)")
        
        # Tabla de lecturas por usuario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notification_reads (
                id               SERIAL PRIMARY KEY,
                notification_id  INTEGER NOT NULL REFERENCES notifications(id) ON DELETE CASCADE,
                user_id          INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                read_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE(notification_id, user_id)
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS notification_reads_user_idx ON notification_reads(user_id)")
        
        # Tabla de suscripciones Web Push
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_devices (
                id               SERIAL PRIMARY KEY,
                user_id          INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                endpoint         TEXT NOT NULL,
                p256dh           TEXT NOT NULL,
                auth             TEXT NOT NULL,
                ua               TEXT,
                subscribed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                last_seen_at     TIMESTAMPTZ,
                UNIQUE(endpoint)
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS user_devices_user_idx ON user_devices(user_id)")
        
        conn.commit()
        print("✅ Tablas de notificaciones creadas exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando tablas de notificaciones: {e}")
        if conn:
            conn.rollback()

def enviar_notificacion_push(notification_id: int):
    """Enviar notificación push a todos los dispositivos del público objetivo"""
    try:
        print(f"🔔 Enviando notificación push para ID: {notification_id}")
        
        # Obtener la notificación
        cursor.execute("""
            SELECT id, title, body, type, audience, metadata, status
            FROM notifications 
            WHERE id = %s
        """, (notification_id,))
        
        notification = cursor.fetchone()
        if not notification:
            print(f"❌ Notificación {notification_id} no encontrada")
            return False
        
        # Verificar que esté lista para envío
        if notification[6] not in ['scheduled', 'draft']:  # status
            print(f"❌ Notificación {notification_id} tiene status {notification[6]}, no se puede enviar")
            return False
        
        # Actualizar status a 'sending'
        cursor.execute("UPDATE notifications SET status = 'sending' WHERE id = %s", (notification_id,))
        conn.commit()
        
        # Obtener dispositivos según el público objetivo
        if notification[4] == 'all':  # audience
            cursor.execute("""
                SELECT DISTINCT ud.endpoint, ud.p256dh, ud.auth, ud.user_id
                FROM user_devices ud
                JOIN usuarios u ON ud.user_id = u.id
            """)
        elif notification[4] == 'users':
            cursor.execute("""
                SELECT DISTINCT ud.endpoint, ud.p256dh, ud.auth, ud.user_id
                FROM user_devices ud
                JOIN notification_targets nt ON ud.user_id = nt.user_id
                WHERE nt.notification_id = %s
            """, (notification_id,))
        else:
            print(f"❌ Tipo de audiencia {notification[4]} no soportado")
            return False
        
        devices = cursor.fetchall()
        
        if not devices:
            print(f"⚠️ No hay dispositivos registrados para la audiencia {notification[4]}")
            cursor.execute("UPDATE notifications SET status = 'sent', sent_at = NOW() WHERE id = %s", (notification_id,))
            conn.commit()
            return True
        
        # Preparar payload de la notificación
        payload = {
            "title": notification[1],  # title
            "body": notification[2],   # body
            "type": notification[3],   # type
            "data": {
                "notification_id": notification[0],
                "metadata": notification[5] or {}
            }
        }
        
        # Enviar a cada dispositivo
        successful_sends = 0
        failed_sends = 0
        endpoints_to_remove = []
        
        for device in devices:
            try:
                endpoint, p256dh, auth, user_id = device
                
                webpush(
                    subscription_info={
                        "endpoint": endpoint,
                        "keys": {
                            "p256dh": p256dh,
                            "auth": auth
                        }
                    },
                    data=json.dumps(payload),
                    vapid_private_key=VAPID_PRIVATE_KEY,
                    vapid_claims={
                        "sub": VAPID_SUBJECT
                    }
                )
                
                successful_sends += 1
                print(f"✅ Push enviado a usuario {user_id}")
                
            except WebPushException as e:
                failed_sends += 1
                print(f"❌ Error enviando push a usuario {user_id}: {e}")
                
                # Si el endpoint es inválido, marcarlo para eliminación
                if e.response and e.response.status_code in [400, 404, 410]:
                    endpoints_to_remove.append(endpoint)
                    
            except Exception as e:
                failed_sends += 1
                print(f"❌ Error general enviando push a usuario {user_id}: {e}")
        
        # Eliminar endpoints inválidos
        for endpoint in endpoints_to_remove:
            try:
                cursor.execute("DELETE FROM user_devices WHERE endpoint = %s", (endpoint,))
                print(f"🗑️ Endpoint inválido eliminado: {endpoint}")
            except Exception as e:
                print(f"⚠️ Error eliminando endpoint {endpoint}: {e}")
        
        # Actualizar status final
        cursor.execute("""
            UPDATE notifications 
            SET status = 'sent', sent_at = NOW() 
            WHERE id = %s
        """, (notification_id,))
        
        conn.commit()
        
        print(f"✅ Notificación {notification_id} enviada: {successful_sends} éxitos, {failed_sends} fallos")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando notificación push {notification_id}: {e}")
        # Revertir status a draft en caso de error crítico
        cursor.execute("UPDATE notifications SET status = 'failed' WHERE id = %s", (notification_id,))
        conn.commit()
        return False

# Inicializar tablas de notificaciones al arrancar
crear_tablas_notificaciones()

# Configuración para autenticación JWT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "cambia-esto-por-una-clave-muy-larga-y-unica-para-admin-2025"

# Configuración VAPID para Web Push
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY", "BKyQWjwbVU_gE9CUPTq8qyUdOhW_sEm3Dq4cUW9lq3CylRzrM_g6HJ8vWb9qU7mP")
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY", "BBFowQQqtRsHr5W0CrRO4J-1TwNEt0vXDBJq1Gf3iOJYHnIxNLZ5nJG0BvSqYmVy")
VAPID_SUBJECT = os.getenv("VAPID_SUBJECT", "mailto:admin@sembrandodatos.com")
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE", "America/Mexico_City"))

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

# ==================== ENDPOINTS DE NOTIFICACIONES ====================

@app.post("/notifications")
async def crear_notificacion(notification: NotificationCreate):
    """Crear una nueva notificación"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"📝 Creando notificación: {notification.title}")
        
        # Validar audiencia
        if notification.audience not in ['all', 'users']:
            raise HTTPException(status_code=400, detail="Audiencia debe ser 'all' o 'users'")
        
        # Si es para usuarios específicos, validar que se proporcionen IDs
        if notification.audience == 'users' and not notification.users:
            raise HTTPException(status_code=400, detail="Debe proporcionar users para audiencia 'users'")
        
        # Crear la notificación
        cursor.execute("""
            INSERT INTO notifications (title, body, type, audience, metadata, status, created_by, scheduled_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            notification.title,
            notification.body,
            notification.type,
            notification.audience,
            json.dumps(notification.metadata) if notification.metadata else None,
            'draft',  # Status por defecto
            None,     # created_by por defecto
            notification.scheduled_at
        ))
        
        notification_id = cursor.fetchone()[0]
        
        # Si es para usuarios específicos, crear targets
        if notification.audience == 'users' and notification.users:
            for user_id in notification.users:
                cursor.execute("""
                    INSERT INTO notification_targets (notification_id, user_id)
                    VALUES (%s, %s)
                """, (notification_id, user_id))
        
        conn.commit()
        
        # Si el status es 'scheduled' o 'sent', enviar inmediatamente
        # if notification.status in ['scheduled', 'sent']:
        #     enviar_notificacion_push(notification_id)
        
        print(f"✅ Notificación {notification_id} creada exitosamente")
        return {"id": notification_id, "status": "created"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error creando notificación: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error creando notificación: {str(e)}")

@app.get("/notifications")
async def listar_notificaciones(
    status: str = None,
    type: str = None,
    limit: int = 50,
    offset: int = 0,
    search: str = None
):
    """Listar notificaciones con filtros opcionales"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Construir query base
        conditions = []
        params = []
        
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        if type:
            conditions.append("type = %s")
            params.append(type)
        
        if search:
            conditions.append("(title ILIKE %s OR body ILIKE %s)")
            params.extend([f"%{search}%", f"%{search}%"])
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        
        # Query principal
        cursor.execute(f"""
            SELECT 
                id, title, body, type, audience, metadata, status,
                created_by, created_at, scheduled_at, sent_at
            FROM notifications
            {where_clause}
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, params + [limit, offset])
        
        notifications = []
        for row in cursor.fetchall():
            # Obtener estadísticas de cada notificación
            cursor.execute("""
                SELECT 
                    (CASE WHEN n.audience = 'all' 
                        THEN (SELECT COUNT(*) FROM usuarios)
                        ELSE (SELECT COUNT(*) FROM notification_targets WHERE notification_id = %s)
                    END) as total_recipients,
                    (SELECT COUNT(*) FROM notification_reads WHERE notification_id = %s) as total_reads
            """, (row[0], row[0]))
            
            stats = cursor.fetchone()
            
            notifications.append({
                "id": row[0],
                "title": row[1],
                "body": row[2],
                "type": row[3],
                "audience": row[4],
                "metadata": row[5] if row[5] else {},
                "status": row[6],
                "created_by": row[7],
                "created_at": row[8].isoformat() if row[8] else None,
                "scheduled_at": row[9].isoformat() if row[9] else None,
                "sent_at": row[10].isoformat() if row[10] else None,
                "stats": {
                    "total_recipients": stats[0] or 0,
                    "total_reads": stats[1] or 0,
                    "read_rate": round((stats[1] / stats[0] * 100) if stats[0] > 0 else 0, 2)
                }
            })
        
        # Obtener total de registros
        cursor.execute(f"""
            SELECT COUNT(*) FROM notifications {where_clause}
        """, params)
        
        total = cursor.fetchone()[0]
        
        return {
            "notifications": notifications,
            "total": total,
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        print(f"❌ Error listando notificaciones: {e}")
        raise HTTPException(status_code=500, detail=f"Error listando notificaciones: {str(e)}")

@app.get("/notifications/{notification_id}")
async def obtener_notificacion(notification_id: int):
    """Obtener detalles de una notificación específica"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Obtener la notificación
        cursor.execute("""
            SELECT 
                id, title, body, type, audience, metadata, status,
                created_by, created_at, scheduled_at, sent_at
            FROM notifications
            WHERE id = %s
        """, (notification_id,))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        # Obtener destinatarios si es para usuarios específicos
        recipients = []
        if row[4] == 'users':  # audience
            cursor.execute("""
                SELECT u.id, u.nombre_completo, u.correo
                FROM notification_targets nt
                JOIN usuarios u ON nt.user_id = u.id
                WHERE nt.notification_id = %s
            """, (notification_id,))
            
            recipients = [
                {
                    "id": r[0],
                    "nombre_completo": r[1],
                    "correo": r[2]
                }
                for r in cursor.fetchall()
            ]
        
        # Obtener estadísticas de lectura
        cursor.execute("""
            SELECT 
                u.id, u.nombre_completo, u.correo, nr.read_at
            FROM notification_reads nr
            JOIN usuarios u ON nr.user_id = u.id
            WHERE nr.notification_id = %s
            ORDER BY nr.read_at DESC
        """, (notification_id,))
        
        reads = [
            {
                "user_id": r[0],
                "nombre_completo": r[1],
                "correo": r[2],
                "read_at": r[3].isoformat() if r[3] else None
            }
            for r in cursor.fetchall()
        ]
        
        return {
            "id": row[0],
            "title": row[1],
            "body": row[2],
            "type": row[3],
            "audience": row[4],
            "metadata": row[5] if row[5] else {},
            "status": row[6],
            "created_by": row[7],
            "created_at": row[8].isoformat() if row[8] else None,
            "scheduled_at": row[9].isoformat() if row[9] else None,
            "sent_at": row[10].isoformat() if row[10] else None,
            "recipients": recipients,
            "reads": reads,
            "stats": {
                "total_recipients": len(recipients) if recipients else 0,
                "total_reads": len(reads),
                "read_rate": round((len(reads) / len(recipients) * 100) if recipients else 0, 2)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error obteniendo notificación {notification_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo notificación: {str(e)}")

@app.post("/notifications/{notification_id}/send")
async def enviar_notificacion(notification_id: int):
    """Enviar una notificación específica"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Verificar que la notificación existe y se puede enviar
        cursor.execute("SELECT status FROM notifications WHERE id = %s", (notification_id,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        if result[0] not in ['draft', 'scheduled']:
            raise HTTPException(status_code=400, detail=f"No se puede enviar notificación con status: {result[0]}")
        
        # Enviar notificación
        success = enviar_notificacion_push(notification_id)
        
        if success:
            return {"status": "sent", "message": "Notificación enviada exitosamente"}
        else:
            raise HTTPException(status_code=500, detail="Error enviando la notificación")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error enviando notificación {notification_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error enviando notificación: {str(e)}")

@app.delete("/notifications/{notification_id}")
async def eliminar_notificacion(notification_id: int):
    """Eliminar una notificación"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Verificar que existe
        cursor.execute("SELECT id FROM notifications WHERE id = %s", (notification_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        # Eliminar (cascade se encarga de targets y reads)
        cursor.execute("DELETE FROM notifications WHERE id = %s", (notification_id,))
        conn.commit()
        
        print(f"✅ Notificación {notification_id} eliminada exitosamente")
        return {"status": "deleted", "message": "Notificación eliminada exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error eliminando notificación {notification_id}: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error eliminando notificación: {str(e)}")

@app.post("/notifications/{notification_id}/read")
async def marcar_como_leida(notification_id: int, user_id: int):
    """Marcar una notificación como leída por un usuario"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Insertar registro de lectura (ON CONFLICT para evitar duplicados)
        cursor.execute("""
            INSERT INTO notification_reads (notification_id, user_id)
            VALUES (%s, %s)
            ON CONFLICT (notification_id, user_id) DO NOTHING
        """, (notification_id, user_id))
        
        conn.commit()
        return {"status": "marked_read", "message": "Notificación marcada como leída"}
        
    except Exception as e:
        print(f"❌ Error marcando notificación como leída: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error marcando como leída: {str(e)}")

# ==================== ENDPOINTS DE WEB PUSH ====================

@app.post("/push/subscribe")
async def suscribir_dispositivo(subscription: DeviceSubscription):
    """Registrar una nueva suscripción de dispositivo para Web Push"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"📱 Registrando suscripción para usuario: {subscription.user_id}")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (subscription.user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Insertar o actualizar suscripción
        cursor.execute("""
            INSERT INTO user_devices (user_id, endpoint, p256dh, auth, ua, last_seen_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            ON CONFLICT (endpoint) 
            DO UPDATE SET 
                user_id = EXCLUDED.user_id,
                p256dh = EXCLUDED.p256dh,
                auth = EXCLUDED.auth,
                ua = EXCLUDED.ua,
                last_seen_at = NOW()
            RETURNING id
        """, (
            subscription.user_id,
            subscription.endpoint,
            subscription.p256dh,
            subscription.auth,
            subscription.user_agent
        ))
        
        device_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ Dispositivo {device_id} registrado para usuario {subscription.user_id}")
        return {"status": "subscribed", "device_id": device_id}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error registrando suscripción: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error registrando suscripción: {str(e)}")

@app.post("/push/unsubscribe")
async def desuscribir_dispositivo(endpoint: str):
    """Eliminar una suscripción de dispositivo"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        cursor.execute("DELETE FROM user_devices WHERE endpoint = %s", (endpoint,))
        deleted_count = cursor.rowcount
        conn.commit()
        
        if deleted_count > 0:
            print(f"✅ Dispositivo con endpoint {endpoint[:50]}... desuscrito")
            return {"status": "unsubscribed"}
        else:
            return {"status": "not_found", "message": "Endpoint no encontrado"}
        
    except Exception as e:
        print(f"❌ Error desuscribiendo dispositivo: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error desuscribiendo: {str(e)}")

@app.get("/push/test/{user_id}")
async def test_notificacion_push(user_id: int):
    """Enviar notificación de prueba a un usuario específico"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Crear notificación de prueba
        cursor.execute("""
            INSERT INTO notifications (title, body, type, audience, status, created_by)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            "Notificación de Prueba",
            "Esta es una notificación de prueba del sistema PWA",
            "info",
            "users",
            "sent",
            None
        ))
        
        notification_id = cursor.fetchone()[0]
        
        # Añadir target específico
        cursor.execute("""
            INSERT INTO notification_targets (notification_id, user_id)
            VALUES (%s, %s)
        """, (notification_id, user_id))
        
        conn.commit()
        
        # Enviar notificación
        success = enviar_notificacion_push(notification_id)
        
        if success:
            return {"status": "sent", "notification_id": notification_id}
        else:
            raise HTTPException(status_code=500, detail="Error enviando notificación de prueba")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en notificación de prueba: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error en prueba: {str(e)}")

@app.get("/notifications/stats")
async def estadisticas_notificaciones():
    """Obtener estadísticas generales del sistema de notificaciones"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Estadísticas generales
        cursor.execute("""
            SELECT 
                COUNT(*) as total_notifications,
                COUNT(CASE WHEN status = 'sent' THEN 1 END) as sent_notifications,
                COUNT(CASE WHEN status = 'draft' THEN 1 END) as draft_notifications,
                COUNT(CASE WHEN status = 'scheduled' THEN 1 END) as scheduled_notifications
            FROM notifications
        """)
        
        stats = cursor.fetchone()
        
        # Dispositivos registrados
        cursor.execute("SELECT COUNT(*) FROM user_devices")
        total_devices = cursor.fetchone()[0]
        
        # Notificaciones por tipo
        cursor.execute("""
            SELECT type, COUNT(*) 
            FROM notifications 
            GROUP BY type
            ORDER BY COUNT(*) DESC
        """)
        
        by_type = [{"type": row[0], "count": row[1]} for row in cursor.fetchall()]
        
        # Actividad reciente (últimos 7 días)
        cursor.execute("""
            SELECT 
                DATE(created_at) as fecha,
                COUNT(*) as cantidad
            FROM notifications
            WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY DATE(created_at)
            ORDER BY fecha DESC
        """)
        
        activity = [
            {
                "fecha": row[0].isoformat() if row[0] else None,
                "cantidad": row[1]
            }
            for row in cursor.fetchall()
        ]
        
        return {
            "general": {
                "total_notifications": stats[0] or 0,
                "sent_notifications": stats[1] or 0,
                "draft_notifications": stats[2] or 0,
                "scheduled_notifications": stats[3] or 0,
                "total_devices": total_devices or 0
            },
            "by_type": by_type,
            "recent_activity": activity
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

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
