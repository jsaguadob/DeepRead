from extensions import db
from models.lectura import Lectura, Pregunta
from datetime import datetime

LECTURAS_INICIALES = [
    {
        'titulo': '¿Qué es la contaminación?',
        'contenido': '''La contaminación es la presencia de sustancias peligrosas en el medio ambiente. Estos pueden ser productos químicos, partículas, o microorganismos que afectan negativamente la salud de los seres vivos.

Tipos principales de contaminación:
- Contaminación del aire: Causada por emisiones de fábricas, vehículos y quemas.
- Contaminación del agua: Provocada por descargas industriales y residuos domésticos.
- Contaminación del suelo: Ocurre cuando productos químicos se filtran en la tierra.

Efectos en la salud:
La contaminación puede causar enfermedades respiratorias, alergias, y problemas crónicos. Los niños y personas mayores son más vulnerables.

¿Qué podemos hacer?
- Reducir el uso de plásticos
- Usar transporte público o bicicleta
- Reciclar correctamente
- Ahorrar energía en casa''',
        'nivel': 1,
        'tiempo_estimado_minutos': 5,
        'puntos_recompensa': 10,
        'categoria': 'ciencia',
        'activa': True
    },
    {
        'titulo': 'El ciclo del agua',
        'contenido': '''El ciclo del agua es el proceso mediante el cual el agua circula constantemente en la Tierra. Este ciclo es fundamental para la vida en nuestro planeta.

Las etapas del ciclo del agua:
1. Evaporación: El sol calienta el agua de océanos, ríos y lagos, transformándola en vapor de agua que sube a la atmósfera.

2. Condensación: Cuando el vapor de agua se eleva y se enfría, se transforma en pequeñas gotitas que forman las nubes.

3. Precipitación: Cuando las nubes se cargan de demasiada agua, caen en forma de lluvia, nieve o granizo.

4. Escurrimiento: El agua fluye por ríos y arroyos de regreso a los océanos y lagos, comenzando el ciclo de nuevo.

Importancia del ciclo:
- Regula el clima global
- Distribuye agua dulce por la Tierra
- Mantiene los ecosistemas saludables
- Permite la agricultura

El ser humano interviene en este ciclo mediante la construcción de presas, sistemas de riego y plantas de tratamiento de agua.''',
        'nivel': 1,
        'tiempo_estimado_minutos': 5,
        'puntos_recompensa': 10,
        'categoria': 'ciencia',
        'activa': True
    },
    {
        'titulo': 'Los dinosaurios',
        'contenido': '''Los dinosaurios fueron reptiles的大型 que dominaron la Tierra durante el Período Mesozoico, hace aproximadamente 230 a 65 millones de años.

Características generales:
- Eran animales vertebrados
- Alguns eran herbívoros, otros carnívoros
- Variaban en tamaño: desde el tamaño de un gallo hasta más de 30 metros de largo
- Ponían huevos, como las aves actuales

Períodos de los dinosaurios:
- Triásico (250-200 millones de años): Surgimiento
- Jurásico (200-145 millones de años): Mayor diversidad
- Cretácico (145-65 millones de años): Extinción

¿Por qué se extinguieron?
La teoría más aceptada es que un asteroide impactó la Tierra hace 65 millones de años, causando cambios climáticos catastróficos.

 legados:
- Las aves son descendientes de los dinosaurios
- Los fósiles nos ayudan a entender la historia de la vida
- Inspiraron la paleontología como ciencia

Los dinosaurios siguen fascinando a científicos y niños, siendo uno de los temas más populares en la ciencia y el entretenimiento.''',
        'nivel': 1,
        'tiempo_estimado_minutos': 5,
        'puntos_recompensa': 10,
        'categoria': 'ciencia',
        'activa': True
    },
    {
        'titulo': 'La Revolución Industrial',
        'contenido': '''La Revolución Industrial fue un período de grands cambios económicos y tecnológicos que comenzó en Gran Bretaña a mediados del siglo XVIII y se extendió por todo el mundo.

Orígenes:
En el siglo XVIII, Gran Bretaña experimentó un boom económico gracias al comercio y la manufactura textil. La invención de nuevas máquinas cambió radicalmente la forma de producir bienes.

Innovaciones clave:
- Máquina de vapor: Transformó el transporte y la industria
- Telar mecánico: Automatizó la producción de tela
- Máquina de tren: Permitió transportar mercancías a larga distancia
- Revolución en la energía: Del carbón a la electricidad

Impacto social:
-Urbanización: Las ciudades crecieron enormamente
- Nuevas clases sociales: La clase obrera y la burguesía industrial
- Cambios en el trabajo: De talleres familiares a fábricas
- Condiciones laborales: Larguitas horas, bajos sueldos, trabajo infantil

Consecuencias a largo plazo:
- Aumento significativo de la producción
- Crecimiento económico sin precedentes
- Cambios sociales y políticos profundos
- Fundación del capitalismo moderno

La Revolución Industrial transformó completamente la sociedad y sentó las bases del mundo moderno en el que vivimos.''',
        'nivel': 2,
        'tiempo_estimado_minutos': 10,
        'puntos_recompensa': 15,
        'categoria': 'historia',
        'activa': True
    },
    {
        'titulo': 'Cambios climáticos',
        'contenido': '''El cambio climático es uno de los mayores desafíos que enfrenta la humanidad en el siglo XXI. Se refiere al calentamiento global del planeta causado principalmente por actividades humanas.

Causes del cambio climático:
1. Emisiones de CO2: La quema de combustibles fósiles (petrógeno, carbón, gas) libera dióxido de carbono a la atmósfera.
2. Deforestación: Los árboles absorben CO2, cuando se talan, este carbono se libera.
3. Agricultura: El ganado y los fertilizantes liberan gases de efecto invernadero.

Efectos del cambio climático:
- Aumento de la temperatura global
- Derretimiento de glaciares y polos
- Subida del nivel del mar
- Eventos climáticos extremos (sequías, inundaciones, huracanes)
- Pérdida de biodiversidad

Acciones para combatirlo:
- Transición hacia energías renovables
- Reducción del consumo de carne
- Transporte sostenible
- Reciclaje y reducción de residuos
- Reforestación

Papel de los jóvenes:
Los jóvenes desempenan un papel crucial en la lucha contra el cambio climático. A través de la educación, la innovación y la presión social, pueden impulsar cambios significativos.

El futuro depende de las decisiones que tomemos hoy. Cada acción cuenta en la transición hacia un mundo más sostenible.''',
        'nivel': 2,
        'tiempo_estimado_minutos': 10,
        'puntos_recompensa': 15,
        'categoria': 'ciencia',
        'activa': True
    },
    {
        'titulo': 'Internet y sociedad',
        'contenido': '''Internet ha transformado prácticamente todos los aspectos de nuestra vida cotidiana, desde la comunicación hasta el trabajo y el entretenimiento.

Impacto en la comunicación:
- Correo electrónico y mensajería instantánea
- Redes sociales para conectar con otros
- Videollamadas que reducen distancias
- Acceso instantáneo a información global

Efectos en la educación:
- Recursos educativos en línea
- Cursos masiva abiertos (MOOCs)
- Bibliotecas digitales
- Aprendizaje a distancia

Cambios en el trabajo:
- Trabajo remoto y nomadismo digital
- Colaboración en línea
- Tiendas electrónicas
- Automatización de procesos

Desafíos de la era digital:
- Privacidad y seguridad de datos
- Desinformación y fake news
- Brecha digital
- Adicción a pantallas
- Cyberdelincuencia

¿Qué significa ser un ciudadano digital responsable?
- Verificar fuentes antes de compartir
- Proteger datos personales
- Mantener conducta ética en línea
- Equilibrar tiempo en línea y fuera de línea
- Respetar a otros usuarios

Internet es una herramienta poderosa que, usada sabiamente, puede melhorar nuestra sociedad y conectar personas de todo el mundo.''',
        'nivel': 2,
        'tiempo_estimado_minutos': 10,
        'puntos_recompensa': 15,
        'categoria': 'actualidad',
        'activa': True
    },
    {
        'titulo': 'Filosofía del conocimiento',
        'contenido': '''La filosofía del conocimiento, también llamada epistemología, es la rama de la filosofía que estudia la naturaleza del conocimiento y la justificación de las creencias.

Preguntas fundamentales:
- ¿Qué es el conocimiento?
- ¿Cómo sabemos que algo es verdadero?
- ¿Cuál es la diferencia entre opinión y conocimiento?
- ¿Podemos confiar en nuestros sentidos?

Teorías principales del conocimiento:

1. Racionalismo:
Afirma que el conocimiento proviene principalmente de la razón. Filósofos como Platón y Descartes sostenían que ciertas verdades pueden conocerse mediante la lógica.

2. Empirismo:
主张 que todo conocimiento viene de la experiencia sensorial. Locke, Hume y Berkeley argumentaban que la mente es unaTabla rasa al nacer.

3. Constructivismo:
Sugiere que el conocimiento se construye activamente por el sujeto, integrando experiencia y reflexión.

El método científico:
La ciencia desarrolla un método riguroso para obtener conocimiento: observación, hipótesis, experimentación, análisis y teoría.

Límites del conocimiento:
- Nuestros sentidos pueden engañarnos
- El lenguaje tiene limitaciones
- Existe el problema de la regresión infinita
- La objetividad absoluta es difícil de lograr

Aplicaciones práticas:
- Evaluación críticade información
- Tomar decisiones informadas
- Evitar manipulaciones
- Desarrollo del pensamiento propio

La reflexión filosófica sobre el conocimiento nos ayuda a pensar de manera más clara y profunda sobre cualquier tema.''',
        'nivel': 3,
        'tiempo_estimado_minutos': 15,
        'puntos_recompensa': 25,
        'categoria': 'filosofía',
        'activa': True
    },
    {
        'titulo': 'Análisis crítico de medios',
        'contenido': '''El análisis crítico de medios es la práctica de examinar los mensajes de los medios de comunicación para comprender sus propósitos, sesgos e impactos en la sociedad.

¿Por qué es importante?
Vivimos rodeado de información mediática. Ser capaces de analizarla críticamente nos ayuda a tomar decisiones informadas y evitar manipulaciones.

Elementos a analizar:

1. Fuentes:
- ¿Quién produce la información?
- ¿Tiene intereses económicos o políticos?
- ¿Es una fuente confiable?

2. Sesgos:
- Todo medio tiene un punto de vista
- ¿Qué perspectivas se incluyen y cuáles se excluyen?
- ¿Cómo se presenta la información?

3. Técnicas de persuasión:
- Uso de emociones (miedo, esperanza, enojo)
- Generalizaciones y falacias lógicas
- Imágenes selecionadas estratégicamente
- Testimonios de expertos o celebridades

4. Contexto:
- ¿Cuándo se publicó?
- ¿Qué otros datos existen?
- ¿Cuál es la historia completa?

Tipos de medios:
- Medios tradicionales (periódico, TV, radio)
- Medios digitales y redes sociales
- Blogs y plataformas independientes
- Redes sociales como fuentes de noticias

Preguntas clave para el análisis:
- ¿Qué no me están diciendo?
- ¿Cuál es el propósito de este mensaje?
- ¿De dónde viene esta información?
- ¿Es verificable en otras fuentes?

Ser un consumidor crítico de medios es esencial para la democracia y la participación ciudadana informada.''',
        'nivel': 3,
        'tiempo_estimado_minutos': 15,
        'puntos_recompensa': 25,
        'categoria': 'actualidad',
        'activa': True
    },
    {
        'titulo': 'Pensamiento crítico',
        'contenido': '''El pensamiento crítico es la habilidad de analizar información de manera sistemática para formar un juicio fundamentado. Es una competencia esencial en el mundo actual.

Características del pensador crítico:
- Pregunta siempre: ¿Por qué es esto así?
- Considera múltiples perspectivas
- Busca evidencia antes de concluir
- Reconoce sus propios sesgos
- Está dispuesto a cambiar de opinión

Procesos del pensamiento crítico:

1. Identificar el problema o pregunta
2. Recopilar información relevante
3. Analizar supuestos y sesgos
4. Evaluar evidencia
5. Considerar alternativas
6. Sacar conclusiones fundamentadas
7. Reflexionar sobre el proceso

Obstáculos para pensar críticamente:
- Sesgo de confirmación: Buscar solo lo que confirma nuestras creencias
- Ad hominem: Atacar a la persona en lugar del argumento
- Generalizaciones amplias: Sacar conclusiones de casos aislados
- Apelar a la autoridad: Aceptar algo solo porque lo dice un experto
- Pensamiento grupal: Seguir a la mayoría sin cuestionar

Aplicaciones en la vida diaria:
- Evaluar noticias y redes sociales
- Tomar decisiones importantes
- Resolver problemas complejos
- Comunicarse efectivamente
- Evitar estafas y engaños

Cómo desarrollar el pensamiento crítico:
- Lee diversidad de fuentes
- Practica el hábito de cuestionar
- Escribe tus razonamientos
- Discute con otros puntos de vista
- Sé paciente contigo mismo

El pensamiento crítico no significa ser escéptico de todo, sino usar la razón y la evidencia para llegar a conclusiones más cercanas a la verdad.''',
        'nivel': 3,
        'tiempo_estimado_minutos': 15,
        'puntos_recompensa': 25,
        'categoria': 'filosofía',
        'activa': True
    },
    {
        'titulo': 'Economía de la atención y transformación cognitiva en la era digital',
        'contenido': '''La economía de la atención es un paradigma económico donde la atención humana se considera un recurso scarce y valioso. En la era digital, las empresas compiten por captar nuestra atención, ya que es el primer paso para obtener nuestro tiempo, dinero y lealtad.

La atención como recurso limitado:
Nuestro cerebro puede procesar información limitada en un momento dado. Estimamos que tomamos entre 20,000 a 50,000 decisiones al día, muchas de ellas automáticas. Cuando prestamos atención a algo, dejamos de prestar atención a otra cosa. Por eso, la atención esZero-sum: si una app la captura, otra la pierde.

El modelo de negocio de las redes sociales:
Plataformas como Facebook, Instagram, TikTok y YouTube no cobran al usuario directamente. Su producto es la atención del usuario, que luego venden a anunciantes. Cuanto más tiempo pasamos en la plataforma, más valiosa es para los anunciantes.

Técnicas de captura de atención:
- Notificaciones push: Crean urgencia artificial
- Scroll infinito: Eliminan puntos de cierre naturales
- Likes y validación social: Activan circuitos de recompensa
- Contenido algorítmico: Optimizan lo que más nos engancha
- Microcompromiso: Piden pequeñas acciones que generan apego
- FOMO (Fear of Missing Out): Crean miedo a perderse algo

La dopamina y el ciclo de recompensa:
Cada like, comentario oseguidor nuevo libera dopamina, la misma sustancia asociada con la comida, el sexo y las drogas. Este ciclo de recompensas variables es altamente adictivo, similar a las máquinas tragamón.

Efectos en nuestra cognición:
- Dificultad para concentrarse en tareas largas
- Reducción de la capacidad de atención sostenida
- Cambios en la estructura cerebral relacionados con la memoria
- Aumento de niveles de ansiedad y depresión, especialmente en jóvenes
- Desplazamiento de actividades Offline por otras Online

La transformación cognitiva:
Pasamos de ser cazadores de información a ser cazadores de validación. Priorizamos la cantidad de likes sobre la calidad de nuestras experiencias. Documentamos momentos en lugar de vivirlos.

Estrategias para proteger nuestra atención:
- Desactivar notificaciones push
- Establecer tiempos específicos para revisar redes
- Usar aplicaciones que bloquean distracciones
- Practicar la单任务 (hacer una cosa a la vez)
- Medir el tiempo de pantalla y establecer límites
- Elegir intencionalmente qué consumir

La atención es el filtro más importante de nuestra realidad. Lo que atendemos define qué experiencias tenemos y, en última instancia, quiénes somos.''',
        'nivel': 3,
        'tiempo_estimado_minutos': 15,
        'puntos_recompensa': 25,
        'categoria': 'psicología',
        'activa': True
    }
]

