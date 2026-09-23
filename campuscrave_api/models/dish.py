from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from campuscrave_api.models.base import Base

if TYPE_CHECKING:
    from campuscrave_api.models.order_item import OrderItem


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(120))

    description: Mapped[str | None] = mapped_column(String(300))

    # Whole rupees. The canteen has never charged paise and never will.
    price_rupees: Mapped[int]

    category: Mapped[str] = mapped_column(String(40))

    vegetarian: Mapped[bool]

    # Portions left today. Reset by the kitchen every morning.
    stock: Mapped[int] = mapped_column(default=0)

    emoji: Mapped[str | None] = mapped_column(String(8))

    prep_minutes: Mapped[int] = mapped_column(default=10)

    wednesday_special: Mapped[bool] = mapped_column(default=False)

    active: Mapped[bool] = mapped_column(default=True)

    # Every line ever ordered for this dish. Loaded the first time you touch it.
    order_items: Mapped[list["OrderItem"]] = relationship(viewonly=True, lazy="select")
