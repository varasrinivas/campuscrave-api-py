from alembic import context
from sqlalchemy import create_engine

from campuscrave_api.settings import load_settings

config = context.config


def run_migrations() -> None:
    # The API hands us its own open connection; the alembic CLI does not.
    connection = config.attributes.get("connection")
    if connection is not None:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()
        return

    engine = create_engine(load_settings().database_url)
    with engine.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()


run_migrations()
