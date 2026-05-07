from extensions import db
from datetime import datetime

class Grupo(db.Model):
    __tablename__ = 'grupos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    profesor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    codigo_unico = db.Column(db.String(10), unique=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'profesor_id': self.profesor_id,
            'codigo_unico': self.codigo_unico,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'activo': self.activo
        }


class MiembroGrupo(db.Model):
    __tablename__ = 'miembros_grupo'
    
    id = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    rol_en_grupo = db.Column(db.String(20), default='estudiante')
    fecha_union = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('grupo_id', 'usuario_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'grupo_id': self.grupo_id,
            'usuario_id': self.usuario_id,
            'rol_en_grupo': self.rol_en_grupo,
            'fecha_union': self.fecha_union.isoformat() if self.fecha_union else None
        }
