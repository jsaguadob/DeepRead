import os
from flask import Flask
from flask_login import LoginManager
from extensions import db

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'deepread-secret-key-2024'

db_url = os.environ.get('DATABASE_URL')
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deepread.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from models.user import Usuario
from models.lectura import Lectura, Pregunta
from models.progreso import ProgresoLectura
from models.grupo import Grupo, MiembroGrupo
from models.quiz import RespuestaQuiz
try:
    from models.actividad import Actividad, ProgresoActividad
except:
    pass
from routes.auth import auth_bp
from routes.main import main_bp
from routes.admin import admin_bp

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()
    
    from sqlalchemy import text, inspect
    inspector = inspect(db.engine)
    lectura_columns = [c['name'] for c in inspector.get_columns('lecturas')]
    progreso_columns = [c['name'] for c in inspector.get_columns('progreso_lecturas')]
    
    try:
        if 'fecha_cierre' not in lectura_columns:
            db.session.execute(text('ALTER TABLE lecturas ADD COLUMN fecha_cierre TIMESTAMP'))
    except: pass
    try:
        if 'cerrada' not in lectura_columns:
            db.session.execute(text('ALTER TABLE lecturas ADD COLUMN cerrada INTEGER DEFAULT 0'))
    except: pass
    try:
        if 'intentos_maximos' not in lectura_columns:
            db.session.execute(text('ALTER TABLE lecturas ADD COLUMN intentos_maximos INTEGER DEFAULT 3'))
    except: pass
    try:
        if 'incompleta' not in progreso_columns:
            db.session.execute(text('ALTER TABLE progreso_lecturas ADD COLUMN incompleta INTEGER DEFAULT 0'))
    except: pass
    try:
        if 'quiz_aprobado' not in progreso_columns:
            db.session.execute(text('ALTER TABLE progreso_lecturas ADD COLUMN quiz_aprobado INTEGER DEFAULT 0'))
    except: pass
    try:
        if 'quiz_porcentaje' not in progreso_columns:
            db.session.execute(text('ALTER TABLE progreso_lecturas ADD COLUMN quiz_porcentaje REAL DEFAULT 0'))
    except: pass
    try: db.session.commit()
    except: db.session.rollback()
    
    try:
        inspector = inspect(db.engine)
        actividad_columns = [c['name'] for c in inspector.get_columns('actividades')]
    except:
        actividad_columns = []
    
    try:
        if 'lectura_id' not in actividad_columns:
            db.session.execute(text('ALTER TABLE actividades ADD COLUMN lectura_id INTEGER'))
    except: pass
    
    try: db.session.commit()
    except: db.session.rollback()
    
    try:
        pass  # Datos iniciales removidos
    except Exception as e:
        print(f"Error al inicializar datos: {e}")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)