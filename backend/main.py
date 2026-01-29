from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse, HTMLResponse
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

app = FastAPI()

# Permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003", "http://127.0.0.1:3003", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Configuración para autenticación JWT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "cambia-esto-por-una-clave-muy-larga-y-unica-para-admin-2025"

# Conexión a PostgreSQL con manejo robusto
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

# Variables globales para la conexión
conn = None
cursor = None

def conectar_base_datos():
    """Función para establecer/reestablecer conexión a la base de datos"""
    global conn, cursor
    try:
        if conn:
            conn.close()
        
        conn = psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS,
            # Configuraciones para mejor manejo de conexiones
            connect_timeout=10,
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=5,
            keepalives_count=5
        )
        cursor = conn.cursor()
        print("✅ Conexión a la base de datos exitosa")
        return True
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        conn = None
        cursor = None
        return False

def verificar_conexion_db():
    """Verificar y reestablecer conexión si es necesario"""
    global conn, cursor
    try:
        if not conn or conn.closed:
            print("🔄 Reestableciendo conexión cerrada...")
            return conectar_base_datos()
        
        # Test de conexión simple
        cursor.execute("SELECT 1")
        cursor.fetchone()
        return True
    except (psycopg2.Error, psycopg2.OperationalError, AttributeError):
        print("🔄 Conexión perdida, reestableciendo...")
        return conectar_base_datos()

def ejecutar_consulta_segura(query, params=None, fetch_type='all'):
    """Ejecutar consulta con manejo robusto de errores y reconexión"""
    global conn, cursor
    max_reintentos = 3
    
    for intento in range(1, max_reintentos + 1):
        try:
            # Verificar conexión antes de ejecutar
            if not verificar_conexion_db():
                raise HTTPException(status_code=500, detail="No se pudo establecer conexión a la base de datos")
            
            # Ejecutar la consulta
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Obtener resultados según el tipo
            if fetch_type == 'one':
                result = cursor.fetchone()
            elif fetch_type == 'all':
                result = cursor.fetchall()
            else:  # fetch_type == 'none' para INSERT/UPDATE/DELETE
                result = None
            
            # Commit si es necesario
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                conn.commit()
            
            return result
            
        except psycopg2.Error as e:
            print(f"❌ Error de PostgreSQL en intento {intento}: {e}")
            
            # Hacer rollback para limpiar la transacción corrupta
            try:
                if conn and not conn.closed:
                    conn.rollback()
                    print("🔄 Rollback ejecutado para limpiar transacción")
            except Exception as rollback_error:
                print(f"⚠️ Error en rollback: {rollback_error}")
            
            if intento == max_reintentos:
                raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
            
            # Intentar reconectar para el siguiente intento
            conectar_base_datos()
            
        except Exception as e:
            print(f"❌ Error general en intento {intento}: {e}")
            
            # Hacer rollback también para errores generales
            try:
                if conn and not conn.closed:
                    conn.rollback()
                    print("🔄 Rollback ejecutado para error general")
            except Exception as rollback_error:
                print(f"⚠️ Error en rollback: {rollback_error}")
            
            if intento == max_reintentos:
                raise HTTPException(status_code=500, detail=f"Error al ejecutar consulta: {str(e)}")

# Establecer conexión inicial
try:
    conectar_base_datos()
    
    # Crear tabla admin_users si no existe
    ejecutar_consulta_segura("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            rol VARCHAR(20) DEFAULT 'admin' CHECK (rol IN ('admin', 'user')),
            activo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """, fetch_type='none')
    
    # Verificar si existen usuarios admin, si no crear uno por defecto
    count_result = ejecutar_consulta_segura("SELECT COUNT(*) FROM admin_users", fetch_type='one')
    count = count_result[0] if count_result else 0
    
    if count == 0:
        # Crear usuario admin por defecto
        default_password = pwd_context.hash("admin123")
        ejecutar_consulta_segura(
            "INSERT INTO admin_users (username, password, rol) VALUES (%s, %s, %s)",
            ("admin", default_password, "admin"),
            fetch_type='none'
        )
        print("✅ Usuario administrador por defecto creado: admin/admin123")
    
    # ===== MIGRACIÓN: Agregar columna permisos a tabla admin_users =====
    try:
        ejecutar_consulta_segura("""
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'admin_users' AND column_name = 'permisos'
                ) THEN
                    ALTER TABLE admin_users ADD COLUMN permisos TEXT DEFAULT NULL;
                    RAISE NOTICE 'Columna permisos agregada a admin_users';
                END IF;
            END $$;
        """, fetch_type='none')
        print("✅ Migración de columna permisos verificada")
    except Exception as e:
        print(f"⚠️ Error en migración de permisos: {e}")
    
    # ===== MIGRACIÓN: Agregar columna activo a tabla admin_users =====
    try:
        ejecutar_consulta_segura("""
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'admin_users' AND column_name = 'activo'
                ) THEN
                    ALTER TABLE admin_users ADD COLUMN activo BOOLEAN DEFAULT TRUE;
                    RAISE NOTICE 'Columna activo agregada a admin_users';
                END IF;
            END $$;
        """, fetch_type='none')
        print("✅ Migración de columna activo verificada")
    except Exception as e:
        print(f"⚠️ Error en migración de activo: {e}")
    
    # ===== MIGRACIÓN: Agregar columnas es_territorial y territorio a tabla admin_users =====
    try:
        ejecutar_consulta_segura("""
            DO $$ 
            BEGIN
                -- Agregar columna es_territorial
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'admin_users' AND column_name = 'es_territorial'
                ) THEN
                    ALTER TABLE admin_users ADD COLUMN es_territorial BOOLEAN DEFAULT FALSE;
                    RAISE NOTICE 'Columna es_territorial agregada a admin_users';
                END IF;
                
                -- Agregar columna territorio
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'admin_users' AND column_name = 'territorio'
                ) THEN
                    ALTER TABLE admin_users ADD COLUMN territorio VARCHAR(100) DEFAULT NULL;
                    RAISE NOTICE 'Columna territorio agregada a admin_users';
                END IF;
            END $$;
        """, fetch_type='none')
        print("✅ Migración de columnas es_territorial y territorio verificada")
    except Exception as e:
        print(f"⚠️ Error en migración de es_territorial/territorio: {e}")
    
    # ===== MIGRACIÓN: Agregar columnas categoria_actividad a tabla registros =====
    try:
        # Verificar si la columna categoria_actividad existe
        ejecutar_consulta_segura("""
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'registros' AND column_name = 'categoria_actividad'
                ) THEN
                    ALTER TABLE registros ADD COLUMN categoria_actividad VARCHAR(100);
                    RAISE NOTICE 'Columna categoria_actividad agregada a registros';
                END IF;
                
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'registros' AND column_name = 'categoria_actividad_otro'
                ) THEN
                    ALTER TABLE registros ADD COLUMN categoria_actividad_otro VARCHAR(255);
                    RAISE NOTICE 'Columna categoria_actividad_otro agregada a registros';
                END IF;
            END $$;
        """, fetch_type='none')
        print("✅ Verificación de columnas categoria_actividad completada")
    except Exception as migration_error:
        print(f"⚠️ Advertencia en migración de categoria_actividad: {migration_error}")
    
    # ===== MIGRACIÓN: Agregar columna territorio a tabla usuarios =====
    try:
        ejecutar_consulta_segura("""
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'usuarios' AND column_name = 'territorio'
                ) THEN
                    ALTER TABLE usuarios ADD COLUMN territorio VARCHAR(100) DEFAULT NULL;
                    RAISE NOTICE 'Columna territorio agregada a usuarios';
                END IF;
            END $$;
        """, fetch_type='none')
        print("✅ Migración de columna territorio verificada")
    except Exception as e:
        print(f"⚠️ Error en migración de territorio: {e}")
    
except Exception as e:
    print(f"❌ Error en inicialización de base de datos: {e}")
    conn = None
    cursor = None

# Carpeta para guardar fotos
FOTOS_DIR = "fotos"
os.makedirs(FOTOS_DIR, exist_ok=True)

# ==================== ENDPOINT DE SALUD ====================

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la API y la base de datos"""
    try:
        # Verificar conexión a la base de datos
        if not verificar_conexion_db():
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "message": "No se pudo conectar a la base de datos",
                "timestamp": datetime.now().isoformat()
            }
        
        # Prueba simple de consulta
        test_result = ejecutar_consulta_segura("SELECT 1 as test", fetch_type='one')
        
        if test_result and test_result[0] == 1:
            return {
                "status": "healthy",
                "database": "connected",
                "message": "API y base de datos funcionando correctamente",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "unhealthy", 
                "database": "error",
                "message": "Error en consulta de prueba",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "message": f"Error en health check: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# ==================== FIN ENDPOINT DE SALUD ====================

# Modelos para autenticación
class UserCreate(BaseModel):
    correo: str
    nombre_completo: str
    cargo: str
    supervisor: str = None
    contrasena: str
    curp: str  # CURP obligatoria
    telefono: str  # Teléfono obligatorio
    territorio: str = None  # Estado de México (opcional pero recomendado)
    rol: str = 'user'  # Rol por defecto es user

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
    territorio: str = None

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

class NotificacionLeer(BaseModel):
    usuario_id: int
    device_id: Optional[str] = None

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

# ==================== FIN MODELOS NOTIFICACIONES ====================

# Montar carpeta de fotos para servir estáticamente
app.mount("/fotos", StaticFiles(directory="fotos"), name="fotos")

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
    """Crear usuario con rol y automáticamente registrar aceptación de términos"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
            
        print(f"👤 Creando usuario: {usuario.correo} con rol {usuario.rol}")
        
        # Validación de rol
        if usuario.rol not in ['admin', 'user']:
            raise HTTPException(status_code=400, detail="Rol inválido. Debe ser 'admin' o 'user'")
        
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
        
        # Validación de territorio (estado de México)
        territorio_value = None
        if usuario.territorio and usuario.territorio.strip():
            territorio_value = usuario.territorio.strip()
            print(f"📍 Territorio asignado: {territorio_value}")
        
        # Comprobar si el correo ya existe
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (usuario.correo,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        
        # Comprobar si la CURP ya existe
        cursor.execute("SELECT id FROM usuarios WHERE curp = %s", (curp_upper,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="La CURP ya está registrada")
        
        # Verificar si la columna 'rol' existe, si no, agregarla
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'usuarios' AND column_name = 'rol'
        """)
        
        if not cursor.fetchone():
            print("📝 Agregando columna 'rol' a la tabla usuarios")
            cursor.execute("ALTER TABLE usuarios ADD COLUMN rol VARCHAR(10) DEFAULT 'user'")
            conn.commit()
        
        # Insertar usuario con CURP, teléfono, territorio y rol (contraseña sin encriptar)
        cursor.execute(
            "INSERT INTO usuarios (correo, nombre_completo, cargo, supervisor, contrasena, curp, telefono, territorio, rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (usuario.correo, usuario.nombre_completo, usuario.cargo, usuario.supervisor, usuario.contrasena, curp_upper, usuario.telefono, territorio_value, usuario.rol)
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

# ==================== ENDPOINTS DE HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Endpoint para verificar la salud del servidor"""
    try:
        if not verificar_conexion_db():
            return {"status": "warning", "message": "Servidor en línea pero sin conexión a base de datos"}
        return {"status": "ok", "message": "Servidor en línea y conectado a base de datos"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.options("/{path:path}")
async def preflight(path: str):
    """Manejar solicitudes CORS preflight"""
    return {"message": "OK"}

@app.post("/login")
async def login(usuario: UserLogin):
    # Buscar usuario por correo incluyendo territorio, curp y supervisor
    cursor.execute("SELECT id, correo, nombre_completo, cargo, contrasena, territorio, curp, supervisor FROM usuarios WHERE correo = %s", (usuario.correo,))
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
        "cargo": user[3],
        "territorio": user[5] if len(user) > 5 else None,
        "curp": user[6] if len(user) > 6 else None,
        "supervisor": user[7] if len(user) > 7 else None
    }

# ==================== ENDPOINT PARA VERIFICAR CONTRASEÑA ====================

@app.post("/verificar_contrasena")
async def verificar_contrasena(datos: dict):
    """Verifica si la contraseña actual es correcta"""
    try:
        usuario_id = datos.get('usuario_id')
        contrasena = datos.get('contrasena')
        
        if not usuario_id or not contrasena:
            raise HTTPException(status_code=400, detail="usuario_id y contrasena son obligatorios")
        
        # Verificar que el usuario existe y obtener su contraseña
        cursor.execute("SELECT id, contrasena FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Comparar contraseña (sin encriptación, verificar si está encriptada primero)
        contrasena_almacenada = usuario[1]
        
        # Intentar comparar directamente primero (por si no está encriptada)
        if contrasena == contrasena_almacenada:
            return {"success": True, "message": "Contraseña verificada"}
        
        # Si no coincide, intentar con bcrypt (por si está encriptada)
        try:
            if bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_almacenada.encode('utf-8')):
                return {"success": True, "message": "Contraseña verificada"}
        except Exception:
            pass
        
        # Contraseña incorrecta
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al verificar contraseña: {e}")
        raise HTTPException(status_code=500, detail=f"Error al verificar contraseña: {str(e)}")

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
    tipo_actividad: str = Form("campo"),  # Campo con valor por defecto para compatibilidad con registros offline antiguos
    categoria_actividad: str = Form(""),  # Campo con valor vacío por defecto para compatibilidad
    categoria_actividad_otro: str = Form(None),  # Campo opcional: especificación cuando se selecciona "Otro"
    foto: UploadFile = File(...),
    timestamp_offline: str = Form(None)  # Nuevo campo opcional para registro offline
):
    print(f"🔍 REGISTRO - Datos recibidos:")
    print(f"   usuario_id: {usuario_id}")
    print(f"   latitud: {latitud}")
    print(f"   longitud: {longitud}")
    print(f"   descripcion: {descripcion}")
    print(f"   tipo_actividad: {tipo_actividad}")
    print(f"   categoria_actividad: {categoria_actividad}")
    print(f"   categoria_actividad_otro: {categoria_actividad_otro}")
    print(f"   foto: {foto.filename}")
    print(f"   timestamp_offline: {timestamp_offline}")
    
    # Validar y corregir tipo de actividad con valor por defecto
    if not tipo_actividad or tipo_actividad not in ['campo', 'gabinete']:
        print(f"⚠️ tipo_actividad inválido o vacío ('{tipo_actividad}'), usando valor por defecto 'campo'")
        tipo_actividad = 'campo'
    
    # Validar categoría de actividad
    categorias_validas = [
        'Acompañamiento técnico',
        'Productivas directas',
        'Ahorro y trámites financieros',
        'Capacitación / talleres / cursos',
        'Difusión y comunicación',
        'Eventos comunitarios / ferias / tianguis',
        'Reuniones y asambleas',
        'Trabajo administrativo y captura',
        'Viveros y biofábricas',
        'Otro'
    ]
    
    # MEJORA: Asignar valor por defecto si categoria_actividad está vacía o es inválida
    if not categoria_actividad or categoria_actividad not in categorias_validas:
        # Inferir categoría basada en tipo de actividad
        if tipo_actividad == 'gabinete':
            categoria_actividad_default = 'Trabajo administrativo y captura'
        else:
            categoria_actividad_default = 'Acompañamiento técnico'
        print(f"⚠️ categoria_actividad inválida o vacía ('{categoria_actividad}'), usando valor por defecto '{categoria_actividad_default}'")
        categoria_actividad = categoria_actividad_default
    
    # Si la categoría es "Otro", se requiere especificación
    if categoria_actividad == 'Otro' and not categoria_actividad_otro:
        raise HTTPException(status_code=400, detail="Cuando categoria_actividad es 'Otro', se requiere especificar en categoria_actividad_otro")
    
    print(f"✅ Categoría de actividad válida: {categoria_actividad}" + (f" (Otro: {categoria_actividad_otro})" if categoria_actividad == 'Otro' else ""))
    
    print(f"✅ Tipo de actividad válido: {tipo_actividad}")
    
    # ✅ SOLUCIÓN: Usar la misma función que asistencias para manejar zona horaria CDMX
    if timestamp_offline:
        # Usar la función especializada que maneja correctamente CDMX
        fecha_cdmx, hora_cdmx_datetime, timestamp_for_filename = obtener_fecha_hora_cdmx(timestamp_offline)
        # ✅ CORRECCIÓN: Guardar en CDMX (igual que asistencias), no convertir a UTC
        fecha_hora = hora_cdmx_datetime.replace(tzinfo=None)
        print(f"📅 ✅ Usando timestamp offline con zona CDMX: {fecha_hora}")
    else:
        # ✅ SOLUCIÓN: Usar función CDMX en lugar de datetime.utcnow()
        fecha_cdmx, hora_cdmx_datetime, timestamp_for_filename = obtener_fecha_hora_cdmx()
        # ✅ CORRECCIÓN: Guardar en CDMX (igual que asistencias), no convertir a UTC
        fecha_hora = hora_cdmx_datetime.replace(tzinfo=None)
        print(f"📅 ⏰ Usando timestamp actual CDMX: {fecha_hora}")

    # Guardar la foto en disco usando el timestamp correcto
    ext = os.path.splitext(foto.filename)[1]
    nombre_archivo = f"{usuario_id}_{timestamp_for_filename}{ext}"
    ruta_archivo = os.path.join(FOTOS_DIR, nombre_archivo)
    print(f"📁 Guardando foto como: {nombre_archivo}")
    
    with open(ruta_archivo, "wb") as f:
        contenido = await foto.read()
        f.write(contenido)

    # Guardar registro en la base usando consulta segura
    ejecutar_consulta_segura(
        "INSERT INTO registros (usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora, tipo_actividad, categoria_actividad, categoria_actividad_otro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (usuario_id, latitud, longitud, descripcion, ruta_archivo, fecha_hora, tipo_actividad, categoria_actividad, categoria_actividad_otro),
        fetch_type='none'
    )
    print(f"✅ Registro guardado en BD con fecha_hora: {fecha_hora}, tipo_actividad: {tipo_actividad}, categoria_actividad: {categoria_actividad}")

    return {"status": "ok", "foto_url": ruta_archivo, "tipo_actividad": tipo_actividad, "categoria_actividad": categoria_actividad}

# ENDPOINT CORREGIDO - Esta es la parte importante que debe actualizarse
@app.get("/registros")
def obtener_registros(usuario_id: int = None, limit: int = None, page: int = 1, page_size: int = 1000, territorio: str = None):
    try:
        # Aplicar límite de seguridad para evitar saturación del servidor
        if limit is None or limit > 5000:
            limit = 5000  # Límite máximo de seguridad
            print(f"⚠️ Aplicando límite de seguridad: {limit} registros")
        
        # Calcular offset para paginación
        offset = (page - 1) * page_size if page > 1 else 0
        
        print(f"🔍 Obteniendo registros - Usuario: {usuario_id}, Límite: {limit}, Página: {page}, Offset: {offset}, Territorio: {territorio}")
        
        # Construir query base con JOIN si hay filtro de territorio
        base_select = """SELECT r.id, r.usuario_id, r.latitud, r.longitud, r.descripcion, r.foto_url, r.fecha_hora, r.tipo_actividad, r.categoria_actividad, r.categoria_actividad_otro 
                        FROM registros r"""
        
        if territorio:
            base_select += " INNER JOIN usuarios u ON r.usuario_id = u.id"
        
        # Construir condiciones WHERE
        conditions = []
        params = []
        
        if usuario_id:
            conditions.append("r.usuario_id = %s")
            params.append(usuario_id)
        
        if territorio:
            conditions.append("u.territorio = %s")
            params.append(territorio)
        
        # Construir query completa
        query = base_select
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY r.fecha_hora DESC LIMIT %s OFFSET %s"
        
        effective_limit = min(limit, page_size) if limit else page_size
        params.extend([effective_limit, offset])
        
        # Ejecutar consulta con manejo seguro y timeout
        try:
            resultados = ejecutar_consulta_segura(query, tuple(params), fetch_type='all')
        except Exception as db_error:
            print(f"❌ Error de base de datos al obtener registros: {db_error}")
            # Si hay error, devolver respuesta vacía en lugar de fallar
            return {
                "registros": [],
                "total": 0,
                "error": "Error temporal de base de datos",
                "page": page,
                "page_size": page_size
            }
        
        if not resultados:
            resultados = []
        
        print(f"📊 Encontrados {len(resultados)} registros")
        
        # Obtener total de registros para paginación (solo si es necesario)
        total_registros = len(resultados)
        if page == 1 and len(resultados) == page_size:
            # Solo calcular total si podría haber más páginas
            try:
                count_query = "SELECT COUNT(*) FROM registros r"
                if territorio:
                    count_query += " INNER JOIN usuarios u ON r.usuario_id = u.id"
                count_conditions = []
                count_params = []
                if usuario_id:
                    count_conditions.append("r.usuario_id = %s")
                    count_params.append(usuario_id)
                if territorio:
                    count_conditions.append("u.territorio = %s")
                    count_params.append(territorio)
                if count_conditions:
                    count_query += " WHERE " + " AND ".join(count_conditions)
                cursor.execute(count_query, tuple(count_params) if count_params else None)
                total_registros = cursor.fetchone()[0]
            except Exception:
                total_registros = len(resultados)  # Fallback al conteo actual
        
        # Convertir tuplas a diccionarios manualmente con manejo de errores
        registros = []
        for i, row in enumerate(resultados):
            try:
                # ✅ SOLUCIÓN: Agregar zona horaria CDMX al ISO format para que JavaScript lo interprete correctamente
                fecha_iso = None
                if row[6]:
                    # row[6] es un datetime sin zona horaria (CDMX)
                    # Agregamos explícitamente la zona horaria CDMX (-06:00)
                    fecha_iso = row[6].isoformat() + "-06:00"
                    print(f"📅 Fecha con zona CDMX: {fecha_iso}")
                
                registro = {
                    "id": row[0],
                    "usuario_id": row[1],
                    "latitud": float(row[2]) if row[2] is not None else None,
                    "longitud": float(row[3]) if row[3] is not None else None,
                    "descripcion": row[4] if row[4] is not None else "",
                    "foto_url": row[5] if row[5] is not None else None,
                    "fecha_hora": fecha_iso,
                    "tipo_actividad": row[7] if len(row) > 7 and row[7] is not None else "campo",
                    "categoria_actividad": row[8] if len(row) > 8 and row[8] is not None else None,
                    "categoria_actividad_otro": row[9] if len(row) > 9 and row[9] is not None else None
                }
                registros.append(registro)
            except Exception as row_error:
                print(f"⚠️ Error procesando registro {i}: {row_error}")
                continue  # Saltar registros problemáticos
        
        print(f"✅ {len(registros)} registros procesados correctamente")
        
        # Respuesta con información de paginación
        response_data = {
            "registros": registros,
            "total": total_registros,
            "page": page,
            "page_size": page_size,
            "has_more": len(registros) == page_size
        }
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener registros: {str(e)}")

