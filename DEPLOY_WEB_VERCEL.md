# 🌐 DEPLOY DESDE LA WEB DE VERCEL - GUÍA PASO A PASO

## 🎯 Método: Import desde GitHub en Vercel.com

**Ventajas de este método**:
- ✅ No necesitas instalar Vercel CLI
- ✅ Interface visual fácil de usar
- ✅ Deploy automático en cada push
- ✅ Dominio incluido: `edm04.vercel.app`

**Tiempo estimado**: 15-20 minutos

---

## 📋 REQUISITOS PREVIOS

### 1. Cuentas Necesarias

- [ ] **GitHub** - Para alojar tu código
  - ➡️ https://github.com/signup

- [ ] **Vercel** - Para hacer el deploy
  - ➡️ https://vercel.com/signup
  - 💡 Tip: Registrate con tu cuenta de GitHub (más fácil)

- [ ] **PlanetScale** - Para base de datos MySQL
  - ➡️ https://planetscale.com/
  - 💡 Plan gratis: 5GB storage, suficiente para empezar

### 2. Código en GitHub

```bash
# Si aún no has subido el código
cd d:\Apps\EDM04
git add .
git commit -m "Preparado para deploy en Vercel"
git push origin main
```

✅ **Verificar**: Tu repositorio debe estar en: `https://github.com/BanderJ/EDM04`

---

## 🗄️ PASO 1: CREAR BASE DE DATOS EN PLANETSCALE (5 min)

### 1.1 Crear Cuenta

1. Ir a: https://planetscale.com/
2. Click en **"Sign up"**
3. Registrarse con GitHub (recomendado)
4. Verificar email

### 1.2 Crear Base de Datos

1. Click en **"New database"**
2. **Name**: `frutos-oro-db` (o el nombre que prefieras)
3. **Region**: Seleccionar región más cercana (ej: `US East`)
4. Click en **"Create database"**
5. Esperar ~30 segundos mientras se crea

### 1.3 Obtener Credenciales de Conexión

1. En tu base de datos, ir a **"Connect"**
2. Seleccionar: **"Connect with: Python"**
3. Framework: **"Django/Flask"**
4. Copiar los datos que aparecen:

```
Host: xxxxxxxxxxxx.connect.psdb.cloud
Username: xxxxxxxxxxxxx
Password: xxxxxxxxxxxxx
Database: frutos-oro-db
Port: 3306
```

⚠️ **IMPORTANTE**: Guarda estos datos en un archivo temporal, los necesitarás en el Paso 3.

### 1.4 Ejecutar Schema SQL

**Opción A - Desde PlanetScale Console (Recomendado)**:

1. En tu base de datos, ir a **"Console"** (pestaña arriba)
2. Abrir el archivo `d:\Apps\EDM04\database\schema.sql` en tu editor
3. Copiar **TODO** el contenido del archivo
4. Pegar en el console de PlanetScale
5. Click en **"Execute"** o presionar `Ctrl + Enter`
6. Verificar: Debe decir "Query executed successfully"

**Opción B - Desde MySQL Workbench**:

1. Abrir MySQL Workbench
2. New Connection:
   - Connection Name: `PlanetScale Frutos Oro`
   - Hostname: `xxxxxxxxxxxx.connect.psdb.cloud`
   - Port: `3306`
   - Username: `[tu username]`
   - Password: `[tu password]`
   - Default Schema: `frutos-oro-db`
3. Click **"Test Connection"** → Debe decir "Successfully connected"
4. Connect
5. File → Run SQL Script → Seleccionar `d:\Apps\EDM04\database\schema.sql`
6. Click **"Run"**

✅ **Verificar**: Ir a Console y ejecutar:
```sql
SHOW TABLES;
```
Debe mostrar: `user`, `certification`, `audit`, `policy`, etc.

---

## 🚀 PASO 2: IMPORTAR PROYECTO EN VERCEL (3 min)

### 2.1 Acceder a Vercel

1. Ir a: https://vercel.com/
2. **Login** (con tu cuenta de GitHub si la creaste así)
3. Te llevará al Dashboard

### 2.2 Importar Repositorio desde GitHub

1. Click en **"Add New..."** (botón arriba a la derecha)
2. Seleccionar **"Project"**
3. Si es tu primera vez, te pedirá conectar con GitHub:
   - Click en **"Continue with GitHub"**
   - Autorizar a Vercel a acceder a tus repositorios
   - Seleccionar si quieres dar acceso a todos o solo a EDM04

4. Buscar tu repositorio: **`EDM04`**
5. Click en **"Import"** al lado del repositorio

### 2.3 Configurar Proyecto

