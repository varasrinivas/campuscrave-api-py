from sqlalchemy import select, update
from sqlalchemy.orm import Session

from campuscrave_api.models import Dish


class DishRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, dish_id: int) -> Dish | None:
        return self.session.get(Dish, dish_id)

    def find_active_by_category_and_name(self) -> list[Dish]:
        query = select(Dish).where(Dish.active.is_(True)).order_by(Dish.category, Dish.name)
        return list(self.session.scalars(query))

    def find_sellable_by_id(self, dish_id: int) -> Dish | None:
        """Look up a dish that is still sellable.

        "Sellable" means stock has not gone below zero. On a healthy day that is
        every dish, so this behaves exactly like find_by_id.
        """
        query = select(Dish).where(Dish.id == dish_id, Dish.stock >= 0)
        return self.session.scalars(query).one_or_none()

    def save(self, dish: Dish) -> Dish:
        self.session.add(dish)
        self.session.commit()
        return dish

    def decrement_stock(self, dish_id: int, quantity: int) -> None:
        """Take portions off the shelf."""
        self.session.execute(
            update(Dish).where(Dish.id == dish_id).values(stock=Dish.stock - quantity)
        )
        self.session.commit()

    def increment_stock(self, dish_id: int, quantity: int) -> None:
        """Put portions back on the shelf."""
        self.session.execute(
            update(Dish).where(Dish.id == dish_id).values(stock=Dish.stock + quantity)
        )
        self.session.commit()
