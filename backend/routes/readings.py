from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from extensions import db
from models.user import Usuario
from models.lectura import Lectura, Pregunta
from models.progreso import ProgresoLectura
from models.grupo import Grupo, MiembroGrupo
from datetime import datetime
import os
import tempfile

readings_bp = Blueprint('readings', __name__)

def get_current_user():
    user_id = int(get_jwt_identity())
    return db.session.get(Usuario, user_id)


@readings_bp.route('', methods=['GET'])
@jwt_required()
def list_readings():
    user = get_current_user()
    nivel = request.args.get('nivel', type=int)
    categoria = request.args.get('categoria')
    
    mis_grupo_ids = [m.grupo_id for m in MiembroGrupo.query.filter_by(usuario_id=user.id).all()]
    
    if user.es_admin():
        query = Lectura.query.filter_by(activa=True)
    elif user.es_profesor():
        query = Lectura.query.filter(
            (Lectura.activa == True),
            ((Lectura.profesor_id == user.id) | (Lectura.es_publica == True))
        )
    elif user.es_gratuito():
        query = Lectura.query.filter(Lectura.activa == True, Lectura.es_publica == True)
    elif user.es_institucional():
        if mis_grupo_ids:
            query = Lectura.query.filter(
                Lectura.activa == True,
                Lectura.grupo_id.in_(mis_grupo_ids)
            )
        else:
            query = Lectura.query.filter(Lectura.activa == False)
    elif mis_grupo_ids:
        query = Lectura.query.filter(
            (Lectura.activa == True),
            ((Lectura.grupo_id.in_(mis_grupo_ids)) | (Lectura.es_publica == True))
        )
    else:
        query = Lectura.query.filter(Lectura.activa == True, Lectura.es_publica == True)
    
    if nivel:
        query = query.filter_by(nivel=nivel)
    if categoria:
        query = query.filter_by(categoria=categoria)
    
    lecturas = query.all()
    
    completadas_ids = [
        p.lectura_id for p in ProgresoLectura.query.filter_by(
            usuario_id=user.id, completada=True
        ).all()
    ]
    
    categorias = [c[0] for c in db.session.query(Lectura.categoria).distinct().all() if c[0]]
    
    result = []
    for l in lecturas:
        d = l.to_dict()
        d['completada'] = l.id in completadas_ids
        result.append(d)
    
    return jsonify({
        'lecturas': result,
        'categorias': categorias
    })


@readings_bp.route('/<int:lectura_id>', methods=['GET'])
@jwt_required()
def get_reading(lectura_id):
    user = get_current_user()
    lectura = db.session.get(Lectura, lectura_id)
    
    if not lectura or not lectura.activa:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    
    if lectura.cerrada:
        return jsonify({'error': 'Esta lectura está cerrada', 'cerrada': True}), 403
    
    if lectura.fecha_cierre and lectura.fecha_cierre < datetime.utcnow():
        lectura.cerrada = True
        db.session.commit()
        return jsonify({'error': 'Esta lectura ha cerrado', 'cerrada': True}), 403
    
    mis_grupo_ids = [m.grupo_id for m in MiembroGrupo.query.filter_by(usuario_id=user.id).all()]
    
    tiene_acceso = False
    if user.es_admin():
        tiene_acceso = True
    elif user.es_profesor() and lectura.profesor_id == user.id:
        tiene_acceso = True
    elif lectura.es_publica and not user.es_institucional():
        tiene_acceso = True
    elif mis_grupo_ids and lectura.grupo_id in mis_grupo_ids and not user.es_gratuito():
        tiene_acceso = True
    
    if not tiene_acceso:
        return jsonify({'error': 'No tienes acceso a esta lectura'}), 403
    
    progreso = ProgresoLectura.query.filter_by(
        usuario_id=user.id, lectura_id=lectura_id
    ).first()
    
    preguntas = Pregunta.query.filter_by(lectura_id=lectura_id).all()
    tiene_quiz = len(preguntas) > 0
    
    try:
        from models.actividad import Actividad, ProgresoActividad
        actividades = Actividad.query.filter_by(lectura_id=lectura_id, activa=True).all()
        actividades_pendientes = []
        for a in actividades:
            prog = ProgresoActividad.query.filter_by(
                usuario_id=user.id, actividad_id=a.id, completado=True
            ).first()
            if not prog:
                actividades_pendientes.append(a)
        actividades = [a.to_dict() for a in actividades_pendientes]
    except:
        actividades = []
    
    sin_intentos = False
    if tiene_quiz and progreso and not progreso.quiz_aprobado:
        intentos_max = lectura.intentos_maximos or 3
        sin_intentos = progreso.intentos >= intentos_max
    
    return jsonify({
        'lectura': lectura.to_dict(),
        'progreso': progreso.to_dict() if progreso else None,
        'tiene_quiz': tiene_quiz,
        'quiz_completado': progreso.quiz_aprobado == True if (tiene_quiz and progreso) else False,
        'sin_intentos': sin_intentos,
        'total_preguntas': len(preguntas),
        'actividades': actividades
    })


