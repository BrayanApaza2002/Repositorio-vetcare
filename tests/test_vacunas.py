from datetime import date

from app.extensions import db
from app.models import (
    Vacuna,
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


def crear_datos_vacuna():
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
    email="ana.flores@test.com",
    especialidad="Cirugía",
    matricula_profesional="VET-001",
    activo=True
)

    db.session.add_all([mascota, veterinario])
    db.session.commit()

    return mascota, veterinario


def datos_vacuna(mascota, veterinario, **cambios):
    datos = {
        "nombre": "Antirrábica",
        "precio": "150.00",
        "descripcion": "Vacuna contra la rabia",
        "fecha_aplicacion": "2026-11-02",
        "fecha_proxima": "2027-11-02",
        "lote": "LOT-2026-001",
        "mascota_id": str(mascota.id),
        "veterinario_id": str(veterinario.id),
        "observaciones": "Aplicación correcta"
    }

    datos.update(cambios)
    return datos


def registrar_vacuna_prueba(mascota, veterinario):
    vacuna = Vacuna(
        nombre="Antirrábica",
        descripcion="Vacuna contra la rabia",
        precio=150.00,
        fecha_aplicacion=date(2026, 11, 2),
        fecha_proxima=date(2027, 11, 2),
        lote="LOT-2026-001",
        mascota_id=mascota.id,
        veterinario_id=veterinario.id,
        observaciones="Aplicación correcta"
    )

    db.session.add(vacuna)
    db.session.commit()

    return vacuna


def test_listado_vacunas_carga(client, usuario_admin):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/vacunas/")

    assert respuesta.status_code == 200


def test_formulario_nueva_vacuna_carga(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    crear_datos_vacuna()

    respuesta = client.get("/vacunas/nuevo")

    assert respuesta.status_code == 200


def test_registrar_vacuna_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_vacuna()

    respuesta = client.post(
        "/vacunas/nuevo",
        data=datos_vacuna(mascota, veterinario),
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    vacuna = Vacuna.query.filter_by(
        nombre="Antirrábica"
    ).first()

    assert vacuna is not None
    assert float(vacuna.precio) == 150.00
    assert vacuna.mascota_id == mascota.id
    assert vacuna.veterinario_id == veterinario.id
    assert vacuna.fecha_aplicacion == date(2026, 11, 2)
    assert vacuna.fecha_proxima == date(2027, 11, 2)


def test_rechazar_veterinario_inactivo(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_vacuna()

    veterinario.activo = False
    db.session.commit()

    respuesta = client.post(
        "/vacunas/nuevo",
        data=datos_vacuna(mascota, veterinario),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Vacuna.query.count() == 0


def test_rechazar_fecha_proxima_anterior(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_vacuna()

    respuesta = client.post(
        "/vacunas/nuevo",
        data=datos_vacuna(
            mascota,
            veterinario,
            fecha_proxima="2026-10-01"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Vacuna.query.count() == 0


def test_rechazar_nombre_vacio(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_vacuna()

    respuesta = client.post(
        "/vacunas/nuevo",
        data=datos_vacuna(
            mascota,
            veterinario,
            nombre=""
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Vacuna.query.count() == 0


def test_rechazar_fecha_aplicacion_vacia(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_vacuna()

    respuesta = client.post(
        "/vacunas/nuevo",
        data=datos_vacuna(
            mascota,
            veterinario,
            fecha_aplicacion=""
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Vacuna.query.count() == 0


def test_editar_vacuna_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_vacuna()

    vacuna = registrar_vacuna_prueba(
        mascota,
        veterinario
    )

    respuesta = client.post(
        f"/vacunas/editar/{vacuna.id}",
        data=datos_vacuna(
            mascota,
            veterinario,
            nombre="Séxtuple",
            descripcion="Vacuna séxtuple canina",
            lote="LOT-2026-002"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    vacuna_actualizada = db.session.get(
        Vacuna,
        vacuna.id
    )

    assert vacuna_actualizada.nombre == "Séxtuple"
    assert vacuna_actualizada.descripcion == "Vacuna séxtuple canina"
    assert vacuna_actualizada.lote == "LOT-2026-002"


def test_editar_vacuna_inexistente(
    client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/vacunas/editar/999")

    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/vacunas/")


def test_eliminar_vacuna_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)
    mascota, veterinario = crear_datos_vacuna()

    vacuna = registrar_vacuna_prueba(
        mascota,
        veterinario
    )

    respuesta = client.post(
        f"/vacunas/eliminar/{vacuna.id}",
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert db.session.get(Vacuna, vacuna.id) is None


def test_recepcionista_no_puede_listar_vacunas(
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

    respuesta = client.get("/vacunas/")

    assert respuesta.status_code == 403


def test_veterinario_puede_listar_vacunas(
    client,
    iniciar_sesion_rol
):
    iniciar_sesion_rol("veterinario")

    respuesta = client.get("/vacunas/")

    assert respuesta.status_code == 200
