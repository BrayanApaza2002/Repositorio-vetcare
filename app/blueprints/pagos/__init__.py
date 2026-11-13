
from flask import Blueprint

bp = Blueprint(
    "pagos",
    __name__,
    url_prefix="/pagos"
)

from app.blueprints.pagos import routes
