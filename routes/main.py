from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, User, Usuario, Rol, Actividad, Entrenamiento, Asistencia, Competicion, ResultadoCompeticion
from datetime import datetime, date

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Obtener el rol del usuario desde la relación
    if hasattr(current_user, 'rol') and current_user.rol:
        if current_user.rol.nombre_rol == 'Administrador':
            return redirect(url_for('admin.dashboard'))
        elif current_user.rol.nombre_rol == 'Entrenador':
            return redirect(url_for('trainer.dashboard'))
        elif current_user.rol.nombre_rol == 'Miembro':
            return redirect(url_for('member.dashboard'))
    
    return redirect(url_for('auth.login'))

@main_bp.route('/calendar')
@login_required
def calendar():
    competitions = Competicion.query.filter(
        Competicion.fecha >= date.today()
    ).order_by(Competicion.fecha).all()
    
    trainings = Entrenamiento.query.all()
    
    return render_template('calendar.html', competitions=competitions, trainings=trainings)

@main_bp.route('/profile')
@login_required
def profile():
    # Obtener estadísticas del usuario
    user_stats = {
        'total_trainings': 0,
        'total_attendance': 0,
        'attendance_rate': 0,
        'recent_activities': []
    }
    
    if hasattr(current_user, 'rol') and current_user.rol:
        if current_user.rol.nombre_rol == 'Miembro':
            # Estadísticas para miembros
            user_stats['total_trainings'] = Entrenamiento.query.count()
            user_stats['total_attendance'] = Asistencia.query.filter_by(id_miembro=current_user.id_usuario).count()
            if user_stats['total_trainings'] > 0:
                user_stats['attendance_rate'] = round((user_stats['total_attendance'] / user_stats['total_trainings']) * 100, 1)
            
            # Actividades recientes
            recent_attendances = Asistencia.query.filter_by(id_miembro=current_user.id_usuario)\
                .join(Entrenamiento).order_by(Entrenamiento.fecha.desc()).limit(5).all()
            user_stats['recent_activities'] = recent_attendances
    
    return render_template('profile.html', user_stats=user_stats)

@main_bp.route('/api/search')
@login_required
def search():
    """Endpoint para búsqueda en tiempo real"""
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', '')
    search_role = request.args.get('role', '')
    search_date = request.args.get('date', '')
    
    if not query or len(query) < 2:
        return jsonify([])
    
    results = []
    
    try:
        # Buscar usuarios
        if not search_type or search_type == 'usuario':
            usuarios_query = Usuario.query.join(Rol)
            
            if search_role:
                usuarios_query = usuarios_query.filter(Rol.nombre_rol == search_role)
            
            usuarios = usuarios_query.filter(
                db.or_(
                    Usuario.nombre.contains(query),
                    Usuario.apellido.contains(query),
                    Usuario.email.contains(query),
                    Rol.nombre_rol.contains(query)
                )
            ).limit(10).all()
            
            for usuario in usuarios:
                results.append({
                    'type': 'usuario',
                    'title': f"{usuario.nombre} {usuario.apellido}",
                    'description': f"{usuario.rol.nombre_rol} - {usuario.email}",
                    'url': '/admin/usuarios' if current_user.rol and current_user.rol.nombre_rol == 'Administrador' else '/profile',
                    'icon': 'fa-user'
                })
        
        # Buscar entrenamientos
        if not search_type or search_type == 'entrenamiento':
            entrenamientos_query = Entrenamiento.query.join(Actividad).join(Usuario, Entrenamiento.id_entrenador == Usuario.id_usuario)
            
            if search_date:
                entrenamientos_query = entrenamientos_query.filter(Entrenamiento.fecha == search_date)
            
            entrenamientos = entrenamientos_query.filter(
                db.or_(
                    Actividad.nombre_actividad.contains(query),
                    Usuario.nombre.contains(query),
                    Usuario.apellido.contains(query)
                )
            ).limit(10).all()
            
            for entrenamiento in entrenamientos:
                results.append({
                    'type': 'entrenamiento',
                    'title': f"Entrenamiento de {entrenamiento.actividad.nombre_actividad}",
                    'description': f"Entrenador: {entrenamiento.entrenador.nombre} {entrenamiento.entrenador.apellido} - {entrenamiento.fecha.strftime('%d/%m/%Y')}",
                    'url': '/admin/entrenamientos' if current_user.rol and current_user.rol.nombre_rol == 'Administrador' else '/trainer/trainings',
                    'icon': 'fa-running'
                })
        
        # Buscar competiciones
        if not search_type or search_type == 'competicion':
            competiciones_query = Competicion.query.join(Actividad)
            
            if search_date:
                competiciones_query = competiciones_query.filter(Competicion.fecha == search_date)
            
            competiciones = competiciones_query.filter(
                db.or_(
                    Competicion.nombre.contains(query),
                    Competicion.ubicacion.contains(query),
                    Competicion.descripcion.contains(query),
                    Actividad.nombre_actividad.contains(query)
                )
            ).limit(10).all()
            
            for competicion in competiciones:
                results.append({
                    'type': 'competicion',
                    'title': competicion.nombre,
                    'description': f"{competicion.ubicacion or 'Sin ubicación'} - {competicion.fecha.strftime('%d/%m/%Y')}",
                    'url': '/admin/competiciones' if current_user.rol and current_user.rol.nombre_rol == 'Administrador' else '/member/competitions',
                    'icon': 'fa-trophy'
                })
        
        # Buscar actividades
        if not search_type or search_type == 'actividad':
            actividades = Actividad.query.filter(
                Actividad.nombre_actividad.contains(query)
            ).limit(10).all()
            
            for actividad in actividades:
                results.append({
                    'type': 'actividad',
                    'title': actividad.nombre_actividad,
                    'description': 'Actividad deportiva',
                    'url': '/admin/actividades' if current_user.rol and current_user.rol.nombre_rol == 'Administrador' else '/calendar',
                    'icon': 'fa-dumbbell'
                })
        
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        return jsonify([])
    
    return jsonify(results[:20])  # Limitar a 20 resultados