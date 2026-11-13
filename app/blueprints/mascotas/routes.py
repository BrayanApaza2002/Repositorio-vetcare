
from flask import render_template, redirect, url_for, flash
from wtforms.fields.choices import SelectChoice
from app.models import Mascota, Cliente
from app.models import Mascota, Cliente, Cita, Historial, Vacuna

from app.extensions import db
from app.models import Mascota, Cliente
from app.blueprints.mascotas import bp
from app.blueprints.mascotas.forms import MascotaForm
from app.utils.decorators import roles_requeridos


@bp.route("/")
@roles_requeridos("administrador", "veterinario", "recepcionista", "usuario")
def listar():

    mascotas = Mascota.query.order_by(
        Mascota.created_at.desc()
    ).all()

    return render_template(
        "mascotas/listar.html",
        mascotas=mascotas
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@roles_requeridos("administrador", "veterinario", "recepcionista", "usuario")
def nuevo():

    form = MascotaForm()

    clientes = Cliente.query.filter_by(
        activo=True
    ).order_by(Cliente.nombre).all()

    form.cliente_id.choices = [
    SelectChoice(
        str(cliente.id),
        f"{cliente.nombre} {cliente.apellido} - CI: {cliente.ci}"
    )
    for cliente in clientes
]

    if not clientes:
        flash(
            "Primero debes registrar un cliente para poder registrar mascotas.",
            "warning"
        )

        return redirect(url_for("clientes.nuevo"))

    if form.validate_on_submit():

        mascota = Mascota(
            nombre=form.nombre.data.strip(),
            especie=form.especie.data,
            raza=form.raza.data.strip() if form.raza.data else None,
            sexo=form.sexo.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            color=form.color.data.strip() if form.color.data else None,
            peso=form.peso.data,
            observaciones=form.observaciones.data,
            cliente_id=form.cliente_id.data
        )

        try:
            db.session.add(mascota)
            db.session.commit()

            flash(
                "Mascota registrada correctamente.",
                "success"
            )

            return redirect(url_for("mascotas.listar"))

        except Exception:
            db.session.rollback()

            flash(
                "Ocurrió un error al registrar la mascota.",
                "danger"
            )

    return render_template(
        "mascotas/nuevo.html",
        form=form
    )


@bp.route("/editar/<int:id>", methods=["GET", "POST"])
@roles_requeridos("administrador", "veterinario", "recepcionista", "usuario")
def editar(id):

    mascota = Mascota.query.get_or_404(id)

    form = MascotaForm(obj=mascota)

    clientes = Cliente.query.filter_by(
        activo=True
    ).order_by(Cliente.nombre).all()

    # Incluir al propietario actual aunque esté desactivado.
    cliente_actual = Cliente.query.get(mascota.cliente_id)

    if cliente_actual and cliente_actual not in clientes:
        clientes.append(cliente_actual)

    form.cliente_id.choices = [
    SelectChoice(
        str(cliente.id),
        f"{cliente.nombre} {cliente.apellido} - CI: {cliente.ci}"
    )
    for cliente in clientes
]

    if form.validate_on_submit():

        mascota.nombre = form.nombre.data.strip()
        mascota.especie = form.especie.data
        mascota.raza = form.raza.data.strip() if form.raza.data else None
        mascota.sexo = form.sexo.data
        mascota.fecha_nacimiento = form.fecha_nacimiento.data
        mascota.color = form.color.data.strip() if form.color.data else None
        mascota.peso = form.peso.data
        mascota.observaciones = form.observaciones.data
        mascota.cliente_id = form.cliente_id.data

        try:
            db.session.commit()

            flash(
                "Mascota modificada correctamente.",
                "success"
            )

            return redirect(url_for("mascotas.listar"))

        except Exception:
            db.session.rollback()

            flash(
                "Ocurrió un error al modificar la mascota.",
                "danger"
            )

    return render_template(
        "mascotas/editar.html",
        form=form,
        mascota=mascota
    )


@bp.route("/eliminar/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "veterinario", "recepcionista", "usuario")
def eliminar(id):

    mascota = Mascota.query.get_or_404(id)

    try:
        mascota.activo = False
        db.session.commit()

        flash(
            "Mascota desactivada correctamente.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "Ocurrió un error al desactivar la mascota.",
            "danger"
        )

    return redirect(url_for("mascotas.listar"))

@bp.route("/activar/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "veterinario", "recepcionista", "usuario")
def activar(id):
    mascota = Mascota.query.get_or_404(id)

    try:
        mascota.activo = True
        db.session.commit()
        flash("Mascota activada correctamente.", "success")

    except Exception:
        db.session.rollback()
        flash("Ocurrió un error al activar la mascota.", "danger")

    return redirect(url_for("mascotas.listar"))


@bp.route("/eliminar-definitivamente/<int:id>", methods=["POST"])
@roles_requeridos("administrador", "veterinario", "recepcionista", "usuario")
def eliminar_definitivamente(id):

    mascota = Mascota.query.get_or_404(id)

    # Comprobar citas asociadas.
    if Cita.query.filter_by(mascota_id=id).first():
        flash(
            "No se puede eliminar: la mascota tiene citas registradas.",
            "warning"
        )
        return redirect(url_for("mascotas.listar"))

    # Comprobar historiales clínicos.
    if Historial.query.filter_by(mascota_id=id).first():
        flash(
            "No se puede eliminar: la mascota tiene historiales clínicos.",
            "warning"
        )
        return redirect(url_for("mascotas.listar"))

    # Comprobar vacunas asociadas.
    if Vacuna.query.filter_by(mascota_id=id).first():
        flash(
            "No se puede eliminar: la mascota tiene vacunas registradas.",
            "warning"
        )
        return redirect(url_for("mascotas.listar"))

    try:
        db.session.delete(mascota)
        db.session.commit()

        flash(
            "Mascota eliminada definitivamente.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "No se pudo eliminar la mascota. Comprueba sus registros relacionados.",
            "danger"
        )

    return redirect(url_for("mascotas.listar"))
