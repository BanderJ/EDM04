#!/usr/bin/env python
"""
Script para inicializar la base de datos en producción (Vercel)
Ejecutar una sola vez después del primer deploy
"""
import os
import sys
from getpass import getpass
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar aplicación
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def init_production_db():
    """Inicializar base de datos en producción"""
    
    print("=" * 60)
    print("🚀 INICIALIZACIÓN DE BASE DE DATOS EN PRODUCCIÓN")
    print("=" * 60)
    print()
    
    # Crear aplicación en modo producción
    app = create_app('production')
    
    with app.app_context():
        print("📊 Verificando conexión a la base de datos...")
        
        try:
            # Verificar conexión
            db.engine.connect()
            print("✅ Conexión exitosa a la base de datos")
            print()
            
            # Crear tablas
            print("🔧 Creando tablas en la base de datos...")
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            print()
            
            # Verificar si ya existe un usuario admin
            admin_exists = User.query.filter_by(role='admin').first()
            
            if admin_exists:
                print("⚠️  Ya existe un usuario administrador")
                print(f"   Usuario: {admin_exists.username}")
                print(f"   Email: {admin_exists.email}")
                print()
                respuesta = input("¿Desea crear un nuevo administrador? (s/N): ")
                
                if respuesta.lower() != 's':
                    print("❌ Operación cancelada")
                    return
                print()
            
            # Solicitar datos del administrador
            print("👤 CREAR USUARIO ADMINISTRADOR")
            print("-" * 60)
            
            username = input("Nombre de usuario (ej: admin): ").strip()
            if not username:
                print("❌ Error: El nombre de usuario es requerido")
                return
            
            email = input("Email: ").strip()
            if not email:
                print("❌ Error: El email es requerido")
                return
            
            full_name = input("Nombre completo: ").strip()
            if not full_name:
                print("❌ Error: El nombre completo es requerido")
                return
            
            password = getpass("Contraseña: ")
            if len(password) < 8:
                print("❌ Error: La contraseña debe tener al menos 8 caracteres")
                return
            
            password_confirm = getpass("Confirmar contraseña: ")
            if password != password_confirm:
                print("❌ Error: Las contraseñas no coinciden")
                return
            
            print()
            print("🔐 Creando usuario administrador...")
            
            # Verificar si el usuario ya existe
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                print(f"❌ Error: Ya existe un usuario con ese nombre de usuario o email")
                return
            
            # Crear usuario administrador
            admin_user = User(
                username=username,
                email=email,
                full_name=full_name,
                role='admin',
                is_active=True
            )
            admin_user.set_password(password)
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Usuario administrador creado exitosamente")
            print()
            print("=" * 60)
            print("🎉 BASE DE DATOS INICIALIZADA CORRECTAMENTE")
            print("=" * 60)
            print()
            print("📝 Credenciales del administrador:")
            print(f"   Usuario: {username}")
            print(f"   Email: {email}")
            print(f"   Nombre: {full_name}")
            print()
            print("🌐 Puedes acceder al sistema en:")
            print("   https://tu-proyecto.vercel.app")
            print()
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print()
            print("🔍 Verificar:")
            print("   • Variables de entorno configuradas en Vercel")
            print("   • Credenciales de MySQL correctas")
            print("   • Base de datos creada en el servidor")
            print("   • Firewall permite conexiones desde Vercel")
            sys.exit(1)

if __name__ == '__main__':
    init_production_db()
