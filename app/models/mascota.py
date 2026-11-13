from app.extensions import db
from app.models.base import BaseModel


class Mascota(BaseModel):
    """Modelo para registrar las mascotas de la veterinaria."""

    __tablename__ = "mascotas"

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    especie = db.Column(
        db.String(50),
        nullable=False
    )

    raza = db.Column(
        db.String(100),
        nullable=True
    )

    sexo = db.Column(
        db.String(20),
        nullable=False
    )

    fecha_nacimiento = db.Column(
        db.Date,
        nullable=True
    )

    color = db.Column(
        db.String(50),
        nullable=True
    )

    peso = db.Column(
        db.Float,
        nullable=True
    )

    observaciones = db.Column(
        db.Text,
        nullable=True
    )

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=False
    )

    activo = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    cliente = db.relationship(
        "Cliente",
        backref=db.backref("mascotas", lazy=True)
    )

    def __repr__(self):
        return f"<Mascota {self.nombre}>"