@readings_bp.route('', methods=['POST'])
@jwt_required()
def create_reading():
    user = get_current_user()
    if not user.es_admin() and not user.es_profesor():
        return jsonify({'error': 'No tienes permiso para crear lecturas'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400
    
    if user.es_profesor() and not user.es_admin():
        if not data.get('grupo_id'):
            return jsonify({'error': 'Como profesor, debes crear lecturas dentro de un grupo'}), 400
        grupo = db.session.get(Grupo, data['grupo_id'])
        if not grupo or grupo.profesor_id != user.id:
            return jsonify({'error': 'No eres el profesor de este grupo'}), 403
        data['es_publica'] = False
    
    fecha_cierre = None
    if data.get('fecha_cierre'):
        try:
            fecha_cierre = datetime.strptime(data['fecha_cierre'], '%Y-%m-%dT%H:%M')
        except:
            pass
    
    lectura = Lectura(
        titulo=data.get('titulo'),
        contenido=data.get('contenido'),
        nivel=int(data.get('nivel', 1)),
        tiempo_estimado_minutos=int(data.get('tiempo_estimado_minutos', 10)),
        puntos_recompensa=int(data.get('puntos_recompensa', 100)),
        categoria=data.get('categoria'),
        profesor_id=user.id,
        grupo_id=data.get('grupo_id'),
        es_publica=data.get('es_publica', True),
        intentos_maximos=int(data.get('intentos_maximos', 3)),
        fecha_cierre=fecha_cierre
    )
    db.session.add(lectura)
    db.session.commit()
    
    return jsonify({'message': 'Lectura creada', 'lectura': lectura.to_dict()}), 201


def _texto_es_valido(texto):
    if not texto or len(texto.strip()) < 20:
        return False
    chars_alfa = sum(1 for c in texto if c.isalpha() or c.isspace())
    return (chars_alfa / max(len(texto), 1)) > 0.1

@readings_bp.route('/importar-archivo', methods=['POST'])
@jwt_required()
def importar_archivo():
    from services.ai_client import extraer_texto_archivo, procesar_texto_con_ia, esta_listo

    user = get_current_user()
    if not user.es_admin() and not user.es_profesor():
        return jsonify({'error': 'No tienes permiso'}), 403

    if 'archivo' not in request.files:
        return jsonify({'error': 'Archivo requerido'}), 400

    archivo = request.files['archivo']
    if archivo.filename == '':
        return jsonify({'error': 'Archivo vacío'}), 400

    ext = os.path.splitext(archivo.filename)[1].lower()
    if ext not in ('.pdf', '.docx', '.txt'):
        return jsonify({'error': 'Formato no soportado. Usa PDF, DOCX o TXT.'}), 400

    cantidad_preguntas = int(request.form.get('cantidad_preguntas', 5))
    necesita_ia = cantidad_preguntas > 0
    nivel_forzado = request.form.get('nivel')
    categoria = request.form.get('categoria', '')
    grupo_id = request.form.get('grupo_id')
    if grupo_id:
        grupo_id = int(grupo_id)

    if necesita_ia and not esta_listo():
        return jsonify({'error': 'IA no configurada. Para subir sin generar preguntas, desmarca "Generar preguntas automáticamente".'}), 503

    if user.es_profesor() and not user.es_admin():
        if not grupo_id:
            return jsonify({'error': 'Como profesor, debes asignar la lectura a un grupo'}), 400
        grupo = db.session.get(Grupo, grupo_id)
        if not grupo or grupo.profesor_id != user.id:
            return jsonify({'error': 'No eres el profesor de este grupo'}), 403

    fd, tmp_path = tempfile.mkstemp(suffix=ext)
    os.close(fd)
    try:
        archivo.save(tmp_path)

        texto = extraer_texto_archivo(tmp_path, ext)
        if not _texto_es_valido(texto):
            return jsonify({'error': 'No se pudo extraer texto válido del archivo. Asegúrate de que no sea un PDF escaneado o esté corrupto.'}), 400

        if necesita_ia and esta_listo():
            resultado_ia = procesar_texto_con_ia(texto, cantidad_preguntas)
            if 'error' in resultado_ia:
                titulo = os.path.splitext(archivo.filename)[0][:200]
                contenido = texto[:50000]
                nivel = int(nivel_forzado) if nivel_forzado else 2
                preguntas_data = []
            else:
                titulo = resultado_ia.get('titulo_sugerido', os.path.splitext(archivo.filename)[0])[:200]
                contenido = resultado_ia.get('contenido_limpio', texto)[:50000]
                nivel = int(nivel_forzado) if nivel_forzado else int(resultado_ia.get('nivel_sugerido', 2))
                preguntas_data = resultado_ia.get('preguntas', [])
        else:
            titulo = os.path.splitext(archivo.filename)[0][:200]
            contenido = texto[:50000]
            nivel = int(nivel_forzado) if nivel_forzado else 2
            preguntas_data = []

        if user.es_profesor() and not user.es_admin():
            es_publica = False
        else:
            es_publica = request.form.get('es_publica', 'true').lower() == 'true'

        lectura = Lectura(
            titulo=titulo,
            contenido=contenido,
            nivel=nivel,
            tiempo_estimado_minutos=int(request.form.get('tiempo_estimado_minutos', 10)),
            puntos_recompensa=int(request.form.get('puntos_recompensa', 100)),
            categoria=categoria or None,
            profesor_id=user.id,
            grupo_id=grupo_id,
            es_publica=es_publica,
            intentos_maximos=int(request.form.get('intentos_maximos', 3))
        )
        db.session.add(lectura)
        db.session.flush()

        preguntas_creadas = []
        for q in preguntas_data:
            if all(k in q for k in ('pregunta', 'opcion_a', 'opcion_b', 'opcion_c', 'opcion_d', 'respuesta_correcta')):
                pregunta = Pregunta(
                    lectura_id=lectura.id,
                    pregunta=q['pregunta'],
                    opcion_a=q['opcion_a'],
                    opcion_b=q['opcion_b'],
                    opcion_c=q['opcion_c'],
                    opcion_d=q['opcion_d'],
                    respuesta_correcta=q['respuesta_correcta'],
                    explicacion=q.get('explicacion', ''),
                    profesor_id=user.id
                )
                db.session.add(pregunta)
                preguntas_creadas.append(pregunta)

        db.session.commit()

        return jsonify({
            'message': f'Lectura importada con {len(preguntas_creadas)} preguntas',
            'lectura': lectura.to_dict(),
            'total_preguntas': len(preguntas_creadas)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al importar: {str(e)}'}), 500
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass


@readings_bp.route('/<int:lectura_id>', methods=['PUT'])
@jwt_required()
def update_reading(lectura_id):
    user = get_current_user()
    lectura = db.session.get(Lectura, lectura_id)
    
    if not lectura:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    
    if not user.es_admin() and lectura.profesor_id != user.id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    data = request.get_json()
    if data.get('titulo'): lectura.titulo = data['titulo']
    if data.get('contenido'): lectura.contenido = data['contenido']
    if data.get('nivel'): lectura.nivel = int(data['nivel'])
    if data.get('tiempo_estimado_minutos'): lectura.tiempo_estimado_minutos = int(data['tiempo_estimado_minutos'])
    if data.get('puntos_recompensa'): lectura.puntos_recompensa = int(data['puntos_recompensa'])
    if data.get('categoria'): lectura.categoria = data['categoria']
    if data.get('intentos_maximos'): lectura.intentos_maximos = int(data['intentos_maximos'])
    if data.get('cerrada') is not None: lectura.cerrada = data['cerrada']
    if data.get('fecha_cierre'):
        try:
            lectura.fecha_cierre = datetime.strptime(data['fecha_cierre'], '%Y-%m-%dT%H:%M')
        except:
            pass
    
    db.session.commit()
    return jsonify({'message': 'Lectura actualizada', 'lectura': lectura.to_dict()})


@readings_bp.route('/<int:lectura_id>', methods=['DELETE'])
@jwt_required()
def delete_reading(lectura_id):
    user = get_current_user()
    lectura = db.session.get(Lectura, lectura_id)
    
    if not lectura:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    
    if not user.es_admin() and lectura.profesor_id != user.id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    Pregunta.query.filter_by(lectura_id=lectura_id).delete()
    db.session.delete(lectura)
    db.session.commit()
    
    return jsonify({'message': 'Lectura eliminada'})


@readings_bp.route('/<int:lectura_id>/replicar', methods=['POST'])
@jwt_required()
def replicar_lectura(lectura_id):
    user = get_current_user()
    if not user.es_admin() and not user.es_profesor():
        return jsonify({'error': 'No tienes permiso'}), 403

    original = db.session.get(Lectura, lectura_id)
    if not original:
        return jsonify({'error': 'Lectura no encontrada'}), 404

    if user.es_profesor() and not user.es_admin() and original.profesor_id != user.id:
        return jsonify({'error': 'No eres el dueño de esta lectura'}), 403

    data = request.get_json()
    grupo_destino_id = data.get('grupo_id')
    if not grupo_destino_id:
        return jsonify({'error': 'grupo_id requerido'}), 400

    grupo = db.session.get(Grupo, grupo_destino_id)
    if not grupo:
        return jsonify({'error': 'Grupo no encontrado'}), 404

    if user.es_profesor() and not user.es_admin() and grupo.profesor_id != user.id:
        return jsonify({'error': 'No eres el profesor de este grupo'}), 403

    copia = Lectura(
        titulo=original.titulo,
        contenido=original.contenido,
        nivel=original.nivel,
        tiempo_estimado_minutos=original.tiempo_estimado_minutos,
        puntos_recompensa=original.puntos_recompensa,
        categoria=original.categoria,
        profesor_id=user.id,
        grupo_id=grupo_destino_id,
        es_publica=False,
        activa=True,
        intentos_maximos=original.intentos_maximos
    )
    db.session.add(copia)
    db.session.flush()

    preguntas_originales = Pregunta.query.filter_by(lectura_id=lectura_id).all()
    for pq in preguntas_originales:
        copia_pregunta = Pregunta(
            lectura_id=copia.id,
            pregunta=pq.pregunta,
            opcion_a=pq.opcion_a,
            opcion_b=pq.opcion_b,
            opcion_c=pq.opcion_c,
            opcion_d=pq.opcion_d,
            respuesta_correcta=pq.respuesta_correcta,
            explicacion=pq.explicacion,
            profesor_id=user.id
        )
        db.session.add(copia_pregunta)

    db.session.commit()

    return jsonify({
        'message': f'Lectura "{original.titulo}" replicada al grupo "{grupo.nombre}"',
        'lectura': copia.to_dict(),
        'total_preguntas': len(preguntas_originales)
    }), 201


@readings_bp.route('/<int:lectura_id>/completar', methods=['POST'])
@jwt_required()
def complete_reading(lectura_id):
    user = get_current_user()
    lectura = db.session.get(Lectura, lectura_id)
    
    if not lectura:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    
    preguntas = Pregunta.query.filter_by(lectura_id=lectura_id).all()
    tiene_quiz = len(preguntas) > 0
    
    progreso = ProgresoLectura.query.filter_by(
        usuario_id=user.id, lectura_id=lectura_id
    ).first()
    
    quiz_completado = False
    sin_intentos = False
    if tiene_quiz and progreso:
        quiz_completado = progreso.quiz_aprobado == True
        intentos_max = lectura.intentos_maximos or 3
        sin_intentos = progreso.intentos >= intentos_max and not quiz_completado
    
    if tiene_quiz and not quiz_completado and not sin_intentos:
        return jsonify({'error': 'Aproba el quiz con 80% para terminar la lectura'}), 400
    
    if not progreso:
        progreso = ProgresoLectura(
            usuario_id=user.id, lectura_id=lectura_id,
            completada=False, puntos_obtenidos=0
        )
        db.session.add(progreso)
    
    progreso.completada = True
    progreso.fecha_completado = datetime.utcnow()
    
    puntos_otorgados = 0
    if sin_intentos:
        puntos_otorgados = max(1, lectura.puntos_recompensa // 5)
        progreso.puntos_obtenidos = puntos_otorgados
    else:
        puntos_otorgados = lectura.puntos_recompensa
        progreso.puntos_obtenidos = puntos_otorgados
    
    usuario_db = db.session.get(Usuario, user.id)
    if usuario_db and puntos_otorgados > 0:
        usuario_db.puntos_totales += puntos_otorgados
        nuevo_nivel = (usuario_db.puntos_totales // 500) + 1
        if nuevo_nivel > usuario_db.nivel_actual and nuevo_nivel <= 3:
            usuario_db.nivel_actual = nuevo_nivel
    
    db.session.commit()
    
    if sin_intentos:
        mensaje = f'Lectura completada (sin aprobar el quiz). +{puntos_otorgados} punto(s) de esfuerzo.'
    else:
        mensaje = f'Lectura completada! +{puntos_otorgados} puntos'
    
    return jsonify({
        'message': mensaje,
        'sin_quiz': sin_intentos,
        'puntos_otorgados': puntos_otorgados,
        'puntos_totales': usuario_db.puntos_totales if usuario_db else 0,
        'nivel_actual': usuario_db.nivel_actual if usuario_db else 1
    })
