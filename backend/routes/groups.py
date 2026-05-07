from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import Usuario
from models.lectura import Lectura, Pregunta
from models.progreso import ProgresoLectura
from models.grupo import Grupo, MiembroGrupo
from datetime import datetime
import random
import string

groups_bp = Blueprint('groups', __name__)

def get_current_user():
    user_id = int(get_jwt_identity())
    return db.session.get(Usuario, user_id)

def gerar_codigo(length=6):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


@groups_bp.route('', methods=['GET'])
@jwt_required()
def list_groups():
    user = get_current_user()
    
    grupos_creados = []
    if user.es_profesor() or user.es_admin():
        q = Grupo.query.filter_by(profesor_id=user.id)
        if user.es_admin():
            q = Grupo.query
        grupos_creados = [g.to_dict() for g in q.all()]
    
    miembro_grupos = MiembroGrupo.query.filter_by(usuario_id=user.id).all()
    grupos_miembro = []
    for m in miembro_grupos:
        grupo = db.session.get(Grupo, m.grupo_id)
        if grupo and grupo.activo:
            d = grupo.to_dict()
            d['rol'] = m.rol_en_grupo
            d['es_dueno'] = grupo.profesor_id == user.id
            lecturas = Lectura.query.filter_by(grupo_id=grupo.id).all()
            d['lecturas'] = [{
                'id': l.id, 'titulo': l.titulo,
                'nivel': l.nivel, 'tiempo': l.tiempo_estimado_minutos,
                'puntos': l.puntos_recompensa
            } for l in lecturas]
            grupos_miembro.append(d)
    
    return jsonify({
        'grupos_creados': grupos_creados,
        'grupos': grupos_miembro
    })


@groups_bp.route('', methods=['POST'])
@jwt_required()
def create_group():
    user = get_current_user()
    if not user.es_profesor():
        return jsonify({'error': 'Solo profesores pueden crear grupos'}), 403
    
    data = request.get_json()
    if not data or not data.get('nombre'):
        return jsonify({'error': 'Nombre del grupo requerido'}), 400
    
    codigo = gerar_codigo(6)
    
    grupo = Grupo(
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        profesor_id=user.id,
        codigo_unico=codigo
    )
    db.session.add(grupo)
    db.session.flush()
    
    miembro = MiembroGrupo(
        grupo_id=grupo.id,
        usuario_id=user.id,
        rol_en_grupo='profesor'
    )
    db.session.add(miembro)
    db.session.commit()
    
    return jsonify({
        'message': f'Grupo "{grupo.nombre}" creado',
        'grupo': grupo.to_dict(),
        'codigo': codigo
    }), 201


@groups_bp.route('/unirse', methods=['POST'])
@jwt_required()
def join_group():
    user = get_current_user()
    data = request.get_json()
    if not data or not data.get('codigo'):
        return jsonify({'error': 'Código requerido'}), 400
    
    codigo = data['codigo'].strip().upper()
    grupo = Grupo.query.filter_by(codigo_unico=codigo, activo=True).first()
    
    if not grupo:
        return jsonify({'error': 'Código de grupo no válido'}), 404
    
    existente = MiembroGrupo.query.filter_by(
        grupo_id=grupo.id, usuario_id=user.id
    ).first()
    
    if existente:
        return jsonify({'message': 'Ya eres miembro de este grupo', 'grupo': grupo.to_dict()})
    
    miembro = MiembroGrupo(
        grupo_id=grupo.id,
        usuario_id=user.id,
        rol_en_grupo='estudiante'
    )
    db.session.add(miembro)
    db.session.commit()
    
    return jsonify({
        'message': f'Te uniste al grupo "{grupo.nombre}"',
        'grupo': grupo.to_dict()
    })


