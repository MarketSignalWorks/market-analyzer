"""create tickers and prices tables

Revision ID: 0001
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tickers",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("symbol", sa.String(16), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.UniqueConstraint("symbol"),
    )
    op.create_index("ix_tickers_symbol", "tickers", ["symbol"])

    op.create_table(
        "prices",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("symbol", sa.String(16), nullable=False),
        sa.Column(
            "ts",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("price", sa.Float(), nullable=False),
    )
    op.create_index("ix_prices_symbol", "prices", ["symbol"])
    op.create_index("ix_prices_ts", "prices", ["ts"])
    op.create_index("ix_prices_symbol_ts", "prices", ["symbol", "ts"])


def downgrade() -> None:
    op.drop_table("prices")
    op.drop_table("tickers")
