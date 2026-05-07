from extensions import db
from models.lectura import Lectura, Pregunta


SEED_READINGS = [
    {
        "titulo": "El origen del universo",
        "contenido": "El universo tal como lo conocemos comenzó hace aproximadamente 13.800 millones de años con el Big Bang. En ese momento, toda la materia y la energía estaban concentradas en un punto infinitamente pequeño y denso. De repente, ese punto explotó y comenzó a expandirse.\n\nEn los primeros segundos después del Big Bang, el universo era una sopa caliente de partículas elementales. A medida que se enfrió, los protones y neutrones comenzaron a formarse. Después de unos 380.000 años, los electrones se combinaron con los protones para formar los primeros átomos de hidrógeno y helio.\n\nLas primeras estrellas aparecieron unos 200 millones de años después del Big Bang. Estas estrellas eran enormes y vivían poco tiempo, pero en su interior crearon elementos más pesados como el carbono y el oxígeno. Cuando estas estrellas explotaron como supernovas, esparcieron estos elementos por el espacio, permitiendo la formación de planetas y, eventualmente, la vida.\n\nHoy sabemos que el universo continúa expandiéndose, y cada vez lo hace más rápido. Los científicos creen que esto se debe a la energía oscura, una fuerza misteriosa que representa aproximadamente el 68% del universo. El resto está compuesto por materia oscura (27%) y materia ordinaria (5%), que es todo lo que podemos ver.",
        "categoria": "Ciencia",
        "nivel": 1,
        "preguntas": [
            {"pregunta": "¿Hace cuánto tiempo ocurrió el Big Bang?", "a": "5.000 millones de años", "b": "13.800 millones de años", "c": "1.000 millones de años", "d": "100.000 años", "correcta": "B"},
            {"pregunta": "¿Qué elementos se formaron primero después del Big Bang?", "a": "Carbono y oxígeno", "b": "Hidrógeno y helio", "c": "Hierro y níquel", "d": "Uranio y plutonio", "correcta": "B"},
            {"pregunta": "¿Cómo se crearon los elementos más pesados como el carbono?", "a": "En el interior de las estrellas", "b": "Directamente en el Big Bang", "c": "En la atmósfera de los planetas", "d": "Por descomposición radiactiva", "correcta": "A"},
            {"pregunta": "¿Qué porcentaje del universo es materia ordinaria?", "a": "68%", "b": "27%", "c": "5%", "d": "50%", "correcta": "C"},
            {"pregunta": "¿Qué causa que el universo se expanda más rápido?", "a": "La gravedad", "b": "La energía oscura", "c": "La materia oscura", "d": "Las supernovas", "correcta": "B"}
        ]
    },
    {
        "titulo": "Breve historia del internet",
        "contenido": "El Internet comenzó como un proyecto militar estadounidense en la década de 1960 llamado ARPANET. Su objetivo era crear una red de comunicaciones que pudiera sobrevivir a un ataque nuclear. La primera conexión exitosa ocurrió en 1969 entre la Universidad de California y el Instituto de Investigación de Stanford.\n\nEn la década de 1970, Vint Cerf y Bob Kahn desarrollaron el protocolo TCP/IP, que permitió que diferentes redes se conectaran entre sí. Este protocolo se convirtió en el estándar en 1983 y es la base del Internet actual.\n\nLa World Wide Web fue inventada en 1989 por Tim Berners-Lee mientras trabajaba en el CERN en Suiza. Él creó el primer navegador web y el lenguaje HTML. En 1991, la web se abrió al público. Los primeros sitios web eran solo texto, sin imágenes ni videos.\n\nEn 1998 se fundó Google, revolucionando la forma en que encontramos información en línea. Para el año 2000, la burbuja de las puntocom estalló, pero las empresas que sobrevivieron como Amazon y eBay se convirtieron en gigantes tecnológicos.\n\nLas redes sociales transformaron Internet en la década de 2000: Facebook en 2004, YouTube en 2005 y Twitter en 2006. Hoy, más de 5.000 millones de personas usan Internet, y se ha vuelto esencial para el trabajo, la educación y el entretenimiento.",
        "categoria": "Tecnología",
        "nivel": 1,
        "preguntas": [
            {"pregunta": "¿Cómo se llamó el proyecto que dio origen a Internet?", "a": "ENIAC", "b": "ARPANET", "c": "World Wide Web", "d": "TCP/IP", "correcta": "B"},
            {"pregunta": "¿En qué año ocurrió la primera conexión exitosa?", "a": "1965", "b": "1969", "c": "1975", "d": "1983", "correcta": "B"},
            {"pregunta": "¿Quién inventó la World Wide Web?", "a": "Vint Cerf", "b": "Bill Gates", "c": "Tim Berners-Lee", "d": "Steve Jobs", "correcta": "C"},
            {"pregunta": "¿Qué permitió el protocolo TCP/IP?", "a": "Conectar diferentes redes", "b": "Crear el primer navegador", "c": "Enviar correos electrónicos", "d": "Comprimir datos", "correcta": "A"},
            {"pregunta": "¿Cuántas personas usan Internet hoy?", "a": "1.000 millones", "b": "3.000 millones", "c": "5.000 millones", "d": "8.000 millones", "correcta": "C"}
        ]
    },
    {
        "titulo": "El ciclo del agua",
        "contenido": "El ciclo del agua es el proceso continuo mediante el cual el agua se mueve a través de la Tierra y su atmósfera. Es esencial para la vida y mantiene el equilibrio de nuestros ecosistemas. El ciclo no tiene principio ni fin, pero podemos describirlo en varias etapas principales.\n\nLa evaporación es la primera etapa. El sol calienta el agua de océanos, lagos y ríos, convirtiéndola en vapor de agua que asciende a la atmósfera. La transpiración de las plantas también libera vapor de agua, un proceso conocido como evapotranspiración. Se estima que el 90% del vapor de agua en la atmósfera proviene de los océanos.\n\nLa condensación ocurre cuando el vapor de agua se enfría en la atmósfera y se convierte nuevamente en gotitas líquidas, formando nubes. Cuando estas gotitas se unen y crecen lo suficiente, caen por su propio peso en forma de precipitación: lluvia, nieve o granizo.\n\nLa precipitación devuelve el agua a la superficie terrestre. Parte de esta agua se infiltra en el suelo, recargando los acuíferos subterráneos. Otra parte escurre por la superficie hacia ríos y lagos, y eventualmente regresa al océano. El ciclo entonces comienza de nuevo.\n\nEl agua dulce disponible para el consumo humano representa solo el 2.5% de toda el agua del planeta, y la mayor parte está congelada en glaciares. Esto hace que la conservación del agua sea fundamental para nuestro futuro.",
        "categoria": "Ciencia Ambiental",
        "nivel": 1,
        "preguntas": [
            {"pregunta": "¿Qué porcentaje del vapor de agua atmosférico proviene de los océanos?", "a": "50%", "b": "70%", "c": "90%", "d": "99%", "correcta": "C"},
            {"pregunta": "¿Cómo se llama el proceso por el cual las plantas liberan vapor?", "a": "Evaporación", "b": "Condensación", "c": "Transpiración", "d": "Precipitación", "correcta": "C"},
            {"pregunta": "¿Qué ocurre durante la condensación?", "a": "El agua se convierte en vapor", "b": "El vapor se convierte en gotitas", "c": "El agua cae como lluvia", "d": "El agua se filtra en el suelo", "correcta": "B"},
            {"pregunta": "¿Qué porcentaje del agua del planeta es dulce?", "a": "2.5%", "b": "10%", "c": "25%", "d": "50%", "correcta": "A"},
            {"pregunta": "¿Qué etapa devuelve el agua a la superficie terrestre?", "a": "Evaporación", "b": "Condensación", "c": "Precipitación", "d": "Infiltración", "correcta": "C"}
        ]
    },
    {
        "titulo": "El Renacimiento: un nuevo amanecer",
        "contenido": "El Renacimiento fue un movimiento cultural y artístico que comenzó en Italia en el siglo XIV y se extendió por Europa hasta el siglo XVII. La palabra 'renacimiento' significa 'renacer', y el período se caracterizó por un renovado interés en el arte, la ciencia y la cultura de la antigua Grecia y Roma.\n\nUno de los aspectos más importantes del Renacimiento fue el humanismo, una filosofía que ponía al ser humano en el centro del universo. Los humanistas creían en el potencial de las personas para lograr grandes cosas a través de la educación y la razón. Esto contrastaba con la mentalidad medieval, que se centraba principalmente en Dios y la religión.\n\nLeonardo da Vinci (1452-1519) es quizás el ejemplo más famoso del 'hombre renacentista'. Fue pintor, escultor, arquitecto, científico, matemático e inventor. Sus obras más conocidas incluyen la Mona Lisa y La Última Cena. También diseñó máquinas voladoras y estudió la anatomía humana mediante disecciones.\n\nMiguel Ángel (1475-1564) fue otro gigante del Renacimiento. Esculpió el David y pintó la bóveda de la Capilla Sixtina en el Vaticano. Su trabajo mostraba un profundo conocimiento de la anatomía humana y una belleza idealizada.\n\nLa invención de la imprenta por Johannes Gutenberg alrededor de 1440 fue crucial para difundir las ideas renacentistas. Por primera vez, los libros podían producirse en masa, lo que permitió que el conocimiento llegara a más personas y aceleró el cambio cultural en toda Europa.",
        "categoria": "Arte e Historia",
        "nivel": 2,
        "preguntas": [
            {"pregunta": "¿En qué siglo comenzó el Renacimiento en Italia?", "a": "Siglo XII", "b": "Siglo XIV", "c": "Siglo XVI", "d": "Siglo XVIII", "correcta": "B"},
            {"pregunta": "¿Qué filosofía caracterizó al Renacimiento?", "a": "Estoicismo", "b": "Humanismo", "c": "Escolasticismo", "d": "Positivismo", "correcta": "B"},
            {"pregunta": "¿Qué obra famosa creó Leonardo da Vinci?", "a": "El David", "b": "La Capilla Sixtina", "c": "La Mona Lisa", "d": "El Nacimiento de Venus", "correcta": "C"},
            {"pregunta": "¿Qué invento difundió las ideas renacentistas?", "a": "El telescopio", "b": "La brújula", "c": "La imprenta", "d": "El reloj", "correcta": "C"},
            {"pregunta": "¿Quién pintó la Capilla Sixtina?", "a": "Leonardo da Vinci", "b": "Rafael", "c": "Donatello", "d": "Miguel Ángel", "correcta": "D"}
        ]
    },
    {
        "titulo": "El sistema solar",
        "contenido": "Nuestro sistema solar está formado por el Sol y todos los objetos celestes que orbitan a su alrededor. Se formó hace aproximadamente 4.600 millones de años a partir de una nube gigante de gas y polvo llamada nebulosa solar.\n\nEl Sol es una estrella de tamaño mediano que contiene el 99.8% de toda la masa del sistema solar. Su energía proviene de reacciones de fusión nuclear en su núcleo, donde el hidrógeno se convierte en helio a temperaturas de aproximadamente 15 millones de grados Celsius.\n\nLos planetas del sistema solar se dividen en dos grupos. Los planetas interiores o terrestres son Mercurio, Venus, Tierra y Marte. Son rocosos y relativamente pequeños. Los planetas exteriores o gigantes son Júpiter, Saturno, Urano y Neptuno. Son mucho más grandes y están compuestos principalmente de gas.\n\nJúpiter es el planeta más grande del sistema solar, con un diámetro 11 veces mayor que el de la Tierra. Su Gran Mancha Roja es una tormenta gigante que ha durado cientos de años. Saturno es famoso por sus impresionantes anillos, compuestos de hielo y roca.\n\nMarte ha sido objeto de gran interés científico porque muestra evidencia de que pudo haber tenido agua líquida en su superficie en el pasado. Los rovers como Perseverance están explorando el planeta en busca de señales de vida pasada. Plutón fue reclasificado como planeta enano en 2006 por la Unión Astronómica Internacional.",
        "categoria": "Astronomía",
        "nivel": 2,
        "preguntas": [
            {"pregunta": "¿Cuánta masa del sistema solar contiene el Sol?", "a": "50%", "b": "75%", "c": "99.8%", "d": "100%", "correcta": "C"},
            {"pregunta": "¿Cuáles son los planetas interiores?", "a": "Júpiter, Saturno, Urano, Neptuno", "b": "Mercurio, Venus, Tierra, Marte", "c": "Venus, Tierra, Marte, Júpiter", "d": "Mercurio, Tierra, Marte, Saturno", "correcta": "B"},
            {"pregunta": "¿Qué es la Gran Mancha Roja de Júpiter?", "a": "Un volcán", "b": "Un océano", "c": "Una tormenta gigante", "d": "Un cráter", "correcta": "C"},
            {"pregunta": "¿Por qué Plutón ya no es considerado un planeta?", "a": "Es demasiado pequeño", "b": "Fue reclasificado como planeta enano", "c": "Se desintegró", "d": "Salió del sistema solar", "correcta": "B"},
            {"pregunta": "¿Qué reacción genera la energía del Sol?", "a": "Fisión nuclear", "b": "Fusión nuclear", "c": "Combustión química", "d": "Energía geotérmica", "correcta": "B"}
        ]
    },
    {
        "titulo": "La fotosíntesis",
        "contenido": "La fotosíntesis es el proceso mediante el cual las plantas, algas y algunas bacterias convierten la energía de la luz solar en energía química. Es uno de los procesos más importantes para la vida en la Tierra, ya que produce el oxígeno que respiramos y es la base de la cadena alimenticia.\n\nEl proceso ocurre principalmente en las hojas de las plantas, dentro de orgánulos llamados cloroplastos. Estos contienen clorofila, el pigmento que da a las plantas su color verde y que captura la energía de la luz solar.\n\nLa fotosíntesis se puede resumir en una ecuación simple: dióxido de carbono (CO2) más agua (H2O), con la ayuda de la luz solar, produce glucosa (C6H12O6) y oxígeno (O2). En términos más simples, las plantas toman CO2 del aire y agua del suelo, y usando la energía del sol, producen su alimento y liberan oxígeno.\n\nLa fotosíntesis tiene dos fases principales. La fase luminosa depende de la luz solar y produce ATP y NADPH. La fase oscura o ciclo de Calvin no necesita luz directamente y utiliza el ATP y NADPH para convertir el CO2 en glucosa.\n\nSin la fotosíntesis, la atmósfera terrestre no tendría oxígeno y la vida como la conocemos no existiría. Además, este proceso ayuda a regular el clima al absorber grandes cantidades de CO2, uno de los principales gases de efecto invernadero.",
        "categoria": "Biología",
        "nivel": 2,
        "preguntas": [
            {"pregunta": "¿Dónde ocurre la fotosíntesis dentro de las células vegetales?", "a": "En las mitocondrias", "b": "En los cloroplastos", "c": "En el núcleo", "d": "En la membrana celular", "correcta": "B"},
            {"pregunta": "¿Qué pigmento captura la energía solar?", "a": "Melanina", "b": "Clorofila", "c": "Hemoglobina", "d": "Carotenoides", "correcta": "B"},
            {"pregunta": "¿Qué produce la fotosíntesis además de glucosa?", "a": "Dióxido de carbono", "b": "Nitrógeno", "c": "Oxígeno", "d": "Hidrógeno", "correcta": "C"},
            {"pregunta": "¿Qué fase de la fotosíntesis no necesita luz directamente?", "a": "Fase luminosa", "b": "Ciclo de Calvin", "c": "Fase de oxidación", "d": "Ciclo de Krebs", "correcta": "B"},
            {"pregunta": "¿De dónde toman las plantas el CO2?", "a": "Del suelo", "b": "Del agua", "c": "Del aire", "d": "De los fertilizantes", "correcta": "C"}
        ]
    }
]


def seed_database():
    existing = Lectura.query.filter_by(es_publica=True).count()
    if existing > 0:
        return False, f"Ya existen {existing} lecturas públicas. No se agregaron datos para evitar duplicados."

    count = 0
    for item in SEED_READINGS:
        lectura = Lectura(
            titulo=item["titulo"],
            contenido=item["contenido"],
            categoria=item["categoria"],
            nivel=item["nivel"],
            es_publica=True,
            activa=True,
            tiempo_estimado_minutos=10,
            puntos_recompensa=100,
            intentos_maximos=3,
        )
        db.session.add(lectura)
        db.session.flush()

        for pq in item["preguntas"]:
            pregunta = Pregunta(
                lectura_id=lectura.id,
                pregunta=pq["pregunta"],
                opcion_a=pq["a"],
                opcion_b=pq["b"],
                opcion_c=pq["c"],
                opcion_d=pq["d"],
                respuesta_correcta=pq["correcta"],
            )
            db.session.add(pregunta)

        count += 1

    db.session.commit()
    return True, f"Se crearon {count} lecturas públicas con sus quizzes."
