
from datetime import datetime
from decimal import Decimal

from app.extensions import db
from app.models import (
    Historial,
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


def crear_datos_historial():
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

    return mascota, veterinario


def datos_historial(mascota, veterinario, **cambios):
    datos = {
        "fecha_consulta": "2026-11-15T10:30",
        "mascota_id": str(mascota.id),
        "veterinario_id": str(veterinario.id),
        "sintomas": "Falta de apetito",
        "diagnostico": "Gastritis leve",
        "tratamiento": "Medicamento y dieta especial",
        "observaciones": "Control en una semana",
        "peso": "8.50",
        "temperatura": "38.50"
    }

    datos.update(cambios)
    return datos


def registrar_historial_prueba(mascota, veterinario):
    historial = Historial(
        fecha_consulta=datetime(2026, 11, 15, 10, 30),
        mascota_id=mascota.id,
        veterinario_id=veterinario.id,
        sintomas="Falta de apetito",
        diagnostico="Gastritis leve",
        tratamiento="Medicamento y dieta especial",
        observaciones="Control en una semana",
        peso=Decimal("8.50"),
        temperatura=Decimal("38.50")
    )

    db.session.add(historial)
    db.session.commit()

    return historial


def test_listado_historiales_carga(client, usuario_admin):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/historiales/")

    assert respuesta.status_code == 200


def test_formulario_nuevo_historial_carga(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    crear_datos_historial()

    respuesta = client.get("/historiales/nuevo")

    assert respuesta.status_code == 200


def test_registrar_historial_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_historial()

    respuesta = client.post(
        "/historiales/nuevo",
        data=datos_historial(mascota, veterinario),
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    historial = Historial.query.filter_by(
        diagnostico="Gastritis leve"
    ).first()

    assert historial is not None
    assert historial.mascota_id == mascota.id
    assert historial.veterinario_id == veterinario.id
    assert historial.sintomas == "Falta de apetito"
    assert historial.tratamiento == "Medicamento y dieta especial"


def test_rechazar_veterinario_inactivo(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_historial()

    veterinario.activo = False
    db.session.commit()

    respuesta = client.post(
        "/historiales/nuevo",
        data=datos_historial(mascota, veterinario),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Historial.query.count() == 0


def test_rechazar_sintomas_vacios(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_historial()

    respuesta = client.post(
        "/historiales/nuevo",
        data=datos_historial(
            mascota,
            veterinario,
            sintomas=""
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Historial.query.count() == 0


def test_rechazar_peso_fuera_de_rango(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_historial()

    respuesta = client.post(
        "/historiales/nuevo",
        data=datos_historial(
            mascota,
            veterinario,
            peso="-5"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Historial.query.count() == 0


def test_rechazar_temperatura_fuera_de_rango(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_historial()

    respuesta = client.post(
        "/historiales/nuevo",
        data=datos_historial(
            mascota,
            veterinario,
            temperatura="150"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Historial.query.count() == 0


def test_editar_historial_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_historial()

    historial = registrar_historial_prueba(
        mascota,
        veterinario
    )

    respuesta = client.post(
        f"/historiales/editar/{historial.id}",
        data=datos_historial(
            mascota,
            veterinario,
            diagnostico="Infección leve",
            tratamiento="Nuevo tratamiento",
            peso="9.20"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    historial_actualizado = db.session.get(
        Historial,
        historial.id
    )

    assert historial_actualizado.diagnostico == "Infección leve"
    assert historial_actualizado.tratamiento == "Nuevo tratamiento"
    assert float(historial_actualizado.peso) == 9.20


def test_editar_historial_inexistente(
    client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/historiales/editar/999")

    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/historiales/")


def test_eliminar_historial_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_historial()

    historial = registrar_historial_prueba(
        mascota,
        veterinario
    )

    respuesta = client.post(
        f"/historiales/eliminar/{historial.id}",
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert db.session.get(Historial, historial.id) is None


def test_recepcionista_no_puede_listar_historiales(
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

    respuesta = client.get("/historiales/")

    assert respuesta.status_code == 403
def test_veterinario_puede_listar_historiales(client, iniciar_sesion_rol):
    iniciar_sesion_rol("veterinario")

    respuesta = client.get("/historiales/")

    assert respuesta.status_code == 200

def test_cajero_no_puede_listar_historiales(client, iniciar_sesion_rol):
    iniciar_sesion_rol("cajero")

    respuesta = client.get("/historiales/")

    assert respuesta.status_code == 403