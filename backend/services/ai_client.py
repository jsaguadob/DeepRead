import json
import re

modelo = None
cliente = None

def iniciar(api_key):
    global modelo, cliente
    if not api_key:
        print("[AI] GEMINI_API_KEY no configurada")
        return False
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        cliente = genai
        modelo = genai.GenerativeModel('models/gemini-2.5-flash-lite')
        print(f"[AI] Inicializado correctamente con modelo: models/gemini-2.5-flash-lite")
        return True
    except Exception as e:
        print(f"[AI] Error al iniciar: {e}")
        return False

def esta_listo():
    return modelo is not None

def _extraer_json(texto):
    texto = texto.strip()
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', texto)
    if match:
        texto = match.group(1)
    texto = texto.strip()
    if texto.startswith('[') or texto.startswith('{'):
        try:
            return json.loads(texto)
        except json.JSONDecodeError:
            pass
    try:
        inicio = texto.index('[')
        fin = texto.rindex(']') + 1
        return json.loads(texto[inicio:fin])
    except (ValueError, json.JSONDecodeError):
        return None

def generar_quiz(contenido, nivel, cantidad=5):
    if not modelo:
        return {'error': 'IA no configurada. El administrador debe configurar GEMINI_API_KEY.'}

    prompt = f"""Eres un profesor experto en comprensión lectora. Genera exactamente {cantidad} preguntas de opción múltiple para una lectura de nivel {nivel} (1=fácil, 2=medio, 3=avanzado).

REGLAS ESTRICTAS (violar estas reglas hará que el examen no sirva):
- Cada pregunta debe basarse ESTRICTAMENTE en el texto. NO inventes NADA.
- La respuesta correcta debe poder verificarse explícitamente en el texto proporcionado abajo.
- Las opciones incorrectas deben ser distracciones basadas en información del texto.
- NO uses palabras como "embarazo", "gato", "una vez" ni ningún concepto que NO esté en el texto.
- Si el texto es muy corto y no permite generar {cantidad} preguntas, genera solo las que puedas (mínimo 1).

Responde ÚNICAMENTE con un array JSON válido, sin texto adicional:
[
  {{
    "pregunta": "texto de la pregunta",
    "opcion_a": "texto opción a",
    "opcion_b": "texto opción b",
    "opcion_c": "texto opción c",
    "opcion_d": "texto opción d",
    "respuesta_correcta": "a",
    "explicacion": "explicación breve citando el texto"
  }}
]

Texto de la lectura:
{contenido}"""

    try:
        respuesta = modelo.generate_content(prompt)
        data = _extraer_json(respuesta.text)
        if data and isinstance(data, list):
            for p in data:
                if not all(k in p for k in ('pregunta', 'opcion_a', 'opcion_b', 'opcion_c', 'opcion_d', 'respuesta_correcta')):
                    return {'error': 'Formato inválido de la IA', 'raw': respuesta.text}
            return {'preguntas': data}
        return {'error': 'No se pudo interpretar la respuesta', 'raw': respuesta.text}
    except Exception as e:
        return {'error': f'Error al generar: {str(e)}'}

def chat_estadisticas(mensaje, contexto):
    if not modelo:
        return {'error': 'IA no configurada'}

    prompt = f"""Eres un asistente de análisis educativo. Tu tarea es ANALIZAR los datos de rendimiento de estudiantes y DETECTAR patrones de error.

REGLAS ESTRICTAS:
- SOLO usa los datos del contexto que se proporciona abajo.
- NUNCA inventes números, nombres o información que no esté en el contexto.
- Si te preguntan por un estudiante o lectura específica, busca esa información en el contexto y responde con los datos exactos que encuentres.
- Si el contexto incluye preguntas_falladas, analiza: ¿hay algún patrón? (ej. todas las preguntas falladas son de la misma lectura, o son sobre temas similares).
- Si no hay suficientes datos para identificar una causa, sé honesto pero sugiere qué datos adicionales ayudarían.
- Cuando sea apropiado, sugiere acciones concretas: "refuerza el tema X", "revisa la lectura Y".

Contexto actual del sistema:
{json.dumps(contexto, indent=2, ensure_ascii=False)}

Pregunta del usuario:
{mensaje}

Responde de forma clara, breve y útil en español."""

    try:
        respuesta = modelo.generate_content(prompt)
        return {'respuesta': respuesta.text}
    except Exception as e:
        return {'error': f'Error al consultar: {str(e)}'}

def resumir_texto(contenido):
    if not modelo:
        return {'error': 'IA no configurada'}
    try:
        respuesta = modelo.generate_content(
            f"Resume el siguiente texto en 3-5 oraciones claras:\n\n{contenido}"
        )
        return {'resumen': respuesta.text}
    except Exception as e:
        return {'error': f'Error al resumir: {str(e)}'}


