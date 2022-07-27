from flask import Flask
from source.extensions import db, migrate
from flask_login import LoginManager, login_required, logout_user

login_manager = LoginManager()


def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    register_extensions(app)
    register_blueprints(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    # app.app_context().push()
    #
    # with app.app_context():
    #     db.create_all()


def register_blueprints(app):
    from source.user.views import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    from source.front.views import base_blueprint
    app.register_blueprint(base_blueprint)



