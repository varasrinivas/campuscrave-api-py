from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from campuscrave_api.models.base import Base

if TYPE_CHECKING:
    from campuscrave_api.models.dish import Dish
    from campuscrave_api.models.order import Order


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship(back_populates="items")

    dish_id: Mapped[int] = mapped_column(ForeignKey("dishes.id"))
    dish: Mapped["Dish"] = relationship()

    quantity: Mapped[int]

    # Price captured at order time — the menu can change tomorrow.
    unit_price_rupees: Mapped[int]

    @classmethod
    def of(cls, dish: "Dish", quantity: int) -> "OrderItem":
        return cls(dish=dish, quantity=quantity, unit_price_rupees=dish.price_rupees)

    def line_total_rupees(self) -> int:
        return self.unit_price_rupees * self.quantity
