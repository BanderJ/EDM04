#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para iniciar la aplicación Flask y verificar la conexión a MySQL
Autor: Frutos de Oro
Fecha: Octubre 2025
"""

import os
import sys
import time
import subprocess
import socket
from pathlib import Path

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Mostrar encabezado"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("╔" + "═"*78 + "╗")
    print("║" + " "*20 + "🍓 FRUTOS DE ORO - INICIALIZADOR" + " "*25 + "║")
    print("║" + " "*15 + "Sistema de Gestión de Cumplimiento Normativo" + " "*20 + "║")
    print("╚" + "═"*78 + "╝")
    print(f"{Colors.ENDC}\n")

def check_mysql_connection(host='127.0.0.1', port=3307):
    """Verificar si MySQL está disponible"""
    print(f"{Colors.OKCYAN}[1/4]{Colors.ENDC} Verificando conexión a MySQL en {host}:{port}...")
    
    try:
        sock = socket.create_connection((host, port), timeout=2)
        sock.close()
        print(f"{Colors.OKGREEN}✅ MySQL disponible en puerto 3307{Colors.ENDC}\n")
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        print(f"{Colors.WARNING}⚠️  MySQL NO está disponible en puerto 3307{Colors.ENDC}\n")
        return False

def check_venv():
    """Verificar que el entorno virtual existe"""
    print(f"{Colors.OKCYAN}[2/4]{Colors.ENDC} Verificando entorno virtual...")
    
    venv_path = Path('.venv')
    if venv_path.exists():
        print(f"{Colors.OKGREEN}✅ Entorno virtual (.venv) encontrado{Colors.ENDC}\n")
        return True
    else:
        print(f"{Colors.FAIL}❌ Entorno virtual no encontrado{Colors.ENDC}\n")
        print(f"{Colors.WARNING}Crea el entorno virtual con: python -m venv .venv{Colors.ENDC}")
        return False

def check_dependencies():
    """Verificar que las dependencias están instaladas"""
    print(f"{Colors.OKCYAN}[3/4]{Colors.ENDC} Verificando dependencias...")
    
    try:
        import flask
        import sqlalchemy
        import flask_login
        print(f"{Colors.OKGREEN}✅ Todas las dependencias instaladas{Colors.ENDC}\n")
        return True
    except ImportError as e:
        print(f"{Colors.FAIL}❌ Falta instalar: {e}{Colors.ENDC}\n")
        print(f"{Colors.WARNING}Ejecuta: pip install -r requirements.txt{Colors.ENDC}")
        return False

def check_config_files():
    """Verificar archivos de configuración"""
    print(f"{Colors.OKCYAN}[4/4]{Colors.ENDC} Verificando archivos de configuración...")
    
    files = ['config.py', '.env', 'app/__init__.py', 'app.py']
    missing = [f for f in files if not Path(f).exists()]
    
    if missing:
        print(f"{Colors.FAIL}❌ Archivos faltantes: {', '.join(missing)}{Colors.ENDC}\n")
        return False
    else:
        print(f"{Colors.OKGREEN}✅ Todos los archivos de configuración presentes{Colors.ENDC}\n")
        return True

def print_mysql_instructions():
    """Mostrar instrucciones para iniciar MySQL"""
    print(f"\n{Colors.WARNING}{Colors.BOLD}━ INSTRUCCIONES PARA INICIAR MYSQL ━{Colors.ENDC}\n")
    print("Opción 1: XAMPP Control Panel (Recomendado)")
    print("  1. Abre: C:\\xampp\\xampp-control.exe")
    print("  2. Haz click en 'Start' para MySQL")
    print("  3. Espera a que muestre 'Running' en puerto 3307")
    print("  4. Luego ejecuta: .\\venv\\Scripts\\python app.py")
    print("\nOpción 2: Línea de comandos")
    print("  1. Abre cmd.exe")
    print("  2. cd C:\\xampp\\mysql\\bin")
    print("  3. mysql -u root --port=3307 frutos_oro_db")
    print("\n" + "="*80 + "\n")

def start_flask_app():
    """Iniciar la aplicación Flask"""
    print(f"{Colors.OKBLUE}{Colors.BOLD}═ Iniciando Aplicación Flask ═{Colors.ENDC}\n")
    
    try:
        # Ejecutar la aplicación
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Aplicación detenida por el usuario{Colors.ENDC}\n")
    except Exception as e:
        print(f"{Colors.FAIL}Error al iniciar la aplicación: {e}{Colors.ENDC}")

def main():
    """Función principal"""
    print_header()
    
    # Verificaciones
    mysql_available = check_mysql_connection()
    venv_ok = check_venv()
    deps_ok = check_dependencies()
    files_ok = check_config_files()
    
    # Mostrar estado
    print(f"{Colors.BOLD}━ ESTADO GENERAL ━{Colors.ENDC}")
    print(f"MySQL (3307):           {Colors.OKGREEN}✅{Colors.ENDC}" if mysql_available else f"MySQL (3307):           {Colors.WARNING}⚠️{Colors.ENDC}")
    print(f"Entorno virtual:        {Colors.OKGREEN}✅{Colors.ENDC}" if venv_ok else f"Entorno virtual:        {Colors.FAIL}❌{Colors.ENDC}")
    print(f"Dependencias:           {Colors.OKGREEN}✅{Colors.ENDC}" if deps_ok else f"Dependencias:           {Colors.FAIL}❌{Colors.ENDC}")
    print(f"Configuración:          {Colors.OKGREEN}✅{Colors.ENDC}" if files_ok else f"Configuración:          {Colors.FAIL}❌{Colors.ENDC}")
    print()
    
    # Verificar requisitos mínimos
    if not venv_ok or not deps_ok or not files_ok:
        print(f"{Colors.FAIL}❌ No se pueden cumplir los requisitos mínimos.{Colors.ENDC}")
        print("Por favor, revisa los errores anteriores.\n")
        sys.exit(1)
    
    # Si MySQL no está disponible
    if not mysql_available:
        print(f"{Colors.WARNING}{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.WARNING}║  ⚠️  MySQL NO está disponible en puerto 3307                     ║{Colors.ENDC}")
        print(f"{Colors.WARNING}║  La aplicación se ejecutará pero SIN base de datos              ║{Colors.ENDC}")
        print(f"{Colors.WARNING}╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
        
        print_mysql_instructions()
        
        response = input(f"{Colors.BOLD}¿Deseas continuar sin base de datos? (s/n): {Colors.ENDC}").strip().lower()
        if response != 's':
            print(f"{Colors.OKCYAN}Iniciando XAMPP Control Panel...{Colors.ENDC}\n")
            try:
                subprocess.Popen('C:\\xampp\\xampp-control.exe')
                print(f"{Colors.WARNING}Espera a que MySQL esté 'Running' y luego ejecuta esta aplicación nuevamente.{Colors.ENDC}\n")
            except:
                print(f"{Colors.FAIL}No se pudo abrir XAMPP. Abrelo manualmente.{Colors.ENDC}\n")
            sys.exit(0)
    else:
        print(f"{Colors.OKGREEN}{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.OKGREEN}║  ✅ Todos los sistemas están LISTOS                               ║{Colors.ENDC}")
        print(f"{Colors.OKGREEN}║  Iniciando aplicación...                                          ║{Colors.ENDC}")
        print(f"{Colors.OKGREEN}╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
    
    # Iniciar Flask
    print(f"{Colors.OKBLUE}Accesible en: http://localhost:5000{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Presiona Ctrl+C para detener la aplicación{Colors.ENDC}\n")
    
    start_flask_app()
    
    print(f"\n{Colors.OKGREEN}¡Gracias por usar Frutos de Oro!{Colors.ENDC}\n")

if __name__ == '__main__':
    main()
