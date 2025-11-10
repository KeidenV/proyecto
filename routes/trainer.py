from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Usuario, Rol, Actividad, Entrenamiento, Asistencia, Competicion, ResultadoCompeticion
from forms import EntrenamientoForm, AsistenciaForm
from datetime import datetime, date, time

trainer_bp = Blueprint('trainer', __name__)

def trainer_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'rol') or current_user.rol.nombre_rol != 'Entrenador':
            flash('Acceso denegado. Se requieren permisos de entrenador.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@trainer_bp.route('/dashboard')
@login_required
@trainer_required
def dashboard():
    # Estadísticas del entrenador
    stats = {
        'total_entrenamientos': Entrenamiento.query.filter_by(id_entrenador=current_user.id_usuario).count(),
        'total_asistencias': Asistencia.query.join(Entrenamiento).filter(
            Entrenamiento.id_entrenador == current_user.id_usuario
        ).count(),
        'hoy_asistencias': Asistencia.query.join(Entrenamiento).filter(
            Entrenamiento.id_entrenador == current_user.id_usuario,
            Asistencia.id_entrenamiento == Entrenamiento.id_entrenamiento
        ).count()
    }
    
    # Entrenamientos del entrenador
    entrenamientos = Entrenamiento.query.filter_by(id_entrenador=current_user.id_usuario).all()
    
    # Asistencias recientes
    recent_asistencias = Asistencia.query.join(Entrenamiento).filter(
        Entrenamiento.id_entrenador == current_user.id_usuario
    ).order_by(Asistencia.id_asistencia.desc()).limit(10).all()
    
    return render_template('trainer/dashboard.html', 
                         stats=stats, 
                         entrenamientos=entrenamientos, 
                         recent_asistencias=recent_asistencias)

@trainer_bp.route('/entrenamientos')
@login_required
@trainer_required
def entrenamientos():
    entrenamientos = Entrenamiento.query.filter_by(id_entrenador=current_user.id_usuario).all()
    return render_template('trainer/entrenamientos.html', entrenamientos=entrenamientos)

@trainer_bp.route('/entrenamientos/add', methods=['GET', 'POST'])
@login_required
@trainer_required
def add_entrenamiento():
    form = EntrenamientoForm()
    
    if form.validate_on_submit():
        try:
            entrenamiento = Entrenamiento(
                id_entrenador=current_user.id_usuario,
                id_actividad=form.id_actividad.data,
                fecha=form.fecha.data
            )
            db.session.add(entrenamiento)
            db.session.commit()
            flash('Entrenamiento agregado exitosamente', 'success')
            return redirect(url_for('trainer.entrenamientos'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear entrenamiento', 'error')
    
    return render_template('trainer/add_entrenamiento.html', form=form)

@trainer_bp.route('/asistencias')
@login_required
@trainer_required
def asistencias():
    # Obtener asistencias de los entrenamientos del entrenador
    asistencias = Asistencia.query.join(Entrenamiento).filter(
        Entrenamiento.id_entrenador == current_user.id_usuario
    ).order_by(Asistencia.id_asistencia.desc()).all()
    
    return render_template('trainer/asistencias.html', asistencias=asistencias)

@trainer_bp.route('/asistencias/add', methods=['GET', 'POST'])
@login_required
@trainer_required
def add_asistencia():
    form = AsistenciaForm()
    
    if form.validate_on_submit():
        try:
            # Verificar que el entrenamiento pertenece al entrenador
            entrenamiento = Entrenamiento.query.filter_by(
                id_entrenamiento=form.id_entrenamiento.data,
                id_entrenador=current_user.id_usuario
            ).first()
            
            if not entrenamiento:
                flash('Entrenamiento no válido', 'error')
                return redirect(url_for('trainer.add_asistencia'))
            
            asistencia = Asistencia(
                id_entrenamiento=form.id_entrenamiento.data,
                id_miembro=form.id_miembro.data,
                presente=form.presente.data,
                observaciones=form.observaciones.data
            )
            db.session.add(asistencia)
            db.session.commit()
            flash('Asistencia registrada exitosamente', 'success')
            return redirect(url_for('trainer.asistencias'))
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar asistencia', 'error')
    
    return render_template('trainer/add_asistencia.html', form=form)

@trainer_bp.route('/miembros')
@login_required
@trainer_required
def miembros():
    # Obtener miembros (usuarios con rol de miembro)
    miembros = Usuario.query.join(Rol).filter(Rol.nombre_rol == 'Miembro').all()
    return render_template('trainer/miembros.html', miembros=miembros)