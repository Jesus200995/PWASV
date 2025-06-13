from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from datetime import datetime
import os

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

@app.get("/registros")
def obtener_registros():
    cursor.execute("SELECT * FROM registros ORDER BY fecha_hora DESC LIMIT 20")
    registros = cursor.fetchall()
    return {"registros": registros}
