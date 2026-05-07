from extensions import db
from models.user import Usuario
from models.lectura import Lectura
from models.quiz import Quiz
from datetime import datetime, date
from werkzeug.security import generate_password_hash


SEED_READINGS = [
    {
        "titulo": "El origen del universo",
        "contenido": """El universo tal como lo conocemos comenzó hace aproximadamente 13.800 millones de años con el Big Bang. En ese momento, toda la materia y la energía estaban concentradas en un punto infinitamente pequeño y denso. De repente, ese punto explotó y comenzó a expandirse.

En los primeros segundos después del Big Bang, el universo era una sopa caliente de partículas elementales. A medida que se enfrió, los protones y neutrones comenzaron a formarse. Después de unos 380.000 años, los electrones se combinaron con los protones para formar los primeros átomos de hidrógeno y helio.

Las primeras estrellas aparecieron unos 200 millones de años después del Big Bang. Estas estrellas eran enormes y vivían poco tiempo, pero en su interior crearon elementos más pesados como el carbono y el oxígeno. Cuando estas estrellas explotaron como supernovas, esparcieron estos elementos por el espacio, permitiendo la formación de planetas y, eventualmente, la vida.

Hoy sabemos que el universo continúa expandiéndose, y cada vez lo hace más rápido. Los científicos creen que esto se debe a la energía oscura, una fuerza misteriosa que representa aproximadamente el 68% del universo. El resto está compuesto por materia oscura (27%) y materia ordinaria (5%), que es todo lo que podemos ver.""",
        "categoria": "Ciencia",
        "nivel": 1,
        "publica": True,
        "preguntas": [
            {
                "pregunta": "¿Hace cuánto tiempo ocurrió el Big Bang?",
                "opciones": ["5.000 millones de años", "13.800 millones de años", "1.000 millones de años", "100.000 años"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿Qué elementos se formaron primero después del Big Bang?",
                "opciones": ["Carbono y oxígeno", "Hidrógeno y helio", "Hierro y níquel", "Uranio y plutonio"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿Cómo se crearon los elementos más pesados como el carbono?",
                "opciones": ["En el interior de las estrellas", "Directamente en el Big Bang", "En la atmósfera de los planetas", "Por descomposición radiactiva"],
                "respuesta_correcta": 0
            },
            {
                "pregunta": "¿Qué porcentaje del universo está compuesto por materia ordinaria?",
                "opciones": ["68%", "27%", "5%", "50%"],
                "respuesta_correcta": 2
            },
            {
                "pregunta": "¿Qué causa que el universo se expanda cada vez más rápido?",
                "opciones": ["La gravedad", "La energía oscura", "La materia oscura", "Las supernovas"],
                "respuesta_correcta": 1
            }
        ]
    },
    {
        "titulo": "Breve historia del internet",
        "contenido": """El Internet comenzó como un proyecto militar estadounidense en la década de 1960 llamado ARPANET. Su objetivo era crear una red de comunicaciones que pudiera sobrevivir a un ataque nuclear. La primera conexión exitosa ocurrió en 1969 entre la Universidad de California y el Instituto de Investigación de Stanford.

En la década de 1970, Vint Cerf y Bob Kahn desarrollaron el protocolo TCP/IP, que permitió que diferentes redes se conectaran entre sí. Este protocolo se convirtió en el estándar en 1983 y es la base del Internet actual.

La World Wide Web fue inventada en 1989 por Tim Berners-Lee mientras trabajaba en el CERN en Suiza. Él creó el primer navegador web y el lenguaje HTML. En 1991, la web se abrió al público. Los primeros sitios web eran solo texto, sin imágenes ni videos.

En 1998 se fundó Google, revolucionando la forma en que encontramos información en línea. Para el año 2000, la burbuja de las puntocom estalló, pero las empresas que sobrevivieron como Amazon y eBay se convirtieron en gigantes tecnológicos.

Las redes sociales transformaron Internet en la década de 2000: Facebook en 2004, YouTube en 2005 y Twitter en 2006. Hoy, más de 5.000 millones de personas usan Internet, y se ha vuelto esencial para el trabajo, la educación y el entretenimiento.""",
        "categoria": "Tecnología",
        "nivel": 1,
        "publica": True,
        "preguntas": [
            {
                "pregunta": "¿Cómo se llamó el proyecto que dio origen a Internet?",
                "opciones": ["ENIAC", "ARPANET", "World Wide Web", "TCP/IP"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿En qué año ocurrió la primera conexión exitosa de ARPANET?",
                "opciones": ["1965", "1969", "1975", "1983"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿Quién inventó la World Wide Web?",
                "opciones": ["Vint Cerf", "Bill Gates", "Tim Berners-Lee", "Steve Jobs"],
                "respuesta_correcta": 2
            },
            {
                "pregunta": "¿Cuál fue la innovación clave del protocolo TCP/IP?",
                "opciones": ["Permitir la conexión entre diferentes redes", "Crear el primer navegador", "Permitir el envío de correos", "Comprimir datos"],
                "respuesta_correcta": 0
            },
            {
                "pregunta": "¿Aproximadamente cuántas personas usan Internet hoy?",
                "opciones": ["1.000 millones", "3.000 millones", "5.000 millones", "8.000 millones"],
                "respuesta_correcta": 2
            }
        ]
    },
    {
        "titulo": "El ciclo del agua",
        "contenido": """El ciclo del agua es el proceso continuo mediante el cual el agua se mueve a través de la Tierra y su atmósfera. Es esencial para la vida y mantiene el equilibrio de nuestros ecosistemas. El ciclo no tiene principio ni fin, pero podemos describirlo en varias etapas principales.

La evaporación es la primera etapa. El sol calienta el agua de océanos, lagos y ríos, convirtiéndola en vapor de agua que asciende a la atmósfera. La transpiración de las plantas también libera vapor de agua, un proceso conocido como evapotranspiración. Se estima que el 90% del vapor de agua en la atmósfera proviene de los océanos.

La condensación ocurre cuando el vapor de agua se enfría en la atmósfera y se convierte nuevamente en gotitas líquidas, formando nubes. Cuando estas gotitas se unen y crecen lo suficiente, caen por su propio peso en forma de precipitación: lluvia, nieve o granizo.

La precipitación devuelve el agua a la superficie terrestre. Parte de esta agua se infiltra en el suelo, recargando los acuíferos subterráneos. Otra parte escurre por la superficie hacia ríos y lagos, y eventualmente regresa al océano. El ciclo entonces comienza de nuevo.

El agua dulce disponible para el consumo humano representa solo el 2.5% de toda el agua del planeta, y la mayor parte está congelada en glaciares. Esto hace que la conservación del agua sea fundamental para nuestro futuro.""",
        "categoria": "Ciencia Ambiental",
        "nivel": 1,
        "publica": True,
        "preguntas": [
            {
                "pregunta": "¿Qué porcentaje del vapor de agua en la atmósfera proviene de los océanos?",
                "opciones": ["50%", "70%", "90%", "99%"],
                "respuesta_correcta": 2
            },
            {
                "pregunta": "¿Cómo se llama el proceso por el cual las plantas liberan vapor de agua?",
                "opciones": ["Evaporación", "Condensación", "Transpiración", "Precipitación"],
                "respuesta_correcta": 2
            },
            {
                "pregunta": "¿Qué ocurre durante la condensación?",
                "opciones": ["El agua se convierte en vapor", "El vapor se convierte en gotitas", "El agua cae como lluvia", "El agua se filtra en el suelo"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿Qué porcentaje del agua del planeta es agua dulce?",
                "opciones": ["2.5%", "10%", "25%", "50%"],
                "respuesta_correcta": 0
            },
            {
                "pregunta": "¿Cuál es la etapa que devuelve el agua a la superficie terrestre?",
                "opciones": ["Evaporación", "Condensación", "Precipitación", "Infiltración"],
                "respuesta_correcta": 2
            }
        ]
    },
    {
        "titulo": "El Renacimiento: un nuevo amanecer",
        "contenido": """El Renacimiento fue un movimiento cultural y artístico que comenzó en Italia en el siglo XIV y se extendió por Europa hasta el siglo XVII. La palabra "renacimiento" significa "renacer", y el período se caracterizó por un renovado interés en el arte, la ciencia y la cultura de la antigua Grecia y Roma.

Uno de los aspectos más importantes del Renacimiento fue el humanismo, una filosofía que ponía al ser humano en el centro del universo. Los humanistas creían en el potencial de las personas para lograr grandes cosas a través de la educación y la razón. Esto contrastaba con la mentalidad medieval, que se centraba principalmente en Dios y la religión.

Leonardo da Vinci (1452-1519) es quizás el ejemplo más famoso del "hombre renacentista". Fue pintor, escultor, arquitecto, científico, matemático e inventor. Sus obras más conocidas incluyen la Mona Lisa y La Última Cena. También diseñó máquinas voladoras y estudió la anatomía humana mediante disecciones.

Miguel Ángel (1475-1564) fue otro gigante del Renacimiento. Esculpió el David y pintó la bóveda de la Capilla Sixtina en el Vaticano. Su trabajo mostraba un profundo conocimiento de la anatomía humana y una belleza idealizada.

La invención de la imprenta por Johannes Gutenberg alrededor de 1440 fue crucial para difundir las ideas renacentistas. Por primera vez, los libros podían producirse en masa, lo que permitió que el conocimiento llegara a más personas y aceleró el cambio cultural en toda Europa.""",
        "categoria": "Arte e Historia",
        "nivel": 2,
        "publica": True,
        "preguntas": [
            {
                "pregunta": "¿En qué siglo comenzó el Renacimiento en Italia?",
                "opciones": ["Siglo XII", "Siglo XIV", "Siglo XVI", "Siglo XVIII"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿Qué filosofía caracterizó al Renacimiento?",
                "opciones": ["El estoicismo", "El humanismo", "El escolasticismo", "El positivismo"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿Cuál de estas obras fue creada por Leonardo da Vinci?",
                "opciones": ["El David", "La Capilla Sixtina", "La Mona Lisa", "El Nacimiento de Venus"],
                "respuesta_correcta": 2
            },
            {
                "pregunta": "¿Qué invento ayudó a difundir las ideas renacentistas?",
                "opciones": ["El telescopio", "La brújula", "La imprenta", "El reloj"],
                "respuesta_correcta": 2
            },
            {
                "pregunta": "¿Quién pintó la bóveda de la Capilla Sixtina?",
                "opciones": ["Leonardo da Vinci", "Rafael", "Donatello", "Miguel Ángel"],
                "respuesta_correcta": 3
            }
        ]
    },
    {
        "titulo": "El sistema solar",
        "contenido": """Nuestro sistema solar está formado por el Sol y todos los objetos celestes que orbitan a su alrededor. Se formó hace aproximadamente 4.600 millones de años a partir de una nube gigante de gas y polvo llamada nebulosa solar.

El Sol es una estrella de tamaño mediano que contiene el 99.8% de toda la masa del sistema solar. Su energía proviene de reacciones de fusión nuclear en su núcleo, donde el hidrógeno se convierte en helio a temperaturas de aproximadamente 15 millones de grados Celsius.

Los planetas del sistema solar se dividen en dos grupos. Los planetas interiores o terrestres son Mercurio, Venus, Tierra y Marte. Son rocosos y relativamente pequeños. Los planetas exteriores o gigantes son Júpiter, Saturno, Urano y Neptuno. Son mucho más grandes y están compuestos principalmente de gas.

Júpiter es el planeta más grande del sistema solar, con un diámetro 11 veces mayor que el de la Tierra. Su Gran Mancha Roja es una tormenta gigante que ha durado cientos de años. Saturno es famoso por sus impresionantes anillos, compuestos de hielo y roca.

Marte ha sido objeto de gran interés científico porque muestra evidencia de que pudo haber tenido agua líquida en su superficie en el pasado. Los rovers como Perseverance están explorando el planeta en busca de señales de vida pasada. Plutón fue reclasificado como planeta enano en 2006 por la Unión Astronómica Internacional.""",
        "categoria": "Astronomía",
        "nivel": 2,
        "publica": True,
        "preguntas": [
            {
                "pregunta": "¿Cuánta masa del sistema solar contiene el Sol?",
                "opciones": ["50%", "75%", "99.8%", "100%"],
                "respuesta_correcta": 2
            },
            {
                "pregunta": "¿Cuáles son los planetas interiores o terrestres?",
                "opciones": ["Júpiter, Saturno, Urano, Neptuno", "Mercurio, Venus, Tierra, Marte", "Venus, Tierra, Marte, Júpiter", "Mercurio, Tierra, Marte, Saturno"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿Qué es la Gran Mancha Roja de Júpiter?",
                "opciones": ["Un volcán", "Un océano", "Una tormenta gigante", "Un cráter"],
                "respuesta_correcta": 2
            },
            {
                "pregunta": "¿Por qué Plutón ya no se considera un planeta?",
                "opciones": ["Porque es demasiado pequeño", "Porque fue reclasificado como planeta enano", "Porque se desintegró", "Porque salió del sistema solar"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿Qué tipo de reacción genera la energía del Sol?",
                "opciones": ["Fisión nuclear", "Fusión nuclear", "Combustión química", "Energía geotérmica"],
                "respuesta_correcta": 1
            }
        ]
    },
    {
        "titulo": "La fotosíntesis",
        "contenido": """La fotosíntesis es el proceso mediante el cual las plantas, algas y algunas bacterias convierten la energía de la luz solar en energía química. Es uno de los procesos más importantes para la vida en la Tierra, ya que produce el oxígeno que respiramos y es la base de la cadena alimenticia.

El proceso ocurre principalmente en las hojas de las plantas, dentro de orgánulos llamados cloroplastos. Estos contienen clorofila, el pigmento que da a las plantas su color verde y que captura la energía de la luz solar.

La fotosíntesis se puede resumir en una ecuación simple: dióxido de carbono (CO2) más agua (H2O), con la ayuda de la luz solar, produce glucosa (C6H12O6) y oxígeno (O2). En términos más simples, las plantas toman CO2 del aire y agua del suelo, y usando la energía del sol, producen su alimento y liberan oxígeno.

La fotosíntesis tiene dos fases principales. La fase luminosa depende de la luz solar y produce ATP y NADPH. La fase oscura o ciclo de Calvin no necesita luz directamente y utiliza el ATP y NADPH para convertir el CO2 en glucosa.

Sin la fotosíntesis, la atmósfera terrestre no tendría oxígeno y la vida como la conocemos no existiría. Además, este proceso ayuda a regular el clima al absorber grandes cantidades de CO2, uno de los principales gases de efecto invernadero.""",
        "categoria": "Biología",
        "nivel": 2,
        "publica": True,
        "preguntas": [
            {
                "pregunta": "¿Dónde ocurre la fotosíntesis dentro de las células de las plantas?",
                "opciones": ["En las mitocondrias", "En los cloroplastos", "En el núcleo", "En la membrana celular"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿Qué pigmento captura la energía de la luz solar?",
                "opciones": ["La melanina", "La clorofila", "La hemoglobina", "La carotenoides"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿Qué produce la fotosíntesis además de glucosa?",
                "opciones": ["Dióxido de carbono", "Nitrógeno", "Oxígeno", "Hidrógeno"],
                "respuesta_correcta": 2
            },
            {
                "pregunta": "¿Cuál es la fase de la fotosíntesis que no necesita luz directamente?",
                "opciones": ["Fase luminosa", "Ciclo de Calvin", "Fase de oxidación", "Ciclo de Krebs"],
                "respuesta_correcta": 1
            },
            {
                "pregunta": "¿De dónde toman las plantas el dióxido de carbono para la fotosíntesis?",
                "opciones": ["Del suelo", "Del agua", "Del aire", "De los fertilizantes"],
                "respuesta_correcta": 2
            }
        ]
    }
]


def seed_database(admin_id=None):
    existing = Lectura.query.filter_by(publica=True).count()
    if existing > 0:
        return False, f"Ya existen {existing} lecturas públicas. No se agregaron datos para evitar duplicados."

    count = 0
    for item in SEED_READINGS:
        lectura = Lectura(
            titulo=item["titulo"],
            contenido=item["contenido"],
            categoria=item["categoria"],
            nivel=item["nivel"],
            publica=item["publica"],
            creador_id=admin_id,
            intentos_maximos=3,
            fecha_creacion=datetime.utcnow()
        )
        db.session.add(lectura)
        db.session.flush()

        for i, pq in enumerate(item["preguntas"]):
            from models.quiz import Opcion
            quiz = Quiz(
                lectura_id=lectura.id,
                pregunta=pq["pregunta"],
                orden=i + 1
            )
            db.session.add(quiz)
            db.session.flush()

            for j, opt_text in enumerate(pq["opciones"]):
                opcion = Opcion(
                    quiz_id=quiz.id,
                    texto=opt_text,
                    es_correcta=(j == pq["respuesta_correcta"]),
                    orden=j
                )
                db.session.add(opcion)

        count += 1

    db.session.commit()
    return True, f"Se crearon {count} lecturas públicas con sus quizzes."
