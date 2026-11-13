
from app.extensions import db
from app.models import Cliente, Usuario


def iniciar_sesion_admin(client, usuario_admin):
    client.post(
        "/login",
        data={
            "email": "admin@test.com",
            "password": "Prueba123"
        },
        follow_redirects=True
    )


def test_listado_clientes_carga(client, usuario_admin):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/clientes/")

    assert respuesta.status_code == 200


def test_formulario_nuevo_cliente_carga(client, usuario_admin):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/clientes/nuevo")

    assert respuesta.status_code == 200


def test_registrar_cliente_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.post(
        "/clientes/nuevo",
        data={
            "nombre": "Carlos",
            "apellido": "Mamani",
            "ci": "12345678",
            "telefono": "70000000",
            "email": "carlos@test.com",
            "direccion": "La Paz"
        },
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    cliente = Cliente.query.filter_by(
        ci="12345678"
    ).first()

    assert cliente is not None
    assert cliente.nombre == "Carlos"


def test_rechazar_ci_duplicado(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    cliente = Cliente(
        nombre="Ana",
        apellido="Lopez",
        ci="11111111",
        telefono="71111111"
    )

    db.session.add(cliente)
    db.session.commit()

    respuesta = client.post(
        "/clientes/nuevo",
        data={
            "nombre": "Pedro",
            "apellido": "Rojas",
            "ci": "11111111",
            "telefono": "72222222",
            "email": "pedro@test.com",
            "direccion": "La Paz"
        },
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Cliente.query.filter_by(ci="11111111").count() == 1


def test_rechazar_email_duplicado(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    cliente = Cliente(
        nombre="Laura",
        apellido="Perez",
        ci="22222222",
        telefono="73333333",
        email="laura@test.com"
    )

    db.session.add(cliente)
    db.session.commit()

    respuesta = client.post(
        "/clientes/nuevo",
        data={
            "nombre": "Mario",
            "apellido": "Flores",
            "ci": "33333333",
            "telefono": "74444444",
            "email": "laura@test.com",
            "direccion": "El Alto"
        },
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Cliente.query.filter_by(email="laura@test.com").count() == 1


def test_recepcionista_puede_listar_clientes(
    app, client
):
    usuario = Usuario(
        nombre="Recepcionista",
        apellido="Prueba",
        email="recepcion@test.com",
        rol="recepcionista",
        activo=True
    )

    usuario.establecer_password("Prueba123")

    db.session.add(usuario)
    db.session.commit()

    client.post(
        "/login",
        data={
            "email": "recepcion@test.com",
            "password": "Prueba123"
        },
        follow_redirects=True
    )

    respuesta = client.get("/clientes/")

    assert respuesta.status_code == 200

def test_cajero_no_puede_listar_clientes(client, iniciar_sesion_rol):
    iniciar_sesion_rol("cajero")

    respuesta = client.get("/clientes/")

    assert respuesta.status_code == 403