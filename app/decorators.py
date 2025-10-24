"""
Decoradores personalizados para control de acceso
"""
from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user


def require_permission(module_name, action):
    """
    Decorador para verificar permisos antes de ejecutar una ruta
    
    Args:
        module_name (str): Nombre del módulo (ej: 'certifications', 'audits', 'policies')
        action (str): Acción requerida (ej: 'view', 'create', 'edit', 'delete', 'export', 'approve')
    
    Uso:
        @app.route('/audits/new', methods=['GET', 'POST'])
        @login_required
        @require_permission('audits', 'create')
        def new_audit():
            # Solo usuarios con permiso can_create en audits pueden acceder
            pass
    
    Si el usuario no tiene el permiso, devuelve un error 403 Forbidden
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debe iniciar sesión para acceder a esta página', 'warning')
                return redirect(url_for('auth.login'))
            
            if not current_user.can(module_name, action):
                flash(f'No tiene permisos para realizar esta acción en {module_name}', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """
    Decorador para rutas que solo pueden ser accedidas por administradores
    
    Uso:
        @app.route('/admin/settings')
        @login_required
        @admin_required
        def admin_settings():
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debe iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.role != 'administrador':
            flash('Solo los administradores pueden acceder a esta sección', 'danger')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """
    Decorador para verificar que el usuario tenga uno de los roles especificados
    
    Args:
        *roles: Lista de roles permitidos (ej: 'administrador', 'jefe_calidad', 'auditor')
    
    Uso:
        @app.route('/quality/dashboard')
        @login_required
        @role_required('administrador', 'jefe_calidad', 'jefe_produccion')
        def quality_dashboard():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debe iniciar sesión para acceder a esta página', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in roles:
                flash('No tiene los permisos necesarios para acceder a esta sección', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def check_permission(module_name, action):
    """
    Función auxiliar para verificar permisos en templates o código
    
    Args:
        module_name (str): Nombre del módulo
        action (str): Acción a verificar
    
    Returns:
        bool: True si el usuario tiene el permiso
    
    Uso en template Jinja2:
        {% if check_permission('audits', 'edit') %}
            <button>Editar</button>
        {% endif %}
    
    Uso en código Python:
        if check_permission('policies', 'delete'):
            # Permitir eliminación
    """
    if not current_user.is_authenticated:
        return False
    
    return current_user.can(module_name, action)
