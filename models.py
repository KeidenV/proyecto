from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Crear instancia de SQLAlchemy que será inicializada en app.py
db = SQLAlchemy()

class Rol(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_rol = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Rol {self.nombre_rol}>'

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=False)
    
    # Relaciones
    rol = db.relationship('Rol', backref='usuarios')
    
    # Propiedades para compatibilidad con Flask-Login
    @property
    def id(self):
        return self.id_usuario
    
    @property
    def username(self):
        return self.email
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.nombre} {self.apellido}>'

class Actividad(db.Model):
    __tablename__ = 'actividades'
    id_actividad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_actividad = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Actividad {self.nombre_actividad}>'

class Entrenamiento(db.Model):
    __tablename__ = 'entrenamientos'
    id_entrenamiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_entrenador = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_actividad = db.Column(db.Integer, db.ForeignKey('actividades.id_actividad'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    
    # Relaciones
    entrenador = db.relationship('Usuario', backref='entrenamientos')
    actividad = db.relationship('Actividad', backref='entrenamientos')
    asistencias = db.relationship('Asistencia', backref='entrenamiento', lazy=True)
    
    def __repr__(self):
        return f'<Entrenamiento {self.fecha}>'

class Asistencia(db.Model):
    __tablename__ = 'asistencias'
    id_asistencia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_entrenamiento = db.Column(db.Integer, db.ForeignKey('entrenamientos.id_entrenamiento'), nullable=False)
    id_miembro = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    presente = db.Column(db.Boolean, nullable=False, default=True)
    observaciones = db.Column(db.Text)
    
    # Relaciones
    miembro = db.relationship('Usuario', backref='asistencias')
    
    # Restricción única
    __table_args__ = (db.UniqueConstraint('id_entrenamiento', 'id_miembro', name='uq_asistencia_entrenamiento_miembro'),)
    
    def __repr__(self):
        return f'<Asistencia {self.id_miembro} - {self.id_entrenamiento}>'

class Competicion(db.Model):
    __tablename__ = 'competiciones'
    id_competicion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    ubicacion = db.Column(db.String(150))
    descripcion = db.Column(db.Text)
    id_actividad = db.Column(db.Integer, db.ForeignKey('actividades.id_actividad'))
    
    # Relaciones
    actividad = db.relationship('Actividad', backref='competiciones')
    resultados = db.relationship('ResultadoCompeticion', backref='competicion', lazy=True)
    
    def __repr__(self):
        return f'<Competicion {self.nombre}>'

class ResultadoCompeticion(db.Model):
    __tablename__ = 'resultados_competicion'
    id_resultado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_competicion = db.Column(db.Integer, db.ForeignKey('competiciones.id_competicion'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    posicion = db.Column(db.Integer)
    marca = db.Column(db.String(100))
    observaciones = db.Column(db.Text)
    
    # Relaciones
    usuario = db.relationship('Usuario', backref='resultados_competicion')
    
    # Restricción única
    __table_args__ = (db.UniqueConstraint('id_competicion', 'id_usuario', name='uq_resultado_competicion_participante'),)
    
    def __repr__(self):
        return f'<ResultadoCompeticion {self.id_competicion} - {self.id_usuario}>'

# Alias para compatibilidad con el código existente
User = Usuario
Member = Usuario  # Los miembros ahora son usuarios con rol específico
Trainer = Usuario  # Los entrenadores ahora son usuarios con rol específico
Training = Entrenamiento
Competition = Competicion
Attendance = Asistencia