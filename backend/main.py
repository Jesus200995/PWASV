from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
import bcrypt
from pydantic import BaseModel

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

class UserLogin(BaseModel):
    correo: str
    contrasena: str

class PasswordChange(BaseModel):
    usuario_id: int
    nueva_contrasena: str

# Montar carpeta de fotos para servir estáticamente
app.mount("/fotos", StaticFiles(directory="fotos"), name="fotos")

# Endpoints de autenticación
@app.post("/usuarios")
async def crear_usuario(usuario: UserCreate):
    try:
        # Comprobar si el correo ya existe
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (usuario.correo,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        
        # Hash de la contraseña
        hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
        
        # Insertar usuario
        cursor.execute(
            "INSERT INTO usuarios (correo, nombre_completo, cargo, supervisor, contrasena) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (usuario.correo, usuario.nombre_completo, usuario.cargo, usuario.supervisor, hashed_password.decode('utf-8'))
        )
        
        user_id = cursor.fetchone()[0]
        conn.commit()
        
        return {"id": user_id, "mensaje": "Usuario creado exitosamente"}
    except Exception as e:
        conn.rollback()
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
