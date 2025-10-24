"""
WSGI Config para PythonAnywhere
"""
import sys
import os
from dotenv import load_dotenv

# Agregar el path del proyecto
path = '/home/TU_USUARIO/EDM04'  # Cambiar TU_USUARIO por tu nombre de usuario de PythonAnywhere
if path not in sys.path:
    sys.path.insert(0, path)

# Cargar variables de entorno
load_dotenv(os.path.join(path, '.env'))

# Importar la aplicación
from app import create_app

# Crear aplicación
application = create_app(os.environ.get('FLASK_ENV', 'production'))
