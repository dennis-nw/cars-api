"""Initial migration

Revision ID: a98cc789d0ac
Revises: 
Create Date: 2024-04-24 15:06:07.083818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a98cc789d0ac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "car_makes",
        sa.Column(
            "id", sa.String(100), primary_key=True, autoincrement=False, nullable=False
        ),
        sa.Column("name", sa.String(100), unique=True, nullable=False),
    )
    op.create_index("ix_name", "car_makes", ["name"])

    op.create_table(
        "car_models",
        sa.Column(
            "id", sa.String(100), primary_key=True, autoincrement=False, nullable=False
        ),
        sa.Column("name", sa.String(100), unique=True, nullable=False),
        sa.Column("make_id", sa.String(100), nullable=False),
    )

    # See https://alembic.sqlalchemy.org/en/latest/batch.html
    with op.batch_alter_table("car_models") as batch_op:
        batch_op.create_foreign_key(
            "fk_car_models_make_id", "car_makes", ["make_id"], ["id"]
        )
        batch_op.create_unique_constraint(
            "uq_car_models_name_make_id", ["name", "make_id"]
        )


def downgrade() -> None:
    op.drop_constraint("uq_car_models_name_make_id", "car_models")
    op.drop_table("car_models")
    op.drop_table("car_makes")
