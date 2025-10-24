from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from app.models import db, User, Certification, Audit, AuditFinding, Policy, PolicyConfirmation, Alert, AuditLog, UserRole, CertificationStatus
from app.utils import allowed_file, save_upload_file, send_email_alert, generate_pdf_report, generate_excel_report

# Blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
certifications_bp = Blueprint('certifications', __name__, url_prefix='/certifications')
audits_bp = Blueprint('audits', __name__, url_prefix='/audits')
policies_bp = Blueprint('policies', __name__, url_prefix='/policies')
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
api_bp = Blueprint('api', __name__, url_prefix='/api')

# ============ RUTAS RAÍZ ============
@auth_bp.route('/')
def root_index():
    """Ruta raíz - redirige al login o dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

# ============ AUTENTICACIÓN ============
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login con manejo robusto de errores"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            user = User.query.filter_by(username=username).first()
            
            if user is None or not user.check_password(password):
                flash('Usuario o contraseña incorrectos.', 'danger')
                return redirect(url_for('auth.login'))
            
            if not user.is_active:
                flash('Tu cuenta está desactivada.', 'warning')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=request.form.get('remember_me'))
            
            # Registrar en audit log
            try:
                log_entry = AuditLog(
                    user_id=user.id,
                    action='login',
                    ip_address=request.remote_addr
                )
                db.session.add(log_entry)
                db.session.commit()
            except Exception as e:
                print(f"Error al registrar login en auditoría: {e}")
                db.session.rollback()
            
            next_page = request.args.get('next')
            if not next_page or not url_has_allowed_host_and_scheme(next_page):
                next_page = url_for('dashboard.index')
            
            flash(f'Bienvenido {user.full_name}!', 'success')
            return redirect(next_page)
            
        except Exception as e:
            # Error de conexión a BD u otro error
            error_msg = str(e)
            if 'Can\'t connect' in error_msg or 'OperationalError' in error_msg or 'InterfaceError' in error_msg:
                flash('⚠️ Error de conexión a la base de datos. Por favor, verifica la conexión.', 'danger')
                print(f"\n{'='*80}\n⚠️ Error de conexión a la base de datos:\n{error_msg}\n{'='*80}\n")
            else:
                flash(f'Error en el login: {error_msg}', 'danger')
                print(f"Error en login: {error_msg}")
            
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    try:
        log_entry = AuditLog(
            user_id=current_user.id,
            action='logout',
            ip_address=request.remote_addr
        )
        db.session.add(log_entry)
        db.session.commit()
    except Exception as e:
        print(f"Error al registrar logout: {e}")
        db.session.rollback()
    
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))

def url_has_allowed_host_and_scheme(url, allowed_hosts=None, require_https=False):
    """Validar que la URL es segura para redireccionamiento"""
    if allowed_hosts is None:
        allowed_hosts = []
    if not url.startswith(('http://', 'https://', '/')):
        return False
    if url.startswith('/'):
        return True
    return False

# ============ DASHBOARD ============
@dashboard_bp.route('/')
@login_required
def index():
    """Panel de control principal"""
    try:
        # Datos para el dashboard
        total_certifications = Certification.query.count()
        vigent_certifications = Certification.query.filter_by(status=CertificationStatus.VIGENTE.value).count()
        expiring_certifications = Certification.query.filter_by(status=CertificationStatus.PROXIMA_VENCER.value).count()
        expired_certifications = Certification.query.filter_by(status=CertificationStatus.VENCIDA.value).count()
        
        total_audits = Audit.query.count()
        completed_audits = Audit.query.filter_by(status='completada').count()
        scheduled_audits = Audit.query.filter_by(status='programada').count()
        
        total_policies = Policy.query.filter_by(is_active=True).count()
        
        # Certificaciones próximas a vencer (próximos 30 días)
        upcoming_certifications = Certification.query.filter(
            Certification.expiration_date <= datetime.now().date() + timedelta(days=30),
            Certification.expiration_date >= datetime.now().date()
        ).order_by(Certification.expiration_date).limit(5).all()
        
        # Auditorías recientes
        recent_audits = Audit.query.order_by(Audit.created_at.desc()).limit(5).all()
        
        # Alertas pendientes
        pending_alerts = Alert.query.filter_by(is_read=False).order_by(Alert.created_at.desc()).limit(5).all()
        
        context = {
            'total_certifications': total_certifications,
            'vigent_certifications': vigent_certifications,
            'expiring_certifications': expiring_certifications,
            'expired_certifications': expired_certifications,
            'total_audits': total_audits,
            'completed_audits': completed_audits,
            'scheduled_audits': scheduled_audits,
            'total_policies': total_policies,
            'upcoming_certifications': upcoming_certifications,
            'recent_audits': recent_audits,
            'pending_alerts': pending_alerts,
            'certification_percentage': int((vigent_certifications / total_certifications * 100) if total_certifications > 0 else 0),
            'audit_percentage': int((completed_audits / total_audits * 100) if total_audits > 0 else 0)
        }
        
        return render_template('dashboard/index.html', **context)
    
    except Exception as e:
        # Si hay error de BD, mostrar dashboard vacío
        flash(f'Advertencia: Error al cargar datos. {str(e)}', 'warning')
        context = {
            'total_certifications': 0,
            'vigent_certifications': 0,
            'expiring_certifications': 0,
            'expired_certifications': 0,
            'total_audits': 0,
            'completed_audits': 0,
            'scheduled_audits': 0,
            'total_policies': 0,
            'upcoming_certifications': [],
            'recent_audits': [],
            'pending_alerts': [],
            'certification_percentage': 0,
            'audit_percentage': 0
        }
        return render_template('dashboard/index.html', **context)

@dashboard_bp.route('/alerts/mark-as-read/<int:alert_id>', methods=['POST'])
@login_required
def mark_alert_as_read(alert_id):
    """Marcar alerta como leída"""
    alert = Alert.query.get_or_404(alert_id)
    alert.is_read = True
    db.session.commit()
    return jsonify({'success': True})

# ============ CERTIFICACIONES ============
@certifications_bp.route('/')
@login_required
def list_certifications():
    """Listar todas las certificaciones"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    
    query = Certification.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    certifications = query.paginate(page=page, per_page=10)
    
    # Actualizar estados
    for cert in certifications.items:
        cert.get_status()
    
    return render_template('certifications/list.html', certifications=certifications, status_filter=status_filter)

