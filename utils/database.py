from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
        inspector = inspect(db.engine)
        lectura_columns = [c['name'] for c in inspector.get_columns('lecturas')]
        progreso_columns = [c['name'] for c in inspector.get_columns('progreso_lecturas')]
        
        try:
            if 'fecha_cierre' not in lectura_columns:
                db.session.execute(text('ALTER TABLE lecturas ADD COLUMN fecha_cierre TIMESTAMP'))
                db.session.commit()
        except:
            db.session.rollback()
        
        try:
            if 'cerrada' not in lectura_columns:
                db.session.execute(text('ALTER TABLE lecturas ADD COLUMN cerrada INTEGER DEFAULT 0'))
                db.session.commit()
        except:
            db.session.rollback()
        
        try:
            if 'intentos_maximos' not in lectura_columns:
                db.session.execute(text('ALTER TABLE lecturas ADD COLUMN intentos_maximos INTEGER DEFAULT 3'))
                db.session.commit()
        except:
            db.session.rollback()
        
        try:
            if 'incompleta' not in progreso_columns:
                db.session.execute(text('ALTER TABLE progreso_lecturas ADD COLUMN incompleta INTEGER DEFAULT 0'))
                db.session.commit()
        except:
            db.session.rollback()
        
        try:
            if 'intentos' not in progreso_columns:
                db.session.execute(text('ALTER TABLE progreso_lecturas ADD COLUMN intentos INTEGER DEFAULT 0'))
                db.session.commit()
        except:
            db.session.rollback()