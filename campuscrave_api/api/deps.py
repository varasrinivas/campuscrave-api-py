"""Hands each request its own database session, and the services built on it."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from campuscrave_api.db.session import get_session

SessionDep = Annotated[Session, Depends(get_session)]
