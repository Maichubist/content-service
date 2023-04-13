from flask_marshmallow import Marshmallow

from db.post_db import PostDBModel
from db.db_config import db

ma = Marshmallow()

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PostDBModel
        load_instance = True
        sqla_session = db.session

    user_id = ma.Integer(required=True)
    title = ma.String(required=True)
    text = ma.String(required=True)

