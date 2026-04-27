from extensions import db

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
    fecha_completado = db.Column(db.DateTime, default=None)
    
    __table_args__ = (db.UniqueConstraint('usuario_id', 'lectura_id', name='uix_usuario_lectura'),)
    
    def to_dict(self):
        return {
            'lectura_id': self.lectura_id,
            'completada': self.completada,
            'puntos_obtenidos': self.puntos_obtenidos,
            'quiz_aprobado': self.quiz_aprobado,
            'quiz_porcentaje': self.quiz_porcentaje
        }