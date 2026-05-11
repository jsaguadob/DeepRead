from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import Usuario
from models.lectura import Lectura, Pregunta
from models.progreso import ProgresoLectura
from datetime import date
from services.ai_client import generar_quiz, chat_estadisticas, resumir_texto, chat_estudiante, explicar_pregunta, esta_listo

ai_bp = Blueprint('ai', __name__)

def get_current_user():
    user_id = int(get_jwt_identity())
    return db.session.get(Usuario, user_id)


@ai_bp.route('/generar-quiz', methods=['POST'])
@jwt_required()
def api_generar_quiz():
    user = get_current_user()
    if not user.es_admin() and not user.es_profesor():
        return jsonify({'error': 'Solo profesores y administradores'}), 403

    data = request.get_json()
    lectura_id = data.get('lectura_id')
    cantidad = int(data.get('cantidad', 5))

    if not lectura_id:
        return jsonify({'error': 'lectura_id requerido'}), 400

    lectura = db.session.get(Lectura, lectura_id)
    if not lectura:
        return jsonify({'error': 'Lectura no encontrada'}), 404

    if not lectura.contenido or len(lectura.contenido.strip()) < 10:
        return jsonify({'error': 'La lectura no tiene suficiente contenido'}), 400

    if not esta_listo():
        return jsonify({'error': 'IA no configurada. El administrador debe configurar GEMINI_API_KEY.'}), 503

    resultado = generar_quiz(lectura.contenido, lectura.nivel, cantidad)
    return jsonify(resultado)


