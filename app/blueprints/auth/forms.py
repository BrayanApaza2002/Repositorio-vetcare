
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)


class LoginForm(FlaskForm):
    """Formulario para iniciar sesión en VetCare."""

    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo electrónico es obligatorio."),
            Email(message="Ingresa un correo electrónico válido."),
            Length(max=120)
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria.")
        ]
    )

    submit = SubmitField("Iniciar sesión")


class RegisterForm(FlaskForm):
    """Formulario para registrar nuevos usuarios."""

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

    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo electrónico es obligatorio."),
            Email(message="Ingresa un correo electrónico válido."),
            Length(max=120)
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(
                min=8,
                max=72,
                message="La contraseña debe tener al menos 8 caracteres."
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Debes confirmar tu contraseña."),
            EqualTo(
                "password",
                message="Las contraseñas no coinciden."
            )
        ]
    )

    submit = SubmitField("Registrarme")
