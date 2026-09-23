from datetime import datetime

from pydantic import Field

from campuscrave_api.models import OrderStatus
from campuscrave_api.schemas import CamelModel


class PlaceOrderLine(CamelModel):
    dish_id: int
    quantity: int = Field(ge=1)


class PlaceOrderRequest(CamelModel):
    """What the browser posts when a student taps "Place order".

    total_rupees is the cart total the web app already worked out and showed
    the student, so the two never disagree on screen.
    """

    student_id: int
    pickup_block: str | None = None
    total_rupees: int = Field(default=0, ge=0)
    items: list[PlaceOrderLine] = Field(min_length=1)


class OrderResponse(CamelModel):
    order_id: int
    token_number: int
    status: OrderStatus
    total_rupees: int
    pickup_block: str | None
    remaining_stock: int


class OrderLine(CamelModel):
    dish_name: str
    quantity: int
    unit_price_rupees: int


class OrderStatusView(CamelModel):
    order_id: int
    token_number: int
    status: OrderStatus
    total_rupees: int
    pickup_block: str | None
    created_at: datetime
    items: list[OrderLine]
