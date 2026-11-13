from flask import Blueprint

bp = Blueprint(
    "historiales",
    __name__,
    url_prefix="/historiales"
)

from app.blueprints.historiales import routes