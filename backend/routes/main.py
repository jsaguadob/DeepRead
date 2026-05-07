from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.lectura import Lectura, Pregunta
from models.progreso import ProgresoLectura
from models.user import Usuario
from models.grupo import Grupo, MiembroGrupo
try:
    from models.actividad import Actividad, ProgresoActividad
except:
    Actividad = None
    ProgresoActividad = None
from datetime import datetime
import random
import string

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    usuario = db.session.get(Usuario, current_user.id)
    
    total_lecturas = Lectura.query.filter_by(nivel=usuario.nivel_actual, activa=True).count()
    lecturas_completadas = ProgresoLectura.query.filter_by(
        usuario_id=usuario.id,
        completada=True
    ).count()
    
    progreso_nivel = 0
    puntos_necesarios = (usuario.nivel_actual + 1) * 500
    if puntos_necesarios > 0:
        progreso_nivel = min((usuario.puntos_totales / puntos_necesarios) * 100, 100)
    
    lecturas_recientes = ProgresoLectura.query.filter_by(
        usuario_id=usuario.id
    ).order_by(ProgresoLectura.fecha_completado.desc()).limit(5).all()
    
    return render_template(
        'dashboard.html',
        usuario=usuario,
        total_lecturas=total_lecturas,
        lecturas_completadas=lecturas_completadas,
        progreso_nivel=progreso_nivel,
        puntos_necesarios=puntos_necesarios,
        lecturas_recientes=lecturas_recientes
    )


@main_bp.route('/lecturas')
@login_required
def lecturas():
    nivel = request.args.get('nivel', type=int)
    categoria = request.args.get('categoria')
    
    mis_grupo_ids = [m.grupo_id for m in MiembroGrupo.query.filter_by(usuario_id=current_user.id).all()]
    
    if current_user.es_admin():
        query = Lectura.query.filter_by(activa=True)
    elif current_user.es_profesor():
        query = Lectura.query.filter(
            (Lectura.activa == True),
            (Lectura.profesor_id == current_user.id)
        )
    elif mis_grupo_ids:
        query = Lectura.query.filter(
            (Lectura.activa == True),
            (Lectura.grupo_id.in_(mis_grupo_ids))
        )
    else:
        query = Lectura.query.filter( Lectura.id == 0 )
    
    if nivel:
        query = query.filter_by(nivel=nivel)
    if categoria:
        query = query.filter_by(categoria=categoria)
    
    lecturas = query.all()
    
    categorias = db.session.query(Lectura.categoria).distinct().all()
    categorias = [c[0] for c in categorias]
    
    lecturas_completadas_ids = [
        p.lectura_id for p in ProgresoLectura.query.filter_by(
            usuario_id=current_user.id,
            completada=True
        ).all()
    ]
    
    return render_template(
        'lecturas.html',
        lecturas=lecturas,
        categorias=categorias,
        nivel_seleccionado=nivel,
        categoria_seleccionada=categoria,
        lecturas_completadas_ids=lecturas_completadas_ids
    )


@main_bp.route('/mis_grupos')
@login_required
def mis_grupos():
    from models.actividad import Actividad, ProgresoActividad
    
    grupos_creados = []
    if current_user.es_profesor() or current_user.es_admin():
        grupos_creados = Grupo.query.filter(
            (Grupo.profesor_id == current_user.id) | (Grupo.profesor_id == None)
        ).all() if current_user.es_admin() else Grupo.query.filter_by(profesor_id=current_user.id).all()
    
    miembro_grupos = MiembroGrupo.query.filter_by(usuario_id=current_user.id).all()
    grupos = []
    for m in miembro_grupos:
        grupo = db.session.get(Grupo, m.grupo_id)
        if grupo and grupo.activo:
            if current_user.es_profesor() and grupo.profesor_id != current_user.id and not current_user.es_admin():
                continue
            lecturas = Lectura.query.filter_by(grupo_id=grupo.id).all()
            grupos.append({
                'id': grupo.id,
                'nombre': grupo.nombre,
                'descripcion': grupo.descripcion,
                'codigo': grupo.codigo_unico,
                'rol': m.rol_en_grupo,
                'es_dueno': grupo.profesor_id == current_user.id,
                'lecturas': [{
                    'id': l.id,
                    'titulo': l.titulo,
                    'nivel': l.nivel,
                    'tiempo': l.tiempo_estimado_minutos,
                    'puntos': l.puntos_recompensa
                } for l in lecturas]
            })
    
    return render_template('mis_grupos.html', grupos=grupos, grupos_creados=grupos_creados)


