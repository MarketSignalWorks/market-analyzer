"""Database query helpers.  All functions return pandas DataFrames."""

from __future__ import annotations

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------


def get_latest_prices(engine: Engine) -> pd.DataFrame:
    """Return the most recent price row for each symbol."""
    sql = text("""
        SELECT DISTINCT ON (symbol)
               symbol, ts, price
        FROM   prices
        ORDER  BY symbol, ts DESC
        """)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)


def get_pg_version(engine: Engine) -> str:
    """Return the PostgreSQL version string."""
    with engine.connect() as conn:
        row = conn.execute(text("SELECT version()")).fetchone()
        return row[0] if row else "unknown"


# ---------------------------------------------------------------------------
# Write (idempotent seed)
# ---------------------------------------------------------------------------

SEED_TICKERS = [
    ("AAPL", "Apple Inc."),
    ("MSFT", "Microsoft Corp."),
    ("GOOG", "Alphabet Inc."),
]

SEED_PRICES = [
    ("AAPL", 227.50),
    ("MSFT", 415.30),
    ("GOOG", 176.80),
]


def seed_demo_data(engine: Engine) -> None:
    """Insert demo tickers and prices.  Safe to call multiple times."""
    with engine.begin() as conn:
        # Tickers – ON CONFLICT DO NOTHING keeps it idempotent
        for symbol, name in SEED_TICKERS:
            conn.execute(
                text(
                    "INSERT INTO tickers (symbol, name) "
                    "VALUES (:symbol, :name) "
                    "ON CONFLICT (symbol) DO NOTHING"
                ),
                {"symbol": symbol, "name": name},
            )

        # Prices – only insert when the table is empty so repeated
        # clicks don't pile up duplicate rows.
        count = conn.execute(text("SELECT count(*) FROM prices")).scalar()
        if count == 0:
            for symbol, price in SEED_PRICES:
                conn.execute(
                    text("INSERT INTO prices (symbol, price) " "VALUES (:symbol, :price)"),
                    {"symbol": symbol, "price": price},
                )
