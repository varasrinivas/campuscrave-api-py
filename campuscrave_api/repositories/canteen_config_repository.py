from sqlalchemy.orm import Session

from campuscrave_api.models import CanteenConfig


class CanteenConfigRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, config_id: int) -> CanteenConfig | None:
        return self.session.get(CanteenConfig, config_id)
