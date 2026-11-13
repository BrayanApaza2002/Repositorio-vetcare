
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional
)


class VeterinarioForm(FlaskForm):

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
            DataRequired(message="El correo es obligatorio."),
            Email(message="Introduce un correo electrónico válido."),
            Length(max=120)
        ]
    )

    especialidad = StringField(
        "Especialidad",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    matricula_profesional = StringField(
        "Matrícula profesional",
        validators=[
            DataRequired(message="La matrícula profesional es obligatoria."),
            Length(max=50)
        ]
    )

    submit = SubmitField("Guardar veterinario")
