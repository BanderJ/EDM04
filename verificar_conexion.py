"""
Script para verificar la conexión a MySQL y validar configuración
Ejecutar antes de iniciar la aplicación para diagnosticar problemas
"""
import os
import sys
from dotenv import load_dotenv
import pymysql

# Cargar variables de entorno
load_dotenv()

print("=" * 80)
print("VERIFICACIÓN DE CONEXIÓN A MYSQL")
print("=" * 80)

# Leer configuración desde .env
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = int(os.environ.get('DB_PORT', '3306'))
DB_NAME = os.environ.get('DB_NAME', 'frutos_oro_db')

print("\n📋 CONFIGURACIÓN DETECTADA:")
print(f"   Usuario: {DB_USER}")
print(f"   Contraseña: {'(vacía)' if not DB_PASSWORD else '***'}")
print(f"   Host: {DB_HOST}")
print(f"   Puerto: {DB_PORT}")
print(f"   Base de datos: {DB_NAME}")

# Verificar si existe el archivo .env
if not os.path.exists('.env'):
    print("\n⚠️  ADVERTENCIA: No se encontró el archivo .env")
    print("   Crea el archivo .env copiando .env.example:")
    print("   Windows: copy .env.example .env")
    print("   Linux/Mac: cp .env.example .env")
    print("=" * 80)
    sys.exit(1)

# Intentar conexión
print("\n🔌 Intentando conectar a MySQL...")

try:
    # Conectar sin especificar base de datos primero
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    print("✅ Conexión exitosa a MySQL")
    
    # Verificar si existe la base de datos
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]
    
    if DB_NAME in databases:
        print(f"✅ Base de datos '{DB_NAME}' encontrada")
        
        # Conectar a la base de datos específica
        connection.select_db(DB_NAME)
        
        # Verificar tablas
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        print(f"\n📊 Tablas encontradas ({len(tables)}):")
        expected_tables = ['users', 'certifications', 'audits', 'audit_findings', 
                          'policies', 'policy_confirmations', 'alerts', 'audit_logs']
        
        for table in expected_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table} ({count} registros)")
            else:
                print(f"   ❌ {table} (no encontrada)")
        
        # Verificar usuario admin
        cursor.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
        admin_exists = cursor.fetchone()[0] > 0
        
        if admin_exists:
            print("\n✅ Usuario 'admin' encontrado en la base de datos")
        else:
            print("\n⚠️  Usuario 'admin' NO encontrado")
            print("   Ejecuta el script database/schema.sql para crear datos iniciales")
        
    else:
        print(f"❌ Base de datos '{DB_NAME}' NO encontrada")
        print(f"\n📝 Bases de datos disponibles:")
        for db in databases:
            print(f"   - {db}")
        print(f"\n💡 Solución:")
        print(f"   1. Abre phpMyAdmin (http://localhost/phpmyadmin)")
        print(f"   2. Ejecuta el archivo database/schema.sql")
        print(f"   O desde terminal: mysql -u {DB_USER} -p < database/schema.sql")
    
    cursor.close()
    connection.close()
    
    print("\n" + "=" * 80)
    print("✅ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print("\n🚀 Puedes iniciar la aplicación con: python app.py")
    
except pymysql.err.OperationalError as e:
    error_code = e.args[0]
    
    print(f"\n❌ ERROR DE CONEXIÓN: {e}")
    
    if error_code == 2003:
        print("\n💡 SOLUCIONES:")
        print("   1. Verifica que XAMPP MySQL esté ejecutándose")
        print("   2. Abre el Panel de Control de XAMPP")
        print("   3. Inicia el servicio 'MySQL'")
        print("   4. Verifica el puerto en XAMPP (puede ser 3306 o 3307)")
        
    elif error_code == 1045:
        print("\n💡 SOLUCIONES:")
        print("   1. Verifica el usuario y contraseña en el archivo .env")
        print("   2. Por defecto en XAMPP:")
        print("      DB_USER=root")
        print("      DB_PASSWORD=   (vacío)")
        
    elif error_code == 2002:
        print("\n💡 SOLUCIONES:")
        print("   1. Verifica que el host sea correcto (127.0.0.1 o localhost)")
        print("   2. Verifica que el puerto sea correcto en .env")
    
    print("\n" + "=" * 80)
    sys.exit(1)

except Exception as e:
    print(f"\n❌ ERROR INESPERADO: {e}")
    print("\n" + "=" * 80)
    sys.exit(1)
