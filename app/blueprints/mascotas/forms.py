from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    DateField,
    FloatField,
    TextAreaField,
    SubmitField
)
from wtforms.fields.choices import SelectChoice
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    NumberRange
)


class MascotaForm(FlaskForm):
    """Formulario para registrar y editar mascotas."""

    nombre = StringField(
        "Nombre de la mascota",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(max=100)
        ]
    )

    especie = SelectField(
        "Especie",
        choices=[
            SelectChoice("perro", "Perro"),
            SelectChoice("gato", "Gato"),
            SelectChoice("ave", "Ave"),
            SelectChoice("conejo", "Conejo"),
            SelectChoice("otro", "Otro")
        ],
        validators=[
            DataRequired(message="Selecciona una especie.")
        ]
    )

    raza = StringField(
        "Raza",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    sexo = SelectField(
        "Sexo",
        choices=[
            SelectChoice("macho", "Macho"),
            SelectChoice("hembra", "Hembra")
        ],
        validators=[
            DataRequired(message="Selecciona el sexo.")
        ]
    )

    fecha_nacimiento = DateField(
        "Fecha de nacimiento",
        format="%Y-%m-%d",
        validators=[Optional()]
    )

    color = StringField(
        "Color",
        validators=[
            Optional(),
            Length(max=50)
        ]
    )

    peso = FloatField(
        "Peso (kg)",
        validators=[
            Optional(),
            NumberRange(
                min=0.01,
                max=1000,
                message="El peso debe ser mayor que cero."
            )
        ]
    )

    observaciones = TextAreaField(
        "Observaciones",
        validators=[Optional()]
    )

    cliente_id = SelectField(
        "Propietario",
        coerce=int,
        validators=[
            DataRequired(message="Selecciona un propietario.")
        ]
    )

    submit = SubmitField("Guardar mascota")