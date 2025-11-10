from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, User, Usuario, Rol, Actividad, Entrenamiento, Asistencia, Competicion, ResultadoCompeticion
import os

# Crear la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)
# En producción (por defecto) requerimos que se provea DATABASE_URL.
# Esto evita intentar conectar a 'localhost' en plataformas como Railway.
if os.environ.get('FLASK_ENV', 'production') == 'production' and not os.environ.get('DATABASE_URL'):
    # Mensaje claro para los logs de Railway
    print('\n[ERROR] DATABASE_URL no encontrada en las variables de entorno.')
    print('[ERROR] En Railway añade la variable de entorno DATABASE_URL con la cadena de conexión provista por el plugin MySQL/Service.')
    print("[ERROR] Ejemplo: mysql+pymysql://user:pass@host:3306/dbname\n")
    raise RuntimeError('DATABASE_URL no configurada en entorno de producción')
# app.config['WTF_CSRF_ENABLED'] = False  # CSRF habilitado por defecto

# Inicializar extensiones
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'

# Importar rutas
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.trainer import trainer_bp
from routes.member import member_bp
from routes.main import main_bp
from routes.reports import reports_bp

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(trainer_bp, url_prefix='/trainer')
app.register_blueprint(member_bp, url_prefix='/member')
app.register_blueprint(main_bp)
app.register_blueprint(reports_bp, url_prefix='/reports')

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    # No ejecutar db.create_all() automáticamente en el arranque.
    # Para inicializar la base de datos localmente usa: python init_db.py
    app.run(debug=True, host='0.0.0.0')