PREGUNTAS_INICIALES = [
    {
        'lectura_id': 1,
        'pregunta': '¿Qué tipo de contaminación es causada por emisiones de fábricas?',
        'opcion_a': 'Contaminación del aire',
        'opcion_b': 'Contaminación del agua',
        'opcion_c': 'Contaminación del suelo',
        'opcion_d': 'Contaminación auditiva',
        'respuesta_correcta': 'a',
        'explicacion': 'Las fábricas liberan gases y partículas a la atmósfera, lo que causa contaminación del aire.'
    },
    {
        'lectura_id': 1,
        'pregunta': '¿Quiénes son más vulnerables a la contaminación?',
        'opcion_a': 'Los adultos jóvenes',
        'opcion_b': 'Los niños y personas mayores',
        'opcion_c': 'Los deportistas',
        'opcion_d': 'Los doctores',
        'respuesta_correcta': 'b',
        'explicacion': 'Los niños y personas mayores tienen sistemas imunológicos más débiles.'
    },
    {
        'lectura_id': 2,
        'pregunta': '¿Qué es la evaporación?',
        'opcion_a': 'El agua cae de las nubes',
        'opcion_b': 'El agua se transforma en vapor por el calor',
        'opcion_c': 'El agua fluye por los ríos',
        'opcion_d': 'El agua se congela',
        'respuesta_correcta': 'b',
        'explicacion': 'La evaporación ocurre cuando el calor transforma el agua líquida en vapor.'
    },
    {
        'lectura_id': 3,
        'pregunta': '¿Cuándo se extinguieron los dinosaurios?',
        'opcion_a': 'Hace 1 millón de años',
        'opcion_b': 'Hace 65 millones de años',
        'opcion_c': 'Hace 1000 años',
        'opcion_d': 'Hace 250 millones de años',
        'respuesta_correcta': 'b',
        'explicacion': 'Los dinosaurios se extinguieron hace aproximadamente 65 millones de años.'
    },
    {
        'lectura_id': 4,
        'pregunta': '¿En qué país comenzó la Revolución Industrial?',
        'opcion_a': 'Francia',
        'opcion_b': 'España',
        'opcion_c': 'Gran Bretaña',
        'opcion_d': 'Alemania',
        'respuesta_correcta': 'c',
        'explicacion': 'La Revolución Industrial comenzó en Gran Bretaña a mediados del siglo XVIII.'
    },
    {
        'lectura_id': 5,
        'pregunta': '¿Cuál es una causa principal del cambio climático?',
        'opcion_a': 'Quema de combustibles fósiles',
        'opcion_b': 'Más personas en el mundo',
        'opcion_c': 'Animales salvajes',
        'opcion_d': 'Lluvia ácida',
        'respuesta_correcta': 'a',
        'explicacion': 'La quema de combustibles fósiles libera CO2, principal gas de efecto invernadero.'
    },
    {
        'lectura_id': 6,
        'pregunta': '¿Qué es el nomadismo digital?',
        'opcion_a': 'Viajar por el mundo',
        'opcion_b': 'Trabajar desde cualquier lugar con internet',
        'opcion_c': 'Vivir en tiendas',
        'opcion_d': 'Navegar en internet',
        'respuesta_correcta': 'b',
        'explicacion': 'El nomadismo digital es trabajar remotamente desde cualquier ubicación.'
    },
    {
        'lectura_id': 7,
        'pregunta': '¿Qué sostiene el empirismo?',
        'opcion_a': 'El conocimiento viene de la razón',
        'opcion_b': 'El conocimiento viene de la experiencia',
        'opcion_c': 'El conocimiento es innato',
        'opcion_d': 'No hay conocimiento posible',
        'respuesta_correcta': 'b',
        'explicacion': 'El empirismo sostiene que todo conocimiento proviene de la experiencia sensorial.'
    },
    {
        'lectura_id': 8,
        'pregunta': '¿Qué es el sesgo de confirmación?',
        'opcion_a': 'Buscar solo información que confirma nuestras creencias',
        'opcion_b': 'Confirmar identidad de usuario',
        'opcion_c': 'Editar imágenes',
        'opcion_d': 'Publicar noticias falsas',
        'respuesta_correcta': 'a',
        'explicacion': 'Es la tendencia a buscar información que confirma lo que já sabemos.'
    },
    {
        'lectura_id': 9,
        'pregunta': '¿Qué implica el pensamiento crítico?',
        'opcion_a': 'Aceptar todo lo que nos dicen',
        'opcion_b': 'Solo creer en científicos',
        'opcion_c': 'Analizar información usando razón y evidencia',
        'opcion_d': 'No confiar en nadie',
        'respuesta_correcta': 'c',
        'explicacion': 'El pensamiento crítico analiza información sistemáticamente para formar juicios fundamentados.'
    }
]


