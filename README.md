# 📈 Market Data Starter

A production-quality starter repository: **Python 3.12 · Streamlit · PostgreSQL · SQLAlchemy 2.0 · Alembic · GitHub Actions CI**.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.12+ |
| Docker Desktop | Latest |
| Git | Latest |

---

## Quickstart

### macOS / Linux

```bash
git clone <repo-url> market-starter
cd market-starter

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env          # edit if needed

docker compose up -d           # start Postgres
alembic upgrade head           # run migrations
streamlit run app/Home.py      # open the app 🚀
```

### Windows (PowerShell)

```powershell
git clone <repo-url> market-starter
cd market-starter

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

Copy-Item .env.example .env    # edit if needed

docker compose up -d
alembic upgrade head
streamlit run app/Home.py
```

---

## What the app does

1. Connects to Postgres using `DATABASE_URL` from `.env`.
2. Shows a **DB connected** status badge with the Postgres version.
3. **Seed demo data** button inserts sample tickers and prices (idempotent — safe to click repeatedly).
4. Displays a dataframe of the latest price per ticker.

---

## CI (GitHub Actions)

Every push to `main` and every pull request runs:

| Step | Command |
|------|---------|
| Lint | `ruff check .` |
| Format | `black --check .` |
| Test | `pytest -q` |

CI does **not** require a Postgres database — tests are pure-Python smoke tests.

---

## Updating dependency pins

Versions in `requirements.txt` are pinned with `==`. To bump:

```bash
pip install --upgrade <package>
pip freeze | grep <package>   # copy version into requirements.txt
```

---

## Reset the database

```bash
docker compose down -v         # removes volumes (all data)
docker compose up -d
alembic upgrade head
```

---

## Troubleshooting

### Port 5432 already in use

Another Postgres is running. Stop it, or change the port mapping in `docker-compose.yml` and update `DATABASE_URL` in `.env`.

### Docker not running

Make sure Docker Desktop is started. Run `docker info` to verify.

### `.env` not found / DATABASE_URL missing

```bash
cp .env.example .env
```

Ensure `python-dotenv` is installed (`pip install -r requirements.txt`).

### macOS terminal cannot access Downloads

Go to **System Settings → Privacy & Security → Full Disk Access** and add your terminal app.

---

## Team workflow

1. **Branches** — use `feat/<slug>`, `fix/<slug>`, or `chore/<slug>`.
2. **Pull requests** — all changes go through PRs to `main`.
3. **Reviews** — at least 1 approval recommended before merging.
4. **CI must be green** — do not merge with failing checks.
