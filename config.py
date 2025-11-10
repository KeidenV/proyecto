import os

class Config:
    """Configuración de la aplicación"""
    SECRET_KEY = 'tu-clave-secreta-aqui'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/club_deportivo'