# NUEVO ENDPOINT OPTIMIZADO PARA ADMIN-PWA
@app.get("/admin/registros")
def obtener_registros_admin(page: int = 1, page_size: int = 50, usuario_id: int = None, territorio: str = None):
    """Endpoint optimizado para el admin-pwa con paginación obligatoria y filtro territorial"""
    try:
        # Límites de seguridad para admin
        max_page_size = 200
        page_size = min(page_size, max_page_size)
        page = max(1, page)  # Asegurar página mínima
        
        offset = (page - 1) * page_size
        
        print(f"🔍 [ADMIN] Obteniendo registros - Página: {page}, Tamaño: {page_size}, Offset: {offset}, Usuario: {usuario_id}, Territorio: {territorio}")
        
        # Verificar conexión antes de continuar
        if not verificar_conexion_db():
            raise HTTPException(status_code=503, detail="Servicio de base de datos no disponible")
        
        # Construir consulta optimizada con JOIN si hay filtro territorial
        if territorio:
            base_query = """
                SELECT r.id, r.usuario_id, r.latitud, r.longitud, r.descripcion, r.foto_url, r.fecha_hora, r.tipo_actividad, r.categoria_actividad, r.categoria_actividad_otro 
                FROM registros r
                INNER JOIN usuarios u ON r.usuario_id = u.id
            """
            count_query = "SELECT COUNT(*) FROM registros r INNER JOIN usuarios u ON r.usuario_id = u.id"
        else:
            base_query = """
                SELECT id, usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora, tipo_actividad, categoria_actividad, categoria_actividad_otro 
                FROM registros 
            """
            count_query = "SELECT COUNT(*) FROM registros"
        
        # Construir condiciones WHERE
        conditions = []
        params = []
        
        if usuario_id:
            if territorio:
                conditions.append("r.usuario_id = %s")
            else:
                conditions.append("usuario_id = %s")
            params.append(usuario_id)
        
        if territorio:
            conditions.append("u.territorio = %s")
            params.append(territorio)
        
        # Agregar WHERE clause si hay condiciones
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
            base_query += where_clause
            count_query += where_clause
        
        # Obtener total de registros primero (para paginación)
        try:
            total_registros = ejecutar_consulta_segura(count_query, tuple(params) if params else None, fetch_type='one')[0]
        except Exception as count_error:
            print(f"⚠️ Error obteniendo conteo: {count_error}")
            total_registros = 0
        
        # Consulta principal con paginación y orden optimizado
        if territorio:
            main_query = base_query + " ORDER BY r.id DESC LIMIT %s OFFSET %s"
        else:
            main_query = base_query + " ORDER BY id DESC LIMIT %s OFFSET %s"
        
        pagination_params = tuple(params) + (page_size, offset) if params else (page_size, offset)
        
        try:
            resultados = ejecutar_consulta_segura(main_query, pagination_params, fetch_type='all')
        except Exception as query_error:
            print(f"❌ Error en consulta principal: {query_error}")
            return {
                "registros": [],
                "total": 0,
                "page": page,
                "page_size": page_size,
                "total_pages": 0,
                "has_more": False,
                "error": "Error temporal de base de datos"
            }
        
        if not resultados:
            resultados = []
        
        # Procesar resultados de forma segura
        registros = []
        for row in resultados:
            try:
                registro = {
                    "id": row[0],
                    "usuario_id": row[1],
                    "latitud": float(row[2]) if row[2] is not None else 0.0,
                    "longitud": float(row[3]) if row[3] is not None else 0.0,
                    "descripcion": row[4] if row[4] is not None else "",
                    "foto_url": row[5] if row[5] is not None else None,
                    "fecha_hora": row[6].isoformat() if row[6] else None,
                    "tipo_actividad": row[7] if len(row) > 7 and row[7] is not None else "campo",
                    "categoria_actividad": row[8] if len(row) > 8 and row[8] is not None else None,
                    "categoria_actividad_otro": row[9] if len(row) > 9 and row[9] is not None else None
                }
                registros.append(registro)
            except Exception as row_error:
                print(f"⚠️ Error procesando registro: {row_error}")
                continue
        
        # Calcular paginación
        total_pages = (total_registros + page_size - 1) // page_size if total_registros > 0 else 0
        has_more = page < total_pages
        
        print(f"✅ [ADMIN] {len(registros)} registros procesados - Total: {total_registros}, Páginas: {total_pages}")
        
        return {
            "registros": registros,
            "total": total_registros,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_more": has_more
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ [ADMIN] Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener registros: {str(e)}")

# NUEVO ENDPOINT PARA ESTADÍSTICAS COMPLETAS (SIN LÍMITES)
@app.get("/estadisticas")
def obtener_estadisticas(territorio: str = None):
    """Obtener estadísticas completas del sistema sin límites.
    Si se proporciona territorio, filtra las estadísticas solo para usuarios de ese territorio."""
    try:
        print(f"🔍 Obteniendo estadísticas completas del sistema (territorio: {territorio or 'TODOS'})")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Si hay filtro por territorio, obtener los IDs de usuarios de ese territorio
        usuario_ids_territorio = None
        if territorio:
            cursor.execute("SELECT id FROM usuarios WHERE territorio = %s", (territorio,))
            usuario_ids_territorio = [row[0] for row in cursor.fetchall()]
            print(f"📊 Usuarios en territorio '{territorio}': {len(usuario_ids_territorio)}")
            
            if not usuario_ids_territorio:
                # Si no hay usuarios en el territorio, devolver estadísticas en cero
                return {"estadisticas": {
                    "total_registros": 0,
                    "total_usuarios": 0,
                    "registros_hoy": 0,
                    "total_asistencias": 0,
                    "asistencias_hoy": 0,
                    "usuarios_presentes": 0,
                    "territorio": territorio
                }}
        
        # Obtener total real de registros (actividades)
        if territorio and usuario_ids_territorio:
            cursor.execute("SELECT COUNT(*) FROM registros WHERE usuario_id = ANY(%s)", (usuario_ids_territorio,))
        else:
            cursor.execute("SELECT COUNT(*) FROM registros")
        total_registros = cursor.fetchone()[0]
        
        # Obtener total de usuarios
        if territorio:
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE territorio = %s", (territorio,))
        else:
            cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        # Obtener registros de hoy
        if territorio and usuario_ids_territorio:
            cursor.execute("SELECT COUNT(*) FROM registros WHERE DATE(fecha_hora) = CURRENT_DATE AND usuario_id = ANY(%s)", (usuario_ids_territorio,))
        else:
            cursor.execute("SELECT COUNT(*) FROM registros WHERE DATE(fecha_hora) = CURRENT_DATE")
        registros_hoy = cursor.fetchone()[0]
        
        # Obtener total de asistencias
        if territorio and usuario_ids_territorio:
            cursor.execute("SELECT COUNT(*) FROM asistencias WHERE usuario_id = ANY(%s)", (usuario_ids_territorio,))
        else:
            cursor.execute("SELECT COUNT(*) FROM asistencias")
        total_asistencias = cursor.fetchone()[0]
        
        # Obtener asistencias de hoy (usando zona horaria de Ciudad de México)
        if territorio and usuario_ids_territorio:
            cursor.execute("""
                SELECT COUNT(*) FROM asistencias 
                WHERE fecha = (CURRENT_DATE AT TIME ZONE 'America/Mexico_City')::date
                AND usuario_id = ANY(%s)
            """, (usuario_ids_territorio,))
        else:
            cursor.execute("""
                SELECT COUNT(*) FROM asistencias 
                WHERE fecha = (CURRENT_DATE AT TIME ZONE 'America/Mexico_City')::date
            """)
        asistencias_hoy = cursor.fetchone()[0]
        
        # Obtener usuarios presentes AHORA (con entrada pero SIN salida) - tiempo real CDMX
        # Solo cuenta usuarios que marcaron entrada hoy pero aún NO han marcado salida
        if territorio and usuario_ids_territorio:
            cursor.execute("""
                SELECT COUNT(DISTINCT usuario_id) FROM asistencias 
                WHERE fecha = (CURRENT_DATE AT TIME ZONE 'America/Mexico_City')::date
                AND hora_entrada IS NOT NULL
                AND hora_salida IS NULL
                AND usuario_id = ANY(%s)
            """, (usuario_ids_territorio,))
        else:
            cursor.execute("""
                SELECT COUNT(DISTINCT usuario_id) FROM asistencias 
                WHERE fecha = (CURRENT_DATE AT TIME ZONE 'America/Mexico_City')::date
                AND hora_entrada IS NOT NULL
                AND hora_salida IS NULL
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
        
        # Agregar info de territorio si se filtró
        if territorio:
            estadisticas["territorio"] = territorio
        
        print(f"✅ Estadísticas obtenidas (tiempo real CDMX){' para territorio: ' + territorio if territorio else ''}:")
        print(f"   - Total asistencias: {total_asistencias:,}")
        print(f"   - Asistencias hoy: {asistencias_hoy}")
        print(f"   - Usuarios PRESENTES ahora (con entrada, sin salida): {usuarios_presentes}")
        print(f"   - Total registros: {total_registros:,}")
        print(f"   - Registros hoy: {registros_hoy}")
        print(f"   - Total usuarios: {total_usuarios}")
        
        return {"estadisticas": estadisticas}
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

# NUEVOS ENDPOINTS PARA ESTADÍSTICAS DEL DÍA EN HORARIO CDMX
@app.get("/estadisticas/dia-actual")
def obtener_estadisticas_dia_actual(territorio: str = None):
    """Obtener estadísticas del día actual en horario CDMX (America/Mexico_City).
    Si se proporciona territorio, filtra las estadísticas solo para usuarios de ese territorio."""
    try:
        print(f"🔍 Obteniendo estadísticas del día actual en horario CDMX (territorio: {territorio or 'TODOS'})")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Configurar zona horaria CDMX
        cdmx_tz = pytz.timezone('America/Mexico_City')
        ahora_cdmx = datetime.now(cdmx_tz)
        fecha_hoy_cdmx = ahora_cdmx.date()
        
        print(f"📅 Calculando para fecha CDMX: {fecha_hoy_cdmx}")
        
        # Si hay filtro por territorio, obtener los IDs de usuarios de ese territorio
        usuario_ids_territorio = None
        if territorio:
            cursor.execute("SELECT id FROM usuarios WHERE territorio = %s", (territorio,))
            usuario_ids_territorio = [row[0] for row in cursor.fetchall()]
            print(f"📊 Usuarios en territorio '{territorio}': {len(usuario_ids_territorio)}")
            
            if not usuario_ids_territorio:
                # Si no hay usuarios en el territorio, devolver estadísticas en cero
                return {"estadisticas": {
                    "total_usuarios_dia": 0,
                    "entradas_dia": 0,
                    "salidas_dia": 0,
                    "actividades_dia": 0,
                    "fecha_cdmx": fecha_hoy_cdmx.isoformat(),
                    "territorio": territorio
                }}
        
        # Obtener rango de fechas en UTC para el día actual CDMX
        inicio_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.min.time()))
        fin_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.max.time()))
        
        # Convertir a UTC para consultar la BD
        inicio_utc = inicio_dia_cdmx.astimezone(pytz.UTC)
        fin_utc = fin_dia_cdmx.astimezone(pytz.UTC)
        
        # 1. Total de usuarios únicos que tuvieron al menos un registro hoy
        if territorio and usuario_ids_territorio:
            cursor.execute("""
                SELECT COUNT(DISTINCT usuario_id) FROM (
                    SELECT usuario_id FROM registros 
                    WHERE fecha_hora >= %s AND fecha_hora <= %s AND usuario_id = ANY(%s)
                    UNION
                    SELECT usuario_id FROM asistencias 
                    WHERE ((hora_entrada >= %s AND hora_entrada <= %s) 
                       OR (hora_salida >= %s AND hora_salida <= %s))
                       AND usuario_id = ANY(%s)
                ) AS usuarios_activos
            """, (inicio_utc, fin_utc, usuario_ids_territorio, inicio_utc, fin_utc, inicio_utc, fin_utc, usuario_ids_territorio))
        else:
            cursor.execute("""
                SELECT COUNT(DISTINCT usuario_id) FROM (
                    SELECT usuario_id FROM registros 
                    WHERE fecha_hora >= %s AND fecha_hora <= %s
                    UNION
                    SELECT usuario_id FROM asistencias 
                    WHERE (hora_entrada >= %s AND hora_entrada <= %s) 
                       OR (hora_salida >= %s AND hora_salida <= %s)
                ) AS usuarios_activos
            """, (inicio_utc, fin_utc, inicio_utc, fin_utc, inicio_utc, fin_utc))
        total_usuarios_dia = cursor.fetchone()[0]
        
        # 2. Total de entradas del día
        if territorio and usuario_ids_territorio:
            cursor.execute("""
                SELECT COUNT(*) FROM asistencias 
                WHERE hora_entrada >= %s AND hora_entrada <= %s AND usuario_id = ANY(%s)
            """, (inicio_utc, fin_utc, usuario_ids_territorio))
        else:
            cursor.execute("""
                SELECT COUNT(*) FROM asistencias 
                WHERE hora_entrada >= %s AND hora_entrada <= %s
            """, (inicio_utc, fin_utc))
        entradas_dia = cursor.fetchone()[0]
        
        # 3. Total de salidas del día
        if territorio and usuario_ids_territorio:
            cursor.execute("""
                SELECT COUNT(*) FROM asistencias 
                WHERE hora_salida >= %s AND hora_salida <= %s AND usuario_id = ANY(%s)
            """, (inicio_utc, fin_utc, usuario_ids_territorio))
        else:
            cursor.execute("""
                SELECT COUNT(*) FROM asistencias 
                WHERE hora_salida >= %s AND hora_salida <= %s
            """, (inicio_utc, fin_utc))
        salidas_dia = cursor.fetchone()[0]
        
        # 4. Total de actividades/registros del día
        if territorio and usuario_ids_territorio:
            cursor.execute("""
                SELECT COUNT(*) FROM registros 
                WHERE fecha_hora >= %s AND fecha_hora <= %s AND usuario_id = ANY(%s)
            """, (inicio_utc, fin_utc, usuario_ids_territorio))
        else:
            cursor.execute("""
                SELECT COUNT(*) FROM registros 
                WHERE fecha_hora >= %s AND fecha_hora <= %s
            """, (inicio_utc, fin_utc))
        actividades_dia = cursor.fetchone()[0]
        
        estadisticas_dia = {
            "total_usuarios_dia": total_usuarios_dia,
            "entradas_dia": entradas_dia,
            "salidas_dia": salidas_dia,
            "actividades_dia": actividades_dia,
            "fecha_cdmx": fecha_hoy_cdmx.isoformat()
        }
        
        # Agregar info de territorio si se filtró
        if territorio:
            estadisticas_dia["territorio"] = territorio
        
        print(f"✅ Estadísticas del día CDMX obtenidas{' para territorio: ' + territorio if territorio else ''}: {estadisticas_dia}")
        return {"estadisticas": estadisticas_dia}
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas del día: {str(e)}")

@app.get("/estadisticas/usuarios-dia")
def obtener_usuarios_activos_dia():
    """Obtener total de usuarios únicos activos del día actual en horario CDMX"""
    try:
        print("👥 Obteniendo usuarios únicos activos del día CDMX")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Configurar zona horaria CDMX
        cdmx_tz = pytz.timezone('America/Mexico_City')
        ahora_cdmx = datetime.now(cdmx_tz)
        fecha_hoy_cdmx = ahora_cdmx.date()
        
        # Obtener rango de fechas en UTC para el día actual CDMX
        inicio_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.min.time()))
        fin_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.max.time()))
        
        # Convertir a UTC para consultar la BD
        inicio_utc = inicio_dia_cdmx.astimezone(pytz.UTC)
        fin_utc = fin_dia_cdmx.astimezone(pytz.UTC)
        
        # Obtener usuarios únicos que tuvieron actividad hoy
        cursor.execute("""
            SELECT COUNT(DISTINCT usuario_id) FROM (
                SELECT usuario_id FROM registros 
                WHERE fecha_hora >= %s AND fecha_hora <= %s
                UNION
                SELECT usuario_id FROM asistencias 
                WHERE (hora_entrada >= %s AND hora_entrada <= %s) 
                   OR (hora_salida >= %s AND hora_salida <= %s)
            ) AS usuarios_activos
        """, (inicio_utc, fin_utc, inicio_utc, fin_utc, inicio_utc, fin_utc))
        
        total_usuarios = cursor.fetchone()[0]
        
        return {
            "total_usuarios_dia": total_usuarios,
            "fecha_cdmx": fecha_hoy_cdmx.isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo usuarios del día: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/estadisticas/entradas-dia")
def obtener_entradas_dia():
    """Obtener total de entradas del día actual en horario CDMX"""
    try:
        print("🚪➡️ Obteniendo entradas del día CDMX")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Configurar zona horaria CDMX
        cdmx_tz = pytz.timezone('America/Mexico_City')
        ahora_cdmx = datetime.now(cdmx_tz)
        fecha_hoy_cdmx = ahora_cdmx.date()
        
        # Obtener rango de fechas en UTC para el día actual CDMX
        inicio_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.min.time()))
        fin_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.max.time()))
        
        # Convertir a UTC para consultar la BD
        inicio_utc = inicio_dia_cdmx.astimezone(pytz.UTC)
        fin_utc = fin_dia_cdmx.astimezone(pytz.UTC)
        
        cursor.execute("""
            SELECT COUNT(*) FROM asistencias 
            WHERE hora_entrada >= %s AND hora_entrada <= %s
        """, (inicio_utc, fin_utc))
        
        entradas = cursor.fetchone()[0]
        
        return {
            "entradas_dia": entradas,
            "fecha_cdmx": fecha_hoy_cdmx.isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo entradas del día: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/estadisticas/salidas-dia")
def obtener_salidas_dia():
    """Obtener total de salidas del día actual en horario CDMX"""
    try:
        print("🚪⬅️ Obteniendo salidas del día CDMX")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Configurar zona horaria CDMX
        cdmx_tz = pytz.timezone('America/Mexico_City')
        ahora_cdmx = datetime.now(cdmx_tz)
        fecha_hoy_cdmx = ahora_cdmx.date()
        
        # Obtener rango de fechas en UTC para el día actual CDMX
        inicio_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.min.time()))
        fin_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.max.time()))
        
        # Convertir a UTC para consultar la BD
        inicio_utc = inicio_dia_cdmx.astimezone(pytz.UTC)
        fin_utc = fin_dia_cdmx.astimezone(pytz.UTC)
        
        cursor.execute("""
            SELECT COUNT(*) FROM asistencias 
            WHERE hora_salida >= %s AND hora_salida <= %s
        """, (inicio_utc, fin_utc))
        
        salidas = cursor.fetchone()[0]
        
        return {
            "salidas_dia": salidas,
            "fecha_cdmx": fecha_hoy_cdmx.isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo salidas del día: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/estadisticas/actividades-dia")
def obtener_actividades_dia():
    """Obtener total de actividades/registros del día actual en horario CDMX"""
    try:
        print("📝 Obteniendo actividades del día CDMX")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Configurar zona horaria CDMX
        cdmx_tz = pytz.timezone('America/Mexico_City')
        ahora_cdmx = datetime.now(cdmx_tz)
        fecha_hoy_cdmx = ahora_cdmx.date()
        
        # Obtener rango de fechas en UTC para el día actual CDMX
        inicio_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.min.time()))
        fin_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.max.time()))
        
        # Convertir a UTC para consultar la BD
        inicio_utc = inicio_dia_cdmx.astimezone(pytz.UTC)
        fin_utc = fin_dia_cdmx.astimezone(pytz.UTC)
        
        cursor.execute("""
            SELECT COUNT(*) FROM registros 
            WHERE fecha_hora >= %s AND fecha_hora <= %s
        """, (inicio_utc, fin_utc))
        
        actividades = cursor.fetchone()[0]
        
        return {
            "actividades_dia": actividades,
            "fecha_cdmx": fecha_hoy_cdmx.isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo actividades del día: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# NUEVO ENDPOINT PARA ESTADÍSTICAS POR TIPO DE ACTIVIDAD
@app.get("/estadisticas/tipo-actividad")
def obtener_estadisticas_tipo_actividad(territorio: str = None):
    """Obtener estadísticas de registros por tipo de actividad.
    Si se proporciona territorio, filtra las estadísticas solo para usuarios de ese territorio."""
    try:
        print(f"📊 Obteniendo estadísticas por tipo de actividad (territorio: {territorio or 'TODOS'})")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Si hay filtro por territorio, obtener los IDs de usuarios de ese territorio
        usuario_ids_territorio = None
        filtro_usuarios_sql = ""
        if territorio:
            cursor.execute("SELECT id FROM usuarios WHERE territorio = %s", (territorio,))
            usuario_ids_territorio = [row[0] for row in cursor.fetchall()]
            print(f"📊 Usuarios en territorio '{territorio}': {len(usuario_ids_territorio)}")
            
            if not usuario_ids_territorio:
                # Si no hay usuarios en el territorio, devolver estadísticas en cero
                return {"estadisticas_tipo": {
                    "total": {
                        "campo": 0,
                        "gabinete": 0,
                        "total_general": 0
                    },
                    "dia_actual": {
                        "campo": 0,
                        "gabinete": 0,
                        "total_dia": 0,
                        "fecha_cdmx": datetime.now(pytz.timezone('America/Mexico_City')).date().isoformat()
                    },
                    "territorio": territorio
                }}
        
        # Obtener estadísticas generales por tipo
        if territorio and usuario_ids_territorio:
            cursor.execute("""
                SELECT 
                    COALESCE(tipo_actividad, 'campo') as tipo,
                    COUNT(*) as total
                FROM registros 
                WHERE usuario_id = ANY(%s)
                GROUP BY COALESCE(tipo_actividad, 'campo')
                ORDER BY total DESC
            """, (usuario_ids_territorio,))
        else:
            cursor.execute("""
                SELECT 
                    COALESCE(tipo_actividad, 'campo') as tipo,
                    COUNT(*) as total
                FROM registros 
                GROUP BY COALESCE(tipo_actividad, 'campo')
                ORDER BY total DESC
            """)
        tipos_general = cursor.fetchall()
        
        # Obtener estadísticas del día actual por tipo en CDMX
        cdmx_tz = pytz.timezone('America/Mexico_City')
        ahora_cdmx = datetime.now(cdmx_tz)
        fecha_hoy_cdmx = ahora_cdmx.date()
        
        inicio_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.min.time()))
        fin_dia_cdmx = cdmx_tz.localize(datetime.combine(fecha_hoy_cdmx, datetime.max.time()))
        
        inicio_utc = inicio_dia_cdmx.astimezone(pytz.UTC)
        fin_utc = fin_dia_cdmx.astimezone(pytz.UTC)
        
        if territorio and usuario_ids_territorio:
            cursor.execute("""
                SELECT 
                    COALESCE(tipo_actividad, 'campo') as tipo,
                    COUNT(*) as total_dia
                FROM registros 
                WHERE fecha_hora >= %s AND fecha_hora <= %s AND usuario_id = ANY(%s)
                GROUP BY COALESCE(tipo_actividad, 'campo')
                ORDER BY total_dia DESC
            """, (inicio_utc, fin_utc, usuario_ids_territorio))
        else:
            cursor.execute("""
                SELECT 
                    COALESCE(tipo_actividad, 'campo') as tipo,
                    COUNT(*) as total_dia
                FROM registros 
                WHERE fecha_hora >= %s AND fecha_hora <= %s
                GROUP BY COALESCE(tipo_actividad, 'campo')
                ORDER BY total_dia DESC
            """, (inicio_utc, fin_utc))
        tipos_dia = cursor.fetchall()
        
        # Convertir resultados
        estadisticas_general = {tipo[0]: tipo[1] for tipo in tipos_general}
        estadisticas_dia = {tipo[0]: tipo[1] for tipo in tipos_dia}
        
        # Asegurar que ambos tipos estén presentes
        for tipo in ['campo', 'gabinete']:
            if tipo not in estadisticas_general:
                estadisticas_general[tipo] = 0
            if tipo not in estadisticas_dia:
                estadisticas_dia[tipo] = 0
        
        resultado = {
            "total": {
                "campo": estadisticas_general['campo'],
                "gabinete": estadisticas_general['gabinete'],
                "total_general": sum(estadisticas_general.values())
            },
            "dia_actual": {
                "campo": estadisticas_dia['campo'],
                "gabinete": estadisticas_dia['gabinete'],
                "total_dia": sum(estadisticas_dia.values()),
                "fecha_cdmx": fecha_hoy_cdmx.isoformat()
            }
        }
        
        # Agregar info de territorio si se filtró
        if territorio:
            resultado["territorio"] = territorio
        
        print(f"📊 Estadísticas por tipo de actividad obtenidas{' para territorio: ' + territorio if territorio else ''}: {resultado}")
        return {"estadisticas_tipo": resultado}
        
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas por tipo: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ==================== ENDPOINTS PARA REPORTES GENERADOS ====================

@app.post("/reportes/guardar")
async def guardar_reporte(datos: dict):
    """
    Guardar un reporte generado en la base de datos.
    
    NUEVO FLUJO:
    - Se guardan los DATOS del reporte (JSON) + firma del usuario
    - NO se genera el PDF aquí, se genera al descargar
    - El supervisor puede firmar después
    - El PDF final se genera con ambas firmas cuando se descarga
    """
    try:
        # Verificar conexión a la base de datos
        verificar_conexion_db()
        
        usuario_id = datos.get('usuario_id')
        nombre_reporte = datos.get('nombre_reporte')
        mes = datos.get('mes')
        anio = datos.get('anio')
        tipo = datos.get('tipo')  # PDF o CSV
        
        # NUEVO: Datos estructurados del reporte
        datos_reporte = datos.get('datos_reporte')  # JSON con actividades, info usuario, etc.
        firma_usuario_base64 = datos.get('firma_usuario_base64')  # Firma del usuario
        
        # Mantener compatibilidad con el flujo anterior
        pdf_base64 = datos.get('pdf_base64')  # PDF en formato base64 (opcional ahora)
        
        print(f"📥 Recibiendo reporte para guardar:")
        print(f"   - usuario_id: {usuario_id}")
        print(f"   - nombre_reporte: {nombre_reporte}")
        print(f"   - mes: {mes}, anio: {anio}")
        print(f"   - tipo: {tipo}")
        print(f"   - datos_reporte: {'Sí' if datos_reporte else 'No'}")
        print(f"   - firma_usuario_base64: {'Sí (' + str(len(firma_usuario_base64)) + ' chars)' if firma_usuario_base64 else 'No'}")
        print(f"   - pdf_base64: {'Sí (' + str(len(pdf_base64)) + ' chars)' if pdf_base64 else 'No'}")
        
        if not all([usuario_id, nombre_reporte, tipo]):
            raise HTTPException(status_code=400, detail="Faltan datos requeridos")
        
        # Verificar si ya existe un reporte para este mes/año
        if mes and anio:
            cursor.execute("""
                SELECT id, nombre_reporte, fecha_generacion 
                FROM reportes_generados 
                WHERE usuario_id = %s AND mes = %s AND anio = %s
            """, (usuario_id, mes, anio))
            existente = cursor.fetchone()
            if existente:
                print(f"⚠️ Ya existe reporte para {mes} {anio}: ID {existente[0]}")
                raise HTTPException(
                    status_code=409, 
                    detail=f"Ya existe un reporte firmado para {mes} {anio}. Solo puedes generar un reporte por mes."
                )
        
        print(f"💾 Guardando reporte: {nombre_reporte} para usuario {usuario_id}")
        
        # Convertir datos_reporte a JSON si es dict
        import json as json_module
        datos_reporte_json = json_module.dumps(datos_reporte) if datos_reporte else None
        
        cursor.execute("""
            INSERT INTO reportes_generados 
            (usuario_id, nombre_reporte, mes, anio, tipo, fecha_generacion, pdf_base64, datos_reporte, firma_usuario_base64)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s)
            RETURNING id, fecha_generacion
        """, (usuario_id, nombre_reporte, mes, anio, tipo, pdf_base64, datos_reporte_json, firma_usuario_base64))
        
        resultado = cursor.fetchone()
        conn.commit()
        
        print(f"✅ Reporte guardado exitosamente con ID: {resultado[0]}")
        
        return {
            "success": True,
            "reporte_id": resultado[0],
            "fecha_generacion": resultado[1].isoformat() if resultado[1] else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error guardando reporte: {e}")
        raise HTTPException(status_code=500, detail=f"Error al guardar reporte: {str(e)}")


@app.get("/reportes/verificar/{usuario_id}")
async def verificar_reporte_existente(usuario_id: int, mes: str, anio: int):
    """Verificar si ya existe un reporte para el mes/año especificado"""
    try:
        print(f"🔍 Verificando reporte existente para usuario {usuario_id}: {mes} {anio}")
        
        cursor.execute("""
            SELECT id, nombre_reporte, fecha_generacion 
            FROM reportes_generados 
            WHERE usuario_id = %s AND mes = %s AND anio = %s
        """, (usuario_id, mes, anio))
        
        existente = cursor.fetchone()
        
        if existente:
            print(f"✅ Reporte encontrado: ID {existente[0]}")
            return {
                "success": True,
                "existe": True,
                "reporte": {
                    "id": existente[0],
                    "nombre": existente[1],
                    "fecha_generacion": existente[2].isoformat() if existente[2] else None
                }
            }
        else:
            print(f"ℹ️ No existe reporte para {mes} {anio}")
            return {
                "success": True,
                "existe": False
            }
            
    except Exception as e:
        print(f"❌ Error verificando reporte: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/reportes/historial/{usuario_id}")
async def obtener_historial_reportes(usuario_id: int, limite: int = 50):
    """Obtener el historial de reportes generados por un usuario"""
    try:
        # Verificar conexión a la base de datos
        verificar_conexion_db()
        
        print(f"📋 Obteniendo historial de reportes para usuario {usuario_id}")
        
        cursor.execute("""
            SELECT 
                id,
                nombre_reporte,
                mes,
                anio,
                tipo,
                fecha_generacion,
                CASE WHEN pdf_base64 IS NOT NULL AND pdf_base64 != '' THEN true ELSE false END as tiene_pdf,
                COALESCE(firmado_supervisor, false) as firmado_supervisor,
                fecha_firma_supervisor,
                nombre_supervisor
            FROM reportes_generados
            WHERE usuario_id = %s
            ORDER BY fecha_generacion DESC
            LIMIT %s
        """, (usuario_id, limite))
        
        reportes = cursor.fetchall()
        
        resultado = []
        for reporte in reportes:
            resultado.append({
                "id": reporte[0],
                "nombre": reporte[1],
                "mes": reporte[2],
                "anio": reporte[3],
                "tipo": reporte[4],
                "fecha": reporte[5].isoformat() if reporte[5] else None,
                "tiene_pdf": reporte[6] if len(reporte) > 6 else False,
                "firmado_supervisor": reporte[7] if len(reporte) > 7 else False,
                "fecha_firma_supervisor": reporte[8].isoformat() if len(reporte) > 8 and reporte[8] else None,
                "nombre_supervisor": reporte[9] if len(reporte) > 9 else None
            })
        
        print(f"✅ {len(resultado)} reportes encontrados para usuario {usuario_id}")
        if resultado:
            print(f"   📄 Primer reporte: {resultado[0].get('nombre')}, tiene_pdf: {resultado[0].get('tiene_pdf')}")
        
        return {
            "success": True,
            "reportes": resultado,
            "total": len(resultado)
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo historial de reportes: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.delete("/reportes/eliminar/{reporte_id}")
async def eliminar_reporte(reporte_id: int):
    """Eliminar un reporte de la base de datos"""
    try:
        # Verificar conexión a la base de datos
        verificar_conexion_db()
        
        print(f"🗑️ Eliminando reporte ID: {reporte_id}")
        
        # Verificar que el reporte existe y si está firmado
        cursor.execute("""
            SELECT id, nombre_reporte, COALESCE(firmado_supervisor, false) as firmado
            FROM reportes_generados WHERE id = %s
        """, (reporte_id,))
        reporte = cursor.fetchone()
        
        if not reporte:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
        # Verificar si está firmado por el supervisor
        if reporte[2]:  # firmado_supervisor es True
            raise HTTPException(
                status_code=403, 
                detail="No se puede eliminar un reporte que ya ha sido firmado por el supervisor"
            )
        
        # Eliminar el reporte
        cursor.execute("DELETE FROM reportes_generados WHERE id = %s", (reporte_id,))
        conn.commit()
        
        print(f"✅ Reporte eliminado: {reporte[1]}")
        
        return {
            "success": True,
            "message": f"Reporte '{reporte[1]}' eliminado correctamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error eliminando reporte: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/reportes/descargar/{reporte_id}")
async def descargar_reporte(reporte_id: int):
    """
    Obtener los datos de un reporte guardado para generar el PDF en el frontend.
    
    NUEVO FLUJO:
    - Devuelve los datos estructurados del reporte (datos_reporte JSON)
    - Incluye la firma del usuario (firma_usuario_base64)
    - Incluye la firma del supervisor si existe (firma_supervisor_base64)
    - El frontend genera el PDF con las firmas disponibles
    - Si hay pdf_base64 guardado (compatibilidad), también lo devuelve
    """
    try:
        print(f"📥 Descargando reporte ID: {reporte_id}")
        
        cursor.execute("""
            SELECT 
                id,
                nombre_reporte,
                mes,
                anio,
                tipo,
                fecha_generacion,
                pdf_base64,
                firmado_supervisor,
                fecha_firma_supervisor,
                firma_supervisor_base64,
                nombre_supervisor,
                supervisor_id,
                datos_reporte,
                firma_usuario_base64
            FROM reportes_generados
            WHERE id = %s
        """, (reporte_id,))
        
        reporte = cursor.fetchone()
        
        if not reporte:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
        pdf_base64 = reporte[6]
        datos_reporte = reporte[12]  # JSONB - puede ser dict o string
        firma_usuario_base64 = reporte[13]
        
        # Si no hay datos_reporte ni pdf_base64, no hay nada que descargar
        if not pdf_base64 and not datos_reporte:
            raise HTTPException(status_code=404, detail="El reporte no tiene datos disponibles para descarga")
        
        print(f"✅ Reporte encontrado: {reporte[1]}")
        print(f"   Firmado por supervisor: {reporte[7]}")
        print(f"   Tiene datos_reporte: {'Sí' if datos_reporte else 'No'}")
        print(f"   Tiene pdf_base64: {'Sí' if pdf_base64 else 'No'}")
        print(f"   Tiene firma_usuario: {'Sí' if firma_usuario_base64 else 'No'}")
        
        return {
            "success": True,
            "reporte": {
                "id": reporte[0],
                "nombre": reporte[1],
                "mes": reporte[2],
                "anio": reporte[3],
                "tipo": reporte[4],
                "fecha": reporte[5].isoformat() if reporte[5] else None,
                "pdf_base64": pdf_base64,  # Para compatibilidad con reportes antiguos
                # Datos estructurados del reporte (NUEVO)
                "datos_reporte": datos_reporte,
                "firma_usuario_base64": firma_usuario_base64,
                # Datos de firma del supervisor
                "firmado_supervisor": reporte[7] or False,
                "fecha_firma_supervisor": reporte[8].isoformat() if reporte[8] else None,
                "firma_supervisor_base64": reporte[9],
                "nombre_supervisor": reporte[10],
                "supervisor_id": reporte[11]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error descargando reporte: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================
# ENDPOINT PARA FIRMAR REPORTES (SUPERVISOR)
# ============================================

class FirmaReporteRequest(BaseModel):
    supervisor_id: int
    nombre_supervisor: str
    firma_base64: Optional[str] = None  # Firma digital opcional

@app.post("/reportes/firmar/{reporte_id}")
async def firmar_reporte_supervisor(reporte_id: int, firma_data: FirmaReporteRequest):
    """
    Permite a un supervisor firmar un reporte.
    Una vez firmado, el reporte no puede ser eliminado por el usuario.
    Actualiza el PDF agregando la firma del supervisor en la sección 'Autorizó'.
    """
    try:
        # Verificar conexión a la base de datos
        verificar_conexion_db()
        
        print(f"✍️ [FIRMA] Firmando reporte ID: {reporte_id}")
        print(f"   Supervisor: {firma_data.nombre_supervisor} (ID: {firma_data.supervisor_id})")
        
        # Verificar que el reporte existe y obtener datos actuales
        cursor.execute("""
            SELECT 
                id,
                nombre_reporte,
                pdf_base64,
                firmado_supervisor,
                usuario_id
            FROM reportes_generados
            WHERE id = %s
        """, (reporte_id,))
        
        reporte = cursor.fetchone()
        
        if not reporte:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
        # Verificar si ya está firmado
        if reporte[3]:
            raise HTTPException(status_code=400, detail="Este reporte ya ha sido firmado por un supervisor")
        
        # Obtener zona horaria de CDMX
        from zoneinfo import ZoneInfo
        cdmx_tz = ZoneInfo("America/Mexico_City")
        fecha_firma = datetime.now(cdmx_tz)
        
        # Actualizar el reporte con la firma
        cursor.execute("""
            UPDATE reportes_generados
            SET 
                firmado_supervisor = TRUE,
                fecha_firma_supervisor = %s,
                firma_supervisor_base64 = %s,
                nombre_supervisor = %s,
                supervisor_id = %s
            WHERE id = %s
        """, (
            fecha_firma,
            firma_data.firma_base64,
            firma_data.nombre_supervisor,
            firma_data.supervisor_id,
            reporte_id
        ))
        
        conn.commit()
        
        print(f"✅ Reporte firmado exitosamente por {firma_data.nombre_supervisor}")
        
        return {
            "success": True,
            "message": f"Reporte firmado exitosamente por {firma_data.nombre_supervisor}",
            "data": {
                "reporte_id": reporte_id,
                "firmado_supervisor": True,
                "fecha_firma": fecha_firma.isoformat(),
                "nombre_supervisor": firma_data.nombre_supervisor,
                "supervisor_id": firma_data.supervisor_id
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error firmando reporte: {e}")
        raise HTTPException(status_code=500, detail=f"Error al firmar el reporte: {str(e)}")

@app.delete("/reportes/quitar-firma/{reporte_id}")
async def quitar_firma_reporte(reporte_id: int, supervisor_id: int):
    """
    Permite quitar la firma de un reporte (solo el mismo supervisor que firmó o un admin).
    """
    try:
        print(f"🔓 [FIRMA] Quitando firma del reporte ID: {reporte_id}")
        
        # Verificar que el reporte existe y está firmado
        cursor.execute("""
            SELECT 
                id,
                nombre_reporte,
                firmado_supervisor,
                supervisor_id
            FROM reportes_generados
            WHERE id = %s
        """, (reporte_id,))
        
        reporte = cursor.fetchone()
        
        if not reporte:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
        if not reporte[2]:
            raise HTTPException(status_code=400, detail="Este reporte no tiene firma de supervisor")
        
        # Quitar la firma
        cursor.execute("""
            UPDATE reportes_generados
            SET 
                firmado_supervisor = FALSE,
                fecha_firma_supervisor = NULL,
                firma_supervisor_base64 = NULL,
                nombre_supervisor = NULL,
                supervisor_id = NULL
            WHERE id = %s
        """, (reporte_id,))
        
        conn.commit()
        
        print(f"✅ Firma del reporte removida exitosamente")
        
        return {
            "success": True,
            "message": "Firma del reporte removida exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error quitando firma: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/reportes/admin/todos")
async def obtener_todos_reportes_admin(
    limite: int = 100,
    offset: int = 0,
    mes: str = None,
    anio: int = None,
    territorio: str = None,
    usuario_id: int = None
):
    """
    Obtener todos los reportes de todos los usuarios (para admin-pwa)
    Incluye información del usuario que generó cada reporte
    """
    try:
        print(f"📋 [ADMIN] Obteniendo todos los reportes...")
        print(f"   Filtros: mes={mes}, anio={anio}, territorio={territorio}, usuario_id={usuario_id}")
        
        # Construir query con JOINs para obtener info del usuario
        query = """
            SELECT 
                r.id,
                r.usuario_id,
                r.nombre_reporte,
                r.mes,
                r.anio,
                r.tipo,
                r.fecha_generacion,
                CASE WHEN r.pdf_base64 IS NOT NULL AND r.pdf_base64 != '' THEN true ELSE false END as tiene_pdf,
                u.nombre_completo,
                u.correo,
                u.territorio,
                u.cargo
            FROM reportes_generados r
            LEFT JOIN usuarios u ON r.usuario_id = u.id
            WHERE 1=1
        """
        params = []
        
        # Filtros opcionales
        if mes:
            query += " AND r.mes = %s"
            params.append(mes)
        
        if anio:
            query += " AND r.anio = %s"
            params.append(anio)
            
        if territorio:
            query += " AND u.territorio = %s"
            params.append(territorio)
            
        if usuario_id:
            query += " AND r.usuario_id = %s"
            params.append(usuario_id)
        
        # Ordenar por fecha más reciente
        query += " ORDER BY r.fecha_generacion DESC"
        
        # Primero obtener el total
        count_query = query.replace(
            """SELECT 
                r.id,
                r.usuario_id,
                r.nombre_reporte,
                r.mes,
                r.anio,
                r.tipo,
                r.fecha_generacion,
                CASE WHEN r.pdf_base64 IS NOT NULL AND r.pdf_base64 != '' THEN true ELSE false END as tiene_pdf,
                u.nombre_completo,
                u.correo,
                u.territorio,
                u.cargo""",
            "SELECT COUNT(*)"
        ).replace(" ORDER BY r.fecha_generacion DESC", "")
        
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        # Ahora con paginación
        query += " LIMIT %s OFFSET %s"
        params.extend([limite, offset])
        
        cursor.execute(query, params)
        reportes = cursor.fetchall()
        
        resultado = []
        for r in reportes:
            resultado.append({
                "id": r[0],
                "usuario_id": r[1],
                "nombre_reporte": r[2],
                "mes": r[3],
                "anio": r[4],
                "tipo": r[5],
                "fecha_generacion": r[6].isoformat() if r[6] else None,
                "tiene_pdf": r[7],
                "usuario": {
                    "nombre_completo": r[8],
                    "correo": r[9],
                    "territorio": r[10],
                    "cargo": r[11]
                }
            })
        
        print(f"✅ [ADMIN] {len(resultado)} reportes encontrados de {total} totales")
        
        return {
            "success": True,
            "reportes": resultado,
            "total": total,
            "pagina_actual": offset // limite + 1 if limite > 0 else 1,
            "total_paginas": (total + limite - 1) // limite if limite > 0 else 1
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo reportes admin: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/reportes/admin/estadisticas")
async def obtener_estadisticas_reportes_admin():
    """
    Obtener estadísticas de reportes para el dashboard admin
    """
    try:
        print(f"📊 [ADMIN] Obteniendo estadísticas de reportes...")
        
        # Total de reportes
        cursor.execute("SELECT COUNT(*) FROM reportes_generados")
        total_reportes = cursor.fetchone()[0]
        
        # Reportes este mes
        cursor.execute("""
            SELECT COUNT(*) FROM reportes_generados 
            WHERE EXTRACT(MONTH FROM fecha_generacion) = EXTRACT(MONTH FROM CURRENT_DATE)
            AND EXTRACT(YEAR FROM fecha_generacion) = EXTRACT(YEAR FROM CURRENT_DATE)
        """)
        reportes_mes = cursor.fetchone()[0]
        
        # Reportes por tipo
        cursor.execute("""
            SELECT tipo, COUNT(*) 
            FROM reportes_generados 
            GROUP BY tipo
        """)
        por_tipo = {r[0]: r[1] for r in cursor.fetchall()}
        
        # Usuarios con reportes
        cursor.execute("SELECT COUNT(DISTINCT usuario_id) FROM reportes_generados")
        usuarios_con_reportes = cursor.fetchone()[0]
        
        # Reportes por territorio
        cursor.execute("""
            SELECT u.territorio, COUNT(r.id)
            FROM reportes_generados r
            LEFT JOIN usuarios u ON r.usuario_id = u.id
            WHERE u.territorio IS NOT NULL
            GROUP BY u.territorio
            ORDER BY COUNT(r.id) DESC
        """)
        por_territorio = {r[0]: r[1] for r in cursor.fetchall()}
        
        # Reportes por mes (últimos 6 meses)
        cursor.execute("""
            SELECT 
                TO_CHAR(fecha_generacion, 'YYYY-MM') as mes,
                COUNT(*)
            FROM reportes_generados
            WHERE fecha_generacion >= CURRENT_DATE - INTERVAL '6 months'
            GROUP BY TO_CHAR(fecha_generacion, 'YYYY-MM')
            ORDER BY mes DESC
        """)
        por_mes = {r[0]: r[1] for r in cursor.fetchall()}
        
        print(f"✅ [ADMIN] Estadísticas obtenidas")
        
        return {
            "success": True,
            "estadisticas": {
                "total_reportes": total_reportes,
                "reportes_mes_actual": reportes_mes,
                "por_tipo": por_tipo,
                "usuarios_con_reportes": usuarios_con_reportes,
                "por_territorio": por_territorio,
                "por_mes": por_mes
            }
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Nuevo endpoint para obtener usuarios (para el panel de administración)
@app.get("/usuarios")
async def obtener_usuarios(territorio: str = None):
    try:
        print(f"🔍 Obteniendo usuarios... (filtro territorio: {territorio})")
        
        # Verificar si la columna 'rol' existe
        rol_check = ejecutar_consulta_segura("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'usuarios' AND column_name = 'rol'
        """, fetch_type='one')
        
        tiene_columna_rol = bool(rol_check)
        
        # Construir query base
        if tiene_columna_rol:
            base_query = "SELECT id, correo, nombre_completo, cargo, supervisor, curp, contrasena, telefono, rol, territorio FROM usuarios"
        else:
            base_query = "SELECT id, correo, nombre_completo, cargo, supervisor, curp, contrasena, telefono, territorio FROM usuarios"
        
        # Agregar filtro de territorio si se proporciona
        if territorio:
            query = f"{base_query} WHERE territorio = %s ORDER BY id DESC"
            resultados = ejecutar_consulta_segura(query, (territorio,), fetch_type='all')
        else:
            query = f"{base_query} ORDER BY id DESC"
            resultados = ejecutar_consulta_segura(query, fetch_type='all')
        
        if not resultados:
            resultados = []
        
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
                "contrasena": row[6],
                "telefono": row[7] if len(row) > 7 else None,
                "rol": row[8] if tiene_columna_rol and len(row) > 8 else 'user',
                "territorio": row[9] if tiene_columna_rol and len(row) > 9 else (row[8] if not tiene_columna_rol and len(row) > 8 else None)
            }
            usuarios.append(usuario)
        
        print(f"✅ Usuarios procesados correctamente con información de roles")
        return {"usuarios": usuarios}
        
    except HTTPException:
        raise
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
        
        # Buscar usuario por ID con CURP, teléfono, contraseña y territorio
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp, contrasena, telefono, territorio FROM usuarios WHERE id = %s",
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
            "telefono": resultado[7] if len(resultado) > 7 else None,  # Incluir teléfono si existe
            "territorio": resultado[8] if len(resultado) > 8 else None  # Incluir territorio si existe
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
class UserUpdate(BaseModel):
    correo: str
    nombre_completo: str
    cargo: str
    supervisor: Optional[str] = None
    curp: Optional[str] = None
    telefono: Optional[str] = None
    rol: str = 'user'
    territorio: Optional[str] = None
    nueva_contrasena: Optional[str] = None  # Contraseña opcional para actualización