@main_bp.route('/lectura/<int:lectura_id>')
@login_required
def ver_lectura(lectura_id):
    from datetime import datetime
    
    lectura = db.session.get(Lectura, lectura_id)
    
    if not lectura:
        flash('Lectura no encontrada', 'error')
        return redirect(url_for('main.lecturas'))
    
    if lectura.cerrada:
        flash('Esta lectura está cerrada', 'error')
        return redirect(url_for('main.lecturas'))
    
    if lectura.fecha_cierre and lectura.fecha_cierre < datetime.utcnow():
        lectura.cerrada = True
        db.session.commit()
        flash('Esta lectura ha cerrado', 'error')
        return redirect(url_for('main.lecturas'))
    
    mis_grupo_ids = [m.grupo_id for m in MiembroGrupo.query.filter_by(usuario_id=current_user.id).all()]
    
    tiene_acceso = False
    if current_user.es_admin():
        tiene_acceso = True
    elif current_user.es_profesor() and lectura.profesor_id == current_user.id:
        tiene_acceso = True
    elif mis_grupo_ids and lectura.grupo_id in mis_grupo_ids:
        tiene_acceso = True
    
    if not tiene_acceso:
        flash('No tienes acceso a esta lectura', 'error')
        return redirect(url_for('main.lecturas'))
    
    progreso = ProgresoLectura.query.filter_by(
        usuario_id=current_user.id,
        lectura_id=lectura_id
    ).first()
    
    preguntas = Pregunta.query.filter_by(lectura_id=lectura_id).all()
    
    tiene_quiz = len(preguntas) > 0
    quiz_completado = False
    if tiene_quiz and progreso and hasattr(progreso, 'quiz_aprobado'):
        quiz_completado = progreso.quiz_aprobado == True
    
    try:
        from models.actividad import Actividad, ProgresoActividad
        actividades = Actividad.query.filter_by(lectura_id=lectura_id, activa=True).all()
        
        actividades_pendientes = []
        for a in actividades:
            prog = ProgresoActividad.query.filter_by(
                usuario_id=current_user.id,
                actividad_id=a.id,
                completado=True
            ).first()
            if not prog:
                actividades_pendientes.append(a)
        actividades = actividades_pendientes
    except Exception as e:
        print(f"Error actividades: {e}")
        actividades = []
    
    return render_template(
        'lectura.html',
        lectura=lectura,
        preguntas=preguntas if (not quiz_completado and tiene_quiz) else [],
        progreso=progreso,
        actividades=actividades,
        tiene_quiz=tiene_quiz,
        quiz_completado=quiz_completado
    )