@ai_bp.route('/chat', methods=['POST'])
@jwt_required()
def api_chat():
    user = get_current_user()
    if not user.es_admin() and not user.es_profesor():
        return jsonify({'error': 'Solo profesores y administradores'}), 403

    data = request.get_json()
    mensaje = data.get('mensaje', '').strip()
    if not mensaje:
        return jsonify({'error': 'Mensaje requerido'}), 400

    from models.actividad import ProgresoActividad
    from models.quiz import RespuestaQuiz

    progresos = ProgresoLectura.query.all()
    lecturas = Lectura.query.all()
    usuarios = Usuario.query.all()
    preguntas = Pregunta.query.all()

    # Stats por lectura
    lecturas_stats = {}
    for p in progresos:
        lid = p.lectura_id
        if lid not in lecturas_stats:
            lecturas_stats[lid] = {'intentos': 0, 'aprobados': 0, 'fallos': 0, 'completadas': 0}
        lecturas_stats[lid]['intentos'] += 1
        lecturas_stats[lid]['aprobados'] += 1 if p.quiz_aprobado else 0
        lecturas_stats[lid]['fallos'] += p.fallos or 0
        lecturas_stats[lid]['completadas'] += 1 if p.completada else 0

    # Stats por pregunta (cuál se falla más)
    respuestas = RespuestaQuiz.query.all()
    preguntas_stats = {}
    for r in respuestas:
        pid = r.pregunta_id
        if pid not in preguntas_stats:
            preguntas_stats[pid] = {'total': 0, 'errores': 0}
        preguntas_stats[pid]['total'] += 1
        if not r.correcta:
            preguntas_stats[pid]['errores'] += 1

    # Progreso por usuario y lectura
    progresos_por_usuario = {}
    for p in progresos:
        u = p.usuario_id
        if u not in progresos_por_usuario:
            progresos_por_usuario[u] = {'quizzes': 0, 'aprobados': 0, 'fallos': 0, 'completadas': 0, 'lecturas': {}}
        progresos_por_usuario[u]['quizzes'] += 1 if p.intentos > 0 else 0
        progresos_por_usuario[u]['aprobados'] += 1 if p.quiz_aprobado else 0
        progresos_por_usuario[u]['fallos'] += p.fallos or 0
        progresos_por_usuario[u]['completadas'] += 1 if p.completada else 0
        progresos_por_usuario[u]['lecturas'][str(p.lectura_id)] = {
            'aprobado': p.quiz_aprobado,
            'fallos': p.fallos or 0,
            'completada': p.completada,
        }

    titulos_lectura = {str(l.id): l.titulo for l in lecturas}
    textos_pregunta = {str(p.id): p.pregunta[:100] for p in preguntas}
    preguntas_por_lectura = {}
    for p in preguntas:
        preguntas_por_lectura.setdefault(str(p.lectura_id), []).append({
            'id': p.id, 'pregunta': p.pregunta[:100], 'respuesta_correcta': p.respuesta_correcta
        })

    # Respuestas por usuario (qué preguntas falló cada uno)
    respuestas_por_usuario = {}
    for r in respuestas:
        uid = r.usuario_id
        if uid not in respuestas_por_usuario:
            respuestas_por_usuario[uid] = {'total': 0, 'falladas': []}
        respuestas_por_usuario[uid]['total'] += 1
        if not r.correcta:
            respuestas_por_usuario[uid]['falladas'].append(r.pregunta_id)

    # Per-reading detail
    lecturas_detalle = {}
    for l in lecturas:
        s = lecturas_stats.get(l.id, {})
        lecturas_detalle[str(l.id)] = {
            'titulo': l.titulo,
            'total_intentos': s.get('intentos', 0),
            'veces_aprobado': s.get('aprobados', 0),
            'total_fallos': s.get('fallos', 0),
            'veces_completada': s.get('completadas', 0),
        }

    # Per-question detail
    preguntas_detalle = {}
    for p in preguntas:
        s = preguntas_stats.get(p.id, {})
        total = s.get('total', 0)
        errores = s.get('errores', 0)
        if total > 0:
            preguntas_detalle[str(p.id)] = {
                'lectura_id': p.lectura_id,
                'pregunta': p.pregunta[:100],
                'veces_respondida': total,
                'veces_fallada': errores,
                'porcentaje_error': round(errores / total * 100, 1),
            }

    usuarios_detalle = {}
    for u in usuarios:
        p = progresos_por_usuario.get(u.id, {})
        lecturas_usuario = {}
        for lid, info in p.get('lecturas', {}).items():
            lecturas_usuario[lid] = {
                'titulo': titulos_lectura.get(lid, 'Desconocida'),
                'aprobado': info['aprobado'],
                'fallos': info['fallos'],
                'completada': info['completada'],
            }
        # Preguntas que este usuario falló
        r = respuestas_por_usuario.get(u.id, {})
        preguntas_falladas = []
        for pid in r.get('falladas', []):
            ptexto = textos_pregunta.get(str(pid), '')
            # Buscar la lectura de esta pregunta
            lectura_preg = None
            for l in lecturas:
                if any(str(q['id']) == str(pid) for q in (preguntas_por_lectura.get(str(l.id), []))):
                    lectura_preg = l.titulo
                    break
            # Simple: buscar en preguntas_por_lectura
            for lid, qs in preguntas_por_lectura.items():
                for q in qs:
                    if q['id'] == pid:
                        lectura_preg = titulos_lectura.get(lid, '')
                        break
                if lectura_preg:
                    break
            preguntas_falladas.append({
                'pregunta': ptexto,
                'lectura': lectura_preg or '',
            })
        usuarios_detalle[u.username] = {
            'rol': u.rol,
            'lecturas_completadas': p.get('completadas', 0),
            'quizzes_realizados': p.get('quizzes', 0),
            'quizzes_aprobados': p.get('aprobados', 0),
            'total_fallos': p.get('fallos', 0),
            'puntos_totales': u.puntos_totales or 0,
            'lecturas': lecturas_usuario,
            'preguntas_falladas': preguntas_falladas,
        }

    contexto = {
        'total_usuarios': len(usuarios),
        'total_lecturas': len(lecturas),
        'total_preguntas': len(preguntas),
        'estudiantes': len([u for u in usuarios if u.rol == 'estudiante']),
        'profesores': len([u for u in usuarios if u.rol == 'profesor']),
        'quizzes_realizados': len([p for p in progresos if p.intentos > 0]),
        'quizzes_aprobados': len([p for p in progresos if p.quiz_aprobado]),
        'total_fallos': sum(p.fallos or 0 for p in progresos),
        'lecturas_completadas': len([p for p in progresos if p.completada]),
        'lecturas': lecturas_detalle,
        'preguntas_con_errores': preguntas_detalle,
        'usuarios': usuarios_detalle,
    }

    if not esta_listo():
        return jsonify({'error': 'IA no configurada'}), 503

    resultado = chat_estadisticas(mensaje, contexto)
    return jsonify(resultado)