Vercel detectará automáticamente que es un proyecto Python/Flask.

**En la pantalla de configuración**:

1. **Project Name**: 
   - Cambiar a: `edm04` o `edm-04` (lo que prefieras)
   - Esto será tu dominio: `edm04.vercel.app` o `edm-04.vercel.app`

2. **Framework Preset**: 
   - Debe decir: `Other` o detectar Python automáticamente
   - ✅ Si pregunta por framework, seleccionar "Other"
   - ✅ NO seleccionar "Create React App" o similar

3. **Root Directory**: 
   - Dejar: `./` (raíz del proyecto)
   - ✅ NO cambiar a src/ u otra carpeta

4. **Build and Output Settings**:
   - ✅ Dejar todo por defecto
   - Vercel usará automáticamente `vercel.json` para la configuración
   
5. **Build Command**: 
   - Dejar vacío o: `pip install -r requirements.txt`
   
6. **Output Directory**:
   - Dejar vacío (Vercel lo maneja automáticamente)

⚠️ **IMPORTANTE**: 
- **NO cambiar Root Directory a "src"** - Este es un proyecto Flask, no HTML estático
- Vercel usará `api/index.py` como punto de entrada (configurado en `vercel.json`)
- **NO hacer click en "Deploy" todavía**

---

## ⚙️ PASO 3: CONFIGURAR VARIABLES DE ENTORNO (5 min)

**Antes de deployar**, debes configurar las variables de entorno.

### 3.1 Expandir Sección "Environment Variables"

En la misma pantalla de configuración del proyecto:
1. Buscar la sección **"Environment Variables"**
2. Click para expandirla

### 3.2 Agregar Variables UNA POR UNA

**⚠️ IMPORTANTE**: 
- Para cada variable: Agregar → Name → Value → Add
- Environment: Dejar en **"All"** (Production, Preview, and Development)
- NO usar comillas en los valores

#### Variable 1: DB_HOST
```
Name:  DB_HOST
Value: xxxxxxxxxxxx.connect.psdb.cloud
       ☝️ Tu host de PlanetScale (del Paso 1.3)
```
Click **"Add"**

#### Variable 2: DB_PORT
```
Name:  DB_PORT
Value: 3306
```
Click **"Add"**

#### Variable 3: DB_NAME
```
Name:  DB_NAME
Value: frutos-oro-db
       ☝️ El nombre de tu base de datos en PlanetScale
```
Click **"Add"**

#### Variable 4: DB_USER
```
Name:  DB_USER
Value: xxxxxxxxxxxxx
       ☝️ Tu username de PlanetScale (del Paso 1.3)
```
Click **"Add"**

#### Variable 5: DB_PASSWORD
```
Name:  DB_PASSWORD
Value: xxxxxxxxxxxxx
       ☝️ Tu password de PlanetScale (del Paso 1.3)
```
Click **"Add"**

#### Variable 6: FLASK_ENV
```
Name:  FLASK_ENV
Value: production
```
Click **"Add"**

#### Variable 7: SECRET_KEY

**Primero, generar una clave segura**:

En tu terminal (PowerShell):
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copiar el resultado (será algo como: `a1b2c3d4e5f6...`)

```
Name:  SECRET_KEY
Value: [pegar el resultado del comando anterior]
```
Click **"Add"**

### 3.3 Verificar Variables

Asegúrate de haber agregado **TODAS** estas 7 variables:
- ☑️ DB_HOST
- ☑️ DB_PORT
- ☑️ DB_NAME
- ☑️ DB_USER
- ☑️ DB_PASSWORD
- ☑️ FLASK_ENV
- ☑️ SECRET_KEY

---

## 🎉 PASO 4: DEPLOY (2 min)

### 4.1 Iniciar Deploy

1. Scroll hasta abajo
2. Click en el botón grande **"Deploy"**
3. Vercel comenzará a:
   - Clonar tu repositorio
   - Detectar Python
   - Instalar dependencias de `requirements.txt`
   - Construir la aplicación
   - Deployar

### 4.2 Esperar

- ⏱️ **Tiempo estimado**: 2-3 minutos
- Verás un log en tiempo real del proceso
- Al final debe aparecer: **"🎉 Congratulations! Your project is live!"**

### 4.3 Obtener URL

Una vez completado:
1. Verás tu URL de producción: **`https://edm04.vercel.app`**
2. Click en **"Visit"** o copiar la URL

⚠️ **IMPORTANTE**: Si abres la URL ahora, verás la página de login pero **NO funcionará** todavía porque falta crear el usuario administrador.

---

## 👤 PASO 5: CREAR USUARIO ADMINISTRADOR (5 min)