@certifications_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_certification():
    """Crear nueva certificación"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            norm = request.form.get('norm')
            issuing_entity = request.form.get('issuing_entity')
            emission_date = datetime.strptime(request.form.get('emission_date'), '%Y-%m-%d').date()
            expiration_date = datetime.strptime(request.form.get('expiration_date'), '%Y-%m-%d').date()
            responsible_id = request.form.get('responsible_id', current_user.id)
            notes = request.form.get('notes', '')
            
            # Validaciones
            if not all([name, norm, issuing_entity, emission_date, expiration_date]):
                flash('Todos los campos son obligatorios.', 'danger')
                return redirect(url_for('certifications.new_certification'))
            
            if expiration_date <= emission_date:
                flash('La fecha de vencimiento debe ser posterior a la de emisión.', 'danger')
                return redirect(url_for('certifications.new_certification'))
            
            # Guardar documento si se adjuntó
            document_path = None
            if 'document' in request.files:
                file = request.files['document']
                if file and allowed_file(file.filename):
                    document_path = save_upload_file(file, 'certifications')
            
            certification = Certification(
                name=name,
                norm=norm,
                issuing_entity=issuing_entity,
                emission_date=emission_date,
                expiration_date=expiration_date,
                responsible_id=responsible_id,
                document_path=document_path,
                notes=notes
            )
            
            certification.get_status()
            db.session.add(certification)
            
            # Audit log
            log_entry = AuditLog(
                user_id=current_user.id,
                action='create',
                entity_type='certification',
                entity_id=certification.id if certification.id else 'new',
                ip_address=request.remote_addr
            )
            db.session.add(log_entry)
            db.session.commit()
            
            flash(f'Certificación "{name}" registrada exitosamente.', 'success')
            return redirect(url_for('certifications.list_certifications'))
        
        except Exception as e:
            flash(f'Error al registrar la certificación: {str(e)}', 'danger')
            return redirect(url_for('certifications.new_certification'))
    
    users = User.query.filter_by(is_active=True).all()
    return render_template('certifications/new.html', users=users)

@certifications_bp.route('/<int:cert_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_certification(cert_id):
    """Editar certificación"""
    from app.utils import log_action, get_entity_changes
    
    certification = Certification.query.get_or_404(cert_id)
    
    if request.method == 'POST':
        try:
            # Capturar datos originales para comparar
            original_data = {
                'name': certification.name,
                'norm': certification.norm,
                'issuing_entity': certification.issuing_entity,
                'emission_date': certification.emission_date,
                'expiration_date': certification.expiration_date,
                'responsible_id': certification.responsible_id,
                'notes': certification.notes
            }
            
            # Actualizar datos
            new_data = {
                'name': request.form.get('name'),
                'norm': request.form.get('norm'),
                'issuing_entity': request.form.get('issuing_entity'),
                'emission_date': datetime.strptime(request.form.get('emission_date'), '%Y-%m-%d').date(),
                'expiration_date': datetime.strptime(request.form.get('expiration_date'), '%Y-%m-%d').date(),
                'responsible_id': request.form.get('responsible_id'),
                'notes': request.form.get('notes', '')
            }
            
            # Aplicar cambios
            certification.name = new_data['name']
            certification.norm = new_data['norm']
            certification.issuing_entity = new_data['issuing_entity']
            certification.emission_date = new_data['emission_date']
            certification.expiration_date = new_data['expiration_date']
            certification.responsible_id = new_data['responsible_id']
            certification.notes = new_data['notes']
            
            # Guardar nuevo documento si se adjuntó
            if 'document' in request.files:
                file = request.files['document']
                if file and allowed_file(file.filename):
                    certification.document_path = save_upload_file(file, 'certifications')
            
            certification.get_status()
            certification.updated_at = datetime.now()
            
            # Detectar cambios para audit log
            changes = get_entity_changes(
                Certification.query.get(cert_id),
                new_data,
                ['name', 'norm', 'issuing_entity', 'emission_date', 'expiration_date', 'notes']
            )
            
            # Audit log con cambios específicos
            log_action(
                user_id=current_user.id,
                action='update',
                entity_type='certification',
                entity_id=cert_id,
                changes=changes,
                ip_address=request.remote_addr
            )
            
            db.session.commit()
            
            flash('Certificación actualizada exitosamente.', 'success')
            return redirect(url_for('certifications.list_certifications'))
        
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    users = User.query.filter_by(is_active=True).all()
    return render_template('certifications/edit.html', certification=certification, users=users)

@certifications_bp.route('/<int:cert_id>/delete', methods=['POST'])
@login_required
def delete_certification(cert_id):
    """Eliminar certificación"""
    certification = Certification.query.get_or_404(cert_id)
    
    if current_user.role != UserRole.ADMINISTRADOR.value:
        flash('No tienes permiso para eliminar certificaciones.', 'danger')
        return redirect(url_for('certifications.list_certifications'))
    
    try:
        # Eliminar archivo si existe
        if certification.document_path and os.path.exists(certification.document_path):
            os.remove(certification.document_path)
        
        db.session.delete(certification)
        
        # Audit log
        log_entry = AuditLog(
            user_id=current_user.id,
            action='delete',
            entity_type='certification',
            entity_id=cert_id,
            ip_address=request.remote_addr
        )
        db.session.add(log_entry)
        db.session.commit()
        
        flash('Certificación eliminada exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar: {str(e)}', 'danger')
    
    return redirect(url_for('certifications.list_certifications'))

# ============ AUDITORÍAS ============
@audits_bp.route('/')
@login_required
def list_audits():
    """Listar auditorías"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    type_filter = request.args.get('type', 'all')
    
    query = Audit.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    if type_filter != 'all':
        query = query.filter_by(audit_type=type_filter)
    
    audits = query.order_by(Audit.scheduled_date.desc()).paginate(page=page, per_page=10)
    
    return render_template('audits/list.html', audits=audits, status_filter=status_filter, type_filter=type_filter)

