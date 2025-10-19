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
    
    # Registrar blueprints
    from app.routes import auth_bp, dashboard_bp, certifications_bp, audits_bp, policies_bp, reports_bp, admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(certifications_bp)
    app.register_blueprint(audits_bp)
    app.register_blueprint(policies_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(admin_bp)
    
    # Crear contexto de aplicación e intentar inicializar BD
    with app.app_context():
        try:
            db.create_all()
            print("✅ Base de datos conectada exitosamente")
        except Exception as e:
            print("\n" + "="*80)
            print("⚠️  ADVERTENCIA: No se pudo conectar a MySQL")
            print("="*80)
            print("\n📋 Configuración esperada:")
            print("   • Host: 127.0.0.1")
            print("   • Puerto: 3307")
            print("   • Usuario: root")
            print("   • Contraseña: (vacía)")
            print("   • BD: frutos_oro_db")
            print("\n🔧 Solución:")
            print("   1. Abre XAMPP Control Panel")
            print("   2. Haz click en 'Start' para MySQL")
            print("   3. Espera a que muestre 'Running' en puerto 3307")
            print("   4. Reinicia esta aplicación")
            print("\n📝 Más información en: INSTALACION_MYSQL.md")
            print("="*80 + "\n")
            
            # La aplicación continúa ejecutándose aunque no esté la BD
            app.config['DB_ERROR'] = True
    
    return app
