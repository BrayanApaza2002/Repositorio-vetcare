from app.extensions import db
from app.models.base import BaseModel


class Cita(BaseModel):
    """Modelo para gestionar las citas veterinarias."""

    __tablename__ = "citas"

    fecha_hora = db.Column(
        db.DateTime,
        nullable=False
    )

    motivo = db.Column(
        db.String(250),
        nullable=False
    )

    estado = db.Column(
        db.String(30),
        default="pendiente",
        nullable=False
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

    cliente = db.relationship("Cliente")
    mascota = db.relationship("Mascota")
    veterinario = db.relationship("Veterinario")

    def __repr__(self):
        return f"<Cita {self.id} - {self.fecha_hora}>"