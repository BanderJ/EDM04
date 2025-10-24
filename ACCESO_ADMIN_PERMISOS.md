# 🔐 Resumen de Roles y Permisos

## 📊 Estado Actual del Sistema

### ✅ Implementación Completada

1. **Base de Datos** - Tablas creadas en `schema.sql`:
   - ✅ `roles` - 7 roles del sistema
   - ✅ `modules` - 9 módulos de la aplicación  
   - ✅ `role_permissions` - 63 configuraciones de permisos

2. **Backend Python**:
   - ✅ Modelos: `Role`, `Module`, `RolePermission` en `app/models.py`
   - ✅ Métodos de usuario: `user.can(module, action)` y `user.get_accessible_modules()`
   - ✅ Decoradores: `@require_permission()`, `@admin_required`, `@role_required()`
   - ✅ Rutas de administración en `app/routes.py`:
     - `/admin/permissions` - Vista de gestión
     - `/admin/permissions/update` - API para actualizar permisos

3. **Frontend**:
   - ✅ Sidebar actualizado con opción "Gestión de Permisos"
   - ✅ Template `admin/permissions.html` con toggles interactivos
   - ✅ JavaScript para guardar cambios automáticamente

---

## 🎯 Acceso al Usuario Admin

### ¿Qué Rol Tiene el Usuario Admin?

Según el schema SQL (línea 226):

```sql
INSERT INTO `users` (`username`, `email`, `password_hash`, `full_name`, `department`, `role`, `is_active`) 
VALUES ('admin', 'admin@frutosoro.com', 'pbkdf2:sha256:...', 'Administrador Sistema', 'Dirección', 'administrador', TRUE);
```

**El usuario `admin` tiene el rol: `administrador`**

### ¿Qué Permisos Tiene el Rol Administrador?

Según el schema SQL (líneas 287-295), el administrador tiene **TODOS LOS PERMISOS**:

| Módulo | Ver | Crear | Editar | Eliminar | Exportar | Aprobar |
|--------|-----|-------|--------|----------|----------|---------|
| Dashboard | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Certificaciones | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Auditorías | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Hallazgos | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Políticas | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Reportes | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Usuarios** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Permisos** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Bitácora | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |

---

## 🔍 Verificación de Acceso

### Sidebar del Administrador

En `app/templates/base.html` (líneas 116-130), el sidebar muestra estas opciones solo si `current_user.role == 'administrador'`:

```html
{% if current_user.role == 'administrador' %}
    <li class="nav-item">
        <a class="nav-link" href="{{ url_for('admin.list_users') }}">
            <i class="fas fa-users"></i> Administrar Usuarios
        </a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="{{ url_for('admin.permissions') }}">
            <i class="fas fa-user-shield"></i> Gestión de Permisos
        </a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="{{ url_for('admin.audit_log') }}">
            <i class="fas fa-history"></i> Registro de Sistema
        </a>
    </li>
{% endif %}
```

### Rutas Protegidas

En `app/routes.py`, las rutas verifican:

```python
if current_user.role != UserRole.ADMINISTRADOR.value:
    flash('No tienes permiso para acceder a esta sección.', 'danger')
    return redirect(url_for('dashboard.index'))
```

---

## 🚀 Cómo Acceder

### Opción 1: Recargar la Página

1. **Cierra sesión** del usuario actual
2. **Inicia sesión** nuevamente con:
   - Usuario: `admin`
   - Contraseña: `admin123`
3. Verás en el sidebar:
   - 📊 Inicio
   - 📜 Certificaciones
   - ✅ Auditorías
   - 📋 Políticas
   - 📈 Reportes
   - **👥 Administrar Usuarios**
   - **🔐 Gestión de Permisos** ← NUEVA OPCIÓN
   - **📜 Registro de Sistema**

### Opción 2: Verificar que la Base de Datos Está Actualizada

Si no ves la opción, ejecuta este script SQL para verificar:

```sql
-- Verificar que existen las tablas
SHOW TABLES LIKE 'role%';

-- Verificar que el usuario admin tiene el rol correcto
SELECT username, role FROM users WHERE username = 'admin';

-- Verificar que existen los roles
SELECT * FROM roles;

-- Verificar que existen los módulos
SELECT * FROM modules;

-- Verificar permisos del administrador
SELECT r.display_name as rol, m.display_name as modulo,
       rp.can_view, rp.can_create, rp.can_edit, rp.can_delete, rp.can_export, rp.can_approve
FROM role_permissions rp
JOIN roles r ON rp.role_id = r.id
JOIN modules m ON rp.module_id = m.id
WHERE r.name = 'administrador';
```

