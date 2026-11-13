
from flask import render_template, redirect, url_for, flash
from app.models import Cliente
from app.models import Cliente, Mascota, Cita, Pago

from app.extensions import db
from app.models import Cliente
from app.blueprints.clientes import bp
from app.blueprints.clientes.forms import ClienteForm
from app.utils.decorators import roles_requeridos


@bp.route("/")
@roles_requeridos("administrador", "recepcionista", "usuario")
def listar():

    clientes = Cliente.query.order_by(
        Cliente.created_at.desc()
    ).all()

    return render_template(
        "clientes/listar.html",
        clientes=clientes
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@roles_requeridos("administrador", "recepcionista", "usuario")
def nuevo():

    form = ClienteForm()

    if form.validate_on_submit():

        cliente_existente = Cliente.query.filter_by(
            ci=form.ci.data.strip()
        ).first()

        if cliente_existente:
            flash(
                "Ya existe un cliente con ese carnet de identidad.",
                "warning"
            )

            return render_template(
                "clientes/nuevo.html",
                form=form
            )

        email = form.email.data.strip().lower() if form.email.data else None

        if email:
            email_existente = Cliente.query.filter_by(
                email=email
            ).first()

            if email_existente:
                flash(
                    "Este correo electrónico ya está registrado.",
                    "warning"
                )

                return render_template(
                    "clientes/nuevo.html",
                    form=form
                )

        cliente = Cliente(
            nombre=form.nombre.data.strip(),
            apellido=form.apellido.data.strip(),
            ci=form.ci.data.strip(),
            telefono=form.telefono.data.strip(),
            email=email,
            direccion=form.direccion.data.strip() if form.direccion.data else None
        )

        try:
            db.session.add(cliente)
            db.session.commit()

            flash(
                "Cliente registrado correctamente.",
                "success"
            )

            return redirect(url_for("clientes.listar"))

        except Exception:
            db.session.rollback()

            flash(
                "Ocurrió un error al registrar el cliente.",
                "danger"
            )

    return render_template(
        "clientes/nuevo.html",
        form=form
    )


@bp.route("/editar/<int:id>", methods=["GET", "POST"])
@roles_requeridos("administrador", "recepcionista", "usuario")
def editar(id):

    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)

    if form.validate_on_submit():

        ci = form.ci.data.strip()

        cliente_existente = Cliente.query.filter(
            Cliente.ci == ci,
            Cliente.id != cliente.id
        ).first()

        if cliente_existente:
            flash(
                "Ya existe otro cliente con ese carnet de identidad.",
                "warning"
            )
            return render_template(
                "clientes/editar.html",
                form=form,
                cliente=cliente
            )

        email = (
            form.email.data.strip().lower()
            if form.email.data
            else None
        )

        if email:
            email_existente = Cliente.query.filter(
                Cliente.email == email,
                Cliente.id != cliente.id
            ).first()

            if email_existente:
                flash(
                    "Este correo electrónico ya está registrado.",
                    "warning"
                )
                return render_template(
                    "clientes/editar.html",
                    form=form,
                    cliente=cliente
                )

        try:
            cliente.nombre = form.nombre.data.strip()
            cliente.apellido = form.apellido.data.strip()
            cliente.ci = ci
            cliente.telefono = form.telefono.data.strip()
            cliente.email = email
            cliente.direccion = (
                form.direccion.data.strip()
                if form.direccion.data
                else None
            )

            db.session.commit()

            flash(
                "Cliente actualizado correctamente.",
                "success"
            )

            return redirect(url_for("clientes.listar"))

        except Exception:
            db.session.rollback()

            flash(
                "Ocurrió un error al actualizar el cliente.",
                "danger"
            )

    return render_template(
        "clientes/editar.html",
        form=form,
        cliente=cliente
    )


@bp.route("/eliminar/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "recepcionista", "usuario")
def eliminar(id):

    cliente = Cliente.query.get_or_404(id)

    try:
        cliente.activo = False

        db.session.commit()

        flash(
            "Cliente desactivado correctamente.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "Ocurrió un error al desactivar el cliente.",
            "danger"
        )

    return redirect(url_for("clientes.listar"))

@bp.route("/activar/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "recepcionista", "usuario")
def activar(id):

    cliente = Cliente.query.get_or_404(id)

    try:
        cliente.activo = True

        db.session.commit()

        flash(
            "Cliente activado correctamente.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "Ocurrió un error al activar el cliente.",
            "danger"
        )

    return redirect(url_for("clientes.listar"))


@bp.route("/eliminar-definitivamente/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "recepcionista", "usuario")
def eliminar_definitivamente(id):

    cliente = Cliente.query.get_or_404(id)

    # Comprobar si tiene mascotas asociadas.
    if Mascota.query.filter_by(cliente_id=id).first():
        flash(
            "No se puede eliminar: el cliente tiene mascotas registradas.",
            "warning"
        )
        return redirect(url_for("clientes.listar"))

    # Comprobar si tiene citas asociadas.
    if Cita.query.filter_by(cliente_id=id).first():
        flash(
            "No se puede eliminar: el cliente tiene citas registradas.",
            "warning"
        )
        return redirect(url_for("clientes.listar"))

    # Comprobar si tiene pagos asociados.
    if Pago.query.filter_by(cliente_id=id).first():
        flash(
            "No se puede eliminar: el cliente tiene pagos registrados.",
            "warning"
        )
        return redirect(url_for("clientes.listar"))

    try:
        db.session.delete(cliente)
        db.session.commit()

        flash(
            "Cliente eliminado definitivamente.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "No se pudo eliminar el cliente. Comprueba sus registros relacionados.",
            "danger"
        )

    return redirect(url_for("clientes.listar"))
