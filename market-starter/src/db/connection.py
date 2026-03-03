"""Database connection helpers."""

from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    """Return a SQLAlchemy engine using DATABASE_URL from the environment."""
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. " "Copy .env.example to .env and make sure it is loaded."
        )
    return create_engine(url, pool_pre_ping=True)
