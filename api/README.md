# 📁 Carpeta `/api` - Vercel Serverless Functions

## 🎯 Propósito

Esta carpeta contiene el **punto de entrada** para desplegar la aplicación Flask en **Vercel como función serverless**.

Vercel detecta automáticamente archivos en la carpeta `api/` y los trata como serverless functions.

---

## 📄 Archivos

### `index.py`

**Función**: Punto de entrada principal de la aplicación.

**Ruta**: `api/index.py` → `https://tu-proyecto.vercel.app/*`

**Contenido**:
- Importa la aplicación Flask desde `app/`
- Configura el entorno de producción
- Exporta el handler para Vercel

```python
# Estructura básica
from app import create_app

app = create_app('production')
handler = app  # Vercel usa esto
```

---

## 🚀 ¿Cómo Funciona?

### En Desarrollo Local

```bash
python app.py
```

→ Usa `app.py` en la raíz
→ Entorno de desarrollo
→ Flask Debug Mode activado

### En Vercel (Producción)

```
Request → https://tu-proyecto.vercel.app/login
         ↓
      Vercel detecta ruta
         ↓
   Ejecuta api/index.py
         ↓
    Flask maneja request
         ↓
      Responde HTML
```

---

## ⚙️ Configuración en `vercel.json`

```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

**Explicación**:
- `"src": "app.py"` → Archivo principal de Flask
- `"use": "@vercel/python"` → Builder de Python de Vercel
- `"dest": "app.py"` → Redirige todas las rutas a app.py

---

## 🔄 Diferencias con `app.py`

| Aspecto | `app.py` (Local) | `api/index.py` (Vercel) |
|---------|------------------|-------------------------|
| **Entorno** | Development | Production |
| **Servidor** | Flask dev server | Vercel Serverless |
| **Hot reload** | ✅ Sí | ❌ No (redeploy) |
| **Debug** | ✅ Activado | ❌ Desactivado |
| **Base de datos** | MySQL local (XAMPP) | MySQL en la nube |
| **Persistencia** | ✅ Archivos locales | ❌ Efímero (usar S3/Blob) |

---

## 🐛 Debugging

### Ver qué se está ejecutando

```bash
# Ver logs de Vercel
vercel logs --follow

# Buscar errores
vercel logs --grep "error"
```

### Errores comunes

#### Error: "Module not found"

**Causa**: Python no encuentra el módulo `app`

**Solución**: Verificar que `sys.path.insert()` esté en `api/index.py`:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

#### Error: "Application failed to respond"

**Causa**: Flask no está exportando el handler correctamente

**Solución**: Verificar última línea de `api/index.py`:

```python
handler = app  # Vercel busca esta variable
```

---

## 📝 Notas Importantes

### ⚠️ NO modificar en producción

Este archivo se ejecuta en cada request en Vercel. Cambios aquí requieren **redeploy completo**.

### ⚠️ Imports pesados

Evitar imports innecesarios que aumenten el cold start time:

```python
# ❌ Evitar (si no se usan)
import pandas
import numpy
import tensorflow

# ✅ Solo lo necesario
from flask import Flask
from app import create_app
```

### ⚠️ Variables de entorno

Siempre usar variables de entorno, nunca hardcodear:

```python
# ❌ Nunca así
DB_PASSWORD = "mi_password_123"

# ✅ Así
DB_PASSWORD = os.environ.get('DB_PASSWORD')
```

---

## 🔧 Personalización

### Agregar más serverless functions

Puedes agregar más archivos en `api/` para endpoints específicos:

```
api/
├── index.py          # → https://tu-proyecto.vercel.app/*
├── webhook.py        # → https://tu-proyecto.vercel.app/api/webhook
└── cron.py           # → https://tu-proyecto.vercel.app/api/cron
```

Ejemplo `api/webhook.py`:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Procesar webhook
    return jsonify({"status": "ok"})

handler = app
```

---

## 📚 Recursos

- **Vercel Python Docs**: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- **Flask on Vercel Guide**: https://vercel.com/guides/using-flask-with-vercel
- **Serverless Functions**: https://vercel.com/docs/functions/serverless-functions

---

## ✅ Checklist

Antes de deploy, verificar:

- [ ] `api/index.py` existe
- [ ] Importa correctamente desde `app/`
- [ ] Exporta `handler = app`
- [ ] Sin imports innecesarios
- [ ] Variables de entorno usadas correctamente
- [ ] `vercel.json` apunta a `app.py`

---

**Última actualización**: Octubre 2025
**Mantenido por**: Equipo Frutos de Oro
