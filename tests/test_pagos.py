
from datetime import datetime
from decimal import Decimal

from app.extensions import db
from app.models import (
    Pago,
    Cliente,
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


def crear_cliente_pago():
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


def datos_pago(cliente, **cambios):
    datos = {
        "concepto": "Consulta veterinaria",
        "monto": "150.00",
        "metodo_pago": "efectivo",
        "fecha_pago": "2026-11-02T10:30",
        "estado": "pagado",
        "comprobante": "COMP-001",
        "cliente_id": str(cliente.id),
        "cita_id": "0",
        "observaciones": "Pago por consulta general"
    }

    datos.update(cambios)
    return datos


def registrar_pago_prueba(cliente, **cambios):
    datos = {
        "concepto": "Consulta veterinaria",
        "monto": Decimal("150.00"),
        "metodo_pago": "efectivo",
        "fecha_pago": datetime(2026, 11, 2, 10, 30),
        "estado": "pagado",
        "comprobante": "COMP-001",
        "cliente_id": cliente.id,
        "cita_id": None,
        "observaciones": "Pago por consulta general"
    }

    datos.update(cambios)

    pago = Pago(**datos)

    db.session.add(pago)
    db.session.commit()

    return pago


def test_listado_pagos_carga(client, usuario_admin):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/pagos/")

    assert respuesta.status_code == 200


def test_formulario_nuevo_pago_carga(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    crear_cliente_pago()

    respuesta = client.get("/pagos/nuevo")

    assert respuesta.status_code == 200


def test_registrar_pago_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente = crear_cliente_pago()

    respuesta = client.post(
        "/pagos/nuevo",
        data=datos_pago(cliente),
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    pago = Pago.query.filter_by(
        comprobante="COMP-001"
    ).first()

    assert pago is not None
    assert pago.concepto == "Consulta veterinaria"
    assert pago.monto == Decimal("150.00")
    assert pago.metodo_pago == "efectivo"
    assert pago.estado == "pagado"
    assert pago.cliente_id == cliente.id
    assert pago.cita_id is None


def test_registrar_pago_sin_comprobante(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente = crear_cliente_pago()

    respuesta = client.post(
        "/pagos/nuevo",
        data=datos_pago(
            cliente,
            comprobante=""
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    pago = Pago.query.first()

    assert pago is not None
    assert pago.comprobante is None


def test_rechazar_monto_cero(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente = crear_cliente_pago()

    respuesta = client.post(
        "/pagos/nuevo",
        data=datos_pago(
            cliente,
            monto="0"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Pago.query.count() == 0


def test_rechazar_monto_negativo(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente = crear_cliente_pago()

    respuesta = client.post(
        "/pagos/nuevo",
        data=datos_pago(
            cliente,
            monto="-50"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Pago.query.count() == 0


def test_rechazar_concepto_vacio(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente = crear_cliente_pago()

    respuesta = client.post(
        "/pagos/nuevo",
        data=datos_pago(
            cliente,
            concepto=""
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Pago.query.count() == 0


def test_rechazar_comprobante_duplicado(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente = crear_cliente_pago()

    registrar_pago_prueba(cliente)

    respuesta = client.post(
        "/pagos/nuevo",
        data=datos_pago(
            cliente,
            concepto="Segunda consulta"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Pago.query.count() == 1


def test_editar_pago_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente = crear_cliente_pago()

    pago = registrar_pago_prueba(cliente)

    respuesta = client.post(
        f"/pagos/editar/{pago.id}",
        data=datos_pago(
            cliente,
            concepto="Consulta especializada",
            monto="250.00",
            metodo_pago="transferencia",
            estado="pendiente",
            comprobante="COMP-002"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    pago_actualizado = db.session.get(
        Pago,
        pago.id
    )

    assert pago_actualizado.concepto == "Consulta especializada"
    assert pago_actualizado.monto == Decimal("250.00")
    assert pago_actualizado.metodo_pago == "transferencia"
    assert pago_actualizado.estado == "pendiente"
    assert pago_actualizado.comprobante == "COMP-002"


def test_editar_pago_inexistente(
    client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/pagos/editar/999")

    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/pagos/")


def test_eliminar_pago_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    cliente = crear_cliente_pago()

    pago = registrar_pago_prueba(cliente)

    respuesta = client.post(
        f"/pagos/eliminar/{pago.id}",
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert db.session.get(Pago, pago.id) is None


def test_recepcionista_no_puede_listar_pagos(
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

    respuesta = client.get("/pagos/")

    assert respuesta.status_code == 403

def test_cajero_puede_listar_pagos(client, iniciar_sesion_rol):
    iniciar_sesion_rol("cajero")

    respuesta = client.get("/pagos/")

    assert respuesta.status_code == 200