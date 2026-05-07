from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import Usuario
from models.progreso import ProgresoLectura

users_bp = Blueprint('users', __name__)

def get_current_user():
    user_id = int(get_jwt_identity())
    return db.session.get(Usuario, user_id)


@users_bp.route('', methods=['GET'])
@jwt_required()
def list_users():
    user = get_current_user()
    if not user.es_admin():
        return jsonify({'error': 'Solo administradores'}), 403
    
    usuarios = Usuario.query.all()
    total_estudiantes = Usuario.query.filter_by(rol='estudiante').count()
    total_profesores = Usuario.query.filter_by(rol='profesor').count()
    usuarios_activos = Usuario.query.filter(Usuario.ultimo_login != None).count()
    lecturas_completadas = ProgresoLectura.query.filter_by(completada=True).count()
    
    return jsonify({
        'usuarios': [u.to_dict() for u in usuarios],
        'stats': {
            'total_estudiantes': total_estudiantes,
            'total_profesores': total_profesores,
            'usuarios_activos': usuarios_activos,
            'lecturas_completadas': lecturas_completadas
        }
    })


@users_bp.route('/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def update_user(usuario_id):
    user = get_current_user()
    if not user.es_admin():
        return jsonify({'error': 'Solo administradores'}), 403
    
    target = db.session.get(Usuario, usuario_id)
    if not target:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    data = request.get_json()
    if data.get('rol'):
        target.rol = data['rol']
    if data.get('tipo_usuario'):
        target.tipo_usuario = data['tipo_usuario']
    
    db.session.commit()
    return jsonify({'message': 'Usuario actualizado', 'user': target.to_dict()})


@users_bp.route('/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
def delete_user(usuario_id):
    user = get_current_user()
    if not user.es_admin():
        return jsonify({'error': 'Solo administradores'}), 403
    
    if usuario_id == user.id:
        return jsonify({'error': 'No puedes eliminarte a ti mismo'}), 400
    
    target = db.session.get(Usuario, usuario_id)
    if not target:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    db.session.delete(target)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado'})