@groups_bp.route('/<int:grupo_id>', methods=['GET'])
@jwt_required()
def get_group(grupo_id):
    user = get_current_user()
    grupo = db.session.get(Grupo, grupo_id)
    
    if not grupo:
        return jsonify({'error': 'Grupo no encontrado'}), 404
    
    tiene_acceso = False
    if user.es_admin():
        tiene_acceso = True
    elif user.es_profesor() and grupo.profesor_id == user.id:
        tiene_acceso = True
    else:
        miembro = MiembroGrupo.query.filter_by(grupo_id=grupo_id, usuario_id=user.id).first()
        if miembro:
            tiene_acceso = True
    
    if not tiene_acceso:
        return jsonify({'error': 'No tienes acceso a este grupo'}), 403
    
    miembros = []
    if user.es_admin() or (user.es_profesor() and grupo.profesor_id == user.id):
        miembros_rows = MiembroGrupo.query.filter_by(grupo_id=grupo_id).all()
        for m in miembros_rows:
            usuario = db.session.get(Usuario, m.usuario_id)
            completadas = ProgresoLectura.query.filter_by(
                usuario_id=usuario.id, completada=True
            ).count()
            miembros.append({
                'id': usuario.id, 'username': usuario.username,
                'email': usuario.email, 'rol': m.rol_en_grupo,
                'puntos': usuario.puntos_totales, 'nivel': usuario.nivel_actual,
                'completadas': completadas
            })
    
    lecturas = Lectura.query.filter_by(grupo_id=grupo_id).all()
    es_dueno = user.es_admin() or (user.es_profesor() and grupo.profesor_id == user.id)
    
    return jsonify({
        'grupo': grupo.to_dict(),
        'miembros': miembros,
        'lecturas': [l.to_dict() for l in lecturas],
        'es_dueno': es_dueno
    })


