from flask import Flask, Blueprint
from flask_restful import Api

from api.resources.post import (
    PostListResource,
    PostResource)
from api.resources.user import (
    RegistrationResource,
    LoginResource,
    LogoutResource)
from config import Config
from db.db_config import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    api.add_resource(RegistrationResource, '/registration')
    api.add_resource(LoginResource, '/login')
    api.add_resource(LogoutResource, '/logout')
    api.add_resource(PostListResource, '/posts')
    api.add_resource(PostResource, '/post/<int:post_id>')

    app.register_blueprint(api_bp)

    return app

app = create_app()
db = init_db(app)


if __name__ == '__main__':
    app.run(port=5000, debug=True)


