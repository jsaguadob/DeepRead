from extensions import db
from datetime import datetime

class RespuestaQuiz(db.Model):
    __tablename__ = 'respuestas_quiz'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('preguntas.id'), nullable=False)
    respondida = db.Column(db.String(1), nullable=False)
    correcta = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'pregunta_id': self.pregunta_id,
            'respondida': self.respondida,
            'correcta': self.correcta,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
