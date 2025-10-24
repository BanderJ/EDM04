# Sistema de Permisos - Guía de Implementación

## 📋 Descripción General

El sistema de permisos implementa control de acceso basado en roles (RBAC) con permisos granulares por módulo y acción.

## 🏗️ Arquitectura

### Tablas de Base de Datos

1. **roles**: Define los roles del sistema
   - `administrador`: Acceso total al sistema
   - `jefe_calidad`: Gestión completa de certificaciones, auditorías y hallazgos
   - `jefe_produccion`: Crear/editar certificaciones y auditorías
   - `auditor_interno`: Gestión completa de auditorías y hallazgos
   - `auditor`: Crear auditorías y hallazgos
   - `jefe_unidad`: Permisos personalizados por unidad
   - `usuario`: Solo lectura en módulos principales

2. **modules**: Módulos del sistema
   - `dashboard`: Panel principal
   - `certifications`: Certificaciones
   - `audits`: Auditorías
   - `findings`: Hallazgos
   - `policies`: Políticas
   - `reports`: Reportes
   - `users`: Gestión de usuarios (solo admin)
   - `permissions`: Gestión de permisos (solo admin)
   - `audit_logs`: Bitácora del sistema (solo admin)

3. **role_permissions**: Permisos por rol y módulo
   - `can_view`: Puede ver/listar
   - `can_create`: Puede crear nuevos registros
   - `can_edit`: Puede editar registros existentes
   - `can_delete`: Puede eliminar registros
   - `can_export`: Puede exportar datos
   - `can_approve`: Puede aprobar/confirmar

## 🔧 Uso en Python (Routes)

### 1. Proteger Rutas con Decorador

```python
from flask import Blueprint, render_template
from flask_login import login_required
from app.decorators import require_permission

audits_bp = Blueprint('audits', __name__)

@audits_bp.route('/audits')
@login_required
@require_permission('audits', 'view')
def list_audits():
    """Solo usuarios con can_view en audits pueden acceder"""
    # Código para listar auditorías
    pass

@audits_bp.route('/audits/new', methods=['GET', 'POST'])
@login_required
@require_permission('audits', 'create')
def new_audit():
    """Solo usuarios con can_create en audits pueden acceder"""
    # Código para crear auditoría
    pass

@audits_bp.route('/audits/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@require_permission('audits', 'edit')
def edit_audit(id):
    """Solo usuarios con can_edit en audits pueden acceder"""
    # Código para editar auditoría
    pass

@audits_bp.route('/audits/<int:id>/delete', methods=['POST'])
@login_required
@require_permission('audits', 'delete')
def delete_audit(id):
    """Solo usuarios con can_delete en audits pueden acceder"""
    # Código para eliminar auditoría
    pass
```

### 2. Verificar Permisos en Código

```python
from flask import flash, redirect, url_for
from flask_login import current_user

def some_function():
    # Verificar permiso antes de realizar acción
    if not current_user.can('policies', 'approve'):
        flash('No tiene permisos para aprobar políticas', 'danger')
        return redirect(url_for('policies.list'))
    
    # Continuar con la acción
    policy.approved = True
    db.session.commit()
```

### 3. Obtener Módulos Accesibles

```python
from flask_login import current_user

@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Obtener módulos a los que el usuario tiene acceso
    modules = current_user.get_accessible_modules()
    
    # modules = [
    #     {
    #         'name': 'certifications',
    #         'display_name': 'Certificaciones',
    #         'icon': 'fa-certificate',
    #         'can_create': True,
    #         'can_edit': True,
    #         'can_delete': False,
    #         'can_export': True,
    #         'can_approve': False
    #     },
    #     ...
    # ]
    
    return render_template('dashboard/index.html', modules=modules)
```

## 🎨 Uso en Templates (Jinja2)

### 1. Mostrar/Ocultar Elementos

```html
<!-- Mostrar botón solo si tiene permiso para crear -->
{% if check_permission('audits', 'create') %}
<a href="{{ url_for('audits.new') }}" class="btn btn-primary">
    <i class="fas fa-plus"></i> Nueva Auditoría
</a>
{% endif %}

<!-- Mostrar botón de editar solo si tiene permiso -->
{% if check_permission('audits', 'edit') %}
<a href="{{ url_for('audits.edit', id=audit.id) }}" class="btn btn-sm btn-warning">
    <i class="fas fa-edit"></i> Editar
</a>
{% endif %}

<!-- Mostrar botón de eliminar solo si tiene permiso -->
{% if check_permission('audits', 'delete') %}
<button type="button" class="btn btn-sm btn-danger" onclick="confirmDelete({{ audit.id }})">
    <i class="fas fa-trash"></i> Eliminar
</button>
{% endif %}
```

### 2. Menú de Navegación Dinámico

