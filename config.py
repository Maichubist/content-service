import os

class Config:
    DEBUG = os.environ.get('DEBUG', False)
    # SQLALCHEMY_DATABASE_URI = "postgresql://andrii.maichub:kam8elio2@localhost:5432/db"
    SQLALCHEMY_DATABASE_URI ='sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret-key'
    REDIS_URL = 'redis://localhost:6379/0'
    JWT_ACCESS_TOKEN_EXPIRES = 86400
