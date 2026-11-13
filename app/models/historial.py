from app.extensions import db
from app.models.base import BaseModel


class Historial(BaseModel):
    """Modelo para almacenar el historial clínico de las mascotas."""

    __tablename__ = "historiales"

    fecha_consulta = db.Column(
        db.DateTime,
        nullable=False
    )

    sintomas = db.Column(
        db.Text,
        nullable=True
    )

    diagnostico = db.Column(
        db.Text,
        nullable=False
    )

    tratamiento = db.Column(
        db.Text,
        nullable=True
    )

    observaciones = db.Column(
        db.Text,
        nullable=True
    )

    peso = db.Column(
        db.Float,
        nullable=True
    )

    temperatura = db.Column(
        db.Float,
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

    def __repr__(self):
        return f"<Historial {self.id} - Mascota {self.mascota_id}>"