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
    from app.utils import get_action_display_name
    
    @app.context_processor
    def inject_permissions():
        """Inyecta funciones útiles en todos los templates"""
        return dict(
            check_permission=check_permission,
            get_action_display_name=get_action_display_name
        )
    
    # Registrar filtros personalizados
    @app.template_filter('format_audit_changes')
    def format_audit_changes(changes_text):
        """Formatea el texto de cambios para que sea más legible"""
        if not changes_text:
            return ''
        
        import json
        
        # Si ya es texto descriptivo (no JSON), devolverlo tal cual
        if not changes_text.strip().startswith('{'):
            return changes_text
        
        # Intentar parsear como JSON y formatear
        try:
            changes_dict = json.loads(changes_text)
            
            # Importar modelos para obtener nombres reales
            from app.models import Role, Module
            
            # Mapeo de nombres técnicos a nombres amigables
            field_names = {
                'role_id': 'Rol',
                'module_id': 'Módulo',
                'can_view': 'Permiso Ver',
                'can_create': 'Permiso Crear',
                'can_edit': 'Permiso Editar',
                'can_delete': 'Permiso Eliminar',
                'can_export': 'Permiso Exportar',
                'can_approve': 'Permiso Aprobar',
                'username': 'Usuario',
                'old_status': 'Estado anterior',
                'new_status': 'Estado nuevo',
                'full_name': 'Nombre completo',
                'email': 'Correo electrónico',
                'role': 'Rol',
                'department': 'Departamento'
            }
            
            # Mapeo de valores booleanos
            bool_map = {
                True: '✓ Activado',
                False: '✗ Desactivado',
                'true': '✓ Activado',
                'false': '✗ Desactivado'
            }
            
            formatted_lines = []
            for key, value in changes_dict.items():
                # Traducir nombre del campo
                field_label = field_names.get(key, key)
                
                # Formatear valor según el tipo de campo
                if key == 'role_id':
                    # Buscar nombre del rol
                    try:
                        role = Role.query.get(int(value))
                        formatted_value = role.display_name if role else f"Rol #{value}"
                    except:
                        formatted_value = f"Rol #{value}"
                        
                elif key == 'module_id':
                    # Buscar nombre del módulo
                    try:
                        module = Module.query.get(int(value))
                        formatted_value = module.display_name if module else f"Módulo #{value}"
                    except:
                        formatted_value = f"Módulo #{value}"
                        
                elif isinstance(value, bool) or value in ['true', 'false']:
                    formatted_value = bool_map.get(value, value)
                    
                elif value == 'active':
                    formatted_value = '✓ Activo'
                elif value == 'inactive':
                    formatted_value = '✗ Inactivo'
                else:
                    formatted_value = value
                
                formatted_lines.append(f"• {field_label}: {formatted_value}")
            
            return '\n'.join(formatted_lines)
            
        except (json.JSONDecodeError, Exception) as e:
            # Si falla el parseo, devolver el texto original
            return changes_text
    
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
