"""One database connection pool for the whole API, one session per request."""

import logging
from collections.abc import Iterator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

SessionLocal = sessionmaker(expire_on_commit=True)

_engine: Engine | None = None


def configure(url: str, echo: bool = False) -> Engine:
    global _engine
    if _engine is not None:
        _engine.dispose()

    # One line per statement, in the API's own log format.
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO if echo else logging.WARNING)

    if url.startswith("sqlite"):
        # Every request runs on its own thread, so connections must be shareable,
        # and a writer should wait its turn rather than fail straight away.
        _engine = create_engine(url, connect_args={"check_same_thread": False, "timeout": 30})
        event.listen(_engine, "connect", _sqlite_pragmas)
    else:
        _engine = create_engine(url)

    SessionLocal.configure(bind=_engine)
    return _engine


def engine() -> Engine:
    if _engine is None:
        raise RuntimeError("Database not configured — call configure() first")
    return _engine


def _sqlite_pragmas(dbapi_connection, _record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("PRAGMA journal_mode = WAL")
    cursor.close()


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session
