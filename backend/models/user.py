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
    consultas_ia_hoy = db.Column(db.Integer, default=0)
    fecha_ultima_consulta = db.Column(db.Date, default=None)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_id(self):
        return str(self.id)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'rol': self.rol,
            'tipo_usuario': self.tipo_usuario,
            'nivel_actual': self.nivel_actual,
            'puntos_totales': self.puntos_totales,
            'racha_dias': self.racha_dias,
            'ultimo_login': self.ultimo_login.isoformat() if self.ultimo_login else None,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    def consultas_restantes_hoy(self):
        from datetime import date
        hoy = date.today()
        if self.fecha_ultima_consulta != hoy:
            self.consultas_ia_hoy = 0
            self.fecha_ultima_consulta = hoy
        limite = 30 if self.es_institucional() else 5
        return max(0, limite - self.consultas_ia_hoy)

    def usar_consulta(self):
        from datetime import date
        hoy = date.today()
        if self.fecha_ultima_consulta != hoy:
            self.consultas_ia_hoy = 0
            self.fecha_ultima_consulta = hoy
        self.consultas_ia_hoy += 1

    def es_admin(self):
        return self.rol == 'admin'
    
    def es_profesor(self):
        return self.rol in ['profesor', 'admin']
    
    def es_institucional(self):
        return self.tipo_usuario == 'institucional'
    
    def es_gratuito(self):
        return self.tipo_usuario == 'gratuito'

    def es_estudiante(self):
        return self.rol == 'estudiante'


class Institucion(db.Model):
    __tablename__ = 'instituciones'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'codigo': self.codigo,
            'activa': self.activa,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
