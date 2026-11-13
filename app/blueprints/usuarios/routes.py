
from flask import render_template, redirect, url_for, flash
from flask_login import current_user

from app.extensions import db
from app.blueprints.usuarios import bp
from app.blueprints.usuarios.forms import (
    UsuarioForm,
    RegistrarUsuarioForm,
    RestablecerPasswordForm
)
from app.models import Usuario
from app.utils.decorators import roles_requeridos


def es_ultimo_administrador_activo(usuario):
    """Comprueba si el usuario es el último administrador activo."""

    if usuario.rol != "administrador" or not usuario.activo:
        return False

    administradores_activos = Usuario.query.filter(
        Usuario.rol == "administrador",
        Usuario.activo.is_(True),
        Usuario.id != usuario.id
    ).count()

    return administradores_activos == 0


def es_ultimo_administrador_registrado(usuario):
    """Comprueba si es la última cuenta con rol administrador."""

    if usuario.rol != "administrador":
        return False

    administradores = Usuario.query.filter(
        Usuario.rol == "administrador",
        Usuario.id != usuario.id
    ).count()

    return administradores == 0


@bp.route("/")
@roles_requeridos("administrador")
def listar():

    usuarios = Usuario.query.order_by(
        Usuario.id.desc()
    ).all()

    return render_template(
        "usuarios/listar.html",
        usuarios=usuarios
    )


@bp.route("/registrar", methods=["GET", "POST"])
@roles_requeridos("administrador")
def registrar():

    form = RegistrarUsuarioForm()

    if not form.is_submitted():
        form.activo.data = True
        form.rol.data = "usuario"
        form.cargo.data = "Recepcionista"

    if form.validate_on_submit():

        email = form.email.data.lower().strip()

        existente = Usuario.query.filter_by(
            email=email
        ).first()

        if existente:
            flash(
                "Ya existe un usuario con ese correo electrónico.",
                "danger"
            )
            return render_template(
                "usuarios/registrar.html",
                form=form
            )

        usuario = Usuario(
            nombre=form.nombre.data.strip(),
            apellido=form.apellido.data.strip(),
            email=email,
            cargo=form.cargo.data,
            rol=form.rol.data,
            activo=form.activo.data
        )

        usuario.establecer_password(form.password.data)

        db.session.add(usuario)
        db.session.commit()

        flash(
            "El usuario se registró correctamente.",
            "success"
        )

        return redirect(url_for("usuarios.listar"))

    return render_template(
        "usuarios/registrar.html",
        form=form
    )


@bp.route("/editar/<int:usuario_id>", methods=["GET", "POST"])
@roles_requeridos("administrador")
def editar(usuario_id):

    usuario = Usuario.query.get_or_404(usuario_id)
    form = UsuarioForm(obj=usuario)

    if form.validate_on_submit():

        nuevo_email = form.email.data.lower().strip()

        existente = Usuario.query.filter(
            Usuario.email == nuevo_email,
            Usuario.id != usuario.id
        ).first()

        if existente:
            flash(
                "Ese correo electrónico ya pertenece a otro usuario.",
                "danger"
            )
            return render_template(
                "usuarios/editar.html",
                form=form,
                usuario=usuario
            )

        if usuario.id == current_user.id:
            if form.rol.data != "administrador" or not form.activo.data:
                flash(
                    "No puedes quitarte tus propios permisos de administrador ni desactivar tu cuenta.",
                    "danger"
                )
                return redirect(
                    url_for("usuarios.editar", usuario_id=usuario.id)
                )

        if (
            es_ultimo_administrador_activo(usuario)
            and (
                form.rol.data != "administrador"
                or not form.activo.data
            )
        ):
            flash(
                "No puedes quitar los permisos o desactivar al último administrador activo.",
                "danger"
            )
            return redirect(
                url_for("usuarios.editar", usuario_id=usuario.id)
            )

        usuario.nombre = form.nombre.data.strip()
        usuario.apellido = form.apellido.data.strip()
        usuario.email = nuevo_email
        usuario.cargo = form.cargo.data
        usuario.rol = form.rol.data
        usuario.activo = form.activo.data

        db.session.commit()

        flash(
            "Los datos del usuario se actualizaron correctamente.",
            "success"
        )

        return redirect(url_for("usuarios.listar"))

    return render_template(
        "usuarios/editar.html",
        form=form,
        usuario=usuario
    )


@bp.route("/estado/<int:usuario_id>", methods=["POST"])
@roles_requeridos("administrador")
def cambiar_estado(usuario_id):

    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.id == current_user.id:
        flash(
            "No puedes desactivar tu propia cuenta.",
            "danger"
        )
        return redirect(url_for("usuarios.listar"))

    if usuario.activo and es_ultimo_administrador_activo(usuario):
        flash(
            "No puedes desactivar al último administrador activo.",
            "danger"
        )
        return redirect(url_for("usuarios.listar"))

    usuario.activo = not usuario.activo
    db.session.commit()

    mensaje = (
        "activado" if usuario.activo else "desactivado"
    )

    flash(
        f"El usuario fue {mensaje} correctamente.",
        "success"
    )

    return redirect(url_for("usuarios.listar"))


@bp.route("/eliminar/<int:usuario_id>", methods=["POST"])
@roles_requeridos("administrador")
def eliminar(usuario_id):

    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.id == current_user.id:
        flash(
            "No puedes eliminar tu propia cuenta.",
            "danger"
        )
        return redirect(url_for("usuarios.listar"))

    if es_ultimo_administrador_registrado(usuario):
        flash(
            "No puedes eliminar la última cuenta de administrador.",
            "danger"
        )
        return redirect(url_for("usuarios.listar"))

    db.session.delete(usuario)
    db.session.commit()

    flash(
        "El usuario fue eliminado correctamente.",
        "success"
    )

    return redirect(url_for("usuarios.listar"))


@bp.route(
    "/restablecer-password/<int:usuario_id>",
    methods=["GET", "POST"]
)
@roles_requeridos("administrador")
def restablecer_password(usuario_id):

    usuario = Usuario.query.get_or_404(usuario_id)
    form = RestablecerPasswordForm()

    if form.validate_on_submit():

        usuario.establecer_password(form.password.data)

        db.session.commit()

        flash(
            "La contraseña del usuario se restableció correctamente.",
            "success"
        )

        return redirect(url_for("usuarios.listar"))

    return render_template(
        "usuarios/restablecer_password.html",
        form=form,
        usuario=usuario
    )
