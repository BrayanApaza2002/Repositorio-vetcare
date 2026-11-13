
from datetime import datetime, timezone

from app.extensions import db


def obtener_fecha_utc():
    """Obtiene la fecha y hora actual con zona horaria UTC."""
    return datetime.now(timezone.utc)


class BaseModel(db.Model):
    """Modelo base para los modelos del sistema."""

    __abstract__ = True

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=obtener_fecha_utc,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=obtener_fecha_utc,
        onupdate=obtener_fecha_utc,
        nullable=False
    )
