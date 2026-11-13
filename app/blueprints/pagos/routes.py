from flask import render_template, redirect, url_for, flash
from wtforms.fields.choices import SelectChoice

from app.extensions import db
from app.models import Pago, Cliente, Cita
from app.blueprints.pagos import bp
from app.blueprints.pagos.forms import PagoForm
from app.utils.decorators import roles_requeridos


@bp.route("/")
@roles_requeridos("administrador", "cajero")
def listar():

    pagos = Pago.query.order_by(
        Pago.id.desc()
    ).all()

    return render_template(
        "pagos/listar.html",
        pagos=pagos
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@roles_requeridos("administrador", "cajero")
def nuevo():

    form = PagoForm()

    clientes = Cliente.query.order_by(
        Cliente.nombre
    ).all()

    citas = Cita.query.order_by(
        Cita.fecha_hora.desc()
    ).all()

    form.cliente_id.choices = [
        SelectChoice(
            str(cliente.id),
            f"{cliente.nombre} {cliente.apellido}"
        )
        for cliente in clientes
    ]

    form.cita_id.choices = [
        SelectChoice("0", "Sin cita asociada")
    ] + [
        SelectChoice(
            str(cita.id),
            f"Cita #{cita.id} - {cita.mascota.nombre} - "
            f"{cita.fecha_hora.strftime('%d/%m/%Y %H:%M')}"
        )
        for cita in citas
    ]

    if not clientes:
        flash(
            "Necesitas registrar al menos un cliente para crear un pago.",
            "warning"
        )
        return redirect(url_for("pagos.listar"))

    if form.validate_on_submit():

        if form.estado.data == "pagado" and (
            not form.metodo_pago.data or not form.fecha_pago.data
        ):
            flash(
                "Para registrar un pago como pagado debes indicar el método "
                "y la fecha del pago.",
                "warning"
            )
            return render_template(
                "pagos/nuevo.html",
                form=form
            )

        comprobante = (
            form.comprobante.data.strip()
            if form.comprobante.data else None
        )

        if comprobante:
            existente = Pago.query.filter_by(
                comprobante=comprobante
            ).first()

            if existente:
                flash(
                    "El número de comprobante ya está registrado.",
                    "warning"
                )
                return render_template(
                    "pagos/nuevo.html",
                    form=form
                )

        pago = Pago(
            concepto=form.concepto.data.strip(),
            monto=form.monto.data,
            metodo_pago=form.metodo_pago.data or None,
            fecha_pago=form.fecha_pago.data,
            estado=form.estado.data,
            comprobante=comprobante,
            observaciones=(
                form.observaciones.data.strip()
                if form.observaciones.data else None
            ),
            cliente_id=form.cliente_id.data,
            cita_id=form.cita_id.data or None
        )

        try:
            db.session.add(pago)
            db.session.commit()

            flash(
                "Pago registrado correctamente.",
                "success"
            )

            return redirect(url_for("pagos.listar"))

        except Exception:
            db.session.rollback()

            flash(
                "Ocurrió un error al registrar el pago.",
                "danger"
            )

    return render_template(
        "pagos/nuevo.html",
        form=form
    )


@bp.route("/editar/<int:id>", methods=["GET", "POST"])
@roles_requeridos("administrador", "cajero")
def editar(id):

    pago = db.session.get(Pago, id)

    if pago is None:
        flash(
            "El pago solicitado no existe.",
            "warning"
        )
        return redirect(url_for("pagos.listar"))

    form = PagoForm(obj=pago)

    clientes = Cliente.query.order_by(
        Cliente.nombre
    ).all()

    citas = Cita.query.order_by(
        Cita.fecha_hora.desc()
    ).all()

    form.cliente_id.choices = [
        SelectChoice(
            str(cliente.id),
            f"{cliente.nombre} {cliente.apellido}"
        )
        for cliente in clientes
    ]

    form.cita_id.choices = [
        SelectChoice("0", "Sin cita asociada")
    ] + [
        SelectChoice(
            str(cita.id),
            f"Cita #{cita.id} - {cita.mascota.nombre} - "
            f"{cita.fecha_hora.strftime('%d/%m/%Y %H:%M')}"
        )
        for cita in citas
    ]

    if not form.is_submitted():
        form.cita_id.data = pago.cita_id or 0

    if form.validate_on_submit():

        if form.estado.data == "pagado" and (
            not form.metodo_pago.data or not form.fecha_pago.data
        ):
            flash(
                "Para registrar un pago como pagado debes indicar el método "
                "y la fecha del pago.",
                "warning"
            )
            return render_template(
                "pagos/editar.html",
                form=form,
                pago=pago
            )

        comprobante = (
            form.comprobante.data.strip()
            if form.comprobante.data else None
        )

        if comprobante:
            existente = Pago.query.filter(
                Pago.comprobante == comprobante,
                Pago.id != pago.id
            ).first()

            if existente:
                flash(
                    "El número de comprobante ya está registrado.",
                    "warning"
                )
                return render_template(
                    "pagos/editar.html",
                    form=form,
                    pago=pago
                )

        try:
            if pago.vacuna_id is not None:
                # Un pago de vacuna conserva su concepto, importe,
                # propietario y relación con la vacunación.
                pago.metodo_pago = form.metodo_pago.data or None
                pago.fecha_pago = form.fecha_pago.data
                pago.estado = form.estado.data
                pago.comprobante = comprobante
                pago.observaciones = (
                    form.observaciones.data.strip()
                    if form.observaciones.data else None
                )

            else:
                # Los pagos normales conservan la edición completa.
                pago.concepto = form.concepto.data.strip()
                pago.monto = form.monto.data
                pago.metodo_pago = form.metodo_pago.data or None
                pago.fecha_pago = form.fecha_pago.data
                pago.estado = form.estado.data
                pago.comprobante = comprobante
                pago.cliente_id = form.cliente_id.data
                pago.cita_id = form.cita_id.data or None
                pago.observaciones = (
                    form.observaciones.data.strip()
                    if form.observaciones.data else None
                )

            db.session.commit()

            flash(
                "Pago actualizado correctamente.",
                "success"
            )

            return redirect(url_for("pagos.listar"))

        except Exception:
            db.session.rollback()

            flash(
                "Ocurrió un error al actualizar el pago.",
                "danger"
            )

    return render_template(
        "pagos/editar.html",
        form=form,
        pago=pago
    )


@bp.route("/eliminar/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "cajero")
def eliminar(id):

    pago = db.session.get(Pago, id)

    if pago is None:
        flash(
            "El pago solicitado no existe.",
            "warning"
        )
        return redirect(url_for("pagos.listar"))

    if pago.vacuna_id is not None:
        flash(
            "No se puede eliminar este pago porque está asociado a una vacuna. "
            "Se debe conservar el historial de vacunación y cobro.",
            "warning"
        )
        return redirect(url_for("pagos.listar"))

    try:
        db.session.delete(pago)
        db.session.commit()

        flash(
            "Pago eliminado correctamente.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "Ocurrió un error al eliminar el pago.",
            "danger"
        )

    return redirect(url_for("pagos.listar"))
