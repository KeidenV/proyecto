import os


class Config:
    """Configuración de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu-clave-secreta-aqui')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Usar la variable de entorno DATABASE_URL en entornos de despliegue (Railway, Heroku, etc.)
    # Fallback para desarrollo local a MySQL en localhost
    # Normalizar URL de conexión: muchos proveedores ponen 'mysql://', SQLAlchemy
    # con PyMySQL necesita 'mysql+pymysql://'. Hacemos una pequeña corrección.
    _env_db = os.environ.get('DATABASE_URL')
    if _env_db and _env_db.startswith('mysql://'):
        _env_db = _env_db.replace('mysql://', 'mysql+pymysql://', 1)

    SQLALCHEMY_DATABASE_URI = _env_db or 'mysql+pymysql://root@localhost/club_deportivo'
