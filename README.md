# 🍓 Sistema de Gestión de Cumplimiento Normativo
## Agroindustria Frutos de Oro S.A.C.

Plataforma web administrativa para gestionar, registrar y monitorear el cumplimiento de certificaciones, auditorías y normativas legales relacionadas con exportación de frutas congeladas.

---

## 🚀 **DEPLOY EN VERCEL (PRODUCCIÓN)**

### 🌐 Subir a Vercel desde la Web (Recomendado)

| 📌 **Deploy Web** | Archivo | Descripción |
|------------------|---------|-------------|
| **RECOMENDADO** | **`DEPLOY_WEB_VERCEL.md`** | 👉 **Deploy desde vercel.com sin CLI** |
| Índice | `INDICE_DEPLOY_VERCEL.md` | Guía de todas las opciones disponibles |

**Ventajas del deploy desde la web**:
- ✅ No necesitas instalar nada
- ✅ Interface visual fácil
- ✅ Obtienes dominio: `edm04.vercel.app`
- ✅ Deploy automático en cada push a GitHub

### 📋 Otras opciones de deploy:

| Método | Archivo | Para quién |
|--------|---------|------------|
| CLI Rápido | `DEPLOY_RAPIDO.md` | Usuarios que prefieren terminal |
| Completo | `DEPLOY_VERCEL.md` | Guía detallada con todas las opciones |

---

## 🏠 **DESARROLLO LOCAL? LEE ESTO PRIMERO**

### 📝 Guías de Inicio Rápido

| 🔴 **IMPORTANTE** | Archivo | Descripción |
|------------------|---------|-------------|
| **LEER PRIMERO** | **`CONFIGURAR_MYSQL.txt`** | 👉 **Guía paso a paso para configurar tu base de datos local** |
| Resumen | `INICIO_RAPIDO.txt` | Pasos rápidos de instalación |
| Completa | `README_INSTALACION.md` | Guía de instalación detallada |
| Técnico | `COMO_CONECTA_MYSQL.md` | Cómo funciona la conexión a MySQL |

### ⚡ Pasos Rápidos
```bash
# 1. Clonar proyecto
git clone <URL_REPOSITORIO>
cd EDM04

# 2. Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos (LEE: CONFIGURAR_MYSQL.txt)
copy .env.example .env
# Edita .env con tus credenciales de XAMPP

# 5. Verificar conexión
python verificar_conexion.py

# 6. Ejecutar aplicación
python app.py
```

**Usuario:** `admin` | **Contraseña:** `admin123`

---

## �📋 Características Principales

### 1. **Módulo de Certificaciones**
- Registro de certificaciones (GlobalG.A.P., HACCP, BRC, ISO 22000, etc.)
- Adjuntar documentos escaneados (PDF, JPG, PNG, DOC, DOCX)
- Alertas automáticas por vencimiento (15, 30 y 60 días)
- Seguimiento de estado (Vigente, Próxima a Vencer, Vencida)
- Responsable asignado por certificación

### 2. **Módulo de Auditorías**
- Programación de auditorías internas y externas
- Registro de hallazgos y observaciones
- Acciones correctivas con fechas límite
- Indicadores de cumplimiento
- Clasificación de severidad (Crítica, Mayor, Menor)

### 3. **Módulo de Políticas**
- Publicación de políticas de cumplimiento
- Confirmación de cumplimiento por usuario
- Reporte de confirmaciones por área
- Versionamiento de políticas
- Firma digital

### 4. **Módulo de Reportes**
- Dashboard con gráficos interactivos
- Porcentaje de certificaciones vigentes
- Auditorías aprobadas
- Cumplimiento de políticas por unidad
- Exportación a PDF y Excel

### 5. **Administración**
- Gestión de usuarios por roles
- Sistema de auditoría del sistema
- Registro de cambios
- Control de acceso basado en roles (RBAC)

---

## 🔧 Requerimientos Técnicos

### Backend
- **Python** 3.8+
- **Flask** 2.3.3
- **Flask-SQLAlchemy** para ORM
- **Flask-Login** para autenticación

### Base de Datos
- **MySQL** 5.7+ O **PostgreSQL** 12+

