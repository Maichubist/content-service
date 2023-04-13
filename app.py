from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from db.db_config import db
from api.resources.post import PostResource, PostListResource
from api.resources.user import RegistrationResource, LoginResource, LogoutResource
from config import Config



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES


api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(RegistrationResource, '/registration')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(PostListResource, '/posts')
api.add_resource(PostResource, '/post/<int:post_id>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)