---

## 🔧 Solución de Problemas

### Problema: "No veo Gestión de Permisos en el sidebar"

**Posibles causas:**

1. **Base de datos no actualizada**
   - Solución: Ejecutar `database/schema.sql` completo
   ```bash
   mysql -u root -p frutos_oro_db < database/schema.sql
   ```

2. **Caché del navegador**
   - Solución: Presionar `Ctrl + Shift + R` para recargar sin caché

3. **Sesión antigua**
   - Solución: Cerrar sesión y volver a iniciar sesión

4. **Rol incorrecto del usuario**
   - Verificar en la base de datos:
   ```sql
   SELECT username, role FROM users WHERE username = 'admin';
   ```
   - Debe ser: `administrador` (no `admin`)

5. **Servidor no reiniciado**
   - Solución: Detener y reiniciar el servidor Flask
   ```bash
   # Presionar Ctrl+C en la terminal
   # Luego ejecutar:
   python app.py
   ```

### Problema: "Error 403 al acceder a /admin/permissions"

**Verificar:**
```python
# En routes.py debe estar:
if current_user.role != UserRole.ADMINISTRADOR.value:
```

**UserRole.ADMINISTRADOR.value debe ser igual a 'administrador'**

---

## 📝 Matriz Completa de Acceso por Rol

| Rol | Dashboard | Certs | Audits | Findings | Policies | Reports | Users | Perms | Logs |
|-----|-----------|-------|--------|----------|----------|---------|-------|-------|------|
| **Administrador** | ✅✅✅✅✅✅ | ✅✅✅✅✅✅ | ✅✅✅✅✅✅ | ✅✅✅✅✅✅ | ✅✅✅✅✅✅ | ✅✅✅✅✅✅ | ✅✅✅✅✅✅ | ✅✅✅✅✅✅ | ✅❌❌❌✅❌ |
| **Jefe Calidad** | ✅❌❌❌✅❌ | ✅✅✅✅✅✅ | ✅✅✅✅✅✅ | ✅✅✅✅✅✅ | ✅✅✅❌✅✅ | ✅✅❌❌✅❌ | ✅❌❌❌❌❌ | ❌❌❌❌❌❌ | ❌❌❌❌❌❌ |
| **Jefe Producción** | ✅❌❌❌✅❌ | ✅✅✅❌✅❌ | ✅✅✅❌✅❌ | ✅✅✅❌✅❌ | ✅❌❌❌✅❌ | ✅✅❌❌✅❌ | ✅❌❌❌❌❌ | ❌❌❌❌❌❌ | ❌❌❌❌❌❌ |
| **Auditor Interno** | ✅❌❌❌✅❌ | ✅❌❌❌✅❌ | ✅✅✅❌✅❌ | ✅✅✅❌✅❌ | ✅❌❌❌✅❌ | ✅✅❌❌✅❌ | ✅❌❌❌❌❌ | ❌❌❌❌❌❌ | ❌❌❌❌❌❌ |
| **Auditor** | ✅❌❌❌❌❌ | ✅❌❌❌✅❌ | ✅✅❌❌✅❌ | ✅✅❌❌✅❌ | ✅❌❌❌❌❌ | ✅❌❌❌✅❌ | ❌❌❌❌❌❌ | ❌❌❌❌❌❌ | ❌❌❌❌❌❌ |
| **Usuario** | ✅❌❌❌❌❌ | ✅❌❌❌❌❌ | ✅❌❌❌❌❌ | ✅❌❌❌❌❌ | ✅❌❌❌❌❌ | ✅❌❌❌❌❌ | ❌❌❌❌❌❌ | ❌❌❌❌❌❌ | ❌❌❌❌❌❌ |

**Leyenda:** ✅Ver ✅Crear ✅Editar ✅Eliminar ✅Exportar ✅Aprobar

---

## 📞 Próximos Pasos Sugeridos

1. **Probar el Sistema:**
   - Iniciar sesión como `admin`
   - Ir a "Gestión de Permisos"
   - Cambiar algunos toggles
   - Verificar que se guardan correctamente

2. **Aplicar Decoradores:**
   - Agregar `@require_permission()` a rutas existentes
   - Actualizar templates con `check_permission()`

3. **Crear Usuarios de Prueba:**
   - Crear usuarios con diferentes roles
   - Probar acceso a cada módulo
   - Verificar restricciones funcionan correctamente

---

**¿El usuario admin debería ver "Gestión de Permisos"? SÍ ✅**

Si no lo ves, sigue los pasos de "Solución de Problemas" arriba.
