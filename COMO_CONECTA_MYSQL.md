# 🔌 FLUJO DE CONEXIÓN A MYSQL - Sistema Frutos de Oro

## 📊 Diagrama de Flujo de Conexión

```
┌─────────────────────────────────────────────────────────────────┐
│                    1. INICIO DE APLICACIÓN                       │
│                         python app.py                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    2. CARGAR VARIABLES .env                       │
│                    Archivo: app.py (línea 2)                      │
│                    load_dotenv()                                  │
│                                                                   │
│  Lee el archivo .env:                                            │
│  • DB_USER=root                                                  │
│  • DB_PASSWORD=                                                  │
│  • DB_HOST=127.0.0.1                                            │
│  • DB_PORT=3306                                                  │
│  • DB_NAME=frutos_oro_db                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                3. CARGAR CONFIGURACIÓN (config.py)                │
│                                                                   │
│  DevelopmentConfig.SQLALCHEMY_DATABASE_URI:                      │
│  mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/..  │
│                                                                   │
│  Resultado:                                                       │
│  mysql+pymysql://root:@127.0.0.1:3306/frutos_oro_db            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              4. CREAR APLICACIÓN FLASK (app.py)                   │
│              app = create_app('development')                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            5. INICIALIZAR SQLALCHEMY (app/__init__.py)            │
│            db.init_app(app)                                       │
│                                                                   │
│  SQLAlchemy configura la conexión usando el URI:                 │
│  mysql+pymysql://root:@127.0.0.1:3306/frutos_oro_db            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              6. INTENTAR CONEXIÓN A MYSQL                         │
│              db.create_all() - Línea 43 de __init__.py           │
│                                                                   │
│  PyMySQL intenta conectar:                                       │
│  • Host: 127.0.0.1                                              │
│  • Puerto: 3306                                                  │
│  • Usuario: root                                                 │
│  • Sin contraseña                                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
     ┌──────────────────┐      ┌──────────────────┐
     │   ✅ ÉXITO       │      │   ❌ ERROR       │
     │                  │      │                  │
     │ Mensaje:         │      │ Muestra:         │
     │ "✅ Base de     │      │ • Configuración  │
     │  datos          │      │ • Solución       │
     │  conectada"     │      │ • Pasos XAMPP    │
     │                  │      │                  │
     │ App lista ✓     │      │ App continúa     │
     └──────────────────┘      └──────────────────┘
```

## 🔍 ARCHIVOS INVOLUCRADOS EN LA CONEXIÓN

### 1️⃣ **`.env`** (Variables de Entorno)
```bash
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=frutos_oro_db
```
**Propósito:** Almacenar credenciales de MySQL de cada desarrollador

---

### 2️⃣ **`app.py`** (Punto de Entrada)
```python
# Línea 2: Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Línea 9: Crear aplicación con configuración
app = create_app(os.environ.get('FLASK_ENV', 'development'))
```
**Propósito:** Iniciar la aplicación y cargar variables .env

---

### 3️⃣ **`config.py`** (Configuración de BD)
```python
# Líneas 5-6: Cargar variables
from dotenv import load_dotenv
load_dotenv()

# Líneas 41-46: Construir URI de conexión
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_NAME = os.environ.get('DB_NAME', 'frutos_oro_db')

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
```
**Propósito:** Construir la cadena de conexión a MySQL

**Formato URI:**
```
mysql+pymysql://usuario:contraseña@host:puerto/nombre_base_datos
        │          │         │        │     │          │
        │          │         │        │     │          └─ Nombre BD
        │          │         │        │     └─ Puerto MySQL (3306 o 3307)
        │          │         │        └─ Host (127.0.0.1 o localhost)
        │          │         └─ Contraseña (vacía en XAMPP por defecto)
        │          └─ Usuario (root en XAMPP)
        └─ Driver para conectar Python con MySQL
```

---

