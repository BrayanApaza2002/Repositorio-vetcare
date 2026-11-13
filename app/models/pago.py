from app.extensions import db
from app.models.base import BaseModel


class Pago(BaseModel):
    """Modelo para gestionar los pagos de la veterinaria."""

    __tablename__ = "pagos"

    concepto = db.Column(
        db.String(150),
        nullable=False
    )

    monto = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    metodo_pago = db.Column(
        db.String(30),
        nullable=True
    )

    fecha_pago = db.Column(
        db.DateTime,
        nullable=True
    )

    estado = db.Column(
        db.String(30),
        default="pendiente",
        nullable=False
    )

    comprobante = db.Column(
        db.String(100),
        unique=True,
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

    cita_id = db.Column(
        db.Integer,
        db.ForeignKey("citas.id"),
        nullable=True
    )

    vacuna_id = db.Column(
        db.Integer,
        db.ForeignKey("vacunas.id"),
        nullable=True,
        unique=True
    )

    cliente = db.relationship("Cliente")
    cita = db.relationship("Cita")

    vacuna = db.relationship(
        "Vacuna",
        back_populates="pago"
    )

    def __repr__(self):
        return f"<Pago {self.id} - {self.monto}>"
