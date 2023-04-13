from datetime import datetime, timedelta

from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


from db.user_db import UserDBModel
from db.db_config import db, redis_store
from config import Config



class RegistrationResource(Resource):
    def post(self):
        user = request.json
        db.session.add(UserDBModel(user.get("name"),
                                   user.get("phone_number"),
                                   user.get("login"),
                                   generate_password_hash(user.get("password")
                                                          )
                                   )
                       )
        db.session.commit()
        return {'message': 'User registered successfully'}, 201


class LoginResource(Resource):
    def post(self):
        print(request.json)
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


class LogoutResource(Resource):
    def post(self):
        token = request.headers.get("Autorization").split()[1]
        redis_store.delete(token)
        return {"message": "Logout successful"}, 200
