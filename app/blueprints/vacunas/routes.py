from flask import render_template, redirect, url_for, flash

from app.extensions import db
from app.models import Vacuna, Mascota, Veterinario, Pago
from app.blueprints.vacunas import bp
from app.blueprints.vacunas.forms import VacunaForm
from app.utils.decorators import roles_requeridos


@bp.route("/")
@roles_requeridos("administrador", "veterinario", "usuario")
def listar():

    vacunas = Vacuna.query.order_by(
        Vacuna.fecha_aplicacion.desc()
    ).all()

    return render_template(
        "vacunas/listar.html",
        vacunas=vacunas
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@roles_requeridos("administrador", "veterinario", "usuario")
def nuevo():

    form = VacunaForm()

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
            "Necesitas al menos una mascota y un veterinario activo para registrar una vacuna.",
            "warning"
        )
        return redirect(url_for("vacunas.listar"))

    if form.validate_on_submit():

        veterinario = db.session.get(
            Veterinario,
            form.veterinario_id.data
        )

        mascota = db.session.get(
            Mascota,
            form.mascota_id.data
        )

        if not veterinario or not veterinario.activo:
            flash(
                "El veterinario seleccionado no está disponible.",
                "warning"
            )
            return render_template(
                "vacunas/nuevo.html",
                form=form
            )

        if not mascota:
            flash(
                "La mascota seleccionada no existe.",
                "warning"
            )
            return render_template(
                "vacunas/nuevo.html",
                form=form
            )

        if (
            form.fecha_proxima.data
            and form.fecha_proxima.data < form.fecha_aplicacion.data
        ):
            flash(
                "La próxima aplicación no puede ser anterior a la fecha de aplicación.",
                "warning"
            )
            return render_template(
                "vacunas/nuevo.html",
                form=form
            )

        vacuna = Vacuna(
            nombre=form.nombre.data.strip(),
            descripcion=(
                form.descripcion.data.strip()
                if form.descripcion.data else None
            ),
            precio=form.precio.data,
            fecha_aplicacion=form.fecha_aplicacion.data,
            fecha_proxima=form.fecha_proxima.data,
            lote=form.lote.data.strip() if form.lote.data else None,
            mascota_id=mascota.id,
            veterinario_id=veterinario.id,
            observaciones=(
                form.observaciones.data.strip()
                if form.observaciones.data else None
            )
        )

        try:
            db.session.add(vacuna)
            db.session.flush()

            pago = Pago(
                concepto=(
                    f"Vacuna: {vacuna.nombre} - "
                    f"Mascota: {mascota.nombre}"
                ),
                monto=vacuna.precio,
                estado="pendiente",
                metodo_pago=None,
                fecha_pago=None,
                cliente_id=mascota.cliente_id,
                vacuna_id=vacuna.id,
                observaciones="Pago generado automáticamente al registrar la vacuna."
            )

            db.session.add(pago)
            db.session.commit()

            flash(
                "Vacuna registrada y pago pendiente generado correctamente.",
                "success"
            )

            return redirect(url_for("vacunas.listar"))

        except Exception:
            db.session.rollback()

            flash(
                "Ocurrió un error al registrar la vacuna y generar su pago.",
                "danger"
            )

    return render_template(
        "vacunas/nuevo.html",
        form=form
    )


@bp.route("/editar/<int:id>", methods=["GET", "POST"])
@roles_requeridos("administrador", "veterinario", "usuario")
def editar(id):

    vacuna = db.session.get(Vacuna, id)

    if not vacuna:
        flash(
            "El registro de vacunación no existe.",
            "warning"
        )
        return redirect(url_for("vacunas.listar"))

    form = VacunaForm()

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
        return redirect(url_for("vacunas.listar"))

    if form.validate_on_submit():

        veterinario = db.session.get(
            Veterinario,
            form.veterinario_id.data
        )

        mascota = db.session.get(
            Mascota,
            form.mascota_id.data
        )

        if not veterinario or not veterinario.activo:
            flash(
                "El veterinario seleccionado no está disponible.",
                "warning"
            )
            return render_template(
                "vacunas/editar.html",
                form=form,
                vacuna=vacuna
            )

        if not mascota:
            flash(
                "La mascota seleccionada no existe.",
                "warning"
            )
            return render_template(
                "vacunas/editar.html",
                form=form,
                vacuna=vacuna
            )

        if vacuna.pago and mascota.id != vacuna.mascota_id:
            flash(
                "No puedes cambiar la mascota de esta vacuna porque ya tiene "
                "un pago asociado. Esto protege el historial del propietario.",
                "warning"
            )
            return render_template(
                "vacunas/editar.html",
                form=form,
                vacuna=vacuna
            )

        if (
            form.fecha_proxima.data
            and form.fecha_proxima.data < form.fecha_aplicacion.data
        ):
            flash(
                "La próxima aplicación no puede ser anterior a la fecha de aplicación.",
                "warning"
            )
            return render_template(
                "vacunas/editar.html",
                form=form,
                vacuna=vacuna
            )

        vacuna.nombre = form.nombre.data.strip()
        vacuna.descripcion = (
            form.descripcion.data.strip()
            if form.descripcion.data else None
        )
        vacuna.precio = form.precio.data
        vacuna.fecha_aplicacion = form.fecha_aplicacion.data
        vacuna.fecha_proxima = form.fecha_proxima.data
        vacuna.lote = (
            form.lote.data.strip()
            if form.lote.data else None
        )
        vacuna.mascota_id = mascota.id
        vacuna.veterinario_id = veterinario.id
        vacuna.observaciones = (
            form.observaciones.data.strip()
            if form.observaciones.data else None
        )

        try:
            db.session.commit()

            flash(
                "Registro de vacunación actualizado correctamente. "
                "El importe de los pagos existentes no fue modificado.",
                "success"
            )

            return redirect(url_for("vacunas.listar"))

        except Exception:
            db.session.rollback()

            flash(
                "Ocurrió un error al actualizar la vacuna.",
                "danger"
            )

    elif not form.is_submitted():

        form.nombre.data = vacuna.nombre
        form.descripcion.data = vacuna.descripcion
        form.precio.data = vacuna.precio
        form.fecha_aplicacion.data = vacuna.fecha_aplicacion
        form.fecha_proxima.data = vacuna.fecha_proxima
        form.lote.data = vacuna.lote
        form.mascota_id.data = vacuna.mascota_id
        form.veterinario_id.data = vacuna.veterinario_id
        form.observaciones.data = vacuna.observaciones

    return render_template(
        "vacunas/editar.html",
        form=form,
        vacuna=vacuna
    )


@bp.route("/eliminar/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "veterinario", "usuario")
def eliminar(id):

    vacuna = db.session.get(Vacuna, id)

    if not vacuna:
        flash(
            "El registro de vacunación no existe.",
            "warning"
        )
        return redirect(url_for("vacunas.listar"))

    pago_existente = Pago.query.filter_by(
        vacuna_id=vacuna.id
    ).first()

    if pago_existente:
        flash(
            "No se puede eliminar esta vacuna porque tiene un pago asociado. "
            "Conserva el registro para mantener el historial de cobros.",
            "warning"
        )
        return redirect(url_for("vacunas.listar"))

    try:
        db.session.delete(vacuna)
        db.session.commit()

        flash(
            "Registro de vacunación eliminado correctamente.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "Ocurrió un error al eliminar el registro de vacunación.",
            "danger"
        )

    return redirect(url_for("vacunas.listar"))