@main_bp.route('/completar_lectura/<int:lectura_id>', methods=['POST'])
@login_required
def completar_lectura(lectura_id):
    lectura = db.session.get(Lectura, lectura_id)
    
    if not lectura:
        flash('Lectura no encontrada', 'error')
        return redirect(url_for('main.lecturas'))
    
    preguntas = Pregunta.query.filter_by(lectura_id=lectura_id).all()
    tiene_quiz = len(preguntas) > 0
    
    progreso = ProgresoLectura.query.filter_by(
        usuario_id=current_user.id,
        lectura_id=lectura_id
    ).first()
    
    quiz_completado = False
    if tiene_quiz and progreso and hasattr(progreso, 'quiz_aprobado'):
        quiz_completado = progreso.quiz_aprobado == True
    
    if tiene_quiz and not quiz_completado:
        flash('Aproba el quiz con 80% para terminar la lectura', 'warning')
        return redirect(url_for('main.ver_lectura', lectura_id=lectura_id))
    
    if not progreso:
        progreso = ProgresoLectura(
            usuario_id=current_user.id,
            lectura_id=lectura_id,
            completada=False,
            puntos_obtenidos=0
        )
        db.session.add(progreso)
    
    progreso.completada = True
    progreso.puntos_obtenidos = lectura.puntos_recompensa
    progreso.fecha_completado = datetime.utcnow()
    
    usuario = db.session.get(Usuario, current_user.id)
    if usuario:
        usuario.puntos_totales += lectura.puntos_recompensa
        
        nuevo_nivel = (usuario.puntos_totales // 500) + 1
        if nuevo_nivel > usuario.nivel_actual and nuevo_nivel <= 3:
            usuario.nivel_actual = nuevo_nivel
            flash(f'¡Felicidades! Has avanzado al nivel {nuevo_nivel}', 'success')
    
    db.session.commit()
    
    flash(f'¡Lectura completada! +{lectura.puntos_recompensa} puntos', 'success')
    return redirect(url_for('main.dashboard'))


@main_bp.route('/quiz/<int:lectura_id>', methods=['GET', 'POST'])
@login_required
def quiz(lectura_id):
    from datetime import datetime
    import secrets
    
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura:
        flash('Lectura no encontrada', 'error')
        return redirect(url_for('main.lecturas'))
    
    if lectura.cerrada:
        flash('Esta lectura está cerrada', 'error')
        return redirect(url_for('main.lecturas'))
    
    if lectura.fecha_cierre and lectura.fecha_cierre < datetime.utcnow():
        lectura.cerrada = True
        db.session.commit()
        flash('El plazo ha vencido', 'error')
        return redirect(url_for('main.lecturas'))
    
    preguntas = Pregunta.query.filter_by(lectura_id=lectura_id).all()
    if not preguntas:
        flash('No hay preguntas para este quiz', 'error')
        return redirect(url_for('main.lecturas'))
    
    progreso = ProgresoLectura.query.filter_by(
        usuario_id=current_user.id,
        lectura_id=lectura_id
    ).first()
    
    quiz_token = request.args.get('token')
    
    if not quiz_token:
        quiz_token = secrets.token_urlsafe(32)
        return redirect(url_for('main.quiz', lectura_id=lectura_id, token=quiz_token))
    
    intentos_actuales = getattr(progreso, 'intentos', 0) if progreso else 0
    intentos_max = lectura.intentos_maximos or 3
    
    if request.method == 'POST':
        session_token = request.form.get('session_token')
        if session_token != quiz_token:
            flash('Sesión inválida. Cierra otras ventanas del quiz.', 'error')
            return redirect(url_for('main.dashboard'))
        
        if intentos_actuales >= intentos_max:
            flash('Sin intentos disponibles', 'error')
            return redirect(url_for('main.dashboard'))
        
        respuestas = request.form.to_dict()
        correctas = 0
        total_preguntas = len(preguntas)
        
        for pregunta in preguntas:
            respuesta = respuestas.get(f'pregunta_{pregunta.id}')
            if respuesta == pregunta.respuesta_correcta:
                correctas += 1
        
        porcentaje = (correctas / total_preguntas * 100) if total_preguntas > 0 else 0
        puntos_por_pregunta = 5.0 / total_preguntas
        puntos = 0
        if correctas > 0:
            puntos = int(correctas * puntos_por_pregunta * 100) / 100
        
        if lectura.cerrada and puntos > 0:
            puntos = int(puntos * 0.5)
        
        quiz_aprobado = porcentaje >= 80
        
        if progreso:
            progreso.intentos = intentos_actuales + 1
            progreso.puntos_obtenidos = puntos
            progreso.quiz_aprobado = quiz_aprobado
            progreso.quiz_porcentaje = porcentaje
            progreso.fecha_completado = datetime.utcnow()
        else:
            progreso = ProgresoLectura(
                usuario_id=current_user.id,
                lectura_id=lectura_id,
                completada=False,
                puntos_obtenidos=puntos,
                intentos=1,
                quiz_aprobado=quiz_aprobado,
                quiz_porcentaje=porcentaje,
                fecha_completado=datetime.utcnow()
            )
            db.session.add(progreso)
        
        if puntos > 0:
            usuario = db.session.get(Usuario, current_user.id)
            if usuario:
                tiene_quiz = len(preguntas) > 0
                try:
                    from models.actividad import Actividad
                    actividades = Actividad.query.filter_by(lectura_id=lectura_id, activa=True).all()
                    tiene_actividad = len(actividades) > 0
                except:
                    tiene_actividad = False
                
                puede_subir = True
                if tiene_quiz:
                    quiz_progreso = ProgresoLectura.query.filter_by(
                        usuario_id=current_user.id, lectura_id=lectura_id
                    ).first()
                    if not quiz_progreso or quiz_progreso.intentos < 1:
                        puede_subir = False
                
                if tiene_actividad and puede_subir:
                    for act in actividades:
                        try:
                            act_prog = ProgresoActividad.query.filter_by(
                                usuario_id=current_user.id, actividad_id=act.id
                            ).first()
                            if not act_prog or not act_prog.completado:
                                puede_subir = False
                                break
                        except:
                            pass
                
                if puede_subir:
                    usuario.puntos_totales += puntos
                    flash(f'¡Quiz aprobado! ({porcentaje:.0f}%) +{puntos} puntos', 'success')
                else:
                    if quiz_aprobado:
                        flash(f'Quiz aprobado ({porcentaje:.0f}%) pero completa las actividades.', 'info')
                    else:
                        flash(f'Necesitas 80% para aprobar. Obtuviste {porcentaje:.0f}%. Intenta de nuevo.', 'error')
        
        db.session.commit()
        
        if quiz_aprobado:
            flash(f'¡Quiz aprobado! ({porcentaje:.0f}%)', 'success')
            return redirect(url_for('main.ver_lectura', lectura_id=lectura_id))
        else:
            flash(f'Necesitas 80% para aprobar. Obtuviste {porcentaje:.0f}%. Intenta de nuevo.', 'error')
            return redirect(url_for('main.quiz', lectura_id=lectura_id))
    
    return render_template('quiz.html', lectura=lectura, preguntas=preguntas, 
                         intentos=intentos_actuales, max_intentos=intentos_max,
                         session_token=quiz_token)


@main_bp.route('/progreso')
@login_required
def progreso():
    usuario = db.session.get(Usuario, current_user.id)
    
    progresos = ProgresoLectura.query.filter_by(
        usuario_id=usuario.id
    ).all()
    
    lecturas_completadas = []
    for p in progresos:
        if p.completada:
            lectura = db.session.get(Lectura, p.lectura_id)
            if lectura:
                lecturas_completadas.append({
                    'titulo': lectura.titulo,
                    'nivel': lectura.nivel,
                    'puntos': p.puntos_obtenidos,
                    'fecha': p.fecha_completado
                })
    
    return render_template(
        'progreso.html',
        usuario=usuario,
        lecturas=lecturas_completadas
    )


@main_bp.route('/api/estadisticas')
@login_required
def api_estadisticas():
    usuario = db.session.get(Usuario, current_user.id)
    
    return {
        'puntos_totales': usuario.puntos_totales,
        'nivel_actual': usuario.nivel_actual,
        'racha_dias': usuario.racha_dias
    }


@main_bp.route('/actividades')
@login_required
def actividades():
    try:
        from models.actividad import Actividad, ProgresoActividad
        mis_grupo_ids = [m.grupo_id for m in MiembroGrupo.query.filter_by(usuario_id=current_user.id).all()]
        
        if mis_grupo_ids:
            actividades = Actividad.query.filter(
                (Actividad.activa == True),
                (Actividad.es_publica == True) | (Actividad.grupo_id.in_(mis_grupo_ids))
            ).all()
        else:
            actividades = Actividad.query.filter_by(activa=True, es_publica=True).all()
    except:
        actividades = []
    
    return render_template('actividades.html', actividades=actividades)


@main_bp.route('/actividad/<int:actividad_id>', methods=['GET', 'POST'])
@login_required
def resolver_actividad(actividad_id):
    try:
        from models.actividad import Actividad, ProgresoActividad
    except:
        flash('No hay actividades disponibles', 'error')
        return redirect(url_for('main.dashboard'))
    
    actividad = db.session.get(Actividad, actividad_id)
    if not actividad:
        flash('Actividad no encontrada', 'error')
        return redirect(url_for('main.actividades'))
    
    if request.method == 'POST' and actividad.tipo == 'sopa':
        encontradas_raw = request.form.get('encontradas', '')
        
        palabras_a_encontrar = set(p.strip().upper() for p in actividad.contenido.split(','))
        palabras_encontradas = set()
        
        if encontradas_raw:
            palabras_encontradas = set(p.strip().upper() for p in encontradas_raw.split(',') if p.strip())
        
        faltantes = palabras_a_encontrar - palabras_encontradas
        correcta = len(faltantes) == 0
        
        progreso = ProgresoActividad.query.filter_by(
            usuario_id=current_user.id,
            actividad_id=actividad_id
        ).first()
        
        if progreso and progreso.completado:
            flash('Ya completaste esta actividad', 'info')
            return redirect(url_for('main.ver_lectura', lectura_id=actividad.lectura_id))
        
        if not progreso:
            progreso = ProgresoActividad(
                usuario_id=current_user.id,
                actividad_id=actividad_id
            )
            db.session.add(progreso)
        
        if correcta:
            progreso.completado = True
            progreso.puntos_obtenidos = actividad.puntos
            progreso.respuesta = ','.join(palabras_encontradas)
            progreso.fecha_completado = datetime.utcnow()
            db.session.commit()
            flash(f'¡Perfecto! Has completado la sopa de letras. +{actividad.puntos} puntos', 'success')
            return redirect(url_for('main.ver_lectura', lectura_id=actividad.lectura_id))
        else:
            db.session.commit()
            if len(palabras_encontradas) == 0:
                flash('Selecciona letras en la sopa para encontrar las palabras', 'info')
            else:
                flash(f'Has encontrado {len(palabras_encontradas)} de {len(palabras_a_encontrar)} palabras. ¡Sigue buscando!', 'info')
            return render_template('resolver_sopa.html', actividad=actividad)
    
    if actividad.tipo == 'sopa':
        return render_template('resolver_sopa.html', actividad=actividad)
    
    if request.method == 'POST' and actividad.tipo != 'sopa':
        respuesta = request.form.get('respuesta', '').strip().lower()
        correcta = respuesta == actividad.solucion.lower()
        
        progreso = ProgresoActividad.query.filter_by(
            usuario_id=current_user.id,
            actividad_id=actividad_id
        ).first()
        
        if progreso and progreso.completado:
            flash('Ya completaste esta actividad', 'info')
            return redirect(url_for('main.ver_lectura', lectura_id=actividad.lectura_id))
        
        if not progreso:
            progreso = ProgresoActividad(
                usuario_id=current_user.id,
                actividad_id=actividad_id
            )
            db.session.add(progreso)
        
        if correcta:
            progreso.completado = True
            progreso.puntos_obtenidos = actividad.puntos
            progreso.respuesta = respuesta
            progreso.fecha_completado = datetime.utcnow()
            
            try:
                from models.lectura import Pregunta
                preguntas = Pregunta.query.filter_by(lectura_id=actividad.lectura_id).all()
                tiene_quiz = len(preguntas) > 0
                
                quiz_progreso = ProgresoLectura.query.filter_by(
                    usuario_id=current_user.id, lectura_id=actividad.lectura_id
                ).first()
                
                try:
                    from models.actividad import Actividad
                    actividades = Actividad.query.filter_by(
                        lectura_id=actividad.lectura_id, activa=True
                    ).all()
                except:
                    actividades = []
                
                puede_subir = True
                if tiene_quiz and (not quiz_progreso or quiz_progreso.intentos < 1):
                    puede_subir = False
                
                for act in actividades:
                    if act.id == actividad.id:
                        continue
                    try:
                        ap = ProgresoActividad.query.filter_by(
                            usuario_id=current_user.id, actividad_id=act.id
                        ).first()
                        if not ap or not ap.completado:
                            puede_subir = False
                            break
                    except:
                        pass
                
                if puede_subir:
                    usuario = db.session.get(Usuario, current_user.id)
                    if usuario:
                        usuario.puntos_totales += actividad.puntos
                    flash(f'¡Completo! +{actividad.puntos} puntos', 'success')
                else:
                    flash('Guardado. Completa todo para summation puntos.', 'info')
            except:
                flash('Incorrecto. Intenta de nuevo.', 'error')
        else:
            flash('Incorrecto. Intenta de nuevo.', 'error')
        
        db.session.commit()
        return redirect(url_for('main.ver_lectura', lectura_id=actividad.lectura_id))
    
    return render_template('resolver_actividad.html', actividad=actividad)