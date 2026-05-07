# DeepRead v2.0

Plataforma de lectura crítica con quizzes, actividades y gestión de grupos.

## Stack

- **Backend:** Flask (Python) + SQLAlchemy + JWT + PostgreSQL/SQLite
- **Frontend:** React 18 + Vite + Tailwind CSS 4 + FontAwesome 6

## Desarrollo

### Requisitos
- Python 3.9+
- Node.js 20+

### Iniciar
Ejecuta `iniciar.bat` y selecciona la opción 1, o manualmente:

```bash
# Backend (ventana 1)
cd backend
pip install -r requirements.txt
python app.py

# Frontend (ventana 2)
cd frontend
npm install
npm run dev
```

- API: http://localhost:5000
- Frontend: http://localhost:5173

## Producción

```bash
cd frontend
npm run build
cd ../backend
gunicorn 'app:create_app()'
```

El frontend compilado en `frontend/dist/` se sirve desde Flask.
