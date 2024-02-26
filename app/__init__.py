from flask import Flask
from flask_restx import Api
from app.view import view_bp
from app.api import api_ns
from flask_cors import CORS


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)

    app.register_blueprint(view_bp)

    api = Api(app, doc='/docs')

    api.add_namespace(api_ns)

    # if app.config['FLASK_ENV'] == 'prod':
    # app.config['SWAGGER_ENABLED'] = False

    return app
