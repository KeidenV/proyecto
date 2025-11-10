from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Usuario, Rol, Actividad, Entrenamiento, Asistencia, Competicion, ResultadoCompeticion
from forms import UsuarioForm, ActividadForm, EntrenamientoForm, CompeticionForm, AsistenciaForm
from datetime import datetime, date

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'rol') or current_user.rol.nombre_rol != 'Administrador':
            flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Estadísticas básicas
    stats = {
        'total_usuarios': Usuario.query.count(),
        'total_entrenadores': Usuario.query.join(Rol).filter(Rol.nombre_rol == 'Entrenador').count(),
        'total_miembros': Usuario.query.join(Rol).filter(Rol.nombre_rol == 'Miembro').count(),
        'total_entrenamientos': Entrenamiento.query.count(),
        'total_competiciones': Competicion.query.count()
    }
    
    # Usuarios recientes
    recent_usuarios = Usuario.query.order_by(Usuario.id_usuario.desc()).limit(5).all()
    
    # Próximas competiciones
    upcoming_competiciones = Competicion.query.filter(
        Competicion.fecha >= date.today()
    ).order_by(Competicion.fecha).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_usuarios=recent_usuarios, 
                         upcoming_competiciones=upcoming_competiciones)

# Gestión de Usuarios
@admin_bp.route('/usuarios')
@login_required
@admin_required
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/usuarios/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_usuario():
    form = UsuarioForm()
    
    if form.validate_on_submit():
        try:
            usuario = Usuario(
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                email=form.email.data,
                fecha_nacimiento=form.fecha_nacimiento.data,
                id_rol=form.id_rol.data
            )
            usuario.set_password('password123')  # Contraseña temporal
            
            db.session.add(usuario)
            db.session.commit()
            flash('Usuario agregado exitosamente', 'success')
            return redirect(url_for('admin.usuarios'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear usuario', 'error')
    
    return render_template('admin/add_usuario.html', form=form)

@admin_bp.route('/usuarios/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(usuario)
            db.session.commit()
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('admin.usuarios'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar usuario', 'error')
    
    return render_template('admin/edit_usuario.html', form=form, usuario=usuario)

@admin_bp.route('/usuarios/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado exitosamente', 'success')
    return redirect(url_for('admin.usuarios'))

# Gestión de Actividades
@admin_bp.route('/actividades')
@login_required
@admin_required
def actividades():
    actividades = Actividad.query.order_by(Actividad.nombre_actividad).all()
    return render_template('admin/actividades.html', actividades=actividades)

@admin_bp.route('/actividades/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_actividad():
    form = ActividadForm()
    
    if form.validate_on_submit():
        try:
            actividad = Actividad(nombre_actividad=form.nombre_actividad.data)
            db.session.add(actividad)
            db.session.commit()
            flash('Actividad agregada exitosamente', 'success')
            return redirect(url_for('admin.actividades'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear actividad', 'error')
    
    return render_template('admin/add_actividad.html', form=form)

@admin_bp.route('/actividades/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_actividad(id):
    actividad = Actividad.query.get_or_404(id)
    form = ActividadForm(obj=actividad)
    
    if form.validate_on_submit():
        actividad.nombre_actividad = form.nombre_actividad.data
        db.session.commit()
        flash('Actividad actualizada exitosamente', 'success')
        return redirect(url_for('admin.actividades'))
    
    return render_template('admin/edit_actividad.html', form=form, actividad=actividad)

@admin_bp.route('/actividades/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_actividad(id):
    actividad = Actividad.query.get_or_404(id)
    db.session.delete(actividad)
    db.session.commit()
    flash('Actividad eliminada exitosamente', 'success')
    return redirect(url_for('admin.actividades'))

# Gestión de Entrenamientos
@admin_bp.route('/entrenamientos')
@login_required
@admin_required
def entrenamientos():
    entrenamientos = Entrenamiento.query.join(Usuario, Entrenamiento.id_entrenador == Usuario.id_usuario)\
        .join(Actividad, Entrenamiento.id_actividad == Actividad.id_actividad)\
        .order_by(Entrenamiento.fecha.desc()).all()
    return render_template('admin/entrenamientos.html', entrenamientos=entrenamientos)

@admin_bp.route('/entrenamientos/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_entrenamiento():
    form = EntrenamientoForm()
    
    if form.validate_on_submit():
        try:
            entrenamiento = Entrenamiento(
                id_entrenador=form.id_entrenador.data,
                id_actividad=form.id_actividad.data,
                fecha=form.fecha.data
            )
            db.session.add(entrenamiento)
            db.session.commit()
            flash('Entrenamiento agregado exitosamente', 'success')
            return redirect(url_for('admin.entrenamientos'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear entrenamiento', 'error')
    
    return render_template('admin/add_entrenamiento.html', form=form)

@admin_bp.route('/entrenamientos/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_entrenamiento(id):
    entrenamiento = Entrenamiento.query.get_or_404(id)
    form = EntrenamientoForm(obj=entrenamiento)
    
    if form.validate_on_submit():
        entrenamiento.id_entrenador = form.id_entrenador.data
        entrenamiento.id_actividad = form.id_actividad.data
        entrenamiento.fecha = form.fecha.data
        db.session.commit()
        flash('Entrenamiento actualizado exitosamente', 'success')
        return redirect(url_for('admin.entrenamientos'))
    
    return render_template('admin/edit_entrenamiento.html', form=form, entrenamiento=entrenamiento)

@admin_bp.route('/entrenamientos/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_entrenamiento(id):
    entrenamiento = Entrenamiento.query.get_or_404(id)
    db.session.delete(entrenamiento)
    db.session.commit()
    flash('Entrenamiento eliminado exitosamente', 'success')
    return redirect(url_for('admin.entrenamientos'))

# Gestión de Competiciones
@admin_bp.route('/competiciones')
@login_required
@admin_required
def competiciones():
    competiciones = Competicion.query.join(Actividad, Competicion.id_actividad == Actividad.id_actividad, isouter=True)\
        .order_by(Competicion.fecha.desc()).all()
    return render_template('admin/competiciones.html', competiciones=competiciones)

@admin_bp.route('/competiciones/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_competicion():
    form = CompeticionForm()
    
    if form.validate_on_submit():
        try:
            competicion = Competicion(
                nombre=form.nombre.data,
                fecha=form.fecha.data,
                ubicacion=form.ubicacion.data,
                descripcion=form.descripcion.data,
                id_actividad=form.id_actividad.data
            )
            db.session.add(competicion)
            db.session.commit()
            flash('Competición agregada exitosamente', 'success')
            return redirect(url_for('admin.competiciones'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear competición', 'error')
    
    return render_template('admin/add_competicion.html', form=form)

@admin_bp.route('/competiciones/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_competicion(id):
    competicion = Competicion.query.get_or_404(id)
    form = CompeticionForm(obj=competicion)
    
    if form.validate_on_submit():
        competicion.nombre = form.nombre.data
        competicion.fecha = form.fecha.data
        competicion.ubicacion = form.ubicacion.data
        competicion.descripcion = form.descripcion.data
        competicion.id_actividad = form.id_actividad.data
        db.session.commit()
        flash('Competición actualizada exitosamente', 'success')
        return redirect(url_for('admin.competiciones'))
    
    return render_template('admin/edit_competicion.html', form=form, competicion=competicion)

@admin_bp.route('/competiciones/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_competicion(id):
    competicion = Competicion.query.get_or_404(id)
    db.session.delete(competicion)
    db.session.commit()
    flash('Competición eliminada exitosamente', 'success')
    return redirect(url_for('admin.competiciones'))