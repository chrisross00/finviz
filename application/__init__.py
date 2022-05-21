from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_assets import Environment

db = SQLAlchemy()
r = FlaskRedis()

def init_app():
    """"Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    r.init_app(app)

    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        # Include Routes
        from . import routes
        from .assets import compile_static_assets

        # Register Blueprints
        # app.register_blueprint(auth.auth_bp)
        # app.register_blueprint(admin.admin_bp)

        # Import Dash App
        from .dash.dashboard import init_dashboard

        app = init_dashboard(app)

        # Compile Static Assets
        compile_static_assets(assets)

        return app