### Opción A: Usando PlanetScale Console (Más Fácil)

#### 5.1 Generar Hash de Password

En tu terminal (PowerShell):
```powershell
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('Admin123!@#'))"
```

💡 Cambiar `Admin123!@#` por la contraseña que quieras usar.

Copiar el resultado completo (será algo como: `pbkdf2:sha256:600000$...`)

#### 5.2 Insertar Usuario en PlanetScale

1. Ir a tu base de datos en PlanetScale
2. Tab **"Console"**
3. Copiar y pegar este SQL (reemplazar el password_hash):

```sql
-- Usar la base de datos
USE frutos_oro_db;

-- Insertar usuario administrador
INSERT INTO user (username, email, password_hash, full_name, role, is_active, created_at)
VALUES (
    'admin',
    'admin@frutosdeoro.com',
    'pbkdf2:sha256:600000$AQUI_TU_HASH_GENERADO_ARRIBA',
    'Administrador Sistema',
    'admin',
    1,
    NOW()
);
```

4. Reemplazar `AQUI_TU_HASH_GENERADO_ARRIBA` con el hash que generaste
5. Click **"Execute"** o `Ctrl + Enter`
6. Debe decir: "Query executed successfully. 1 row affected"

### Opción B: Usando MySQL Workbench

1. Conectar a PlanetScale (como en Paso 1.4 Opción B)
2. Ejecutar el mismo SQL de arriba
3. Verificar que se insertó:
```sql
SELECT username, email, role FROM user WHERE role = 'admin';
```

✅ **Verificar**: Debe mostrar tu usuario admin.

---

## ✅ PASO 6: VERIFICAR QUE TODO FUNCIONE (3 min)

### 6.1 Acceder a la Aplicación

1. Ir a tu URL: **`https://edm04.vercel.app`**
   (o el nombre que hayas elegido)

2. Debe cargar la página de **login**

### 6.2 Probar Login

Credenciales:
```
Usuario: admin
Contraseña: [la que usaste al generar el hash]
```

Si usaste el ejemplo: `Admin123!@#`

### 6.3 Explorar la Aplicación

Una vez dentro:
- ✅ Dashboard debe cargar
- ✅ Módulos deben ser accesibles
- ✅ No debe haber errores 500

### 6.4 Verificar en Vercel

1. Ir a: https://vercel.com/dashboard
2. Click en tu proyecto: **edm04**
3. Ver:
   - ✅ Status: **"Ready"** (verde)
   - ✅ Last deployment: Successful
   - ✅ Production URL activa

---

## 🔧 PASO 7: CONFIGURACIONES POST-DEPLOY (Opcional)

### 7.1 Dominio Custom (Opcional)

Si tienes un dominio propio (ej: `sistema.frutosdeoro.com`):

1. En Vercel Dashboard → Tu proyecto
2. Tab **"Settings"**
3. Sección **"Domains"**
4. Click **"Add"**
5. Ingresar tu dominio
6. Seguir instrucciones para configurar DNS

### 7.2 Deploy Automático

Ya configurado! 🎉

Cada vez que hagas:
```bash
git push origin main
```

Vercel automáticamente:
- Detecta el push
- Hace deploy de la nueva versión
- Actualiza tu sitio en ~2 minutos

### 7.3 Ver Logs

Para ver logs de tu aplicación:

1. En Vercel Dashboard → Tu proyecto
2. Click en el último deployment (arriba)
3. Click en **"View Function Logs"**
4. Ver logs en tiempo real

---

## 🐛 TROUBLESHOOTING

### ❌ Error: "Vercel pide index.html en carpeta src"

**Causa**: Vercel está detectando el proyecto como sitio estático HTML en lugar de Python/Flask

**Solución**:
1. En Vercel Dashboard → Tu proyecto
2. Settings → General
3. **Framework Preset**: Cambiar a **"Other"**
4. **Root Directory**: Asegurar que esté en **"./"** (raíz)
5. **Build Command**: Dejar vacío o `pip install -r requirements.txt`
6. Scroll abajo → Click **"Save"**
7. Ir a Deployments → Latest → ⋮ → **"Redeploy"**

**Archivos clave que debe detectar Vercel**:
- ✅ `vercel.json` → Configura Python serverless
- ✅ `api/index.py` → Punto de entrada Flask
- ✅ `requirements.txt` → Dependencias Python

Si sigue sin funcionar:
1. Verificar que `vercel.json` esté en la raíz del proyecto
2. Verificar que `api/index.py` exista
3. Hacer redeploy forzado

### ❌ Error: "Application Error" al abrir la URL

