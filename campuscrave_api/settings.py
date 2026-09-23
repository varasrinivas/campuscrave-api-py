"""Where the API reads its settings from.

`config/application.toml` holds the dev defaults. Set CAMPUSCRAVE_PROFILE=prod and
`config/application-prod.toml` is laid over the top of it. A few environment
variables win over both files:

- DATABASE_URL            — where the database lives
- CAMPUSCRAVE_SQL_ECHO=1  — print every SQL statement the API sends
- CAMPUSCRAVE_EXTRA_SEED  — more seed files to load after data.sql, comma-separated
"""

import os
import tomllib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"


@dataclass(frozen=True)
class Settings:
    profile: str
    server_host: str
    server_port: int
    database_url: str
    database_fresh_on_start: bool
    echo_sql: bool
    seed_mode: str
    seed_files: tuple[Path, ...]
    cors_allowed_origins: tuple[str, ...]
    payments_api_secret: str
    log_level: str


def _merge(base: dict, override: dict) -> dict:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _read(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def _absolute_sqlite(url: str) -> str:
    """A relative SQLite path means relative to the project, not to wherever you ran the command."""
    prefix = "sqlite:///"
    if not url.startswith(prefix):
        return url
    path = Path(url[len(prefix):])
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return prefix + path.as_posix()


def load_settings() -> Settings:
    profile = os.environ.get("CAMPUSCRAVE_PROFILE", "dev")

    raw = _read(CONFIG_DIR / "application.toml")
    profile_file = CONFIG_DIR / f"application-{profile}.toml"
    if profile != "dev" and profile_file.exists():
        raw = _merge(raw, _read(profile_file))

    database_url = os.environ.get("DATABASE_URL", raw["database"]["url"])

    seed_files = [PROJECT_ROOT / f for f in raw["seed"].get("files", [])]
    extra = os.environ.get("CAMPUSCRAVE_EXTRA_SEED", "")
    seed_files += [PROJECT_ROOT / f.strip() for f in extra.split(",") if f.strip()]

    echo_sql = raw["database"].get("echo_sql", False)
    if os.environ.get("CAMPUSCRAVE_SQL_ECHO"):
        echo_sql = os.environ["CAMPUSCRAVE_SQL_ECHO"] not in ("0", "false", "")

    return Settings(
        profile=profile,
        server_host=raw["server"]["host"],
        server_port=raw["server"]["port"],
        database_url=_absolute_sqlite(database_url),
        database_fresh_on_start=raw["database"].get("fresh_on_start", False),
        echo_sql=echo_sql,
        seed_mode=raw["seed"]["mode"],
        seed_files=tuple(seed_files),
        cors_allowed_origins=tuple(raw["cors"]["allowed_origins"]),
        payments_api_secret=raw["campuscrave"]["payments"]["api_secret"],
        log_level=raw["logging"]["level"],
    )


@lru_cache
def get_settings() -> Settings:
    return load_settings()
