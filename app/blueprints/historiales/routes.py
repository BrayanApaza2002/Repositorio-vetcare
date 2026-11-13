from flask import render_template, redirect, url_for, flash

from app.extensions import db
from app.models import Historial, Mascota, Veterinario
from app.blueprints.historiales import bp
from app.blueprints.historiales.forms import HistorialForm
from app.utils.decorators import roles_requeridos


@bp.route("/")
@roles_requeridos("administrador", "veterinario", "usuario")
def listar():

    historiales = Historial.query.order_by(
        Historial.fecha_consulta.desc()
    ).all()

    return render_template(
        "historiales/listar.html",
        historiales=historiales
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@roles_requeridos("administrador", "veterinario", "usuario")
def nuevo():

    form = HistorialForm()

    mascotas = Mascota.query.order_by(
        Mascota.nombre
    ).all()

    veterinarios = Veterinario.query.filter_by(
        activo=True
    ).order_by(Veterinario.nombre).all()

    form.mascota_id.choices = [
        (
            mascota.id,
            f"{mascota.nombre} - Propietario: "
            f"{mascota.cliente.nombre} {mascota.cliente.apellido}"
        )
        for mascota in mascotas
    ]

    form.veterinario_id.choices = [
        (
            veterinario.id,
            f"{veterinario.nombre} {veterinario.apellido}"
        )
        for veterinario in veterinarios
    ]

    if not mascotas or not veterinarios:
        flash(
            "Necesitas al menos una mascota y un veterinario activo para registrar un historial.",
            "warning"
        )
        return redirect(url_for("historiales.listar"))

    if form.validate_on_submit():

        veterinario = db.session.get(
            Veterinario,
            form.veterinario_id.data
        )

        if not veterinario or not veterinario.activo:
            flash(
                "El veterinario seleccionado no está disponible.",
                "warning"
            )
            return render_template(
                "historiales/nuevo.html",
                form=form
            )

        historial = Historial(
            fecha_consulta=form.fecha_consulta.data,
            mascota_id=form.mascota_id.data,
            veterinario_id=form.veterinario_id.data,
            sintomas=form.sintomas.data.strip(),
            diagnostico=form.diagnostico.data.strip(),
            tratamiento=form.tratamiento.data.strip(),
            observaciones=(
                form.observaciones.data.strip()
                if form.observaciones.data else None
            ),
            peso=form.peso.data,
            temperatura=form.temperatura.data
        )

        try:
            db.session.add(historial)
            db.session.commit()

            flash(
                "Historial clínico registrado correctamente.",
                "success"
            )

            return redirect(url_for("historiales.listar"))

        except Exception:
            db.session.rollback()

            flash(
                "Ocurrió un error al registrar el historial clínico.",
                "danger"
            )

    return render_template(
        "historiales/nuevo.html",
        form=form
    )

@bp.route("/editar/<int:id>", methods=["GET", "POST"])
@roles_requeridos("administrador", "veterinario", "usuario")
def editar(id):

    historial = db.session.get(Historial, id)

    if not historial:
        flash(
            "El historial clínico no existe.",
            "warning"
        )
        return redirect(url_for("historiales.listar"))

    form = HistorialForm()

    mascotas = Mascota.query.order_by(
        Mascota.nombre
    ).all()

    veterinarios = Veterinario.query.filter_by(
        activo=True
    ).order_by(Veterinario.nombre).all()

    form.mascota_id.choices = [
        (
            mascota.id,
            f"{mascota.nombre} - Propietario: "
            f"{mascota.cliente.nombre} {mascota.cliente.apellido}"
        )
        for mascota in mascotas
    ]

    form.veterinario_id.choices = [
        (
            veterinario.id,
            f"{veterinario.nombre} {veterinario.apellido}"
        )
        for veterinario in veterinarios
    ]

    if not mascotas or not veterinarios:
        flash(
            "Necesitas al menos una mascota y un veterinario activo.",
            "warning"
        )
        return redirect(url_for("historiales.listar"))

    if form.validate_on_submit():

        veterinario = db.session.get(
            Veterinario,
            form.veterinario_id.data
        )

        if not veterinario or not veterinario.activo:
            flash(
                "El veterinario seleccionado no está disponible.",
                "warning"
            )
            return render_template(
                "historiales/editar.html",
                form=form,
                historial=historial
            )

        historial.fecha_consulta = form.fecha_consulta.data
        historial.mascota_id = form.mascota_id.data
        historial.veterinario_id = form.veterinario_id.data
        historial.sintomas = form.sintomas.data.strip()
        historial.diagnostico = form.diagnostico.data.strip()
        historial.tratamiento = form.tratamiento.data.strip()

        historial.observaciones = (
            form.observaciones.data.strip()
            if form.observaciones.data else None
        )

        historial.peso = form.peso.data
        historial.temperatura = form.temperatura.data

        try:
            db.session.commit()

            flash(
                "Historial clínico actualizado correctamente.",
                "success"
            )

            return redirect(url_for("historiales.listar"))

        except Exception:
            db.session.rollback()

            flash(
                "Ocurrió un error al actualizar el historial clínico.",
                "danger"
            )

    elif not form.is_submitted():

        form.fecha_consulta.data = historial.fecha_consulta
        form.mascota_id.data = historial.mascota_id
        form.veterinario_id.data = historial.veterinario_id
        form.sintomas.data = historial.sintomas
        form.diagnostico.data = historial.diagnostico
        form.tratamiento.data = historial.tratamiento
        form.observaciones.data = historial.observaciones
        form.peso.data = historial.peso
        form.temperatura.data = historial.temperatura

    return render_template(
        "historiales/editar.html",
        form=form,
        historial=historial
    )

@bp.route("/eliminar/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "veterinario", "usuario")
def eliminar(id):

    historial = db.session.get(Historial, id)

    if not historial:
        flash(
            "El historial clínico no existe.",
            "warning"
        )
        return redirect(url_for("historiales.listar"))

    try:
        db.session.delete(historial)
        db.session.commit()

        flash(
            "Historial clínico eliminado correctamente.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "Ocurrió un error al eliminar el historial clínico.",
            "danger"
        )

    return redirect(url_for("historiales.listar"))