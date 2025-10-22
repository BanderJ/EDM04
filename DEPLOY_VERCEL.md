# 🚀 Guía de Deploy en Vercel

## 📋 Requisitos Previos

1. **Cuenta en Vercel**: https://vercel.com/signup
2. **Base de datos MySQL en la nube** (una de estas opciones):
   - [PlanetScale](https://planetscale.com/) (Recomendado - Free tier generoso)
   - [Railway](https://railway.app/)
   - [Clever Cloud](https://www.clever-cloud.com/)
   - AWS RDS, Google Cloud SQL, Azure Database

---

## 🗄️ PASO 1: Configurar Base de Datos en la Nube

### Opción A: PlanetScale (Recomendado)

1. Crear cuenta en https://planetscale.com/
2. Crear nueva base de datos
3. Obtener la **Connection String**:
   ```
   mysql://usuario:password@host.connect.psdb.cloud/nombre_db?sslaccept=strict
   ```
4. Ejecutar el schema:
   ```bash
   mysql -h host.connect.psdb.cloud -u usuario -p nombre_db < database/schema.sql
   ```

### Opción B: Railway

1. Crear cuenta en https://railway.app/
2. New Project → Provision MySQL
3. Copiar las credenciales de conexión
4. Usar los datos para configurar las variables de entorno

---

## 🔧 PASO 2: Preparar el Proyecto

### 1. Instalar Vercel CLI (opcional pero recomendado)
```bash
npm install -g vercel
```

### 2. Verificar archivos creados
Asegúrate de tener estos archivos:
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `api/index.py` - Punto de entrada serverless
- ✅ `.vercelignore` - Archivos a ignorar en deploy
- ✅ `requirements.txt` - Dependencias Python

---

## 🌐 PASO 3: Deploy en Vercel

### Método A: Deploy desde GitHub (Recomendado)

1. **Subir código a GitHub**:
   ```bash
   git add .
   git commit -m "Preparado para deploy en Vercel"
   git push origin main
   ```

2. **Conectar con Vercel**:
   - Ir a https://vercel.com/new
   - Importar tu repositorio de GitHub
   - Vercel detectará automáticamente que es un proyecto Python/Flask

3. **Configurar Variables de Entorno**:
   En Vercel Dashboard → Settings → Environment Variables, agregar:

   ```
   # Base de Datos (Usar tu MySQL en la nube)
   DB_HOST=tu-host.connect.psdb.cloud
   DB_PORT=3306
   DB_NAME=nombre_base_datos
   DB_USER=tu_usuario
   DB_PASSWORD=tu_password_seguro

   # Flask
   FLASK_ENV=production
   SECRET_KEY=genera-una-clave-super-segura-aqui-min-32-caracteres
   
   # Seguridad
   SESSION_COOKIE_SECURE=true
   SESSION_COOKIE_HTTPONLY=true
   SESSION_COOKIE_SAMESITE=Lax
   
   # Opcional: Email (si usas notificaciones)
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=tu_email@gmail.com
   MAIL_PASSWORD=tu_app_password
   ```

4. **Deploy**:
   - Click en "Deploy"
   - Esperar 2-3 minutos
   - ¡Listo! Tu app estará en `https://tu-proyecto.vercel.app`

### Método B: Deploy desde CLI

```bash
# 1. Login en Vercel
vercel login

# 2. Deploy (primera vez)
vercel

# 3. Configurar variables de entorno
vercel env add DB_HOST
vercel env add DB_PORT
vercel env add DB_NAME
vercel env add DB_USER
vercel env add DB_PASSWORD
vercel env add SECRET_KEY

# 4. Deploy a producción
vercel --prod
```

---

## ⚙️ PASO 4: Configuración Post-Deploy

### 1. Crear Usuario Administrador

Opción A - Desde tu computadora local:
```bash
# Conectar a la base de datos en la nube
mysql -h tu-host.connect.psdb.cloud -u usuario -p

# Insertar usuario admin
USE nombre_base_datos;

INSERT INTO user (username, email, password_hash, full_name, role, is_active, created_at)
VALUES (
    'admin',
    'admin@frutosdeoro.com',
    'pbkdf2:sha256:600000$...',  -- Genera el hash en Python (ver abajo)
    'Administrador Sistema',
    'admin',
    1,
    NOW()
);
```

**Generar hash de password**:
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash('TuPasswordSeguro123!'))
```

Opción B - Usar script de inicialización:
```bash
# Modificar init.py para usar DB en la nube
python init.py
```

### 2. Verificar el Deploy

Visitar: `https://tu-proyecto.vercel.app`
- ✅ Debe cargar la página de login
- ✅ Probar login con usuario creado
- ✅ Verificar que carga el dashboard

---

## 📦 Archivos de Uploads (Certificados PDF)

⚠️ **IMPORTANTE**: Vercel es serverless y **no persiste archivos**.

### Solución: Usar almacenamiento externo

**Opción 1: AWS S3**
- Crear bucket en AWS S3
- Configurar `boto3` en Python
- Modificar rutas de upload en `app/routes.py`

**Opción 2: Cloudinary**
- Gratis hasta 25GB
- Fácil integración con Python
- Soporta PDFs y archivos

**Opción 3: Vercel Blob Storage**
- Integración nativa con Vercel
- Instalar: `pip install vercel-blob`
- Configurar en el código

---

## 🔒 Seguridad en Producción

### Variables de Entorno Críticas

```bash
# Generar SECRET_KEY segura (en Python)
python -c "import secrets; print(secrets.token_hex(32))"

# Resultado ejemplo:
# a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456
```

### Configuración HTTPS

Vercel proporciona **HTTPS automático** con certificados SSL gratuitos.

### Cookies Seguras

Ya configuradas en las variables de entorno:
```
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
```

---

## 🐛 Troubleshooting

### Error: "No module named 'app'"
**Solución**: Verifica que `api/index.py` tenga el `sys.path.insert()`

### Error: "Can't connect to MySQL server"
**Solución**: 
- Verificar que las variables de entorno estén configuradas en Vercel
- Probar conexión desde local con las mismas credenciales

### Error: "500 Internal Server Error"
**Solución**: Ver logs en Vercel Dashboard → Deployments → View Function Logs

### Páginas muy lentas
**Solución**: 
- Vercel serverless tiene "cold start" (primer request lento)
- Considerar usar Vercel Edge Functions para rutas estáticas
- Optimizar queries SQL con índices

---

## 📊 Monitoreo

### Ver Logs en Tiempo Real
```bash
vercel logs --follow
```

### Dashboard de Vercel
- Analytics: Visitas, performance
- Logs: Errores y warnings
- Deployments: Historial de versiones

---

## 🔄 Actualizaciones Futuras

### Deploy automático con Git
Una vez conectado a GitHub:
1. Hacer cambios en el código
2. `git push origin main`
3. Vercel detecta y despliega automáticamente
4. Preview en: `https://tu-proyecto-git-branch.vercel.app`
5. Producción en: `https://tu-proyecto.vercel.app`

---

## 💡 Recomendaciones Finales

1. ✅ **Usar base de datos en la nube** (no SQLite en Vercel)
2. ✅ **Configurar almacenamiento externo** para uploads
3. ✅ **Monitorear logs** regularmente
4. ✅ **Backup de base de datos** semanal
5. ✅ **Variables de entorno** nunca en el código
6. ✅ **HTTPS siempre activo** (gratis en Vercel)

---

## 📞 Soporte

- **Vercel Docs**: https://vercel.com/docs
- **Flask on Vercel**: https://vercel.com/guides/using-flask-with-vercel
- **PlanetScale Docs**: https://planetscale.com/docs

---

## 🎉 ¡Deploy Exitoso!

Tu aplicación **Frutos de Oro - Sistema de Gestión de Cumplimiento Normativo** ahora está en producción en Vercel.

URL: `https://tu-proyecto.vercel.app`

**Recuerda**:
- Configurar base de datos en la nube
- Agregar todas las variables de entorno
- Crear usuario administrador inicial
- Configurar almacenamiento para PDFs

¡Felicidades! 🚀
