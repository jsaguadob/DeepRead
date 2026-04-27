# DeepRead - Aplicación de Lectura Crítica

## Descripción

DeepRead es una aplicación web educativa para mejorar habilidades de lectura crítica en estudiantes mediante lecturas adaptadas a diferentes niveles y quizzes interactivos.

## Requisitos Previos

- **Python 3.9+** (descargar de https://www.python.org/downloads/)
- **PostgreSQL** (se configurará en Neon)

## Instalación Local

### 1. Clonar el proyecto
```bash
git clone <tu-repo-url>
cd DeepRead
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar base de datos

#### Opción A: PostgreSQL local
1. Instalar PostgreSQL desde https://www.postgresql.org/download/
2. Crear una base de datos llamada `deepread`
3. Editar `.env` con tus credenciales

#### Opción B: PostgreSQL en Neon (recomendado)
1. Crear cuenta en https://neon.tech
2. Crear un nuevo proyecto
3. Copiar la URL de conexión en `.env`

### 6. Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en http://localhost:5000

## Deployment

### Render (Backend)

1. Crear cuenta en https://render.com
2. Conectar tu repositorio de GitHub
3. Crear un nuevo Web Service:
   - Name: `deepread-api`
   - Root Directory: `.`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Agregar variable de entorno:
   - `DATABASE_URL`: Tu URL de Neon

### Netlify (Frontend estático)

1. Crear cuenta en https://netlify.com
2. Arrastrar la carpeta `static` o conectar tu repositorio

## Estructura del Proyecto

```
DeepRead/
├── app.py                 # Aplicación Flask principal
├── config.py              # Configuración
├── requirements.txt       # Dependencias Python
├── .env                # Variables de entorno (no subirlas a git)
├── static/             # Archivos estáticos
│   ├── css/
│   └── js/
├── templates/           # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── lecturas.html
│   ├── lectura.html
│   ├── quiz.html
│   └── progreso.html
├── routes/            # Rutas de la aplicación
│   ├── auth.py
│   └── main.py
├── models/            # Modelos de base de datos
│   ├── user.py
│   ├── lectura.py
│   ├── progreso.py
│   └── quiz.py
├── utils/             # Utilidades
│   └── database.py
└── data/             # Datos iniciales
    └── seed_data.py
```

## Funcionalidades

- ✅ Sistema de usuarios (registro/login)
- ✅ Niveles de lectura (Básico, Intermedio, Avanzado)
- ✅ Sistema de puntos/XP
- ✅ Metas diarias
- ✅ Rastreo de progreso
- ✅ Quizzes de comprensión
- ✅ Diseño responsivo (móvil/escritorio)

## Tecnologías

- **Backend**: Flask (Python)
- **Base de datos**: PostgreSQL (Neon)
- **Frontend**: HTML + TailwindCSS
- **Deployment**: Render + Netlify