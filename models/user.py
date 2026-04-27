from extensions import db
from flask_login import UserMixin
from datetime import datetime

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), default='estudiante')
    tipo_usuario = db.Column(db.String(20), default='gratuito')
    nivel_actual = db.Column(db.Integer, default=1)
    puntos_totales = db.Column(db.Integer, default=0)
    racha_dias = db.Column(db.Integer, default=0)
    ultimo_login = db.Column(db.Date, default=None)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_id(self):
        return str(self.id)
    
    def es_admin(self):
        return self.rol == 'admin'
    
    def es_profesor(self):
        return self.rol in ['profesor', 'admin']
    
    def es_institucional(self):
        return self.tipo_usuario == 'institucional'
    
    def es_gratuito(self):
        return self.tipo_usuario == 'gratuito'


class Institucion(db.Model):
    __tablename__ = 'instituciones'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)