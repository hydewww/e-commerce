from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_uploads import UploadSet, configure_uploads, IMAGES

bootstrap = Bootstrap()
db = SQLAlchemy()
images = UploadSet('images', IMAGES)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
# imag_name = {}


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    configure_uploads(app, images)

    from .public import public as public_blueprint
    app.register_blueprint(public_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .buy import buy as buy_blueprint
    app.register_blueprint(buy_blueprint, url_prefix='/my')

    from .sell import sell as sell_blueprint
    app.register_blueprint(sell_blueprint, url_prefix='/sell')

    return app
