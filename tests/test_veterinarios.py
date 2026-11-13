
from app.extensions import db
from app.models import Veterinario, Usuario


def iniciar_sesion_admin(client, usuario_admin):
    client.post(
        "/login",
        data={
            "email": "admin@test.com",
            "password": "Prueba123"
        },
        follow_redirects=True
    )


def datos_veterinario(**cambios):
    datos = {
        "nombre": "Carlos",
        "apellido": "Mamani",
        "ci": "45678901",
        "telefono": "70000001",
        "email": "carlos.vet@test.com",
        "especialidad": "Cirugía",
        "matricula_profesional": "VET-001"
    }

    datos.update(cambios)
    return datos


def test_listado_veterinarios_carga(client, usuario_admin):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/veterinarios/")

    assert respuesta.status_code == 200


def test_formulario_nuevo_veterinario_carga(
    client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.get("/veterinarios/nuevo")

    assert respuesta.status_code == 200


def test_registrar_veterinario_correctamente(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.post(
        "/veterinarios/nuevo",
        data=datos_veterinario(),
        follow_redirects=True
    )

    assert respuesta.status_code == 200

    veterinario = Veterinario.query.filter_by(
        ci="45678901"
    ).first()

    assert veterinario is not None
    assert veterinario.nombre == "Carlos"
    assert veterinario.email == "carlos.vet@test.com"
    assert veterinario.matricula_profesional == "VET-001"
    assert veterinario.activo is True


def test_rechazar_ci_duplicado(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    veterinario = Veterinario(**datos_veterinario())
    db.session.add(veterinario)
    db.session.commit()

    respuesta = client.post(
        "/veterinarios/nuevo",
        data=datos_veterinario(
            nombre="Pedro",
            email="pedro.vet@test.com",
            matricula_profesional="VET-002"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Veterinario.query.filter_by(
        ci="45678901"
    ).count() == 1


def test_rechazar_email_duplicado(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    veterinario = Veterinario(**datos_veterinario())
    db.session.add(veterinario)
    db.session.commit()

    respuesta = client.post(
        "/veterinarios/nuevo",
        data=datos_veterinario(
            ci="45678902",
            email="carlos.vet@test.com",
            matricula_profesional="VET-002"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Veterinario.query.filter_by(
        email="carlos.vet@test.com"
    ).count() == 1


def test_rechazar_matricula_duplicada(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    veterinario = Veterinario(**datos_veterinario())
    db.session.add(veterinario)
    db.session.commit()

    respuesta = client.post(
        "/veterinarios/nuevo",
        data=datos_veterinario(
            ci="45678902",
            email="pedro.vet@test.com",
            matricula_profesional="VET-001"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Veterinario.query.filter_by(
        matricula_profesional="VET-001"
    ).count() == 1


def test_rechazar_correo_invalido(
    app, client, usuario_admin
):
    iniciar_sesion_admin(client, usuario_admin)

    respuesta = client.post(
        "/veterinarios/nuevo",
        data=datos_veterinario(
            email="correo-invalido"
        ),
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert Veterinario.query.filter_by(
        ci="45678901"
    ).first() is None


def test_recepcionista_puede_listar_veterinarios(
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

    respuesta = client.get("/veterinarios/")

    assert respuesta.status_code == 200
