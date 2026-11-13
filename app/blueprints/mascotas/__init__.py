
from flask import Blueprint

bp = Blueprint("mascotas", __name__, url_prefix="/mascotas")

from app.blueprints.mascotas import routes
