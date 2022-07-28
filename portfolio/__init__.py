import os

from flask import Flask

BASE_DIR = os.path.dirname(__file__)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER=UPLOAD_FOLDER
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from portfolio import database
    database.init_app(app)

    # Blueprints
    from portfolio.views import general
    from portfolio.views import auth
    from portfolio.views import admin
    app.register_blueprint(general.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)

    # Get categories in templates
    app.jinja_env.globals.update(get_categories=general.get_categories)

    return app
