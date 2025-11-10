from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, DateField, TimeField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import Usuario, Rol, Actividad, Entrenamiento, Competicion
from datetime import date

def validate_fecha_nacimiento(form, field):
    """Validador personalizado para fechas de nacimiento"""
    if field.data:
        today = date.today()
        if field.data > today:
            raise ValidationError('La fecha de nacimiento no puede ser futura.')
        # Verificar que no sea demasiado antigua (más de 150 años)
        if field.data < date(today.year - 150, today.month, today.day):
            raise ValidationError('La fecha de nacimiento no puede ser anterior a 150 años.')
        # Verificar que no sea demasiado reciente (menos de 13 años)
        if field.data > date(today.year - 13, today.month, today.day):
            raise ValidationError('La fecha de nacimiento debe ser de al menos 13 años atrás.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[validate_fecha_nacimiento])
    id_rol = SelectField('Rol', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Cargar roles disponibles
        self.id_rol.choices = [(rol.id_rol, rol.nombre_rol) for rol in Rol.query.all()]

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('El email ya está registrado. Por favor usa otro.')

class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[validate_fecha_nacimiento])
    id_rol = SelectField('Rol', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        # Cargar roles disponibles
        self.id_rol.choices = [(rol.id_rol, rol.nombre_rol) for rol in Rol.query.all()]

    def validate_email(self, email):
        # Solo validar si es un nuevo usuario o si el email cambió
        if hasattr(self, 'usuario_id'):
            user = Usuario.query.filter_by(email=email.data).first()
            if user and user.id_usuario != self.usuario_id:
                raise ValidationError('El email ya está registrado. Por favor usa otro.')
        else:
            user = Usuario.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('El email ya está registrado. Por favor usa otro.')

class ActividadForm(FlaskForm):
    nombre_actividad = StringField('Nombre de la Actividad', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Guardar')

    def validate_nombre_actividad(self, nombre_actividad):
        actividad = Actividad.query.filter_by(nombre_actividad=nombre_actividad.data).first()
        if actividad:
            raise ValidationError('Esta actividad ya existe. Por favor elige otro nombre.')

class EntrenamientoForm(FlaskForm):
    id_entrenador = SelectField('Entrenador', coerce=int, validators=[DataRequired()])
    id_actividad = SelectField('Actividad', coerce=int, validators=[DataRequired()])
    fecha = DateField('Fecha del Entrenamiento', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(EntrenamientoForm, self).__init__(*args, **kwargs)
        # Cargar entrenadores (usuarios con rol de entrenador)
        entrenadores = Usuario.query.join(Rol).filter(Rol.nombre_rol == 'Entrenador').all()
        self.id_entrenador.choices = [(u.id_usuario, f"{u.nombre} {u.apellido}") for u in entrenadores]
        
        # Cargar actividades disponibles
        self.id_actividad.choices = [(a.id_actividad, a.nombre_actividad) for a in Actividad.query.all()]

class CompeticionForm(FlaskForm):
    nombre = StringField('Nombre de la Competición', validators=[DataRequired(), Length(min=2, max=150)])
    fecha = DateField('Fecha del Evento', validators=[DataRequired()], format='%Y-%m-%d')
    ubicacion = StringField('Ubicación', validators=[Length(max=150)])
    descripcion = TextAreaField('Descripción')
    id_actividad = SelectField('Actividad', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(CompeticionForm, self).__init__(*args, **kwargs)
        # Cargar actividades disponibles
        self.id_actividad.choices = [(a.id_actividad, a.nombre_actividad) for a in Actividad.query.all()]

class AsistenciaForm(FlaskForm):
    id_entrenamiento = SelectField('Entrenamiento', coerce=int, validators=[DataRequired()])
    id_miembro = SelectField('Miembro', coerce=int, validators=[DataRequired()])
    presente = BooleanField('Presente', default=True)
    observaciones = TextAreaField('Observaciones')
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(AsistenciaForm, self).__init__(*args, **kwargs)
        # Cargar entrenamientos disponibles
        self.id_entrenamiento.choices = [(e.id_entrenamiento, f"{e.actividad.nombre_actividad} - {e.fecha}") for e in Entrenamiento.query.all()]
        
        # Cargar miembros (usuarios con rol de miembro)
        miembros = Usuario.query.join(Rol).filter(Rol.nombre_rol == 'Miembro').all()
        self.id_miembro.choices = [(u.id_usuario, f"{u.nombre} {u.apellido}") for u in miembros]

# Alias para compatibilidad
MemberForm = UsuarioForm
TrainerForm = UsuarioForm
TrainingForm = EntrenamientoForm
CompetitionForm = CompeticionForm
