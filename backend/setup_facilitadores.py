"""
Script completo de setup para el sistema de Facilitadores.
Ejecutar en el VPS: python setup_facilitadores.py

Pasos:
  1. Migraciones de BD (usuario_id en admin_users, tabla facilitador_tecnico_asignaciones)
  2. Leer CSV routes_enriched.csv, crear usuarios facilitadores en admin_users
  3. Vincular facilitador con usuario real en tabla usuarios (por CURP)
  4. Crear asignaciones facilitador -> tecnico
  5. Generar CSV de credenciales: credenciales_facilitadores.csv
"""

import psycopg2
import csv
import io
import unicodedata
import re
import sys
import os
from passlib.context import CryptContext

# ── Configuración ────────────────────────────────────────────────
DB_HOST = "localhost"   # en el VPS, acceso local
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

CSV_PATH = "/var/www/PWASV/routes_enriched.csv"
OUT_CSV  = "/var/www/PWASV/credenciales_facilitadores.csv"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Utilidades ───────────────────────────────────────────────────

def normalizar(texto):
    """Quita acentos y caracteres especiales, devuelve minúsculas solo [a-z0-9_]."""
    nfkd = unicodedata.normalize('NFKD', texto)
    sin_acento = ''.join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', sin_acento.lower())

def generar_username(nombre_completo, existentes):
    """
    username = primera_letra_primer_nombre + primer_apellido
    Ejemplo: JOSE VIDALES TRUJILLO -> jvidales
    Si ya existe, agrega número: jvidales2, jvidales3 ...
    """
    partes = nombre_completo.strip().split()
    if len(partes) >= 2:
        base = normalizar(partes[0][0]) + normalizar(partes[1])
    else:
        base = normalizar(partes[0])
    
    cand = base
    n = 2
    while cand in existentes:
        cand = f"{base}{n}"
        n += 1
    existentes.add(cand)
    return cand

def generar_password(nombre_completo):
    """
    password = primer_apellido_min + 2026
    Ejemplo: JOSE VIDALES TRUJILLO -> vidales2026
    """
    partes = nombre_completo.strip().split()
    if len(partes) >= 2:
        ape = normalizar(partes[1])
    else:
        ape = normalizar(partes[0])
    return f"{ape}2026"

# ── Conexión a BD ─────────────────────────────────────────────────

def conectar():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# ── Paso 1: Migraciones ──────────────────────────────────────────

def migrar(conn):
    cur = conn.cursor()
    
    print("=== PASO 1: Migraciones ===")

    # Agregar usuario_id a admin_users
    cur.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name='admin_users' AND column_name='usuario_id'
            ) THEN
                ALTER TABLE admin_users ADD COLUMN usuario_id INTEGER REFERENCES usuarios(id);
                RAISE NOTICE 'Columna usuario_id agregada a admin_users';
            ELSE
                RAISE NOTICE 'Columna usuario_id ya existe en admin_users';
            END IF;
        END $$;
    """)
    print("  ✅ usuario_id en admin_users: OK")

    # Crear tabla facilitador_tecnico_asignaciones
    cur.execute("""
        CREATE TABLE IF NOT EXISTS facilitador_tecnico_asignaciones (
            id                      BIGSERIAL PRIMARY KEY,
            facilitador_usuario_id  INTEGER NOT NULL REFERENCES usuarios(id),
            tecnico_usuario_id      INTEGER NOT NULL REFERENCES usuarios(id),
            origen                  VARCHAR(10) NOT NULL DEFAULT 'csv'
                                        CHECK (origen IN ('csv', 'manual')),
            activo                  BOOLEAN NOT NULL DEFAULT TRUE,
            created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            created_by_admin_user_id INTEGER REFERENCES admin_users(id),
            UNIQUE (facilitador_usuario_id, tecnico_usuario_id)
        );
    """)
    print("  ✅ Tabla facilitador_tecnico_asignaciones: OK")

    # Índices para consultas rápidas
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_fta_facilitador
            ON facilitador_tecnico_asignaciones(facilitador_usuario_id)
            WHERE activo = TRUE;
        CREATE INDEX IF NOT EXISTS idx_fta_tecnico
            ON facilitador_tecnico_asignaciones(tecnico_usuario_id)
            WHERE activo = TRUE;
    """)
    print("  ✅ Índices creados: OK")

    conn.commit()
    cur.close()
    print()

