import os

class Config:
    DEBUG = os.environ.get('DEBUG', False)
    SQLALCHEMY_DATABASE_URI = "postgresql://user:admin@localhost:5432/db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret-key'
    REDIS_URL = 'redis://localhost:6379/0'
    JWT_ACCESS_TOKEN_EXPIRES = 86400
