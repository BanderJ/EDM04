import os
os.environ['DB_ENGINE'] = 'mysql'

from app import create_app, db
from app.models import Certification

app = create_app()

with app.app_context():
    certs = Certification.query.all()
    print(f"Total certificaciones: {len(certs)}")
    
    for cert in certs:
        if not cert.document_path:
            continue
            
        old = cert.document_path
        
        # Si es una ruta física (Windows o Unix), dejarla como está
        if (cert.document_path.startswith('D:') or 
            cert.document_path.startswith('/var') or
            cert.document_path.startswith('C:')):
            print(f"\n{cert.name}: Ruta física - SIN CAMBIOS")
            print(f"  {cert.document_path}")
            continue
        
        # Normalizar rutas estáticas
        if 'sample_documents/' in cert.document_path:
            # Extraer solo la parte después de sample_documents/
            if 'sample_documents/' in cert.document_path:
                filename = cert.document_path.split('sample_documents/')[-1]
                cert.document_path = f'/static/sample_documents/{filename}'
                print(f"\n{cert.name}: NORMALIZADO")
                print(f"  Antes: {old}")
                print(f"  Ahora: {cert.document_path}")
    
    db.session.commit()
    print("\n✅ Rutas actualizadas correctamente")
