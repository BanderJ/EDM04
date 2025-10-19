import os
from dotenv import load_dotenv
from flask import render_template, redirect, url_for
from app import create_app, db
from app.models import User, Certification, Audit, Policy, Alert, AuditLog

# Cargar variables de entorno
load_dotenv()

# Crear aplicación
app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Contexto para el shell interactivo de Flask"""
    return {
        'db': db,
        'User': User,
        'Certification': Certification,
        'Audit': Audit,
        'Policy': Policy,
        'Alert': Alert,
        'AuditLog': AuditLog
    }

@app.route('/')
def index():
    """Ruta raíz - redirige al login o dashboard"""
    from flask_login import current_user
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

@app.errorhandler(404)
def not_found_error(error):
    """Manejo de error 404"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de error 500"""
    try:
        db.session.rollback()
    except:
        pass
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    """Manejo de error 403"""
    return render_template('errors/403.html'), 403

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
