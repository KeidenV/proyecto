from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Usuario, Rol, Actividad, Entrenamiento, Asistencia, Competicion, ResultadoCompeticion
from datetime import datetime, date

member_bp = Blueprint('member', __name__)

def member_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'rol') or current_user.rol.nombre_rol != 'Miembro':
            flash('Acceso denegado. Se requieren permisos de miembro.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@member_bp.route('/dashboard')
@login_required
@member_required
def dashboard():
    # Estadísticas del miembro
    stats = {
        'total_asistencias': Asistencia.query.filter_by(id_miembro=current_user.id_usuario).count(),
        'este_mes_asistencias': Asistencia.query.filter(
            Asistencia.id_miembro == current_user.id_usuario,
            Asistencia.id_entrenamiento == Entrenamiento.id_entrenamiento
        ).count(),
        'esta_semana_asistencias': Asistencia.query.filter(
            Asistencia.id_miembro == current_user.id_usuario,
            Asistencia.id_entrenamiento == Entrenamiento.id_entrenamiento
        ).count()
    }
    
    # Asistencias recientes del miembro
    recent_asistencias = Asistencia.query.filter_by(
        id_miembro=current_user.id_usuario
    ).order_by(Asistencia.id_asistencia.desc()).limit(10).all()
    
    # Próximos entrenamientos disponibles
    available_entrenamientos = Entrenamiento.query.all()
    
    # Próximas competiciones
    upcoming_competiciones = Competicion.query.filter(
        Competicion.fecha >= date.today()
    ).order_by(Competicion.fecha).limit(5).all()
    
    return render_template('member/dashboard.html', 
                         stats=stats, 
                         recent_asistencias=recent_asistencias,
                         available_entrenamientos=available_entrenamientos,
                         upcoming_competiciones=upcoming_competiciones)

@member_bp.route('/entrenamientos')
@login_required
@member_required
def entrenamientos():
    entrenamientos = Entrenamiento.query.all()
    return render_template('member/entrenamientos.html', entrenamientos=entrenamientos)

@member_bp.route('/asistencias')
@login_required
@member_required
def asistencias():
    asistencias = Asistencia.query.filter_by(
        id_miembro=current_user.id_usuario
    ).order_by(Asistencia.id_asistencia.desc()).all()
    return render_template('member/asistencias.html', asistencias=asistencias)

@member_bp.route('/competiciones')
@login_required
@member_required
def competiciones():
    competiciones = Competicion.query.filter(
        Competicion.fecha >= date.today()
    ).order_by(Competicion.fecha).all()
    return render_template('member/competiciones.html', competiciones=competiciones)

@member_bp.route('/perfil')
@login_required
@member_required
def perfil():
    return render_template('member/perfil.html', usuario=current_user)

@member_bp.route('/historial')
@login_required
@member_required
def historial():
    # Obtener historial de asistencias con estadísticas
    asistencias = Asistencia.query.filter_by(
        id_miembro=current_user.id_usuario
    ).order_by(Asistencia.id_asistencia.desc()).all()
    
    # Estadísticas por mes
    monthly_stats = {}
    for asistencia in asistencias:
        # Obtener la fecha del entrenamiento
        entrenamiento = Entrenamiento.query.get(asistencia.id_entrenamiento)
        if entrenamiento:
            month_key = entrenamiento.fecha.strftime('%Y-%m')
            if month_key not in monthly_stats:
                monthly_stats[month_key] = 0
            monthly_stats[month_key] += 1
    
    return render_template('member/historial.html', 
                         asistencias=asistencias,
                         monthly_stats=monthly_stats)