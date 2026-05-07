from extensions import db
from datetime import datetime

class Lectura(db.Model):
    __tablename__ = 'lecturas'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    tiempo_estimado_minutos = db.Column(db.Integer, nullable=False)
    puntos_recompensa = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(50))
    activa = db.Column(db.Boolean, default=True)
    es_publica = db.Column(db.Boolean, default=True)
    fecha_cierre = db.Column(db.DateTime, nullable=True)
    cerrada = db.Column(db.Boolean, default=False)
    intentos_maximos = db.Column(db.Integer, default=3)
    profesor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'contenido': self.contenido,
            'nivel': self.nivel,
            'tiempo_estimado_minutos': self.tiempo_estimado_minutos,
            'puntos_recompensa': self.puntos_recompensa,
            'categoria': self.categoria,
            'activa': self.activa,
            'es_publica': self.es_publica,
            'fecha_cierre': self.fecha_cierre.isoformat() if self.fecha_cierre else None,
            'cerrada': self.cerrada,
            'intentos_maximos': self.intentos_maximos,
            'profesor_id': self.profesor_id,
            'grupo_id': self.grupo_id
        }


class Pregunta(db.Model):
    __tablename__ = 'preguntas'
    
    id = db.Column(db.Integer, primary_key=True)
    lectura_id = db.Column(db.Integer, db.ForeignKey('lecturas.id'), nullable=False)
    pregunta = db.Column(db.Text, nullable=False)
    opcion_a = db.Column(db.Text, nullable=False)
    opcion_b = db.Column(db.Text, nullable=False)
    opcion_c = db.Column(db.Text, nullable=False)
    opcion_d = db.Column(db.Text, nullable=False)
    respuesta_correcta = db.Column(db.String(1), nullable=False)
    explicacion = db.Column(db.Text, nullable=True)
    profesor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'lectura_id': self.lectura_id,
            'pregunta': self.pregunta,
            'opcion_a': self.opcion_a,
            'opcion_b': self.opcion_b,
            'opcion_c': self.opcion_c,
            'opcion_d': self.opcion_d,
            'respuesta_correcta': self.respuesta_correcta,
            'explicacion': self.explicacion,
            'profesor_id': self.profesor_id
        }
