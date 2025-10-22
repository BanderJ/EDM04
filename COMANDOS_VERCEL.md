# 🛠️ COMANDOS ÚTILES PARA VERCEL

## 📦 INSTALACIÓN VERCEL CLI

```bash
# Instalar Vercel CLI globalmente
npm install -g vercel

# Verificar instalación
vercel --version
```

---

## 🚀 DEPLOY BÁSICO

```bash
# Login en Vercel (primera vez)
vercel login

# Deploy a preview (ambiente de prueba)
vercel

# Deploy a producción
vercel --prod

# Deploy forzando rebuild
vercel --prod --force
```

---

## 📊 LOGS Y DEBUGGING

```bash
# Ver logs en tiempo real
vercel logs --follow

# Ver logs de un proyecto específico
vercel logs mi-proyecto --follow

# Ver logs de producción
vercel logs --prod

# Ver últimos 100 logs
vercel logs --limit 100

# Ver logs con filtro
vercel logs --grep "error"
```

---

## ⚙️ VARIABLES DE ENTORNO

```bash
# Listar variables de entorno
vercel env ls

# Agregar variable de entorno
vercel env add DB_HOST

# Agregar variable para producción solamente
vercel env add SECRET_KEY production

# Eliminar variable
vercel env rm DB_HOST

# Actualizar variable
vercel env rm DB_HOST
vercel env add DB_HOST

# Importar desde archivo .env
vercel env pull .env.local
```

---

## 🔍 INFORMACIÓN DEL PROYECTO

```bash
# Ver información del proyecto actual
vercel inspect

# Listar todos tus proyectos
vercel list

# Ver dominios configurados
vercel domains ls

# Ver deployments recientes
vercel ls
```

---

## 🌐 DOMINIOS

```bash
# Listar dominios
vercel domains ls

# Agregar dominio custom
vercel domains add sistema.frutosdeoro.com

# Verificar dominio
vercel domains verify sistema.frutosdeoro.com

# Remover dominio
vercel domains rm sistema.frutosdeoro.com
```

---

## 🔄 GESTIÓN DE DEPLOYMENTS

```bash
# Ver historial de deployments
vercel list

# Ver deployment específico
vercel inspect [deployment-url]

# Eliminar deployment
vercel remove [deployment-url]

# Promover deployment a producción
vercel promote [deployment-url]

# Alias (cambiar URL de producción)
vercel alias [deployment-url] tu-proyecto.vercel.app
```

---

## 🧪 DESARROLLO LOCAL CON VERCEL

```bash
# Ejecutar proyecto localmente con entorno de Vercel
vercel dev

# Ejecutar en puerto específico
vercel dev --listen 8080

# Usar variables de entorno de producción
vercel env pull .env.local
vercel dev
```

---

## 📁 GESTIÓN DE ARCHIVOS

```bash
# Descargar código de deployment
vercel download [deployment-url]

# Ver estructura del proyecto en Vercel
vercel inspect [deployment-url]
```

---

## 🔐 SECRETS (Variables Sensibles)

```bash
# Listar secrets
vercel secrets ls

# Agregar secret
vercel secrets add db-password "mi-password-seguro"

# Remover secret
vercel secrets rm db-password

# Renombrar secret
vercel secrets rename db-password database-password
```

---

## 🏗️ PROYECTOS

```bash
# Crear nuevo proyecto
vercel init

# Vincular carpeta actual a proyecto existente
vercel link

# Desvincular proyecto
vercel unlink

# Ver configuración del proyecto
vercel inspect
```

---

## 📧 EQUIPOS Y COLABORACIÓN

```bash
# Crear equipo
vercel teams create mi-equipo

# Cambiar a equipo
vercel switch mi-equipo

# Invitar miembro
vercel teams invite usuario@email.com

# Listar equipos
vercel teams ls
```

---

## 🎯 COMANDOS PYTHON ÚTILES

### Generar SECRET_KEY

```bash
# Generar SECRET_KEY segura
python -c "import secrets; print(secrets.token_hex(32))"
```

### Generar Password Hash

```bash
# Para crear usuarios en la base de datos
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('MiPassword123'))"
```

### Verificar Imports

```bash
# Verificar que todos los módulos se importan correctamente
python -c "from app import create_app; print('OK')"
```

### Test de Conexión a Base de Datos

```bash
# Probar conexión a MySQL en la nube
python -c "import pymysql; conn = pymysql.connect(host='tu-host', user='tu-user', password='tu-pwd', database='tu-db'); print('Conexión OK'); conn.close()"
```

---

## 🗄️ COMANDOS MYSQL

### Conectar a Base de Datos en la Nube

```bash
# PlanetScale
mysql -h your-host.connect.psdb.cloud -u username -p database_name

# Con password en el comando (menos seguro)
mysql -h your-host.connect.psdb.cloud -u username -pYOUR_PASSWORD database_name

# Railway
mysql -h containers-us-west-123.railway.app -P 1234 -u root -p
```

### Ejecutar Schema SQL

```bash
# Desde terminal
mysql -h host -u user -p database < database/schema.sql

# Desde MySQL
mysql> source /path/to/database/schema.sql;
```