@audits_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_audit():
    """Crear nueva auditoría"""
    if request.method == 'POST':
        try:
            audit_type = request.form.get('audit_type')
            scheduled_date = datetime.strptime(request.form.get('scheduled_date'), '%Y-%m-%d').date()
            evaluated_area = request.form.get('evaluated_area')
            responsible_id = request.form.get('responsible_id', current_user.id)
            description = request.form.get('description', '')
            
            if not all([audit_type, scheduled_date, evaluated_area]):
                flash('Todos los campos son obligatorios.', 'danger')
                return redirect(url_for('audits.new_audit'))
            
            audit = Audit(
                audit_type=audit_type,
                scheduled_date=scheduled_date,
                evaluated_area=evaluated_area,
                responsible_id=responsible_id,
                description=description,
                status='programada'
            )
            
            db.session.add(audit)
            db.session.flush()
            
            # Audit log
            log_entry = AuditLog(
                user_id=current_user.id,
                action='create',
                entity_type='audit',
                entity_id=audit.id,
                ip_address=request.remote_addr
            )
            db.session.add(log_entry)
            db.session.commit()
            
            flash('Auditoría programada exitosamente.', 'success')
            return redirect(url_for('audits.list_audits'))
        
        except Exception as e:
            flash(f'Error al programar auditoría: {str(e)}', 'danger')
    
    users = User.query.filter_by(is_active=True).all()
    return render_template('audits/new.html', users=users)

@audits_bp.route('/<int:audit_id>/view')
@login_required
def view_audit(audit_id):
    """Ver detalles de auditoría"""
    audit = Audit.query.get_or_404(audit_id)
    findings = audit.findings.all()
    today = datetime.now().date()
    
    return render_template('audits/view.html', audit=audit, findings=findings, today=today)

