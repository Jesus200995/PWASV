"""
Regenera el CSV de credenciales leyendo el CSV fuente y aplicando la misma
lógica que setup_facilitadores.py. Requiere solo Python estándar.
"""
import csv, unicodedata, re, os

CSV_IN  = os.path.join(os.path.dirname(__file__), '..', 'routes_enriched.csv')
CSV_OUT = os.path.join(os.path.dirname(__file__), '..', 'credenciales_facilitadores.csv')

def normalizar(t):
    n = unicodedata.normalize('NFKD', t)
    s = ''.join(c for c in n if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', s.lower())

def generar_username(nombre, existentes):
    partes = nombre.strip().split()
    base = (normalizar(partes[0][0]) + normalizar(partes[1])) if len(partes)>=2 else normalizar(partes[0])
    cand, n = base, 2
    while cand in existentes:
        cand = f"{base}{n}"; n += 1
    existentes.add(cand)
    return cand

def generar_password(nombre):
    partes = nombre.strip().split()
    ape = normalizar(partes[1]) if len(partes)>=2 else normalizar(partes[0])
    return f"{ape}2026"

existentes_usernames = set()
facilitadores = {}

with open(CSV_IN, encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        curp  = row['facilitador_curp_resuelto'].strip().upper()
        nombre = row['facilitador_nombre'].strip()
        if curp and curp not in ('VACANTE',''):
            facilitadores[curp] = nombre

rows = []
for curp, nombre in facilitadores.items():
    user = generar_username(nombre, existentes_usernames)
    pwd  = generar_password(nombre)
    rows.append({'nombre': nombre, 'curp': curp, 'username': user, 'password': pwd})

with open(CSV_OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['nombre','curp','username','password'])
    w.writeheader(); w.writerows(rows)

print(f"✅ CSV generado: {CSV_OUT}")
print(f"   Total: {len(rows)} facilitadores")
print(f"\n{'NOMBRE':<40} {'USERNAME':<22} {'PASSWORD'}")
print('-'*80)
for r in rows[:10]:
    print(f"{r['nombre']:<40} {r['username']:<22} {r['password']}")
if len(rows)>10:
    print(f"  ... y {len(rows)-10} más")
