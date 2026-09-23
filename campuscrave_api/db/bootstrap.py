"""Gets the database ready before the first request: schema first, then seed data."""

import logging
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import text

from campuscrave_api.db import session
from campuscrave_api.settings import PROJECT_ROOT, Settings

log = logging.getLogger(__name__)


def prepare_database(settings: Settings) -> None:
    if settings.database_fresh_on_start:
        _delete_sqlite_file(settings.database_url)

    engine = session.configure(settings.database_url, echo=settings.echo_sql)
    _migrate(engine)

    if settings.seed_mode == "always":
        for seed_file in settings.seed_files:
            _run_sql_file(engine, seed_file)
            log.info("Seeded from %s", seed_file.relative_to(PROJECT_ROOT).as_posix())


def _delete_sqlite_file(url: str) -> None:
    prefix = "sqlite:///"
    if not url.startswith(prefix):
        return
    db_file = Path(url[len(prefix):])
    db_file.parent.mkdir(parents=True, exist_ok=True)
    for suffix in ("", "-wal", "-shm"):
        Path(str(db_file) + suffix).unlink(missing_ok=True)


def _migrate(engine) -> None:
    """Alembic owns the schema. Same job Flyway does on the Java side."""
    config = Config(str(PROJECT_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(PROJECT_ROOT / "migrations"))
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")


def _run_sql_file(engine, path: Path) -> None:
    lines = [
        line
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.strip().startswith("--")
    ]
    statements = [s.strip() for s in "\n".join(lines).split(";") if s.strip()]
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