```html
<!-- sidebar.html -->
<nav class="sidebar">
    <ul class="nav flex-column">
        <!-- Dashboard - Siempre visible si está autenticado -->
        <li class="nav-item">
            <a class="nav-link" href="{{ url_for('dashboard.index') }}">
                <i class="fas fa-home"></i> Dashboard
            </a>
        </li>
        
        <!-- Certificaciones - Solo si tiene permiso de ver -->
        {% if check_permission('certifications', 'view') %}
        <li class="nav-item">
            <a class="nav-link" href="{{ url_for('certifications.list') }}">
                <i class="fas fa-certificate"></i> Certificaciones
            </a>
        </li>
        {% endif %}
        
        <!-- Auditorías - Solo si tiene permiso de ver -->
        {% if check_permission('audits', 'view') %}
        <li class="nav-item">
            <a class="nav-link" href="{{ url_for('audits.list') }}">
                <i class="fas fa-clipboard-check"></i> Auditorías
            </a>
        </li>
        {% endif %}
        
        <!-- Políticas - Solo si tiene permiso de ver -->
        {% if check_permission('policies', 'view') %}
        <li class="nav-item">
            <a class="nav-link" href="{{ url_for('policies.list') }}">
                <i class="fas fa-file-alt"></i> Políticas
            </a>
        </li>
        {% endif %}
        
        <!-- Gestión de Permisos - Solo administradores -->
        {% if current_user.role == 'administrador' %}
        <li class="nav-item">
            <a class="nav-link" href="{{ url_for('admin.permissions') }}">
                <i class="fas fa-user-shield"></i> Permisos
            </a>
        </li>
        {% endif %}
    </ul>
</nav>
```

### 3. Tabla de Datos con Acciones Condicionales

```html
<!-- list_audits.html -->
<table class="table">
    <thead>
        <tr>
            <th>Código</th>
            <th>Nombre</th>
            <th>Tipo</th>
            <th>Estado</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        {% for audit in audits %}
        <tr>
            <td>{{ audit.code }}</td>
            <td>{{ audit.name }}</td>
            <td>{{ audit.audit_type }}</td>
            <td>{{ audit.status }}</td>
            <td>
                <!-- Ver - Siempre visible si tiene permiso de ver -->
                <a href="{{ url_for('audits.view', id=audit.id) }}" 
                   class="btn btn-sm btn-info" title="Ver detalles">
                    <i class="fas fa-eye"></i>
                </a>
                
                <!-- Editar - Solo si tiene permiso -->
                {% if check_permission('audits', 'edit') %}
                <a href="{{ url_for('audits.edit', id=audit.id) }}" 
                   class="btn btn-sm btn-warning" title="Editar">
                    <i class="fas fa-edit"></i>
                </a>
                {% endif %}
                
                <!-- Eliminar - Solo si tiene permiso -->
                {% if check_permission('audits', 'delete') %}
                <button type="button" class="btn btn-sm btn-danger" 
                        onclick="confirmDelete({{ audit.id }})" title="Eliminar">
                    <i class="fas fa-trash"></i>
                </button>
                {% endif %}
                
                <!-- Exportar - Solo si tiene permiso -->
                {% if check_permission('audits', 'export') %}
                <a href="{{ url_for('audits.export', id=audit.id) }}" 
                   class="btn btn-sm btn-success" title="Exportar">
                    <i class="fas fa-download"></i>
                </a>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

## 🔐 Decoradores Disponibles

### 1. `@require_permission(module, action)`
Verifica permisos específicos para un módulo y acción.

```python
@require_permission('audits', 'create')
@require_permission('policies', 'approve')
@require_permission('users', 'delete')
```

### 2. `@admin_required`
Solo permite acceso a administradores.

```python
@admin_required
def admin_settings():
    pass
```

### 3. `@role_required(*roles)`
Permite acceso a roles específicos.

```python
@role_required('administrador', 'jefe_calidad', 'auditor_interno')
def quality_report():
    pass
```

## 📊 Matriz de Permisos por Rol

| Módulo | Administrador | Jefe Calidad | Jefe Producción | Auditor Interno | Auditor | Usuario |
|--------|--------------|--------------|-----------------|-----------------|---------|---------|
| **Dashboard** |
| Ver | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Exportar | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Certificaciones** |
| Ver | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Crear | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Editar | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Eliminar | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Exportar | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Auditorías** |
| Ver | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Crear | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Editar | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Eliminar | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Exportar | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Aprobar | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Hallazgos** |
| Ver | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Crear | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Editar | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Eliminar | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Políticas** |
| Ver | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Crear | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Editar | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Eliminar | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Aprobar | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Usuarios** |
| Ver | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Crear | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Editar | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Eliminar | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Permisos** |
| Ver | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Editar | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Bitácora** |
| Ver | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Exportar | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

## 🚀 Próximos Pasos

1. **Aplicar decoradores a todas las rutas**
   - Actualizar `app/routes.py` con `@require_permission`
   - Proteger rutas de creación, edición y eliminación

2. **Actualizar templates**
   - Actualizar sidebar con `check_permission`
   - Actualizar tablas de listado con botones condicionales
   - Actualizar páginas de detalle con acciones condicionales

3. **Crear interfaz de gestión de permisos**
   - Ruta `/admin/permissions` para administradores
   - UI con toggles para configurar permisos
   - Guardar cambios en `role_permissions`

4. **Testing**
   - Probar cada rol en cada módulo
   - Verificar que los permisos se respetan
   - Validar mensajes de error 403

## 📝 Notas Importantes

- Los permisos se validan tanto en backend (decoradores) como frontend (templates)
- La validación en frontend es para UX, pero el backend siempre valida
- Los cambios en permisos requieren que el usuario cierre sesión y vuelva a entrar
- El rol `administrador` tiene acceso completo excepto audit_logs (solo view+export)
- Los módulos `users`, `permissions` y `audit_logs` son solo para administradores
