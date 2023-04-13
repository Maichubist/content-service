from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields

from db.post_db import PostDBModel


class PostSchema(SQLAlchemySchema):
    class Meta:
        model = PostDBModel
        load_instance = True

    user_id = fields.Integer(required=True)
    title = fields.String(required=True)
    text = fields.String(required=True)

