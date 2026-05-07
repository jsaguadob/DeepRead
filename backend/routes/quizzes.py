from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import Usuario
from models.lectura import Lectura, Pregunta
from models.progreso import ProgresoLectura
from models.grupo import Grupo, MiembroGrupo
from datetime import datetime
import secrets

quizzes_bp = Blueprint('quizzes', __name__)

def get_current_user():
    user_id = int(get_jwt_identity())
    return db.session.get(Usuario, user_id)


# --- Question CRUD ---

@quizzes_bp.route('/lecturas/<int:lectura_id>/preguntas', methods=['GET'])
@jwt_required()
def get_questions(lectura_id):
    user = get_current_user()
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    
    preguntas = Pregunta.query.filter_by(lectura_id=lectura_id).all()
    progreso = ProgresoLectura.query.filter_by(
        usuario_id=user.id, lectura_id=lectura_id
    ).first()
    
    intentos_max = lectura.intentos_maximos or 3
    intentos_usados = progreso.intentos if progreso else 0
    bloqueado = intentos_usados >= intentos_max
    
    if user.es_admin() or user.es_profesor():
        return jsonify({
            'preguntas': [p.to_dict() for p in preguntas],
            'total': len(preguntas)
        })
    else:
        return jsonify({
            'preguntas': [{
                'id': p.id,
                'lectura_id': p.lectura_id,
                'pregunta': p.pregunta,
                'opcion_a': p.opcion_a,
                'opcion_b': p.opcion_b,
                'opcion_c': p.opcion_c,
                'opcion_d': p.opcion_d
            } for p in preguntas],
            'total': len(preguntas),
            'bloqueado': bloqueado,
            'quiz_aprobado': progreso.quiz_aprobado if progreso else False,
            'intentos_usados': intentos_usados,
            'intentos_max': intentos_max
        })


