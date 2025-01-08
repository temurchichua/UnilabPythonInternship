import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'grgrdhtbg343'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'test.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
