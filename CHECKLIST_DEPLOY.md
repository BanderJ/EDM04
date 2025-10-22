# ✅ CHECKLIST: DEPLOY A VERCEL

## 📋 ANTES DE EMPEZAR

### 1. Base de Datos en la Nube
- [ ] Cuenta creada en PlanetScale (o Railway/AWS RDS)
- [ ] Base de datos MySQL creada
- [ ] Connection string obtenida
- [ ] Schema SQL ejecutado (`database/schema.sql`)
- [ ] Conexión probada desde local

### 2. Cuenta y Código
- [ ] Cuenta en Vercel creada (vercel.com)
- [ ] Código subido a GitHub
- [ ] Repository público o privado accesible

---

## 🔧 ARCHIVOS NECESARIOS (Ya Creados)

- [x] `vercel.json` - Configuración de Vercel
- [x] `api/index.py` - Punto de entrada serverless
- [x] `.vercelignore` - Archivos a ignorar en deploy
- [x] `requirements.txt` - Dependencias Python
- [x] `config.py` - Configuración para producción
- [x] `DEPLOY_RAPIDO.md` - Guía rápida
- [x] `DEPLOY_VERCEL.md` - Guía completa
- [x] `NOTAS_VERCEL.md` - Notas importantes

---

## 🚀 PROCESO DE DEPLOY

### PASO 1: Preparar Variables de Entorno
Tener lista esta información:

```bash
# Base de Datos (de PlanetScale/Railway)
DB_HOST=___________________.connect.psdb.cloud
DB_PORT=3306
DB_NAME=frutos_oro_db
DB_USER=___________________
DB_PASSWORD=___________________

# Flask
FLASK_ENV=production
SECRET_KEY=___________________ # Generar con: python -c "import secrets; print(secrets.token_hex(32))"

# Seguridad (Opcional)
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax
```

**✏️ Completar los espacios en blanco arriba antes de continuar**

---

### PASO 2: Subir a GitHub
```bash
git add .
git commit -m "Deploy: Configuración para Vercel"
git push origin main
```

- [ ] Código subido exitosamente
- [ ] Sin errores en el push

---

### PASO 3: Importar en Vercel

1. Ir a: https://vercel.com/new
2. Click "Import Git Repository"
3. Seleccionar repositorio: `EDM04`
4. Framework Preset: Vercel lo detecta automáticamente
5. **NO hacer click en Deploy todavía**

- [ ] Repositorio importado
- [ ] Proyecto detectado como Python/Flask

---

### PASO 4: Configurar Variables de Entorno

En la página de configuración de Vercel:

1. Expandir sección "Environment Variables"
2. Agregar **UNA POR UNA** las variables de arriba:
   - [ ] `DB_HOST`
   - [ ] `DB_PORT`
   - [ ] `DB_NAME`
   - [ ] `DB_USER`
   - [ ] `DB_PASSWORD`
   - [ ] `FLASK_ENV`
   - [ ] `SECRET_KEY`
   - [ ] (Opcional) Variables de seguridad

3. Verificar que **todas** estén agregadas

**⚠️ IMPORTANTE**: 
- Environment: Seleccionar "Production, Preview, and Development"
- Sin comillas en los valores
- Sin espacios al inicio/final

---

### PASO 5: Deploy
- [ ] Click en botón **"Deploy"**
- [ ] Esperar 2-3 minutos
- [ ] Deploy exitoso (checkmark verde ✅)
- [ ] URL generada: `https://_________________.vercel.app`

---

### PASO 6: Inicializar Base de Datos

#### Opción A: Desde PlanetScale Console
1. Ir a: https://app.planetscale.com
2. Seleccionar tu base de datos
3. Tab "Console"
4. Copiar y pegar contenido de `database/schema.sql`
5. Click "Execute"

- [ ] Schema ejecutado sin errores
- [ ] Tablas creadas

#### Opción B: Desde MySQL Workbench
```bash
# Conectar a base de datos en la nube
Host: tu-host.connect.psdb.cloud
Port: 3306
User: tu_usuario
Password: tu_password

# Ejecutar schema.sql
File → Run SQL Script → Seleccionar database/schema.sql
```

- [ ] Conectado exitosamente
- [ ] Schema ejecutado
- [ ] Tablas verificadas

---

### PASO 7: Crear Usuario Administrador

#### Método SQL Directo

En la consola de tu base de datos:

