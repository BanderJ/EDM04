# ⚠️ IMPORTANTE: ESTRUCTURA PARA VERCEL

## 🏗️ Estructura Correcta del Proyecto

Tu proyecto Flask para Vercel debe tener esta estructura:

```
EDM04/                          ← Raíz del proyecto (Root Directory)
│
├── vercel.json                 ← ✅ CRÍTICO: Config de Vercel
├── requirements.txt            ← ✅ CRÍTICO: Dependencias Python
├── .vercelignore              ← Archivos a ignorar
│
├── api/                        ← ✅ CRÍTICO: Serverless functions
│   └── index.py               ← ✅ CRÍTICO: Punto de entrada Flask
│
├── app/                        ← Tu aplicación Flask
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── static/                ← CSS, JS, imágenes
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/             ← HTML templates
│       └── ...
│
├── config.py
├── app.py                      ← Para desarrollo local solamente
└── database/
    └── schema.sql
```

---

## ❌ ERRORES COMUNES

### Error 1: "Vercel pide index.html en src/"

**❌ Causa**: Vercel cree que es un sitio HTML estático

**Esto NO es un proyecto HTML estático**, es una **aplicación Flask (Python)**.

**✅ Solución**:

1. **Verificar `vercel.json` en la raíz**:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

2. **Verificar que existe `api/index.py`**

3. **En configuración de Vercel**:
   - Framework Preset: **"Other"**
   - Root Directory: **"./"** (raíz, NO "src")
   - Build Command: vacío o `pip install -r requirements.txt`

---

### Error 2: "No Build Output directory"

**❌ Causa**: Vercel busca carpeta de output como "dist/" o "build/"

**✅ Solución**: 
- En Vercel settings, dejar **Output Directory** vacío
- Las serverless functions no necesitan output directory

---

### Error 3: "Module not found: app"

**❌ Causa**: Python no encuentra el módulo `app`

**✅ Solución**: Verificar que `api/index.py` tenga:

```python
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
```

---

## ✅ CHECKLIST PRE-DEPLOY

Antes de importar en Vercel, verificar:

- [ ] `vercel.json` existe en la raíz
- [ ] `vercel.json` apunta a `api/index.py`
- [ ] `api/index.py` existe y tiene contenido correcto
- [ ] `requirements.txt` existe en la raíz
- [ ] `app/` carpeta existe con `__init__.py`
- [ ] NO hay carpeta `src/` (esto es Flask, no React/Vue)
- [ ] Código está en GitHub

---

## 🔧 CONFIGURACIÓN CORRECTA EN VERCEL WEB

Al importar el proyecto en vercel.com:

### Paso 1: Framework Preset
```
Framework Preset: Other
```
**NO seleccionar**: Next.js, React, Vue, etc.

### Paso 2: Root Directory
```
Root Directory: ./
```
**NO cambiar** a "src" o cualquier otra carpeta

### Paso 3: Build Settings

**Build Command**:
```
[dejar vacío]
```
O si pide algo:
```
pip install -r requirements.txt
```

**Output Directory**:
```
[dejar vacío]
```

**Install Command**:
```
pip install -r requirements.txt
```

### Paso 4: Environment Variables

Agregar antes de deploy:
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `FLASK_ENV=production`
- `SECRET_KEY`

---

## 📁 NO Crear Carpeta "src"

⚠️ **IMPORTANTE**: 

Este proyecto **NO necesita** carpeta `src/` porque:

- ✅ Es una aplicación Flask (Python backend)
- ✅ Usa serverless functions de Vercel
- ✅ El punto de entrada es `api/index.py`
- ✅ Los templates están en `app/templates/`
- ✅ Los archivos estáticos en `app/static/`

La carpeta `src/` es para proyectos frontend (React, Vue, etc.), **no para Flask**.

---

## 🎯 Estructura Frontend vs Backend

### ❌ Proyecto Frontend (React/Vue/HTML)
```
proyecto/
├── src/              ← Aquí va el código
│   └── index.html
├── public/
└── package.json
```

### ✅ Proyecto Backend (Flask/Python) ← TU PROYECTO
```
proyecto/
├── api/              ← Serverless functions
│   └── index.py
├── app/              ← Aplicación Flask
│   ├── static/
│   └── templates/
├── vercel.json       ← Config
└── requirements.txt  ← Dependencias
```

---

## 🔍 Verificar Deploy

Después de deployar, verificar en Vercel Dashboard:

1. **Functions Tab**:
   - Debe mostrar: `api/index.py`
   - Status: Active

2. **Build Logs**:
   - Debe mostrar: "Installing Python dependencies"
   - Debe instalar desde `requirements.txt`
   - NO debe buscar `index.html`

3. **Runtime Logs**:
   - Debe mostrar requests a Flask
   - NO debe mostrar errores de "Module not found"

---

## 🆘 Si Sigue Sin Funcionar

### Opción 1: Re-importar Proyecto

1. En Vercel Dashboard → Settings
2. Scroll abajo → **Delete Project**
3. Volver a importar desde GitHub
4. Asegurar configuración correcta

### Opción 2: Usar Vercel CLI

```bash
# Instalar Vercel CLI
npm install -g vercel

# En la carpeta del proyecto
cd d:\Apps\EDM04

# Deploy
vercel

# Seguir instrucciones
```

### Opción 3: Verificar vercel.json

Asegurar que `vercel.json` tenga exactamente:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "app/static/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/app/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

---

## 📞 Recursos

- **Vercel Python Functions**: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- **Flask on Vercel**: https://vercel.com/guides/using-flask-with-vercel
- **Vercel Build Configuration**: https://vercel.com/docs/build-step

---

**Fecha**: Octubre 2025
**Proyecto**: Frutos de Oro - Sistema de Gestión de Cumplimiento
**Stack**: Flask + MySQL + Vercel Serverless
