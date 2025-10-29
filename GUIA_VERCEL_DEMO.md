# 🚀 Guía de Despliegue en Vercel con Documentos de Muestra

## 📋 Descripción

Esta guía explica cómo desplegar el sistema en Vercel usando **documentos de muestra** para demostración, evitando el problema del filesystem read-only.

## ✨ Características del Modo Demo

- ✅ **Vista previa de documentos funcional** sin subir archivos
- ✅ **PDFs de muestra** precargados en `/app/static/sample_documents/`
- ✅ **Sin errores de filesystem** en Vercel
- ✅ **Demo completa** con certificaciones de ejemplo
- ✅ **Automático** cuando `USE_SAMPLE_DOCUMENTS=true`

## 📁 Archivos de Muestra Incluidos

Los siguientes PDFs están en `app/static/sample_documents/`:

1. **certificacion_iso9001.pdf** - Certificación ISO 9001:2015
2. **certificacion_haccp.pdf** - Certificación HACCP

## 🔧 Configuración

### 1. Variables de Entorno en Vercel

Agrega en el dashboard de Vercel:

```env
# Base de datos (AWS RDS o tu servidor MySQL)
DATABASE_URL=mysql+pymysql://usuario:password@host:puerto/database?ssl=true

# Modo demostración (IMPORTANTE para Vercel)
USE_SAMPLE_DOCUMENTS=true

# Flask
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta-super-segura-aqui
```

### 2. Estructura del Proyecto

```
EDM04/
├── app/
│   ├── static/
│   │   ├── sample_documents/        ← 📄 PDFs de muestra
│   │   │   ├── certificacion_iso9001.pdf
│   │   │   ├── certificacion_haccp.pdf
│   │   │   └── README.md
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── ...
├── api/
│   └── index.py                     ← Entry point de Vercel
├── init_demo_data.py                ← Script para crear datos de muestra
├── vercel.json                      ← Configuración de Vercel
└── ...
```

## 🚀 Pasos de Despliegue

### 1. Preparar el Repositorio

```bash
# Asegúrate de que los archivos de muestra estén incluidos
git add app/static/sample_documents/
git add init_demo_data.py
git add vercel.json
git commit -m "Agregar documentos de muestra para Vercel"
git push
```

### 2. Desplegar en Vercel

```bash
# Opción A: Desde la CLI
vercel --prod

# Opción B: Desde el dashboard de Vercel
# 1. Importar proyecto desde GitHub
# 2. Configurar variables de entorno
# 3. Deploy
```

### 3. Inicializar Datos de Muestra

**Después del primer despliegue**, ejecuta localmente conectando a tu BD de producción:

```bash
# En tu máquina local, configurar .env con BD de producción
DATABASE_URL=mysql+pymysql://usuario:password@host/database

# Ejecutar script de inicialización
python init_demo_data.py
```

Esto creará 5 certificaciones de muestra:
- ✅ 2 vigentes
- ⏰ 1 próxima a vencer
- ❌ 1 vencida
- ✅ 1 BPM activa

## 🎯 Cómo Funciona

### Flujo de Vista Previa de Documentos

1. Usuario hace clic en "Ver Documento"
2. Sistema detecta `USE_SAMPLE_DOCUMENTS=true`
3. En lugar de buscar archivo subido:
   - Identifica el tipo de certificación (ISO, HACCP, BPM)
   - Sirve el PDF de muestra correspondiente desde `/static/sample_documents/`
4. El PDF se muestra en el modal de vista previa

### Código en `app/routes.py`

```python
@certifications_bp.route('/document/<int:cert_id>')
@login_required
def view_document(cert_id):
    """Servir documento con modo demo en Vercel"""
    
    # Si está en modo demo, usar archivos estáticos
    if current_app.config.get('USE_SAMPLE_DOCUMENTS', False):
        sample_folder = current_app.config.get('SAMPLE_DOCUMENTS_FOLDER')
        
        # Mapear tipo de certificación → archivo de muestra
        sample_files = {
            'ISO 9001': 'certificacion_iso9001.pdf',
            'HACCP': 'certificacion_haccp.pdf',
            'BPM': 'certificacion_iso9001.pdf'
        }
        
        sample_file = sample_files.get(certification.certification_type, 'certificacion_iso9001.pdf')
        return send_from_directory(sample_folder, sample_file)
    
    # Modo normal: archivo subido por el usuario
    return send_from_directory(directory, filename)
```

## 📊 Datos de Muestra Creados

| Certificación | Entidad | Número | Estado | Área |
|--------------|---------|--------|--------|------|
| ISO 9001 | Bureau Veritas | ISO-2024-001 | ✅ Vigente | Calidad |
| HACCP | SGS International | HACCP-2024-045 | ⏰ Por vencer | Producción |
| BPM | ICONTEC | BPM-2024-078 | ✅ Vigente | Operaciones |
| ISO 9001 | TÜV Rheinland | ISO-2023-234 | ❌ Vencida | Logística |
| HACCP | Bureau Veritas | HACCP-2024-112 | ⏰ Por vencer | Empaque |

## 🔄 Actualizar para Producción Real

Cuando quieras permitir subida real de archivos (en EC2, VPS, etc.):

1. Cambiar variable de entorno:
   ```env
   USE_SAMPLE_DOCUMENTS=false
   ```

2. El sistema automáticamente usará archivos reales subidos por usuarios

## ⚡ Ventajas de Este Enfoque

✅ **Sin errores de filesystem** en Vercel  
✅ **Demo completamente funcional** para mostrar a clientes  
✅ **Fácil de probar** la funcionalidad de vista previa  
✅ **Migración simple** a producción real (solo cambiar variable)  
✅ **PDFs reales** con contenido visible  
✅ **Sin dependencias externas** (no requiere S3, Cloudinary, etc.)

## 🎨 Testing Local

Para probar el modo demo localmente:

```bash
# En .env local
USE_SAMPLE_DOCUMENTS=true

# Iniciar servidor
python app.py

# Navegar a Certificaciones → Ver Documento
# Debería mostrar el PDF de muestra
```

## 📝 Notas Importantes

1. **Subida de archivos**: Aunque los usuarios vean el formulario de subida, los archivos NO se guardan en Vercel (filesystem read-only). El sistema simplemente muestra los PDFs de muestra.

2. **Para producción real**: Considera EC2, VPS, PythonAnywhere o usar S3/Cloudinary para almacenar archivos reales.

3. **Base de datos**: Los registros de certificaciones SÍ se guardan en la BD (AWS RDS), solo los archivos físicos son de muestra.

## 🆘 Troubleshooting

### El PDF no se muestra

```bash
# Verificar que los archivos existan
ls app/static/sample_documents/

# Verificar variable de entorno en Vercel
vercel env ls

# Verificar logs
vercel logs
```

### Error 404 en documentos

Asegúrate de que `vercel.json` incluya:

```json
{
  "routes": [
    {
      "src": "/static/sample_documents/(.*)",
      "dest": "/app/static/sample_documents/$1"
    }
  ]
}
```

## 🎉 ¡Listo!

Ahora tienes un sistema completamente funcional en Vercel con documentos de muestra que se pueden visualizar sin problemas de filesystem.