```sql
USE frutos_oro_db;

-- Generar hash de password primero en Python:
-- python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('TuPassword123'))"

INSERT INTO user (username, email, password_hash, full_name, role, is_active, created_at)
VALUES (
    'admin',
    'admin@frutosdeoro.com',
    'TU_PASSWORD_HASH_AQUI',
    'Administrador Sistema',
    'admin',
    1,
    NOW()
);
```

- [ ] Hash de password generado
- [ ] Usuario insertado
- [ ] Insert exitoso

---

### PASO 8: Verificar Deploy

1. Abrir URL de Vercel: `https://tu-proyecto.vercel.app`
2. Debe cargar la página de login
3. Probar login con usuario creado
4. Explorar módulos

**Checklist de verificación**:
- [ ] Página de login carga
- [ ] Login funciona
- [ ] Dashboard muestra datos
- [ ] No hay errores 500
- [ ] CSS y JavaScript cargan correctamente

---

## 🐛 TROUBLESHOOTING

### Si hay errores, verificar:

#### Error: "Application Error"
```bash
# Ver logs
vercel logs --follow

# O en Vercel Dashboard
Deployments → [tu deploy] → View Function Logs
```
- [ ] Logs revisados
- [ ] Error identificado

#### Error: "Can't connect to database"
- [ ] Variables de entorno correctas en Vercel
- [ ] Base de datos accesible desde internet
- [ ] Credenciales correctas (probar desde local)

#### Error: "404 Not Found"
- [ ] `vercel.json` existe en raíz
- [ ] `api/index.py` existe
- [ ] Re-deploy realizado

#### Página en blanco
- [ ] JavaScript cargando (ver consola del navegador F12)
- [ ] CSS cargando (ver Network tab)
- [ ] Rutas de archivos estáticos correctas

---

## ✅ POST-DEPLOY

### Configuraciones adicionales

- [ ] Dominio custom configurado (opcional)
  - Vercel → Settings → Domains
  - Agregar: `sistema.frutosdeoro.com`
  - Configurar DNS

- [ ] Backup de base de datos programado
  - PlanetScale: Backups automáticos
  - O: Script cron manual semanal

- [ ] Storage para PDFs configurado
  - [ ] Vercel Blob Storage, o
  - [ ] Cloudinary, o
  - [ ] AWS S3

- [ ] Monitoreo de uptime
  - [ ] UptimeRobot (gratis)
  - [ ] Pingdom
  - [ ] StatusCake

- [ ] Notificaciones configuradas
  - [ ] Vercel Deploy Notifications
  - [ ] Webhook a Slack/Discord
  - [ ] Email alerts

---

## 📝 DOCUMENTAR

### Información para el equipo

```
🌐 URL DE PRODUCCIÓN
https://_________________.vercel.app

👤 USUARIO ADMINISTRADOR
Usuario: admin
Email: admin@frutosdeoro.com
Password: [Guardar en lugar seguro]

🗄️ BASE DE DATOS
Proveedor: PlanetScale / Railway / Otro
URL Dashboard: ___________________

📦 REPOSITORIO
GitHub: https://github.com/BanderJ/EDM04

🔧 VERCEL DASHBOARD
https://vercel.com/tu-usuario/tu-proyecto
```

- [ ] Información documentada
- [ ] Compartida con el equipo
- [ ] Passwords en lugar seguro (LastPass, 1Password, etc.)

---

## 🎉 ¡DEPLOY COMPLETADO!

### Próximos pasos

1. [ ] Entrenar al equipo en el uso del sistema
2. [ ] Migrar datos existentes (si aplica)
3. [ ] Configurar backups automáticos
4. [ ] Monitorear logs las primeras semanas
5. [ ] Optimizar performance según uso real

---

## 📞 AYUDA

**Guías creadas**:
- `DEPLOY_RAPIDO.md` - Pasos rápidos (5 min)
- `DEPLOY_VERCEL.md` - Guía completa detallada
- `NOTAS_VERCEL.md` - Notas técnicas importantes

**Recursos externos**:
- Vercel Docs: https://vercel.com/docs
- Vercel Support: https://vercel.com/support
- PlanetScale Docs: https://planetscale.com/docs

---

**Fecha de deploy**: ___________________
**Deployado por**: ___________________
**Versión**: 1.0.0
**Status**: ⬜ Pendiente | ⬜ En proceso | ⬜ Completado

---

## 💾 GUARDAR ESTE CHECKLIST

Una vez completado, guardar como referencia para futuros deploys o troubleshooting.

¡Éxito! 🚀
