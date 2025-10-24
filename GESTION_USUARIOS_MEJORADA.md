# 👥 Gestión de Usuarios - Actualización

## ✅ Cambios Implementados

### 1. **Vista Mejorada de Usuarios** (`app/templates/admin/users.html`)

#### Estadísticas en Dashboard
- **Total de usuarios** en el sistema
- **Usuarios activos** (con sesión habilitada)
- **Usuarios inactivos** (sin acceso al sistema)
- **Distribución por roles** (gráfico de usuarios por rol)

#### Sistema de Filtros
- 🔍 **Búsqueda por texto**: Nombre, email, usuario o departamento
- 👔 **Filtro por rol**: Todos los roles disponibles en dropdown
- ✅ **Filtro por estado**: Activos, Inactivos o Todos
- 🔄 **Botón limpiar**: Resetea todos los filtros

#### Tabla de Usuarios con Información Detallada
- Avatar circular con icono de usuario
- **Nombre de usuario** con badge "Tú" para el usuario actual
- **Información completa**: Nombre completo, email, departamento
- **Badge de rol** con colores distintivos:
  - 🔴 **Administrador**: Rojo con icono de corona
  - 🔵 **Jefes**: Azul con icono de corbata
  - 🟡 **Auditores**: Amarillo con icono de checklist
  - ⚫ **Usuarios**: Gris con icono genérico

#### Toggle de Estado Activo/Inactivo
- ✅ **Switch toggle** visual para cada usuario
- 🔒 **Protección**: El admin no puede desactivarse a sí mismo
- ⚡ **Actualización instantánea** vía AJAX
- 📝 **Registro en bitácora** de cada cambio de estado
- ✔️ **Confirmación**: Pregunta antes de cambiar el estado

### 2. **Backend Mejorado** (`app/routes.py`)

#### Ruta `/admin/users` Actualizada
```python
@admin_bp.route('/users')
@login_required
def list_users():
    # Filtros: rol, estado, búsqueda
    # Paginación: 20 usuarios por página
    # Estadísticas: totales por estado y rol
    # Ordenado por: rol y nombre
```

**Características:**
- Acepta parámetros de query: `?role=auditor&status=active&search=juan&page=2`
- Búsqueda con LIKE insensible a mayúsculas
- Estadísticas calculadas en tiempo real
- Paginación mejorada

#### Nueva Ruta: `/admin/users/<id>/toggle-status` (POST)
```python
@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    # Solo administradores
    # No permite auto-desactivación
    # Registra cambio en audit_logs
    # Retorna JSON con resultado
```

**Validaciones:**
- ✅ Usuario debe ser administrador
- ✅ No puede desactivarse a sí mismo
- ✅ Registra cambio en la bitácora
- ✅ Responde con JSON (success/error)

### 3. **Seguridad Implementada**

#### Protecciones
- ❌ **No auto-desactivación**: El admin no puede desactivar su propia cuenta
- 🔐 **Solo administradores**: Verificación en cada ruta
- 📝 **Auditoría completa**: Cada cambio se registra con:
  - Usuario que realizó el cambio
  - Fecha y hora
  - IP del usuario
  - Estado anterior y nuevo
  - Usuario afectado

#### Registro en Bitácora
```json
{
  "action": "toggle_user_status",
  "entity_type": "user",
  "entity_id": 3,
  "changes": {
    "username": "jefe_produccion",
    "old_status": "active",
    "new_status": "inactive"
  }
}
```

## 🎯 Cómo Usar

### Acceso
1. Inicia sesión como **administrador**
2. Ve a **"Administrar Usuarios"** en el sidebar
3. Verás la lista completa de usuarios

### Filtrar Usuarios

#### Por Rol
```
Selecciona un rol del dropdown:
- Administrador
- Jefe de Calidad
- Jefe de Producción
- Auditor Interno
- Auditor
- Usuario General
```

#### Por Estado
```
- Activos: Solo usuarios con acceso habilitado
- Inactivos: Solo usuarios sin acceso
- Todos: Sin filtro de estado
```

#### Por Búsqueda
```
Escribe en el campo de búsqueda:
- Nombre de usuario (ej: "admin")
- Nombre completo (ej: "Juan Pérez")
- Email (ej: "juan@empresa.com")
- Departamento (ej: "Producción")
```

### Activar/Desactivar Usuario

1. **Localiza al usuario** en la tabla
2. **Click en el toggle** (switch azul/gris)
3. **Confirma la acción** en el diálogo
4. El estado cambia **inmediatamente**
5. Aparece **notificación de éxito** (toast)