@quizzes_bp.route('/lecturas/<int:lectura_id>/preguntas', methods=['POST'])
@jwt_required()
def create_question(lectura_id):
    user = get_current_user()
    if not user.es_admin() and not user.es_profesor():
        return jsonify({'error': 'No tienes permiso'}), 403
    
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    
    if not user.es_admin() and lectura.profesor_id != user.id:
        return jsonify({'error': 'No tienes permiso para esta lectura'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400
    
    pregunta = Pregunta(
        lectura_id=lectura_id,
        pregunta=data.get('pregunta'),
        opcion_a=data.get('opcion_a'),
        opcion_b=data.get('opcion_b'),
        opcion_c=data.get('opcion_c'),
        opcion_d=data.get('opcion_d'),
        respuesta_correcta=data.get('respuesta_correcta'),
        explicacion=data.get('explicacion'),
        profesor_id=user.id
    )
    db.session.add(pregunta)
    db.session.commit()
    
    return jsonify({'message': 'Pregunta agregada', 'pregunta': pregunta.to_dict()}), 201


@quizzes_bp.route('/lecturas/<int:lectura_id>/preguntas/batch', methods=['POST'])
@jwt_required()
def create_questions_batch(lectura_id):
    user = get_current_user()
    if not user.es_admin() and not user.es_profesor():
        return jsonify({'error': 'No tienes permiso'}), 403
    
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    
    if not user.es_admin() and lectura.profesor_id != user.id:
        return jsonify({'error': 'No tienes permiso para esta lectura'}), 403
    
    data = request.get_json()
    if not data or not isinstance(data.get('preguntas'), list):
        return jsonify({'error': 'Lista de preguntas requerida'}), 400
    
    preguntas_creadas = []
    for q_data in data['preguntas']:
        pregunta = Pregunta(
            lectura_id=lectura_id,
            pregunta=q_data.get('pregunta'),
            opcion_a=q_data.get('opcion_a'),
            opcion_b=q_data.get('opcion_b'),
            opcion_c=q_data.get('opcion_c'),
            opcion_d=q_data.get('opcion_d'),
            respuesta_correcta=q_data.get('respuesta_correcta'),
            explicacion=q_data.get('explicacion'),
            profesor_id=user.id
        )
        db.session.add(pregunta)
        preguntas_creadas.append(pregunta)
    
    db.session.commit()
    
    return jsonify({
        'message': f'{len(preguntas_creadas)} preguntas agregadas',
        'preguntas': [p.to_dict() for p in preguntas_creadas]
    }), 201


@quizzes_bp.route('/preguntas/<int:pregunta_id>', methods=['PUT'])
@jwt_required()
def update_question(pregunta_id):
    user = get_current_user()
    pregunta = db.session.get(Pregunta, pregunta_id)
    
    if not pregunta:
        return jsonify({'error': 'Pregunta no encontrada'}), 404
    
    if not user.es_admin() and pregunta.profesor_id != user.id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    data = request.get_json()
    if data.get('pregunta'): pregunta.pregunta = data['pregunta']
    if data.get('opcion_a'): pregunta.opcion_a = data['opcion_a']
    if data.get('opcion_b'): pregunta.opcion_b = data['opcion_b']
    if data.get('opcion_c'): pregunta.opcion_c = data['opcion_c']
    if data.get('opcion_d'): pregunta.opcion_d = data['opcion_d']
    if data.get('respuesta_correcta'): pregunta.respuesta_correcta = data['respuesta_correcta']
    if data.get('explicacion') is not None: pregunta.explicacion = data['explicacion']
    
    db.session.commit()
    return jsonify({'message': 'Pregunta actualizada', 'pregunta': pregunta.to_dict()})


@quizzes_bp.route('/preguntas/<int:pregunta_id>', methods=['DELETE'])
@jwt_required()
def delete_question(pregunta_id):
    user = get_current_user()
    pregunta = db.session.get(Pregunta, pregunta_id)
    
    if not pregunta:
        return jsonify({'error': 'Pregunta no encontrada'}), 404
    
    if not user.es_admin() and pregunta.profesor_id != user.id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    db.session.delete(pregunta)
    db.session.commit()
    
    return jsonify({'message': 'Pregunta eliminada'})


# --- Quiz taking ---

@quizzes_bp.route('/lecturas/<int:lectura_id>/quiz/submit', methods=['POST'])
@jwt_required()
def submit_quiz(lectura_id):
    user = get_current_user()
    lectura = db.session.get(Lectura, lectura_id)
    
    if not lectura:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    
    if lectura.cerrada:
        return jsonify({'error': 'Esta lectura está cerrada'}), 403
    
    if lectura.fecha_cierre and lectura.fecha_cierre < datetime.utcnow():
        lectura.cerrada = True
        db.session.commit()
        return jsonify({'error': 'El plazo ha vencido'}), 403
    
    preguntas = Pregunta.query.filter_by(lectura_id=lectura_id).all()
    if not preguntas:
        return jsonify({'error': 'No hay preguntas para este quiz'}), 404
    
    progreso = ProgresoLectura.query.filter_by(
        usuario_id=user.id, lectura_id=lectura_id
    ).first()
    
    intentos_actuales = progreso.intentos if progreso else 0
    intentos_max = lectura.intentos_maximos or 3
    
    if intentos_actuales >= intentos_max:
        return jsonify({'error': 'Sin intentos disponibles'}), 400
    
    data = request.get_json()
    if not data or not isinstance(data.get('respuestas'), dict):
        return jsonify({'error': 'Respuestas requeridas'}), 400
    
    respuestas = data['respuestas']
    correctas = 0
    detalles = []
    
    for pregunta in preguntas:
        respuesta_usuario = respuestas.get(f'pregunta_{pregunta.id}', '')
        es_correcta = respuesta_usuario == pregunta.respuesta_correcta
        if es_correcta:
            correctas += 1
        detalles.append({
            'pregunta_id': pregunta.id,
            'respondida': respuesta_usuario,
            'correcta': es_correcta,
            'respuesta_correcta': pregunta.respuesta_correcta
        })
    
    total = len(preguntas)
    incorrectas = total - correctas
    porcentaje = (correctas / total * 100) if total > 0 else 0
    puntos_por_pregunta = 5.0 / total
    puntos = int(correctas * puntos_por_pregunta * 100) / 100 if correctas > 0 else 0
    
    if lectura.cerrada and puntos > 0:
        puntos = int(puntos * 0.5)
    
    quiz_aprobado = porcentaje >= 80
    
    if progreso:
        progreso.intentos = intentos_actuales + 1
        progreso.puntos_obtenidos = puntos
        progreso.quiz_aprobado = quiz_aprobado
        progreso.quiz_porcentaje = porcentaje
        progreso.fallos = progreso.fallos + incorrectas
        progreso.fecha_completado = datetime.utcnow()
    else:
        progreso = ProgresoLectura(
            usuario_id=user.id, lectura_id=lectura_id,
            completada=False, puntos_obtenidos=puntos,
            intentos=1, quiz_aprobado=quiz_aprobado,
            quiz_porcentaje=porcentaje, fallos=incorrectas,
            fecha_completado=datetime.utcnow()
        )
        db.session.add(progreso)
    
    if puntos > 0 and quiz_aprobado:
        usuario_db = db.session.get(Usuario, user.id)
        if usuario_db:
            usuario_db.puntos_totales += puntos
    
    db.session.commit()
    
    intentos_restantes = intentos_max - intentos_actuales - 1
    mostrar_feedback = quiz_aprobado or intentos_restantes <= 0
    puede_completar_sin_quiz = intentos_restantes <= 0 and not quiz_aprobado

    return jsonify({
        'message': 'Quiz completado',
        'resultado': {
            'correctas': correctas,
            'incorrectas': incorrectas,
            'total': total,
            'porcentaje': porcentaje,
            'puntos': puntos,
            'aprobado': quiz_aprobado,
            'intentos_restantes': intentos_restantes,
            'mostrar_feedback': mostrar_feedback,
            'puede_completar_sin_quiz': puede_completar_sin_quiz
        },
        'detalles': detalles if mostrar_feedback else [],
        'explicaciones': [{
            'id': p.id,
            'pregunta': p.pregunta,
            'respuesta_correcta': p.respuesta_correcta,
            'explicacion': p.explicacion
        } for p in preguntas] if mostrar_feedback else []
    })
