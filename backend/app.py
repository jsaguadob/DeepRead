import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path)

from flask import Flask, send_from_directory
from flask_cors import CORS
from extensions import db, jwt
from config import Config

def create_app():
    app = Flask(__name__, static_folder='../frontend/dist', instance_path=os.path.join(os.path.dirname(__file__), 'instance'))
    app.config.from_object(Config)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    db.init_app(app)
    jwt.init_app(app)
    
    from routes.auth import auth_bp
    from routes.readings import readings_bp
    from routes.quizzes import quizzes_bp
    from routes.groups import groups_bp
    from routes.activities import activities_bp
    from routes.users import users_bp
    from routes.institutions import institutions_bp
    from routes.stats import stats_bp
    from routes.ai import ai_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(readings_bp, url_prefix='/api/lecturas')
    app.register_blueprint(quizzes_bp, url_prefix='/api')
    app.register_blueprint(groups_bp, url_prefix='/api/grupos')
    app.register_blueprint(activities_bp, url_prefix='/api/actividades')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(institutions_bp, url_prefix='/api/instituciones')
    app.register_blueprint(stats_bp, url_prefix='/api')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    
    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'version': '2.0'}
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')
    
    with app.app_context():
        db.create_all()
        from services.ai_client import iniciar
        iniciar(app.config.get('GEMINI_API_KEY', ''))
        
        from sqlalchemy import text, inspect
        inspector = inspect(db.engine)
        
        try:
            lectura_columns = [c['name'] for c in inspector.get_columns('lecturas')]
            progreso_columns = [c['name'] for c in inspector.get_columns('progreso_lecturas')]
            
            if 'fecha_cierre' not in lectura_columns:
                db.session.execute(text('ALTER TABLE lecturas ADD COLUMN fecha_cierre TIMESTAMP'))
            if 'cerrada' not in lectura_columns:
                db.session.execute(text('ALTER TABLE lecturas ADD COLUMN cerrada INTEGER DEFAULT 0'))
            if 'intentos_maximos' not in lectura_columns:
                db.session.execute(text('ALTER TABLE lecturas ADD COLUMN intentos_maximos INTEGER DEFAULT 3'))
            if 'incompleta' not in progreso_columns:
                db.session.execute(text('ALTER TABLE progreso_lecturas ADD COLUMN incompleta INTEGER DEFAULT 0'))
            if 'quiz_aprobado' not in progreso_columns:
                db.session.execute(text('ALTER TABLE progreso_lecturas ADD COLUMN quiz_aprobado INTEGER DEFAULT 0'))
            if 'quiz_porcentaje' not in progreso_columns:
                db.session.execute(text('ALTER TABLE progreso_lecturas ADD COLUMN quiz_porcentaje REAL DEFAULT 0'))
            if 'fallos' not in progreso_columns:
                db.session.execute(text('ALTER TABLE progreso_lecturas ADD COLUMN fallos INTEGER DEFAULT 0'))
        except:
            pass
        
        try:
            actividad_columns = [c['name'] for c in inspector.get_columns('actividades')]
            if 'lectura_id' not in actividad_columns:
                db.session.execute(text('ALTER TABLE actividades ADD COLUMN lectura_id INTEGER'))
        except:
            pass
        
        try:
            db.session.commit()
        except:
            db.session.rollback()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
