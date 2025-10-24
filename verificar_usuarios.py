"""
Script para verificar y crear usuario administrador en la base de datos
"""
from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    try:
        # Verificar conexión
        print("🔍 Verificando conexión a la base de datos...")
        db.engine.connect()
        print("✅ Conexión exitosa!")
        
        # Verificar si existe la tabla users
        print("\n🔍 Verificando tablas...")
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"✅ Tablas encontradas: {', '.join(tables)}")
        
        if 'users' not in tables:
            print("\n⚠️ La tabla 'users' no existe. Creando tablas...")
            db.create_all()
            print("✅ Tablas creadas!")
        
        # Contar usuarios
        print("\n🔍 Verificando usuarios...")
        user_count = User.query.count()
        print(f"📊 Total de usuarios: {user_count}")
        
        if user_count == 0:
            print("\n⚠️ No hay usuarios. Creando usuario administrador...")
            
            # Crear usuario admin
            admin = User(
                username='admin',
                email='admin@frutosoro.com',
                full_name='Administrador Sistema',
                department='Dirección',
                role='administrador',
                is_active=True
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Usuario administrador creado exitosamente!")
            print("\n📋 Credenciales:")
            print("   Usuario: admin")
            print("   Contraseña: admin123")
            print("   ⚠️ CAMBIA esta contraseña después del primer login")
        else:
            print("\n📋 Usuarios existentes:")
            users = User.query.all()
            for user in users:
                status = "✅ Activo" if user.is_active else "❌ Inactivo"
                print(f"   • {user.username} ({user.full_name}) - Rol: {user.role} - {status}")
            
            # Verificar si existe admin
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print(f"\n✅ Usuario 'admin' existe - Estado: {'Activo' if admin.is_active else 'Inactivo'}")
                print("   Puedes iniciar sesión con: admin / admin123")
            else:
                print("\n⚠️ No existe usuario 'admin'")
                create = input("¿Deseas crear el usuario admin? (s/n): ")
                if create.lower() == 's':
                    admin = User(
                        username='admin',
                        email='admin@frutosoro.com',
                        full_name='Administrador Sistema',
                        department='Dirección',
                        role='administrador',
                        is_active=True
                    )
                    admin.set_password('admin123')
                    db.session.add(admin)
                    db.session.commit()
                    print("✅ Usuario administrador creado!")
        
        print("\n" + "="*80)
        print("✅ Verificación completada exitosamente")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nDetalles del error:")
        import traceback
        traceback.print_exc()
