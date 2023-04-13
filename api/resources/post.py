from flask import request
from flask_restful import Resource

from db.post_db import PostDBModel
from db.db_config import redis_store, db
from api.auth import required_auth
from api.schemas.post_schema import PostSchema


class PostResource(Resource):

    def get(self, post_id: int):
        try:
            schema = PostSchema()
            post = PostDBModel.query.filter_by(id=post_id).first()
            if not post:
                return {"message": "post not found"}, 404
            return {'posts': schema.dump(post)}, 200
        except Exception as e:
            raise e
        
    @required_auth
    def put(self, post_id: int):
        try:
            user_id = redis_store.get(request.headers.get("Authorization"))
            if not user_id:
                return {"message": "Unauthorized"}, 401

            schema = PostSchema(partial=True)
            post = PostDBModel.query.filter_by(user_id=int(user_id), id=post_id).first()
            if not post:
                return {"message": "post not found"}, 404
            post = schema.load(request.json, instance=post)

            db.session.commit()
            return {"message": "post updated"}, 200
        except TypeError:
            return {"message": "user doesn`t have any post"}, 404
        except Exception as e:
            raise e

    @required_auth
    def delete(self, post_id: int):
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
            post = schema.load(data)

            db.session.add(post)
            db.session.commit()
            return {'message': 'Post created successfully'}, 201
        except TypeError:
            return {"message": "post not found"}, 404
        except Exception as a:
            raise a


    def get(self):
        user_id = request.args.get('user_id')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        ordering = request.args.get('ordering', default='asc')

        query = PostDBModel.query
        if user_id:
            query = query.filter_by(user_id=user_id)

        if ordering == 'asc':
            query = query.order_by(PostDBModel.created_at)
        elif ordering == 'desc':
            query = query.order_by(PostDBModel.created_at.desc())

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        schema = PostSchema(many=True)
        posts = query.all()

        return {'posts': schema.dump(posts)}, 200
