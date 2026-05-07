from extensions import db
from datetime import datetime

class ProgresoLectura(db.Model):
    __tablename__ = 'progreso_lecturas'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    lectura_id = db.Column(db.Integer, db.ForeignKey('lecturas.id'), nullable=False)
    completada = db.Column(db.Boolean, default=False)
    incompleta = db.Column(db.Boolean, default=False)
    puntos_obtenidos = db.Column(db.Integer, default=0)
    intentos = db.Column(db.Integer, default=0)
    quiz_aprobado = db.Column(db.Boolean, default=False)
    quiz_porcentaje = db.Column(db.Float, default=0.0)
    fallos = db.Column(db.Integer, default=0)
    fecha_completado = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'lectura_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'lectura_id': self.lectura_id,
            'completada': self.completada,
            'incompleta': self.incompleta,
            'puntos_obtenidos': self.puntos_obtenidos,
            'intentos': self.intentos,
            'quiz_aprobado': self.quiz_aprobado,
            'quiz_porcentaje': self.quiz_porcentaje,
            'fallos': self.fallos,
            'fecha_completado': self.fecha_completado.isoformat() if self.fecha_completado else None
        }