@app.put("/usuarios/{user_id}")
async def actualizar_usuario(user_id: int, usuario: UserUpdate):
    """Actualiza los datos de un usuario específico incluyendo rol y contraseña opcional"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"✏️ Actualizando usuario {user_id}...")
        
        # Validación de rol
        if usuario.rol not in ['admin', 'user']:
            raise HTTPException(status_code=400, detail="Rol inválido. Debe ser 'admin' o 'user'")
        
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
        cursor.execute("SELECT id, contrasena FROM usuarios WHERE id = %s", (user_id,))
        usuario_actual = cursor.fetchone()
        if not usuario_actual:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar si la columna 'rol' existe, si no, agregarla
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'usuarios' AND column_name = 'rol'
        """)
        
        if not cursor.fetchone():
            print("📝 Agregando columna 'rol' a la tabla usuarios")
            cursor.execute("ALTER TABLE usuarios ADD COLUMN rol VARCHAR(10) DEFAULT 'user'")
            conn.commit()
        
        # Determinar la contraseña a usar
        contrasena_final = usuario_actual[1]  # Mantener la actual por defecto
        if usuario.nueva_contrasena and usuario.nueva_contrasena.strip():
            contrasena_final = usuario.nueva_contrasena.strip()
            print("🔑 Actualizando contraseña del usuario")
        
        # Actualizar usuario con rol y territorio
        cursor.execute(
            """UPDATE usuarios 
               SET correo = %s, nombre_completo = %s, cargo = %s, 
                   supervisor = %s, contrasena = %s, curp = %s, telefono = %s, rol = %s, territorio = %s 
               WHERE id = %s""",
            (usuario.correo, usuario.nombre_completo, usuario.cargo, 
             usuario.supervisor, contrasena_final, curp_upper, usuario.telefono, usuario.rol, usuario.territorio, user_id)
        )
        
        conn.commit()
        
        # Obtener usuario actualizado
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, contrasena, curp, telefono, rol, territorio FROM usuarios WHERE id = %s",
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
            "telefono": resultado[7],
            "rol": resultado[8] if len(resultado) > 8 else 'user',
            "territorio": resultado[9] if len(resultado) > 9 else None
        }
        
        print(f"✅ Usuario {user_id} actualizado exitosamente con rol {usuario.rol}")
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
                   supervisor = %s, curp = %s, telefono = %s, territorio = %s 
               WHERE id = %s""",
            (info.correo, info.nombre_completo, info.cargo, 
             info.supervisor, curp_upper, info.telefono, info.territorio, user_id)
        )
        
        conn.commit()
        
        # Obtener usuario actualizado
        cursor.execute(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp, telefono, territorio FROM usuarios WHERE id = %s",
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
            "telefono": resultado[6],
            "territorio": resultado[7]
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

# ==================== ENDPOINT PARA ACTUALIZAR TERRITORIO ====================

# Lista de territorios de Sembrando Vida
TERRITORIOS_SEMBRANDO_VIDA = [
    "Acapulco - Centro - Norte - Tierra Caliente",
    "Acayucan",
    "Balancán",
    "Chihuahua / Sonora",
    "Colima",
    "Comalcalco",
    "Córdoba",
    "Costa Chica - Montaña",
    "Costa Grande - Sierra",
    "Durango / Zacatecas",
    "Hidalgo",
    "Istmo",
    "Michoacán",
    "Mixteca",
    "Morelos",
    "Nayarit / Jalisco",
    "Ocosingo",
    "Palenque",
    "Papantla",
    "Pichucalco",
    "Puebla",
    "San Luis Potosí",
    "Sinaloa",
    "Tamaulipas",
    "Tantoyuca",
    "Tapachula",
    "Teapa",
    "Tlaxcala / Estado de México",
    "Tzucacab / Opb",
    "Xpujil",
    "Oficinas Centrales"
]

class TerritorioUpdate(BaseModel):
    territorio: str

@app.patch("/usuarios/{user_id}/territorio")
async def actualizar_territorio(user_id: int, data: TerritorioUpdate):
    """Actualiza el territorio de un usuario"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Validar que el territorio sea uno de los territorios de Sembrando Vida
        if data.territorio not in TERRITORIOS_SEMBRANDO_VIDA:
            raise HTTPException(status_code=400, detail=f"Territorio inválido. Debe ser uno de los territorios de Sembrando Vida.")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Actualizar territorio
        cursor.execute(
            "UPDATE usuarios SET territorio = %s WHERE id = %s",
            (data.territorio, user_id)
        )
        conn.commit()
        
        print(f"✅ Territorio del usuario {user_id} actualizado a: {data.territorio}")
        return {
            "success": True,
            "mensaje": "Territorio actualizado exitosamente",
            "territorio": data.territorio
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
        raise HTTPException(status_code=500, detail=f"Error al actualizar territorio: {str(e)}")

# Endpoint para obtener lista de territorios de Sembrando Vida
@app.get("/territorios-sembrando-vida")
async def obtener_territorios():
    """Devuelve la lista de territorios de Sembrando Vida"""
    return {"territorios": TERRITORIOS_SEMBRANDO_VIDA}

# Mantener endpoint antiguo por compatibilidad (redirige a territorios)
@app.get("/estados-mexico")
async def obtener_estados_mexico():
    """DEPRECADO: Usar /territorios-sembrando-vida en su lugar"""
    return {"territorios": TERRITORIOS_SEMBRANDO_VIDA}

# Endpoint para resetear todos los territorios de usuarios (para migración)
@app.post("/admin/reset-territorios")
async def reset_todos_territorios():
    """Resetea el campo territorio de todos los usuarios a NULL para que vuelvan a seleccionar"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Contar cuántos usuarios tienen territorio asignado
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE territorio IS NOT NULL")
        usuarios_con_territorio = cursor.fetchone()[0]
        
        # Resetear todos los territorios a NULL
        cursor.execute("UPDATE usuarios SET territorio = NULL WHERE territorio IS NOT NULL")
        conn.commit()
        
        print(f"✅ Se resetearon {usuarios_con_territorio} territorios de usuarios")
        return {
            "success": True,
            "mensaje": f"Se resetearon {usuarios_con_territorio} territorios de usuarios",
            "usuarios_afectados": usuarios_con_territorio
        }
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al resetear territorios: {str(e)}")

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

# Endpoint de autenticación para administradores con información de usuario
@app.post("/admin/login")
def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        username = form_data.username
        password = form_data.password
        
        print(f"🔐 Intento de login para usuario: {username}")
        
        # Buscar usuario administrador en la base de datos incluyendo permisos, estado activo, es_territorial, territorio, nombre_completo, curp y cargo
        cursor.execute("SELECT id, password, rol, permisos, activo, es_territorial, territorio, nombre_completo, curp, cargo FROM admin_users WHERE username = %s", (username,))
        row = cursor.fetchone()
        
        if not row or not pwd_context.verify(password, row[1]):
            print(f"❌ Credenciales incorrectas para usuario: {username}")
            raise HTTPException(status_code=400, detail="Credenciales incorrectas")
        
        user_id = row[0]
        user_rol = row[2] or 'admin'  # rol por defecto admin
        user_activo = row[4] if row[4] is not None else True  # activo por defecto True
        es_territorial = row[5] if row[5] is not None else False
        territorio = row[6]
        nombre_completo = row[7] or ''
        curp = row[8] or ''
        cargo = row[9] or ''
        
        # Verificar si el usuario está activo
        if not user_activo:
            print(f"❌ Usuario inactivo intentando acceder: {username}")
            raise HTTPException(status_code=403, detail="Tu cuenta ha sido desactivada. Contacta al administrador.")
        
        # Parsear permisos
        permisos_str = row[3]
        if permisos_str:
            try:
                permisos = json.loads(permisos_str)
            except:
                permisos = PERMISOS_ADMIN_DEFAULT if user_rol == 'admin' else PERMISOS_USER_DEFAULT
        else:
            permisos = PERMISOS_ADMIN_DEFAULT if user_rol == 'admin' else PERMISOS_USER_DEFAULT
        
        # Generar token JWT con información del usuario incluyendo territorio
        token_data = {
            "sub": username, 
            "role": user_rol,
            "user_id": user_id,
            "tipo": "admin_user",
            "es_territorial": es_territorial,
            "territorio": territorio
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
        
        print(f"✅ Login exitoso para usuario: {username} con rol: {user_rol}" + (f" (territorial: {territorio})" if es_territorial else ""))
        
        return {
            "access_token": token, 
            "token_type": "bearer",
            "user_info": {
                "id": user_id,
                "username": username,
                "rol": user_rol,
                "tipo": "admin_user",
                "permisos": permisos,
                "activo": user_activo,
                "es_territorial": es_territorial,
                "territorio": territorio,
                "nombre_completo": nombre_completo,
                "curp": curp,
                "cargo": cargo
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en admin login: {e}")
        raise HTTPException(status_code=500, detail=f"Error en autenticación: {str(e)}")

# Nuevo endpoint para obtener información del usuario actual
@app.get("/auth/me")
async def get_current_user():
    """Obtener información del usuario actualmente logueado"""
    try:
        # Este endpoint simula obtener la información del usuario desde el token
        # En una implementación real, se verificaría el token JWT
        print("🔍 Obteniendo información del usuario actual")
        
        # Por ahora devuelve información por defecto de admin
        return {
            "id": 1,
            "username": "admin",
            "rol": "admin",
            "tipo": "admin_user",
            "is_authenticated": True
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo usuario actual: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")

# Endpoint para verificar si un usuario está activo (para verificación en tiempo real)
@app.get("/auth/check-active/{username}")
async def check_user_active(username: str):
    """Verificar si un usuario específico está activo"""
    try:
        print(f"🔍 Verificando estado activo de usuario: {username}")
        
        cursor.execute("SELECT id, activo FROM admin_users WHERE username = %s", (username,))
        row = cursor.fetchone()
        
        if not row:
            return {"active": False, "exists": False, "message": "Usuario no encontrado"}
        
        activo = row[1] if row[1] is not None else True
        
        return {
            "active": activo,
            "exists": True,
            "user_id": row[0],
            "username": username
        }
        
    except Exception as e:
        print(f"❌ Error verificando estado de usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al verificar usuario: {str(e)}")

# Endpoint para verificación completa de sesión (activo, rol, permisos) - TIEMPO REAL
@app.get("/auth/check-session/{username}")
async def check_user_session(username: str):
    """Verificar estado completo de sesión de un usuario (activo, rol, permisos, territorio)"""
    try:
        print(f"🔍 Verificando sesión completa de usuario: {username}")
        
        cursor.execute("""
            SELECT id, rol, permisos, activo, es_territorial, territorio 
            FROM admin_users 
            WHERE username = %s
        """, (username,))
        row = cursor.fetchone()
        
        if not row:
            return {
                "active": False, 
                "exists": False, 
                "message": "Usuario no encontrado"
            }
        
        user_id = row[0]
        user_rol = row[1] or 'user'
        permisos_str = row[2]
        activo = row[3] if row[3] is not None else True
        es_territorial = row[4] if row[4] is not None else False
        territorio = row[5]
        
        # Parsear permisos
        if permisos_str:
            try:
                permisos = json.loads(permisos_str)
            except:
                permisos = PERMISOS_ADMIN_DEFAULT if user_rol == 'admin' else PERMISOS_USER_DEFAULT
        else:
            permisos = PERMISOS_ADMIN_DEFAULT if user_rol == 'admin' else PERMISOS_USER_DEFAULT
        
        return {
            "active": activo,
            "exists": True,
            "user_id": user_id,
            "username": username,
            "rol": user_rol,
            "permisos": permisos,
            "es_territorial": es_territorial,
            "territorio": territorio
        }
        
    except Exception as e:
        print(f"❌ Error verificando sesión de usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al verificar sesión: {str(e)}")

# Endpoint para verificar permisos específicos
@app.get("/auth/check-permission/{permission}")
async def check_permission(permission: str):
    """Verificar si el usuario actual tiene un permiso específico"""
    try:
        print(f"🔐 Verificando permiso: {permission}")
        
        # Lista de permisos que requieren admin
        admin_permissions = [
            "usuarios.view",
            "usuarios.create", 
            "usuarios.edit",
            "usuarios.delete",
            "permisos.view",
            "permisos.manage",
            "configuracion.view",
            "configuracion.manage",
            "admin.access"
        ]
        
        # Por ahora siempre devolver admin = True
        # En implementación real se verificaría el token JWT
        user_role = "admin"  # Obtener del token
        
        has_permission = user_role == "admin" or permission not in admin_permissions
        
        return {
            "permission": permission,
            "granted": has_permission,
            "user_role": user_role
        }
        
    except Exception as e:
        print(f"❌ Error verificando permiso: {e}")
        raise HTTPException(status_code=500, detail=f"Error al verificar permiso: {str(e)}")

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
async def obtener_historial_asistencias(usuario_id: int = None, limit: int = None, offset: int = 0, territorio: str = None):
    try:
        # Verificar y reconectar si es necesario
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🔍 Obteniendo historial de asistencias - Usuario: {usuario_id}, Límite: {limit if limit else 'Sin límite'}, Offset: {offset}, Territorio: {territorio}")
        
        # Construir la query base con JOIN a usuarios si hay filtro de territorio
        base_select = """SELECT a.id, a.usuario_id, a.fecha, a.hora_entrada, a.hora_salida, 
                         a.latitud_entrada, a.longitud_entrada, a.latitud_salida, a.longitud_salida,
                         a.foto_entrada_url, a.foto_salida_url, a.descripcion_entrada, a.descripcion_salida
                  FROM asistencias a"""
        
        if territorio:
            base_select += " INNER JOIN usuarios u ON a.usuario_id = u.id"
        
        # Construir condiciones WHERE
        conditions = []
        params = []
        
        if usuario_id:
            conditions.append("a.usuario_id = %s")
            params.append(usuario_id)
        
        if territorio:
            conditions.append("u.territorio = %s")
            params.append(territorio)
        
        # Construir query completa
        query = base_select
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY a.fecha DESC, a.hora_entrada DESC"
        
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        
        query += " OFFSET %s"
        params.append(offset)
        
        cursor.execute(query, tuple(params))
        
        resultados = cursor.fetchall()
        print(f"📊 Encontradas {len(resultados)} asistencias (limit: {limit}, offset: {offset}, territorio: {territorio})")
        
        # Convertir tuplas a diccionarios manualmente
        asistencias = []
        for row in resultados:
            # Procesar fecha correctamente (es DATE, no DATETIME)
            # No agregar timezone a la fecha, solo formatearla como YYYY-MM-DD
            fecha_str = row[2].isoformat() if row[2] else None
            
            # Procesar hora_entrada (es TIME o DATETIME)
            hora_entrada_str = None
            if row[3]:
                # Si es un objeto time, convertirlo a string simple
                if hasattr(row[3], 'isoformat'):
                    hora_entrada_str = row[3].isoformat()
                else:
                    hora_entrada_str = str(row[3])
            
            # Procesar hora_salida (es TIME o DATETIME)
            hora_salida_str = None
            if row[4]:
                if hasattr(row[4], 'isoformat'):
                    hora_salida_str = row[4].isoformat()
                else:
                    hora_salida_str = str(row[4])
            
            asistencia = {
                "id": row[0],
                "usuario_id": row[1],
                "fecha": fecha_str,
                "hora_entrada": hora_entrada_str,
                "hora_salida": hora_salida_str,
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
                   u.nombre_completo, u.correo, u.curp, u.cargo
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
                "usuario_correo": row[9],
                "usuario_curp": row[10],
                "usuario_cargo": row[11]
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
                   u.nombre_completo, u.correo, u.curp, u.cargo
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
                "usuario_correo": row[9],
                "usuario_curp": row[10],
                "usuario_cargo": row[11]
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
        
        return {
            "id": notificacion_id,
            "status": "success",
            "message": "Notificación creada exitosamente",
            "titulo": titulo,
            "enviada_a_todos": enviada_a_todos,
            "usuarios_destinatarios": len(usuarios_seleccionados) if not enviada_a_todos else "todos",
            "tiene_archivo": archivo_nombre is not None,
            "fecha_envio": fecha_envio.isoformat()
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

# ==================== ENDPOINTS ESPECÍFICOS (DEBEN IR ANTES DEL GENÉRICO) ====================

@app.get("/notificaciones/unread_count")
async def obtener_conteo_no_leidas(usuario_id: int):
    """Obtener conteo de notificaciones no leídas para un usuario"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
            
        if not usuario_id:
            raise HTTPException(status_code=400, detail="usuario_id es obligatorio")
        
        print(f"📊 Obteniendo conteo de no leídas para usuario {usuario_id}")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Configurar zona horaria para la sesión
        cursor.execute("SET TIME ZONE 'America/Mexico_City'")
        
        # Contar notificaciones visibles sin lectura
        cursor.execute("""
            SELECT COUNT(DISTINCT n.id)
            FROM notificaciones n
            LEFT JOIN notificacion_usuarios nu ON n.id = nu.notificacion_id
            LEFT JOIN notificacion_leidos nl ON n.id = nl.notificacion_id AND nl.usuario_id = %s
            WHERE (n.enviada_a_todos = TRUE OR nu.usuario_id = %s)
            AND n.fecha_envio IS NOT NULL
            AND nl.id IS NULL
        """, (usuario_id, usuario_id))
        
        count = cursor.fetchone()[0] or 0
        
        print(f"📊 Usuario {usuario_id} tiene {count} notificaciones no leídas")
        
        return {"count": count}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error obteniendo conteo no leídas: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener conteo: {str(e)}")

@app.get("/notificaciones/list")
async def listar_notificaciones_usuario(
    usuario_id: int,
    filtro: str = "all",  # "unread" | "all"
    limit: int = 200,
    offset: int = 0
):
    """Listar notificaciones para un usuario con filtro de leídas/no leídas"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
            
        if not usuario_id:
            raise HTTPException(status_code=400, detail="usuario_id es obligatorio")
        
        if filtro not in ["unread", "all"]:
            raise HTTPException(status_code=400, detail="filtro debe ser 'unread' o 'all'")
        
        print(f"📋 Listando notificaciones para usuario {usuario_id} (filtro: {filtro})")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Configurar zona horaria para la sesión
        cursor.execute("SET TIME ZONE 'America/Mexico_City'")
        
        # Construir consulta base
        base_query = """
            SELECT DISTINCT n.id, n.titulo, n.subtitulo, n.descripcion, n.enlace_url,
                   n.archivo_nombre, n.archivo_tipo, n.enviada_a_todos,
                   n.fecha_creacion, n.fecha_envio,
                   CASE WHEN nl.id IS NOT NULL THEN TRUE ELSE FALSE END as leida
            FROM notificaciones n
            LEFT JOIN notificacion_usuarios nu ON n.id = nu.notificacion_id
            LEFT JOIN notificacion_leidos nl ON n.id = nl.notificacion_id AND nl.usuario_id = %s
            WHERE (n.enviada_a_todos = TRUE OR nu.usuario_id = %s)
            AND n.fecha_envio IS NOT NULL
        """
        
        # Agregar filtro si es solo no leídas
        if filtro == "unread":
            base_query += " AND nl.id IS NULL"
        
        # Agregar orden y límites
        query = base_query + """
            ORDER BY n.fecha_envio DESC NULLS LAST, n.fecha_creacion DESC
            LIMIT %s OFFSET %s
        """
        
        cursor.execute(query, (usuario_id, usuario_id, limit, offset))
        resultados = cursor.fetchall()
        
        # Obtener total sin límites para paginación
        count_query = """
            SELECT COUNT(DISTINCT n.id)
            FROM notificaciones n
            LEFT JOIN notificacion_usuarios nu ON n.id = nu.notificacion_id
            LEFT JOIN notificacion_leidos nl ON n.id = nl.notificacion_id AND nl.usuario_id = %s
            WHERE (n.enviada_a_todos = TRUE OR nu.usuario_id = %s)
            AND n.fecha_envio IS NOT NULL
        """
        
        if filtro == "unread":
            count_query += " AND nl.id IS NULL"
            
        cursor.execute(count_query, (usuario_id, usuario_id))
        total = cursor.fetchone()[0] or 0
        
        # Convertir resultados
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
                "leida": bool(row[10]),
                "tiene_archivo": bool(row[5])
            }
            notificaciones.append(notificacion)
        
        print(f"📋 {len(notificaciones)} notificaciones listadas para usuario {usuario_id}")
        
        return {
            "notificaciones": notificaciones,
            "total": total,
            "filtro": filtro,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error listando notificaciones del usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al listar notificaciones: {str(e)}")

# ==================== ENDPOINTS GENÉRICOS (VAN DESPUÉS DE LOS ESPECÍFICOS) ====================

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

@app.post("/notificaciones/{notificacion_id}/leer")
async def marcar_notificacion_leida(notificacion_id: int, data: NotificacionLeer):
    """Marcar una notificación como leída por un usuario"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"✅ Marcando notificación {notificacion_id} como leída para usuario {data.usuario_id}")
        
        # Verificar que la notificación existe
        cursor.execute("SELECT id FROM notificaciones WHERE id = %s", (notificacion_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (data.usuario_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar que la notificación es visible para el usuario
        cursor.execute("""
            SELECT 1
            FROM notificaciones n
            LEFT JOIN notificacion_usuarios nu ON n.id = nu.notificacion_id
            WHERE n.id = %s 
            AND (n.enviada_a_todos = TRUE OR nu.usuario_id = %s)
        """, (notificacion_id, data.usuario_id))
        
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Notificación no visible para este usuario")
        
        # Configurar zona horaria para la sesión
        cursor.execute("SET TIME ZONE 'America/Mexico_City'")
        
        # Insertar o actualizar el registro de lectura
        cursor.execute("""
            INSERT INTO notificacion_leidos (notificacion_id, usuario_id, device_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (notificacion_id, usuario_id) 
            DO UPDATE SET 
                leida_en = NOW() AT TIME ZONE 'America/Mexico_City',
                device_id = EXCLUDED.device_id
        """, (notificacion_id, data.usuario_id, data.device_id))
        
        conn.commit()
        
        print(f"✅ Notificación {notificacion_id} marcada como leída para usuario {data.usuario_id}")
        
        return {"ok": True}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error marcando notificación como leída: {e}")
        raise HTTPException(status_code=500, detail=f"Error al marcar como leída: {str(e)}")

@app.get("/notificaciones/{notificacion_id}/archivo")
async def descargar_archivo_notificacion(notificacion_id: int, safe: bool = False):
    """Descargar o ver el archivo adjunto de una notificación con encoding mejorado"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"📎 Descargando archivo de notificación {notificacion_id} (safe={safe})")
        
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
        
        # NUEVA LÓGICA DE MANEJO DE ENCODING DE NOMBRES DE ARCHIVO
        try:
            # Intentar usar el nombre original si no contiene caracteres problemáticos
            nombre_seguro = archivo_nombre
            # Verificar si el nombre es seguro para ASCII
            nombre_seguro.encode('ascii')
        except (UnicodeEncodeError, UnicodeDecodeError):
            # Si el nombre tiene caracteres especiales, crear un nombre seguro
            import hashlib
            from datetime import datetime
            
            # Generar nombre seguro basado en el hash y timestamp
            hash_nombre = hashlib.md5(archivo_nombre.encode('utf-8', errors='replace')).hexdigest()[:8]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Mantener la extensión si es posible
            try:
                ext = archivo_nombre.split('.')[-1] if '.' in archivo_nombre else 'bin'
                # Limpiar la extensión de caracteres especiales
                ext_segura = ''.join(c for c in ext if c.isalnum())[:10]
                nombre_seguro = f"archivo_{timestamp}_{hash_nombre}.{ext_segura}"
            except:
                nombre_seguro = f"archivo_{timestamp}_{hash_nombre}.bin"
            
            print(f"⚠️ Nombre original problemático: '{archivo_nombre}' -> nombre seguro: '{nombre_seguro}'")
        
        # Definir Content-Type según el tipo de archivo
        content_types = {
            'imagen': 'image/jpeg',
            'pdf': 'application/pdf',
            'video': 'video/mp4'
        }
        
        content_type = content_types.get(archivo_tipo, 'application/octet-stream')
        
        # Ajustar Content-Type para modo seguro (forzar descarga)
        if safe:
            content_type = 'application/octet-stream'
        
        print(f"📎 Enviando archivo: {nombre_seguro} ({archivo_tipo}, {len(archivo_bytes)} bytes)")
        
        # Preparar headers seguros
        headers = {
            "Content-Length": str(len(archivo_bytes)),
            "Cache-Control": "public, max-age=3600"  # Cache por 1 hora
        }
        
        # NUEVA LÓGICA MEJORADA PARA CONTENT-DISPOSITION
        try:
            # Para modo seguro o nombres problemáticos, usar attachment
            if safe:
                headers["Content-Disposition"] = f"attachment; filename=\"{nombre_seguro}\""
            else:
                # Para visualización inline, usar el nombre seguro
                headers["Content-Disposition"] = f"inline; filename=\"{nombre_seguro}\""
            
        except Exception as e:
            print(f"⚠️ Error configurando Content-Disposition: {e}")
            # Fallback ultra-seguro
            headers["Content-Disposition"] = f"attachment; filename=\"archivo_{notificacion_id}.bin\""
        
        # Crear stream del archivo con manejo de memoria mejorado
        try:
            archivo_stream = io.BytesIO(archivo_bytes)
            
            return StreamingResponse(
                archivo_stream,
                media_type=content_type,
                headers=headers
            )
            
        except Exception as e:
            print(f"❌ Error creando stream: {e}")
            raise HTTPException(status_code=500, detail=f"Error procesando archivo: {str(e)}")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error descargando archivo: {e}")
        # Error más específico para debugging
        error_msg = f"Error al descargar archivo: {str(e)}"
        if "codec" in str(e).lower() or "encode" in str(e).lower():
            error_msg = f"Error de codificación de caracteres: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/notificaciones/{notificacion_id}/archivo/base64")
async def obtener_archivo_base64(notificacion_id: int):
    """Obtener el archivo como base64 para evitar problemas de encoding"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"📎 Obteniendo archivo base64 de notificación {notificacion_id}")
        
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
        
        # Convertir a base64
        import base64
        archivo_base64 = base64.b64encode(archivo_bytes).decode('ascii')
        
        # Determinar MIME type
        mime_types = {
            'imagen': 'image/jpeg',
            'pdf': 'application/pdf', 
            'video': 'video/mp4'
        }
        
        mime_type = mime_types.get(archivo_tipo, 'application/octet-stream')
        
        # Crear nombre seguro para el archivo
        try:
            nombre_seguro = archivo_nombre
            # Verificar que no tenga caracteres problemáticos
            nombre_seguro.encode('ascii')
        except:
            # Crear nombre seguro si hay problemas
            import hashlib
            hash_nombre = hashlib.md5(archivo_nombre.encode('utf-8', errors='replace')).hexdigest()[:8]
            ext = archivo_nombre.split('.')[-1] if '.' in archivo_nombre else 'bin'
            ext_segura = ''.join(c for c in ext if c.isalnum())[:10]
            nombre_seguro = f"archivo_{hash_nombre}.{ext_segura}"
        
        print(f"📎 Archivo convertido a base64: {nombre_seguro} ({len(archivo_base64)} chars)")
        
        return {
            "base64": archivo_base64,
            "mime_type": mime_type,
            "archivo_nombre": nombre_seguro,
            "archivo_tipo": archivo_tipo,
            "size": len(archivo_bytes)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error obteniendo archivo base64: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar archivo: {str(e)}")

@app.get("/notificaciones/{notificacion_id}/archivo/mobile")
async def pagina_carga_archivo_mobile(notificacion_id: int):
    """Página de carga elegante que redirecciona automáticamente al archivo para móviles"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"📱 Generando página de carga móvil para archivo de notificación {notificacion_id}")
        
        # Verificar que la notificación existe y tiene archivo
        cursor.execute("""
            SELECT archivo_nombre, archivo_tipo
            FROM notificaciones
            WHERE id = %s AND archivo IS NOT NULL
        """, (notificacion_id,))
        
        resultado = cursor.fetchone()
        
        if not resultado:
            # Página de error elegante
            html_error = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Archivo no encontrado</title>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        margin: 0;
                        padding: 0;
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }}
                    .container {{
                        text-align: center;
                        padding: 2rem;
                        max-width: 400px;
                    }}
                    .error-icon {{
                        font-size: 4rem;
                        margin-bottom: 1rem;
                        opacity: 0.8;
                    }}
                    .title {{
                        font-size: 1.5rem;
                        margin-bottom: 1rem;
                        font-weight: 600;
                    }}
                    .message {{
                        opacity: 0.9;
                        line-height: 1.6;
                        margin-bottom: 2rem;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="error-icon">📄❌</div>
                    <div class="title">Archivo no encontrado</div>
                    <div class="message">El archivo que intentas abrir no está disponible o ha sido eliminado.</div>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(content=html_error, status_code=404)
        
        archivo_nombre = resultado[0]
        archivo_tipo = resultado[1]
        
        # Determinar ícono según tipo de archivo
        icono_archivo = "📄"
        if archivo_tipo:
            if "pdf" in archivo_tipo.lower():
                icono_archivo = "📑"
            elif "image" in archivo_tipo.lower():
                icono_archivo = "🖼️"
            elif "video" in archivo_tipo.lower():
                icono_archivo = "🎥"
            elif "audio" in archivo_tipo.lower():
                icono_archivo = "🎵"
            elif any(word in archivo_tipo.lower() for word in ["word", "doc"]):
                icono_archivo = "📝"
            elif any(word in archivo_tipo.lower() for word in ["excel", "sheet", "csv"]):
                icono_archivo = "📊"
            elif any(word in archivo_tipo.lower() for word in ["powerpoint", "presentation"]):
                icono_archivo = "📽️"
        
        # URL del archivo actual
        archivo_url = f"/notificaciones/{notificacion_id}/archivo"
        
        # Página HTML elegante de carga
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Abriendo archivo...</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    margin: 0;
                    padding: 0;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                }}
                .container {{
                    text-align: center;
                    padding: 2rem;
                    max-width: 400px;
                }}
                .file-icon {{
                    font-size: 4rem;
                    margin-bottom: 1rem;
                    animation: pulse 2s ease-in-out infinite;
                }}
                .title {{
                    font-size: 1.5rem;
                    margin-bottom: 1rem;
                    font-weight: 600;
                }}
                .filename {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 0.75rem 1.5rem;
                    border-radius: 25px;
                    margin-bottom: 1.5rem;
                    font-weight: 500;
                    word-break: break-word;
                }}
                .loading-text {{
                    opacity: 0.8;
                    margin-bottom: 2rem;
                    line-height: 1.6;
                }}
                .spinner {{
                    width: 40px;
                    height: 40px;
                    border: 3px solid rgba(255, 255, 255, 0.3);
                    border-top: 3px solid white;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin: 0 auto;
                }}
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
                @keyframes pulse {{
                    0%, 100% {{ transform: scale(1); opacity: 1; }}
                    50% {{ transform: scale(1.1); opacity: 0.8; }}
                }}
                .fallback-button {{
                    background: rgba(255, 255, 255, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    color: white;
                    padding: 0.75rem 1.5rem;
                    border-radius: 25px;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 1rem;
                    font-weight: 500;
                    transition: all 0.3s ease;
                }}
                .fallback-button:hover {{
                    background: rgba(255, 255, 255, 0.3);
                    border-color: rgba(255, 255, 255, 0.5);
                    transform: translateY(-2px);
                }}
                .hidden {{
                    display: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="file-icon">{icono_archivo}</div>
                <div class="title">Abriendo archivo</div>
                <div class="filename">{archivo_nombre or f'Archivo {notificacion_id}'}</div>
                <div class="loading-text">Preparando para abrir con tu aplicación favorita...</div>
                <div class="spinner"></div>
                
                <!-- Botón de respaldo que aparece después de unos segundos -->
                <a href="{archivo_url}" class="fallback-button hidden" id="fallbackBtn">
                    💾 Descargar manualmente si no se abre automáticamente
                </a>
            </div>

            <script>
                // Función para intentar abrir el archivo automáticamente
                function abrirArchivo() {{
                    console.log('🔄 Intentando abrir archivo automáticamente...');
                    
                    // Crear enlace temporal
                    const link = document.createElement('a');
                    link.href = '{archivo_url}';
                    link.download = '{archivo_nombre or f'archivo_{notificacion_id}'}';
                    link.target = '_blank';
                    link.rel = 'noopener noreferrer';
                    
                    // Agregar al DOM y hacer click
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    console.log('✅ Enlace de descarga activado');
                }}
                
                // Mostrar botón de respaldo después de 3 segundos
                setTimeout(() => {{
                    document.getElementById('fallbackBtn').classList.remove('hidden');
                }}, 3000);
                
                // Intentar cerrar la pestaña después de 5 segundos (solo funciona si fue abierta por script)
                setTimeout(() => {{
                    try {{
                        window.close();
                    }} catch (e) {{
                        console.log('No se pudo cerrar la pestaña automáticamente');
                    }}
                }}, 5000);
                
                // Ejecutar la descarga cuando la página cargue
                window.addEventListener('load', () => {{
                    setTimeout(abrirArchivo, 1000);
                }});
                
                // También intentar si el usuario hace click en cualquier lugar
                document.addEventListener('click', abrirArchivo);
            </script>
        </body>
        </html>
        """
        
        return HTMLResponse(content=html_content)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generando página de carga móvil: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar solicitud: {str(e)}")

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

@app.get("/notificaciones/{notificacion_id}/estadisticas")
async def obtener_estadisticas_notificacion(notificacion_id: int):
    """Obtener estadísticas de lectura de una notificación específica"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"📊 Obteniendo estadísticas para notificación {notificacion_id}")
        
        # Verificar que la notificación existe
        cursor.execute("""
            SELECT id, titulo, subtitulo, enviada_a_todos, fecha_envio 
            FROM notificaciones 
            WHERE id = %s
        """, (notificacion_id,))
        
        notificacion = cursor.fetchone()
        if not notificacion:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        # Determinar el universo de usuarios que pueden ver esta notificación
        if notificacion[3]:  # enviada_a_todos
            # Obtener todos los usuarios (sin filtro de activo)
            cursor.execute("""
                SELECT COUNT(*) as total_usuarios
                FROM usuarios
            """)
            total_usuarios_objetivo = cursor.fetchone()[0]
            
            # Obtener usuarios que han leído la notificación
            cursor.execute("""
                SELECT COUNT(DISTINCT nl.usuario_id) as usuarios_leido
                FROM notificacion_leidos nl
                INNER JOIN usuarios u ON nl.usuario_id = u.id
                WHERE nl.notificacion_id = %s
            """, (notificacion_id,))
            usuarios_leido = cursor.fetchone()[0]
            
        else:  # enviada a usuarios específicos
            # Obtener usuarios específicos destinatarios
            cursor.execute("""
                SELECT COUNT(*) as total_usuarios
                FROM notificacion_usuarios nu
                INNER JOIN usuarios u ON nu.usuario_id = u.id
                WHERE nu.notificacion_id = %s
            """, (notificacion_id,))
            total_usuarios_objetivo = cursor.fetchone()[0]
            
            # Obtener usuarios específicos que han leído la notificación
            cursor.execute("""
                SELECT COUNT(DISTINCT nl.usuario_id) as usuarios_leido
                FROM notificacion_leidos nl
                INNER JOIN notificacion_usuarios nu ON nl.usuario_id = nu.usuario_id
                INNER JOIN usuarios u ON nl.usuario_id = u.id
                WHERE nl.notificacion_id = %s 
                AND nu.notificacion_id = %s
            """, (notificacion_id, notificacion_id))
            usuarios_leido = cursor.fetchone()[0]
        
        usuarios_no_leido = total_usuarios_objetivo - usuarios_leido
        
        # Calcular porcentajes
        porcentaje_leido = round((usuarios_leido / total_usuarios_objetivo * 100), 2) if total_usuarios_objetivo > 0 else 0
        porcentaje_no_leido = round((usuarios_no_leido / total_usuarios_objetivo * 100), 2) if total_usuarios_objetivo > 0 else 0
        
        # Obtener detalles de usuarios que han leído (máximo 20 para no sobrecargar)
        if notificacion[3]:  # enviada_a_todos
            cursor.execute("""
                SELECT u.id, u.nombre_completo, u.correo, u.curp, nl.leida_en
                FROM notificacion_leidos nl
                INNER JOIN usuarios u ON nl.usuario_id = u.id
                WHERE nl.notificacion_id = %s
                ORDER BY nl.leida_en DESC
                LIMIT 20
            """, (notificacion_id,))
        else:  # usuarios específicos
            cursor.execute("""
                SELECT u.id, u.nombre_completo, u.correo, u.curp, nl.leida_en
                FROM notificacion_leidos nl
                INNER JOIN notificacion_usuarios nu ON nl.usuario_id = nu.usuario_id
                INNER JOIN usuarios u ON nl.usuario_id = u.id
                WHERE nl.notificacion_id = %s 
                AND nu.notificacion_id = %s
                ORDER BY nl.leida_en DESC
                LIMIT 20
            """, (notificacion_id, notificacion_id))
        
        usuarios_que_leyeron = []
        for fila in cursor.fetchall():
            usuarios_que_leyeron.append({
                "id": fila[0],
                "nombre_completo": fila[1],
                "correo": fila[2],
                "curp": fila[3],
                "leida_en": fila[4].isoformat() if fila[4] else None
            })
        
        # Obtener detalles de usuarios que NO han leído (máximo 20 para no sobrecargar)
        if notificacion[3]:  # enviada_a_todos
            cursor.execute("""
                SELECT u.id, u.nombre_completo, u.correo, u.curp
                FROM usuarios u
                WHERE u.id NOT IN (
                    SELECT nl.usuario_id 
                    FROM notificacion_leidos nl 
                    WHERE nl.notificacion_id = %s
                )
                ORDER BY u.nombre_completo
                LIMIT 20
            """, (notificacion_id,))
        else:  # usuarios específicos
            cursor.execute("""
                SELECT u.id, u.nombre_completo, u.correo, u.curp
                FROM notificacion_usuarios nu
                INNER JOIN usuarios u ON nu.usuario_id = u.id
                WHERE nu.notificacion_id = %s 
                AND u.id NOT IN (
                    SELECT nl.usuario_id 
                    FROM notificacion_leidos nl 
                    WHERE nl.notificacion_id = %s
                )
                ORDER BY u.nombre_completo
                LIMIT 20
            """, (notificacion_id, notificacion_id))
        
        usuarios_que_no_leyeron = []
        for fila in cursor.fetchall():
            usuarios_que_no_leyeron.append({
                "id": fila[0],
                "nombre_completo": fila[1],
                "correo": fila[2],
                "curp": fila[3]
            })
        
        estadisticas = {
            "notificacion_id": notificacion_id,
            "titulo": notificacion[1],
            "subtitulo": notificacion[2],
            "enviada_a_todos": notificacion[3],
            "fecha_envio": notificacion[4].isoformat() if notificacion[4] else None,
            "resumen": {
                "total_usuarios_objetivo": total_usuarios_objetivo,
                "usuarios_leido": usuarios_leido,
                "usuarios_no_leido": usuarios_no_leido,
                "porcentaje_leido": porcentaje_leido,
                "porcentaje_no_leido": porcentaje_no_leido
            },
            "usuarios_que_leyeron": usuarios_que_leyeron,
            "usuarios_que_no_leyeron": usuarios_que_no_leyeron,
            "nota": "Solo se muestran los primeros 20 usuarios de cada categoría"
        }
        
        print(f"✅ Estadísticas obtenidas: {usuarios_leido}/{total_usuarios_objetivo} usuarios han leído la notificación")
        
        return estadisticas
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas de notificación: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

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

# ==================== NUEVOS ENDPOINTS DE NOTIFICACIONES LEÍDAS/NO LEÍDAS ====================

# Función para crear tabla de notificación_leidos si no existe
def crear_tabla_notificacion_leidos():
    """Crear tabla notificacion_leidos si no existe"""
    try:
        if conn and cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notificacion_leidos (
                    id SERIAL PRIMARY KEY,
                    notificacion_id INTEGER NOT NULL REFERENCES notificaciones(id) ON DELETE CASCADE,
                    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                    leida_en TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'America/Mexico_City'),
                    device_id TEXT,
                    UNIQUE (notificacion_id, usuario_id)
                )
            """)
            
            # Crear índices si no existen
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS ix_notif_leidos_usuario 
                ON notificacion_leidos(usuario_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS ix_notif_leidos_notif 
                ON notificacion_leidos(notificacion_id)
            """)
            
            conn.commit()
            print("✅ Tabla notificacion_leidos verificada/creada correctamente")
            
    except Exception as e:
        print(f"❌ Error creando tabla notificacion_leidos: {e}")
        if conn:
            conn.rollback()

# Crear la tabla al inicializar
crear_tabla_notificacion_leidos()

# Endpoint mejorado para obtener notificaciones de usuario (compatibilidad con PWASUPER)
@app.get("/notificaciones/usuario/{usuario_id}")
async def obtener_notificaciones_usuario_mejorado(
    usuario_id: int, 
    limit: int = 20, 
    offset: int = 0
):
    """Obtener notificaciones específicas de un usuario con estado de lectura (compatibilidad con PWASUPER)"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"📱 Obteniendo notificaciones para usuario {usuario_id} (limit: {limit}, offset: {offset})")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, nombre_completo FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Configurar zona horaria para la sesión
        cursor.execute("SET TIME ZONE 'America/Mexico_City'")
        
        # Obtener notificaciones del usuario con estado de lectura
        cursor.execute("""
            SELECT DISTINCT n.id, n.titulo, n.subtitulo, n.descripcion, n.enlace_url,
                   n.archivo_nombre, n.archivo_tipo, n.enviada_a_todos,
                   n.fecha_creacion, n.fecha_envio,
                   CASE WHEN nl.id IS NOT NULL THEN TRUE ELSE FALSE END as leida
            FROM notificaciones n
            LEFT JOIN notificacion_usuarios nu ON n.id = nu.notificacion_id
            LEFT JOIN notificacion_leidos nl ON n.id = nl.notificacion_id AND nl.usuario_id = %s
            WHERE (n.enviada_a_todos = TRUE OR nu.usuario_id = %s)
            AND n.fecha_envio IS NOT NULL
            ORDER BY n.fecha_envio DESC NULLS LAST, n.fecha_creacion DESC
            LIMIT %s OFFSET %s
        """, (usuario_id, usuario_id, limit, offset))
        
        resultados = cursor.fetchall()
        
        # Obtener total de notificaciones del usuario
        cursor.execute("""
            SELECT COUNT(DISTINCT n.id)
            FROM notificaciones n
            LEFT JOIN notificacion_usuarios nu ON n.id = nu.notificacion_id
            WHERE (n.enviada_a_todos = TRUE OR nu.usuario_id = %s)
            AND n.fecha_envio IS NOT NULL
        """, (usuario_id,))
        
        total = cursor.fetchone()[0] or 0
        
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
                "tiene_archivo": bool(resultado[5]),
                "leida": bool(resultado[10])  # Nuevo campo con estado de lectura
            }
            notificaciones.append(notificacion)
        
        print(f"✅ {len(notificaciones)} notificaciones obtenidas para usuario {usuario[1]} (con estado de lectura)")
        
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

# ==================== FIN ENDPOINTS DE NOTIFICACIONES LEÍDAS/NO LEÍDAS ====================

# ==================== ENDPOINTS PARA GESTIÓN DE ROLES Y PERMISOS ====================

class UsuarioRolUpdate(BaseModel):
    rol: str  # 'admin' o 'user'

class UsuarioPasswordUpdate(BaseModel):
    nueva_contrasena: str

@app.put("/usuarios/{user_id}/rol")
async def cambiar_rol_usuario(user_id: int, rol_data: UsuarioRolUpdate):
    """Cambiar el rol de un usuario (admin/user)"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🔄 Cambiando rol del usuario {user_id} a {rol_data.rol}")
        
        # Validar rol
        if rol_data.rol not in ['admin', 'user']:
            raise HTTPException(status_code=400, detail="Rol inválido. Debe ser 'admin' o 'user'")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, nombre_completo FROM usuarios WHERE id = %s", (user_id,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar si la columna 'rol' existe, si no, agregarla
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'usuarios' AND column_name = 'rol'
        """)
        
        if not cursor.fetchone():
            print("📝 Agregando columna 'rol' a la tabla usuarios")
            cursor.execute("ALTER TABLE usuarios ADD COLUMN rol VARCHAR(10) DEFAULT 'user'")
            conn.commit()
        
        # Actualizar rol
        cursor.execute("UPDATE usuarios SET rol = %s WHERE id = %s", (rol_data.rol, user_id))
        conn.commit()
        
        print(f"✅ Rol del usuario {usuario[1]} cambiado a {rol_data.rol}")
        return {"mensaje": f"Rol actualizado a {rol_data.rol}", "usuario_id": user_id}
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cambiar rol: {str(e)}")

@app.put("/usuarios/{user_id}/password")
async def cambiar_contrasena_usuario(user_id: int, password_data: UsuarioPasswordUpdate):
    """Cambiar la contraseña de un usuario"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🔄 Cambiando contraseña del usuario {user_id}")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, nombre_completo FROM usuarios WHERE id = %s", (user_id,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Actualizar contraseña (sin encriptar, como en el resto del sistema)
        cursor.execute("UPDATE usuarios SET contrasena = %s WHERE id = %s", (password_data.nueva_contrasena, user_id))
        conn.commit()
        
        print(f"✅ Contraseña del usuario {usuario[1]} actualizada")
        return {"mensaje": "Contraseña actualizada exitosamente", "usuario_id": user_id}
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cambiar contraseña: {str(e)}")

# Modelo para actualizar cargo
class CargoUpdate(BaseModel):
    cargo: str

@app.put("/usuarios/{user_id}/cargo")
async def actualizar_cargo_usuario(user_id: int, cargo_data: CargoUpdate):
    """Actualizar el cargo de un usuario"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print(f"🔄 Actualizando cargo del usuario {user_id}")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, nombre_completo FROM usuarios WHERE id = %s", (user_id,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Validar que el cargo no esté vacío
        cargo = cargo_data.cargo.strip().upper()
        if not cargo:
            raise HTTPException(status_code=400, detail="El cargo no puede estar vacío")
        
        # Actualizar cargo
        cursor.execute("UPDATE usuarios SET cargo = %s WHERE id = %s", (cargo, user_id))
        conn.commit()
        
        print(f"✅ Cargo del usuario {usuario[1]} actualizado a: {cargo}")
        return {"success": True, "mensaje": "Cargo actualizado exitosamente", "usuario_id": user_id, "cargo": cargo}
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar cargo: {str(e)}")

@app.get("/usuarios/estadisticas")
async def obtener_estadisticas_usuarios():
    """Obtener estadísticas de usuarios del sistema"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print("📊 Obteniendo estadísticas de usuarios...")
        
        # Verificar si la columna 'rol' existe
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'usuarios' AND column_name = 'rol'
        """)
        
        tiene_columna_rol = bool(cursor.fetchone())
        
        if tiene_columna_rol:
            # Contar usuarios por rol
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN rol = 'admin' THEN 1 END) as admins,
                    COUNT(CASE WHEN rol = 'user' OR rol IS NULL THEN 1 END) as users
                FROM usuarios
            """)
            resultado = cursor.fetchone()
            total, admins, users = resultado
        else:
            # Si no existe la columna rol, todos son users
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            total = cursor.fetchone()[0]
            admins = 0
            users = total
        
        # Contar usuarios por cargo (top 5)
        cursor.execute("""
            SELECT cargo, COUNT(*) as cantidad 
            FROM usuarios 
            WHERE cargo IS NOT NULL AND cargo != ''
            GROUP BY cargo 
            ORDER BY cantidad DESC 
            LIMIT 5
        """)
        cargos = [{"cargo": row[0], "cantidad": row[1]} for row in cursor.fetchall()]
        
        # Obtener usuarios recientes (últimos 10)
        cursor.execute("""
            SELECT id, nombre_completo, correo, cargo, rol
            FROM usuarios 
            ORDER BY id DESC 
            LIMIT 10
        """)
        usuarios_recientes = []
        for row in cursor.fetchall():
            usuarios_recientes.append({
                "id": row[0],
                "nombre_completo": row[1],
                "correo": row[2],
                "cargo": row[3],
                "rol": row[4] if tiene_columna_rol and row[4] else 'user'
            })
        
        estadisticas = {
            "total_usuarios": total,
            "administradores": admins,
            "usuarios_normales": users,
            "cargos_populares": cargos,
            "usuarios_recientes": usuarios_recientes,
            "sistema_roles_activo": tiene_columna_rol
        }
        
        print(f"✅ Estadísticas obtenidas: {total} usuarios total")
        return estadisticas
        
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@app.get("/usuarios/buscar")
async def buscar_usuarios(correo: Optional[str] = None, nombre: Optional[str] = None, 
                         curp: Optional[str] = None, cargo: Optional[str] = None):
    """Buscar usuarios por diferentes criterios"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Construir consulta dinámica
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
            raise HTTPException(status_code=400, detail="Debe proporcionar al menos un criterio de búsqueda")
        
        # Verificar si existe columna rol
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'usuarios' AND column_name = 'rol'
        """)
        tiene_rol = bool(cursor.fetchone())
        
        consulta = f"""
            SELECT id, correo, nombre_completo, cargo, supervisor, curp, telefono, contrasena
            {'rol' if tiene_rol else ''}
            FROM usuarios 
            WHERE {' AND '.join(condiciones)}
            ORDER BY id DESC
        """
        
        if tiene_rol:
            consulta = consulta.replace("contrasena\n", "contrasena, ")
        
        print(f"🔍 Buscando usuarios con consulta: {consulta}")
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
                "contrasena": row[7],
                "rol": row[8] if tiene_rol and len(row) > 8 else 'user'
            }
            usuarios.append(usuario)
        
        print(f"✅ Búsqueda completada: {len(usuarios)} usuarios encontrados")
        return {"usuarios": usuarios}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

# ==================== MODELOS PARA ADMINISTRADORES ====================

# Permisos por defecto para cada rol
PERMISOS_ADMIN_DEFAULT = {
    "visor": True,
    "asistencia": True,
    "registros": True,
    "usuarios": True,
    "usuarios_acciones": True,
    "historiales": True,
    "notificaciones": True,
    "permisos": True,
    "configuracion": True
}

PERMISOS_USER_DEFAULT = {
    "visor": False,
    "asistencia": False,
    "registros": False,
    "usuarios": False,
    "usuarios_acciones": False,
    "historiales": False,
    "notificaciones": False,
    "permisos": False,
    "configuracion": False
}

class AdminUserCreate(BaseModel):
    username: str
    password: str
    rol: str = 'user'  # admin o user
    permisos: Optional[dict] = None  # Permisos personalizados
    es_territorial: bool = False  # Si es usuario territorial
    territorio: Optional[str] = None  # Territorio asignado (si es_territorial = True)
    nombre_completo: Optional[str] = None  # Nombre completo del usuario
    curp: Optional[str] = None  # CURP del usuario
    cargo: Optional[str] = None  # Cargo del usuario

class AdminUserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    permisos: Optional[dict] = None  # Permisos personalizados
    activo: Optional[bool] = None  # Estado activo/inactivo
    es_territorial: Optional[bool] = None  # Si es usuario territorial
    territorio: Optional[str] = None  # Territorio asignado
    nombre_completo: Optional[str] = None  # Nombre completo del usuario
    curp: Optional[str] = None  # CURP del usuario
    cargo: Optional[str] = None  # Cargo del usuario

# ==================== ENDPOINTS PARA GESTIÓN DE USUARIOS ADMINISTRATIVOS ====================

@app.get("/admin/usuarios")
async def obtener_usuarios_admin():
    """Obtener todos los usuarios administrativos de la tabla admin_users"""
    try:
        print("🔄 Obteniendo usuarios administrativos...")
        
        # Verificar conexión a la base de datos
        if not conn or not cursor:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        # Obtener todos los usuarios administrativos incluyendo permisos, estado activo, es_territorial y territorio
        cursor.execute("""
            SELECT id, username, rol, permisos, activo, es_territorial, territorio, nombre_completo, curp, cargo
            FROM admin_users 
            ORDER BY id ASC
        """)
        
        rows = cursor.fetchall()
        usuarios = []
        
        for row in rows:
            # Parsear permisos JSON o usar defaults
            permisos_str = row[3]
            if permisos_str:
                try:
                    permisos = json.loads(permisos_str)
                except:
                    permisos = PERMISOS_ADMIN_DEFAULT if row[2] == 'admin' else PERMISOS_USER_DEFAULT
            else:
                permisos = PERMISOS_ADMIN_DEFAULT if row[2] == 'admin' else PERMISOS_USER_DEFAULT
            
            # Estado activo (por defecto True si es NULL)
            activo = row[4] if row[4] is not None else True
            
            # Es territorial y territorio
            es_territorial = row[5] if row[5] is not None else False
            territorio = row[6]
            
            usuario = {
                "id": row[0],
                "username": row[1],
                "rol": row[2],
                "permisos": permisos,
                "activo": activo,
                "es_territorial": es_territorial,
                "territorio": territorio,
                "nombre_completo": row[7] or '',
                "curp": row[8] or '',
                "cargo": row[9] or ''
            }
            usuarios.append(usuario)
        
        print(f"✅ {len(usuarios)} usuarios administrativos obtenidos")
        return {"usuarios": usuarios}
        
    except Exception as e:
        print(f"❌ Error obteniendo usuarios administrativos: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

@app.post("/admin/usuarios")
async def crear_usuario_admin(usuario: AdminUserCreate):
    """Crear un nuevo usuario administrativo"""
    try:
        print(f"🔄 Creando usuario administrativo: {usuario.username}")
        
        # Verificar conexión
        if not conn or not cursor:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        # Verificar que el username no existe
        cursor.execute("SELECT id FROM admin_users WHERE username = %s", (usuario.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")
        
        # Validar rol
        if usuario.rol not in ['admin', 'user']:
            raise HTTPException(status_code=400, detail="El rol debe ser 'admin' o 'user'")
        
        # Hashear la contraseña
        hashed_password = pwd_context.hash(usuario.password)
        
        # Determinar permisos (usar los enviados o los por defecto según rol)
        if usuario.permisos:
            permisos_json = json.dumps(usuario.permisos)
        else:
            permisos_default = PERMISOS_ADMIN_DEFAULT if usuario.rol == 'admin' else PERMISOS_USER_DEFAULT
            permisos_json = json.dumps(permisos_default)
        
        # Validar territorio si es territorial
        territorio_valor = None
        if usuario.es_territorial:
            if not usuario.territorio:
                raise HTTPException(status_code=400, detail="Si es territorial, debe especificar un territorio")
            if usuario.territorio not in TERRITORIOS_SEMBRANDO_VIDA:
                raise HTTPException(status_code=400, detail="Territorio inválido. Debe ser uno de los territorios de Sembrando Vida.")
            territorio_valor = usuario.territorio
        
        # Preparar los nuevos campos (convertir a mayúsculas)
        nombre_completo_valor = usuario.nombre_completo.upper() if usuario.nombre_completo else None
        curp_valor = usuario.curp.upper() if usuario.curp else None
        cargo_valor = usuario.cargo.upper() if usuario.cargo else None
        
        # Insertar nuevo usuario con permisos, es_territorial y territorio
        cursor.execute("""
            INSERT INTO admin_users (username, password, rol, permisos, activo, es_territorial, territorio, nombre_completo, curp, cargo) 
            VALUES (%s, %s, %s, %s, TRUE, %s, %s, %s, %s, %s) 
            RETURNING id
        """, (usuario.username, hashed_password, usuario.rol, permisos_json, usuario.es_territorial, territorio_valor, nombre_completo_valor, curp_valor, cargo_valor))
        
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ Usuario administrativo creado con ID: {nuevo_id}" + (f" (territorial: {territorio_valor})" if usuario.es_territorial else ""))
        return {
            "message": "Usuario administrativo creado exitosamente",
            "id": nuevo_id,
            "username": usuario.username,
            "rol": usuario.rol,
            "permisos": json.loads(permisos_json),
            "activo": True,
            "es_territorial": usuario.es_territorial,
            "territorio": territorio_valor,
            "nombre_completo": nombre_completo_valor or '',
            "curp": curp_valor or '',
            "cargo": cargo_valor or ''
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error creando usuario administrativo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@app.get("/admin/usuarios/{user_id}")
async def obtener_usuario_admin(user_id: int):
    """Obtener información de un usuario administrativo específico"""
    try:
        print(f"🔄 Obteniendo usuario administrativo ID: {user_id}")
        
        cursor.execute("""
            SELECT id, username, rol, permisos, activo, es_territorial, territorio, nombre_completo, curp, cargo
            FROM admin_users 
            WHERE id = %s
        """, (user_id,))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Usuario administrativo no encontrado")
        
        # Parsear permisos
        permisos_str = row[3]
        if permisos_str:
            try:
                permisos = json.loads(permisos_str)
            except:
                permisos = PERMISOS_ADMIN_DEFAULT if row[2] == 'admin' else PERMISOS_USER_DEFAULT
        else:
            permisos = PERMISOS_ADMIN_DEFAULT if row[2] == 'admin' else PERMISOS_USER_DEFAULT
        
        # Estado activo (por defecto True si es NULL)
        activo = row[4] if row[4] is not None else True
        
        # Es territorial y territorio
        es_territorial = row[5] if row[5] is not None else False
        territorio = row[6]
        
        usuario = {
            "id": row[0],
            "username": row[1],
            "rol": row[2],
            "permisos": permisos,
            "activo": activo,
            "es_territorial": es_territorial,
            "territorio": territorio,
            "nombre_completo": row[7] or '',
            "curp": row[8] or '',
            "cargo": row[9] or ''
        }
        
        print(f"✅ Usuario administrativo obtenido: {usuario['username']}")
        return usuario
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error obteniendo usuario administrativo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")

@app.put("/admin/usuarios/{user_id}")
async def actualizar_usuario_admin(user_id: int, usuario: AdminUserUpdate):
    """Actualizar información de un usuario administrativo"""
    try:
        print(f"🔄 Actualizando usuario administrativo ID: {user_id}")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM admin_users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario administrativo no encontrado")
        
        # Preparar campos a actualizar
        campos_actualizar = []
        valores = []
        
        if usuario.username:
            # Verificar que el nuevo username no existe (excepto el actual)
            cursor.execute("SELECT id FROM admin_users WHERE username = %s AND id != %s", 
                          (usuario.username, user_id))
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")
            campos_actualizar.append("username = %s")
            valores.append(usuario.username)
        
        if usuario.password:
            hashed_password = pwd_context.hash(usuario.password)
            campos_actualizar.append("password = %s")
            valores.append(hashed_password)
        
        if usuario.rol:
            if usuario.rol not in ['admin', 'user']:
                raise HTTPException(status_code=400, detail="El rol debe ser 'admin' o 'user'")
            campos_actualizar.append("rol = %s")
            valores.append(usuario.rol)
        
        if usuario.permisos is not None:
            permisos_json = json.dumps(usuario.permisos)
            campos_actualizar.append("permisos = %s")
            valores.append(permisos_json)
        
        # Campo activo (puede ser True o False)
        if usuario.activo is not None:
            campos_actualizar.append("activo = %s")
            valores.append(usuario.activo)
        
        # Campo es_territorial
        if usuario.es_territorial is not None:
            campos_actualizar.append("es_territorial = %s")
            valores.append(usuario.es_territorial)
            
            # Si se desactiva territorial, limpiar el territorio
            if not usuario.es_territorial:
                campos_actualizar.append("territorio = %s")
                valores.append(None)
        
        # Campo territorio (solo si es territorial)
        if usuario.territorio is not None:
            if usuario.territorio and usuario.territorio not in TERRITORIOS_SEMBRANDO_VIDA:
                raise HTTPException(status_code=400, detail="Territorio inválido. Debe ser uno de los territorios de Sembrando Vida.")
            campos_actualizar.append("territorio = %s")
            valores.append(usuario.territorio if usuario.territorio else None)
        
        # Campo nombre_completo (convertir a mayúsculas)
        if usuario.nombre_completo is not None:
            campos_actualizar.append("nombre_completo = %s")
            valores.append(usuario.nombre_completo.upper() if usuario.nombre_completo else None)
        
        # Campo curp (convertir a mayúsculas)
        if usuario.curp is not None:
            campos_actualizar.append("curp = %s")
            valores.append(usuario.curp.upper() if usuario.curp else None)
        
        # Campo cargo (convertir a mayúsculas)
        if usuario.cargo is not None:
            campos_actualizar.append("cargo = %s")
            valores.append(usuario.cargo.upper() if usuario.cargo else None)
        
        if not campos_actualizar:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        # Actualizar usuario
        valores.append(user_id)
        query = f"UPDATE admin_users SET {', '.join(campos_actualizar)} WHERE id = %s"
        cursor.execute(query, valores)
        conn.commit()
        
        # Obtener usuario actualizado
        cursor.execute("SELECT id, username, rol, permisos, activo, es_territorial, territorio, nombre_completo, curp, cargo FROM admin_users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        
        # Parsear permisos
        permisos_str = row[3]
        if permisos_str:
            try:
                permisos = json.loads(permisos_str)
            except:
                permisos = PERMISOS_ADMIN_DEFAULT if row[2] == 'admin' else PERMISOS_USER_DEFAULT
        else:
            permisos = PERMISOS_ADMIN_DEFAULT if row[2] == 'admin' else PERMISOS_USER_DEFAULT
        
        # Estado activo
        activo = row[4] if row[4] is not None else True
        
        # Es territorial y territorio
        es_territorial = row[5] if row[5] is not None else False
        territorio = row[6]
        
        usuario_actualizado = {
            "id": row[0],
            "username": row[1],
            "rol": row[2],
            "permisos": permisos,
            "activo": activo,
            "es_territorial": es_territorial,
            "territorio": territorio,
            "nombre_completo": row[7] or '',
            "curp": row[8] or '',
            "cargo": row[9] or ''
        }
        
        print(f"✅ Usuario administrativo actualizado: {usuario_actualizado['username']} (activo: {activo}, territorial: {es_territorial})")
        return {
            "message": "Usuario administrativo actualizado exitosamente",
            **usuario_actualizado
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error actualizando usuario administrativo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")

@app.delete("/admin/usuarios/{user_id}")
async def eliminar_usuario_admin(user_id: int):
    """Eliminar un usuario administrativo"""
    try:
        print(f"🔄 Eliminando usuario administrativo ID: {user_id}")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT username FROM admin_users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Usuario administrativo no encontrado")
        
        username = row[0]
        
        # Eliminar usuario
        cursor.execute("DELETE FROM admin_users WHERE id = %s", (user_id,))
        conn.commit()
        
        print(f"✅ Usuario administrativo eliminado: {username}")
        return {
            "message": "Usuario administrativo eliminado exitosamente",
            "username": username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error eliminando usuario administrativo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")

@app.put("/admin/usuarios/{user_id}/rol")
async def cambiar_rol_usuario_admin(user_id: int, datos: dict):
    """Cambiar el rol de un usuario administrativo"""
    try:
        print(f"🔄 Cambiando rol de usuario administrativo ID: {user_id}")
        
        rol = datos.get("rol")
        if not rol or rol not in ['admin', 'user']:
            raise HTTPException(status_code=400, detail="El rol debe ser 'admin' o 'user'")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT username FROM admin_users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Usuario administrativo no encontrado")
        
        username = row[0]
        
        # Actualizar rol
        cursor.execute("UPDATE admin_users SET rol = %s WHERE id = %s", (rol, user_id))
        conn.commit()
        
        print(f"✅ Rol cambiado para usuario {username} a: {rol}")
        return {
            "message": f"Rol cambiado exitosamente a {rol}",
            "username": username,
            "nuevo_rol": rol
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error cambiando rol: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cambiar rol: {str(e)}")

@app.put("/admin/usuarios/{user_id}/password")
async def resetear_password_usuario_admin(user_id: int, datos: dict):
    """Resetear la contraseña de un usuario administrativo"""
    try:
        print(f"🔄 Reseteando contraseña de usuario administrativo ID: {user_id}")
        
        password = datos.get("password")
        if not password:
            raise HTTPException(status_code=400, detail="La contraseña es requerida")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT username FROM admin_users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Usuario administrativo no encontrado")
        
        username = row[0]
        
        # Hashear nueva contraseña
        hashed_password = pwd_context.hash(password)
        
        # Actualizar contraseña
        cursor.execute("UPDATE admin_users SET password = %s WHERE id = %s", (hashed_password, user_id))
        conn.commit()
        
        print(f"✅ Contraseña reseteada para usuario: {username}")
        return {
            "message": "Contraseña reseteada exitosamente",
            "username": username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error reseteando contraseña: {e}")
        raise HTTPException(status_code=500, detail=f"Error al resetear contraseña: {str(e)}")

@app.get("/admin/usuarios/estadisticas")
async def obtener_estadisticas_admin():
    """Obtener estadísticas de usuarios administrativos"""
    try:
        print("🔄 Obteniendo estadísticas de usuarios administrativos...")
        
        # Total de usuarios admin
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        total_usuarios = cursor.fetchone()[0]
        
        # Usuarios por rol
        cursor.execute("SELECT rol, COUNT(*) FROM admin_users GROUP BY rol")
        roles_data = cursor.fetchall()
        
        usuarios_por_rol = {}
        for rol, count in roles_data:
            usuarios_por_rol[rol] = count
        
        estadisticas = {
            "total_usuarios": total_usuarios,
            "usuarios_por_rol": usuarios_por_rol,
            "roles_disponibles": ["admin", "user"]
        }
        
        print(f"✅ Estadísticas obtenidas: {estadisticas}")
        return estadisticas
        
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@app.get("/admin/usuarios/buscar")
async def buscar_usuarios_admin(username: Optional[str] = None, rol: Optional[str] = None):
    """Buscar usuarios administrativos por criterios específicos"""
    try:
        print(f"🔄 Buscando usuarios administrativos: username={username}, rol={rol}")
        
        # Construir consulta base
        query = "SELECT id, username, rol FROM admin_users WHERE 1=1"
        params = []
        
        # Agregar filtros
        if username:
            query += " AND username ILIKE %s"
            params.append(f"%{username}%")
        
        if rol:
            if rol not in ['admin', 'user']:
                raise HTTPException(status_code=400, detail="El rol debe ser 'admin' o 'user'")
            query += " AND rol = %s"
            params.append(rol)
        
        query += " ORDER BY id ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        usuarios = []
        for row in rows:
            usuario = {
                "id": row[0],
                "username": row[1],
                "rol": row[2]
            }
            usuarios.append(usuario)
        
        print(f"✅ Búsqueda completada: {len(usuarios)} usuarios encontrados")
        return {"usuarios": usuarios}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

@app.get("/admin/auth/validar")
async def validar_permisos_admin():
    """Validar los permisos del usuario administrativo actual"""
    try:
        print("🔐 Validando permisos de usuario administrativo")
        
        # Este endpoint simula la validación de permisos para admin
        # En una implementación real, aquí se verificaría el token JWT
        return {
            "valido": True,
            "rol": "admin",
            "permisos": [
                "leer_usuarios_admin",
                "crear_usuarios_admin", 
                "editar_usuarios_admin",
                "eliminar_usuarios_admin",
                "cambiar_roles_admin",
                "gestionar_admin_sistema"
            ]
        }
        
    except Exception as e:
        print(f"❌ Error validando permisos admin: {e}")
        raise HTTPException(status_code=500, detail=f"Error al validar permisos: {str(e)}")

# ==================== FIN ENDPOINTS DE GESTIÓN DE USUARIOS ADMINISTRATIVOS ====================

@app.get("/auth/validar")
async def validar_permisos_usuario():
    """Validar los permisos del usuario actual basado en el token"""
    try:
        # Este endpoint simula la validación de permisos
        # En una implementación real, aquí se verificaría el token JWT
        print("🔐 Validando permisos de usuario")
        
        return {
            "valido": True,
            "rol": "admin",  # Por ahora siempre admin para el panel de administración
            "permisos": [
                "leer_usuarios",
                "crear_usuarios", 
                "editar_usuarios",
                "eliminar_usuarios",
                "cambiar_roles",
                "gestionar_notificaciones"
            ]
        }
        
    except Exception as e:
        print(f"❌ Error validando permisos: {e}")
        raise HTTPException(status_code=500, detail=f"Error al validar permisos: {str(e)}")

@app.get("/health")
async def verificar_salud_api():
    """Endpoint para verificar que la API está funcionando"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "database_connected": bool(conn)
    }

# ==================== FIN ENDPOINTS DE GESTIÓN DE ROLES Y PERMISOS ====================

# ==================== ENDPOINT PARA ELIMINAR TODAS LAS IMÁGENES ====================

@app.delete("/imagenes/eliminar-todas")
async def eliminar_todas_imagenes():
    """
    Endpoint para eliminar TODAS las imágenes (fotos) almacenadas en la base de datos.
    Elimina:
    - Todas las fotos de registros de actividades
    - Todas las fotos de entrada/salida de asistencias
    - Los archivos físicos del directorio de fotos
    """
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print("🗑️ INICIANDO ELIMINACIÓN DE TODAS LAS IMÁGENES...")
        
        # Contadores
        fotos_bd_eliminadas = 0
        fotos_archivo_eliminadas = 0
        fotos_no_encontradas = 0
        errores = 0
        
        # 1. Obtener todas las fotos de registros
        try:
            cursor.execute("SELECT DISTINCT foto_url FROM registros WHERE foto_url IS NOT NULL")
            fotos_registros = cursor.fetchall()
            print(f"📸 Se encontraron {len(fotos_registros)} fotos en registros")
            
            for foto_row in fotos_registros:
                foto_path = foto_row[0]
                if foto_path:
                    if os.path.exists(foto_path):
                        try:
                            os.remove(foto_path)
                            fotos_archivo_eliminadas += 1
                            print(f"   ✅ Eliminado: {foto_path}")
                        except Exception as e:
                            errores += 1
                            print(f"   ❌ Error eliminando {foto_path}: {e}")
                    else:
                        fotos_no_encontradas += 1
                        print(f"   ⚠️ Archivo no encontrado: {foto_path}")
        except Exception as e:
            print(f"⚠️ Error al obtener fotos de registros: {e}")
            errores += 1
        
        # 2. Obtener todas las fotos de asistencias (entrada y salida)
        try:
            cursor.execute("""
                SELECT DISTINCT foto_entrada_url, foto_salida_url 
                FROM asistencias 
                WHERE foto_entrada_url IS NOT NULL OR foto_salida_url IS NOT NULL
            """)
            fotos_asistencias = cursor.fetchall()
            print(f"📸 Se encontraron {len(fotos_asistencias)} registros de asistencia con fotos")
            
            for foto_row in fotos_asistencias:
                # Foto de entrada
                if foto_row[0]:
                    foto_path = foto_row[0]
                    if os.path.exists(foto_path):
                        try:
                            os.remove(foto_path)
                            fotos_archivo_eliminadas += 1
                            print(f"   ✅ Eliminado: {foto_path}")
                        except Exception as e:
                            errores += 1
                            print(f"   ❌ Error eliminando {foto_path}: {e}")
                    else:
                        fotos_no_encontradas += 1
                        print(f"   ⚠️ Archivo no encontrado: {foto_path}")
                
                # Foto de salida
                if foto_row[1]:
                    foto_path = foto_row[1]
                    if os.path.exists(foto_path):
                        try:
                            os.remove(foto_path)
                            fotos_archivo_eliminadas += 1
                            print(f"   ✅ Eliminado: {foto_path}")
                        except Exception as e:
                            errores += 1
                            print(f"   ❌ Error eliminando {foto_path}: {e}")
                    else:
                        fotos_no_encontradas += 1
                        print(f"   ⚠️ Archivo no encontrado: {foto_path}")
        except Exception as e:
            print(f"⚠️ Error al obtener fotos de asistencias: {e}")
            errores += 1
        
        # 3. Limpiar referencias en la base de datos
        try:
            # Actualizar registros estableciendo foto_url en NULL
            cursor.execute("UPDATE registros SET foto_url = NULL WHERE foto_url IS NOT NULL")
            registros_limpiados = cursor.rowcount
            print(f"🗑️ {registros_limpiados} registros limpios en la BD")
            
            # Actualizar asistencias estableciendo fotos en NULL
            cursor.execute("UPDATE asistencias SET foto_entrada_url = NULL WHERE foto_entrada_url IS NOT NULL")
            entrada_limpiadas = cursor.rowcount
            
            cursor.execute("UPDATE asistencias SET foto_salida_url = NULL WHERE foto_salida_url IS NOT NULL")
            salida_limpiadas = cursor.rowcount
            
            print(f"🗑️ {entrada_limpiadas} fotos de entrada limpias en la BD")
            print(f"🗑️ {salida_limpiadas} fotos de salida limpias en la BD")
            
            fotos_bd_eliminadas = registros_limpiados + entrada_limpiadas + salida_limpiadas
            
            conn.commit()
            print("✅ Cambios confirmados en la base de datos")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error limpiando la base de datos: {e}")
            errores += 1
        
        # 4. Limpiar archivos huérfanos en el directorio de fotos
        try:
            if os.path.exists(FOTOS_DIR):
                archivos_directorio = os.listdir(FOTOS_DIR)
                print(f"📁 Se encontraron {len(archivos_directorio)} archivos en el directorio de fotos")
                
                for archivo in archivos_directorio:
                    ruta_archivo = os.path.join(FOTOS_DIR, archivo)
                    if os.path.isfile(ruta_archivo):
                        try:
                            os.remove(ruta_archivo)
                            fotos_archivo_eliminadas += 1
                            print(f"   ✅ Eliminado archivo huérfano: {archivo}")
                        except Exception as e:
                            errores += 1
                            print(f"   ❌ Error eliminando archivo {archivo}: {e}")
        except Exception as e:
            print(f"⚠️ Error limpiando directorio de fotos: {e}")
            errores += 1
        
        # Preparar resumen
        resumen = {
            "status": "success",
            "message": "Eliminación de imágenes completada",
            "estadisticas": {
                "fotos_bd_limpiadas": fotos_bd_eliminadas,
                "archivos_eliminados": fotos_archivo_eliminadas,
                "archivos_no_encontrados": fotos_no_encontradas,
                "total_eliminado": fotos_archivo_eliminadas + fotos_no_encontradas,
                "errores_encontrados": errores
            },
            "timestamp": datetime.now().isoformat()
        }
        
        print("\n✅ ELIMINACIÓN COMPLETADA:")
        print(f"   📸 Fotos en BD limpiadas: {fotos_bd_eliminadas}")
        print(f"   🗑️ Archivos eliminados: {fotos_archivo_eliminadas}")
        print(f"   ⚠️ Archivos no encontrados: {fotos_no_encontradas}")
        print(f"   ❌ Errores: {errores}")
        
        return resumen
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error general en eliminación de imágenes: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar imágenes: {str(e)}")

# ==================== FIN ENDPOINT ELIMINAR IMÁGENES ====================

# ==================== NUEVO ENDPOINT: DESCARGAR BD COMPLETA RÁPIDA ====================

@app.get("/descargar-bd-completa", response_class=StreamingResponse)
async def descargar_bd_completa():
    """
    Endpoint optimizado para descargar TODA la base de datos en formato SQL de forma MUY RÁPIDA
    Usa streaming para manejo eficiente de memoria
    """
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print("🚀 [BD COMPLETA] Iniciando descarga rápida de base de datos completa...")
        timestamp = datetime.now().isoformat().replace(':', '-')
        nombre_archivo = f"BASE_DATOS_COMPLETA_{timestamp}.sql"
        
        async def generar_sql():
            """Generador de SQL para streaming eficiente"""
            
            try:
                # Header
                yield f"""-- ===============================================
-- EXPORTACIÓN COMPLETA BASE DE DATOS app_registros
-- ===============================================
-- Generado: {datetime.now().isoformat()}
-- Servidor: app_registros (PostgreSQL)
-- ===============================================

"""
                
                # 1. TABLA USUARIOS - Crear e insertar datos de forma rápida
                print("📝 Procesando tabla usuarios...")
                yield """-- ======== TABLA: USUARIOS ========
DROP TABLE IF EXISTS usuarios CASCADE;

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    correo VARCHAR(255) UNIQUE NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    cargo VARCHAR(255),
    supervisor VARCHAR(255),
    contrasena VARCHAR(255) NOT NULL,
    curp VARCHAR(18) UNIQUE,
    telefono VARCHAR(20),
    rol VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""
                
                # Obtener usuarios de forma rápida
                cursor.execute("""
                    SELECT id, correo, nombre_completo, cargo, supervisor, 
                           contrasena, curp, telefono, rol
                    FROM usuarios 
                    ORDER BY id ASC
                """)
                
                usuarios_data = cursor.fetchall()
                print(f"📊 Obtenidos {len(usuarios_data)} usuarios")
                
                if usuarios_data:
                    yield "INSERT INTO usuarios (id, correo, nombre_completo, cargo, supervisor, contrasena, curp, telefono, rol) VALUES\n"
                    
                    for idx, row in enumerate(usuarios_data):
                        id_u, correo, nombre, cargo, supervisor, contrasena, curp, telefono, rol = row
                        
                        # Escapar comillas simples
                        correo = (correo or '').replace("'", "''")
                        nombre = (nombre or '').replace("'", "''")
                        cargo = (cargo or '').replace("'", "''")
                        supervisor = (supervisor or '').replace("'", "''")
                        contrasena = (contrasena or '').replace("'", "''")
                        curp = (curp or '').replace("'", "''")
                        telefono = (telefono or '').replace("'", "''")
                        rol = (rol or 'user').replace("'", "''")
                        
                        coma = "," if idx < len(usuarios_data) - 1 else ";"
                        yield f"({id_u}, '{correo}', '{nombre}', '{cargo}', '{supervisor}', '{contrasena}', '{curp}', '{telefono}', '{rol}'){coma}\n"
                
                yield "\n"
                
                # 2. TABLA REGISTROS - Insertar datos de forma rápida
                print("📋 Procesando tabla registros...")
                yield """-- ======== TABLA: REGISTROS ========
DROP TABLE IF EXISTS registros CASCADE;

CREATE TABLE registros (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    descripcion TEXT,
    foto_url VARCHAR(500),
    fecha_hora TIMESTAMP NOT NULL,
    tipo_actividad VARCHAR(50) DEFAULT 'campo',
    categoria_actividad VARCHAR(100),
    categoria_actividad_otro VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""
                
                # Obtener registros de forma rápida
                cursor.execute("""
                    SELECT id, usuario_id, latitud, longitud, descripcion, 
                           foto_url, fecha_hora, tipo_actividad, categoria_actividad, categoria_actividad_otro
                    FROM registros 
                    ORDER BY id ASC
                """)
                
                registros_data = cursor.fetchall()
                print(f"📊 Obtenidos {len(registros_data)} registros")
                
                if registros_data:
                    yield "INSERT INTO registros (id, usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora, tipo_actividad, categoria_actividad, categoria_actividad_otro) VALUES\n"
                    
                    for idx, row in enumerate(registros_data):
                        id_r, usuario_id, lat, lon, desc, foto, fecha, tipo, cat_act, cat_act_otro = row
                        
                        # Escapar comillas simples
                        desc = (desc or '').replace("'", "''")
                        foto = (foto or '').replace("'", "''")
                        tipo = (tipo or 'campo').replace("'", "''")
                        cat_act = (cat_act or '').replace("'", "''")
                        cat_act_otro = (cat_act_otro or '').replace("'", "''")
                        
                        lat_str = str(lat) if lat is not None else "NULL"
                        lon_str = str(lon) if lon is not None else "NULL"
                        fecha_str = str(fecha) if fecha else "NOW()"
                        cat_act_str = f"'{cat_act}'" if cat_act else "NULL"
                        cat_act_otro_str = f"'{cat_act_otro}'" if cat_act_otro else "NULL"
                        
                        coma = "," if idx < len(registros_data) - 1 else ";"
                        yield f"({id_r}, {usuario_id}, {lat_str}, {lon_str}, '{desc}', '{foto}', '{fecha_str}', '{tipo}', {cat_act_str}, {cat_act_otro_str}){coma}\n"
                
                yield "\n"
                
                # 3. TABLA ASISTENCIAS - Insertar datos de forma rápida
                print("🕐 Procesando tabla asistencias...")
                yield """-- ======== TABLA: ASISTENCIAS ========
DROP TABLE IF EXISTS asistencias CASCADE;

CREATE TABLE asistencias (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    fecha DATE NOT NULL,
    hora_entrada TIMESTAMP,
    hora_salida TIMESTAMP,
    latitud_entrada DECIMAL(10, 8),
    longitud_entrada DECIMAL(11, 8),
    latitud_salida DECIMAL(10, 8),
    longitud_salida DECIMAL(11, 8),
    foto_entrada_url VARCHAR(500),
    foto_salida_url VARCHAR(500),
    descripcion_entrada TEXT,
    descripcion_salida TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""
                
                # Obtener asistencias de forma rápida
                cursor.execute("""
                    SELECT id, usuario_id, fecha, hora_entrada, hora_salida,
                           latitud_entrada, longitud_entrada, latitud_salida, 
                           longitud_salida, foto_entrada_url, foto_salida_url,
                           descripcion_entrada, descripcion_salida
                    FROM asistencias 
                    ORDER BY id ASC
                """)
                
                asistencias_data = cursor.fetchall()
                print(f"📊 Obtenidas {len(asistencias_data)} asistencias")
                
                if asistencias_data:
                    yield "INSERT INTO asistencias (id, usuario_id, fecha, hora_entrada, hora_salida, latitud_entrada, longitud_entrada, latitud_salida, longitud_salida, foto_entrada_url, foto_salida_url, descripcion_entrada, descripcion_salida) VALUES\n"
                    
                    for idx, row in enumerate(asistencias_data):
                        id_a, usuario_id, fecha, hora_ent, hora_sal, lat_ent, lon_ent, lat_sal, lon_sal, foto_ent, foto_sal, desc_ent, desc_sal = row
                        
                        # Escapar comillas simples
                        foto_ent = (foto_ent or '').replace("'", "''")
                        foto_sal = (foto_sal or '').replace("'", "''")
                        desc_ent = (desc_ent or '').replace("'", "''")
                        desc_sal = (desc_sal or '').replace("'", "''")
                        
                        fecha_str = str(fecha) if fecha else "CURRENT_DATE"
                        hora_ent_str = f"'{str(hora_ent)}'" if hora_ent else "NULL"
                        hora_sal_str = f"'{str(hora_sal)}'" if hora_sal else "NULL"
                        lat_ent_str = str(lat_ent) if lat_ent is not None else "NULL"
                        lon_ent_str = str(lon_ent) if lon_ent is not None else "NULL"
                        lat_sal_str = str(lat_sal) if lat_sal is not None else "NULL"
                        lon_sal_str = str(lon_sal) if lon_sal is not None else "NULL"
                        
                        coma = "," if idx < len(asistencias_data) - 1 else ";"
                        yield f"({id_a}, {usuario_id}, '{fecha_str}', {hora_ent_str}, {hora_sal_str}, {lat_ent_str}, {lon_ent_str}, {lat_sal_str}, {lon_sal_str}, '{foto_ent}', '{foto_sal}', '{desc_ent}', '{desc_sal}'){coma}\n"
                
                yield "\n"
                
                # 4. Crear índices para optimización
                print("🔍 Agregando índices...")
                yield """-- ======== ÍNDICES PARA OPTIMIZACIÓN ========
CREATE INDEX IF NOT EXISTS idx_usuarios_correo ON usuarios(correo);
CREATE INDEX IF NOT EXISTS idx_usuarios_curp ON usuarios(curp);
CREATE INDEX IF NOT EXISTS idx_registros_usuario ON registros(usuario_id);
CREATE INDEX IF NOT EXISTS idx_registros_fecha ON registros(fecha_hora);
CREATE INDEX IF NOT EXISTS idx_asistencias_usuario ON asistencias(usuario_id);
CREATE INDEX IF NOT EXISTS idx_asistencias_fecha ON asistencias(fecha);

-- ======== FIN DE EXPORTACIÓN ========
-- Total registros exportados: usuarios={}, registros={}, asistencias={}
-- Fecha: {}
-- ===============================================
""".format(len(usuarios_data), len(registros_data), len(asistencias_data), 
           datetime.now().isoformat())
                
                print("✅ Descarga de BD completa generada exitosamente")
                
            except Exception as e:
                print(f"❌ Error generando SQL: {e}")
                yield f"-- ERROR: {str(e)}\n"
        
        # Headers para descarga
        headers = {
            "Content-Disposition": f"attachment; filename={nombre_archivo}",
            "Content-Type": "application/sql; charset=utf-8"
        }
        
        print(f"📥 Iniciando descarga del archivo: {nombre_archivo}")
        return StreamingResponse(
            content=generar_sql(),
            media_type="application/sql; charset=utf-8",
            headers=headers
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en descarga de BD completa: {e}")
        raise HTTPException(status_code=500, detail=f"Error al descargar base de datos: {str(e)}")

# ==================== FIN DESCARGA BD COMPLETA ====================

# ==================== NUEVO ENDPOINT: EXPORTAR REGISTROS A CSV ====================

@app.get("/exportar-registros-csv", response_class=StreamingResponse)
async def exportar_registros_csv():
    """
    Endpoint optimizado para exportar TODOS los registros de actividades en formato CSV
    Usa streaming para manejo eficiente de memoria
    Incluye: Modalidad (campo/gabinete), Tipo de Actividad y Tipo de Actividad Otro
    """
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        print("📊 [ACTIVIDADES CSV] Iniciando exportación de actividades a CSV...")
        timestamp = datetime.now().isoformat().replace(':', '-')
        nombre_archivo = f"ACTIVIDADES_{timestamp}.csv"
        
        async def generar_csv():
            """Generador de CSV para streaming eficiente"""
            
            try:
                # Header CSV - Incluye Tipo_Actividad (modalidad) y Categoria_Actividad (tipo de actividad)
                header = "ID,Usuario_ID,Nombre_Usuario,Correo_Usuario,Cargo,Latitud,Longitud,Descripcion,Modalidad,Tipo_Actividad,Tipo_Actividad_Otro,Fecha_Hora,Foto_URL\n"
                yield header
                
                print("📝 Procesando registros...")
                
                # Obtener registros con información de usuarios de forma rápida
                # Incluye categoria_actividad (tipo de actividad) y categoria_actividad_otro
                cursor.execute("""
                    SELECT 
                        r.id, 
                        r.usuario_id, 
                        u.nombre_completo, 
                        u.correo, 
                        u.cargo,
                        r.latitud, 
                        r.longitud, 
                        r.descripcion, 
                        r.tipo_actividad,
                        r.categoria_actividad,
                        r.categoria_actividad_otro,
                        r.fecha_hora,
                        r.foto_url
                    FROM registros r
                    LEFT JOIN usuarios u ON r.usuario_id = u.id
                    ORDER BY r.id ASC
                """)
                
                # Procesar resultados en chunks
                chunk_size = 500
                registros_procesados = 0
                
                while True:
                    registros = cursor.fetchmany(chunk_size)
                    if not registros:
                        break
                    
                    for registro in registros:
                        # Ahora incluye categoria_actividad y categoria_actividad_otro
                        id_r, usuario_id, nombre, correo, cargo, lat, lon, desc, modalidad, tipo_actividad, tipo_actividad_otro, fecha, foto = registro
                        
                        # Escapar comillas y saltos de línea en campos de texto
                        nombre = (nombre or '').replace('"', '""').replace('\n', ' ').replace('\r', '')
                        correo = (correo or '').replace('"', '""').replace('\n', ' ').replace('\r', '')
                        cargo = (cargo or '').replace('"', '""').replace('\n', ' ').replace('\r', '')
                        desc = (desc or '').replace('"', '""').replace('\n', ' ').replace('\r', '')
                        modalidad = (modalidad or 'campo').replace('"', '""')
                        tipo_actividad = (tipo_actividad or '').replace('"', '""').replace('\n', ' ').replace('\r', '')
                        tipo_actividad_otro = (tipo_actividad_otro or '').replace('"', '""').replace('\n', ' ').replace('\r', '')
                        foto = (foto or '').replace('"', '""')
                        
                        # Formatear fecha
                        fecha_str = str(fecha) if fecha else ''
                        
                        # Construir línea CSV con nuevos campos
                        # Columnas: ID,Usuario_ID,Nombre_Usuario,Correo_Usuario,Cargo,Latitud,Longitud,Descripcion,Modalidad,Tipo_Actividad,Tipo_Actividad_Otro,Fecha_Hora,Foto_URL
                        linea = f'{id_r},{usuario_id},"{nombre}","{correo}","{cargo}",{lat},{lon},"{desc}","{modalidad}","{tipo_actividad}","{tipo_actividad_otro}","{fecha_str}","{foto}"\n'
                        
                        yield linea
                        registros_procesados += 1
                        
                        # Log cada 1000 registros
                        if registros_procesados % 1000 == 0:
                            print(f"📊 {registros_procesados} registros procesados...")
                
                print(f"✅ {registros_procesados} registros exportados a CSV")
                
            except Exception as e:
                print(f"❌ Error generando CSV: {e}")
                yield f"# ERROR: {str(e)}\n"
        
        # Headers para descarga
        headers = {
            "Content-Disposition": f"attachment; filename={nombre_archivo}",
            "Content-Type": "text/csv; charset=utf-8"
        }
        
        print(f"📥 Iniciando descarga del archivo: {nombre_archivo}")
        return StreamingResponse(
            content=generar_csv(),
            media_type="text/csv; charset=utf-8",
            headers=headers
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en exportación CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Error al exportar registros: {str(e)}")

# ==================== FIN EXPORTAR REGISTROS A CSV ====================

# ==================== BUSCAR USUARIO POR CURP ====================

@app.get("/usuarios/buscar-curp/{curp}")
async def buscar_usuario_por_curp(curp: str):
    """
    Buscar usuario por CURP y devolver su información junto con conteo de actividades
    """
    try:
        print(f"🔍 Buscando usuario con CURP: {curp}")
        
        # Convertir CURP a mayúsculas y limpiar espacios
        curp_upper = curp.upper().strip()
        
        if len(curp_upper) != 18:
            raise HTTPException(status_code=400, detail="La CURP debe tener exactamente 18 caracteres")
        
        # Buscar usuario por CURP
        usuario = ejecutar_consulta_segura(
            "SELECT id, correo, nombre_completo, cargo, supervisor, curp, telefono, territorio, rol FROM usuarios WHERE curp = %s",
            (curp_upper,),
            fetch_type='one'
        )
        
        if not usuario:
            raise HTTPException(status_code=404, detail=f"No se encontró usuario con CURP: {curp_upper}")
        
        # Contar actividades (registros) del usuario
        conteo_actividades = ejecutar_consulta_segura(
            "SELECT COUNT(*) FROM registros WHERE usuario_id = %s",
            (usuario[0],),
            fetch_type='one'
        )
        
        # Contar asistencias del usuario
        conteo_asistencias = ejecutar_consulta_segura(
            "SELECT COUNT(*) FROM asistencias WHERE usuario_id = %s",
            (usuario[0],),
            fetch_type='one'
        )
        
        resultado = {
            "id": usuario[0],
            "correo": usuario[1],
            "nombre_completo": usuario[2],
            "cargo": usuario[3],
            "supervisor": usuario[4],
            "curp": usuario[5],
            "telefono": usuario[6],
            "territorio": usuario[7],
            "rol": usuario[8] if len(usuario) > 8 else 'user',
            "total_actividades": conteo_actividades[0] if conteo_actividades else 0,
            "total_asistencias": conteo_asistencias[0] if conteo_asistencias else 0
        }
        
        print(f"✅ Usuario encontrado: {resultado['nombre_completo']} - Actividades: {resultado['total_actividades']}")
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error buscando usuario por CURP: {e}")
        raise HTTPException(status_code=500, detail=f"Error al buscar usuario: {str(e)}")

# ==================== TRANSFERIR ACTIVIDADES ENTRE USUARIOS ====================

class TransferenciaActividades(BaseModel):
    curp_origen: str
    curp_destino: str
    incluir_asistencias: bool = False

@app.post("/usuarios/transferir-actividades")
async def transferir_actividades(datos: TransferenciaActividades):
    """
    Transferir todas las actividades (registros) de un usuario a otro por CURP.
    Opcionalmente también puede transferir asistencias.
    """
    try:
        print(f"🔄 Iniciando transferencia de actividades:")
        print(f"   Origen CURP: {datos.curp_origen}")
        print(f"   Destino CURP: {datos.curp_destino}")
        print(f"   Incluir asistencias: {datos.incluir_asistencias}")
        
        # Validar y limpiar CURPs
        curp_origen = datos.curp_origen.upper().strip()
        curp_destino = datos.curp_destino.upper().strip()
        
        if len(curp_origen) != 18 or len(curp_destino) != 18:
            raise HTTPException(status_code=400, detail="Las CURPs deben tener exactamente 18 caracteres")
        
        if curp_origen == curp_destino:
            raise HTTPException(status_code=400, detail="La CURP de origen y destino no pueden ser iguales")
        
        # Buscar usuario origen
        usuario_origen = ejecutar_consulta_segura(
            "SELECT id, nombre_completo, correo FROM usuarios WHERE curp = %s",
            (curp_origen,),
            fetch_type='one'
        )
        
        if not usuario_origen:
            raise HTTPException(status_code=404, detail=f"No se encontró usuario origen con CURP: {curp_origen}")
        
        # Buscar usuario destino
        usuario_destino = ejecutar_consulta_segura(
            "SELECT id, nombre_completo, correo FROM usuarios WHERE curp = %s",
            (curp_destino,),
            fetch_type='one'
        )
        
        if not usuario_destino:
            raise HTTPException(status_code=404, detail=f"No se encontró usuario destino con CURP: {curp_destino}")
        
        id_origen = usuario_origen[0]
        id_destino = usuario_destino[0]
        
        print(f"📊 Usuario origen ID: {id_origen} ({usuario_origen[1]})")
        print(f"📊 Usuario destino ID: {id_destino} ({usuario_destino[1]})")
        
        # Contar actividades antes de transferir
        conteo_antes = ejecutar_consulta_segura(
            "SELECT COUNT(*) FROM registros WHERE usuario_id = %s",
            (id_origen,),
            fetch_type='one'
        )
        actividades_a_transferir = conteo_antes[0] if conteo_antes else 0
        
        if actividades_a_transferir == 0 and not datos.incluir_asistencias:
            raise HTTPException(status_code=400, detail="El usuario origen no tiene actividades para transferir")
        
        # Transferir actividades (registros)
        ejecutar_consulta_segura(
            "UPDATE registros SET usuario_id = %s WHERE usuario_id = %s",
            (id_destino, id_origen),
            fetch_type='none'
        )
        
        print(f"✅ {actividades_a_transferir} actividades transferidas")
        
        # Transferir asistencias si se solicita
        asistencias_transferidas = 0
        if datos.incluir_asistencias:
            conteo_asistencias = ejecutar_consulta_segura(
                "SELECT COUNT(*) FROM asistencias WHERE usuario_id = %s",
                (id_origen,),
                fetch_type='one'
            )
            asistencias_a_transferir = conteo_asistencias[0] if conteo_asistencias else 0
            
            if asistencias_a_transferir > 0:
                ejecutar_consulta_segura(
                    "UPDATE asistencias SET usuario_id = %s WHERE usuario_id = %s",
                    (id_destino, id_origen),
                    fetch_type='none'
                )
                asistencias_transferidas = asistencias_a_transferir
                print(f"✅ {asistencias_transferidas} asistencias transferidas")
        
        resultado = {
            "status": "success",
            "mensaje": "Transferencia completada exitosamente",
            "detalles": {
                "usuario_origen": {
                    "id": id_origen,
                    "nombre": usuario_origen[1],
                    "correo": usuario_origen[2],
                    "curp": curp_origen
                },
                "usuario_destino": {
                    "id": id_destino,
                    "nombre": usuario_destino[1],
                    "correo": usuario_destino[2],
                    "curp": curp_destino
                },
                "actividades_transferidas": actividades_a_transferir,
                "asistencias_transferidas": asistencias_transferidas
            }
        }
        
        print(f"✅ Transferencia completada: {actividades_a_transferir} actividades, {asistencias_transferidas} asistencias")
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en transferencia de actividades: {e}")
        # Hacer rollback en caso de error
        try:
            if conn and not conn.closed:
                conn.rollback()
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Error al transferir actividades: {str(e)}")

# ==================== FIN TRANSFERIR ACTIVIDADES ====================

# ==================== SUPERVISOR AUTOMÁTICO POR TERRITORIO ====================

@app.get("/usuarios/{user_id}/supervisor-automatico")
async def obtener_supervisor_automatico(user_id: int):
    """
    Obtiene el supervisor automático para un usuario técnico.
    Si el usuario es TECNICO SOCIAL o TECNICO PRODUCTIVO, 
    busca el nombre_completo del admin territorial asignado a su territorio.
    """
    try:
        print(f"🔍 Buscando supervisor automático para usuario ID: {user_id}")
        
        # Obtener datos del usuario
        cursor.execute("""
            SELECT cargo, territorio FROM usuarios WHERE id = %s
        """, (user_id,))
        
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        cargo = usuario[0] or ''
        territorio = usuario[1]
        
        print(f"   Cargo: {cargo}, Territorio: {territorio}")
        
        # Verificar si es técnico
        cargos_tecnicos = ['TECNICO SOCIAL', 'TECNICO PRODUCTIVO']
        if cargo.upper() not in cargos_tecnicos:
            return {
                "success": True,
                "supervisor": None,
                "mensaje": "El cargo no requiere supervisor automático"
            }
        
        # Si no tiene territorio asignado
        if not territorio:
            return {
                "success": True,
                "supervisor": None,
                "mensaje": "El usuario no tiene territorio asignado"
            }
        
        # Buscar el administrador territorial de ese territorio
        cursor.execute("""
            SELECT nombre_completo FROM admin_users 
            WHERE es_territorial = TRUE 
            AND territorio = %s 
            AND activo = TRUE
            LIMIT 1
        """, (territorio,))
        
        admin_territorial = cursor.fetchone()
        
        if admin_territorial and admin_territorial[0]:
            supervisor_nombre = admin_territorial[0]
            
            # ACTUALIZAR el supervisor en la base de datos del usuario
            cursor.execute("""
                UPDATE usuarios SET supervisor = %s WHERE id = %s
            """, (supervisor_nombre, user_id))
            conn.commit()
            
            print(f"   ✅ Supervisor actualizado en BD: {supervisor_nombre}")
            return {
                "success": True,
                "supervisor": supervisor_nombre,
                "territorio": territorio,
                "actualizado_en_bd": True,
                "mensaje": "Supervisor automático asignado y guardado en base de datos"
            }
        else:
            print(f"   ⚠️ No hay administrador territorial para: {territorio}")
            return {
                "success": True,
                "supervisor": None,
                "territorio": territorio,
                "actualizado_en_bd": False,
                "mensaje": f"No hay administrador territorial asignado para {territorio}"
            }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error obteniendo supervisor automático: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener supervisor: {str(e)}")

# ==================== FIN SUPERVISOR AUTOMÁTICO ====================

# ==================== ACTUALIZACIÓN MASIVA SUPERVISORES ====================

@app.post("/actualizar-supervisores-tecnicos")
async def actualizar_supervisores_tecnicos_masivo():
    """
    Actualiza automáticamente el supervisor de TODOS los técnicos existentes en la base de datos.
    Útil para migración o corrección masiva de supervisores.
    """
    try:
        print("🔄 Iniciando actualización masiva de supervisores técnicos...")
        
        # Obtener todos los técnicos
        cursor.execute("""
            SELECT id, cargo, territorio, nombre_completo 
            FROM usuarios 
            WHERE UPPER(cargo) IN ('TECNICO SOCIAL', 'TECNICO PRODUCTIVO')
            AND territorio IS NOT NULL
        """)
        
        tecnicos = cursor.fetchall()
        total_tecnicos = len(tecnicos)
        actualizados = 0
        sin_supervisor = 0
        errores = []
        
        print(f"📊 Total de técnicos encontrados: {total_tecnicos}")
        
        for tecnico in tecnicos:
            user_id, cargo, territorio, nombre = tecnico
            
            try:
                # Buscar supervisor territorial
                cursor.execute("""
                    SELECT nombre_completo FROM admin_users 
                    WHERE es_territorial = TRUE 
                    AND territorio = %s 
                    AND activo = TRUE
                    LIMIT 1
                """, (territorio,))
                
                admin_territorial = cursor.fetchone()
                
                if admin_territorial and admin_territorial[0]:
                    supervisor_nombre = admin_territorial[0]
                    
                    # Actualizar supervisor en BD
                    cursor.execute("""
                        UPDATE usuarios SET supervisor = %s WHERE id = %s
                    """, (supervisor_nombre, user_id))
                    
                    actualizados += 1
                    print(f"   ✅ {nombre} ({territorio}) → Supervisor: {supervisor_nombre}")
                else:
                    sin_supervisor += 1
                    print(f"   ⚠️ {nombre} ({territorio}) → Sin admin territorial")
                    errores.append({
                        "id": user_id,
                        "nombre": nombre,
                        "territorio": territorio,
                        "razon": "No hay administrador territorial"
                    })
                    
            except Exception as e:
                errores.append({
                    "id": user_id,
                    "nombre": nombre,
                    "error": str(e)
                })
                print(f"   ❌ Error procesando {nombre}: {e}")
        
        # Commit de todos los cambios
        conn.commit()
        
        print(f"✅ Actualización masiva completada:")
        print(f"   - Actualizados: {actualizados}")
        print(f"   - Sin supervisor: {sin_supervisor}")
        print(f"   - Errores: {len(errores)}")
        
        return {
            "success": True,
            "total_tecnicos": total_tecnicos,
            "actualizados": actualizados,
            "sin_supervisor": sin_supervisor,
            "errores": errores,
            "mensaje": f"Se actualizaron {actualizados} de {total_tecnicos} técnicos"
        }
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error en actualización masiva: {e}")
        raise HTTPException(status_code=500, detail=f"Error en actualización masiva: {str(e)}")

# ==================== FIN ACTUALIZACIÓN MASIVA ====================

# ==================== SUPERVISOR POR TERRITORIO ====================

@app.get("/supervisor-territorio/{territorio:path}")
async def obtener_supervisor_por_territorio(territorio: str):
    """
    Obtiene el nombre del supervisor territorial para un territorio específico.
    Busca en admin_users el usuario territorial asignado a ese territorio.
    Usa :path para permitir barras (/) en el nombre del territorio.
    """
    try:
        # Decodificar el territorio (puede venir con %20 en lugar de espacios y %2F en lugar de /)
        from urllib.parse import unquote
        territorio_decoded = unquote(territorio)
        
        print(f"🔍 Buscando supervisor para territorio: {territorio_decoded}")
        
        # Buscar el administrador territorial de ese territorio
        cursor.execute("""
            SELECT nombre_completo FROM admin_users 
            WHERE es_territorial = TRUE 
            AND territorio = %s 
            AND activo = TRUE
            LIMIT 1
        """, (territorio_decoded,))
        
        admin_territorial = cursor.fetchone()
        
        if admin_territorial and admin_territorial[0]:
            supervisor_nombre = admin_territorial[0]
            print(f"   ✅ Supervisor encontrado: {supervisor_nombre}")
            return {
                "success": True,
                "supervisor": supervisor_nombre,
                "territorio": territorio_decoded,
                "mensaje": "Supervisor territorial encontrado"
            }
        else:
            print(f"   ⚠️ No hay administrador territorial para: {territorio_decoded}")
            return {
                "success": True,
                "supervisor": None,
                "territorio": territorio_decoded,
                "mensaje": f"No hay administrador territorial asignado para {territorio_decoded}"
            }
        
    except Exception as e:
        print(f"❌ Error obteniendo supervisor por territorio: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener supervisor: {str(e)}")

# ==================== FIN SUPERVISOR POR TERRITORIO ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
