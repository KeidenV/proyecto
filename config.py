import os


class Config:
    """Configuración de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu-clave-secreta-aqui')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Usar la variable de entorno DATABASE_URL en entornos de despliegue (Railway, Heroku, etc.)
    # Fallback para desarrollo local a MySQL en localhost
    # Buscar la primera variable de entorno conocida que contenga la URL de la BD.
    # Muchos proveedores usan nombres distintos; intentamos los más comunes.
    _candidate_names = [
        'DATABASE_URL',
        'RAILWAY_DATABASE_URL',
        'RAILWAY_MYSQL_URL',
        'MYSQL_URL',
        'CLEARDB_DATABASE_URL',
        'JAWSDB_URL'
    ]

    _env_db = None
    for name in _candidate_names:
        val = os.environ.get(name)
        if val:
            _env_db = val
            break

    # Normalizar esquema: si el proveedor devuelve 'mysql://', SQLAlchemy con PyMySQL
    # necesita 'mysql+pymysql://'. También aceptamos ya 'mysql+pymysql://'.
    if _env_db:
        if _env_db.startswith('mysql://'):
            _env_db = _env_db.replace('mysql://', 'mysql+pymysql://', 1)

    # Fallback local: MySQL en localhost (solo para desarrollo)
    SQLALCHEMY_DATABASE_URI = _env_db or 'mysql+pymysql://root@localhost/club_deportivo'
