from flask import render_template, redirect, url_for, flash, request

from app.extensions import db
from app.models import Cita, Cliente, Mascota, Veterinario
from app.blueprints.citas import bp
from app.blueprints.citas.forms import CitaForm
from app.utils.decorators import roles_requeridos


@bp.route("/")
@roles_requeridos("administrador", "veterinario", "recepcionista", "usuario")
def listar():

    citas = Cita.query.order_by(
        Cita.fecha_hora.desc()
    ).all()

    return render_template(
        "citas/listar.html",
        citas=citas
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@roles_requeridos("administrador", "veterinario", "recepcionista", "usuario")
def nuevo():

    form = CitaForm()

    clientes = Cliente.query.filter_by(
        activo=True
    ).order_by(Cliente.nombre).all()

    mascotas = Mascota.query.join(Cliente).filter(
        Cliente.activo.is_(True)
    ).order_by(Mascota.nombre).all()

    veterinarios = Veterinario.query.filter_by(
        activo=True
    ).order_by(Veterinario.nombre).all()

    form.cliente_id.choices = [
        (cliente.id, f"{cliente.nombre} {cliente.apellido} - CI: {cliente.ci}")
        for cliente in clientes
    ]

    form.mascota_id.choices = [
        (mascota.id, f"{mascota.nombre} - Propietario: {mascota.cliente.nombre}")
        for mascota in mascotas
    ]

    form.veterinario_id.choices = [
        (veterinario.id, f"{veterinario.nombre} {veterinario.apellido}")
        for veterinario in veterinarios
    ]

    if not clientes or not mascotas or not veterinarios:
        flash(
            "Necesitas al menos un cliente, una mascota y un veterinario activo para registrar una cita.",
            "warning"
        )
        return redirect(url_for("citas.listar"))

    if form.validate_on_submit():

        mascota = db.session.get(Mascota, form.mascota_id.data)

        if not mascota or mascota.cliente_id != form.cliente_id.data:
            flash(
                "La mascota seleccionada no pertenece al propietario elegido.",
                "warning"
            )
            return render_template("citas/nuevo.html", form=form)

        veterinario = db.session.get(
            Veterinario,
            form.veterinario_id.data
        )

        if not veterinario or not veterinario.activo:
            flash(
                "El veterinario seleccionado no está disponible.",
                "warning"
            )
            return render_template("citas/nuevo.html", form=form)

        cita = Cita(
            fecha_hora=form.fecha_hora.data,
            cliente_id=form.cliente_id.data,
            mascota_id=form.mascota_id.data,
            veterinario_id=form.veterinario_id.data,
            motivo=form.motivo.data.strip(),
            observaciones=(
                form.observaciones.data.strip()
                if form.observaciones.data else None
            ),
            estado="pendiente"
        )

        try:
            db.session.add(cita)
            db.session.commit()

            flash("Cita registrada correctamente.", "success")
            return redirect(url_for("citas.listar"))

        except Exception:
            db.session.rollback()
            flash("Ocurrió un error al registrar la cita.", "danger")

    return render_template(
        "citas/nuevo.html",
        form=form
    )


@bp.route("/editar/<int:id>", methods=["GET", "POST"])
@roles_requeridos("administrador", "veterinario", "recepcionista", "usuario")
def editar(id):

    cita = db.session.get(Cita, id)

    if not cita:
        flash("La cita solicitada no existe.", "warning")
        return redirect(url_for("citas.listar"))

    form = CitaForm(obj=cita)

    clientes = Cliente.query.filter_by(
        activo=True
    ).order_by(Cliente.nombre).all()

    mascotas = Mascota.query.join(Cliente).filter(
        Cliente.activo.is_(True)
    ).order_by(Mascota.nombre).all()

    veterinarios = Veterinario.query.filter_by(
        activo=True
    ).order_by(Veterinario.nombre).all()

    form.cliente_id.choices = [
        (cliente.id, f"{cliente.nombre} {cliente.apellido} - CI: {cliente.ci}")
        for cliente in clientes
    ]

    form.mascota_id.choices = [
        (mascota.id, f"{mascota.nombre} - Propietario: {mascota.cliente.nombre}")
        for mascota in mascotas
    ]

    form.veterinario_id.choices = [
        (veterinario.id, f"{veterinario.nombre} {veterinario.apellido}")
        for veterinario in veterinarios
    ]

    if form.validate_on_submit():

        mascota = db.session.get(Mascota, form.mascota_id.data)

        if not mascota or mascota.cliente_id != form.cliente_id.data:
            flash(
                "La mascota seleccionada no pertenece al propietario elegido.",
                "warning"
            )
            return render_template(
                "citas/editar.html",
                form=form,
                cita=cita
            )

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
                "citas/editar.html",
                form=form,
                cita=cita
            )

        cita.fecha_hora = form.fecha_hora.data
        cita.cliente_id = form.cliente_id.data
        cita.mascota_id = form.mascota_id.data
        cita.veterinario_id = form.veterinario_id.data
        cita.motivo = form.motivo.data.strip()
        cita.observaciones = (
            form.observaciones.data.strip()
            if form.observaciones.data else None
        )

        try:
            db.session.commit()
            flash("Cita actualizada correctamente.", "success")
            return redirect(url_for("citas.listar"))

        except Exception:
            db.session.rollback()
            flash("Ocurrió un error al actualizar la cita.", "danger")

    return render_template(
        "citas/editar.html",
        form=form,
        cita=cita
    )


@bp.route("/eliminar/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "veterinario", "recepcionista", "usuario")
def eliminar(id):

    cita = db.session.get(Cita, id)

    if not cita:
        flash("La cita solicitada no existe.", "warning")
        return redirect(url_for("citas.listar"))

    try:
        db.session.delete(cita)
        db.session.commit()

        flash("Cita eliminada correctamente.", "success")

    except Exception:
        db.session.rollback()
        flash("No se pudo eliminar la cita.", "danger")

    return redirect(url_for("citas.listar"))

@bp.route("/cambiar-estado/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "veterinario", "recepcionista", "usuario")
def cambiar_estado(id):

    cita = db.session.get(Cita, id)

    if not cita:
        flash("La cita solicitada no existe.", "warning")
        return redirect(url_for("citas.listar"))

    estados_validos = [
        "pendiente",
        "confirmada",
        "completada",
        "cancelada"
    ]

    nuevo_estado = request.form.get("estado", "").strip().lower()

    if nuevo_estado not in estados_validos:
        flash("El estado seleccionado no es válido.", "warning")
        return redirect(url_for("citas.listar"))

    try:
        cita.estado = nuevo_estado
        db.session.commit()

        flash("Estado de la cita actualizado correctamente.", "success")

    except Exception:
        db.session.rollback()
        flash("No se pudo actualizar el estado de la cita.", "danger")

    return redirect(url_for("citas.listar"))
