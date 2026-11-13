from flask import Blueprint

bp = Blueprint(
    "veterinarios",
    __name__,
    url_prefix="/veterinarios"
)

from app.blueprints.veterinarios import routes