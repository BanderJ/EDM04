#!/usr/bin/env python3
"""
Script para inicializar datos de demostración en Vercel
Este script crea certificaciones de muestra que apuntan a archivos estáticos
"""
import os
import sys
from datetime import datetime, timedelta

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Certification

def init_demo_data():
    """Crear datos de demostración para Vercel"""
    app = create_app(os.environ.get('FLASK_ENV', 'production'))
    
    with app.app_context():
        print("🔧 Inicializando datos de demostración...")
        
        # Verificar si ya existen certificaciones
        if Certification.query.count() > 0:
            print("⚠️  Ya existen certificaciones en la base de datos")
            response = input("¿Deseas agregar certificaciones de muestra de todos modos? (s/n): ")
            if response.lower() != 's':
                print("❌ Operación cancelada")
                return
        
        # Buscar un usuario admin para asignar las certificaciones
        admin_user = User.query.filter_by(role='admin').first()
        if not admin_user:
            print("⚠️  No se encontró un usuario admin")
            print("   Por favor, crea un usuario admin primero")
            return
        
        print(f"✅ Usando usuario admin: {admin_user.full_name}")
        
        # Crear certificaciones de muestra
        sample_certs = [
            {
                'certification_type': 'ISO 9001',
                'issuing_entity': 'Bureau Veritas',
                'certificate_number': 'ISO-2024-001',
                'issue_date': datetime.now() - timedelta(days=300),
                'expiry_date': datetime.now() + timedelta(days=765),
                'scope': 'Procesamiento y empaque de frutas deshidratadas',
                'responsible_area': 'Calidad',
                'document_path': 'static/sample_documents/certificacion_iso9001.pdf',
                'notes': 'Certificación de muestra para demostración en Vercel'
            },
            {
                'certification_type': 'HACCP',
                'issuing_entity': 'SGS International',
                'certificate_number': 'HACCP-2024-045',
                'issue_date': datetime.now() - timedelta(days=200),
                'expiry_date': datetime.now() + timedelta(days=165),
                'scope': 'Sistema de Análisis de Peligros y Puntos Críticos de Control',
                'responsible_area': 'Producción',
                'document_path': 'static/sample_documents/certificacion_haccp.pdf',
                'notes': 'Certificación HACCP de muestra para inocuidad alimentaria'
            },
            {
                'certification_type': 'BPM',
                'issuing_entity': 'ICONTEC',
                'certificate_number': 'BPM-2024-078',
                'issue_date': datetime.now() - timedelta(days=150),
                'expiry_date': datetime.now() + timedelta(days=215),
                'scope': 'Buenas Prácticas de Manufactura en planta de procesamiento',
                'responsible_area': 'Operaciones',
                'document_path': 'static/sample_documents/certificacion_iso9001.pdf',
                'notes': 'Certificación BPM de muestra usando documento ISO como referencia'
            },
            {
                'certification_type': 'ISO 9001',
                'issuing_entity': 'TÜV Rheinland',
                'certificate_number': 'ISO-2023-234',
                'issue_date': datetime.now() - timedelta(days=450),
                'expiry_date': datetime.now() - timedelta(days=85),  # Vencida
                'scope': 'Gestión de calidad en almacenamiento y distribución',
                'responsible_area': 'Logística',
                'document_path': 'static/sample_documents/certificacion_iso9001.pdf',
                'notes': '⚠️ Certificación VENCIDA - Requiere renovación urgente'
            },
            {
                'certification_type': 'HACCP',
                'issuing_entity': 'Bureau Veritas',
                'certificate_number': 'HACCP-2024-112',
                'issue_date': datetime.now() - timedelta(days=320),
                'expiry_date': datetime.now() + timedelta(days=45),  # Próxima a vencer
                'scope': 'Control de puntos críticos en línea de empaque',
                'responsible_area': 'Empaque',
                'document_path': 'static/sample_documents/certificacion_haccp.pdf',
                'notes': '⏰ Próxima a vencer - Iniciar proceso de renovación'
            }
        ]
        
        created_count = 0
        for cert_data in sample_certs:
            # Verificar si ya existe esta certificación
            existing = Certification.query.filter_by(
                certificate_number=cert_data['certificate_number']
            ).first()
            
            if existing:
                print(f"⚠️  Certificación {cert_data['certificate_number']} ya existe, omitiendo...")
                continue
            
            # Crear nueva certificación
            certification = Certification(**cert_data)
            certification.created_by = admin_user.id
            
            db.session.add(certification)
            created_count += 1
            print(f"✅ Creada: {cert_data['certification_type']} - {cert_data['certificate_number']}")
        
        # Guardar cambios
        if created_count > 0:
            db.session.commit()
            print(f"\n🎉 ¡Listo! Se crearon {created_count} certificaciones de muestra")
            print("📄 Las certificaciones usan archivos PDF estáticos de /app/static/sample_documents/")
            print("🌐 Perfecto para demostración en Vercel (sin necesidad de subir archivos)")
        else:
            print("\n ℹ️  No se crearon nuevas certificaciones")

if __name__ == '__main__':
    try:
        init_demo_data()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
