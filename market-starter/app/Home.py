"""Streamlit home page – connects to Postgres and displays market data."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so `src` package is importable.
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from src.db.connection import get_engine  # noqa: E402
from src.db.queries import get_latest_prices, get_pg_version, seed_demo_data  # noqa: E402

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Market Starter", page_icon="📈")
st.title("📈 Market Data Starter")

# ---------------------------------------------------------------------------
# Database connection status
# ---------------------------------------------------------------------------
try:
    engine = get_engine()
    pg_version = get_pg_version(engine)
    st.success(f"DB connected — {pg_version}")
except Exception as exc:
    st.error(f"DB connection failed: {exc}")
    st.stop()

# ---------------------------------------------------------------------------
# Seed button (idempotent)
# ---------------------------------------------------------------------------
if st.button("🌱 Seed demo data"):
    seed_demo_data(engine)
    st.toast("Demo data seeded!")

# ---------------------------------------------------------------------------
# Latest prices table
# ---------------------------------------------------------------------------
st.subheader("Latest prices")
df = get_latest_prices(engine)
if df.empty:
    st.info("No price data yet — click **Seed demo data** above.")
else:
    st.dataframe(df, use_container_width=True)
