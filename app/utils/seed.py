
from getpass import getpass

from app import create_app
from app.extensions import db
from app.models import Usuario


def crear_administrador():

    print("\n===== CREAR ADMINISTRADOR VETCARE =====\n")

    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    email = input("Correo electrónico: ").strip().lower()

    if not nombre or not apellido or not email:
        print("Error: todos los campos son obligatorios.")
        return

    if "@" not in email:
        print("Error: el correo electrónico no es válido.")
        return

    # Comprobar si el correo ya está registrado
    existente = Usuario.query.filter_by(email=email).first()

    if existente:
        print("Error: este correo ya está registrado.")
        return

    # Solicitar contraseña sin mostrarla
    password = getpass("Contraseña: ")
    confirmar = getpass("Confirmar contraseña: ")

    if len(password) < 8:
        print("Error: la contraseña debe tener al menos 8 caracteres.")
        return

    if password != confirmar:
        print("Error: las contraseñas no coinciden.")
        return

    # Crear administrador
    administrador = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        rol="administrador",
        activo=True
    )

    administrador.establecer_password(password)

    try:
        db.session.add(administrador)
        db.session.commit()

        print("\nAdministrador creado correctamente.")
        print("Correo:", administrador.email)
        print("Rol:", administrador.rol)

    except Exception as error:
        db.session.rollback()
        print("Error al crear el administrador:", error)


if __name__ == "__main__":

    app = create_app()

    with app.app_context():
        crear_administrador()
