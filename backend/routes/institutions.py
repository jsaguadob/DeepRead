from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import Usuario, Institucion
from datetime import datetime
import random
import string

institutions_bp = Blueprint('institutions', __name__)

def get_current_user():
    user_id = int(get_jwt_identity())
    return db.session.get(Usuario, user_id)

def gerar_codigo(length=8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


@institutions_bp.route('', methods=['GET'])
@jwt_required()
def list_institutions():
    user = get_current_user()
    if not user.es_admin():
        return jsonify({'error': 'Solo administradores'}), 403
    
    instituciones = Institucion.query.all()
    return jsonify({'instituciones': [i.to_dict() for i in instituciones]})


@institutions_bp.route('', methods=['POST'])
@jwt_required()
def create_institution():
    user = get_current_user()
    if not user.es_admin():
        return jsonify({'error': 'Solo administradores'}), 403
    
    data = request.get_json()
    if not data or not data.get('nombre'):
        return jsonify({'error': 'Nombre de la institución requerido'}), 400
    
    nombre = data['nombre'].strip()
    
    existente = Institucion.query.filter_by(nombre=nombre).first()
    if existente:
        return jsonify({'error': 'Ya existe una institución con ese nombre'}), 400
    
    codigo = gerar_codigo()
    while Institucion.query.filter_by(codigo=codigo).first():
        codigo = gerar_codigo()
    
    institucion = Institucion(
        nombre=nombre,
        codigo=codigo,
        activa=True
    )
    db.session.add(institucion)
    db.session.commit()
    
    return jsonify({
        'message': 'Institución creada',
        'institucion': institucion.to_dict()
    }), 201


@institutions_bp.route('/<int:institucion_id>', methods=['PUT'])
@jwt_required()
def update_institution(institucion_id):
    user = get_current_user()
    if not user.es_admin():
        return jsonify({'error': 'Solo administradores'}), 403
    
    institucion = db.session.get(Institucion, institucion_id)
    if not institucion:
        return jsonify({'error': 'Institución no encontrada'}), 404
    
    data = request.get_json()
    if data.get('nombre'):
        institucion.nombre = data['nombre']
    if 'activa' in data:
        institucion.activa = data['activa']
    
    db.session.commit()
    return jsonify({
        'message': 'Institución actualizada',
        'institucion': institucion.to_dict()
    })


@institutions_bp.route('/<int:institucion_id>', methods=['DELETE'])
@jwt_required()
def delete_institution(institucion_id):
    user = get_current_user()
    if not user.es_admin():
        return jsonify({'error': 'Solo administradores'}), 403
    
    institucion = db.session.get(Institucion, institucion_id)
    if not institucion:
        return jsonify({'error': 'Institución no encontrada'}), 404
    
    # Soft delete by deactivating
    institucion.activa = False
    db.session.commit()
    
    return jsonify({'message': 'Institución desactivada'})
