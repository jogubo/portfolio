import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'portfolio.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # Blueprints
    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')
    app.jinja_env.globals.update(load_categories=main.load_categories)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import category
    app.register_blueprint(category.bp)

    return app
