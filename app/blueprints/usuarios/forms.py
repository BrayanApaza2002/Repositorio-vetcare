
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    PasswordField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)


CARGOS = [
    ("Administrador", "Administrador"),
    ("Veterinario", "Veterinario"),
    ("Secretaria", "Secretaria"),
    ("Recepcionista", "Recepcionista"),
    ("Cajero", "Cajero"),
    ("Auxiliar", "Auxiliar"),
    ("Otro", "Otro")
]

ROLES = [
    ("administrador", "Administrador"),
    ("veterinario", "Veterinario"),
    ("recepcionista", "Recepcionista"),
    ("cajero", "Cajero"),
    ("usuario", "Usuario")
]


class UsuarioForm(FlaskForm):
    """Formulario para registrar y editar usuarios."""

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
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingresa un correo válido."),
            Length(max=120)
        ]
    )

    cargo = SelectField(
        "Cargo",
        choices=CARGOS,
        validators=[
            DataRequired(message="Selecciona un cargo.")
        ]
    )

    rol = SelectField(
        "Rol del sistema",
        choices=ROLES,
        validators=[
            DataRequired(message="Selecciona un rol.")
        ]
    )

    activo = BooleanField("Usuario activo")

    submit = SubmitField("Guardar usuario")


class RegistrarUsuarioForm(UsuarioForm):
    """Formulario para registrar un usuario nuevo."""

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(
                min=8,
                max=72,
                message="La contraseña debe tener entre 8 y 72 caracteres."
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Confirma la contraseña."),
            EqualTo(
                "password",
                message="Las contraseñas no coinciden."
            )
        ]
    )

    submit = SubmitField("Registrar usuario")


class RestablecerPasswordForm(FlaskForm):
    """Formulario para cambiar la contraseña de un usuario."""

    password = PasswordField(
        "Nueva contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(
                min=8,
                max=72,
                message="La contraseña debe tener entre 8 y 72 caracteres."
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Confirma la contraseña."),
            EqualTo(
                "password",
                message="Las contraseñas no coinciden."
            )
        ]
    )

    submit = SubmitField("Restablecer contraseña")
