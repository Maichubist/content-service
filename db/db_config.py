from flask_sqlalchemy import SQLAlchemy
import redis

db = SQLAlchemy()

redis_store = redis.StrictRedis(host='localhost', port=6379, db=0)