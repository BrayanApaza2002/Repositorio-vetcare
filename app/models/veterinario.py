from app.extensions import db
from app.models.base import BaseModel


class Veterinario(BaseModel):
    """Modelo para registrar los veterinarios."""

    __tablename__ = "veterinarios"

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
        nullable=False
    )

    telefono = db.Column(
        db.String(20),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    especialidad = db.Column(
        db.String(100),
        nullable=True
    )

    matricula_profesional = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    activo = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    def __repr__(self):
        return f"<Veterinario {self.nombre} {self.apellido}>"