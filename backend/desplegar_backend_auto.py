"""
Script de despliegue AUTOMÁTICO del backend al VPS
Sube el archivo main.py con el fix del endpoint de búsqueda (OR en vez de AND)
"""
import paramiko
import os
from getpass import getpass

def desplegar_backend():
    print("\n" + "="*80)
    print("🚀 DESPLIEGUE AUTOMÁTICO DEL BACKEND AL VPS")
    print("="*80)
    
    # Configuración
    HOST = "31.97.8.51"
    USER = "root"
    LOCAL_FILE = "main.py"
    
    # Solicitar contraseña
    print(f"\n🔐 Conectando a {HOST}...")
    PASSWORD = getpass("Contraseña root: ")
    
    try:
        # Conectar por SSH
        print(f"📡 Estableciendo conexión SSH...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("✅ Conexión establecida\n")
        
        # 1. Encontrar ubicación del backend
        print("🔍 Buscando ubicación del backend en el servidor...")
        stdin, stdout, stderr = ssh.exec_command("find /root /home -name 'main.py' -path '*/backend/*' -o -path '*/pwa*/*' 2>/dev/null | head -3")
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        
        if not output:
            print("❌ No se encontró main.py en el servidor")
            print("\n🔍 Directorios encontrados:")
            stdin, stdout, stderr = ssh.exec_command("ls -la /root")
            print(stdout.read().decode())
            
            remote_path = input("\n📝 Ingresa la ruta completa al archivo main.py en el servidor: ")
        else:
            paths = output.split('\n')
            print(f"\n📂 Archivos main.py encontrados:")
            for i, path in enumerate(paths, 1):
                print(f"   {i}. {path}")
            
            if len(paths) == 1:
                remote_path = paths[0]
                print(f"\n✅ Usando: {remote_path}")
            else:
                choice = input(f"\n📝 Selecciona el número (1-{len(paths)}): ")
                remote_path = paths[int(choice) - 1]
        
        # 2. Crear backup
        backup_path = remote_path + ".backup_" + import_time.strftime("%Y%m%d_%H%M%S")
        print(f"\n💾 Creando backup: {backup_path}")
        ssh.exec_command(f"cp {remote_path} {backup_path}")
        print("✅ Backup creado")
        
        # 3. Subir archivo
        print(f"\n📤 Subiendo {LOCAL_FILE} a {remote_path}...")
        sftp = ssh.open_sftp()
        sftp.put(LOCAL_FILE, remote_path)
        sftp.close()
        print("✅ Archivo subido correctamente")
        
        # 4. Verificar el cambio
        print(f"\n🔍 Verificando el cambio en el servidor...")
        stdin, stdout, stderr = ssh.exec_command(f"grep -n \"OR.*join.*condiciones\" {remote_path}")
        verification = stdout.read().decode().strip()
        
        if "OR" in verification:
            print("✅ Verificación exitosa: El código usa OR")
            print(f"   {verification[:200]}")
        else:
            print("⚠️ No se pudo verificar el cambio automáticamente")
        
        # 5. Detectar método de ejecución
        print(f"\n🔍 Detectando cómo se ejecuta el backend...")
        
        # Buscar en systemd
        stdin, stdout, stderr = ssh.exec_command("systemctl list-units --type=service | grep -E 'pwa|backend|uvicorn'")
        systemd_services = stdout.read().decode().strip()
        
        # Buscar en pm2
        stdin, stdout, stderr = ssh.exec_command("which pm2 && pm2 list")
        pm2_output = stdout.read().decode().strip()
        
        # Buscar proceso uvicorn
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep -E '[u]vicorn|[p]ython.*main'")
        process_output = stdout.read().decode().strip()
        
        print("\n📊 Servicios encontrados:")
        
        restart_command = None
        
        if systemd_services:
            print("\n🔹 Systemd:")
            print(systemd_services)
            services = [line.split()[0] for line in systemd_services.split('\n') if line]
            if services:
                restart_command = f"systemctl restart {services[0]}"
        
        if pm2_output and "pm2" in pm2_output:
            print("\n🔹 PM2:")
            print(pm2_output[:500])
            if "pwa" in pm2_output.lower() or "backend" in pm2_output.lower():
                restart_command = "pm2 restart all"
        
        if process_output:
            print("\n🔹 Procesos activos:")
            for line in process_output.split('\n')[:3]:
                print(f"   {line}")
        
        # 6. Reiniciar servicio
        if restart_command:
            print(f"\n🔄 Comando de reinicio sugerido: {restart_command}")
            confirm = input("¿Ejecutar este comando? (s/n): ")
            
            if confirm.lower() == 's':
                print(f"⏳ Ejecutando: {restart_command}")
                stdin, stdout, stderr = ssh.exec_command(restart_command)
                time.sleep(2)
                output = stdout.read().decode()
                error = stderr.read().decode()
                
                if output:
                    print(f"📤 Output: {output}")
                if error and "warning" not in error.lower():
                    print(f"⚠️ Error: {error}")
                else:
                    print("✅ Servicio reiniciado")
            else:
                print("⏭️ Omitiendo reinicio automático")
                print(f"\n📝 Para reiniciar manualmente, ejecuta en el servidor:")
                print(f"   {restart_command}")
        else:
            print("\n⚠️ No se detectó automáticamente cómo reiniciar")
            print("\n📝 Comandos comunes para reiniciar:")
            print("   systemctl restart [nombre-servicio]")
            print("   pm2 restart [nombre-app]")
            print("   supervisorctl restart [nombre-app]")
            print("   O kill el proceso y reiniciar manualmente")
        
        # 7. Verificar que está corriendo
        print(f"\n🔍 Verificando que el servicio esté corriendo...")
        time.sleep(3)
        
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep -E '[u]vicorn|[p]ython.*main' | head -2")
        running = stdout.read().decode().strip()
        
        if running:
            print("✅ El backend está corriendo:")
            for line in running.split('\n'):
                print(f"   {line[:150]}")
        else:
            print("⚠️ No se detectó el proceso del backend")
            print("   Verifica manualmente que se haya iniciado correctamente")
        
        ssh.close()
        
        print("\n" + "="*80)
        print("✅ DESPLIEGUE COMPLETADO")
        print("="*80)
        print("\n📝 SIGUIENTE PASO:")
        print("   1. Ve al admin-pwa: http://localhost:5173/#/debug-buscador")
        print("   2. Click en '🔍 Verificar Endpoint OR'")
        print("   3. Debería decir 'El backend parece usar OR correctamente'")
        print("   4. Prueba buscar la CURP: ROCR820619MSLJSB05")
        print("\n")
        
    except paramiko.AuthenticationException:
        print("❌ Error de autenticación: Contraseña incorrecta")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import time
    import_time = __import__('time')
    
    # Verificar que el archivo local existe
    if not os.path.exists("main.py"):
        print("❌ Error: No se encuentra el archivo main.py en el directorio actual")
        print(f"   Directorio actual: {os.getcwd()}")
        print("\n💡 Ejecuta este script desde la carpeta 'backend':")
        print("   cd backend")
        print("   python desplegar_backend_auto.py")
        exit(1)
    
    # Verificar que paramiko está instalado
    try:
        import paramiko
    except ImportError:
        print("❌ Error: El módulo 'paramiko' no está instalado")
        print("\n💡 Instálalo con:")
        print("   pip install paramiko")
        exit(1)
    
    desplegar_backend()