# ── Paso 2 y 3: Crear usuarios facilitadores ───────────────────

def crear_facilitadores(conn):
    cur = conn.cursor()
    print("=== PASO 2: Crear usuarios facilitadores en admin_users ===")

    # Leer usernames ya existentes
    cur.execute("SELECT username FROM admin_users")
    existentes_usernames = {r[0] for r in cur.fetchall()}

    # Leer CURPs ya existentes en admin_users
    cur.execute("SELECT curp FROM admin_users WHERE curp IS NOT NULL AND curp != ''")
    existentes_curps = {r[0].strip().upper() for r in cur.fetchall()}

    # Leer CSV
    filas = []
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filas.append(row)

    # Facilitadores únicos por CURP
    facilitadores = {}  # curp -> nombre
    for row in filas:
        curp = row['facilitador_curp_resuelto'].strip().upper()
        nombre = row['facilitador_nombre'].strip()
        if curp and curp not in ('VACANTE', ''):
            facilitadores[curp] = nombre

    print(f"  Facilitadores únicos en CSV: {len(facilitadores)}")

    creados = []
    omitidos = []

    for curp, nombre in facilitadores.items():
        if curp in existentes_curps:
            omitidos.append((nombre, curp, 'ya existe en admin_users por CURP'))
            continue

        # Buscar usuario_id en tabla usuarios por CURP
        cur.execute(
            "SELECT id FROM usuarios WHERE UPPER(TRIM(curp)) = %s LIMIT 1",
            (curp,)
        )
        result = cur.fetchone()
        usuario_id = result[0] if result else None

        username   = generar_username(nombre, existentes_usernames)
        password   = generar_password(nombre)
        pwd_hash   = pwd_context.hash(password)
        permisos   = '{"firmas": true}'
        cargo_adm  = 'FACILITADOR'

        cur.execute("""
            INSERT INTO admin_users
                (username, password, rol, permisos, activo, es_territorial,
                 nombre_completo, curp, cargo, usuario_id)
            VALUES (%s, %s, 'user', %s, TRUE, FALSE, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
            RETURNING id
        """, (username, pwd_hash, permisos, nombre, curp, cargo_adm, usuario_id))

        row_id = cur.fetchone()
        if row_id:
            existentes_curps.add(curp)
            creados.append({
                'nombre': nombre,
                'curp': curp,
                'username': username,
                'password': password,
                'usuario_id_vinculado': usuario_id,
                'admin_user_id': row_id[0]
            })
        else:
            omitidos.append((nombre, curp, 'conflicto de username'))

    conn.commit()
    cur.close()

    print(f"  ✅ Facilitadores creados: {len(creados)}")
    print(f"  ⚠️  Omitidos: {len(omitidos)}")
    for o in omitidos[:5]:
        print(f"     - {o}")
    print()
    return creados

# ── Paso 4: Crear asignaciones facilitador → técnico ──────────

