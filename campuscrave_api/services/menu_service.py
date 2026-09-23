from sqlalchemy.orm import Session

from campuscrave_api.errors import NotFoundError
from campuscrave_api.models import Dish
from campuscrave_api.repositories.dish_repository import DishRepository
from campuscrave_api.schemas.menu import DishSummary


class MenuService:

    def __init__(self, session: Session) -> None:
        self.dish_repository = DishRepository(session)

    def list_menu(self) -> list[DishSummary]:
        """Today's menu, with a "sold so far" number behind each dish so the web app can
        put a bestseller flame on the popular ones.
        """
        dishes = self.dish_repository.find_active_by_category_and_name()

        menu = []
        for dish in dishes:
            sold_so_far = 0
            for item in dish.order_items:
                sold_so_far += item.quantity
            menu.append(self._to_summary(dish, sold_so_far))
        return menu

    def get_dish(self, dish_id: int) -> DishSummary:
        dish = self.dish_repository.find_by_id(dish_id)
        if dish is None:
            raise NotFoundError(f"No dish with id {dish_id}")

        sold_so_far = sum(item.quantity for item in dish.order_items)
        return self._to_summary(dish, sold_so_far)

    @staticmethod
    def _to_summary(dish: Dish, sold_so_far: int) -> DishSummary:
        return DishSummary(
            id=dish.id,
            name=dish.name,
            description=dish.description,
            price_rupees=dish.price_rupees,
            category=dish.category,
            vegetarian=dish.vegetarian,
            stock=dish.stock,
            emoji=dish.emoji,
            prep_minutes=dish.prep_minutes,
            wednesday_special=dish.wednesday_special,
            sold_so_far=sold_so_far,
        )
