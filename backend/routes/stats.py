from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import Usuario
from models.lectura import Lectura, Pregunta
from models.progreso import ProgresoLectura

stats_bp = Blueprint('stats', __name__)

def get_current_user():
    user_id = int(get_jwt_identity())
    return db.session.get(Usuario, user_id)


@stats_bp.route('/progreso', methods=['GET'])
@jwt_required()
def get_progress():
    user = get_current_user()
    
    progresos = ProgresoLectura.query.filter_by(usuario_id=user.id).all()
    lecturas_completadas = []
    quiz_historial = []
    total_fallos = 0
    for p in progresos:
        lectura = db.session.get(Lectura, p.lectura_id)
        if not lectura:
            continue
        if p.completada:
            lecturas_completadas.append({
                'titulo': lectura.titulo,
                'nivel': lectura.nivel,
                'puntos': p.puntos_obtenidos,
                'fecha': p.fecha_completado.isoformat() if p.fecha_completado else None
            })
        if p.intentos > 0:
            quiz_historial.append({
                'lectura': lectura.titulo,
                'nivel': lectura.nivel,
                'intentos': p.intentos,
                'aprobado': p.quiz_aprobado,
                'porcentaje': p.quiz_porcentaje,
                'fallos': p.fallos
            })
            total_fallos += p.fallos
    
    puntos_necesarios = (user.nivel_actual + 1) * 500
    progreso_nivel = min((user.puntos_totales / puntos_necesarios) * 100, 100) if puntos_necesarios > 0 else 0
    
    total_lecturas = Lectura.query.filter_by(nivel=user.nivel_actual, activa=True).count()
    
    return jsonify({
        'usuario': user.to_dict(),
        'lecturas_completadas': lecturas_completadas,
        'quiz_historial': quiz_historial,
        'total_fallos': total_fallos,
        'total_lecturas': total_lecturas,
        'progreso_nivel': progreso_nivel,
        'puntos_necesarios': puntos_necesarios
    })


@stats_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
def get_stats():
    user = get_current_user()
    
    try:
        from models.actividad import ProgresoActividad
    except:
        ProgresoActividad = None
    
    return jsonify({
        'puntos_totales': user.puntos_totales,
        'nivel_actual': user.nivel_actual,
        'racha_dias': user.racha_dias
    })


@stats_bp.route('/admin/metricas', methods=['GET'])
@jwt_required()
def get_admin_metrics():
    user = get_current_user()
    if not user.es_admin():
        return jsonify({'error': 'Solo administradores'}), 403
    
    try:
        from models.actividad import ProgresoActividad
    except:
        ProgresoActividad = None
    
    total_usuarios = Usuario.query.count()
    usuarios_activos = Usuario.query.filter(Usuario.ultimo_login != None).count()
    puntos_promedio = db.session.query(db.func.avg(Usuario.puntos_totales)).scalar() or 0
    puntos_totales_sistema = db.session.query(db.func.sum(Usuario.puntos_totales)).scalar() or 0
    
    niveles = {}
    for u in Usuario.query.all():
        niveles[str(u.nivel_actual)] = niveles.get(str(u.nivel_actual), 0) + 1
    
    total_lecturas = Lectura.query.count()
    lecturas_completadas = ProgresoLectura.query.filter_by(completada=True).count()
    
    quices_totales = ProgresoLectura.query.filter(ProgresoLectura.intentos > 0).count()
    quices_aprobados = ProgresoLectura.query.filter_by(quiz_aprobado=True).count()
    total_fallos = db.session.query(db.func.sum(ProgresoLectura.fallos)).scalar() or 0
    
    actividades_total = 0
    if ProgresoActividad:
        actividades_total = ProgresoActividad.query.filter_by(completado=True).count()
    
    top_estudiantes = Usuario.query.filter_by(rol='estudiante').order_by(Usuario.puntos_totales.desc()).limit(10).all()
    top_list = []
    for u in top_estudiantes:
        progresos = ProgresoLectura.query.filter_by(usuario_id=u.id).all()
        completadas = len([p for p in progresos if p.completada])
        quices = len([p for p in progresos if p.quiz_aprobado == True])
        fallos = db.session.query(db.func.sum(ProgresoLectura.fallos)).filter_by(usuario_id=u.id).scalar() or 0
        actividades = 0
        if ProgresoActividad:
            actividades = ProgresoActividad.query.filter_by(usuario_id=u.id, completado=True).count()
        top_list.append({
            'username': u.username, 'puntos': u.puntos_totales,
            'nivel': u.nivel_actual, 'completadas': completadas,
            'quices': quices, 'fallos': fallos, 'actividades': actividades
        })
    
    return jsonify({
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'puntos_promedio': int(puntos_promedio),
        'puntos_totales_sistema': int(puntos_totales_sistema),
        'niveles': niveles,
        'total_lecturas': total_lecturas,
        'lecturas_completadas': lecturas_completadas,
        'quices_totales': quices_totales,
        'quices_aprobados': quices_aprobados,
        'total_fallos': total_fallos,
        'actividades_completadas': actividades_total,
        'top_estudiantes': top_list
    })