def crear_asignaciones(conn):
    cur = conn.cursor()
    print("=== PASO 3: Crear asignaciones facilitador → técnico ===")

    filas = []
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filas.append(row)

    inseridos = 0
    omitidos  = 0
    sin_match = []

    for row in filas:
        fac_curp = row['facilitador_curp_resuelto'].strip().upper()
        if not fac_curp or fac_curp == 'VACANTE':
            continue

        # ID del facilitador en tabla usuarios
        cur.execute(
            "SELECT id FROM usuarios WHERE UPPER(TRIM(curp)) = %s LIMIT 1",
            (fac_curp,)
        )
        r = cur.fetchone()
        if not r:
            sin_match.append(f"Facilitador CURP {fac_curp} no encontrado en usuarios")
            continue
        fac_uid = r[0]

        # Procesar técnico social
        ts_curp = row['tecnico_social_curp_resuelto'].strip().upper()
        if ts_curp and ts_curp not in ('VACANTE', ''):
            cur.execute(
                "SELECT id FROM usuarios WHERE UPPER(TRIM(curp)) = %s LIMIT 1",
                (ts_curp,)
            )
            r = cur.fetchone()
            if r:
                try:
                    cur.execute("""
                        INSERT INTO facilitador_tecnico_asignaciones
                            (facilitador_usuario_id, tecnico_usuario_id, origen)
                        VALUES (%s, %s, 'csv')
                        ON CONFLICT (facilitador_usuario_id, tecnico_usuario_id) DO NOTHING
                    """, (fac_uid, r[0]))
                    if cur.rowcount > 0:
                        inseridos += 1
                    else:
                        omitidos += 1
                except Exception as e:
                    omitidos += 1
            else:
                sin_match.append(f"Técnico social CURP {ts_curp} no encontrado")

        # Procesar técnico productivo
        tp_curp = row['tecnico_productivo_curp_resuelto'].strip().upper()
        if tp_curp and tp_curp not in ('VACANTE', ''):
            cur.execute(
                "SELECT id FROM usuarios WHERE UPPER(TRIM(curp)) = %s LIMIT 1",
                (tp_curp,)
            )
            r = cur.fetchone()
            if r:
                try:
                    cur.execute("""
                        INSERT INTO facilitador_tecnico_asignaciones
                            (facilitador_usuario_id, tecnico_usuario_id, origen)
                        VALUES (%s, %s, 'csv')
                        ON CONFLICT (facilitador_usuario_id, tecnico_usuario_id) DO NOTHING
                    """, (fac_uid, r[0]))
                    if cur.rowcount > 0:
                        inseridos += 1
                    else:
                        omitidos += 1
                except Exception as e:
                    omitidos += 1
            else:
                sin_match.append(f"Técnico productivo CURP {tp_curp} no encontrado")

    conn.commit()
    cur.close()

    print(f"  ✅ Asignaciones insertadas: {inseridos}")
    print(f"  ⚠️  Ya existían / omitidas: {omitidos}")
    if sin_match:
        print(f"  ❌ Sin match en BD ({len(sin_match)}):")
        for s in sin_match[:10]:
            print(f"     - {s}")
    print()

# ── Paso 5: Generar CSV de credenciales ──────────────────────────

def generar_csv_credenciales(creados):
    print(f"=== PASO 4: Generar CSV de credenciales → {OUT_CSV} ===")
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['nombre', 'curp', 'username', 'password', 'usuario_id_vinculado'])
        writer.writeheader()
        writer.writerows(creados)
    print(f"  ✅ CSV generado con {len(creados)} registros")
    print()

    # También imprimir en pantalla
    print("  CREDENCIALES GENERADAS:")
    print(f"  {'NOMBRE':<40} {'USERNAME':<20} {'PASSWORD':<20} {'VINCULADO'}")
    print(f"  {'-'*40} {'-'*20} {'-'*20} {'-'*10}")
    for c in creados:
        vinc = '✅' if c['usuario_id_vinculado'] else '❌ NO'
        print(f"  {c['nombre']:<40} {c['username']:<20} {c['password']:<20} {vinc}")

# ── Main ─────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 60)
    print("  SETUP SISTEMA FACILITADORES - Sembrando Vida")
    print("=" * 60)
    print()

    if not os.path.exists(CSV_PATH):
        print(f"❌ No se encontró el CSV en {CSV_PATH}")
        sys.exit(1)

    conn = conectar()
    print("✅ Conexión a BD establecida\n")

    migrar(conn)
    creados = crear_facilitadores(conn)
    crear_asignaciones(conn)
    generar_csv_credenciales(creados)

    conn.close()

    print("=" * 60)
    print("  SETUP COMPLETADO")
    print("=" * 60)
