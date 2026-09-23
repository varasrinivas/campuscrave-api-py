from datetime import time

from sqlalchemy.orm import Session

from campuscrave_api.config import business_rules
from campuscrave_api.models import CanteenConfig
from campuscrave_api.repositories.canteen_config_repository import CanteenConfigRepository


class CanteenConfigService:
    """Reads the canteen's own settings, falling back to business_rules defaults
    if nobody has configured anything yet.
    """

    def __init__(self, session: Session) -> None:
        self.repository = CanteenConfigRepository(session)

    def _current(self) -> CanteenConfig | None:
        return self.repository.find_by_id(1)

    def order_cutoff(self) -> time:
        config = self._current()
        return config.order_cutoff if config else business_rules.ORDER_CUTOFF

    def rush_start(self) -> time:
        config = self._current()
        return config.rush_start if config else business_rules.RUSH_WINDOW_START

    def rush_end(self) -> time:
        config = self._current()
        return config.rush_end if config else business_rules.RUSH_WINDOW_END

    def max_active_orders(self) -> int:
        config = self._current()
        return config.max_active_orders if config else business_rules.MAX_ACTIVE_ORDERS

    def is_accepting_orders(self) -> bool:
        config = self._current()
        return config.accepting_orders if config else True
