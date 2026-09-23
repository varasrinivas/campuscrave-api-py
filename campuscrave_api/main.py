"""The front door: builds the FastAPI app and starts the server on :8080."""

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from campuscrave_api.api import menu, rush_meter, wallet
from campuscrave_api.db.bootstrap import prepare_database
from campuscrave_api.errors import install_error_handlers
from campuscrave_api.settings import get_settings


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s.%(msecs)03d %(levelname)-5s %(name)s : %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        force=True,
    )
    logging.getLogger("campuscrave_api").setLevel(level)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    prepare_database(get_settings())
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title="campuscrave-api", lifespan=lifespan)

    # Lets the Vite dev server (campuscrave-web on :5173) talk to us during development.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allowed_origins),
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    install_error_handlers(app)

    for module in (menu, wallet, rush_meter):
        app.include_router(module.router)
    return app


app = create_app()


def run() -> None:
    settings = get_settings()
    uvicorn.run(app, host=settings.server_host, port=settings.server_port, log_config=None)
