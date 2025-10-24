from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from enum import Enum

db = SQLAlchemy()

class UserRole(Enum):
    """Roles de usuario en el sistema"""
    ADMINISTRADOR = 'administrador'
    JEFE_UNIDAD = 'jefe_unidad'
    AUDITOR = 'auditor'
    USUARIO = 'usuario'

class AuditType(Enum):
    """Tipos de auditoría"""
    INTERNA = 'interna'
    EXTERNA = 'externa'

class CertificationStatus(Enum):
    """Estado de certificaciones"""
    VIGENTE = 'vigente'
    PROXIMA_VENCER = 'proxima_vencer'
    VENCIDA = 'vencida'
    RENOVACION = 'renovacion'

class User(UserMixin, db.Model):
    """Modelo de usuario del sistema"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120))
    role = db.Column(db.String(20), nullable=False, default=UserRole.USUARIO.value)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    certifications = db.relationship('Certification', backref='responsible', lazy='dynamic', foreign_keys='Certification.responsible_id')
    audits = db.relationship('Audit', backref='responsible', lazy='dynamic', foreign_keys='Audit.responsible_id')
    policy_confirmations = db.relationship('PolicyConfirmation', backref='confirmed_by', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_role(self):
        return UserRole(self.role)
    
    def get_role_object(self):
        """Obtiene el objeto Role completo del usuario"""
        return Role.query.filter_by(name=self.role).first()
    
    def can(self, module_name, action):
        """
        Verifica si el usuario tiene permiso para realizar una acción en un módulo
        
        Args:
            module_name (str): Nombre del módulo (ej: 'certifications', 'audits')
            action (str): Acción a verificar (ej: 'view', 'create', 'edit', 'delete', 'export', 'approve')
        
        Returns:
            bool: True si tiene el permiso, False si no
        
        Ejemplo:
            if current_user.can('audits', 'create'):
                # Permitir crear auditoría
        """
        if not self.is_active:
            return False
        
        role_obj = self.get_role_object()
        if not role_obj:
            return False
        
        return role_obj.has_permission(module_name, action)
    
    def get_accessible_modules(self):
        """
        Obtiene la lista de módulos a los que el usuario tiene acceso (can_view=True)
        
        Returns:
            list: Lista de diccionarios con información de módulos accesibles
        """
        role_obj = self.get_role_object()
        if not role_obj:
            return []
        
        permissions = RolePermission.query.filter(
            RolePermission.role_id == role_obj.id,
            RolePermission.can_view == True
        ).join(Module).filter(Module.is_active == True).order_by(Module.display_order).all()
        
        modules = []
        for perm in permissions:
            modules.append({
                'name': perm.module.name,
                'display_name': perm.module.display_name,
                'icon': perm.module.icon,
                'can_create': perm.can_create,
                'can_edit': perm.can_edit,
                'can_delete': perm.can_delete,
                'can_export': perm.can_export,
                'can_approve': perm.can_approve
            })
        
        return modules
    
    def __repr__(self):
        return f'<User {self.username}>'

class Certification(db.Model):
    """Modelo para certificaciones"""
    __tablename__ = 'certifications'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    norm = db.Column(db.String(100), nullable=False)
    issuing_entity = db.Column(db.String(150), nullable=False)
    emission_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    responsible_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    document_path = db.Column(db.String(255))
    status = db.Column(db.String(20), nullable=False, default=CertificationStatus.VIGENTE.value)
    alert_sent_15 = db.Column(db.Boolean, default=False)
    alert_sent_30 = db.Column(db.Boolean, default=False)
    alert_sent_60 = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def get_status(self):
        """Calcula el estado de la certificación basado en la fecha de vencimiento"""
        today = datetime.now().date()
        days_until_expiration = (self.expiration_date - today).days
        
        if days_until_expiration < 0:
            self.status = CertificationStatus.VENCIDA.value
        elif days_until_expiration <= 15:
            self.status = CertificationStatus.PROXIMA_VENCER.value
        else:
            self.status = CertificationStatus.VIGENTE.value
        
        return self.status
    
    def days_to_expiration(self):
        """Retorna los días faltantes para el vencimiento"""
        today = datetime.now().date()
        return (self.expiration_date - today).days
    
    def __repr__(self):
        return f'<Certification {self.name}>'

class Audit(db.Model):
    """Modelo para auditorías"""
    __tablename__ = 'audits'
    
    id = db.Column(db.Integer, primary_key=True)
    audit_type = db.Column(db.String(20), nullable=False)  # interna/externa
    scheduled_date = db.Column(db.Date, nullable=False)
    executed_date = db.Column(db.Date)
    evaluated_area = db.Column(db.String(150), nullable=False)
    responsible_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='programada')  # programada, en_ejecucion, completada
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    findings = db.relationship('AuditFinding', backref='audit', lazy='dynamic', cascade='all, delete-orphan')
    
    def has_critical_findings(self):
        """Verifica si la auditoría tiene hallazgos críticos"""
        return self.findings.filter_by(severity='critica').count() > 0
    
    def get_compliance_percentage(self):
        """Calcula el porcentaje de cumplimiento"""
        total_findings = self.findings.count()
        if total_findings == 0:
            return 100
        closed_findings = self.findings.filter_by(status='cerrado').count()
        return int((closed_findings / total_findings) * 100)
    
    def __repr__(self):
        return f'<Audit {self.id} - {self.evaluated_area}>'

class AuditFinding(db.Model):
    """Modelo para hallazgos de auditoría"""
    __tablename__ = 'audit_findings'
    
    id = db.Column(db.Integer, primary_key=True)
    audit_id = db.Column(db.Integer, db.ForeignKey('audits.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # critica, mayor, menor
    corrective_action = db.Column(db.Text)
    responsible = db.Column(db.String(120))
    deadline = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False, default='abierto')  # abierto, cerrado
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<AuditFinding {self.id}>'

class Policy(db.Model):
    """Modelo para políticas de cumplimiento"""
    __tablename__ = 'policies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    version = db.Column(db.String(10), default='1.0')
    effective_date = db.Column(db.Date, nullable=False, default=lambda: datetime.now().date())
    requires_confirmation = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    confirmations = db.relationship('PolicyConfirmation', backref='policy', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_confirmation_percentage(self):
        """Calcula el porcentaje de confirmaciones por unidad"""
        total_confirmations = self.confirmations.count()
        confirmed = self.confirmations.filter_by(confirmed=True).count()
        if total_confirmations == 0:
            return 0
        return int((confirmed / total_confirmations) * 100)
    
    def __repr__(self):
        return f'<Policy {self.title}>'

class PolicyConfirmation(db.Model):
    """Modelo para confirmaciones de políticas por usuario"""
    __tablename__ = 'policy_confirmations'
    
    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_date = db.Column(db.DateTime)
    digital_signature = db.Column(db.String(255))
    ip_address = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def mark_confirmed(self, ip_address=None):
        self.confirmed = True
        self.confirmed_date = datetime.now()
        self.ip_address = ip_address
    
    def __repr__(self):
        return f'<PolicyConfirmation Policy:{self.policy_id} User:{self.user_id}>'

class Alert(db.Model):
    """Modelo para alertas del sistema"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)  # expiration, audit, policy
    related_id = db.Column(db.Integer)  # ID del objeto relacionado (certification_id, audit_id, etc)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    severity = db.Column(db.String(20), default='info')  # info, warning, critical
    is_read = db.Column(db.Boolean, default=False)
    recipient_email = db.Column(db.String(120))
    sent = db.Column(db.Boolean, default=False)
    sent_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Alert {self.title}>'

