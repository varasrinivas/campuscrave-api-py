from dataclasses import replace

import pytest

from campuscrave_api.db.bootstrap import prepare_database
from campuscrave_api.db.session import SessionLocal
from campuscrave_api.settings import load_settings


@pytest.fixture
def session(tmp_path):
    """A fresh Day-1 canteen for every test, in its own throwaway database file."""
    settings = replace(
        load_settings(),
        database_url=f"sqlite:///{(tmp_path / 'test.db').as_posix()}",
        database_fresh_on_start=True,
        echo_sql=False,
    )
    prepare_database(settings)
    with SessionLocal() as s:
        yield s
