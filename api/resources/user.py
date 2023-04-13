from datetime import datetime, timedelta

from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from werkzeug.security import check_password_hash
import jwt

from db.user_db import UserDBModel
from db.db_config import db, redis_store
from api.schemas.user_schema import UserSchema
from config import Config
from api.auth import required_auth


class RegistrationResource(Resource):
    def post(self):
        try:
            schema = UserSchema()
            user = schema.load(request.json)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return {'message': 'User already exists'}, 409
        except Exception as e:
            raise e
        return {'message': 'User registered successfully'}, 201


class LoginResource(Resource):
    def post(self):
        try:

            auth = request.json
            user = UserDBModel.query.filter_by(login=auth.get("login")).first()
            if not user or not check_password_hash(user.password, auth.get("password")):
                return {"message": "Invalid credentials"}, 401
            token = jwt.encode(
                {
                    "user_id": user.id,
                    "exp": datetime.utcnow() + timedelta(days=1)
                },
                Config.JWT_SECRET_KEY,
                algorithm="HS256")
            redis_store.set(token, user.id, ex=86400)

            return {"token": token}, 200
        except Exception as e:
            raise e


class LogoutResource(Resource):
    @required_auth
    def post(self):
        try:
            token = request.headers.get("Authorization")
            if redis_store.exists(token):
                redis_store.delete(token)
                return {"message": "Logout successful"}, 200
            else:
                return {"message": "Token not found"}, 404
        except Exception as e:
            raise e
