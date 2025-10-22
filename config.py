import os
from datetime import timedelta
from dotenv import load_dotenv

# ============================================================================
# CONFIGURACIÓN DEL SISTEMA
# ============================================================================
# ⚠️ NO MODIFICAR ESTE ARCHIVO
# ⚠️ Para cambiar configuración, edita el archivo .env
# ============================================================================

# Cargar variables de entorno desde archivo .env
load_dotenv()

class Config:
    """Configuración base de la aplicación
    
    IMPORTANTE: No modifiques este archivo directamente.
    Para cambiar configuración, edita el archivo .env
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-frutos-oro-2025'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    
    # Configuración de carga de archivos
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx'}
    
    # Configuración de correo (lee desde .env)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@frutosoro.com')

class DevelopmentConfig(Config):
    """Configuración de desarrollo - XAMPP MySQL local
    
    ⚠️ NO MODIFICAR ESTA CLASE
    
    Para cambiar credenciales de MySQL:
    1. Copia: .env.example → .env
    2. Edita: .env
    3. Cambia: DB_PORT, DB_PASSWORD, etc.
    
    Este código lee automáticamente desde .env:
    • DB_USER     (usuario MySQL)
    • DB_PASSWORD (contraseña MySQL)
    • DB_HOST     (servidor MySQL)
    • DB_PORT     (puerto MySQL)
    • DB_NAME     (nombre base de datos)
    """
    DEBUG = True
    
    # Lee credenciales desde .env (NO modificar)
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'frutos_oro_db')
    
    # Construye URI de conexión automáticamente
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class ProductionConfig(Config):
    """Configuración de producción - Vercel + MySQL en la nube
    
    Variables de entorno requeridas en Vercel:
    • DB_USER     → Usuario MySQL en la nube
    • DB_PASSWORD → Password MySQL en la nube
    • DB_HOST     → Host MySQL (ej: xxx.connect.psdb.cloud)
    • DB_PORT     → Puerto MySQL (default: 3306)
    • DB_NAME     → Nombre de la base de datos
    • SECRET_KEY  → Clave secreta (32+ caracteres)
    """
    DEBUG = False
    
    # Configuración de sesión más estricta en producción
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Lee credenciales desde variables de entorno de Vercel
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME')
    
    # Construir URI de conexión para MySQL en la nube
    if all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
    else:
        # Fallback si faltan variables
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')
    
    # Pool de conexiones optimizado para serverless
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 2
    }

class TestingConfig(Config):
    """Configuración de pruebas"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
