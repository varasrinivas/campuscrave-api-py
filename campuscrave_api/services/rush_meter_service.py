from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from campuscrave_api.config import business_rules
from campuscrave_api.repositories.order_repository import OrderRepository
from campuscrave_api.schemas.rush import RushMeter
from campuscrave_api.services.canteen_config_service import CanteenConfigService

CAMPUS_ZONE = ZoneInfo("Asia/Kolkata")
BASE_WAIT_MINUTES = 6


class RushMeterService:
    """Powers the little red dot on the menu screen that tells students whether
    the window is mobbed right now.
    """

    def __init__(self, session: Session) -> None:
        self.order_repository = OrderRepository(session)
        self.canteen_config = CanteenConfigService(session)

    def current(self) -> RushMeter:
        now_on_campus = datetime.now(CAMPUS_ZONE).time()
        start = self.canteen_config.rush_start()
        end = self.canteen_config.rush_end()

        rush_on = not now_on_campus < start and not now_on_campus > end
        recent_orders = self.order_repository.count_placed_since(datetime.now(UTC) - timedelta(hours=1))

        wait = BASE_WAIT_MINUTES + recent_orders // 4
        if rush_on:
            wait += business_rules.RUSH_WAIT_PENALTY_MINUTES

        return RushMeter(
            rush_on=rush_on,
            orders_in_last_hour=recent_orders,
            estimated_wait_minutes=wait,
            window_start=start,
            window_end=end,
        )
