
"""Relacionar vacunas con pagos

Revision ID: af03996e713b
Revises: 8fe65469122b
Create Date: 2026-11-12
"""

from alembic import op
import sqlalchemy as sa


revision = "af03996e713b"
down_revision = "8fe65469122b"
branch_labels = None
depends_on = None


def upgrade():

    # Agregar la relación entre pagos y vacunas.
    with op.batch_alter_table("pagos", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column("vacuna_id", sa.Integer(), nullable=True)
        )

        batch_op.alter_column(
            "metodo_pago",
            existing_type=sa.VARCHAR(length=30),
            nullable=True
        )

        batch_op.alter_column(
            "fecha_pago",
            existing_type=sa.DATETIME(),
            nullable=True
        )

        batch_op.create_unique_constraint(
            "uq_pagos_vacuna_id",
            ["vacuna_id"]
        )

        batch_op.create_foreign_key(
            "fk_pagos_vacuna_id_vacunas",
            "vacunas",
            ["vacuna_id"],
            ["id"]
        )

    # Agregar el precio de cada vacuna.
    with op.batch_alter_table("vacunas", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                "precio",
                sa.Numeric(10, 2),
                nullable=True
            )
        )


def downgrade():

    # Retirar el precio de las vacunas.
    with op.batch_alter_table("vacunas", schema=None) as batch_op:

        batch_op.drop_column("precio")

    # Retirar la relación entre pagos y vacunas.
    with op.batch_alter_table("pagos", schema=None) as batch_op:

        batch_op.drop_constraint(
            "fk_pagos_vacuna_id_vacunas",
            type_="foreignkey"
        )

        batch_op.drop_constraint(
            "uq_pagos_vacuna_id",
            type_="unique"
        )

        batch_op.alter_column(
            "fecha_pago",
            existing_type=sa.DATETIME(),
            nullable=False
        )

        batch_op.alter_column(
            "metodo_pago",
            existing_type=sa.VARCHAR(length=30),
            nullable=False
        )

        batch_op.drop_column("vacuna_id")
