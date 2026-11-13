
from flask import render_template, redirect, url_for, flash, request
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.extensions import db
from app.blueprints.auth import bp
from app.blueprints.auth.forms import LoginForm, RegisterForm
from app.models import Usuario


@bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()

    if form.validate_on_submit():

        usuario = Usuario.query.filter_by(
            email=form.email.data.lower().strip()
        ).first()

        if usuario and usuario.activo and usuario.verificar_password(form.password.data):

            login_user(usuario)

            flash(
                "¡Bienvenido a VetCare!",
                "success"
            )

            next_page = request.args.get("next")

            if next_page and next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)

            return redirect(url_for("main.home"))

        flash(
            "Correo electrónico o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "auth/login.html",
        form=form
    )


@bp.route("/registro", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegisterForm()

    if form.validate_on_submit():

        email = form.email.data.lower().strip()

        usuario_existente = Usuario.query.filter_by(
            email=email
        ).first()

        if usuario_existente:
            flash(
                "Ya existe una cuenta registrada con ese correo electrónico.",
                "danger"
            )

            return render_template(
                "auth/register.html",
                form=form
            )

        nuevo_usuario = Usuario(
            nombre=form.nombre.data.strip(),
            apellido=form.apellido.data.strip(),
            email=email,
            rol="usuario",
            activo=True
        )

        nuevo_usuario.establecer_password(form.password.data)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash(
            "Tu cuenta se ha creado correctamente. Ya puedes iniciar sesión.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/register.html",
        form=form
    )


@bp.route("/logout", methods=["POST"])
@login_required
def logout():

    logout_user()

    flash(
        "Has cerrado sesión correctamente.",
        "success"
    )

    return redirect(url_for("auth.login"))
