"""
Script de prueba para verificar zona horaria y fecha/hora
"""
from datetime import datetime
import pytz

print("=" * 80)
print("PRUEBA DE ZONA HORARIA")
print("=" * 80)

# Hora actual en diferentes formatos
print("\n1. datetime.now() - Hora local del sistema:")
print(f"   {datetime.now()}")
print(f"   Solo fecha: {datetime.now().date()}")

print("\n2. datetime.utcnow() - Hora UTC (NO USAR):")
print(f"   {datetime.utcnow()}")
print(f"   Solo fecha: {datetime.utcnow().date()}")

# Zona horaria de Perú
peru_tz = pytz.timezone('America/Lima')
print("\n3. Hora en Perú (America/Lima):")
print(f"   {datetime.now(peru_tz)}")
print(f"   Solo fecha: {datetime.now(peru_tz).date()}")

# Diferencia
print("\n4. Diferencia entre datetime.now() y datetime.utcnow():")
now_local = datetime.now()
now_utc = datetime.utcnow()
diff = now_utc - now_local
print(f"   {diff}")
print(f"   Horas de diferencia: {diff.total_seconds() / 3600:.1f}")

print("\n" + "=" * 80)
print("RECOMENDACIÓN: Siempre usar datetime.now() en lugar de datetime.utcnow()")
print("=" * 80)
