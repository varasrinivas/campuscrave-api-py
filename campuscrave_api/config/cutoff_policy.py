from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from campuscrave_api.services.canteen_config_service import CanteenConfigService

# India Standard Time runs this far ahead of UTC.
IST_OFFSET_HOURS = 5
IST_OFFSET_MINUTES = 30


class CutoffPolicy:
    """Decides whether the kitchen is still taking orders.

    The cutoff stored in canteen_config is written in IST, because that is what
    Anna Madam types in. The server clock is not guaranteed to be IST, so we shift
    the cutoff onto the server's clock before comparing it with datetime.now().
    """

    def __init__(self, canteen_config: "CanteenConfigService") -> None:
        self.canteen_config = canteen_config

    def cutoff_on_server_clock(self) -> time:
        """The configured IST cutoff, expressed on the server's own clock."""
        shift = timedelta(hours=IST_OFFSET_HOURS, minutes=IST_OFFSET_MINUTES)
        return (datetime.combine(date.today(), self.canteen_config.order_cutoff()) - shift).time()

    def is_past_cutoff(self) -> bool:
        """True once the canteen has stopped taking orders for today."""
        return datetime.now().time() > self.cutoff_on_server_clock()