### Frontend
- **HTML5**
- **CSS3**
- **Bootstrap** 5.3
- **jQuery** 3.6
- **Chart.js** para gráficos
- **DataTables** para tablas interactivas

### Librerías Adicionales
- **ReportLab** para generación de PDF
- **OpenPyXL** para exportación a Excel
- **python-dotenv** para variables de entorno

---

## 🚀 Instalación y Configuración

### 1. **Clonar/Descargar el Proyecto**

```bash
cd D:\Apps\EDM04
```

### 2. **Crear Entorno Virtual**

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. **Instalar Dependencias**

```bash
pip install -r requirements.txt
```

### 4. **Configurar Base de Datos**

#### Opción A: MySQL

```bash
# Crear base de datos
mysql -u root -p

# En la consola MySQL:
CREATE DATABASE frutos_oro_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Cargar esquema inicial
mysql -u root -p frutos_oro_db < database/schema.sql
```

#### Opción B: PostgreSQL

```bash
# Crear base de datos
createdb -U postgres frutos_oro_db

# Cargar esquema
psql -U postgres -d frutos_oro_db -f database/schema.sql
```

### 5. **Configurar Variables de Entorno**

Copiar `.env.example` a `.env` y configurar:

```bash
cp .env.example .env
```

Editar `.env`:

```env
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-muy-segura

# Para MySQL:
DEV_DATABASE_URL=mysql+pymysql://root:password@localhost/frutos_oro_db

# Para PostgreSQL:
# DEV_DATABASE_URL=postgresql://user:password@localhost/frutos_oro_db

# Configuración de correo
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-aplicación
```

### 6. **Ejecutar Aplicación**

```bash
python app.py
```

La aplicación se abrirá en: **http://localhost:5000**

---

## 🔐 Credenciales de Acceso

Usuario de administrador por defecto:

- **Usuario:** `admin`
- **Contraseña:** `admin123`

⚠️ **IMPORTANTE:** Cambiar la contraseña en producción

### Usuarios de Ejemplo

- **jefe_produccion** / `admin123` - Jefe de Producción
- **jefe_calidad** / `admin123` - Jefe de Calidad
- **auditor_interno** / `admin123` - Auditor Interno

---

## 📁 Estructura del Proyecto

```
D:\Apps\EDM04\
├── app/
│   ├── templates/
│   │   ├── base.html              # Plantilla base
│   │   ├── auth/
│   │   │   └── login.html
│   │   ├── dashboard/
│   │   │   └── index.html
│   │   ├── certifications/
│   │   │   ├── list.html
│   │   │   ├── new.html
│   │   │   └── edit.html
│   │   ├── audits/
│   │   │   ├── list.html
│   │   │   ├── new.html
│   │   │   └── view.html
│   │   ├── policies/
│   │   ├── reports/
│   │   ├── admin/
│   │   └── errors/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── img/
│   ├── models.py                  # Modelos SQLAlchemy
│   ├── routes.py                  # Rutas de la aplicación
│   ├── utils.py                   # Funciones utilitarias
│   └── __init__.py                # Factory de aplicación Flask
├── database/
│   └── schema.sql                 # Script SQL inicial
├── uploads/                       # Carpeta para documentos subidos
├── app.py                         # Punto de entrada
├── config.py                      # Configuración
├── requirements.txt               # Dependencias
├── .env.example                   # Variables de entorno
└── README.md                      # Este archivo
```

---

## 🔑 Roles de Usuario

### 1. **Administrador**
- Acceso completo al sistema
- Crear/editar/eliminar usuarios
- Gestionar certificaciones, auditorías y políticas
- Ver registros de auditoría del sistema

### 2. **Jefe de Unidad**
- Gestionar certificaciones de su área
- Confirmar políticas
- Ver reportes de su unidad
- Programar auditorías

### 3. **Auditor**
- Crear y ejecutar auditorías
- Registrar hallazgos
- Ver reportes de cumplimiento
- Acceso de lectura a certificaciones

### 4. **Usuario**
- Acceso limitado
- Confirmar políticas
- Ver información relevante

---

