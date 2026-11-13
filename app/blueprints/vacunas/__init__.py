from flask import Blueprint

bp = Blueprint(
    "vacunas",
    __name__,
    url_prefix="/vacunas"
)

from app.blueprints.vacunas import routes