from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redis import FlaskRedis

db = SQLAlchemy()
migrate = Migrate()
r = FlaskRedis()