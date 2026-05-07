from extensions import db
from datetime import datetime

class Actividad(db.Model):
    __tablename__ = 'actividades'
    
    id = db.Column(db.Integer, primary_key=True)
    lectura_id = db.Column(db.Integer, db.ForeignKey('lecturas.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    solucion = db.Column(db.Text, nullable=False)
    nivel = db.Column(db.Integer, default=1)
    puntos = db.Column(db.Integer, default=5)
    tiempo_estimado = db.Column(db.Integer, default=10)
    activa = db.Column(db.Boolean, default=True)
    profesor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'lectura_id': self.lectura_id,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'contenido': self.contenido,
            'solucion': self.solucion,
            'nivel': self.nivel,
            'puntos': self.puntos,
            'tiempo_estimado': self.tiempo_estimado,
            'activa': self.activa,
            'profesor_id': self.profesor_id
        }


class ProgresoActividad(db.Model):
    __tablename__ = 'progreso_actividades'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividades.id'), nullable=False)
    completado = db.Column(db.Boolean, default=False)
    puntos_obtenidos = db.Column(db.Integer, default=0)
    respuesta = db.Column(db.Text, nullable=True)
    fecha_completado = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'actividad_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'actividad_id': self.actividad_id,
            'completado': self.completado,
            'puntos_obtenidos': self.puntos_obtenidos,
            'respuesta': self.respuesta,
            'fecha_completado': self.fecha_completado.isoformat() if self.fecha_completado else None
        }
