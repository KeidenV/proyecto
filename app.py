from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, User, Usuario, Rol, Actividad, Entrenamiento, Asistencia, Competicion, ResultadoCompeticion

# Crear la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)
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
    with app.app_context():
        db.create_all()
    app.run(debug=True)