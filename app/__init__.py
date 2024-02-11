from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.auth.auth import auth_bp
    from app.views.home import home_bp
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(home_bp, url_prefix='/')

    return app