@audits_bp.route('/<int:audit_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_audit(audit_id):
    """Editar auditoría"""
    audit = Audit.query.get_or_404(audit_id)
    
    if request.method == 'POST':
        try:
            audit.scheduled_date = datetime.strptime(request.form.get('scheduled_date'), '%Y-%m-%d').date()
            if request.form.get('executed_date'):
                audit.executed_date = datetime.strptime(request.form.get('executed_date'), '%Y-%m-%d').date()
            audit.evaluated_area = request.form.get('evaluated_area')
            audit.responsible_id = request.form.get('responsible_id')
            audit.description = request.form.get('description', '')
            audit.status = request.form.get('status', 'programada')
            
            # Audit log
            log_entry = AuditLog(
                user_id=current_user.id,
                action='update',
                entity_type='audit',
                entity_id=audit_id,
                ip_address=request.remote_addr
            )
            db.session.add(log_entry)
            db.session.commit()
            
            flash('Auditoría actualizada exitosamente.', 'success')
            return redirect(url_for('audits.view_audit', audit_id=audit_id))
        
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    users = User.query.filter_by(is_active=True).all()
    return render_template('audits/edit.html', audit=audit, users=users)

@audits_bp.route('/<int:audit_id>/findings/new', methods=['GET', 'POST'])
@login_required
def new_finding(audit_id):
    """Agregar hallazgo a auditoría"""
    audit = Audit.query.get_or_404(audit_id)
    
    if request.method == 'POST':
        try:
            description = request.form.get('description')
            severity = request.form.get('severity')
            corrective_action = request.form.get('corrective_action')
            responsible = request.form.get('responsible')
            deadline = request.form.get('deadline')
            
            if not description:
                flash('La descripción del hallazgo es obligatoria.', 'danger')
                return redirect(url_for('audits.new_finding', audit_id=audit_id))
            
            finding = AuditFinding(
                audit_id=audit_id,
                description=description,
                severity=severity,
                corrective_action=corrective_action,
                responsible=responsible,
                deadline=datetime.strptime(deadline, '%Y-%m-%d').date() if deadline else None,
                status='abierto'
            )
            
            db.session.add(finding)
            db.session.commit()
            
            flash('Hallazgo registrado exitosamente.', 'success')
            return redirect(url_for('audits.view_audit', audit_id=audit_id))
        
        except Exception as e:
            flash(f'Error al registrar hallazgo: {str(e)}', 'danger')
    
    return render_template('audits/new_finding.html', audit=audit)

@audits_bp.route('/<int:audit_id>/findings/<int:finding_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_finding(audit_id, finding_id):
    """Editar hallazgo de auditoría"""
    audit = Audit.query.get_or_404(audit_id)
    finding = AuditFinding.query.get_or_404(finding_id)
    
    if finding.audit_id != audit_id:
        flash('Hallazgo no pertenece a esta auditoría.', 'danger')
        return redirect(url_for('audits.view_audit', audit_id=audit_id))
    
    if request.method == 'POST':
        try:
            finding.description = request.form.get('description')
            finding.severity = request.form.get('severity')
            finding.corrective_action = request.form.get('corrective_action')
            finding.responsible = request.form.get('responsible')
            finding.status = request.form.get('status')
            finding.notes = request.form.get('notes', '')
            
            deadline = request.form.get('deadline')
            finding.deadline = datetime.strptime(deadline, '%Y-%m-%d').date() if deadline else None
            
            db.session.commit()
            
            flash('Hallazgo actualizado exitosamente.', 'success')
            return redirect(url_for('audits.view_audit', audit_id=audit_id))
        
        except Exception as e:
            flash(f'Error al actualizar hallazgo: {str(e)}', 'danger')
    
    return render_template('audits/edit_finding.html', audit=audit, finding=finding)

@audits_bp.route('/<int:audit_id>/findings/<int:finding_id>/close', methods=['POST'])
@login_required
def close_finding(audit_id, finding_id):
    """Cerrar/Resolver un hallazgo"""
    audit = Audit.query.get_or_404(audit_id)
    finding = AuditFinding.query.get_or_404(finding_id)
    
    if finding.audit_id != audit_id:
        flash('Hallazgo no pertenece a esta auditoría.', 'danger')
        return redirect(url_for('audits.view_audit', audit_id=audit_id))
    
    try:
        finding.status = 'cerrado'
        finding.notes = request.form.get('closure_notes', '')
        
        db.session.commit()
        
        # Registrar en audit log
        log_entry = AuditLog(
            user_id=current_user.id,
            action='close_finding',
            entity_type='audit_finding',
            entity_id=finding_id,
            ip_address=request.remote_addr
        )
        db.session.add(log_entry)
        db.session.commit()
        
        flash('Hallazgo cerrado exitosamente.', 'success')
    
    except Exception as e:
        flash(f'Error al cerrar hallazgo: {str(e)}', 'danger')
    
    return redirect(url_for('audits.view_audit', audit_id=audit_id))

@audits_bp.route('/<int:audit_id>/findings/<int:finding_id>/reopen', methods=['POST'])
@login_required
def reopen_finding(audit_id, finding_id):
    """Reabrir un hallazgo cerrado"""
    audit = Audit.query.get_or_404(audit_id)
    finding = AuditFinding.query.get_or_404(finding_id)
    
    if finding.audit_id != audit_id:
        flash('Hallazgo no pertenece a esta auditoría.', 'danger')
        return redirect(url_for('audits.view_audit', audit_id=audit_id))
    
    try:
        finding.status = 'abierto'
        
        db.session.commit()
        
        # Registrar en audit log
        log_entry = AuditLog(
            user_id=current_user.id,
            action='reopen_finding',
            entity_type='audit_finding',
            entity_id=finding_id,
            ip_address=request.remote_addr
        )
        db.session.add(log_entry)
        db.session.commit()
        
        flash('Hallazgo reabierto exitosamente.', 'info')
    
    except Exception as e:
        flash(f'Error al reabrir hallazgo: {str(e)}', 'danger')
    
    return redirect(url_for('audits.view_audit', audit_id=audit_id))

@audits_bp.route('/<int:audit_id>/findings/<int:finding_id>/delete', methods=['POST'])
@login_required
def delete_finding(audit_id, finding_id):
    """Eliminar un hallazgo"""
    audit = Audit.query.get_or_404(audit_id)
    finding = AuditFinding.query.get_or_404(finding_id)
    
    if finding.audit_id != audit_id:
        flash('Hallazgo no pertenece a esta auditoría.', 'danger')
        return redirect(url_for('audits.view_audit', audit_id=audit_id))
    
    try:
        db.session.delete(finding)
        db.session.commit()
        
        flash('Hallazgo eliminado exitosamente.', 'success')
    
    except Exception as e:
        flash(f'Error al eliminar hallazgo: {str(e)}', 'danger')
    
    return redirect(url_for('audits.view_audit', audit_id=audit_id))

# ============ POLÍTICAS ============
@policies_bp.route('/')
@login_required
def list_policies():
    """Listar políticas"""
    page = request.args.get('page', 1, type=int)
    policies = Policy.query.filter_by(is_active=True).paginate(page=page, per_page=10)
    
    return render_template('policies/list.html', policies=policies)

@policies_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_policy():
    """Crear nueva política"""
    if current_user.role != UserRole.ADMINISTRADOR.value:
        flash('Solo administradores pueden crear políticas.', 'danger')
        return redirect(url_for('policies.list_policies'))
    
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            description = request.form.get('description')
            content = request.form.get('content')
            version = request.form.get('version', '1.0')
            effective_date = datetime.strptime(request.form.get('effective_date'), '%Y-%m-%d').date()
            
            if not all([title, description]):
                flash('Todos los campos son obligatorios.', 'danger')
                return redirect(url_for('policies.new_policy'))
            
            policy = Policy(
                title=title,
                description=description,
                content=content,
                version=version,
                effective_date=effective_date
            )
            
            db.session.add(policy)
            db.session.flush()
            
            # Crear confirmaciones para todos los usuarios activos
            users = User.query.filter_by(is_active=True).all()
            for user in users:
                confirmation = PolicyConfirmation(
                    policy_id=policy.id,
                    user_id=user.id
                )
                db.session.add(confirmation)
            
            # Audit log
            log_entry = AuditLog(
                user_id=current_user.id,
                action='create',
                entity_type='policy',
                entity_id=policy.id,
                ip_address=request.remote_addr
            )
            db.session.add(log_entry)
            db.session.commit()
            
            flash('Política creada exitosamente.', 'success')
            return redirect(url_for('policies.list_policies'))
        
        except Exception as e:
            flash(f'Error al crear política: {str(e)}', 'danger')
    
    return render_template('policies/new.html')

@policies_bp.route('/<int:policy_id>/view')
@login_required
def view_policy(policy_id):
    """Ver detalles de política"""
    from app.utils import log_action
    
    policy = Policy.query.get_or_404(policy_id)
    confirmations = PolicyConfirmation.query.filter_by(policy_id=policy_id).all()
    confirmed_count = sum(1 for c in confirmations if c.confirmed)
    pending_count = len(confirmations) - confirmed_count
    
    # Verificar si el usuario actual ya confirmó
    user_confirmed = False
    if current_user.is_authenticated:
        user_confirmation = PolicyConfirmation.query.filter_by(
            policy_id=policy_id,
            user_id=current_user.id
        ).first()
        user_confirmed = user_confirmation.confirmed if user_confirmation else False
    
    # Registrar que el usuario vio esta política
    log_action(
        user_id=current_user.id,
        action='view_policy',
        entity_type='policy',
        entity_id=policy_id,
        ip_address=request.remote_addr
    )
    
    # Obtener historial de cambios de esta política
    policy_history = AuditLog.query.filter_by(
        entity_type='policy',
        entity_id=policy_id
    ).order_by(AuditLog.created_at.desc()).limit(10).all()
    
    return render_template('policies/view.html', 
                         policy=policy, 
                         confirmations=confirmations, 
                         confirmed_count=confirmed_count,
                         pending_count=pending_count,
                         user_confirmed=user_confirmed,
                         policy_history=policy_history)

@policies_bp.route('/<int:policy_id>/confirm', methods=['POST'])
@login_required
def confirm_policy(policy_id):
    """Confirmar cumplimiento de política"""
    policy = Policy.query.get_or_404(policy_id)
    
    confirmation = PolicyConfirmation.query.filter_by(
        policy_id=policy_id,
        user_id=current_user.id
    ).first()
    
    if not confirmation:
        confirmation = PolicyConfirmation(
            policy_id=policy_id,
            user_id=current_user.id
        )
        db.session.add(confirmation)
    
    confirmation.mark_confirmed(ip_address=request.remote_addr)
    
    # Audit log
    log_entry = AuditLog(
        user_id=current_user.id,
        action='confirm_policy',
        entity_type='policy_confirmation',
        entity_id=policy_id,
        ip_address=request.remote_addr
    )
    db.session.add(log_entry)
    db.session.commit()
    
    flash('Política confirmada exitosamente.', 'success')
    return redirect(url_for('policies.view_policy', policy_id=policy_id))

@policies_bp.route('/<int:policy_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_policy(policy_id):
    """Editar política existente"""
    from app.utils import log_action, get_entity_changes
    
    if current_user.role != UserRole.ADMINISTRADOR.value:
        flash('Solo administradores pueden editar políticas.', 'danger')
        return redirect(url_for('policies.list_policies'))
    
    policy = Policy.query.get_or_404(policy_id)
    
    if request.method == 'POST':
        try:
            # Capturar datos originales
            original_data = {
                'title': policy.title,
                'description': policy.description,
                'content': policy.content,
                'version': policy.version,
                'effective_date': policy.effective_date,
                'requires_confirmation': policy.requires_confirmation,
                'is_active': policy.is_active
            }
            
            # Nuevos datos
            new_data = {
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'content': request.form.get('content'),
                'version': request.form.get('version', policy.version),
                'effective_date': datetime.strptime(request.form.get('effective_date'), '%Y-%m-%d').date(),
                'requires_confirmation': 'requires_confirmation' in request.form,
                'is_active': 'is_active' in request.form
            }
            
            if not all([new_data['title'], new_data['description']]):
                flash('El título y descripción son obligatorios.', 'danger')
                return redirect(url_for('policies.edit_policy', policy_id=policy_id))
            
            # Aplicar cambios
            policy.title = new_data['title']
            policy.description = new_data['description']
            policy.content = new_data['content']
            policy.version = new_data['version']
            policy.effective_date = new_data['effective_date']
            policy.requires_confirmation = new_data['requires_confirmation']
            policy.is_active = new_data['is_active']
            policy.updated_at = datetime.now()
            
            # Detectar cambios para audit log
            changes = get_entity_changes(
                Policy.query.get(policy_id),
                new_data,
                ['title', 'description', 'version', 'effective_date']
            )
            
            # Audit log
            log_action(
                user_id=current_user.id,
                action='update',
                entity_type='policy',
                entity_id=policy_id,
                changes=changes,
                ip_address=request.remote_addr
            )
            
            db.session.commit()
            
            flash('Política actualizada exitosamente.', 'success')
            return redirect(url_for('policies.view_policy', policy_id=policy_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar política: {str(e)}', 'danger')
    
    return render_template('policies/edit.html', policy=policy)

@policies_bp.route('/<int:policy_id>/delete', methods=['POST'])
@login_required
def delete_policy(policy_id):
    """Eliminar política"""
    from app.utils import log_action
    
    if current_user.role != UserRole.ADMINISTRADOR.value:
        flash('Solo administradores pueden eliminar políticas.', 'danger')
        return redirect(url_for('policies.list_policies'))
    
    policy = Policy.query.get_or_404(policy_id)
    policy_title = policy.title
    
    try:
        # Audit log antes de eliminar
        log_action(
            user_id=current_user.id,
            action='delete',
            entity_type='policy',
            entity_id=policy_id,
            changes={'title': policy_title},
            ip_address=request.remote_addr
        )
        
        db.session.delete(policy)
        db.session.commit()
        
        flash(f'Política "{policy_title}" eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar política: {str(e)}', 'danger')
    
    return redirect(url_for('policies.list_policies'))

# ============ REPORTES ============
@reports_bp.route('/')
@login_required
def index():
    """Panel de reportes"""
    return render_template('reports/index.html')

@reports_bp.route('/certifications')
@login_required
def certifications_report():
    """Reporte de certificaciones"""
    certifications = Certification.query.all()
    for cert in certifications:
        cert.get_status()
    
    return render_template('reports/certifications.html', certifications=certifications)

@reports_bp.route('/certifications/export/<format>')
@login_required
def export_certifications(format):
    """Exportar reporte de certificaciones"""
    certifications = Certification.query.all()
    
    if format == 'pdf':
        file_path = generate_pdf_report('certifications', certifications)
    elif format == 'excel':
        file_path = generate_excel_report('certifications', certifications)
    else:
        flash('Formato no válido.', 'danger')
        return redirect(url_for('reports.certifications_report'))
    
    return send_file(file_path, as_attachment=True)

@reports_bp.route('/audits')
@login_required
def audits_report():
    """Reporte de auditorías"""
    audits = Audit.query.all()
    
    return render_template('reports/audits.html', audits=audits)

@reports_bp.route('/policies')
@login_required
def policies_report():
    """Reporte de políticas y confirmaciones"""
    policies = Policy.query.filter_by(is_active=True).all()
    
    policy_data = []
    for policy in policies:
        total_confirmations = PolicyConfirmation.query.filter_by(policy_id=policy.id).count()
        confirmed = PolicyConfirmation.query.filter_by(policy_id=policy.id, confirmed=True).count()
        percentage = int((confirmed / total_confirmations * 100) if total_confirmations > 0 else 0)
        
        policy_data.append({
            'policy': policy,
            'total_confirmations': total_confirmations,
            'confirmed': confirmed,
            'percentage': percentage
        })
    
    return render_template('reports/policies.html', policy_data=policy_data)

# ============ ADMINISTRACIÓN ============
@admin_bp.route('/users')
@login_required
def list_users():
    """Listar usuarios (solo administrador)"""
    from app.models import Role
    
    if current_user.role != UserRole.ADMINISTRADOR.value:
        flash('No tienes permiso para acceder a esta sección.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    # Parámetros de filtro
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', None)
    status_filter = request.args.get('status', None)
    search = request.args.get('search', None)
    
    # Query base
    query = User.query
    
    # Aplicar filtros
    if role_filter:
        query = query.filter_by(role=role_filter)
    
    if status_filter == 'active':
        query = query.filter_by(is_active=True)
    elif status_filter == 'inactive':
        query = query.filter_by(is_active=False)
    
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            db.or_(
                User.username.ilike(search_term),
                User.full_name.ilike(search_term),
                User.email.ilike(search_term),
                User.department.ilike(search_term)
            )
        )
    
    # Ordenar por rol y nombre
    users = query.order_by(User.role, User.full_name).paginate(page=page, per_page=20, error_out=False)
    
    # Estadísticas
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    inactive_users = User.query.filter_by(is_active=False).count()
    
    # Usuarios por rol
    users_by_role = db.session.query(
        User.role, 
        db.func.count(User.id)
    ).group_by(User.role).all()
    
    # Obtener todos los roles disponibles
    all_roles = Role.query.order_by(Role.id).all()
    
    return render_template('admin/users.html', 
                         users=users,
                         total_users=total_users,
                         active_users=active_users,
                         inactive_users=inactive_users,
                         users_by_role=users_by_role,
                         all_roles=all_roles,
                         current_role_filter=role_filter,
                         current_status_filter=status_filter,
                         current_search=search)

@admin_bp.route('/users/new', methods=['GET', 'POST'])
@login_required
def new_user():
    """Crear nuevo usuario"""
    if current_user.role != UserRole.ADMINISTRADOR.value:
        flash('No tienes permiso para crear usuarios.', 'danger')
        return redirect(url_for('admin.list_users'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            full_name = request.form.get('full_name')
            department = request.form.get('department')
            role = request.form.get('role', UserRole.USUARIO.value)
            
            if not all([username, email, password, full_name]):
                flash('Todos los campos son obligatorios.', 'danger')
                return redirect(url_for('admin.new_user'))
            
            if User.query.filter_by(username=username).first():
                flash('El nombre de usuario ya existe.', 'danger')
                return redirect(url_for('admin.new_user'))
            
            if User.query.filter_by(email=email).first():
                flash('El email ya existe.', 'danger')
                return redirect(url_for('admin.new_user'))
            
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                department=department,
                role=role
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.flush()
            
            # Audit log
            log_entry = AuditLog(
                user_id=current_user.id,
                action='create_user',
                entity_type='user',
                entity_id=user.id,
                ip_address=request.remote_addr
            )
            db.session.add(log_entry)
            db.session.commit()
            
            flash('Usuario creado exitosamente.', 'success')
            return redirect(url_for('admin.list_users'))
        
        except Exception as e:
            flash(f'Error al crear usuario: {str(e)}', 'danger')
    
    return render_template('admin/new_user.html')

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Editar usuario"""
    if current_user.role != UserRole.ADMINISTRADOR.value:
        flash('No tienes permiso para editar usuarios.', 'danger')
        return redirect(url_for('admin.list_users'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            user.full_name = request.form.get('full_name')
            user.email = request.form.get('email')
            user.department = request.form.get('department')
            user.role = request.form.get('role')
            user.is_active = request.form.get('is_active') == 'on'
            
            if request.form.get('password'):
                user.set_password(request.form.get('password'))
            
            # Audit log
            log_entry = AuditLog(
                user_id=current_user.id,
                action='update_user',
                entity_type='user',
                entity_id=user_id,
                ip_address=request.remote_addr
            )
            db.session.add(log_entry)
            db.session.commit()
            
            flash('Usuario actualizado exitosamente.', 'success')
            return redirect(url_for('admin.list_users'))
        
        except Exception as e:
            flash(f'Error al actualizar usuario: {str(e)}', 'danger')
    
    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    """Activar/Desactivar usuario"""
    import json
    
    if current_user.role != UserRole.ADMINISTRADOR.value:
        return jsonify({'success': False, 'message': 'No autorizado'}), 403
    
    try:
        user = User.query.get_or_404(user_id)
        
        # No permitir que el admin se desactive a sí mismo
        if user.id == current_user.id:
            return jsonify({
                'success': False, 
                'message': 'No puedes desactivar tu propia cuenta'
            }), 400
        
        # Cambiar estado
        old_status = user.is_active
        user.is_active = not user.is_active
        
        # Registrar en audit log
        from app.utils import log_action
        log_action(
            user_id=current_user.id,
            action='toggle_user_status',
            entity_type='user',
            entity_id=user.id,
            changes=json.dumps({
                'username': user.username,
                'old_status': 'active' if old_status else 'inactive',
                'new_status': 'active' if user.is_active else 'inactive'
            }),
            ip_address=request.remote_addr
        )
        
        db.session.commit()
        
        status_text = 'activado' if user.is_active else 'desactivado'
        return jsonify({
            'success': True,
            'message': f'Usuario {status_text} correctamente',
            'is_active': user.is_active
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@admin_bp.route('/audit-log')
@login_required
def audit_log():
    """Ver registro de auditoría del sistema"""
    from datetime import date, timedelta
    from sqlalchemy import func
    
    if current_user.role != UserRole.ADMINISTRADOR.value:
        flash('No tienes permiso para acceder a esta sección.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    # Parámetros de filtro
    page = request.args.get('page', 1, type=int)
    user_id = request.args.get('user_id', type=int)
    action = request.args.get('action', type=str)
    entity_type = request.args.get('entity_type', type=str)
    date_from = request.args.get('date_from', type=str)
    
    # Query base
    query = AuditLog.query
    
    # Aplicar filtros
    if user_id:
        query = query.filter_by(user_id=user_id)
    if action:
        query = query.filter_by(action=action)
    if entity_type:
        query = query.filter_by(entity_type=entity_type)
    if date_from:
        try:
            from datetime import datetime
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(AuditLog.created_at >= date_from_obj)
        except:
            pass
    
    # Ordenar y paginar
    logs = query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    
    # Estadísticas
    total_logs = AuditLog.query.count()
    logs_today = AuditLog.query.filter(
        func.date(AuditLog.created_at) == date.today()
    ).count()
    active_users = User.query.filter_by(is_active=True).count()
    actions_count = db.session.query(func.count(func.distinct(AuditLog.action))).scalar()
    
    # Obtener todos los usuarios para el filtro
    users = User.query.filter_by(is_active=True).order_by(User.full_name).all()
    
    return render_template('admin/audit_log.html', 
                         logs=logs,
                         total_logs=total_logs,
                         logs_today=logs_today,
                         active_users=active_users,
                         actions_count=actions_count,
                         users=users)

@admin_bp.route('/permissions')
@login_required
def permissions():
    """Gestión de permisos por rol"""
    from app.models import Role, Module, RolePermission
    
    if current_user.role != UserRole.ADMINISTRADOR.value:
        flash('No tienes permiso para acceder a esta sección.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    # Obtener todos los roles y módulos
    roles = Role.query.order_by(Role.id).all()
    modules = Module.query.filter_by(is_active=True).order_by(Module.display_order).all()
    
    # Construir matriz de permisos
    permissions_matrix = {}
    for role in roles:
        permissions_matrix[role.id] = {}
        for module in modules:
            # Buscar permiso existente
            perm = RolePermission.query.filter_by(
                role_id=role.id, 
                module_id=module.id
            ).first()
            
            if perm:
                permissions_matrix[role.id][module.id] = {
                    'id': perm.id,
                    'can_view': perm.can_view,
                    'can_create': perm.can_create,
                    'can_edit': perm.can_edit,
                    'can_delete': perm.can_delete,
                    'can_export': perm.can_export,
                    'can_approve': perm.can_approve
                }
            else:
                # No existe permiso, todos en False
                permissions_matrix[role.id][module.id] = {
                    'id': None,
                    'can_view': False,
                    'can_create': False,
                    'can_edit': False,
                    'can_delete': False,
                    'can_export': False,
                    'can_approve': False
                }
    
    return render_template('admin/permissions.html',
                         roles=roles,
                         modules=modules,
                         permissions_matrix=permissions_matrix)

@admin_bp.route('/permissions/update', methods=['POST'])
@login_required
def update_permission():
    """Actualizar un permiso específico"""
    from app.models import RolePermission
    import json
    
    if current_user.role != UserRole.ADMINISTRADOR.value:
        return jsonify({'success': False, 'message': 'No autorizado'}), 403
    
    try:
        data = request.get_json()
        role_id = data.get('role_id')
        module_id = data.get('module_id')
        permission_type = data.get('permission_type')
        value = data.get('value', False)
        
        # Buscar o crear permiso
        perm = RolePermission.query.filter_by(
            role_id=role_id,
            module_id=module_id
        ).first()
        
        if not perm:
            # Crear nuevo registro
            perm = RolePermission(
                role_id=role_id,
                module_id=module_id,
                can_view=False,
                can_create=False,
                can_edit=False,
                can_delete=False,
                can_export=False,
                can_approve=False
            )
            db.session.add(perm)
        
        # Actualizar el permiso específico
        if permission_type == 'can_view':
            perm.can_view = value
        elif permission_type == 'can_create':
            perm.can_create = value
        elif permission_type == 'can_edit':
            perm.can_edit = value
        elif permission_type == 'can_delete':
            perm.can_delete = value
        elif permission_type == 'can_export':
            perm.can_export = value
        elif permission_type == 'can_approve':
            perm.can_approve = value
        
        db.session.commit()
        
        # Registrar en audit log
        from app.utils import log_action
        log_action(
            user_id=current_user.id,
            action='update_permission',
            entity_type='role_permission',
            entity_id=perm.id,
            changes=json.dumps({
                'role_id': role_id,
                'module_id': module_id,
                permission_type: value
            }),
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'success': True, 
            'message': 'Permiso actualizado correctamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False, 
            'message': f'Error al actualizar permiso: {str(e)}'
        }), 500

# ============ API DE PRUEBA ============
@api_bp.route('/test-db', methods=['GET'])
def test_db_connection():
    """Endpoint de prueba para verificar conexión y permisos de BD"""
    try:
        # Probar conexión básica
        db.engine.connect()
        
        # Probar SELECT
        user_count = User.query.count()
        
        # Intentar obtener usuarios
        users = User.query.limit(5).all()
        
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        
        return jsonify({
            'success': True,
            'message': 'Conexión exitosa y permisos funcionando',
            'database': {
                'host': current_app.config.get('DB_HOST'),
                'port': current_app.config.get('DB_PORT'),
                'database': current_app.config.get('DB_NAME'),
                'engine': current_app.config.get('DB_ENGINE')
            },
            'users': {
                'total': user_count,
                'sample': users_data
            }
        }), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        
        return jsonify({
            'success': False,
            'message': 'Error al acceder a la base de datos',
            'error': str(e),
            'error_type': type(e).__name__,
            'trace': error_trace,
            'database': {
                'host': current_app.config.get('DB_HOST'),
                'port': current_app.config.get('DB_PORT'),
                'database': current_app.config.get('DB_NAME'),
                'engine': current_app.config.get('DB_ENGINE')
            }
        }), 500

@api_bp.route('/test-login', methods=['POST'])
def test_login():
    """Endpoint para probar login sin interfaz"""
    try:
        data = request.get_json() or {}
        username = data.get('username', 'admin')
        password = data.get('password', 'admin123')
        
        # Buscar usuario
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({
                'success': False,
                'message': f'Usuario "{username}" no encontrado',
                'step': 'user_lookup'
            }), 404
        
        # Verificar contraseña
        password_ok = user.check_password(password)
        
        # Verificar activo
        is_active = user.is_active
        
        return jsonify({
            'success': password_ok and is_active,
            'message': 'Login correcto' if (password_ok and is_active) else 'Login fallido',
            'details': {
                'user_found': True,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'role': user.role,
                'is_active': is_active,
                'password_correct': password_ok
            }
        }), 200 if (password_ok and is_active) else 401
        
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'message': 'Error al probar login',
            'error': str(e),
            'error_type': type(e).__name__,
            'trace': traceback.format_exc()
        }), 500

@api_bp.route('/create-admin', methods=['POST'])
def create_admin_user():
    """Endpoint para crear usuario admin si no existe"""
    try:
        # Verificar si ya existe
        existing = User.query.filter_by(username='admin').first()
        
        if existing:
            return jsonify({
                'success': False,
                'message': 'Usuario admin ya existe',
                'user': {
                    'username': existing.username,
                    'email': existing.email,
                    'is_active': existing.is_active
                }
            }), 400
        
        # Crear admin
        admin = User(
            username='admin',
            email='admin@frutosoro.com',
            full_name='Administrador Sistema',
            department='Dirección',
            role='administrador',
            is_active=True
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario admin creado exitosamente',
            'credentials': {
                'username': 'admin',
                'password': 'admin123',
                'warning': 'Cambia esta contraseña después del primer login'
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        import traceback
        return jsonify({
            'success': False,
            'message': 'Error al crear usuario admin',
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500
