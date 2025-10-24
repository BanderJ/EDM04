from flask import Flask
from flask_login import LoginManager
from config import config
from app.models import db, User
import os

def create_app(config_name='development'):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Configurar login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except:
            return None
    
    # Registrar context processors para templates
    from app.decorators import check_permission
    
    @app.context_processor
    def inject_permissions():
        """Inyecta la función check_permission en todos los templates"""
        return dict(check_permission=check_permission)
    
    # Registrar blueprints
    from app.routes import auth_bp, dashboard_bp, certifications_bp, audits_bp, policies_bp, reports_bp, admin_bp, api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(certifications_bp)
    app.register_blueprint(audits_bp)
    app.register_blueprint(policies_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    
    # Crear contexto de aplicación e intentar inicializar BD
    with app.app_context():
        try:
            db.create_all()
            
            # Obtener configuración de BD
            db_config = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if 'postgresql' in db_config:
                db_type = "PostgreSQL"
            elif 'mysql' in db_config:
                db_type = "MySQL"
            else:
                db_type = "Base de datos"
            
            print(f"✅ {db_type} conectada exitosamente")
            print(f"   Host: {app.config.get('DB_HOST', 'N/A')}")
            print(f"   Puerto: {app.config.get('DB_PORT', 'N/A')}")
            print(f"   Base de datos: {app.config.get('DB_NAME', 'N/A')}")
            
        except Exception as e:
            db_host = app.config.get('DB_HOST', 'N/A')
            db_port = app.config.get('DB_PORT', 'N/A')
            db_name = app.config.get('DB_NAME', 'N/A')
            db_user = app.config.get('DB_USER', 'N/A')
            
            print("\n" + "="*80)
            print("⚠️  ADVERTENCIA: No se pudo conectar a la base de datos")
            print("="*80)
            print(f"\n📋 Configuración actual (.env):")
            print(f"   • Host: {db_host}")
            print(f"   • Puerto: {db_port}")
            print(f"   • Usuario: {db_user}")
            print(f"   • Base de datos: {db_name}")
            print(f"\n❌ Error: {str(e)[:150]}")
            print("\n🔧 Posibles soluciones:")
            print("   1. Verifica que la base de datos esté corriendo")
            print("   2. Verifica las credenciales en el archivo .env")
            print("   3. Verifica la conectividad de red (firewall/security groups)")
            print("   4. Verifica que el puerto esté correcto")
            print("="*80 + "\n")
            
            # La aplicación continúa ejecutándose aunque no esté la BD
            app.config['DB_ERROR'] = True
    
    return app
