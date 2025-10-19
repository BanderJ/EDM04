#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Inicialización - Frutos de Oro S.A.C.
Sistema de Gestión de Cumplimiento Normativo
Crea la base de datos y carga datos iniciales
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def main():
    print("=" * 80)
    print("  FRUTOS DE ORO - Sistema de Gestión de Cumplimiento Normativo")
    print("  Script de Inicialización")
    print("=" * 80)
    print()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('app.py'):
        print("[ERROR] No se encontró app.py. Asegúrate de ejecutar este script desde")
        print("        la raíz del proyecto (D:\\Apps\\EDM04)")
        sys.exit(1)
    
    # Verificar que existe app/
    if not os.path.exists('app'):
        print("[ERROR] No se encontró la carpeta app/")
        sys.exit(1)
    
    print("[*] Verificando entorno...")
    
    # Verificar Python
    print(f"    Python: {sys.version.split()[0]}")
    
    # Verificar carpetas
    folders = ['uploads', 'uploads/certifications', 'database']
    for folder in folders:
        if not os.path.exists(folder):
            print(f"[!] Creando carpeta: {folder}")
            os.makedirs(folder, exist_ok=True)
        else:
            print(f"[OK] Carpeta existe: {folder}")
    
    print()
    print("[*] Verificando archivo de configuración...")
    
    # Verificar .env
    if not os.path.exists('.env'):
        print("[!] El archivo .env no existe")
        if os.path.exists('.env.example'):
            print("    Copiando .env.example a .env...")
            import shutil
            shutil.copy('.env.example', '.env')
            print("[OK] .env creado. Por favor, edítalo con tus datos.")
        else:
            print("[!] Tampoco existe .env.example")
    else:
        print("[OK] Archivo .env existe")
    
    print()
    print("[*] Iniciando aplicación...")
    print()
    print("="*80)
    print("  ¡Aplicación lista para ejecutar!")
    print("="*80)
    print()
    print("  Próximos pasos:")
    print()
    print("  1. Edita el archivo .env con tus configuraciones")
    print("  2. Configura la base de datos (MySQL o PostgreSQL)")
    print("  3. Ejecuta: python app.py")
    print()
    print("  La aplicación estará disponible en:")
    print("  → http://localhost:5000")
    print()
    print("  Credenciales de acceso:")
    print("  → Usuario: admin")
    print("  → Contraseña: admin123")
    print()
    print("="*80)
    print()
    
    # Preguntar si ejecutar la aplicación
    response = input("¿Deseas ejecutar la aplicación ahora? (s/n): ").lower().strip()
    if response == 's':
        print()
        print("[*] Iniciando Flask...")
        try:
            from app import create_app
            app = create_app()
            print("[OK] Aplicación iniciada")
            print()
            print("    Abre tu navegador en: http://localhost:5000")
            print()
            app.run(debug=True, host='0.0.0.0', port=5000)
        except Exception as e:
            print(f"[ERROR] No se pudo iniciar la aplicación: {e}")
            sys.exit(1)
    else:
        print()
        print("[OK] Inicialización completada.")
        print()
        print("Cuando estés listo, ejecuta:")
        print("  python app.py")
        print()

if __name__ == '__main__':
    main()
