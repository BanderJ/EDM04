# ⚠️ NOTAS IMPORTANTES PARA VERCEL DEPLOYMENT

## 🔒 SEGURIDAD

### Variables de Entorno CRÍTICAS

**NUNCA subir a Git**:
- ❌ `.env` (archivo con credenciales reales)
- ❌ Contraseñas en el código
- ❌ Keys de API en archivos Python

**SÍ configurar en Vercel Dashboard**:
- ✅ `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`
- ✅ `SECRET_KEY` (generar con `secrets.token_hex(32)`)
- ✅ `FLASK_ENV=production`

---

## 📦 ARCHIVOS UPLOADS (PDFs, Certificados)

### ⚠️ PROBLEMA: Vercel es Serverless

Vercel **NO persiste archivos** entre requests. Cada función serverless es efímera.

### ✅ SOLUCIONES

#### Opción 1: Vercel Blob Storage (Recomendado)
```bash
pip install vercel-blob
```

```python
from vercel_blob import upload

# En app/routes.py (modificar upload de certificados)
@certifications.route('/upload', methods=['POST'])
def upload_certificate():
    file = request.files['certificate']
    blob_url = upload(file, 'certifications/')
    # Guardar blob_url en la base de datos
```

#### Opción 2: Cloudinary (Más fácil)
```bash
pip install cloudinary
```

Configurar en Vercel:
```
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

#### Opción 3: AWS S3 (Más robusto)
```bash
pip install boto3
```

Configurar en Vercel:
```
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_BUCKET_NAME=frutos-oro-uploads
```

### 📝 Archivos a Modificar

1. **`app/routes.py`** - Rutas de upload de certificaciones
2. **`requirements.txt`** - Agregar librería de storage
3. **Vercel Environment Variables** - Agregar credenciales

---

## 🗄️ BASE DE DATOS

### ❌ NO USAR SQLite en Vercel

SQLite no funciona en entorno serverless (sin persistencia).

### ✅ USAR MySQL en la Nube

**Opciones recomendadas**:

1. **PlanetScale** (Recomendado)
   - Free tier: 5GB storage, 1B row reads/month
   - MySQL compatible
   - Sin servidor (serverless MySQL)
   - https://planetscale.com/

2. **Railway**
   - $5/mes
   - MySQL tradicional
   - Fácil setup
   - https://railway.app/

3. **AWS RDS**
   - Producción enterprise
   - Más costoso pero más robusto
   - Requiere configuración VPC

### 🔧 Configurar Connection String

En Vercel Dashboard → Environment Variables:

```bash
DB_HOST=your-host.connect.psdb.cloud
DB_PORT=3306
DB_NAME=frutos_oro_db
DB_USER=your_username
DB_PASSWORD=your_password
```

**⚠️ IMPORTANTE**: PlanetScale requiere SSL:
```python
# Ya configurado en config.py
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}?charset=utf8mb4'
```

---

## 🏗️ ESTRUCTURA DE ARCHIVOS PARA VERCEL

```
EDM04/
├── api/                    # ✅ SERVERLESS FUNCTIONS
│   └── index.py           # Punto de entrada (Vercel lo detecta)
├── app/                   # Tu aplicación Flask
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── ...
├── vercel.json            # ✅ Configuración de Vercel
├── .vercelignore          # ✅ Archivos a ignorar
├── requirements.txt       # ✅ Dependencias Python
├── .env.example           # Template de variables
└── app.py                 # Para desarrollo local
```

### ¿Por qué `api/index.py`?

Vercel detecta automáticamente archivos en `api/` como serverless functions.

- `api/index.py` → `https://tu-proyecto.vercel.app/*`
- Todas las rutas de Flask se manejan ahí

---

## ⚡ OPTIMIZACIONES

### 1. Connection Pooling

Ya configurado en `config.py`:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 5,           # Máx 5 conexiones
    'pool_recycle': 3600,     # Reciclar cada hora
    'pool_pre_ping': True,    # Verificar conexión antes de usar
    'max_overflow': 2         # Máx 2 conexiones extra
}
```

### 2. Cold Start

**Problema**: Primera request toma 3-5 segundos.

**Soluciones**:
- ✅ Usar plan Pro de Vercel (reduce cold start)
- ✅ Keep-alive ping (cron job externo)
- ✅ Optimizar imports pesados

### 3. Tamaño del Bundle

Vercel tiene límite de 250MB por función.

**Reducir tamaño**:
```bash
# En requirements.txt, solo lo necesario
# Evitar: pandas, numpy, tensorflow (muy pesados)
```

---

## 🔍 DEBUGGING EN PRODUCCIÓN

### Ver Logs en Tiempo Real

```bash
# Instalar Vercel CLI
npm install -g vercel

