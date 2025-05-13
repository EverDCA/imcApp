import os

class Config:
    SECRET_KEY = '123'  # cámbiala por seguridad
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/clinica_imc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