@ai_bp.route('/resumir', methods=['POST'])
@jwt_required()
def api_resumir():
    data = request.get_json()
    lectura_id = data.get('lectura_id')

    if not lectura_id:
        return jsonify({'error': 'lectura_id requerido'}), 400

    lectura = db.session.get(Lectura, lectura_id)
    if not lectura:
        return jsonify({'error': 'Lectura no encontrada'}), 404

    if not esta_listo():
        return jsonify({'error': 'IA no configurada'}), 503

    resultado = resumir_texto(lectura.contenido)
    return jsonify(resultado)


@ai_bp.route('/consultar-lectura', methods=['POST'])
@jwt_required()
def api_consultar_lectura():
    user = get_current_user()
    if not user.es_estudiante():
        return jsonify({'error': 'Solo estudiantes'}), 403

    if not esta_listo():
        return jsonify({'error': 'IA no configurada'}), 503

    restantes = user.consultas_restantes_hoy()
    if restantes <= 0:
        limite = 30 if user.es_institucional() else 5
        return jsonify({'error': f'Límite diario alcanzado ({limite}/día). Vuelve mañana.'}), 429

    data = request.get_json()
    mensaje = data.get('mensaje', '').strip()
    lectura_id = data.get('lectura_id')

    if not mensaje or not lectura_id:
        return jsonify({'error': 'mensaje y lectura_id requeridos'}), 400

    lectura = db.session.get(Lectura, lectura_id)
    if not lectura:
        return jsonify({'error': 'Lectura no encontrada'}), 404

    user.usar_consulta()
    db.session.commit()

    resultado = chat_estudiante(mensaje, lectura.titulo, lectura.contenido or '')
    resultado['consultas_restantes_hoy'] = max(0, restantes - 1)
    return jsonify(resultado)


@ai_bp.route('/explicar-pregunta', methods=['POST'])
@jwt_required()
def api_explicar_pregunta():
    user = get_current_user()
    if not user.es_estudiante() or not user.es_institucional():
        return jsonify({'error': 'Solo estudiantes institucionales'}), 403

    if not esta_listo():
        return jsonify({'error': 'IA no configurada'}), 503

    data = request.get_json()
    pregunta_id = data.get('pregunta_id')
    if not pregunta_id:
        return jsonify({'error': 'pregunta_id requerido'}), 400

    pregunta = db.session.get(Pregunta, pregunta_id)
    if not pregunta:
        return jsonify({'error': 'Pregunta no encontrada'}), 404

    lectura = db.session.get(Lectura, pregunta.lectura_id)
    contexto = lectura.contenido[:2000] if lectura and lectura.contenido else ''

    resultado = explicar_pregunta(
        pregunta.pregunta,
        pregunta.opcion_a, pregunta.opcion_b,
        pregunta.opcion_c, pregunta.opcion_d,
        pregunta.respuesta_correcta,
        pregunta.explicacion or '',
        contexto
    )
    return jsonify(resultado)


@ai_bp.route('/mis-consultas', methods=['GET'])
@jwt_required()
def api_mis_consultas():
    user = get_current_user()
    restantes = user.consultas_restantes_hoy()
    limite = 30 if user.es_institucional() else 5
    return jsonify({
        'consultas_restantes': restantes,
        'limite_diario': limite
    })


@ai_bp.route('/status', methods=['GET'])
@jwt_required()
def api_status():
    return jsonify({'configurada': esta_listo()})
