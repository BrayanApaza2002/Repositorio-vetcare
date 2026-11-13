from app.extensions import db
from app.models.base import BaseModel


class Cliente(BaseModel):
    """Modelo para registrar los clientes de la veterinaria."""

    __tablename__ = "clientes"

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    apellido = db.Column(
        db.String(100),
        nullable=False
    )

    ci = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
    )

    telefono = db.Column(
        db.String(20),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=True
    )

    direccion = db.Column(
        db.String(200),
        nullable=True
    )

    activo = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    def __repr__(self):
        return f"<Cliente {self.nombre} {self.apellido}>"