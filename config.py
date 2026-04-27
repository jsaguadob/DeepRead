import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'deepread-secret-key-2024'
    
    # Si hay DATABASE_URL (Render), usarla; si no, SQLite local
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///deepread.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
