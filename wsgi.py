"""
WSGI Config para producción (EC2, PythonAnywhere, etc.)
"""
import sys
import os
from dotenv import load_dotenv

# Agregar el directorio actual al path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Cargar variables de entorno
load_dotenv(os.path.join(project_dir, '.env'))

# Importar la aplicación desde app.py (no desde el paquete app/)
from app import app as application

# Para compatibilidad con diferentes servidores
app = application