## 📊 Dashboards y Reportes

### Dashboard Principal
- Resumen de certificaciones (vigentes, próximas a vencer, vencidas)
- Estado de auditorías
- Alertas del sistema
- Gráficos interactivos
- Indicadores clave de desempeño

### Reportes Disponibles
- **Certificaciones:** Listado con estado y vencimiento
- **Auditorías:** Resultados, hallazgos, cumplimiento
- **Políticas:** Confirmaciones por usuario y área
- **Exportación:** PDF y Excel

---

## 🔔 Sistema de Alertas

### Alertas Automáticas
- **60 días antes:** Alerta informativa
- **30 días antes:** Alerta de advertencia
- **15 días antes:** Alerta crítica

### Canales de Notificación
- Panel del sistema
- Correo electrónico
- Registro de auditoría

---

## 🛡️ Seguridad

### Medidas Implementadas
- Autenticación con contraseña hasheada (Werkzeug)
- Control de sesión
- Protección CSRF en formularios
- Validación de entrada
- SQL Injection prevention (SQLAlchemy ORM)
- Rate limiting recomendado para producción
- HTTPS recomendado en producción

### Recomendaciones para Producción
1. Cambiar `SECRET_KEY` a valor único y fuerte
2. Usar HTTPS
3. Configurar base de datos con usuario dedicado
4. Implementar 2FA
5. Hacer backup regular de la base de datos
6. Monitorear registros de auditoría

---

## 📧 Configuración de Correo

### Gmail SMTP
1. Habilitar "Acceso de aplicaciones menos seguras" O usar "Contraseña de aplicación"
2. Configurar en `.env`:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-aplicación
```

### Otro Servidor SMTP
Configurar según el proveedor (por ej: Office365, SendGrid, etc.)

---

## 🐛 Solución de Problemas

### Error de Conexión a Base de Datos
- Verificar que MySQL/PostgreSQL esté ejecutándose
- Verificar credenciales en `.env`
- Verificar nombre de base de datos

### Archivos de carga no se guardan
- Verificar permisos en carpeta `uploads/`
- Verificar tamaño máximo de archivo

### Alertas de correo no se envían
- Verificar configuración SMTP en `.env`
- Verificar que la cuenta de correo permita aplicaciones externas
- Revisar logs de la aplicación

---

## 📞 Soporte y Documentación

### API Endpoints Principales

#### Autenticación
- `POST /auth/login` - Iniciar sesión
- `GET /auth/logout` - Cerrar sesión

#### Certificaciones
- `GET /certifications/` - Listar
- `POST /certifications/new` - Crear
- `POST /certifications/<id>/edit` - Editar
- `POST /certifications/<id>/delete` - Eliminar

#### Auditorías
- `GET /audits/` - Listar
- `POST /audits/new` - Crear
- `GET /audits/<id>/view` - Ver detalles

#### Reportes
- `GET /reports/` - Panel de reportes
- `GET /reports/certifications` - Reporte de certificaciones
- `GET /reports/audits` - Reporte de auditorías

---

## 🔄 Actualización

Para actualizar el sistema:

```bash
# Descargar nuevos cambios
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Migrar base de datos si es necesario
# (Implementar migraciones con Alembic si es necesario)
```

---

## 📝 Licencia

© 2025 Agroindustria Frutos de Oro S.A.C.

---

## 👥 Contribuidores

- Equipo de Desarrollo

---

## 📅 Historial de Cambios

### Versión 1.0.0 (Inicial)
- Sistema de gestión de certificaciones
- Módulo de auditorías
- Confirmación de políticas
- Dashboard y reportes
- Sistema de alertas

---

## ✅ Checklist de Verificación

- [ ] Base de datos creada y poblada
- [ ] Variables de entorno configuradas
- [ ] Dependencias instaladas
- [ ] Aplicación ejecutándose en localhost:5000
- [ ] Credenciales de admin funcionan
- [ ] Carpeta de uploads tiene permisos de escritura
- [ ] Configuración de correo (si es necesario)
- [ ] Certificados HTTPS (para producción)

---

**¡Gracias por usar nuestro sistema!** 🍓