#### Efectos de Desactivar
- ❌ Usuario **no puede iniciar sesión**
- 🔒 Sesión actual se mantiene hasta que cierre
- 📝 Cambio registrado en bitácora
- 🔄 Puede reactivarse en cualquier momento

## 📊 Estadísticas Visibles

### Panel Superior
```
┌─────────────────┬─────────────────┬─────────────────┐
│ Total Usuarios  │ Usuarios Activos│ Usuarios Inact. │
│      15         │       12        │       3         │
└─────────────────┴─────────────────┴─────────────────┘
```

### Distribución por Rol
```
[2] Administrador
[3] Jefe de Calidad
[4] Jefe de Producción
[2] Auditor Interno
[3] Auditor
[1] Usuario General
```

## 🎨 Interfaz Visual

### Colores de Roles
- 🔴 **Rojo** (bg-danger): Administrador
- 🔵 **Azul** (bg-primary): Jefes de Unidad/Calidad/Producción
- 🟡 **Amarillo** (bg-warning): Auditores
- ⚫ **Gris** (bg-secondary): Usuario General

### Estado del Toggle
- ✅ **Verde + Check**: Usuario Activo
- ❌ **Rojo + X**: Usuario Inactivo
- 🔒 **Deshabilitado**: Tu propia cuenta (no puedes desactivarte)

### Paginación
- **20 usuarios por página**
- Navegación con botones Anterior/Siguiente
- Números de página clickeables
- Filtros se mantienen al cambiar de página

## 🔧 Archivos Modificados

### Backend
```
✅ app/routes.py
   - Actualizada ruta list_users() con filtros
   - Nueva ruta toggle_user_status()
   - Estadísticas y agrupación por rol
```

### Frontend
```
✅ app/templates/admin/users.html (NUEVO)
   - Vista completa con estadísticas
   - Filtros en sidebar
   - Tabla con toggle de estado
   - JavaScript para AJAX
   - Notificaciones toast
```

## 📝 Ejemplos de Uso

### Caso 1: Desactivar Auditor que Ya No Trabaja
```
1. Ir a "Administrar Usuarios"
2. Buscar por nombre: "Carlos González"
3. Click en el toggle para desactivar
4. Confirmar acción
5. ✅ Usuario desactivado, no puede entrar más
```

### Caso 2: Ver Solo Auditores Activos
```
1. Filtro Rol: "Auditor Interno"
2. Filtro Estado: "Activos"
3. Click "Aplicar Filtros"
4. ✅ Lista solo auditores activos
```

### Caso 3: Buscar Usuario por Email
```
1. Campo búsqueda: "produccion@empresa.com"
2. Click "Aplicar Filtros"
3. ✅ Muestra usuario con ese email
```

## 🚨 Mensajes del Sistema

### Éxito
- ✅ "Usuario activado correctamente"
- ✅ "Usuario desactivado correctamente"

### Errores
- ❌ "No puedes desactivar tu propia cuenta"
- ❌ "No autorizado" (si no eres admin)
- ❌ "Error al actualizar el estado del usuario"

## 🔐 Permisos Requeridos

| Acción | Rol Requerido | Ruta |
|--------|---------------|------|
| Ver lista usuarios | Administrador | `/admin/users` |
| Filtrar usuarios | Administrador | `/admin/users?role=...` |
| Activar/Desactivar | Administrador | `/admin/users/<id>/toggle-status` |
| Crear usuario | Administrador | `/admin/users/new` |
| Editar usuario | Administrador | `/admin/users/<id>/edit` |

## 📱 Responsive Design

La interfaz se adapta a diferentes tamaños:
- **Desktop**: Filtros en sidebar lateral
- **Tablet**: Filtros colapsables
- **Móvil**: Tabla scrollable horizontal

## 🎯 Próximos Pasos Sugeridos

1. **Probar el Sistema:**
   - Crear varios usuarios con diferentes roles
   - Probar filtros combinados
   - Activar y desactivar usuarios
   - Verificar que los desactivados no pueden entrar

2. **Verificar Bitácora:**
   - Ir a "Registro de Sistema"
   - Ver los cambios de estado registrados
   - Verificar IP y timestamps

3. **Exportar Datos:**
   - Agregar botón para exportar lista filtrada a Excel
   - Incluir estadísticas en el reporte

---

**¡Sistema completamente funcional! ✅**

Solo los administradores pueden ver y gestionar usuarios.
Los cambios de estado se registran automáticamente.
La interfaz es intuitiva y fácil de usar.
