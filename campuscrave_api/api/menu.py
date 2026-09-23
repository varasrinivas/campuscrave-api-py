from fastapi import APIRouter

from campuscrave_api.api.deps import SessionDep
from campuscrave_api.schemas.menu import DishSummary
from campuscrave_api.services.menu_service import MenuService

router = APIRouter(prefix="/api/menu")


@router.get("")
def list_menu(session: SessionDep) -> list[DishSummary]:
    return MenuService(session).list_menu()


@router.get("/{dish_id}")
def detail(dish_id: int, session: SessionDep) -> DishSummary:
    return MenuService(session).get_dish(dish_id)
