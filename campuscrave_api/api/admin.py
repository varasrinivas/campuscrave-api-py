"""Anna Madam's counter tablet. No authentication yet — the tablet never
leaves the counter, which is the whole security model for now.
"""

from fastapi import APIRouter

from campuscrave_api.api.deps import SessionDep
from campuscrave_api.schemas.admin import StockUpdateRequest
from campuscrave_api.schemas.menu import DishSummary
from campuscrave_api.services.admin_service import AdminService
from campuscrave_api.services.legacy_order_helper import LegacyOrderHelper

router = APIRouter(prefix="/api/admin")


@router.put("/dishes/{dish_id}/stock")
def update_stock(dish_id: int, request: StockUpdateRequest, session: SessionDep) -> DishSummary:
    return AdminService(session).update_stock(dish_id, request.stock)


@router.get("/summary")
def day_summary(session: SessionDep, studentId: int | None = None) -> dict:  # noqa: N803 — query param name is API contract
    return LegacyOrderHelper(session).build_day_summary(studentId)
