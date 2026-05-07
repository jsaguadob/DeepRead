from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import Usuario
from models.lectura import Lectura, Pregunta
from models.progreso import ProgresoLectura
from models.grupo import Grupo, MiembroGrupo
from models.actividad import Actividad, ProgresoActividad
from datetime import datetime

activities_bp = Blueprint('activities', __name__)

def get_current_user():
    user_id = int(get_jwt_identity())
    return db.session.get(Usuario, user_id)


@activities_bp.route('', methods=['GET'])
@jwt_required()
def list_activities():
    user = get_current_user()
    mis_grupo_ids = [m.grupo_id for m in MiembroGrupo.query.filter_by(usuario_id=user.id).all()]
    
    if user.es_gratuito():
        actividades = Actividad.query.filter(
            Actividad.activa == True,
            Actividad.lectura_id.in_(
                db.session.query(Lectura.id).filter(Lectura.es_publica == True)
            )
        ).all()
    elif user.es_institucional():
        if mis_grupo_ids:
            actividades = Actividad.query.filter(
                Actividad.activa == True,
                Actividad.lectura_id.in_(
                    db.session.query(Lectura.id).filter(Lectura.grupo_id.in_(mis_grupo_ids))
                )
            ).all()
        else:
            actividades = []
    elif mis_grupo_ids:
        actividades = Actividad.query.filter(
            (Actividad.activa == True),
            (Actividad.lectura_id.in_(
                db.session.query(Lectura.id).filter(
                    (Lectura.grupo_id.in_(mis_grupo_ids)) | (Lectura.es_publica == True)
                )
            ))
        ).all()
    else:
        actividades = Actividad.query.filter(
            Actividad.activa == True,
            Actividad.lectura_id.in_(
                db.session.query(Lectura.id).filter(Lectura.es_publica == True)
            )
        ).all()
    
    result = []
    for a in actividades:
        d = a.to_dict()
        lectura = db.session.get(Lectura, a.lectura_id)
        d['lectura_titulo'] = lectura.titulo if lectura else None
        result.append(d)
    
    return jsonify({'actividades': result})


@activities_bp.route('/<int:actividad_id>', methods=['GET'])
@jwt_required()
def get_activity(actividad_id):
    user = get_current_user()
    actividad = db.session.get(Actividad, actividad_id)
    
    if not actividad:
        return jsonify({'error': 'Actividad no encontrada'}), 404
    
    progreso = ProgresoActividad.query.filter_by(
        usuario_id=user.id, actividad_id=actividad_id
    ).first()
    
    return jsonify({
        'actividad': actividad.to_dict(),
        'progreso': progreso.to_dict() if progreso else None,
        'completado': progreso.completado if progreso else False
    })


@activities_bp.route('', methods=['POST'])
@jwt_required()
def create_activity():
    user = get_current_user()
    if not user.es_admin() and not user.es_profesor():
        return jsonify({'error': 'No tienes permiso'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400
    
    lectura_id = data.get('lectura_id')
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    
    tipo = data.get('tipo', 'seleccionar')
    titulo = data.get('titulo', '').strip()
    contenido = data.get('contenido', '').strip()
    solucion = data.get('solucion', '').strip()
    puntos = int(data.get('puntos', 5))
    
    actividad = Actividad(
        lectura_id=lectura_id,
        titulo=titulo,
        tipo=tipo,
        contenido=contenido,
        solucion=solucion,
        nivel=1,
        puntos=puntos,
        tiempo_estimado=10,
        profesor_id=user.id
    )
    db.session.add(actividad)
    db.session.commit()
    
    return jsonify({'message': 'Actividad creada', 'actividad': actividad.to_dict()}), 201


@activities_bp.route('/<int:actividad_id>/submit', methods=['POST'])
@jwt_required()
def submit_activity(actividad_id):
    user = get_current_user()
    actividad = db.session.get(Actividad, actividad_id)
    
    if not actividad:
        return jsonify({'error': 'Actividad no encontrada'}), 404
    
    progreso = ProgresoActividad.query.filter_by(
        usuario_id=user.id, actividad_id=actividad_id
    ).first()
    
    if progreso and progreso.completado:
        return jsonify({'message': 'Ya completaste esta actividad', 'completado': True})
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400
    
    if actividad.tipo == 'sopa':
        encontradas_raw = data.get('encontradas', '')
        palabras_a_encontrar = set(p.strip().upper() for p in actividad.contenido.split(','))
        palabras_encontradas = set()
        if encontradas_raw:
            palabras_encontradas = set(p.strip().upper() for p in encontradas_raw.split(',') if p.strip())
        
        correcta = len(palabras_a_encontrar - palabras_encontradas) == 0
        faltantes = list(palabras_a_encontrar - palabras_encontradas)
    else:
        respuesta = data.get('respuesta', '').strip().lower()
        correcta = respuesta == actividad.solucion.lower()
        faltantes = []
    
    if not progreso:
        progreso = ProgresoActividad(
            usuario_id=user.id, actividad_id=actividad_id
        )
        db.session.add(progreso)
    
    if correcta:
        progreso.completado = True
        progreso.puntos_obtenidos = actividad.puntos
        progreso.respuesta = data.get('respuesta', '') if actividad.tipo != 'sopa' else ','.join(data.get('encontradas', ''))
        progreso.fecha_completado = datetime.utcnow()
        
        usuario_db = db.session.get(Usuario, user.id)
        if usuario_db:
            usuario_db.puntos_totales += actividad.puntos
        
        db.session.commit()
        return jsonify({
            'message': f'¡Completado! +{actividad.puntos} puntos',
            'completado': True,
            'puntos': actividad.puntos
        })
    
    db.session.commit()
    return jsonify({
        'message': 'Respuesta incorrecta. Intenta de nuevo.',
        'completado': False,
        'encontradas': len(palabras_encontradas) if actividad.tipo == 'sopa' else 0,
        'total_palabras': len(palabras_a_encontrar) if actividad.tipo == 'sopa' else 0,
        'faltantes': faltantes
    })


@activities_bp.route('/<int:actividad_id>', methods=['DELETE'])
@jwt_required()
def delete_activity(actividad_id):
    user = get_current_user()
    actividad = db.session.get(Actividad, actividad_id)
    
    if not actividad:
        return jsonify({'error': 'Actividad no encontrada'}), 404
    
    if not user.es_admin() and actividad.profesor_id != user.id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    db.session.delete(actividad)
    db.session.commit()
    
    return jsonify({'message': 'Actividad eliminada'})
