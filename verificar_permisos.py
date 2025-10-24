"""
Script de verificación de permisos del usuario admin
"""

# Simulación de lo que debería verse en el sidebar
print("=" * 70)
print("VERIFICACIÓN DE ACCESO - USUARIO ADMIN")
print("=" * 70)

print("\n✅ Usuario: admin")
print("✅ Rol esperado: 'administrador'")
print("✅ Contraseña: admin123\n")

print("📋 OPCIONES DEL SIDEBAR QUE DEBERÍA VER EL ADMIN:")
print("-" * 70)
print("📊 Inicio                    (url: /dashboard)")
print("📜 Certificaciones           (url: /certifications)")
print("✅ Auditorías                (url: /audits)")
print("📋 Políticas                 (url: /policies)")
print("📈 Reportes                  (url: /reports)")
print("\n🔐 OPCIONES DE ADMINISTRADOR:")
print("-" * 70)
print("👥 Administrar Usuarios      (url: /admin/users)")
print("🔐 Gestión de Permisos       (url: /admin/permissions)  ⭐ NUEVA")
print("📜 Registro de Sistema       (url: /admin/audit-log)")

print("\n" + "=" * 70)
print("¿NO VES 'GESTIÓN DE PERMISOS'? SOLUCIONES:")
print("=" * 70)

print("\n1️⃣  REINICIAR EL SERVIDOR:")
print("   - Presiona Ctrl+C en la terminal donde corre el servidor")
print("   - Ejecuta: python app.py")
print("   - O ejecuta: iniciar_app.bat")

print("\n2️⃣  LIMPIAR CACHÉ DEL NAVEGADOR:")
print("   - Presiona Ctrl + Shift + R")
print("   - O Ctrl + F5")

print("\n3️⃣  CERRAR Y VOLVER A INICIAR SESIÓN:")
print("   - Haz clic en 'Cerrar Sesión'")
print("   - Vuelve a entrar con admin/admin123")

print("\n4️⃣  VERIFICAR BASE DE DATOS:")
print("   - Abre MySQL Workbench o phpMyAdmin")
print("   - Ejecuta: SELECT username, role FROM users WHERE username = 'admin';")
print("   - Debe mostrar: admin | administrador")

print("\n5️⃣  REINSTALAR BASE DE DATOS:")
print("   - En MySQL ejecuta: SOURCE d:/Apps/EDM04/database/schema.sql")
print("   - O desde terminal: mysql -u root -p frutos_oro_db < database/schema.sql")

print("\n" + "=" * 70)
print("PERMISOS DEL ADMINISTRADOR (desde schema.sql):")
print("=" * 70)

permisos = {
    "Dashboard": "✅ Ver, Crear, Editar, Eliminar, Exportar, Aprobar",
    "Certificaciones": "✅ Ver, Crear, Editar, Eliminar, Exportar, Aprobar",
    "Auditorías": "✅ Ver, Crear, Editar, Eliminar, Exportar, Aprobar",
    "Hallazgos": "✅ Ver, Crear, Editar, Eliminar, Exportar, Aprobar",
    "Políticas": "✅ Ver, Crear, Editar, Eliminar, Exportar, Aprobar",
    "Reportes": "✅ Ver, Crear, Editar, Eliminar, Exportar, Aprobar",
    "Usuarios": "✅ Ver, Crear, Editar, Eliminar, Exportar, Aprobar",
    "Permisos": "✅ Ver, Crear, Editar, Eliminar, Exportar, Aprobar",
    "Bitácora": "✅ Ver, Exportar (sin crear/editar/eliminar/aprobar)",
}

for modulo, permisos_str in permisos.items():
    print(f"\n{modulo}:")
    print(f"  {permisos_str}")

print("\n" + "=" * 70)
print("ARCHIVOS MODIFICADOS RECIENTEMENTE:")
print("=" * 70)
print("✅ app/routes.py           - Agregadas rutas /admin/permissions")
print("✅ app/templates/base.html - Agregada opción en sidebar")
print("✅ app/templates/admin/permissions.html - Nuevo template con toggles")
print("✅ app/models.py           - Modelos Role, Module, RolePermission")
print("✅ app/decorators.py       - Decoradores de permisos")

print("\n" + "=" * 70)
print("¿NECESITAS AYUDA? Ejecuta uno de estos comandos:")
print("=" * 70)
print("python verificar_permisos.py")
print("python app.py")
print("\n")
