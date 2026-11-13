from app.extensions import db
from app.models import Mascota, Cliente, Usuario


def iniciar_sesion_admin(client, usuario_admin):
    client.post(
        "/login",
        data={
            "email": "admin@test.com",
            "password": "Prueba123"
        },
        follow_redirects=True
    )


def crear_cliente_prueba():
    cliente = Cliente(
        nombre="Carlos",
        apellido="Mamani",
        ci="12345678",
        telefono="70000000",
        email="carlos@test.com",
        direccion="La Paz",
        activo=True
    )

    db.session.add(cliente)
    db.session.commit()

    return cliente


def test_listado_mascotas_carga(client, usuario_admin):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/mascotas/")

    assert respuesta.status_code == 200


def test_formulario_nueva_mascota_carga(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    crear_cliente_prueba()

    respuesta = client.get("/mascotas/nuevo")

    assert respuesta.status_code == 200


def test_registrar_mascota_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente = crear_cliente_prueba()

    respuesta = client.post(
        "/mascotas/nuevo",
        data={
            "nombre": "Max",
            "especie": "perro",
            "raza": "Labrador",
            "sexo": "macho",
            "fecha_nacimiento": "2023-05-10",
            "color": "Dorado",
            "peso": "8.5",
            "observaciones": "Mascota de prueba",
            "cliente_id": str(cliente.id)
        },
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    mascota = Mascota.query.filter_by(nombre="Max").first()

    assert mascota is not None
    assert mascota.especie == "perro"
    assert mascota.sexo == "macho"
    assert mascota.peso == 8.5
    assert mascota.cliente_id == cliente.id


def test_rechazar_peso_negativo(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente = crear_cliente_prueba()

    respuesta = client.post(
        "/mascotas/nuevo",
        data={
            "nombre": "Rocky",
            "especie": "perro",
            "raza": "Pastor",
            "sexo": "macho",
            "fecha_nacimiento": "",
            "color": "Negro",
            "peso": "-5",
            "observaciones": "",
            "cliente_id": str(cliente.id)
        },
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Mascota.query.filter_by(nombre="Rocky").first() is None


def test_rechazar_especie_no_permitida(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente = crear_cliente_prueba()

    respuesta = client.post(
        "/mascotas/nuevo",
        data={
            "nombre": "Michi",
            "especie": "dinosaurio",
            "raza": "",
            "sexo": "macho",
            "fecha_nacimiento": "",
            "color": "",
            "peso": "",
            "observaciones": "",
            "cliente_id": str(cliente.id)
        },
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Mascota.query.filter_by(nombre="Michi").first() is None


def test_recepcionista_puede_listar_mascotas(app, client):
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

    respuesta = client.get("/mascotas/")

    assert respuesta.status_code == 200