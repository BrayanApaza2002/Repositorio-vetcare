
from app.extensions import db
from app.models import Usuario


def test_pagina_login_carga_correctamente(client):
    respuesta = client.get("/login")

    assert respuesta.status_code == 200
    assert b"login" in respuesta.data.lower()


def test_administrador_puede_iniciar_sesion(client, usuario_admin):
    respuesta = client.post(
        "/login",
        data={
            "email": "admin@test.com",
            "password": "Prueba123"
        },
        follow_redirects=True
    )

    assert respuesta.status_code == 200


def test_login_rechaza_contrasena_incorrecta(client, usuario_admin):
    respuesta = client.post(
        "/login",
        data={
            "email": "admin@test.com",
            "password": "Incorrecta123"
        },
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert b"incorrectos" in respuesta.data.lower()


def test_usuario_puede_cerrar_sesion(client, usuario_admin):
    with client:
        client.post(
            "/login",
            data={
                "email": "admin@test.com",
                "password": "Prueba123"
            },
            follow_redirects=True
        )

        respuesta = client.post(
            "/logout",
            follow_redirects=True
        )

        assert respuesta.status_code == 200
        assert b"login" in respuesta.data.lower()