@groups_bp.route('/<int:grupo_id>/miembros/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
def remove_member(grupo_id, usuario_id):
    user = get_current_user()
    grupo = db.session.get(Grupo, grupo_id)
    
    if not grupo:
        return jsonify({'error': 'Grupo no encontrado'}), 404
    
    if grupo.profesor_id != user.id and not user.es_admin():
        return jsonify({'error': 'No tienes permiso'}), 403
    
    miembro = MiembroGrupo.query.filter_by(grupo_id=grupo_id, usuario_id=usuario_id).first()
    if miembro:
        db.session.delete(miembro)
        db.session.commit()
        return jsonify({'message': 'Miembro eliminado'})
    
    return jsonify({'error': 'Miembro no encontrado'}), 404


@groups_bp.route('/<int:grupo_id>/calificaciones', methods=['GET'])
@jwt_required()
def get_grades(grupo_id):
    user = get_current_user()
    grupo = db.session.get(Grupo, grupo_id)
    
    if not grupo or grupo.profesor_id != user.id:
        return jsonify({'error': 'Solo el profesor puede ver calificaciones'}), 403
    
    try:
        from models.actividad import ProgresoActividad, Actividad
    except:
        ProgresoActividad = None
        Actividad = None
    
    miembros = MiembroGrupo.query.filter_by(grupo_id=grupo_id).all()
    estudiantes = []
    for m in miembros:
        if m.rol_en_grupo == 'estudiante':
            usuario = db.session.get(Usuario, m.usuario_id)
            progresos = ProgresoLectura.query.filter_by(usuario_id=usuario.id).all()
            
            total_puntos = 0
            lecturas_completadas = 0
            quizzes_completados = 0
            quizzes_fallados = 0
            total_fallos = 0
            actividades_completadas = 0
            lecturas_detalle = []
            
            for p in progresos:
                lectura = db.session.get(Lectura, p.lectura_id)
                if not (lectura and lectura.grupo_id == grupo_id):
                    continue
                
                total_puntos += p.puntos_obtenidos
                
                if p.completada:
                    lecturas_completadas += 1
                
                if p.quiz_aprobado:
                    quizzes_completados += 1
                elif p.intentos > 0:
                    quizzes_fallados += 1
                
                total_fallos += p.fallos
                
                lecturas_detalle.append({
                    'titulo': lectura.titulo,
                    'puntos': p.puntos_obtenidos,
                    'intentos': p.intentos,
                    'fallos': p.fallos,
                    'quiz_aprobado': p.quiz_aprobado,
                    'completada': p.completada,
                    'completada_sin_quiz': p.completada and not p.quiz_aprobado,
                    'fecha': p.fecha_completado.isoformat() if p.fecha_completado else None
                })
            
            if ProgresoActividad and Actividad:
                actividades = Actividad.query.filter_by(lectura_id=grupo_id).all()
                for act in actividades:
                    prog_act = ProgresoActividad.query.filter_by(
                        usuario_id=usuario.id, actividad_id=act.id, completado=True
                    ).first()
                    if prog_act:
                        actividades_completadas += 1
                        total_puntos += prog_act.puntos_obtenidos
            
            dias_activos = []
            for p in progresos:
                if p.fecha_completado:
                    dia = p.fecha_completado.date()
                    if dia not in dias_activos:
                        dias_activos.append(dia)
            
            estudiantes.append({
                'id': usuario.id, 'username': usuario.username,
                'email': usuario.email, 'puntos': total_puntos,
                'lecturas_completadas': lecturas_completadas,
                'quizzes_completados': quizzes_completados,
                'quizzes_fallados': quizzes_fallados,
                'total_fallos': total_fallos,
                'actividades_completadas': actividades_completadas,
                'nivel': usuario.nivel_actual, 'dias_activos': len(dias_activos),
                'lecturas': lecturas_detalle
            })
    
    estudiantes.sort(key=lambda x: x['puntos'], reverse=True)
    return jsonify({'grupo': grupo.to_dict(), 'estudiantes': estudiantes})


@groups_bp.route('/<int:grupo_id>/cerrar_lectura/<int:lectura_id>', methods=['POST'])
@jwt_required()
def toggle_lecture_closure(grupo_id, lectura_id):
    user = get_current_user()
    grupo = db.session.get(Grupo, grupo_id)
    
    if not grupo or grupo.profesor_id != user.id:
        return jsonify({'error': 'Solo el profesor puede cerrar lecturas'}), 403
    
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura or lectura.grupo_id != grupo_id:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    
    data = request.get_json()
    accion = data.get('accion', 'cerrar')
    
    if accion == 'reabrir':
        lectura.cerrada = False
        lectura.fecha_cierre = None
        message = 'Lectura reabierta'
    else:
        fecha_cierre = data.get('fecha_cierre')
        if fecha_cierre:
            lectura.fecha_cierre = datetime.strptime(fecha_cierre, '%Y-%m-%dT%H:%M')
            message = f'Fecha límite establecida'
        else:
            lectura.cerrada = True
            message = 'Lectura cerrada'
    
    db.session.commit()
    return jsonify({'message': message, 'lectura': lectura.to_dict()})


@groups_bp.route('/<int:grupo_id>/estado_lectura/<int:lectura_id>', methods=['GET'])
@jwt_required()
def get_lecture_status(grupo_id, lectura_id):
    user = get_current_user()
    grupo = db.session.get(Grupo, grupo_id)
    
    if not grupo or grupo.profesor_id != user.id:
        return jsonify({'error': 'Solo el profesor puede ver esto'}), 403
    
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura or lectura.grupo_id != grupo_id:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    
    miembros = MiembroGrupo.query.filter_by(grupo_id=grupo_id).all()
    
    completados = []
    no_completados = []
    
    for m in miembros:
        if m.rol_en_grupo == 'estudiante':
            usuario = db.session.get(Usuario, m.usuario_id)
            progreso = ProgresoLectura.query.filter_by(
                usuario_id=usuario.id, lectura_id=lectura_id
            ).first()
            
            if progreso and progreso.completada:
                completados.append({
                    'username': usuario.username,
                    'puntos': progreso.puntos_obtenidos,
                    'fecha': progreso.fecha_completado.isoformat() if progreso.fecha_completado else None
                })
            else:
                no_completados.append({
                    'username': usuario.username,
                    'email': usuario.email
                })
    
    return jsonify({
        'lectura': lectura.to_dict(),
        'completados': completados,
        'no_completados': no_completados
    })
