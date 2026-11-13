from flask_wtf import FlaskForm

from wtforms import (
    DateField,
    DecimalField,
    SelectField,
    StringField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    Optional
)


class VacunaForm(FlaskForm):

    nombre = StringField(
        "Nombre de la vacuna",
        validators=[
            DataRequired(message="El nombre de la vacuna es obligatorio."),
            Length(max=100)
        ]
    )

    precio = DecimalField(
        "Precio de la vacuna (Bs)",
        places=2,
        validators=[
            DataRequired(message="El precio de la vacuna es obligatorio."),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor que cero."
            )
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            Optional()
        ]
    )

    fecha_aplicacion = DateField(
        "Fecha de aplicación",
        format="%Y-%m-%d",
        validators=[
            DataRequired(message="La fecha de aplicación es obligatoria.")
        ]
    )

    fecha_proxima = DateField(
        "Próxima aplicación",
        format="%Y-%m-%d",
        validators=[
            Optional()
        ]
    )

    lote = StringField(
        "Número de lote",
        validators=[
            Optional(),
            Length(max=50)
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

    observaciones = TextAreaField(
        "Observaciones",
        validators=[
            Optional()
        ]
    )

    submit = SubmitField("Registrar vacuna")
