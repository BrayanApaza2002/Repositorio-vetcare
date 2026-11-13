
from flask_login import UserMixin

from app.extensions import db, bcrypt
from app.models.base import BaseModel


class Usuario(UserMixin, BaseModel):
    """Modelo para gestionar los usuarios del sistema."""

    __tablename__ = "usuarios"

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    apellido = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    rol = db.Column(
        db.String(20),
        nullable=False,
        default="usuario"
    )

    cargo = db.Column(
        db.String(50),
        nullable=False,
        default="Recepcionista",
        server_default="Recepcionista"
    )

    activo = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    def establecer_password(self, password):
        """Genera el hash de la contraseña."""
        self.password_hash = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def verificar_password(self, password):
        """Comprueba si la contraseña es correcta."""
        return bcrypt.check_password_hash(
            self.password_hash,
            password
        )

    def __repr__(self):
        return f"<Usuario {self.email}>"
