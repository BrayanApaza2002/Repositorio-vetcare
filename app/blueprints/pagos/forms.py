from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    DecimalField,
    SelectField,
    DateTimeLocalField,
    TextAreaField,
    SubmitField
)

from wtforms.fields.choices import SelectChoice

from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    Optional
)


class PagoForm(FlaskForm):

    concepto = StringField(
        "Concepto",
        validators=[
            DataRequired(message="El concepto es obligatorio."),
            Length(max=150)
        ]
    )

    monto = DecimalField(
        "Monto (Bs)",
        places=2,
        validators=[
            DataRequired(message="El monto es obligatorio."),
            NumberRange(
                min=0.01,
                message="El monto debe ser mayor que cero."
            )
        ]
    )

    metodo_pago = SelectField(
        "Método de pago",
        choices=[
            SelectChoice("", "Sin registrar"),
            SelectChoice("efectivo", "Efectivo"),
            SelectChoice("transferencia", "Transferencia"),
            SelectChoice("tarjeta", "Tarjeta")
        ],
        validators=[
            Optional()
        ]
    )

    fecha_pago = DateTimeLocalField(
        "Fecha y hora del pago",
        format="%Y-%m-%dT%H:%M",
        validators=[
            Optional()
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            SelectChoice("pendiente", "Pendiente"),
            SelectChoice("pagado", "Pagado"),
            SelectChoice("cancelado", "Cancelado")
        ],
        validators=[
            DataRequired(message="Selecciona el estado del pago.")
        ]
    )

    comprobante = StringField(
        "Número de comprobante",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    cliente_id = SelectField(
        "Cliente",
        coerce=int,
        validators=[
            DataRequired(message="Selecciona un cliente.")
        ]
    )

    cita_id = SelectField(
        "Cita asociada",
        coerce=int,
        validators=[
            Optional()
        ]
    )

    observaciones = TextAreaField(
        "Observaciones",
        validators=[
            Optional()
        ]
    )

    submit = SubmitField("Registrar pago")