def chat_estudiante(mensaje, titulo, contenido):
    if not modelo:
        return {'error': 'IA no configurada'}

    prompt = f"""Eres un asistente de lectura que ayuda a estudiantes a comprender un texto.

Título de la lectura: {titulo}
Contenido de la lectura:
{contenido[:3000]}

REGLAS ESTRICTAS:
- SOLO responde basándote en el texto proporcionado arriba.
- Si te preguntan algo que no está en el texto, responde: "Esa información no está en la lectura."
- No inventes ejemplos, datos o explicaciones que no aparezcan en el texto.
- Responde en español, de forma clara y breve (máximo 3 párrafos).

Pregunta del estudiante:
{mensaje}"""

    try:
        respuesta = modelo.generate_content(prompt)
        return {'respuesta': respuesta.text}
    except Exception as e:
        return {'error': f'Error al consultar: {str(e)}'}


def explicar_pregunta(pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, explicacion, contexto_lectura):
    if not modelo:
        return {'error': 'IA no configurada'}

    prompt = f"""Eres un tutor que explica preguntas de comprensión lectora.

Contexto de la lectura:
{contexto_lectura[:2000]}

Pregunta: {pregunta}
Opciones:
A) {opcion_a}
B) {opcion_b}
C) {opcion_c}
D) {opcion_d}
Respuesta correcta: {respuesta_correcta}
Explicación breve: {explicacion}

El estudiante falló esta pregunta. Tu tarea es EXPLICAR por qué la respuesta correcta es la indicada,
basándote en el texto de la lectura. Usa la explicación breve como guía pero amplíala.
Sé didáctico y claro. No agregues información que no esté en el texto o en la explicación.
Responde en español en 2-4 párrafos."""

    try:
        respuesta = modelo.generate_content(prompt)
        return {'respuesta': respuesta.text}
    except Exception as e:
        return {'error': f'Error al consultar: {str(e)}'}


def extraer_texto_archivo(ruta_archivo, extension):
    try:
        if extension == '.pdf':
            import fitz
            doc = fitz.open(ruta_archivo)
            texto = '\n'.join([page.get_text() for page in doc])
            doc.close()
            return texto.strip()
        elif extension == '.docx':
            from docx import Document
            doc = Document(ruta_archivo)
            texto = '\n'.join([p.text for p in doc.paragraphs])
            return texto.strip()
        elif extension == '.txt':
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return None
    except Exception as e:
        print(f"[AI] Error extrayendo texto: {e}")
        return None


def _vincular_texto_valido(texto):
    palabras = texto.split()
    if len(palabras) < 5:
        return False
    palabras_unicas = len(set(p.lower() for p in palabras if p.isalpha()))
    return palabras_unicas >= 4

def procesar_texto_con_ia(texto, cantidad_preguntas=5):
    if not modelo:
        return {'error': 'IA no configurada'}

    if not _vincular_texto_valido(texto):
        return {'error': 'El texto extraído no tiene suficiente contenido coherente'}

    texto_recortado = texto[:5000]
    prompt = f"""Eres un asistente que prepara material educativo a partir de texto extraído de un archivo.

Texto extraído:
{texto_recortado}

INSTRUCCIÓN CRÍTICA: Revisa el texto cuidadosamente. Si el texto no tiene sentido, parece basura, son palabras sueltas sin coherencia, o no es contenido educativo válido, responde ÚNICAMENTE con este JSON exacto:
{{"error": "texto_no_valido", "titulo_sugerido": "{texto[:50].strip()}", "contenido_limpio": "{texto[:5000]}", "nivel_sugerido": 1, "preguntas": []}}

SOLO si el texto es contenido educativo coherente y válido (artículo, ensayo, cuento, texto académico, etc.),
genera un JSON con la siguiente estructura exacta:
{{
  "titulo_sugerido": "título corto y descriptivo basado ESTRICTAMENTE en el texto",
  "contenido_limpio": "el texto limpiado (sin encabezados ni pies de página, conservando solo el contenido útil)",
  "nivel_sugerido": 2,
  "preguntas": [
    {{
      "pregunta": "texto de la pregunta basada ESTRICTAMENTE en el texto",
      "opcion_a": "texto opción a",
      "opcion_b": "texto opción b",
      "opcion_c": "texto opción c",
      "opcion_d": "texto opción d",
      "respuesta_correcta": "a",
      "explicacion": "explicación breve CITANDO el texto"
    }}
  ]
}}

REGLAS ESTRICTAS:
- NO inventes NADA. Cada pregunta y respuesta debe basarse ESTRICTAMENTE en el texto proporcionado.
- NO uses palabras, temas o conceptos que NO aparezcan en el texto.
- Si el texto no permite generar la cantidad solicitada, genera menos preguntas pero todas REALES.
- Las opciones incorrectas deben ser DISTRACCIONES basadas en información del texto.
- Responde ÚNICAMENTE con el JSON, sin texto adicional."""

    try:
        respuesta = modelo.generate_content(prompt)
        data = _extraer_json(respuesta.text)
        if data and isinstance(data, dict):
            if data.get('error') == 'texto_no_valido':
                return {'error': 'El texto no es contenido educativo válido'}
            if 'titulo_sugerido' in data:
                if 'contenido_limpio' not in data:
                    data['contenido_limpio'] = texto[:5000]
                if 'preguntas' not in data:
                    data['preguntas'] = []
                return data
        return {'error': 'No se pudo interpretar la respuesta', 'raw': respuesta.text}
    except Exception as e:
        return {'error': f'Error al procesar: {str(e)}'}
