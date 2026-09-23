from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from campuscrave_api.models.base import Base, UtcDateTime, utc_now
from campuscrave_api.models.order_status import OrderStatus

if TYPE_CHECKING:
    from campuscrave_api.models.order_item import OrderItem
    from campuscrave_api.models.student import Student


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    student: Mapped["Student"] = relationship()

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, native_enum=False, length=20), default=OrderStatus.PLACED
    )

    total_rupees: Mapped[int] = mapped_column(default=0)

    # The canteen token — what the student actually shouts at the window.
    token_number: Mapped[int]

    pickup_block: Mapped[str | None] = mapped_column(String(20))

    created_at: Mapped[datetime] = mapped_column(UtcDateTime, default=utc_now)

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    def add_item(self, item: "OrderItem") -> None:
        self.items.append(item)