class AuditLog(db.Model):
    """Modelo para registro de auditoría del sistema"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    changes = db.Column(db.Text)  # JSON con cambios
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)
    
    # Relación con usuario
    user = db.relationship('User', backref='audit_logs', foreign_keys=[user_id])
    
    def __repr__(self):
        return f'<AuditLog {self.action} {self.entity_type}:{self.entity_id}>'

class Role(db.Model):
    """Modelo para roles de usuario"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_system_role = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    permissions = db.relationship('RolePermission', back_populates='role', cascade='all, delete-orphan')
    
    def has_permission(self, module_name, action):
        """
        Verifica si el rol tiene un permiso específico para un módulo
        
        Args:
            module_name (str): Nombre del módulo (ej: 'certifications', 'audits')
            action (str): Acción a verificar (ej: 'view', 'create', 'edit', 'delete', 'export', 'approve')
        
        Returns:
            bool: True si tiene el permiso, False si no
        """
        permission = RolePermission.query.join(Module).filter(
            RolePermission.role_id == self.id,
            Module.name == module_name,
            Module.is_active == True
        ).first()
        
        if not permission:
            return False
        
        action_map = {
            'view': permission.can_view,
            'create': permission.can_create,
            'edit': permission.can_edit,
            'delete': permission.can_delete,
            'export': permission.can_export,
            'approve': permission.can_approve
        }
        
        return action_map.get(action, False)
    
    def get_module_permissions(self, module_name):
        """Obtiene todos los permisos del rol para un módulo específico"""
        permission = RolePermission.query.join(Module).filter(
            RolePermission.role_id == self.id,
            Module.name == module_name
        ).first()
        
        if not permission:
            return {
                'view': False,
                'create': False,
                'edit': False,
                'delete': False,
                'export': False,
                'approve': False
            }
        
        return {
            'view': permission.can_view,
            'create': permission.can_create,
            'edit': permission.can_edit,
            'delete': permission.can_delete,
            'export': permission.can_export,
            'approve': permission.can_approve
        }
    
    def __repr__(self):
        return f'<Role {self.name}>'

class Module(db.Model):
    """Modelo para módulos del sistema"""
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Clase de icono de Font Awesome
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relaciones
    permissions = db.relationship('RolePermission', back_populates='module', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Module {self.name}>'

class RolePermission(db.Model):
    """Modelo para permisos de roles por módulo"""
    __tablename__ = 'role_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id', ondelete='CASCADE'), nullable=False)
    
    # Permisos específicos
    can_view = db.Column(db.Boolean, default=False, nullable=False)
    can_create = db.Column(db.Boolean, default=False, nullable=False)
    can_edit = db.Column(db.Boolean, default=False, nullable=False)
    can_delete = db.Column(db.Boolean, default=False, nullable=False)
    can_export = db.Column(db.Boolean, default=False, nullable=False)
    can_approve = db.Column(db.Boolean, default=False, nullable=False)
    
    # Campo JSON para permisos personalizados adicionales
    custom_permissions = db.Column(db.Text)  # JSON
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    role = db.relationship('Role', back_populates='permissions')
    module = db.relationship('Module', back_populates='permissions')
    
    # Constraint único para role_id + module_id
    __table_args__ = (
        db.UniqueConstraint('role_id', 'module_id', name='uq_role_module'),
        db.Index('idx_role_permissions', 'role_id', 'module_id'),
    )
    
    def __repr__(self):
        return f'<RolePermission Role:{self.role_id} Module:{self.module_id}>'