def inicializar_datos():
    """Inicializa la base de datos con lecturas y preguntas iniciales."""
    
    for lectura_data in LECTURAS_INICIALES:
        lectura_existente = Lectura.query.filter_by(titulo=lectura_data['titulo']).first()
        if not lectura_existente:
            lectura = Lectura(**lectura_data)
            db.session.add(lectura)
    
    db.session.commit()
    
    for pregunta_data in PREGUNTAS_INICIALES:
        pregunta_existente = Pregunta.query.filter_by(
            lectura_id=pregunta_data['lectura_id'],
            pregunta=pregunta_data['pregunta']
        ).first()
        if not pregunta_existente:
            pregunta = Pregunta(**pregunta_data)
            db.session.add(pregunta)
    
    preguntas_atencion = [
        {
            'lectura_id': 10,
            'pregunta': '¿Por qué la atención humana se considera un recurso valioso en la economía digital?',
            'opcion_a': 'Porque todo el mundo tiene toda la atención que necesita',
            'opcion_b': 'Porque es limitada y las empresas compiten por ella',
            'opcion_c': 'Porque podemos prestar atención a muchas cosas a la vez',
            'opcion_d': 'Porque es gratis',
            'respuesta_correcta': 'b',
            'explicacion': 'La atención es un recurso limitado: si una app la captura, otra la pierde.'
        },
        {
            'lectura_id': 10,
            'pregunta': '¿Cuál es el producto que venden las redes sociales?',
            'opcion_a': 'Contenido gratuito',
            'opcion_b': 'La atención del usuario',
            'opcion_c': 'Seguidores',
            'opcion_d': 'Aplicaciones móviles',
            'respuesta_correcta': 'b',
            'explicacion': 'Las redes sociales venden la atención del usuario a los anunciantes.'
        },
        {
            'lectura_id': 10,
            'pregunta': '¿Qué es el ciclo de recompensa variable?',
            'opcion_a': 'Un ejercicio físico',
            'opcion_b': 'Un patrón de recompensa aleatorio altamente adictivo',
            'opcion_c': 'Una técnica de estudio',
            'opcion_d': 'Un tipo de meditación',
            'respuesta_correcta': 'b',
            'explicacion': 'Similar a las máquinas tragamón, activa los circuitos de dopamina.'
        },
        {
            'lectura_id': 10,
            'pregunta': '¿Cuál es una estrategia para proteger nuestra atención?',
            'opcion_a': 'Mantener notificaciones siempre activas',
            'opcion_b': 'Revisar redes constantemente',
            'opcion_c': 'Desactivar notificaciones push y establecer tiempos específicos',
            'opcion_d': 'Estar siempre conectado',
            'respuesta_correcta': 'c',
            'explicacion': 'Elegir intencionalmente qué consumir ayuda a proteger la atención.'
        },
        {
            'lectura_id': 10,
            'pregunta': '¿Qué define en gran medida quiénes somos?',
            'opcion_a': 'Los likes que recibimos',
            'opcion_b': 'Las redes sociales que usamos',
            'opcion_c': 'Lo que atendemos',
            'opcion_d': 'Cuánto dinero tenemos',
            'respuesta_correcta': 'c',
            'explicacion': 'La atención es el filtro más importante de nuestra realidad.'
        }
    ]
    
    for pregunta_data in preguntas_atencion:
        pregunta_existente = Pregunta.query.filter_by(
            lectura_id=pregunta_data['lectura_id'],
            pregunta=pregunta_data['pregunta']
        ).first()
        if not pregunta_existente:
            pregunta = Pregunta(**pregunta_data)
            db.session.add(pregunta)
    
    db.session.commit()
    print("Datos iniciales cargados correctamente.")