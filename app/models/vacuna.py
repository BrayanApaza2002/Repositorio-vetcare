from app.extensions import db
from app.models.base import BaseModel


class Vacuna(BaseModel):
    """Modelo para gestionar las vacunas de las mascotas."""

    __tablename__ = "vacunas"

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=True
    )

    precio = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    fecha_aplicacion = db.Column(
        db.Date,
        nullable=False
    )

    fecha_proxima = db.Column(
        db.Date,
        nullable=True
    )

    lote = db.Column(
        db.String(50),
        nullable=True
    )

    observaciones = db.Column(
        db.Text,
        nullable=True
    )

    mascota_id = db.Column(
        db.Integer,
        db.ForeignKey("mascotas.id"),
        nullable=False
    )

    veterinario_id = db.Column(
        db.Integer,
        db.ForeignKey("veterinarios.id"),
        nullable=False
    )

    mascota = db.relationship("Mascota")
    veterinario = db.relationship("Veterinario")

    pago = db.relationship(
        "Pago",
        back_populates="vacuna",
        uselist=False
    )

    def __repr__(self):
        return f"<Vacuna {self.nombre} - Mascota {self.mascota_id}>"
