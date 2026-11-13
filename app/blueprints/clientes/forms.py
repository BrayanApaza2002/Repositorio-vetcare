
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class ClienteForm(FlaskForm):
    """Formulario para registrar y editar clientes."""

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(max=100)
        ]
    )

    apellido = StringField(
        "Apellido",
        validators=[
            DataRequired(message="El apellido es obligatorio."),
            Length(max=100)
        ]
    )

    ci = StringField(
        "Carnet de identidad",
        validators=[
            DataRequired(message="El CI es obligatorio."),
            Length(max=20)
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(max=20)
        ]
    )

    email = StringField(
        "Correo electrónico",
        validators=[
            Optional(),
            Email(message="Ingresa un correo válido."),
            Length(max=120)
        ]
    )

    direccion = StringField(
        "Dirección",
        validators=[
            Optional(),
            Length(max=200)
        ]
    )

    submit = SubmitField("Guardar cliente")
