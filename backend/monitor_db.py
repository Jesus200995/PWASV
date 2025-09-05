#!/usr/bin/env python3
"""
Script de monitoreo y diagnóstico de conexiones de base de datos
para el sistema PWA.

Este script:
1. Monitorea continuamente las conexiones de base de datos
2. Proporciona estadísticas de conectividad
3. Detecta cuando el servidor principal vuelve a estar disponible
4. Genera reportes de estado

Uso:
    python monitor_db.py [--interval=5] [--log-file=monitor.log]
"""

import psycopg2
import time
import argparse
import datetime
import json
import sys
from typing import Dict, List

# Configuraciones de base de datos (mismo que main.py)
DB_CONFIGS = [
    {
        "name": "Producción Principal",
        "host": "31.97.8.51",
        "database": "app_registros",
        "user": "jesus",
        "password": "2025",
        "timeout": 5
    },
    {
        "name": "Respaldo Local", 
        "host": "localhost",
        "database": "app_registros_local",
        "user": "postgres",
        "password": "admin",
        "timeout": 3
    }
]

class DatabaseMonitor:
    def __init__(self, interval: int = 5, log_file: str = None):
        self.interval = interval
        self.log_file = log_file
        self.stats = {config["name"]: {"success": 0, "failures": 0, "avg_response_time": 0} for config in DB_CONFIGS}
        self.last_status = {}
        self.start_time = datetime.datetime.now()
        
    def log_message(self, message: str):
        """Registrar mensaje con timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        print(formatted_message)
        
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(formatted_message + '\n')
            except Exception as e:
                print(f"Error escribiendo al log: {e}")
    
    def test_database_connection(self, config: Dict) -> Dict:
        """Probar conexión a una base de datos específica"""
        result = {
            "name": config["name"],
            "host": config["host"],
            "status": "unknown",
            "response_time": None,
            "error": None,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        start_time = time.time()
        try:
            conn = psycopg2.connect(
                host=config['host'], 
                database=config['database'], 
                user=config['user'], 
                password=config['password'],
                connect_timeout=config['timeout']
            )
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            
            response_time = time.time() - start_time
            result["status"] = "connected"
            result["response_time"] = round(response_time, 3)
            
            conn.close()
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            result["response_time"] = time.time() - start_time
            
        return result
    
    def update_stats(self, result: Dict):
        """Actualizar estadísticas de conexión"""
        db_name = result["name"]
        
        if result["status"] == "connected":
            self.stats[db_name]["success"] += 1
            # Actualizar tiempo promedio de respuesta
            current_avg = self.stats[db_name]["avg_response_time"]
            total_attempts = self.stats[db_name]["success"] + self.stats[db_name]["failures"]
            if total_attempts > 1:
                self.stats[db_name]["avg_response_time"] = (
                    (current_avg * (total_attempts - 1) + result["response_time"]) / total_attempts
                )
            else:
                self.stats[db_name]["avg_response_time"] = result["response_time"]
        else:
            self.stats[db_name]["failures"] += 1
    
    def detect_status_change(self, result: Dict):
        """Detectar cambios en el estado de conexión"""
        db_name = result["name"]
        current_status = result["status"]
        previous_status = self.last_status.get(db_name)
        
        if previous_status and previous_status != current_status:
            if current_status == "connected":
                self.log_message(f"🟢 {db_name}: RECUPERADO - Conexión restablecida")
            elif current_status == "error":
                self.log_message(f"🔴 {db_name}: CAÍDO - Conexión perdida")
        
        self.last_status[db_name] = current_status
    
    def generate_report(self) -> Dict:
        """Generar reporte de estado actual"""
        uptime = datetime.datetime.now() - self.start_time
        
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "monitoring_uptime": str(uptime),
            "databases": [],
            "summary": {
                "total_databases": len(DB_CONFIGS),
                "connected": 0,
                "disconnected": 0,
                "recommended_primary": None
            }
        }
        
        for config in DB_CONFIGS:
            result = self.test_database_connection(config)
            self.update_stats(result)
            self.detect_status_change(result)
            
            # Agregar estadísticas acumuladas
            db_stats = self.stats[result["name"]].copy()
            total_attempts = db_stats["success"] + db_stats["failures"]
            
            db_info = {
                **result,
                "statistics": {
                    **db_stats,
                    "total_attempts": total_attempts,
                    "success_rate": round((db_stats["success"] / total_attempts) * 100, 2) if total_attempts > 0 else 0,
                    "avg_response_time": round(db_stats["avg_response_time"], 3) if db_stats["avg_response_time"] else None
                }
            }
            
            report["databases"].append(db_info)
            
            if result["status"] == "connected":
                report["summary"]["connected"] += 1
            else:
                report["summary"]["disconnected"] += 1
        
        # Determinar base de datos recomendada
        connected_dbs = [db for db in report["databases"] if db["status"] == "connected"]
        if connected_dbs:
            # Ordenar por tiempo de respuesta y tasa de éxito
            connected_dbs.sort(key=lambda x: (
                -x["statistics"]["success_rate"],  # Mayor tasa de éxito primero
                x["response_time"] or 999  # Menor tiempo de respuesta
            ))
            report["summary"]["recommended_primary"] = connected_dbs[0]["name"]
        
        return report
    
    def run_continuous_monitoring(self):
        """Ejecutar monitoreo continuo"""
        self.log_message("🚀 Iniciando monitoreo de base de datos...")
        self.log_message(f"📊 Monitoreando {len(DB_CONFIGS)} bases de datos cada {self.interval} segundos")
        
        try:
            while True:
                report = self.generate_report()
                
                # Log de estado resumido
                summary = report["summary"]
                status_msg = f"📊 Estado: {summary['connected']}/{summary['total_databases']} conectadas"
                if summary["recommended_primary"]:
                    status_msg += f" | Recomendada: {summary['recommended_primary']}"
                
                self.log_message(status_msg)
                
                # Log de errores específicos
                for db in report["databases"]:
                    if db["status"] == "error":
                        error_msg = db["error"]
                        if "timeout" in error_msg.lower():
                            self.log_message(f"⏰ {db['name']}: Timeout de conexión")
                        elif "connection" in error_msg.lower():
                            self.log_message(f"🔌 {db['name']}: Error de conexión de red")
                        else:
                            self.log_message(f"❌ {db['name']}: {error_msg}")
                
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            self.log_message("⏹️ Monitoreo detenido por el usuario")
            self.print_final_report()
        except Exception as e:
            self.log_message(f"❌ Error en monitoreo: {e}")
    
    def print_final_report(self):
        """Imprimir reporte final de estadísticas"""
        uptime = datetime.datetime.now() - self.start_time
        
        print("\n" + "="*60)
        print("📊 REPORTE FINAL DE MONITOREO")
        print("="*60)
        print(f"⏱️ Tiempo de monitoreo: {uptime}")
        print(f"📅 Inicio: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📅 Fin: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for db_name, stats in self.stats.items():
            total = stats["success"] + stats["failures"]
            if total > 0:
                success_rate = (stats["success"] / total) * 100
                print(f"\n🗄️ {db_name}:")
                print(f"   ✅ Conexiones exitosas: {stats['success']}")
                print(f"   ❌ Fallos: {stats['failures']}")
                print(f"   📈 Tasa de éxito: {success_rate:.1f}%")
                if stats["avg_response_time"]:
                    print(f"   ⚡ Tiempo promedio: {stats['avg_response_time']:.3f}s")

def main():
    parser = argparse.ArgumentParser(description="Monitor de base de datos PWA")
    parser.add_argument("--interval", type=int, default=5, help="Intervalo de monitoreo en segundos (default: 5)")
    parser.add_argument("--log-file", type=str, help="Archivo de log para guardar resultados")
    parser.add_argument("--single-check", action="store_true", help="Ejecutar una sola verificación")
    
    args = parser.parse_args()
    
    monitor = DatabaseMonitor(interval=args.interval, log_file=args.log_file)
    
    if args.single_check:
        # Ejecutar una sola verificación
        report = monitor.generate_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        # Ejecutar monitoreo continuo
        monitor.run_continuous_monitoring()

if __name__ == "__main__":
    main()
