import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'deepread-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:password@localhost/deepread'
    SQLALCHEMY_TRACK_MODIFICATIONS = False