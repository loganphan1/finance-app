"""store transaction amount as numeric

Revision ID: b65224dd408b
Revises: 0387645463eb
Create Date: 2026-09-29

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b65224dd408b"
down_revision: Union[str, Sequence[str], None] = "0387645463eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "transactions",
        "amount",
        existing_type=sa.Float(),
        type_=sa.Numeric(precision=12, scale=2),
        existing_nullable=False,
        postgresql_using="amount::numeric(12, 2)",
    )


def downgrade() -> None:
    op.alter_column(
        "transactions",
        "amount",
        existing_type=sa.Numeric(precision=12, scale=2),
        type_=sa.Float(),
        existing_nullable=False,
        postgresql_using="amount::double precision",
    )
