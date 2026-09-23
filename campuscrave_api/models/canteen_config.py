from datetime import time

from sqlalchemy.orm import Mapped, mapped_column

from campuscrave_api.models.base import Base


class CanteenConfig(Base):
    """One row. The canteen's own settings, editable by Anna Madam without a redeploy.

    All times in this table are **IST** — the canteen has never thought about
    any other timezone, and neither has this column.
    """

    __tablename__ = "canteen_config"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Last moment an order can be placed for today. Canon: 14:30 IST.
    order_cutoff: Mapped[time]

    # Canon: 12:15 IST.
    rush_start: Mapped[time]

    # Canon: 13:45 IST.
    rush_end: Mapped[time]

    max_active_orders: Mapped[int]

    accepting_orders: Mapped[bool] = mapped_column(default=True)
