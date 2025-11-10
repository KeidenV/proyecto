from flask import Blueprint, render_template, make_response, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Usuario, Rol, Actividad, Entrenamiento, Asistencia, Competicion, ResultadoCompeticion
from datetime import datetime, date, timedelta
from pdf_generator import ClubPDFGenerator

reports_bp = Blueprint('reports', __name__)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'rol') or current_user.rol.nombre_rol != 'Administrador':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@reports_bp.route('/')
@login_required
def index():
    return render_template('reports/index.html')

@reports_bp.route('/usuarios/pdf')
@login_required
@admin_required
def usuarios_pdf():
    """Generar PDF de usuarios"""
    usuarios = Usuario.query.join(Rol).all()
    
    pdf_generator = ClubPDFGenerator()
    
    # Crear un PDF simple con lista de usuarios
    buffer = BytesIO()
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Título
    story.append(Paragraph("REPORTE DE USUARIOS", styles['Title']))
    story.append(Spacer(1, 20))
    
    # Tabla de usuarios
    data = [['ID', 'Nombre', 'Email', 'Rol']]
    for usuario in usuarios:
        data.append([
            str(usuario.id_usuario),
            f"{usuario.nombre} {usuario.apellido}",
            usuario.email,
            usuario.rol.nombre_rol if usuario.rol else 'No asignado'
        ])
    
    table = Table(data, colWidths=[1*inch, 2.5*inch, 2.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    doc.build(story)
    
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=usuarios_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return response

@reports_bp.route('/actividades/pdf')
@login_required
@admin_required
def actividades_pdf():
    """Generar PDF de actividades"""
    actividades = Actividad.query.all()
    
    pdf_generator = ClubPDFGenerator()
    buffer = pdf_generator.generate_activities_report(actividades)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=actividades_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return response

@reports_bp.route('/entrenamientos/pdf')
@login_required
@admin_required
def entrenamientos_pdf():
    """Generar PDF de entrenamientos"""
    entrenamientos = Entrenamiento.query.join(Usuario, Entrenamiento.id_entrenador == Usuario.id_usuario)\
        .join(Actividad, Entrenamiento.id_actividad == Actividad.id_actividad)\
        .order_by(Entrenamiento.fecha.desc()).all()
    
    pdf_generator = ClubPDFGenerator()
    buffer = pdf_generator.generate_trainings_report(entrenamientos)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=entrenamientos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return response

@reports_bp.route('/competiciones/pdf')
@login_required
@admin_required
def competiciones_pdf():
    """Generar PDF de competiciones"""
    competiciones = Competicion.query.join(Actividad, Competicion.id_actividad == Actividad.id_actividad, isouter=True)\
        .order_by(Competicion.fecha.desc()).all()
    
    pdf_generator = ClubPDFGenerator()
    buffer = pdf_generator.generate_competitions_report(competiciones)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=competiciones_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return response

@reports_bp.route('/asistencias/pdf')
@login_required
@admin_required
def asistencias_pdf():
    """Generar PDF de asistencias"""
    asistencias = Asistencia.query.join(Usuario, Asistencia.id_miembro == Usuario.id_usuario)\
        .join(Entrenamiento, Asistencia.id_entrenamiento == Entrenamiento.id_entrenamiento)\
        .join(Actividad, Entrenamiento.id_actividad == Actividad.id_actividad)\
        .order_by(Asistencia.id_asistencia.desc()).all()
    
    pdf_generator = ClubPDFGenerator()
    buffer = pdf_generator.generate_attendance_report(asistencias)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=asistencias_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return response

@reports_bp.route('/miembro/<int:user_id>/pdf')
@login_required
def miembro_pdf(user_id):
    """Generar PDF de miembro individual"""
    # Solo permitir que los usuarios vean su propio reporte o que los admins vean cualquier reporte
    if current_user.id_usuario != user_id and (not hasattr(current_user, 'rol') or current_user.rol.nombre_rol != 'Administrador'):
        flash('No tienes permisos para ver este reporte', 'error')
        return redirect(url_for('main.dashboard'))
    
    usuario = Usuario.query.get_or_404(user_id)
    
    # Obtener entrenamientos y competiciones del usuario
    entrenamientos = []
    competiciones = []
    
    if hasattr(usuario, 'rol') and usuario.rol.nombre_rol == 'Miembro':
        # Obtener asistencias del miembro
        asistencias = Asistencia.query.filter_by(id_miembro=user_id)\
            .join(Entrenamiento).join(Actividad).all()
        entrenamientos = asistencias
    
        # Obtener competiciones relacionadas (esto sería más complejo en un caso real)
        competiciones = Competicion.query.join(Actividad).all()
    
    pdf_generator = ClubPDFGenerator()
    buffer = pdf_generator.generate_member_report(usuario, entrenamientos, competiciones)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=miembro_{usuario.nombre}_{usuario.apellido}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return response

@reports_bp.route('/asistencias')
@login_required
@admin_required
def reporte_asistencias():
    # Obtener parámetros de fecha
    start_date = request.args.get('start_date', (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', date.today().strftime('%Y-%m-%d'))
    
    # Convertir a objetos date
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Obtener asistencias en el rango de fechas
    asistencias = Asistencia.query.join(Entrenamiento).filter(
        Entrenamiento.fecha >= start_date,
        Entrenamiento.fecha <= end_date
    ).order_by(Entrenamiento.fecha.desc()).all()
    
    return render_template('reports/asistencias.html', 
                         asistencias=asistencias, 
                         start_date=start_date, 
                         end_date=end_date)

@reports_bp.route('/usuarios')
@login_required
@admin_required
def reporte_usuarios():
    usuarios = Usuario.query.all()
    return render_template('reports/usuarios.html', usuarios=usuarios)

@reports_bp.route('/entrenamientos')
@login_required
@admin_required
def reporte_entrenamientos():
    entrenamientos = Entrenamiento.query.all()
    return render_template('reports/entrenamientos.html', entrenamientos=entrenamientos)

@reports_bp.route('/competiciones')
@login_required
@admin_required
def reporte_competiciones():
    competiciones = Competicion.query.all()
    return render_template('reports/competiciones.html', competiciones=competiciones)