### Backup de Base de Datos

```bash
# Exportar toda la base de datos
mysqldump -h host -u user -p database_name > backup_$(date +%Y%m%d).sql

# Exportar solo estructura (sin datos)
mysqldump -h host -u user -p --no-data database_name > schema_backup.sql

# Exportar solo datos
mysqldump -h host -u user -p --no-create-info database_name > data_backup.sql

# Restaurar backup
mysql -h host -u user -p database_name < backup.sql
```

### Verificar Tablas

```sql
-- Ver todas las tablas
SHOW TABLES;

-- Ver estructura de tabla
DESCRIBE user;

-- Contar registros
SELECT COUNT(*) FROM user;

-- Ver usuarios admin
SELECT username, email, role FROM user WHERE role = 'admin';
```

---

## 🐛 DEBUGGING

### Ver Errores en Vercel

```bash
# Logs con errores
vercel logs --grep "error" --follow

# Logs con warnings
vercel logs --grep "warning" --follow

# Logs de una función específica
vercel logs --grep "api/index.py" --follow
```

### Probar Localmente con Entorno de Producción

```bash
# 1. Descargar variables de entorno de producción
vercel env pull .env.production

# 2. Ejecutar con variables de producción
export FLASK_ENV=production
python app.py

# O en Windows PowerShell
$env:FLASK_ENV="production"
python app.py
```

### Verificar Build

```bash
# Ver proceso de build en detalle
vercel --prod --debug

# Ver solo warnings
vercel --prod 2>&1 | grep -i warning
```

---

## 📊 MONITOREO

### Analytics

```bash
# Ver analytics en CLI (requiere plan Pro)
vercel analytics

# O visitar:
# https://vercel.com/tu-usuario/tu-proyecto/analytics
```

### Status de Deployments

```bash
# Ver estado de deployment
vercel inspect [deployment-url]

# Ver si hay deployments fallidos
vercel list | grep -i error
```

---

## 🔄 CI/CD CON GITHUB

### Configurar Git Hooks

```bash
# Pre-commit hook (ejecutar antes de commit)
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
python -m pytest
EOF
chmod +x .git/hooks/pre-commit

# Pre-push hook (ejecutar antes de push)
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
vercel --prod --confirm
EOF
chmod +x .git/hooks/pre-push
```

### GitHub Actions (Opcional)

Crear `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## 💡 TIPS Y TRUCOS

### Alias para Comandos Frecuentes

```bash
# Agregar a ~/.bashrc o ~/.zshrc
alias vdeploy="vercel --prod"
alias vlogs="vercel logs --follow"
alias venv="vercel env ls"
alias vdev="vercel dev"

# Recargar configuración
source ~/.bashrc
```

### Script de Deploy Rápido

Crear `quick_deploy.sh`:

```bash
#!/bin/bash
echo "🚀 Deploy rápido a Vercel"

# Verificar cambios
git status

# Commit y push
git add .
git commit -m "Deploy: $(date +%Y-%m-%d_%H:%M)"
git push origin main

# Esperar deployment automático
echo "✅ Código subido - Vercel deploying automáticamente"
echo "📊 Ver logs: vercel logs --follow"
```

```bash
chmod +x quick_deploy.sh
./quick_deploy.sh
```

---

## 📋 CHECKLIST PRE-DEPLOY

```bash
# Ejecutar estos comandos antes de deploy

# 1. Verificar sintaxis Python
python -m py_compile app.py

# 2. Verificar requirements.txt actualizado
pip freeze > requirements.txt

# 3. Verificar .gitignore
cat .gitignore

# 4. Test imports
python -c "from app import create_app; create_app('production')"

# 5. Commit y push
git add .
git commit -m "Deploy ready"
git push origin main

# 6. Deploy
vercel --prod
```

---

## 🆘 COMANDOS DE EMERGENCIA

### Rollback a Deployment Anterior

```bash
# 1. Ver deployments
vercel list

# 2. Copiar URL del deployment anterior (que funcionaba)
# Ejemplo: https://tu-proyecto-abc123.vercel.app

# 3. Promover a producción
vercel alias https://tu-proyecto-abc123.vercel.app tu-proyecto.vercel.app
```

### Pausar Deployment

```bash
# No hay comando directo, pero puedes:

# Opción 1: Revertir último commit
git revert HEAD
git push origin main

# Opción 2: Eliminar deployment
vercel remove [deployment-url]

# Opción 3: En Vercel Dashboard
# Settings → Git → Disconnect
```

### Limpiar Cache

```bash
# Re-deploy forzando rebuild
vercel --prod --force

# O en Vercel Dashboard
# Deployments → [latest] → ⋮ → Redeploy → [x] Use existing Build Cache
```

---

## 📚 RECURSOS

- **Vercel CLI Docs**: https://vercel.com/docs/cli
- **API Reference**: https://vercel.com/docs/rest-api
- **GitHub Integration**: https://vercel.com/docs/git/vercel-for-github

---

**Última actualización**: Octubre 2025
**Versión del documento**: 1.0
