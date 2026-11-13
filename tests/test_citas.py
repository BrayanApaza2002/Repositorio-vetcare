
from datetime import datetime

from app.extensions import db
from app.models import (
    Cita,
    Cliente,
    Mascota,
    Veterinario,
    Usuario
)


def iniciar_sesion_admin(client, usuario_admin):
    client.post(
        "/login",
        data={
            "email": "admin@test.com",
            "password": "Prueba123"
        },
        follow_redirects=True
    )


def crear_datos_cita():
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
    db.session.flush()

    mascota = Mascota(
        nombre="Max",
        especie="perro",
        raza="Labrador",
        sexo="macho",
        peso=8.5,
        cliente_id=cliente.id
    )

    veterinario = Veterinario(
        nombre="Ana",
        apellido="Flores",
        ci="87654321",
        telefono="70000001",
        email="ana.vet@test.com",
        especialidad="Cirugía",
        matricula_profesional="VET-001",
        activo=True
    )

    db.session.add_all([mascota, veterinario])
    db.session.commit()

    return cliente, mascota, veterinario


def datos_cita(cliente, mascota, veterinario, **cambios):
    datos = {
        "fecha_hora": "2026-11-15T10:30",
        "cliente_id": str(cliente.id),
        "mascota_id": str(mascota.id),
        "veterinario_id": str(veterinario.id),
        "motivo": "Consulta general",
        "observaciones": "Primera consulta"
    }

    datos.update(cambios)
    return datos


def registrar_cita_prueba(cliente, mascota, veterinario):
    cita = Cita(
        fecha_hora=datetime(2026, 11, 15, 10, 30),
        cliente_id=cliente.id,
        mascota_id=mascota.id,
        veterinario_id=veterinario.id,
        motivo="Consulta general",
        observaciones="Primera consulta",
        estado="pendiente"
    )

    db.session.add(cita)
    db.session.commit()

    return cita


def test_listado_citas_carga(client, usuario_admin):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/citas/")

    assert respuesta.status_code == 200


def test_formulario_nueva_cita_carga(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    crear_datos_cita()

    respuesta = client.get("/citas/nuevo")

    assert respuesta.status_code == 200


def test_registrar_cita_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente, mascota, veterinario = crear_datos_cita()

    respuesta = client.post(
        "/citas/nuevo",
        data=datos_cita(cliente, mascota, veterinario),
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    cita = Cita.query.filter_by(
        motivo="Consulta general"
    ).first()

    assert cita is not None
    assert cita.estado == "pendiente"
    assert cita.cliente_id == cliente.id
    assert cita.mascota_id == mascota.id
    assert cita.veterinario_id == veterinario.id


def test_rechazar_mascota_de_otro_propietario(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    cliente, mascota, veterinario = crear_datos_cita()

    otro_cliente = Cliente(
        nombre="Pedro",
        apellido="Rojas",
        ci="22222222",
        telefono="70000002",
        email="pedro@test.com",
        activo=True
    )

    db.session.add(otro_cliente)
    db.session.commit()

    respuesta = client.post(
        "/citas/nuevo",
        data=datos_cita(
            otro_cliente,
            mascota,
            veterinario
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Cita.query.count() == 0


def test_rechazar_veterinario_inactivo(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    cliente, mascota, veterinario = crear_datos_cita()

    veterinario.activo = False
    db.session.commit()

    respuesta = client.post(
        "/citas/nuevo",
        data=datos_cita(cliente, mascota, veterinario),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Cita.query.count() == 0


def test_editar_cita_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    cliente, mascota, veterinario = crear_datos_cita()
    cita = registrar_cita_prueba(cliente, mascota, veterinario)

    respuesta = client.post(
        f"/citas/editar/{cita.id}",
        data=datos_cita(
            cliente,
            mascota,
            veterinario,
            fecha_hora="2026-11-20T15:00",
            motivo="Consulta de seguimiento"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    cita_actualizada = db.session.get(Cita, cita.id)

    assert cita_actualizada.motivo == "Consulta de seguimiento"
    assert cita_actualizada.fecha_hora == datetime(2026, 11, 20, 15, 0)


def test_editar_cita_inexistente(client, usuario_admin):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/citas/editar/999")

    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/citas/")


def test_eliminar_cita_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    cliente, mascota, veterinario = crear_datos_cita()
    cita = registrar_cita_prueba(cliente, mascota, veterinario)

    respuesta = client.post(
        f"/citas/eliminar/{cita.id}",
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert db.session.get(Cita, cita.id) is None


def test_cambiar_estado_cita_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    cliente, mascota, veterinario = crear_datos_cita()
    cita = registrar_cita_prueba(cliente, mascota, veterinario)

    respuesta = client.post(
        f"/citas/cambiar-estado/{cita.id}",
        data={"estado": "confirmada"},
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    cita_actualizada = db.session.get(Cita, cita.id)

    assert cita_actualizada.estado == "confirmada"


def test_rechazar_estado_no_valido(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    cliente, mascota, veterinario = crear_datos_cita()
    cita = registrar_cita_prueba(cliente, mascota, veterinario)

    respuesta = client.post(
        f"/citas/cambiar-estado/{cita.id}",
        data={"estado": "invalido"},
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    cita_actualizada = db.session.get(Cita, cita.id)

    assert cita_actualizada.estado == "pendiente"


def test_recepcionista_puede_listar_citas(app, client):
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

    respuesta = client.get("/citas/")

    assert respuesta.status_code == 200
def test_veterinario_puede_listar_citas(client, iniciar_sesion_rol):
    iniciar_sesion_rol("veterinario")

    respuesta = client.get("/citas/")

    assert respuesta.status_code == 200