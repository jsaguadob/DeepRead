from flask_login import UserMixin
from datetime import datetime

db = None

def init_db(database):
    global db
    db = database

class Usuario:
    pass