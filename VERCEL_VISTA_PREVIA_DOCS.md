# Guía de Deploy en Vercel - Vista Previa de Documentos

## Problema Resuelto ✅

La vista previa de documentos PDF ahora funciona correctamente tanto en desarrollo local como en Vercel.

## Cambios Realizados

### 1. Normalización de Rutas en Base de Datos
- ✅ Todas las rutas de documentos ahora usan formato: `/static/sample_documents/archivo.pdf`
- ✅ Script ejecutado: `temp_update.py` para normalizar rutas existentes

### 2. Archivos Estáticos Duplicados
Los PDFs de ejemplo ahora están en DOS ubicaciones:
- `app/static/sample_documents/` - Para desarrollo local
- `public/static/sample_documents/` - Para Vercel

### 3. Código Actualizado

#### `app/routes.py` - Función `view_document()`
- ✅ Maneja rutas estáticas (`/static/...`)
- ✅ Sirve archivos desde `app/static/` en local
- ✅ Logs de debug agregados

#### `app/templates/certifications/list.html`
- ✅ Agregado atributo `data-document-path` a los botones
- ✅ JavaScript actualizado para usar URLs estáticas directamente
- ✅ Evita pasar por Lambda en Vercel (más rápido)

#### `vercel.json`
- ✅ Build configurado para `public/**`
- ✅ Rutas actualizadas para servir desde `/public/static/`
- ✅ Headers correctos para PDFs

## Cómo Funciona

### En Desarrollo Local
1. Usuario hace clic en 👁️
2. JavaScript detecta que `document_path` empieza con `/static/`
3. Usa la URL estática directamente: `/static/sample_documents/archivo.pdf`
4. Flask sirve el archivo desde `app/static/sample_documents/`

### En Vercel
1. Usuario hace clic en 👁️
2. JavaScript detecta que `document_path` empieza con `/static/`
3. Usa la URL estática directamente: `/static/sample_documents/archivo.pdf`
4. Vercel sirve el archivo desde `public/static/sample_documents/` (sin pasar por Python)
5. ⚡ **Más rápido** - No usa función Lambda

## Comandos para Deploy

### 1. Actualizar Archivos PDF (si es necesario)
```powershell
# Copiar PDFs de app/ a public/
Copy-Item "app\static\sample_documents\*.pdf" "public\static\sample_documents\" -Force
```

### 2. Verificar Configuración
```powershell
# Ejecutar script de validación
python validate_vercel_setup.py
```

### 3. Deploy a Vercel
```bash
# Commit cambios
git add .
git commit -m "fix: Vista previa de documentos en Vercel"
git push

# Deploy
vercel --prod
```

## Verificación en Vercel

Después del deploy, verifica:

1. **Archivos estáticos accesibles:**
   - `https://tu-app.vercel.app/static/sample_documents/certificacion_iso9001.pdf`
   - `https://tu-app.vercel.app/static/sample_documents/certificacion_haccp.pdf`

2. **Vista previa funciona:**
   - Ve a Certificaciones
   - Haz clic en el botón 👁️
   - El PDF debe mostrarse en el modal

3. **Consola del navegador (F12):**
   - No debe haber errores 404
   - La petición debe ir directo a `/static/...` (no a `/certifications/document/...`)

## Solución de Problemas

### Los PDFs no se muestran en Vercel
```bash
# Verificar que los archivos están en el deploy
vercel ls public/static/sample_documents/

# Si faltan, copiarlos y volver a deployar
Copy-Item "app\static\sample_documents\*.pdf" "public\static\sample_documents\" -Force
git add public/static/sample_documents/
git commit -m "add: PDFs de ejemplo en public/"
git push
vercel --prod
```

### Error "No se puede mostrar la vista previa"
1. Abre F12 > Console
2. Busca errores de red
3. Verifica que la URL es: `/static/sample_documents/...` (no otra)
4. Prueba abrir el PDF directamente en el navegador

### Los cambios no se reflejan
```bash
# Limpiar caché de Vercel
vercel --prod --force

# O hacer un redeploy desde el dashboard de Vercel
```

## Archivos Modificados

```
✅ app/routes.py (función view_document)
✅ app/templates/certifications/list.html (JavaScript + data-document-path)
✅ vercel.json (rutas + builds)
✅ public/static/sample_documents/ (PDFs copiados)
✅ temp_update.py (normalización de rutas DB)
✅ database/schema.sql (rutas iniciales corregidas)
```

## Próximos Pasos

1. ✅ **Local funciona** - Confirmado
2. ⏳ **Deploy a Vercel** - Pendiente
3. ⏳ **Verificar en producción** - Pendiente

## Notas Importantes

- 📌 Los PDFs deben estar en AMBAS carpetas (`app/` y `public/`)
- 📌 Las rutas en DB deben ser `/static/...` (no rutas físicas)
- 📌 El JavaScript detecta automáticamente rutas estáticas y las usa directamente
- 📌 Vercel sirve archivos de `public/` sin pasar por Python (más eficiente)
