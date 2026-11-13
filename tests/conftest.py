
import pytest

from app import create_app
from app.extensions import db
from app.models import (
    Usuario,
    Cliente,
    Mascota,
    Veterinario,
    Cita,
    Historial,
    Vacuna,
    Pago
)


@pytest.fixture
def app():
    """Crea una aplicación independiente para las pruebas."""

    app = create_app()

    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI="sqlite://"
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Proporciona un cliente HTTP para realizar pruebas."""

    return app.test_client()


@pytest.fixture
def usuario_admin(app):
    """Crea un administrador de prueba."""

    usuario = Usuario(
        nombre="Administrador",
        apellido="Prueba",
        email="admin@test.com",
        rol="administrador",
        activo=True
    )

    usuario.establecer_password("Prueba123")

    db.session.add(usuario)
    db.session.commit()

    return usuario

@pytest.fixture
def iniciar_sesion_rol(app, client):
    """Crea un usuario de prueba con el rol indicado e inicia sesión."""

    def _iniciar(rol):
        email = f"{rol}@test.com"

        usuario = Usuario(
            nombre="Usuario",
            apellido="Prueba",
            email=email,
            rol=rol,
            activo=True
        )

        usuario.establecer_password("Prueba123")

        db.session.add(usuario)
        db.session.commit()

        return client.post(
            "/login",
            data={
                "email": email,
                "password": "Prueba123"
            },
            follow_redirects=True
        )

    return _iniciar