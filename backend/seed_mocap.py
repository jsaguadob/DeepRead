import bcrypt
import random
import string
from datetime import datetime, timedelta
from sqlalchemy import func
from extensions import db
from models.user import Usuario
from models.grupo import Grupo, MiembroGrupo
from models.lectura import Lectura, Pregunta
from models.progreso import ProgresoLectura
from models.quiz import RespuestaQuiz


def gerar_codigo(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def seed_mocap():
    DOMAIN = '@lacolina.edu.co'
    PASSWORD = 'password123'
    today = datetime.utcnow()

    existing = Usuario.query.filter_by(email='profesor' + DOMAIN).first()
    if existing:
        return False, 'Los datos mocap ya existen. Elimina profesor@lacolina.edu.co manualmente si quieres regenerar.'

    pw_hash = bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # --- PROFESOR ---
    profesor = Usuario(
        username='carlos.mendoza',
        email='carlos.mendoza' + DOMAIN,
        password_hash=pw_hash,
        rol='profesor',
        tipo_usuario='institucional',
        puntos_totales=0,
        nivel_actual=3
    )
    db.session.add(profesor)
    db.session.flush()

    # --- GRUPOS ---
    grupo_a = Grupo(nombre='Once A', descripcion='Curso 11° A - Colegio La Colina',
                    profesor_id=profesor.id, codigo_unico=gerar_codigo())
    grupo_b = Grupo(nombre='Once B', descripcion='Curso 11° B - Colegio La Colina',
                    profesor_id=profesor.id, codigo_unico=gerar_codigo())
    db.session.add(grupo_a)
    db.session.add(grupo_b)
    db.session.flush()

    db.session.add(MiembroGrupo(grupo_id=grupo_a.id, usuario_id=profesor.id, rol_en_grupo='profesor'))
    db.session.add(MiembroGrupo(grupo_id=grupo_b.id, usuario_id=profesor.id, rol_en_grupo='profesor'))

    # --- LECTURAS ---
    lecturas_data = [
        {
            'titulo': 'El calentamiento global y sus efectos',
            'contenido': 'El calentamiento global es el aumento gradual de la temperatura de la Tierra debido a la acumulación de gases de efecto invernadero en la atmósfera. Este fenómeno ha provocado el derretimiento de los glaciares, el aumento del nivel del mar y cambios en los patrones climáticos globales. Los científicos advierten que si no se reducen las emisiones de CO2, las consecuencias serán catastróficas para la biodiversidad y las comunidades humanas. Se estima que para el año 2100 la temperatura global podría aumentar entre 1.5 y 4.5 grados Celsius si no se toman medidas urgentes. Los principales responsables son la quema de combustibles fósiles, la deforestación y la agricultura intensiva.',
            'nivel': 2,
            'categoria': 'ciencia',
            'preguntas': [
                {'p': '¿Cuál es la principal causa del calentamiento global?', 'a': 'Los terremotos', 'b': 'La acumulación de gases de efecto invernadero', 'c': 'Las erupciones volcánicas', 'd': 'La rotación de la Tierra', 'r': 'B'},
                {'p': '¿Qué se estima que podría aumentar la temperatura para el año 2100?', 'a': '0.5 a 1 grado', 'b': '1.5 a 4.5 grados', 'c': '5 a 8 grados', 'd': '10 a 15 grados', 'r': 'B'},
                {'p': '¿Cuál NO es un responsable del calentamiento global mencionado?', 'a': 'Quema de combustibles fósiles', 'b': 'Deforestación', 'c': 'Agricultura intensiva', 'd': 'Energía solar', 'r': 'D'},
            ]
        },
        {
            'titulo': 'La Segunda Guerra Mundial',
            'contenido': 'La Segunda Guerra Mundial fue un conflicto militar global que se desarrolló entre 1939 y 1945. Enfrentó a las potencias del Eje (Alemania, Italia y Japón) contra los Aliados (Reino Unido, Francia, Estados Unidos y la Unión Soviética). Fue la guerra más mortífera de la historia, con un saldo de entre 70 y 85 millones de víctimas. El conflicto comenzó con la invasión de Polonia por parte de Alemania el 1 de septiembre de 1939. Terminó en Europa con la rendición de Alemania el 8 de mayo de 1945 y en el Pacífico con la rendición de Japón después de los bombardeos atómicos de Hiroshima y Nagasaki en agosto de 1945.',
            'nivel': 2,
            'categoria': 'historia',
            'preguntas': [
                {'p': '¿Entre qué años ocurrió la Segunda Guerra Mundial?', 'a': '1914-1918', 'b': '1939-1945', 'c': '1945-1950', 'd': '1920-1930', 'r': 'B'},
                {'p': '¿Cuál fue el evento que inició la guerra en Europa?', 'a': 'El bombardeo de Pearl Harbor', 'b': 'La invasión de Polonia', 'c': 'La Batalla de Inglaterra', 'd': 'La invasión de Francia', 'r': 'B'},
                {'p': '¿Cuántas víctimas aproximadamente causó esta guerra?', 'a': '10-20 millones', 'b': '30-50 millones', 'c': '70-85 millones', 'd': '100-120 millones', 'r': 'C'},
            ]
        },
        {
            'titulo': 'Estructura del ADN',
            'contenido': 'El ADN o ácido desoxirribonucleico es la molécula que contiene la información genética de todos los organismos vivos. Su estructura fue descubierta en 1953 por James Watson y Francis Crick, basándose en los estudios de Rosalind Franklin. El ADN tiene forma de doble hélice, compuesta por dos cadenas de nucleótidos enrolladas entre sí. Cada nucleótido está formado por un grupo fosfato, un azúcar (desoxirribosa) y una base nitrogenada (adenina, timina, citosina o guanina). Las bases se emparejan de forma específica: adenina con timina y citosina con guanina. Esta estructura permite la replicación del ADN y la transmisión de la información genética de una generación a otra.',
            'nivel': 3,
            'categoria': 'biologia',
            'preguntas': [
                {'p': '¿Quiénes descubrieron la estructura del ADN en 1953?', 'a': 'Mendel y Darwin', 'b': 'Watson y Crick', 'c': 'Franklin y Wilkins', 'd': 'Pasteur y Koch', 'r': 'B'},
                {'p': '¿Qué forma tiene la molécula de ADN?', 'a': 'Hélice simple', 'b': 'Doble hélice', 'c': 'Triple hélice', 'd': 'Estructura lineal', 'r': 'B'},
                {'p': '¿Con qué base se empareja la adenina?', 'a': 'Citosina', 'b': 'Guanina', 'c': 'Timina', 'd': 'Uracilo', 'r': 'C'},
            ]
        },
        {
            'titulo': 'El Quijote de la Mancha',
            'contenido': 'Don Quijote de la Mancha es una novela escrita por Miguel de Cervantes Saavedra, publicada en dos partes: la primera en 1605 y la segunda en 1615. Es considerada la obra más importante de la literatura española y una de las principales de la literatura universal. La novela narra las aventuras de Alonso Quijano, un hidalgo que enloquece leyendo libros de caballerías y decide hacerse caballero andante bajo el nombre de Don Quijote de la Mancha. Acompañado por su escudero Sancho Panza, vive numerosas aventuras en las que confunde la realidad con su imaginación. La obra es una crítica a los libros de caballerías y una exploración profunda de la naturaleza humana.',
            'nivel': 1,
            'categoria': 'literatura',
            'preguntas': [
                {'p': '¿Quién escribió Don Quijote de la Mancha?', 'a': 'Lope de Vega', 'b': 'Miguel de Cervantes', 'c': 'Garcilaso de la Vega', 'd': 'Francisco de Quevedo', 'r': 'B'},
                {'p': '¿Cómo se llama el escudero de Don Quijote?', 'a': 'Sancho Panza', 'b': 'Dulcinea', 'c': 'Rocinante', 'd': 'Cide Hamete', 'r': 'A'},
                {'p': '¿Por qué Don Quijote decide hacerse caballero andante?', 'a': 'Porque quiere ser famoso', 'b': 'Porque enloquece leyendo libros de caballerías', 'c': 'Porque hereda una armadura', 'd': 'Porque Sancho lo convence', 'r': 'B'},
            ]
        },
        {
            'titulo': 'El ciclo del agua',
            'contenido': 'El ciclo del agua es el proceso continuo mediante el cual el agua se mueve a través de la Tierra y su atmósfera. La evaporación ocurre cuando el sol calienta el agua de océanos, lagos y ríos, convirtiéndola en vapor de agua que asciende a la atmósfera. La transpiración de las plantas también libera vapor de agua. La condensación ocurre cuando el vapor de agua se enfría y se convierte en gotitas líquidas, formando nubes. La precipitación devuelve el agua a la superficie en forma de lluvia, nieve o granizo. El agua dulce disponible para consumo humano representa solo el 2.5% de toda el agua del planeta.',
            'nivel': 1,
            'categoria': 'ciencia',
            'preguntas': [
                {'p': '¿Qué porcentaje del agua del planeta es dulce?', 'a': '2.5%', 'b': '10%', 'c': '25%', 'd': '50%', 'r': 'A'},
                {'p': '¿Qué proceso convierte el agua líquida en vapor?', 'a': 'Condensación', 'b': 'Evaporación', 'c': 'Precipitación', 'd': 'Filtración', 'r': 'B'},
                {'p': '¿Qué ocurre durante la condensación?', 'a': 'El agua se convierte en vapor', 'b': 'El vapor se convierte en gotitas', 'c': 'El agua cae como lluvia', 'd': 'El agua se filtra en el suelo', 'r': 'B'},
            ]
        },
        {
            'titulo': 'Sistema de ecuaciones lineales',
            'contenido': 'Un sistema de ecuaciones lineales es un conjunto de dos o más ecuaciones de primer grado que deben resolverse simultáneamente. Existen tres métodos principales para resolverlos: sustitución, igualación y reducción. El método de sustitución consiste en despejar una variable en una ecuación y sustituirla en la otra. El método de igualación despeja la misma variable en ambas ecuaciones y las iguala. El método de reducción suma o resta las ecuaciones para eliminar una variable. La solución de un sistema de dos ecuaciones con dos incógnitas es un par ordenado (x, y) que satisface ambas ecuaciones. Un sistema puede tener solución única, infinitas soluciones o ninguna solución.',
            'nivel': 3,
            'categoria': 'matematicas',
            'preguntas': [
                {'p': '¿Cuántos métodos principales existen para resolver sistemas de ecuaciones?', 'a': 'Dos', 'b': 'Tres', 'c': 'Cuatro', 'd': 'Cinco', 'r': 'B'},
                {'p': '¿En qué consiste el método de sustitución?', 'a': 'Sumar las ecuaciones', 'b': 'Despejar una variable y sustituirla en la otra ecuación', 'c': 'Igualar las dos ecuaciones', 'd': 'Multiplicar las ecuaciones', 'r': 'B'},
                {'p': '¿Qué es la solución de un sistema 2x2?', 'a': 'Un número', 'b': 'Un par ordenado (x, y)', 'c': 'Una ecuación', 'd': 'Una variable', 'r': 'B'},
            ]
        }
    ]

    lecturas_creadas = []
    grupos_lecturas = [(grupo_a, 6), (grupo_b, 6)]

    for grupo, num_lect in grupos_lecturas:
        for li in range(num_lect):
            ld = lecturas_data[li % len(lecturas_data)]
            lectura = Lectura(
                titulo=ld['titulo'],
                contenido=ld['contenido'],
                nivel=ld['nivel'],
                tiempo_estimado_minutos=random.choice([10, 15, 20]),
                puntos_recompensa=100,
                categoria=ld.get('categoria'),
                profesor_id=profesor.id,
                grupo_id=grupo.id,
                es_publica=False,
                activa=True,
                intentos_maximos=3
            )
            db.session.add(lectura)
            db.session.flush()

            preguntas_ids = []
            for pq in ld['preguntas']:
                p = Pregunta(
                    lectura_id=lectura.id,
                    pregunta=pq['p'],
                    opcion_a=pq['a'],
                    opcion_b=pq['b'],
                    opcion_c=pq['c'],
                    opcion_d=pq['d'],
                    respuesta_correcta=pq['r'],
                    profesor_id=profesor.id
                )
                db.session.add(p)
                db.session.flush()
                preguntas_ids.append(p)

            lecturas_creadas.append((lectura, preguntas_ids, grupo))

    # --- ESTUDIANTES ---
    estudiantes_data = [
        ('Sofia', 'Rodriguez'), ('Valentina', 'Gomez'), ('Isabella', 'Martinez'),
        ('Camila', 'Lopez'), ('Gabriela', 'Gonzalez'), ('Samuel', 'Perez'),
        ('Mateo', 'Ramirez'), ('Santiago', 'Sanchez'), ('Sebastian', 'Torres'),
        ('Nicolas', 'Flores'), ('Laura', 'Diaz'), ('Maria', 'Moreno'),
        ('Daniela', 'Castro'), ('Ana', 'Ortiz'),
        # Once B
        ('Carolina', 'Morales'), ('Andres', 'Silva'), ('Felipe', 'Cruz'),
        ('Diego', 'Reyes'), ('Alejandro', 'Ramos'), ('Juan', 'Vargas'),
        ('Paula', 'Rodriguez'), ('Mariana', 'Gomez'), ('Juliana', 'Martinez'),
        ('Manuela', 'Lopez'), ('Ximena', 'Gonzalez'), ('Carlos', 'Perez'),
        ('Miguel', 'Ramirez'), ('David', 'Sanchez'), ('Jose', 'Torres'),
        ('Luis', 'Flores'), ('Pedro', 'Diaz')
    ]

    def sanitizar(s):
        import unicodedata
        s = s.lower()
        s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
        return s

    grupo_a_estudiantes = []
    grupo_b_estudiantes = []

    for i, (nombre, apellido) in enumerate(estudiantes_data):
        sn = sanitizar(nombre)
        sa = sanitizar(apellido)
        username = f'{sn}.{sa}'
        email = f'{sn}.{sa}{DOMAIN}'

        estudiante = Usuario(
            username=username,
            email=email,
            password_hash=pw_hash,
            rol='estudiante',
            tipo_usuario='institucional',
            puntos_totales=0,
            nivel_actual=1
        )
        db.session.add(estudiante)
        db.session.flush()

        if i < 14:
            grupo_a_estudiantes.append(estudiante)
            db.session.add(MiembroGrupo(grupo_id=grupo_a.id, usuario_id=estudiante.id, rol_en_grupo='estudiante'))
        else:
            grupo_b_estudiantes.append(estudiante)
            db.session.add(MiembroGrupo(grupo_id=grupo_b.id, usuario_id=estudiante.id, rol_en_grupo='estudiante'))

    db.session.flush()

    # --- PROGRESO Y RESPUESTAS ---
    random.seed(42)

    for lectura, preguntas_ids, grupo in lecturas_creadas:
        grupo_estudiantes = grupo_a_estudiantes if grupo.id == grupo_a.id else grupo_b_estudiantes

        for estudiante in grupo_estudiantes:
            # Distribucion realista: 60% completo/aprobado, 25% completo/sin-aprobar, 15% sin completar
            roll = random.random()

            if roll < 0.6:
                # Completo y aprobo el quiz
                intentos = random.randint(1, 2)
                fallos_count = random.randint(0, 2)
                correctas = len(preguntas_ids) - fallos_count
                porcentaje = (correctas / len(preguntas_ids)) * 100
                puntos = 100 if porcentaje >= 80 else 50

                progreso = ProgresoLectura(
                    usuario_id=estudiante.id,
                    lectura_id=lectura.id,
                    completada=True,
                    puntos_obtenidos=puntos,
                    intentos=intentos,
                    quiz_aprobado=porcentaje >= 80,
                    quiz_porcentaje=porcentaje,
                    fallos=fallos_count,
                    fecha_completado=today - timedelta(days=random.randint(1, 30))
                )
                db.session.add(progreso)
                db.session.flush()

                for pi, pq in enumerate(preguntas_ids):
                    correcta = pi < correctas
                    rq = RespuestaQuiz(
                        usuario_id=estudiante.id,
                        pregunta_id=pq.id,
                        respondida=pq.respuesta_correcta if correcta else random.choice(
                            [l for l in ['A', 'B', 'C', 'D'] if l != pq.respuesta_correcta]
                        ),
                        correcta=correcta
                    )
                    db.session.add(rq)

            elif roll < 0.85:
                intentos = random.randint(1, 3)
                fallos_count = random.randint(2, len(preguntas_ids))
                correctas = max(0, len(preguntas_ids) - fallos_count)
                porcentaje = (correctas / len(preguntas_ids)) * 100

                progreso = ProgresoLectura(
                    usuario_id=estudiante.id,
                    lectura_id=lectura.id,
                    completada=True,
                    incompleta=True,
                    puntos_obtenidos=max(1, 100 // intentos),
                    intentos=intentos,
                    quiz_aprobado=False,
                    quiz_porcentaje=porcentaje,
                    fallos=fallos_count,
                    fecha_completado=today - timedelta(days=random.randint(1, 15))
                )
                db.session.add(progreso)
                db.session.flush()

                for pq in preguntas_ids:
                    rq = RespuestaQuiz(
                        usuario_id=estudiante.id,
                        pregunta_id=pq.id,
                        respondida=random.choice(['A', 'B', 'C', 'D']),
                        correcta=False
                    )
                    db.session.add(rq)
            else:
                # No completo
                progreso = ProgresoLectura(
                    usuario_id=estudiante.id,
                    lectura_id=lectura.id,
                    completada=False,
                    puntos_obtenidos=0,
                    intentos=0,
                    quiz_aprobado=False,
                    quiz_porcentaje=0,
                    fallos=0
                )
                db.session.add(progreso)

    # --- CALCULAR PUNTOS TOTALES ---
    for estudiante in grupo_a_estudiantes + grupo_b_estudiantes:
        total = db.session.query(func.coalesce(func.sum(ProgresoLectura.puntos_obtenidos), 0))\
            .filter(ProgresoLectura.usuario_id == estudiante.id).scalar()
        estudiante.puntos_totales = total
        estudiante.nivel_actual = min(3, (total // 500) + 1)

    profesor.puntos_totales = 0

    db.session.commit()

    count_a = len(grupo_a_estudiantes)
    count_b = len(grupo_b_estudiantes)
    total_lect = len(lecturas_creadas)

    return True, f'Mocap creado: 1 profesor, {count_a}+{count_b} estudiantes, 2 grupos, {total_lect} lecturas con quizzes y progreso variado.'
