"""
Sube setup_facilitadores.py y el CSV al VPS y lo ejecuta.
"""
import paramiko
import os

HOST = "31.97.8.51"
USER = "root"
PASS = "Lab-312334062"
REMOTE_DIR = "/var/www/PWASV"

LOCAL_SCRIPT   = os.path.join(os.path.dirname(__file__), "setup_facilitadores.py")
LOCAL_CSV      = os.path.join(os.path.dirname(__file__), "..", "routes_enriched.csv")

def ssh_exec(client, cmd):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=120)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out, err

if __name__ == "__main__":
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS, timeout=20)
    print("✅ SSH conectado")

    # Subir archivos via SFTP
    sftp = client.open_sftp()

    print("📤 Subiendo setup_facilitadores.py ...")
    sftp.put(LOCAL_SCRIPT, f"{REMOTE_DIR}/setup_facilitadores.py")

    print("📤 Subiendo routes_enriched.csv ...")
    sftp.put(os.path.abspath(LOCAL_CSV), f"{REMOTE_DIR}/routes_enriched.csv")
    sftp.close()
    print("✅ Archivos subidos")

    # Ejecutar el script
    print("\n🚀 Ejecutando setup_facilitadores.py en el VPS...\n")
    out, err = ssh_exec(client, f"cd {REMOTE_DIR} && python3 setup_facilitadores.py 2>&1")
    print(out)
    if err.strip():
        print("STDERR:", err[:2000])

    # Descargar el CSV de credenciales generado
    print("\n📥 Descargando credenciales_facilitadores.csv ...")
    sftp = client.open_sftp()
    local_out = os.path.join(os.path.dirname(__file__), "..", "credenciales_facilitadores.csv")
    try:
        sftp.get(f"{REMOTE_DIR}/credenciales_facilitadores.csv", local_out)
        print(f"✅ CSV guardado en: {local_out}")
    except Exception as e:
        print(f"⚠️  No se pudo descargar el CSV: {e}")
    sftp.close()

    client.close()
    print("\n✅ PROCESO COMPLETADO")
