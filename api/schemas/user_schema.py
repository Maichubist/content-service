from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields, post_load

from werkzeug.security import generate_password_hash
from db.user_db import UserDBModel

#
class UserSchema(SQLAlchemySchema):
    class Meta:
        model = UserDBModel
        load_instance = True

    name = fields.String(required=True)
    phone_number = fields.String(required=True)
    login = fields.String(required=True)
    password = fields.String(load_only=True, required=True)

    @post_load
    def make_user(self, data, **kwargs):
        data.password = generate_password_hash(data.password)
        return data
