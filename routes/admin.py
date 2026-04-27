from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.user import Usuario
from models.grupo import Grupo, MiembroGrupo
from models.lectura import Lectura, Pregunta
from models.progreso import ProgresoLectura
import secrets
import string
import random

def gerar_codigo(length=6):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/crear_lectura', methods=['GET', 'POST'])
@login_required
def crear_lectura_publica():
    if not current_user.es_admin():
        flash('Solo admins pueden crear lecturas públicas', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        from datetime import datetime
        lectura = Lectura(
            titulo=request.form.get('titulo'),
            contenido=request.form.get('contenido'),
            nivel=int(request.form.get('nivel')),
            tiempo_estimado_minutos=int(request.form.get('tiempo')),
            puntos_recompensa=int(request.form.get('puntos')),
            categoria=request.form.get('categoria'),
            profesor_id=current_user.id,
            grupo_id=None,
            es_publica=True,
            intentos_maximos=int(request.form.get('intentos', 3))
        )
        db.session.add(lectura)
        db.session.commit()
        flash('Lectura pública creada', 'success')
        return redirect(url_for('main.lecturas'))
    
    return render_template('crear_lectura_publica.html')


@admin_bp.route('/admin/editar_lectura/<int:lectura_id>', methods=['GET', 'POST'])
@login_required
def editar_lectura_admin(lectura_id):
    if not current_user.es_admin():
        flash('Solo admins pueden editar lecturas públicas', 'error')
        return redirect(url_for('main.dashboard'))
    
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura or lectura.profesor_id != current_user.id:
        flash('Lectura no encontrada', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        lectura.titulo = request.form.get('titulo')
        lectura.contenido = request.form.get('contenido')
        lectura.nivel = int(request.form.get('nivel'))
        lectura.tiempo_estimado_minutos = int(request.form.get('tiempo'))
        lectura.puntos_recompensa = int(request.form.get('puntos'))
        lectura.categoria = request.form.get('categoria')
        db.session.commit()
        flash('Lectura actualizada', 'success')
        return redirect(url_for('main.lecturas'))
    
    return render_template('crear_lectura_publica.html', lectura=lectura)


@admin_bp.route('/admin/eliminar_lectura/<int:lectura_id>', methods=['POST'])
@login_required
def eliminar_lectura_admin(lectura_id):
    if not current_user.es_admin():
        flash('Solo admins pueden eliminar lecturas', 'error')
        return redirect(url_for('main.dashboard'))
    
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura or lectura.profesor_id != current_user.id:
        flash('Lectura no encontrada', 'error')
        return redirect(url_for('main.dashboard'))
    
    preguntas = Pregunta.query.filter_by(lectura_id=lectura_id).all()
    for p in preguntas:
        db.session.delete(p)
    db.session.delete(lectura)
    db.session.commit()
    flash('Lectura eliminada', 'success')
    return redirect(url_for('main.lecturas'))


@admin_bp.route('/admin/crear_quiz/<int:lectura_id>', methods=['GET', 'POST'])
@login_required
def crear_quiz_admin(lectura_id):
    if not current_user.es_admin():
        flash('Solo admins pueden crear quizzes', 'error')
        return redirect(url_for('main.dashboard'))
    
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura or lectura.profesor_id != current_user.id:
        flash('Lectura no encontrada', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        pregunta = Pregunta(
            lectura_id=lectura_id,
            pregunta=request.form.get('pregunta'),
            opcion_a=request.form.get('opcion_a'),
            opcion_b=request.form.get('opcion_b'),
            opcion_c=request.form.get('opcion_c'),
            opcion_d=request.form.get('opcion_d'),
            respuesta_correcta=request.form.get('respuesta'),
            explicacion=request.form.get('explicacion'),
            profesor_id=current_user.id
        )
        db.session.add(pregunta)
        db.session.commit()
        flash('Pregunta agregada', 'success')
        return redirect(url_for('main.lecturas'))
    
    return render_template('crear_quiz.html', lectura=lectura)


@admin_bp.route('/grupos/<int:grupo_id>/cerrar_lectura/<int:lectura_id>', methods=['POST'])
@login_required
def cerrar_lectura_grupo(grupo_id, lectura_id):
    from datetime import datetime
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo or grupo.profesor_id != current_user.id:
        flash('Solo el profesor puede cerrar lecturas', 'error')
        return redirect(url_for('main.dashboard'))
    
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura or lectura.grupo_id != grupo_id:
        flash('Lectura no encontrada', 'error')
        return redirect(url_for('admin.ver_grupo', grupo_id=grupo_id))
    
    if request.method == 'POST':
        accion = request.form.get('accion')
        if accion == 'reabrir':
            lectura.cerrada = False
            lectura.fecha_cierre = None
        else:
            fecha_cierre = request.form.get('fecha_cierre')
            if fecha_cierre:
                lectura.fecha_cierre = datetime.strptime(fecha_cierre, '%Y-%m-%dT%H:%M')
            else:
                lectura.cerrada = True
        
        db.session.commit()
        flash('Lectura cerrada', 'success')
        return redirect(url_for('admin.ver_grupo', grupo_id=grupo_id))
    
    return redirect(url_for('admin.ver_grupo', grupo_id=grupo_id))


@admin_bp.route('/grupos/<int:grupo_id>/ver_estado_lectura/<int:lectura_id>')
@login_required
def ver_estado_lectura(grupo_id, lectura_id):
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo or grupo.profesor_id != current_user.id:
        flash('Solo el profesor puede ver esto', 'error')
        return redirect(url_for('main.dashboard'))
    
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura or lectura.grupo_id != grupo_id:
        flash('Lectura no encontrada', 'error')
        return redirect(url_for('admin.ver_grupo', grupo_id=grupo_id))
    
    miembros = MiembroGrupo.query.filter_by(grupo_id=grupo_id).all()
    
    completados = []
    no_completados = []
    
    for m in miembros:
        if m.rol_en_grupo == 'estudiante':
            usuario = db.session.get(Usuario, m.usuario_id)
            progreso = ProgresoLectura.query.filter_by(
                usuario_id=usuario.id,
                lectura_id=lectura_id
            ).first()
            
            if progreso and progreso.completada:
                completados.append({
                    'username': usuario.username,
                    'puntos': progreso.puntos_obtenidos,
                    'fecha': progreso.fecha_completado
                })
            else:
                no_completados.append({
                    'username': usuario.username,
                    'email': usuario.email
                })
    
    return render_template('ver_estado_lectura.html', 
        grupo=grupo, lectura=lectura, 
        completados=completados, no_completados=no_completados)


@admin_bp.route('/admin')
@login_required
def panel_admin():
    if not current_user.es_admin():
        flash('Acceso denegado', 'error')
        return redirect(url_for('main.dashboard'))
    
    usuarios = Usuario.query.all()
    total_estudiantes = Usuario.query.filter_by(rol='estudiante').count()
    total_profesores = Usuario.query.filter_by(rol='profesor').count()
    usuarios_activos = Usuario.query.filter(Usuario.ultimo_login != None).count()
    puntos_promedio = db.session.query(db.func.avg(Usuario.puntos_totales)).scalar() or 0
    lecturas_completadas = ProgresoLectura.query.filter_by(completada=True).count()
    
    return render_template('admin.html', 
        usuarios=usuarios,
        total_estudiantes=total_estudiantes,
        total_profesores=total_profesores,
        usuarios_activos=usuarios_activos,
        puntos_promedio=puntos_promedio,
        lecturas_completadas=lecturas_completadas)


@admin_bp.route('/admin/metricas')
@login_required
def metricas():
    if not current_user.es_admin():
        flash('Acceso denegado', 'error')
        return redirect(url_for('main.dashboard'))
    
    usuarios = Usuario.query.all()
    por_nivel = {n: Usuario.query.filter_by(nivel_actual=n).count() for n in [1, 2, 3]}
    por_rol = {}
    por_rol['estudiante'] = Usuario.query.filter_by(rol='estudiante').count()
    por_rol['profesor'] = Usuario.query.filter_by(rol='profesor').count()
    por_rol['admin'] = Usuario.query.filter_by(rol='admin').count()
    por_tipo = {}
    por_tipo['gratuito'] = Usuario.query.filter_by(tipo_usuario='gratuito').count()
    por_tipo['institucional'] = Usuario.query.filter_by(tipo_usuario='institucional').count()
    puntos_promedio = db.session.query(db.func.avg(Usuario.puntos_totales)).scalar() or 0
    top_estudiantes = Usuario.query.filter_by(rol='estudiante').order_by(Usuario.puntos_totales.desc()).limit(10).all()
    
    return render_template('metricas.html',
        usuarios=usuarios,
        por_nivel=por_nivel,
        por_rol=por_rol,
        por_tipo=por_tipo,
        puntos_promedio=puntos_promedio,
        top_estudiantes=top_estudiantes)


@admin_bp.route('/admin/promover/<int:usuario_id>', methods=['POST'])
@login_required
def promover_usuario(usuario_id):
    if not current_user.es_admin():
        flash('Acceso denegado', 'error')
        return redirect(url_for('main.dashboard'))
    
    nuevo_rol = request.form.get('rol')
    nuevo_tipo = request.form.get('tipo_usuario')
    usuario = db.session.get(Usuario, usuario_id)
    
    if usuario:
        if nuevo_rol:
            usuario.rol = nuevo_rol
        if nuevo_tipo:
            usuario.tipo_usuario = nuevo_tipo
        db.session.commit()
        flash(f'{usuario.username} actualizado', 'success')
    
    return redirect(url_for('admin.panel_admin'))


@admin_bp.route('/mis_grupos')
@login_required
def mis_grupos():
    grupos_creados = Grupo.query.filter_by(profesor_id=current_user.id).all()
    
    miembros = MiembroGrupo.query.filter_by(usuario_id=current_user.id).all()
    grupos_miembro = []
    for m in miembros:
        grupo = db.session.get(Grupo, m.grupo_id)
        if grupo and grupo.id not in [g.id for g in grupos_creados]:
            grupos_miembro.append({
                'id': grupo.id,
                'nombre': grupo.nombre,
                'descripcion': grupo.descripcion,
                'codigo': grupo.codigo_unico,
                'rol': m.rol_en_grupo
            })
    
    return render_template('mis_grupos_admin.html', 
        grupos=grupos_creados, 
        grupos_miembro=grupos_miembro)


@admin_bp.route('/grupos/crear', methods=['GET', 'POST'])
@login_required
def crear_grupo():
    if not current_user.es_profesor():
        flash('Solo profesores pueden crear grupos', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        codigo = gerar_codigo(6)
        
        grupo = Grupo(
            nombre=nombre,
            descripcion=descripcion,
            profesor_id=current_user.id,
            codigo_unico=codigo
        )
        db.session.add(grupo)
        db.session.commit()
        
        miembro = MiembroGrupo(
            grupo_id=grupo.id,
            usuario_id=current_user.id,
            rol_en_grupo='profesor'
        )
        db.session.add(miembro)
        db.session.commit()
        
        flash(f'Grupo "{nombre}" creado. Código: {codigo}', 'success')
        return redirect(url_for('admin.mis_grupos'))
    
    return render_template('crear_grupo.html')


@admin_bp.route('/grupos/unirse', methods=['GET', 'POST'])
@login_required
def unidos_grupo():
    if request.method == 'POST':
        codigo = request.form.get('codigo').strip().upper()
        grupo = Grupo.query.filter_by(codigo_unico=codigo, activo=True).first()
        
        if not grupo:
            flash('Código de grupo no válido', 'error')
            return redirect(url_for('admin.unidos_grupo'))
        
        existente = MiembroGrupo.query.filter_by(
            grupo_id=grupo.id,
            usuario_id=current_user.id
        ).first()
        
        if existente:
            flash('Ya eres miembro de este grupo', 'warning')
            return redirect(url_for('main.dashboard'))
        
        miembro = MiembroGrupo(
            grupo_id=grupo.id,
            usuario_id=current_user.id,
            rol_en_grupo='estudiante'
        )
        db.session.add(miembro)
        db.session.commit()
        
        flash(f'Te uniste al grupo "{grupo.nombre}"', 'success')
        return redirect(url_for('main.mis_grupos'))
    
    return render_template('unirse_grupo.html')


@admin_bp.route('/grupos/<int:grupo_id>')
@login_required
def ver_grupo(grupo_id):
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo:
        flash('Grupo no encontrado', 'error')
        return redirect(url_for('main.dashboard'))
    
    tiene_acceso = False
    if current_user.es_admin():
        tiene_acceso = True
    elif current_user.es_profesor() and grupo.profesor_id == current_user.id:
        tiene_acceso = True
    else:
        miembro = MiembroGrupo.query.filter_by(grupo_id=grupo_id, usuario_id=current_user.id).first()
        if miembro:
            tiene_acceso = True
    
    if not tiene_acceso:
        flash('No tienes acceso a este grupo', 'error')
        return redirect(url_for('main.dashboard'))
    
    miembros = []
    if current_user.es_admin() or (current_user.es_profesor() and grupo.profesor_id == current_user.id):
        miembros = MiembroGrupo.query.filter_by(grupo_id=grupo_id).all()
        usuarios_miembros = []
        for m in miembros:
            usuario = db.session.get(Usuario, m.usuario_id)
            completadas = ProgresoLectura.query.filter_by(usuario_id=usuario.id, completada=True).count()
            usuarios_miembros.append({
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'rol': m.rol_en_grupo,
                'puntos': usuario.puntos_totales,
                'nivel': usuario.nivel_actual,
                'completadas': completadas
            })
        miembros = usuarios_miembros
    else:
        miembros = []
    
    lecturas = Lectura.query.filter_by(grupo_id=grupo_id).all()
    
    es_dueno = current_user.es_admin() or (current_user.es_profesor() and grupo.profesor_id == current_user.id)
    
    return render_template('ver_grupo.html', grupo=grupo, miembros=miembros, lecturas=lecturas, es_dueno=es_dueno)


@admin_bp.route('/grupos/<int:grupo_id>/eliminar_miembro/<int:usuario_id>', methods=['POST'])
@login_required
def eliminar_miembro(grupo_id, usuario_id):
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo:
        flash('Grupo no encontrado', 'error')
        return redirect(url_for('main.dashboard'))
    
    if grupo.profesor_id != current_user.id and not current_user.es_admin():
        flash('No tienes permiso', 'error')
        return redirect(url_for('main.dashboard'))
    
    miembro = MiembroGrupo.query.filter_by(grupo_id=grupo_id, usuario_id=usuario_id).first()
    if miembro:
        db.session.delete(miembro)
        db.session.commit()
        flash('Miembro eliminado', 'success')
    
    return redirect(url_for('admin.ver_grupo', grupo_id=grupo_id))


@admin_bp.route('/grupos/<int:grupo_id>/calificaciones')
@login_required
def ver_calificaciones(grupo_id):
    from datetime import datetime
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo or grupo.profesor_id != current_user.id:
        flash('Solo el profesor puede ver calificaciones', 'error')
        return redirect(url_for('main.dashboard'))
    
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
            actividades_completadas = 0
            
            lecturas_detalle = []
            for p in progresos:
                lectura = db.session.get(Lectura, p.lectura_id)
                if lectura and lectura.grupo_id == grupo_id:
                    if p.intentos and p.intentos > 0:
                        total_puntos += p.puntos_obtenidos
                        lecturas_completadas += 1
                        if p.intentos > 0:
                            quizzes_completados += 1
                        lecturas_detalle.append({
                            'titulo': lectura.titulo,
                            'puntos': p.puntos_obtenidos,
                            'intentos': p.intentos,
                            'fecha': p.fecha_completado
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
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'puntos': total_puntos,
                'lecturas_completadas': lecturas_completadas,
                'quizzes_completados': quizzes_completados,
                'actividades_completadas': actividades_completadas,
                'nivel': usuario.nivel_actual,
                'dias_activos': len(dias_activos),
                'lecturas': lecturas_detalle
            })
    
    estudiantes.sort(key=lambda x: x['puntos'], reverse=True)
    return render_template('calificaciones.html', grupo=grupo, estudiantes=estudiantes)


@admin_bp.route('/estadisticas')
@login_required
def ver_estadisticas():
    if not current_user.es_admin():
        flash('Solo admins', 'error')
        return redirect(url_for('main.dashboard'))
    
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
        niveles[u.nivel_actual] = niveles.get(u.nivel_actual, 0) + 1
    
    total_lecturas = Lectura.query.count()
    lecturas_completadas = ProgresoLectura.query.filter_by(completada=True).count()
    
    quices_totales = ProgresoLectura.query.filter(ProgresoLectura.intentos > 0).count()
    quices_aprobados = ProgresoLectura.query.filter_by(quiz_aprobado=True).count()
    
    actividades_total = 0
    if ProgresoActividad:
        actividades_total = ProgresoActividad.query.filter_by(completado=True).count()
    
    top_estudiantes = Usuario.query.filter_by(rol='estudiante').order_by(Usuario.puntos_totales.desc()).limit(10).all()
    top_list = []
    for u in top_estudiantes:
        progresos = ProgresoLectura.query.filter_by(usuario_id=u.id).all()
        completadas = len([p for p in progresos if p.completada])
        quices = len([p for p in progresos if p.quiz_aprobado == True])
        actividades = 0
        if ProgresoActividad:
            actividades = ProgresoActividad.query.filter_by(usuario_id=u.id, completado=True).count()
        top_list.append({
            'username': u.username,
            'puntos': u.puntos_totales,
            'nivel': u.nivel_actual,
            'completadas': completadas,
            'quices': quices,
            'actividades': actividades
        })
    
    return render_template('estadisticas.html',
        total_usuarios=total_usuarios,
        usuarios_activos=usuarios_activos,
        puntos_promedio=int(puntos_promedio),
        puntos_totales_sistema=int(puntos_totales_sistema),
        niveles=niveles,
        total_lecturas=total_lecturas,
        lecturas_completadas=lecturas_completadas,
        quices_totales=quices_totales,
        quices_aprobados=quices_aprobados,
        actividades_completadas=actividades_total,
        top_estudiantes=top_list)


@admin_bp.route('/grupos/<int:grupo_id>/crear_lectura', methods=['GET', 'POST'])
@login_required
def crear_lectura_grupo(grupo_id):
    from datetime import datetime
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo or grupo.profesor_id != current_user.id:
        flash('Solo el profesor puede crear lecturas', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        fecha_cierre = None
        fecha_str = request.form.get('fecha_cierre')
        if fecha_str:
            try:
                fecha_cierre = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            except:
                pass
        
        lectura = Lectura(
            titulo=request.form.get('titulo'),
            contenido=request.form.get('contenido'),
            nivel=int(request.form.get('nivel')),
            tiempo_estimado_minutos=int(request.form.get('tiempo')),
            puntos_recompensa=int(request.form.get('puntos')),
            categoria=request.form.get('categoria'),
            profesor_id=current_user.id,
            grupo_id=grupo_id,
            es_publica=False,
            fecha_cierre=fecha_cierre,
            intentos_maximos=int(request.form.get('intentos', 3))
        )
        db.session.add(lectura)
        db.session.commit()
        flash('Lectura creada', 'success')
        return redirect(url_for('admin.ver_grupo', grupo_id=grupo_id))
    
    return render_template('crear_lectura.html', grupo=grupo)


@admin_bp.route('/grupos/<int:grupo_id>/crear_quiz/<int:lectura_id>', methods=['GET', 'POST'])
@login_required
def crear_quiz_grupo(grupo_id, lectura_id):
    lectura = db.session.get(Lectura, lectura_id)
    grupo = db.session.get(Grupo, grupo_id)
    if not lectura or not grupo or grupo.profesor_id != current_user.id:
        flash('Grupo o lectura no encontrada', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        pregunta = Pregunta(
            lectura_id=lectura_id,
            pregunta=request.form.get('pregunta'),
            opcion_a=request.form.get('opcion_a'),
            opcion_b=request.form.get('opcion_b'),
            opcion_c=request.form.get('opcion_c'),
            opcion_d=request.form.get('opcion_d'),
            respuesta_correcta=request.form.get('respuesta'),
            explicacion=request.form.get('explicacion'),
            profesor_id=current_user.id
        )
        db.session.add(pregunta)
        db.session.commit()
        flash('Pregunta agregada', 'success')
        return redirect(url_for('admin.ver_grupo', grupo_id=grupo_id))
    
    return render_template('crear_quiz.html', lectura=lectura)


@admin_bp.route('/grupos/<int:grupo_id>/editar_lectura/<int:lectura_id>', methods=['GET', 'POST'])
@login_required
def editar_lectura_grupo(grupo_id, lectura_id):
    grupo = db.session.get(Grupo, grupo_id)
    lectura = db.session.get(Lectura, lectura_id)
    if not grupo or not lectura or grupo.profesor_id != current_user.id:
        flash('Grupo o lectura no encontrada', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        lectura.titulo = request.form.get('titulo')
        lectura.contenido = request.form.get('contenido')
        lectura.nivel = int(request.form.get('nivel'))
        lectura.tiempo_estimado_minutos = int(request.form.get('tiempo'))
        lectura.puntos_recompensa = int(request.form.get('puntos'))
        lectura.categoria = request.form.get('categoria')
        db.session.commit()
        flash('Lectura actualizada', 'success')
        return redirect(url_for('admin.ver_grupo', grupo_id=grupo_id))
    
    return render_template('editar_lectura.html', grupo=grupo, lectura=lectura)


@admin_bp.route('/grupos/<int:grupo_id>/eliminar_lectura/<int:lectura_id>', methods=['POST'])
@login_required
def eliminar_lectura_grupo(grupo_id, lectura_id):
    grupo = db.session.get(Grupo, grupo_id)
    lectura = db.session.get(Lectura, lectura_id)
    if not grupo or not lectura or grupo.profesor_id != current_user.id:
        flash('Grupo o lectura no encontrada', 'error')
        return redirect(url_for('main.dashboard'))
    
    preguntas = Pregunta.query.filter_by(lectura_id=lectura_id).all()
    for p in preguntas:
        db.session.delete(p)
    db.session.delete(lectura)
    db.session.commit()
    flash('Lectura eliminada', 'success')
    return redirect(url_for('admin.ver_grupo', grupo_id=grupo_id))


@admin_bp.route('/grupos/<int:grupo_id>/ver_quiz/<int:lectura_id>')
@login_required
def ver_quiz_grupo(grupo_id, lectura_id):
    lectura = db.session.get(Lectura, lectura_id)
    grupo = db.session.get(Grupo, grupo_id)
    if not lectura or not grupo:
        flash('Grupo o lectura no encontrada', 'error')
        return redirect(url_for('main.dashboard'))
    
    preguntas = Pregunta.query.filter_by(lectura_id=lectura_id).all()
    return render_template('ver_quiz.html', grupo=grupo, lectura=lectura, preguntas=preguntas)


@admin_bp.route('/lectura/<int:lectura_id>/crear_actividad', methods=['GET', 'POST'])
@login_required
def crear_actividad(lectura_id):
    from models.actividad import Actividad
    
    lectura = db.session.get(Lectura, lectura_id)
    if not lectura:
        flash('Lectura no encontrada', 'error')
        return redirect(url_for('main.dashboard'))
    
    if not current_user.es_admin() and not current_user.es_profesor():
        flash('No tienes permiso', 'error')
        return redirect(url_for('main.dashboard'))
    
    es_dueno = False
    if current_user.es_admin():
        es_dueno = True
    elif current_user.es_profesor():
        if lectura.profesor_id == current_user.id:
            es_dueno = True
        elif lectura.grupo_id:
            grupo = db.session.get(Grupo, lectura.grupo_id)
            if grupo and grupo.profesor_id == current_user.id:
                es_dueno = True
    
    if not es_dueno:
        flash('No tienes permiso para esta lectura', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        try:
            from models.actividad import Actividad
            tipo = request.form.get('tipo', 'seleccionar')
            titulo = request.form.get('titulo', '').strip()
            contenido = request.form.get('contenido', '').strip()
            opciones = request.form.get('opciones', '').strip()
            palabras_sopa = request.form.get('palabras_sopa', '').strip()
            puntos = int(request.form.get('puntos', 5))
            
            print(f"[DEBUG] Creating activity: tipo={tipo}, titulo={titulo}, contenido={contenido}, palabras_sopa={palabras_sopa}")
            
            if tipo == 'sopa':
                contenido = palabras_sopa.upper()
                solucion = 'sopa'
            elif tipo == 'completar':
                solucion = request.form.get('palabra', '').strip().lower()
            elif tipo == 'seleccionar':
                opciones_list = [o.strip() for o in opciones.split(',')]
                solucion = opciones_list[-1].lower() if opciones_list else opciones.lower()
            else:
                solucion = opciones.lower()
            
            actividad = Actividad(
                lectura_id=lectura_id,
                titulo=titulo,
                tipo=tipo,
                contenido=contenido,
                solucion=solucion,
                nivel=1,
                puntos=puntos,
                tiempo_estimado=10,
                profesor_id=current_user.id
            )
            db.session.add(actividad)
            db.session.commit()
            flash('Actividad creada', 'success')
            return redirect(url_for('main.ver_lectura', lectura_id=lectura_id))
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Creating activity: {e}")
            flash(f'Error: {e}', 'error')
    
    return render_template('crear_actividad.html', lectura=lectura)


@admin_bp.route('/actividad/<int:actividad_id>/eliminar', methods=['POST'])
@login_required
def eliminar_actividad(actividad_id):
    from models.actividad import Actividad
    
    actividad = db.session.get(Actividad, actividad_id)
    if not actividad:
        flash('Actividad no encontrada', 'error')
        return redirect(url_for('main.dashboard'))
    
    if not current_user.es_admin() and not current_user.es_profesor():
        flash('No tienes permiso', 'error')
        return redirect(url_for('main.dashboard'))
    
    es_dueno = False
    if current_user.es_admin():
        es_dueno = True
    elif current_user.es_profesor():
        if actividad.profesor_id == current_user.id:
            es_dueno = True
    
    if not es_dueno:
        flash('No tienes permiso', 'error')
        return redirect(url_for('main.dashboard'))
    
    lectura_id = actividad.lectura_id
    try:
        db.session.delete(actividad)
        db.session.commit()
        flash('Actividad eliminada', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'error')
    
    return redirect(url_for('main.ver_lectura', lectura_id=lectura_id))


@admin_bp.route('/actividades')
@login_required
def lista_actividades():
    if not current_user.es_admin() and not current_user.es_profesor():
        flash('No tienes permiso', 'error')
        return redirect(url_for('main.dashboard'))
    
    try:
        from models.actividad import Actividad
        if current_user.es_admin():
            actividades = Actividad.query.all()
        else:
            actividades = Actividad.query.filter_by(profesor_id=current_user.id).all()
    except:
        actividades = []
    
    return render_template('lista_actividades.html', actividades=actividades)