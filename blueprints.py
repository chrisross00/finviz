from flask import Blueprint
from application.models.base import db
from application.models.KfiModel import Kfi

# appDb = Blueprint('db', __name__)
kfi = Blueprint('kfi', __name__)