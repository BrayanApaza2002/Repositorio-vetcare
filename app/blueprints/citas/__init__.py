from flask import Blueprint

bp = Blueprint(
    "citas",
    __name__,
    url_prefix="/citas"
)

from app.blueprints.citas import routes