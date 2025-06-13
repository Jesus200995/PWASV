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

conn = psycopg2.connect(
    host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
)
cursor = conn.cursor()

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

# Modificar el endpoint de registros para filtrar por usuario
@app.get("/registros")
def obtener_registros(usuario_id: int = None):
    try:
        if usuario_id:
            cursor.execute(
                "SELECT * FROM registros WHERE usuario_id = %s ORDER BY fecha_hora DESC LIMIT 50",
                (usuario_id,),
                cursor_factory=RealDictCursor
            )
        else:
            cursor.execute(
                "SELECT * FROM registros ORDER BY fecha_hora DESC LIMIT 50",
                cursor_factory=RealDictCursor
            )
        
        registros = cursor.fetchall()
        return {"registros": registros}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener registros: {str(e)}")