### 4️⃣ **`app/__init__.py`** (Inicialización Flask)
```python
# Línea 3: Importar configuración
from config import config

# Línea 9: Aplicar configuración
app.config.from_object(config[config_name])

# Línea 13: Inicializar SQLAlchemy con la configuración
db.init_app(app)

# Líneas 43-45: Intentar conexión
with app.app_context():
    try:
        db.create_all()  # ← AQUÍ SE CONECTA A MYSQL
        print("✅ Base de datos conectada exitosamente")
    except Exception as e:
        print("⚠️ Error de conexión...")
```
**Propósito:** Inicializar SQLAlchemy y conectar a MySQL

---

### 5️⃣ **`app/models.py`** (Modelos de Base de Datos)
```python
# Línea 7: Crear instancia de SQLAlchemy
db = SQLAlchemy()

# Luego se definen los modelos:
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # ...
```
**Propósito:** Definir la estructura de las tablas

---

## 🔄 PROCESO DETALLADO DE CONEXIÓN

### Paso 1: Lectura de Variables
```python
# app.py ejecuta:
load_dotenv()  # Lee .env y carga las variables en os.environ
```

### Paso 2: Construcción del URI
```python
# config.py construye:
DB_USER = os.environ.get('DB_USER', 'root')        # 'root'
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')    # ''
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')  # '127.0.0.1'
DB_PORT = os.environ.get('DB_PORT', '3306')        # '3306'
DB_NAME = os.environ.get('DB_NAME', 'frutos_oro_db') # 'frutos_oro_db'

# Resultado:
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/frutos_oro_db'
```

### Paso 3: Inicialización de SQLAlchemy
```python
# app/__init__.py ejecuta:
db.init_app(app)  # SQLAlchemy recibe la configuración con el URI
```

### Paso 4: Conexión Real a MySQL
```python
# Cuando se ejecuta db.create_all():
# 1. PyMySQL abre socket TCP a 127.0.0.1:3306
# 2. Envía credenciales: usuario='root', password=''
# 3. Intenta seleccionar BD: 'frutos_oro_db'
# 4. Si existe, crea tablas faltantes (si no existen)
```

---

## 🛠️ CÓMO CAMBIAR LA CONFIGURACIÓN

### Opción 1: Modificar archivo `.env` (RECOMENDADO)
```bash
# Editar D:\Apps\EDM04\.env
DB_USER=root
DB_PASSWORD=mi_contraseña
DB_HOST=127.0.0.1
DB_PORT=3307          # ← Cambiar puerto si XAMPP usa 3307
DB_NAME=frutos_oro_db
```

### Opción 2: Variables de Sistema (Avanzado)
```powershell
# PowerShell
$env:DB_PORT="3307"
python app.py
```

---

## 🐛 DEBUGGING: Ver la Conexión Real

Agrega esto en `app/__init__.py` después de la línea 43:

```python
# Ver URI de conexión (sin mostrar contraseña)
uri = app.config['SQLALCHEMY_DATABASE_URI']
safe_uri = uri.replace(f":{DB_PASSWORD}@", ":***@") if DB_PASSWORD else uri
print(f"🔌 Conectando a: {safe_uri}")
```

---

## 📝 RESUMEN

**¿Dónde se conecta?**
→ En `app/__init__.py`, línea 43: `db.create_all()`

**¿Cómo obtiene las credenciales?**
→ Desde archivo `.env` → `config.py` → Flask app → SQLAlchemy

**¿Qué driver usa?**
→ `pymysql` (instalado en requirements.txt)

**¿Cuándo se conecta?**
→ Al iniciar la aplicación con `python app.py`

**¿Dónde cambiar configuración?**
→ Editar archivo `.env` (cada desarrollador tiene el suyo)

---

## 🧪 PROBAR LA CONEXIÓN

Ejecuta el script de verificación:
```bash
python verificar_conexion.py
```

Este script te mostrará:
- ✅ Configuración detectada
- ✅ Estado de conexión
- ✅ Tablas encontradas
- ✅ Número de registros
- ❌ Errores y soluciones
