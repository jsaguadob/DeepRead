from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models.user import Usuario
from datetime import datetime, date
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    tipo = data.get('tipo_usuario', 'gratuito')
    
    if not username or not email or not password:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 400
    
    if Usuario.query.filter_by(username=username).first():
        return jsonify({'error': 'El nombre de usuario ya existe'}), 400
    
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    es_edu = email.endswith('.edu') or '.edu.' in email
    if tipo == 'institucional' and not es_edu:
        return jsonify({'error': 'Email institucional debe ser .edu (ej: usuario@universidad.edu o usuario@uni.edu.mx)'}), 400
    
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    rol = data.get('rol', '')
    if not rol:
        rol = 'profesor' if tipo == 'institucional' else 'estudiante'
    elif rol not in ('estudiante', 'profesor'):
        return jsonify({'error': 'Rol inválido. Debe ser estudiante o profesor.'}), 400
    
    usuario = Usuario(
        username=username,
        email=email,
        password_hash=password_hash,
        rol=rol,
        tipo_usuario=tipo
    )
    db.session.add(usuario)
    db.session.commit()
    
    token = create_access_token(identity=str(usuario.id))
    
    return jsonify({
        'message': 'Registro exitoso',
        'token': token,
        'user': usuario.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400
    
    login_input = data.get('email', data.get('username', '')).strip().lower()
    password = data.get('password', '')
    
    if not login_input or not password:
        return jsonify({'error': 'Email/usuario y contraseña requeridos'}), 400
    
    usuario = Usuario.query.filter(
        (Usuario.email == login_input) | (Usuario.username == login_input)
    ).first()
    
    if not usuario:
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    if not bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    usuario.ultimo_login = date.today()
    db.session.commit()
    
    token = create_access_token(identity=str(usuario.id))
    
    return jsonify({
        'message': 'Login exitoso',
        'token': token,
        'user': usuario.to_dict()
    })


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    usuario = db.session.get(Usuario, user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'user': usuario.to_dict()})
