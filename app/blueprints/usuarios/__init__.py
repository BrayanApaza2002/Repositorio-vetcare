from flask import Blueprint

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

from app.blueprints.usuarios import routes