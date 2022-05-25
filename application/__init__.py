import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_assets import Environment
from flask_migrate import Migrate
from blueprints import kfi
from .models.base import db, migrate, r

BLUEPRINTS = [kfi]

def init_app():
    """"Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    db.app = app
    r.init_app(app)
    migrate.init_app(app, db)

    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        # Include Routes
        from . import routes
        from .assets import compile_static_assets

        # Register Blueprints
        for blueprint in BLUEPRINTS:
            app.register_blueprint(blueprint)

        # Import Dash App
        from .dash.dashboard import init_dashboard

        app = init_dashboard(app)

        # Compile Static Assets
        compile_static_assets(assets)

        return app