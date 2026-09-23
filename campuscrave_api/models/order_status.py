from enum import StrEnum


class OrderStatus(StrEnum):
    """The life of an order, as the canteen sees it.

    The status name travels to the browser exactly as spelled here — the web app
    switches on the raw string.
    """

    # Student tapped "Place order". Money is held, the canteen hasn't looked yet.
    PLACED = "PLACED"

    # Anna Madam accepted it at the counter.
    ACCEPTED = "ACCEPTED"

    # On the stove.
    COOKING = "COOKING"

    # Sitting at the Block C window, waiting for a hungry human.
    READY = "READY"

    # Picked up. Done.
    COLLECTED = "COLLECTED"

    # Cancelled by the student before it was cooked.
    CANCELLED = "CANCELLED"

    def is_active(self) -> bool:
        return self not in (OrderStatus.COLLECTED, OrderStatus.CANCELLED)

    def is_cancellable(self) -> bool:
        return self in (OrderStatus.PLACED, OrderStatus.ACCEPTED)
