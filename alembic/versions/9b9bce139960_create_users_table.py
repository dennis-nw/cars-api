"""create users table

Revision ID: 9b9bce139960
Revises: a98cc789d0ac
Create Date: 2024-05-22 17:20:07.634005

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision: str = '9b9bce139960'
down_revision: Union[str, None] = 'a98cc789d0ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id", sa.Integer, primary_key=True, autoincrement=True
        ),
        sa.Column(
            "email", sa.String(100), unique=True, nullable=False
        ),
        sa.Column(
            "password", sa.String(150), nullable=False
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=False), server_default=func.now()
        )
    )


def downgrade() -> None:
    op.drop_table("users")
