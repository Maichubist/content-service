from datetime import datetime, timedelta

from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from db.post_db import PostDBModel
from db.db_config import redis_store

class PostResource(Resource):
    def post(self):
        user_id = redis_store.get(request.headers.get("Authorization").split()[1])
        if not user_id:
            return {"message": "Unauthorized"}, 401
        data = request.json


        db.session.add(PostDBModel(data.title, data.text, data.user_id))
        db.session.commit()
        return {'message': 'Post created successfully'}, 201


class PostListResource(Resource):
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
