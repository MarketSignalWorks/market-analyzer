"""Smoke tests — these must pass WITHOUT a running Postgres instance."""

from __future__ import annotations


def test_import_models():
    """Models module is importable and has expected tables."""
    from src.db.models import Base, Price, Ticker

    table_names = {t.name for t in Base.metadata.sorted_tables}
    assert "tickers" in table_names
    assert "prices" in table_names
    # Sanity-check that mapped classes exist
    assert Ticker.__tablename__ == "tickers"
    assert Price.__tablename__ == "prices"


def test_import_connection():
    """connection module is importable."""
    from src.db.connection import get_engine  # noqa: F401


def test_import_queries():
    """queries module is importable."""
    from src.db.queries import get_latest_prices, seed_demo_data  # noqa: F401
