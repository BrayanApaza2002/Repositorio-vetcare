
from flask import render_template, redirect, url_for, flash
from app.models import Veterinario
from app.models import Veterinario, Cita, Historial, Vacuna

from app.extensions import db
from app.models import Veterinario
from app.blueprints.veterinarios import bp
from app.blueprints.veterinarios.forms import VeterinarioForm
from app.utils.decorators import roles_requeridos


@bp.route("/")
@roles_requeridos("administrador", "recepcionista", "usuario")
def listar():
    veterinarios = Veterinario.query.order_by(
        Veterinario.created_at.desc()
    ).all()

    return render_template(
        "veterinarios/listar.html",
        veterinarios=veterinarios
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@roles_requeridos("administrador", "recepcionista", "usuario")
def nuevo():
    form = VeterinarioForm()

    if form.validate_on_submit():

        ci = form.ci.data.strip()
        email = form.email.data.strip().lower()
        matricula = form.matricula_profesional.data.strip()

        veterinario_existente = Veterinario.query.filter(
            (Veterinario.ci == ci) |
            (Veterinario.email == email) |
            (Veterinario.matricula_profesional == matricula)
        ).first()

        if veterinario_existente:
            flash(
                "El CI, correo o matrícula profesional ya está registrado.",
                "warning"
            )
            return render_template(
                "veterinarios/nuevo.html",
                form=form
            )

        veterinario = Veterinario(
            nombre=form.nombre.data.strip(),
            apellido=form.apellido.data.strip(),
            ci=ci,
            telefono=form.telefono.data.strip(),
            email=email,
            especialidad=(
                form.especialidad.data.strip()
                if form.especialidad.data else None
            ),
            matricula_profesional=matricula,
            activo=True
        )

        try:
            db.session.add(veterinario)
            db.session.commit()

            flash(
                "Veterinario registrado correctamente.",
                "success"
            )

            return redirect(url_for("veterinarios.listar"))

        except Exception:
            db.session.rollback()
            flash(
                "Ocurrió un error al registrar el veterinario.",
                "danger"
            )

    return render_template(
        "veterinarios/nuevo.html",
        form=form
    )

@bp.route("/editar/<int:id>", methods=["GET", "POST"])
@roles_requeridos("administrador", "recepcionista", "usuario")
def editar(id):

    veterinario = Veterinario.query.get_or_404(id)

    form = VeterinarioForm(obj=veterinario)

    if form.validate_on_submit():

        ci = form.ci.data.strip()
        email = form.email.data.strip().lower()
        matricula = form.matricula_profesional.data.strip()

        veterinario_existente = Veterinario.query.filter(
            Veterinario.id != id,
            (
                (Veterinario.ci == ci) |
                (Veterinario.email == email) |
                (Veterinario.matricula_profesional == matricula)
            )
        ).first()

        if veterinario_existente:
            flash(
                "El CI, correo o matrícula profesional ya está registrado.",
                "warning"
            )

            return render_template(
                "veterinarios/editar.html",
                form=form,
                veterinario=veterinario
            )

        veterinario.nombre = form.nombre.data.strip()
        veterinario.apellido = form.apellido.data.strip()
        veterinario.ci = ci
        veterinario.telefono = form.telefono.data.strip()
        veterinario.email = email
        veterinario.especialidad = (
            form.especialidad.data.strip()
            if form.especialidad.data else None
        )
        veterinario.matricula_profesional = matricula

        try:
            db.session.commit()

            flash(
                "Veterinario modificado correctamente.",
                "success"
            )

            return redirect(url_for("veterinarios.listar"))

        except Exception:
            db.session.rollback()

            flash(
                "Ocurrió un error al modificar el veterinario.",
                "danger"
            )

    return render_template(
        "veterinarios/editar.html",
        form=form,
        veterinario=veterinario
    )

@bp.route("/eliminar/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "recepcionista", "usuario")
def eliminar(id):

    veterinario = Veterinario.query.get_or_404(id)

    try:
        veterinario.activo = False
        db.session.commit()

        flash(
            "Veterinario desactivado correctamente.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "Ocurrió un error al desactivar el veterinario.",
            "danger"
        )

    return redirect(url_for("veterinarios.listar"))

@bp.route("/activar/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "recepcionista", "usuario")
def activar(id):

    veterinario = Veterinario.query.get_or_404(id)

    try:
        veterinario.activo = True
        db.session.commit()

        flash(
            "Veterinario activado correctamente.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "Ocurrió un error al activar el veterinario.",
            "danger"
        )

    return redirect(url_for("veterinarios.listar"))


@bp.route("/eliminar-definitivamente/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "recepcionista", "usuario")
def eliminar_definitivamente(id):

    veterinario = Veterinario.query.get_or_404(id)

    # Comprobar citas asociadas.
    if Cita.query.filter_by(veterinario_id=id).first():
        flash(
            "No se puede eliminar: el veterinario tiene citas registradas.",
            "warning"
        )
        return redirect(url_for("veterinarios.listar"))

    # Comprobar historiales clínicos.
    if Historial.query.filter_by(veterinario_id=id).first():
        flash(
            "No se puede eliminar: el veterinario tiene historiales clínicos.",
            "warning"
        )
        return redirect(url_for("veterinarios.listar"))

    # Comprobar vacunas asociadas.
    if Vacuna.query.filter_by(veterinario_id=id).first():
        flash(
            "No se puede eliminar: el veterinario tiene vacunas registradas.",
            "warning"
        )
        return redirect(url_for("veterinarios.listar"))

    try:
        db.session.delete(veterinario)
        db.session.commit()

        flash(
            "Veterinario eliminado definitivamente.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "No se pudo eliminar el veterinario. Comprueba sus registros relacionados.",
            "danger"
        )

    return redirect(url_for("veterinarios.listar"))
