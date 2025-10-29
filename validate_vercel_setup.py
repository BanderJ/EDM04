#!/usr/bin/env python3
"""
Script de validación para despliegue en Vercel con modo demo
Verifica que todos los archivos necesarios estén presentes
"""
import os
import sys

def check_file_exists(path, description):
    """Verificar si un archivo existe"""
    if os.path.exists(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ FALTA: {description}: {path}")
        return False

def check_folder_exists(path, description):
    """Verificar si una carpeta existe"""
    if os.path.isdir(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ FALTA: {description}: {path}")
        return False

def validate_vercel_setup():
    """Validar configuración para Vercel"""
    print("🔍 Validando configuración para Vercel con modo demo...\n")
    
    all_ok = True
    
    # 1. Verificar archivos de configuración
    print("📋 1. Archivos de configuración:")
    all_ok &= check_file_exists("vercel.json", "Configuración de Vercel")
    all_ok &= check_file_exists("config.py", "Configuración de Flask")
    all_ok &= check_file_exists("requirements.txt", "Dependencias Python")
    print()
    
    # 2. Verificar entry point de Vercel
    print("🚀 2. Entry point de Vercel:")
    all_ok &= check_file_exists("api/index.py", "Handler de Vercel")
    all_ok &= check_file_exists("wsgi.py", "WSGI application")
    print()
    
    # 3. Verificar carpeta de documentos de muestra
    print("📄 3. Documentos de muestra:")
    sample_folder = "app/static/sample_documents"
    all_ok &= check_folder_exists(sample_folder, "Carpeta de documentos de muestra")
    
    if os.path.isdir(sample_folder):
        all_ok &= check_file_exists(
            os.path.join(sample_folder, "certificacion_iso9001.pdf"),
            "PDF ISO 9001"
        )
        all_ok &= check_file_exists(
            os.path.join(sample_folder, "certificacion_haccp.pdf"),
            "PDF HACCP"
        )
    print()
    
    # 4. Verificar archivos estáticos
    print("🎨 4. Archivos estáticos:")
    all_ok &= check_folder_exists("app/static/css", "Carpeta CSS")
    all_ok &= check_folder_exists("app/static/js", "Carpeta JS")
    all_ok &= check_file_exists("app/static/css/style.css", "Estilos principales")
    all_ok &= check_file_exists("app/static/js/main.js", "JavaScript principal")
    print()
    
    # 5. Verificar scripts de inicialización
    print("⚙️ 5. Scripts de inicialización:")
    all_ok &= check_file_exists("init_demo_data.py", "Script de datos de muestra")
    all_ok &= check_file_exists("init.py", "Script de inicialización DB")
    print()
    
    # 6. Verificar templates críticos
    print("📑 6. Templates críticos:")
    all_ok &= check_file_exists("app/templates/base.html", "Template base")
    all_ok &= check_file_exists("app/templates/auth/login.html", "Template login")
    all_ok &= check_file_exists("app/templates/certifications/list.html", "Lista certificaciones")
    all_ok &= check_file_exists("app/templates/reports/index.html", "Reportes")
    print()
    
    # 7. Verificar vercel.json
    print("🔧 7. Validando vercel.json:")
    try:
        import json
        with open('vercel.json', 'r') as f:
            vercel_config = json.load(f)
        
        # Verificar builds
        if 'builds' in vercel_config:
            print("✅ Builds configurados")
            has_python = any(b.get('use') == '@vercel/python' for b in vercel_config['builds'])
            has_static = any(b.get('use') == '@vercel/static' for b in vercel_config['builds'])
            
            if has_python:
                print("   ✅ @vercel/python configurado")
            else:
                print("   ❌ Falta @vercel/python")
                all_ok = False
            
            if has_static:
                print("   ✅ @vercel/static configurado")
            else:
                print("   ⚠️  @vercel/static no configurado (opcional)")
        
        # Verificar routes
        if 'routes' in vercel_config:
            print("✅ Routes configuradas")
            routes = vercel_config['routes']
            has_sample_docs_route = any('/sample_documents/' in r.get('src', '') for r in routes)
            
            if has_sample_docs_route:
                print("   ✅ Ruta para sample_documents configurada")
            else:
                print("   ⚠️  Ruta para sample_documents no encontrada")
        
        # Verificar env
        if 'env' in vercel_config:
            print("✅ Variables de entorno configuradas en vercel.json")
            if 'USE_SAMPLE_DOCUMENTS' in vercel_config['env']:
                value = vercel_config['env']['USE_SAMPLE_DOCUMENTS']
                print(f"   ✅ USE_SAMPLE_DOCUMENTS = {value}")
            else:
                print("   ⚠️  USE_SAMPLE_DOCUMENTS no configurado")
        
    except Exception as e:
        print(f"❌ Error al leer vercel.json: {e}")
        all_ok = False
    print()
    
    # 8. Verificar config.py
    print("🔧 8. Validando config.py:")
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        if 'USE_SAMPLE_DOCUMENTS' in config_content:
            print("✅ USE_SAMPLE_DOCUMENTS definido en config.py")
        else:
            print("❌ USE_SAMPLE_DOCUMENTS no encontrado en config.py")
            all_ok = False
        
        if 'SAMPLE_DOCUMENTS_FOLDER' in config_content:
            print("✅ SAMPLE_DOCUMENTS_FOLDER definido en config.py")
        else:
            print("❌ SAMPLE_DOCUMENTS_FOLDER no encontrado en config.py")
            all_ok = False
        
    except Exception as e:
        print(f"❌ Error al leer config.py: {e}")
        all_ok = False
    print()
    
    # Resultado final
    print("=" * 60)
    if all_ok:
        print("🎉 ¡VALIDACIÓN EXITOSA!")
        print("✅ El proyecto está listo para desplegar en Vercel")
        print("\n📝 Próximos pasos:")
        print("   1. git add .")
        print("   2. git commit -m 'feat: modo demo con documentos de muestra'")
        print("   3. git push")
        print("   4. vercel --prod")
        print("   5. python init_demo_data.py (después del deploy)")
        return 0
    else:
        print("❌ VALIDACIÓN FALLIDA")
        print("⚠️  Hay archivos faltantes o configuración incompleta")
        print("   Por favor, revisa los errores arriba")
        return 1

if __name__ == '__main__':
    try:
        exit_code = validate_vercel_setup()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