# Ver logs
vercel logs --follow
```

### Logs en Dashboard

Vercel Dashboard → Deployments → [tu deploy] → View Function Logs

### Errores Comunes

#### 1. "Module not found"
**Causa**: Dependencia falta en `requirements.txt`
**Solución**: Agregar en `requirements.txt` y re-deploy

#### 2. "Can't connect to database"
**Causa**: Variables de entorno mal configuradas
**Solución**: Verificar en Vercel → Settings → Environment Variables

#### 3. "500 Internal Server Error"
**Causa**: Error en el código
**Solución**: Ver logs con `vercel logs`

#### 4. "Function Timeout (10s)"
**Causa**: Query SQL muy lenta o función bloqueante
**Solución**: 
- Optimizar queries con índices
- Usar plan Pro (60s timeout)
- Hacer operaciones pesadas asíncronas

---

## 📊 MONITOREO

### Analytics de Vercel (Gratis)

- Requests por segundo
- Tiempo de respuesta
- Errores 4xx, 5xx
- Tráfico por ruta

### Logs y Alertas

Configurar en Vercel:
- Email notifications on deploy
- Webhook para Slack/Discord
- Monitor de uptime (UptimeRobot)

---

## 🔄 CI/CD AUTOMÁTICO

Una vez conectado a GitHub:

```bash
# 1. Hacer cambios localmente
git add .
git commit -m "Mejora en certificaciones"

# 2. Push a GitHub
git push origin main

# 3. Vercel detecta y despliega automáticamente
# Sin hacer nada más!

# 4. Deploy disponible en:
#    - Preview: https://edm04-git-main-tu-usuario.vercel.app
#    - Producción: https://tu-proyecto.vercel.app (después de aprobar)
```

### Branches y Previews

- `main` → Deploy a Producción
- `dev`, `feature/X` → Deploy Preview único
- Pull Requests → Preview automático

---

## 💰 COSTOS

### Plan Hobby (Gratis)
- ✅ Suficiente para desarrollo y equipos pequeños
- ✅ 100GB bandwidth
- ✅ Serverless functions
- ❌ Cold start más lento
- ❌ 10s function timeout

### Plan Pro ($20/mes)
- ✅ Cold start más rápido
- ✅ 60s function timeout
- ✅ 1TB bandwidth
- ✅ Analytics avanzados
- ✅ Mejor soporte

---

## 📞 RECURSOS

- **Vercel Docs**: https://vercel.com/docs
- **Flask on Vercel**: https://vercel.com/guides/using-flask-with-vercel
- **PlanetScale Docs**: https://planetscale.com/docs
- **Cloudinary Python**: https://cloudinary.com/documentation/python_quickstart

---

## ✅ CHECKLIST PRE-DEPLOY

Antes de hacer deploy, verificar:

- [ ] MySQL en la nube configurado y accesible
- [ ] Schema SQL ejecutado en la base de datos
- [ ] Variables de entorno listadas (DB_*, SECRET_KEY, etc.)
- [ ] `vercel.json` en la raíz del proyecto
- [ ] `api/index.py` creado
- [ ] `.vercelignore` configurado
- [ ] `requirements.txt` actualizado
- [ ] Código subido a GitHub
- [ ] Plan de storage para uploads (Vercel Blob/Cloudinary/S3)

---

## 🎯 PRÓXIMOS PASOS DESPUÉS DEL DEPLOY

1. ✅ Ejecutar `init_production.py` para crear admin
2. ✅ Probar login en la URL de Vercel
3. ✅ Configurar dominio custom (opcional)
4. ✅ Setup de backup de base de datos (semanal)
5. ✅ Configurar storage para PDFs
6. ✅ Agregar monitoreo de uptime
7. ✅ Documentar URL de producción al equipo

---

¡Éxito con tu deploy! 🚀