**Causa**: Variables de entorno mal configuradas

**Solución**:
1. Vercel Dashboard → Tu proyecto
2. Settings → Environment Variables
3. Verificar que **TODAS** las variables estén correctas
4. Si falta alguna o está mal:
   - Editar variable
   - Ir a Deployments
   - Click **⋮** (3 puntos) → **"Redeploy"**

### ❌ Error: "Can't connect to database"

**Causa**: Credenciales de MySQL incorrectas o DB no accesible

**Solución**:
1. Verificar credenciales en PlanetScale Dashboard
2. Copiar nuevamente desde PlanetScale Connect
3. Actualizar variables en Vercel
4. Redeploy

### ❌ Error: "500 Internal Server Error"

**Causa**: Error en el código o falta alguna tabla en la DB

**Solución**:
1. Ver logs en Vercel Dashboard
2. Verificar que `schema.sql` se ejecutó completamente
3. En PlanetScale Console:
```sql
SHOW TABLES;
-- Debe mostrar 8 tablas
```

### ❌ Login no funciona / "Invalid credentials"

**Causa**: Usuario no existe o password hash incorrecto

**Solución**:
1. Verificar usuario en PlanetScale:
```sql
SELECT username, email, role FROM user WHERE username = 'admin';
```
2. Si no existe, crear con el SQL del Paso 5
3. Si existe pero password mal, generar nuevo hash y actualizar:
```sql
UPDATE user SET password_hash = 'NUEVO_HASH_AQUI' WHERE username = 'admin';
```

### ❌ CSS no carga / Página sin estilos

**Causa**: Archivos estáticos no se deployaron

**Solución**:
1. Verificar que `app/static/` esté en tu repo de GitHub
2. Hacer redeploy:
   - Vercel Dashboard → Deployments
   - Latest → ⋮ → Redeploy

---

## 📊 MONITOREO

### Ver Analytics

1. Vercel Dashboard → Tu proyecto
2. Tab **"Analytics"**
3. Ver:
   - Requests por día
   - Tiempo de respuesta
   - Errores
   - Tráfico por país

### Configurar Notificaciones

1. Vercel Dashboard → Tu proyecto
2. Settings → **"Notifications"**
3. Activar:
   - ☑️ Deployment failed
   - ☑️ Deployment ready
4. Agregar email o Slack webhook

---

## 🎯 RESUMEN

### Lo que hiciste:

1. ✅ Creaste base de datos MySQL en PlanetScale
2. ✅ Ejecutaste schema SQL
3. ✅ Importaste proyecto en Vercel desde GitHub
4. ✅ Configuraste 7 variables de entorno
5. ✅ Hiciste deploy
6. ✅ Creaste usuario administrador
7. ✅ Verificaste que todo funcione

### URLs Importantes:

- 🌐 **Tu aplicación**: https://edm04.vercel.app (o tu nombre)
- 🗄️ **Base de datos**: https://app.planetscale.com/
- 🚀 **Vercel Dashboard**: https://vercel.com/dashboard
- 📁 **Código GitHub**: https://github.com/BanderJ/EDM04

### Credenciales:

```
Aplicación:
- Usuario: admin
- Password: [la que configuraste]

PlanetScale:
- URL: https://app.planetscale.com/
- Database: frutos-oro-db
- User: [guardar en lugar seguro]

Vercel:
- URL: https://vercel.com/
- Deploy automático desde GitHub
```

---

## 🔄 ACTUALIZAR LA APLICACIÓN

Cuando hagas cambios en el código:

```bash
# 1. Hacer cambios en tu código local
# 2. Commit y push
git add .
git commit -m "Descripción de los cambios"
git push origin main

# 3. Vercel deploya automáticamente
# 4. Esperar 2-3 minutos
# 5. Cambios live en https://edm04.vercel.app
```

---

## 📞 SOPORTE

### Vercel
- **Docs**: https://vercel.com/docs
- **Support**: https://vercel.com/support
- **Status**: https://vercel-status.com/

### PlanetScale
- **Docs**: https://planetscale.com/docs
- **Support**: https://support.planetscale.com/

---

## 🎉 ¡FELICIDADES!

Tu aplicación **Sistema de Gestión de Cumplimiento Normativo** está ahora en producción en Vercel! 🚀🍓

**URL**: https://edm04.vercel.app

Comparte la URL con tu equipo y comienza a usar el sistema.

---

**Fecha de deploy**: _____________________
**Deployado por**: _____________________
**Versión**: 1.0.0
**Status**: ✅ EN PRODUCCIÓN

---

💡 **Tip**: Guarda este documento y las credenciales en un lugar seguro.
