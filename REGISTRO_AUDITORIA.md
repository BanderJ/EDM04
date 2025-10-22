# 📋 Sistema de Registro de Auditoría - Frutos de Oro

## Descripción General

Sistema completo de bitácora que registra **todas las acciones** de los usuarios en el sistema, incluyendo:
- ✅ Creación de registros
- ✅ Modificaciones (con detalles de cambios)
- ✅ Eliminaciones
- ✅ Visualizaciones
- ✅ Confirmaciones de políticas
- ✅ Inicio/cierre de sesión
- ✅ IP del usuario
- ✅ Fecha y hora exactas

---

## 🎯 Funcionalidades Implementadas

### 1. **Modelo de Datos (`AuditLog`)**
- `user_id`: Usuario que realizó la acción
- `action`: Tipo de acción (create, update, delete, view, etc.)
- `entity_type`: Tipo de entidad afectada (policy, certification, audit, etc.)
- `entity_id`: ID del registro afectado
- `changes`: JSON con detalles específicos de los cambios
- `ip_address`: Dirección IP del usuario
- `created_at`: Timestamp con fecha y hora

### 2. **Funciones de Utilidad (`utils.py`)**

#### `log_action(user_id, action, entity_type, entity_id, changes, ip_address)`
Registra cualquier acción en el sistema de forma automática.

**Ejemplo de uso:**
```python
from app.utils import log_action

log_action(
    user_id=current_user.id,
    action='create',
    entity_type='certification',
    entity_id=cert.id,
    ip_address=request.remote_addr
)
```

#### `get_entity_changes(old_obj, new_data, fields)`
Compara el estado anterior con el nuevo y genera un JSON con los cambios específicos.

**Ejemplo de uso:**
```python
from app.utils import get_entity_changes

changes = get_entity_changes(
    old_obj=certification,
    new_data={'name': 'Nuevo Nombre', 'norm': 'ISO 9001'},
    fields=['name', 'norm', 'issuing_entity']
)
```

**Salida:**
```json
{
    "name": {"old": "Antiguo Nombre", "new": "Nuevo Nombre"},
    "norm": {"old": "ISO 14001", "new": "ISO 9001"}
}
```

### 3. **Vista de Administración (`/admin/audit-log`)**

#### Características:
- ✅ **Estadísticas en tiempo real**
  - Total de registros
  - Registros del día actual
  - Usuarios activos
  - Tipos de acciones únicas

- ✅ **Filtros avanzados**
  - Por usuario
  - Por tipo de acción
  - Por tipo de entidad
  - Por rango de fechas

- ✅ **Paginación**
  - 20 registros por página
  - Navegación intuitiva

- ✅ **Visualización detallada**
  - Iconos por tipo de acción
  - Colores distintivos
  - Cambios específicos en formato JSON legible
  - Información de IP y timestamp

- ✅ **Exportación** (próximamente)
  - Exportar a Excel
  - Exportar a PDF

---

## 🚀 Acciones Registradas Automáticamente

### **Políticas**
- ✅ `create`: Creación de nueva política
- ✅ `update`: Actualización de política (con cambios detallados)
- ✅ `view_policy`: Visualización de política
- ✅ `confirm_policy`: Confirmación de lectura

### **Certificaciones**
- ✅ `create`: Nueva certificación registrada
- ✅ `update`: Certificación modificada (campos específicos)
- ✅ `delete`: Certificación eliminada

### **Auditorías**
- ✅ `create`: Nueva auditoría programada
- ✅ `update`: Auditoría actualizada
- ✅ Hallazgos registrados

### **Usuarios**
- ✅ `login`: Inicio de sesión
- ✅ `logout`: Cierre de sesión
- ✅ `create`: Nuevo usuario creado
- ✅ `update`: Usuario modificado

---

## 📊 Vista de Políticas Mejorada

### Nuevas Funcionalidades en `/policies/<id>/view`:

1. **Historial de Cambios**
   - Últimas 10 acciones sobre la política
   - Quién hizo cada cambio
   - Cuándo se realizó
   - Qué se modificó (detalles JSON)
   - IP del usuario

2. **Sección de Documentos y Recursos**
   - Documentos adjuntos
   - Botones de edición (solo admin)
   - Botón de eliminación (solo admin)

3. **Registro automático de visualización**
   - Cada vez que un usuario ve una política, se registra
   - Útil para auditorías de cumplimiento

---

## 🎨 Interfaz Visual

### Colores por Acción:
- 🟢 **Verde**: Crear, Login
- 🔵 **Azul**: Actualizar, Ver
- 🔴 **Rojo**: Eliminar
- 🟡 **Amarillo**: Logout, Advertencias
- ⚫ **Gris**: Acciones neutras

### Iconos:
- ➕ Crear
- ✏️ Editar
- 🗑️ Eliminar
- 👁️ Ver
- ✅ Confirmar
- 🔑 Login/Logout

---

## 🔐 Permisos

**Solo administradores** pueden:
- Ver el registro completo de auditoría
- Aplicar filtros avanzados
- Ver cambios detallados de otros usuarios

**Todos los usuarios**:
- Sus acciones se registran automáticamente
- No pueden ver el log de auditoría (solo admins)

---

## 📝 Ejemplos de Uso

### Ver registro completo:
```
http://localhost:5000/admin/audit-log
```

### Filtrar por usuario específico:
```
http://localhost:5000/admin/audit-log?user_id=5
```

### Filtrar por acción:
```
http://localhost:5000/admin/audit-log?action=update
```

### Filtrar por tipo de entidad:
```
http://localhost:5000/admin/audit-log?entity_type=certification
```

### Filtrar por fecha:
```
http://localhost:5000/admin/audit-log?date_from=2025-01-01
```

### Combinar filtros:
```
http://localhost:5000/admin/audit-log?user_id=5&action=update&entity_type=policy&date_from=2025-10-01
```

---

## 🔧 Configuración de Base de Datos

El sistema ya está configurado en `models.py`. Solo necesitas ejecutar las migraciones:

```bash
flask db upgrade
```

O si usas init.py:
```bash
python init.py
```

---

## 📦 Archivos Modificados/Creados

### Nuevos Archivos:
- ✅ `app/templates/admin/audit_log.html` - Vista principal del log
- ✅ `REGISTRO_AUDITORIA.md` - Esta documentación

### Archivos Modificados:
- ✅ `app/utils.py` - Funciones `log_action()` y `get_entity_changes()`
- ✅ `app/models.py` - Relación `user` en `AuditLog`
- ✅ `app/routes.py` - Rutas mejoradas con logging automático
- ✅ `app/templates/policies/view.html` - Historial de cambios
- ✅ `app/templates/base.html` - Sticky footer

---

## 🎯 Beneficios

1. **Cumplimiento Normativo**: Auditoría completa para ISO, BPM, HACCP
2. **Seguridad**: Trazabilidad de todas las acciones
3. **Responsabilidad**: Saber quién hizo qué y cuándo
4. **Análisis**: Estadísticas de uso del sistema
5. **Investigación**: Resolver incidencias con datos precisos

---

## 🚀 Próximas Mejoras (Sugerencias)

- [ ] Exportar logs a Excel/PDF
- [ ] Alertas automáticas por acciones críticas
- [ ] Dashboard de actividad en tiempo real
- [ ] Gráficos de uso por usuario/módulo
- [ ] Retención automática de logs (eliminar antiguos)
- [ ] Búsqueda por texto libre
- [ ] Notificaciones por email de acciones importantes

---

## 📞 Soporte

Para más información o soporte, contacta al administrador del sistema.

**Desarrollado para Agroindustria Frutos de Oro S.A.C.**
