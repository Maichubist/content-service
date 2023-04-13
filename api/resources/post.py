from datetime import datetime, timedelta

from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from db.post_db import PostDBModel
from db.db_config import redis_store, db
from api.auth import required_auth
from api.schemas.post_schema import PostSchema


class PostResource(Resource):

    @required_auth
    def put(self, post_id):
        try:
            user_id = redis_store.get(request.headers.get("Authorization"))
            if not user_id:
                return {"message": "Unauthorized"}, 401

            schema = PostSchema(partial=True)
            post = PostDBModel.query.filter_by(user_id=int(user_id), id=post_id).first()
            post = schema.load(request.json, instance=post, session=db.session)

            db.session.commit()
            return {"message": "post updated"}, 200
        except Exception as e:
            raise e

    @required_auth
    def delete(self, post_id):
        try:
            user_id = redis_store.get(request.headers.get("Authorization"))
            if not user_id:
                return {"message": "Unauthorized"}, 401
            post = PostDBModel.query.filter_by(user_id=int(user_id), id=post_id).first()
            if not post:
                return {"message": "post not found"}, 404
            db.session.delete(post)
            db.session.commit()
            return {"message": "post deleted"}, 200
        except Exception as e:
            raise e


class PostListResource(Resource):

    @required_auth
    def post(self):
        try:
            user_id = redis_store.get(request.headers.get("Authorization"))

            if not user_id:
                return {"message": "Unauthorized"}, 401
            data = request.json
            data["user_id"] = user_id
            schema = PostSchema()
            post = schema.load(data, session=db.session)

            db.session.add(post)
            db.session.commit()
            return {'message': 'Post created successfully'}, 201
        except Exception as a:
            raise a


    def get(self):
        data = request.json
        print(data)
        # parser = reqparse.RequestParser()
        # parser.add_argument('user_id', type=int)
        # parser.add_argument('limit', type=int, default=10)
        # parser.add_argument('offset', type=int, default=0)
        # parser.add_argument('ordering', choices=('asc', 'desc'), default='desc')
        # args = parser.parse_args()
        #
        # query = Post.query
        # if args.get('user_id'):
        #     query = query.filter_by(user_id=args['user_id'])
        # if args.get('ordering') == 'asc':
        #     query = query.order_by(Post.date.asc())
        # else:
        #     query = query.order_by(Post.date.desc())
        # posts = query.offset(args['offset']).limit(args['limit']).all()
        #
        # return {'posts': [post.serialize() for post in posts]}
