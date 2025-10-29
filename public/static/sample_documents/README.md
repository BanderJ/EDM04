# Sample Documents para Vercel

Esta carpeta contiene documentos PDF de ejemplo que se utilizan en el modo de demostración en Vercel.

## Archivos

- `certificacion_iso9001.pdf` - Certificado de ejemplo ISO 9001:2015
- `certificacion_haccp.pdf` - Certificado de ejemplo HACCP

## Importante

⚠️ **Estos archivos deben estar sincronizados con `app/static/sample_documents/`**

En Vercel, los archivos estáticos se sirven desde la carpeta `public/`, por lo que:
- Los archivos en `app/static/sample_documents/` se usan en desarrollo local
- Los archivos en `public/static/sample_documents/` se usan en Vercel

## Actualización

Si actualizas los PDFs de ejemplo, debes copiarlos a ambas ubicaciones:

```powershell
Copy-Item "app\static\sample_documents\*.pdf" "public\static\sample_documents\" -Force
```

## URLs

Los archivos son accesibles en:
- Local: `http://localhost:5000/static/sample_documents/certificacion_iso9001.pdf`
- Vercel: `https://tu-app.vercel.app/static/sample_documents/certificacion_iso9001.pdf`
