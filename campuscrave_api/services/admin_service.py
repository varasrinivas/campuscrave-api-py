import logging

from sqlalchemy.orm import Session

from campuscrave_api.errors import NotFoundError
from campuscrave_api.repositories.dish_repository import DishRepository
from campuscrave_api.schemas.menu import DishSummary
from campuscrave_api.services.menu_service import MenuService

log = logging.getLogger(__name__)


class AdminService:
    """What the counter tablet is allowed to change."""

    def __init__(self, session: Session) -> None:
        self.dish_repository = DishRepository(session)
        self.menu_service = MenuService(session)

    def update_stock(self, dish_id: int, stock: int) -> DishSummary:
        """Kitchen cooked a fresh batch — set the shelf count to what is actually there."""
        dish = self.dish_repository.find_by_id(dish_id)
        if dish is None:
            raise NotFoundError(f"No dish with id {dish_id}")

        before = dish.stock
        dish.stock = stock
        self.dish_repository.save(dish)

        log.info("Stock for %s set from %s to %s", dish.name, before, stock)
        return self.menu_service.get_dish(dish_id)
