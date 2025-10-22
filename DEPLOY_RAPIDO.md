# 🚀 GUÍA RÁPIDA: Deploy en Vercel en 5 Minutos

## 📋 Pre-requisitos
- [ ] Cuenta en Vercel (https://vercel.com/signup)
- [ ] MySQL en la nube configurado (PlanetScale recomendado)
- [ ] Código en GitHub

---

## ⚡ PASOS RÁPIDOS

### 1️⃣ Crear Base de Datos MySQL en PlanetScale (2 min)

```bash
# Ir a: https://planetscale.com/
# Crear cuenta gratis
# New Database → Nombre: frutos-oro-db
# Copiar Connection String
```

**Resultado**: Obtendrás algo como:
```
mysql://username:password@host.connect.psdb.cloud/frutos-oro-db
```

**Descomponer en variables**:
- `DB_HOST`: `host.connect.psdb.cloud`
- `DB_USER`: `username`
- `DB_PASSWORD`: `password`
- `DB_NAME`: `frutos-oro-db`
- `DB_PORT`: `3306`

---

### 2️⃣ Subir Código a GitHub (1 min)

```bash
git add .
git commit -m "Deploy a Vercel"
git push origin main
```

---

### 3️⃣ Importar en Vercel (2 min)

1. Ir a: https://vercel.com/new
2. Click en "Import Git Repository"
3. Seleccionar tu repositorio: `EDM04`
4. Click en "Import"

Vercel detectará automáticamente que es Python/Flask.

---

### 4️⃣ Configurar Variables de Entorno (3 min)

En la pantalla de configuración de Vercel, agregar estas variables:

**⚠️ IMPORTANTE: Agregar TODAS estas variables**

#### Base de Datos
```
DB_HOST = tu-host.connect.psdb.cloud
DB_PORT = 3306
DB_NAME = frutos-oro-db
DB_USER = tu_usuario
DB_PASSWORD = tu_password
```

#### Flask
```
FLASK_ENV = production
SECRET_KEY = [Generar una clave segura - ver abajo]
```

#### Seguridad (Opcional pero recomendado)
```
SESSION_COOKIE_SECURE = true
SESSION_COOKIE_HTTPONLY = true
SESSION_COOKIE_SAMESITE = Lax
```

**🔐 Generar SECRET_KEY segura**:
```bash
# En tu terminal local
python -c "import secrets; print(secrets.token_hex(32))"
```
Copiar el resultado y usarlo como `SECRET_KEY`.

---

### 5️⃣ Deploy (1 min)

1. Click en **"Deploy"**
2. Esperar 2-3 minutos
3. Vercel te dará una URL: `https://tu-proyecto.vercel.app`

---

### 6️⃣ Inicializar Base de Datos (2 min)

**Opción A - Desde MySQL Workbench o terminal**:

```bash
# Conectar a tu base de datos en PlanetScale
mysql -h tu-host.connect.psdb.cloud -u tu_usuario -p

# Ejecutar el schema
source database/schema.sql

# O copiar y pegar el contenido de schema.sql
```

**Opción B - Desde PlanetScale Dashboard**:
1. Ir a tu base de datos en PlanetScale
2. Console → Query
3. Copiar y pegar contenido de `database/schema.sql`
4. Ejecutar

---

### 7️⃣ Crear Usuario Administrador (1 min)

**Opción A - SQL Directo**:

```sql
-- Conectar a la base de datos en la nube
USE frutos_oro_db;

-- Crear usuario admin
INSERT INTO user (username, email, password_hash, full_name, role, is_active, created_at)
VALUES (
    'admin',
    'admin@frutosdeoro.com',
    'pbkdf2:sha256:600000$7ZpwRz8kkSEhpHN7$e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    'Administrador Sistema',
    'admin',
    1,
    NOW()
);
```

**Contraseña del ejemplo anterior**: `admin123`

**Opción B - Generar tu propio hash**:

```python
# En tu terminal local
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('TuPasswordSeguro123'))"
```

---

## ✅ VERIFICAR

1. Abrir: `https://tu-proyecto.vercel.app`
2. Debe aparecer la página de login
3. Ingresar con el usuario administrador creado
4. Explorar el sistema

---

## 🐛 Si algo falla

### Error: "Can't connect to database"
```bash
# Verificar en Vercel Dashboard → Settings → Environment Variables
# Que todas las variables DB_* estén configuradas
```

### Error: "500 Internal Server Error"
```bash
# Ver logs:
vercel logs --follow

# O en Vercel Dashboard → Deployments → [tu deploy] → View Function Logs
```

### No carga ninguna página
```bash
# Verificar que vercel.json esté en la raíz del proyecto
# Verificar que api/index.py exista
```

---

## 📌 URLs Importantes

- **Tu aplicación**: `https://tu-proyecto.vercel.app`
- **Vercel Dashboard**: https://vercel.com/dashboard
- **PlanetScale Dashboard**: https://app.planetscale.com/
- **Logs en tiempo real**: `vercel logs --follow`

---

## 🎯 Resumen de Archivos Creados

✅ `vercel.json` - Configuración de Vercel
✅ `api/index.py` - Punto de entrada para Vercel
✅ `.vercelignore` - Archivos a ignorar
✅ `DEPLOY_VERCEL.md` - Guía completa
✅ `DEPLOY_RAPIDO.md` - Esta guía rápida

---

## 💡 Consejos

1. **Primer deploy siempre toma más tiempo** (cold start)
2. **Variables de entorno** se pueden editar después en Vercel Dashboard
3. **Logs** son tu mejor amigo para debugging
4. **Auto-deploy**: Cada push a `main` actualiza automáticamente

---

## ✨ ¡Listo!

Tu aplicación **Frutos de Oro** ahora está en producción en Vercel 🚀

**Tiempo total estimado**: ~15 minutos

---

## 📞 Ayuda Adicional

- **Documentación completa**: Ver `DEPLOY_VERCEL.md`
- **Vercel Docs**: https://vercel.com/docs
- **Flask on Vercel**: https://vercel.com/guides/using-flask-with-vercel
