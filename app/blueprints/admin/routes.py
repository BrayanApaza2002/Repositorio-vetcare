
from datetime import datetime
from decimal import Decimal

from flask import render_template
from app.extensions import db

from app.blueprints.admin import bp
from app.utils.decorators import roles_requeridos
from app.models import (
    Cliente,
    Mascota,
    Veterinario,
    Cita,
    Pago
)


@bp.route("/")
@roles_requeridos("administrador")
def dashboard():

    # Estadísticas generales
    total_clientes = Cliente.query.count()
    total_mascotas = Mascota.query.count()
    total_veterinarios = Veterinario.query.count()
    total_citas = Cita.query.count()

    # Estadísticas financieras
    total_pagos = Pago.query.count()

    ingresos_confirmados = db.session.query(
        db.func.coalesce(db.func.sum(Pago.monto), 0)
    ).filter(
        Pago.estado == "pagado"
    ).scalar()

    pagos_pendientes = Pago.query.filter_by(
        estado="pendiente"
    ).count()

    # Gráfico 1: citas por estado
    estados_citas = [
        "pendiente",
        "confirmada",
        "completada",
        "cancelada"
    ]

    citas_por_estado = {
        estado: 0 for estado in estados_citas
    }

    resultados_citas = db.session.query(
        Pago.__class__  # Se reemplaza por la consulta de Cita abajo.
    ).first() if False else []

    resultados_citas = db.session.query(
        Cita.estado,
        db.func.count(Cita.id)
    ).group_by(
        Cita.estado
    ).all()

    for estado, cantidad in resultados_citas:
        estado_normalizado = (estado or "").lower()

        if estado_normalizado in citas_por_estado:
            citas_por_estado[estado_normalizado] = cantidad
        elif estado_normalizado:
            citas_por_estado[estado_normalizado] = cantidad

    etiquetas_citas = [
        estado.capitalize()
        for estado in citas_por_estado
    ]

    datos_citas = list(citas_por_estado.values())

    # Gráfico 2: mascotas por especie
    resultados_especies = db.session.query(
        Mascota.especie,
        db.func.count(Mascota.id)
    ).group_by(
        Mascota.especie
    ).all()

    etiquetas_especies = [
        especie or "Sin especificar"
        for especie, cantidad in resultados_especies
    ]

    datos_especies = [
        cantidad
        for especie, cantidad in resultados_especies
    ]

    # Gráfico 3: ingresos de los últimos 12 meses
    nombres_meses = [
        "Enero", "Febrero", "Marzo", "Abril",
        "Mayo", "Junio", "Julio", "Agosto",
        "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    fecha_actual = datetime.now()
    anio = fecha_actual.year
    mes = fecha_actual.month

    meses = []

    for _ in range(12):
        meses.append((anio, mes))

        mes -= 1

        if mes == 0:
            mes = 12
            anio -= 1

    meses.reverse()

    fecha_inicio = datetime(
        meses[0][0],
        meses[0][1],
        1
    )

    if meses[-1][1] == 12:
        fecha_fin = datetime(meses[-1][0] + 1, 1, 1)
    else:
        fecha_fin = datetime(
            meses[-1][0],
            meses[-1][1] + 1,
            1
        )

    pagos_mensuales = Pago.query.filter(
        Pago.estado == "pagado",
        Pago.fecha_pago >= fecha_inicio,
        Pago.fecha_pago < fecha_fin
    ).all()

    ingresos_por_mes = {
        periodo: Decimal("0.00")
        for periodo in meses
    }

    for pago in pagos_mensuales:
        periodo = (
            pago.fecha_pago.year,
            pago.fecha_pago.month
        )

        if periodo in ingresos_por_mes:
            ingresos_por_mes[periodo] += pago.monto

    etiquetas_meses = [
        f"{nombres_meses[mes - 1]} {anio}"
        for anio, mes in meses
    ]

    datos_ingresos = [
        float(ingresos_por_mes[periodo])
        for periodo in meses
    ]

    return render_template(
        "admin/dashboard.html",
        total_clientes=total_clientes,
        total_mascotas=total_mascotas,
        total_veterinarios=total_veterinarios,
        total_citas=total_citas,
        total_pagos=total_pagos,
        ingresos_confirmados=ingresos_confirmados,
        pagos_pendientes=pagos_pendientes,

        etiquetas_citas=etiquetas_citas,
        datos_citas=datos_citas,

        etiquetas_especies=etiquetas_especies,
        datos_especies=datos_especies,

        etiquetas_meses=etiquetas_meses,
        datos_ingresos=datos_ingresos
    )
