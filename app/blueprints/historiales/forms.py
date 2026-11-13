from flask_wtf import FlaskForm

from wtforms import (
    DateTimeLocalField,
    SelectField,
    StringField,
    TextAreaField,
    DecimalField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    NumberRange
)


class HistorialForm(FlaskForm):

    fecha_consulta = DateTimeLocalField(
        "Fecha y hora de consulta",
        format="%Y-%m-%dT%H:%M",
        validators=[
            DataRequired(message="La fecha de consulta es obligatoria.")
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

    sintomas = TextAreaField(
        "Síntomas",
        validators=[
            DataRequired(message="Los síntomas son obligatorios.")
        ]
    )

    diagnostico = TextAreaField(
        "Diagnóstico",
        validators=[
            DataRequired(message="El diagnóstico es obligatorio.")
        ]
    )

    tratamiento = TextAreaField(
        "Tratamiento",
        validators=[
            DataRequired(message="El tratamiento es obligatorio.")
        ]
    )

    observaciones = TextAreaField(
        "Observaciones",
        validators=[Optional()]
    )

    peso = DecimalField(
        "Peso (kg)",
        places=2,
        validators=[
            Optional(),
            NumberRange(min=0.01, max=1000)
        ]
    )

    temperatura = DecimalField(
        "Temperatura (°C)",
        places=2,
        validators=[
            Optional(),
            NumberRange(min=1, max=100)
        ]
    )

    submit = SubmitField("Registrar historial")