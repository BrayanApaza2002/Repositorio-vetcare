
from flask_wtf import FlaskForm
from wtforms import (
    DateTimeLocalField,
    SelectField,
    TextAreaField,
    StringField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Optional
)


class CitaForm(FlaskForm):

    fecha_hora = DateTimeLocalField(
        "Fecha y hora de la cita",
        format="%Y-%m-%dT%H:%M",
        validators=[
            DataRequired(message="La fecha y hora son obligatorias.")
        ]
    )

    cliente_id = SelectField(
        "Propietario",
        coerce=int,
        validators=[
            DataRequired(message="Selecciona un propietario.")
        ]
    )

    mascota_id = SelectField(
        "Mascota",
        coerce=int,
        validators=[
            DataRequired(message="Selecciona una mascota.")
        ]
    )

    veterinario_id = SelectField(
        "Veterinario",
        coerce=int,
        validators=[
            DataRequired(message="Selecciona un veterinario.")
        ]
    )

    motivo = StringField(
        "Motivo de la consulta",
        validators=[
            DataRequired(message="El motivo es obligatorio."),
            Length(max=250)
        ]
    )

    observaciones = TextAreaField(
        "Observaciones",
        validators=[
            Optional()
        ]
    )

    submit = SubmitField("Registrar cita")
