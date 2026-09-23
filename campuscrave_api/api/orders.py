from fastapi import APIRouter, Response, status

from campuscrave_api.api.deps import SessionDep
from campuscrave_api.schemas.orders import OrderResponse, OrderStatusView, PlaceOrderRequest
from campuscrave_api.services.order_service import OrderService

router = APIRouter(prefix="/api/orders")


@router.post("", status_code=status.HTTP_201_CREATED)
def place(request: PlaceOrderRequest, session: SessionDep) -> OrderResponse:
    """Place an order. The request carries the cart total the web app already
    displayed to the student, so the receipt matches what they agreed to pay.
    """
    return OrderService(session).create_order(request)


@router.post("/{order_id}/cancel")
def cancel(order_id: int, session: SessionDep) -> Response:
    OrderService(session).cancel(order_id)
    return Response(status_code=status.HTTP_200_OK)


@router.get("/{order_id}/status")
def order_status(order_id: int, session: SessionDep) -> OrderStatusView:
    return OrderService(session).status(order_id)


@router.get("")
def history(studentId: int, session: SessionDep) -> list[OrderStatusView]:  # noqa: N803 — query param name is API contract
    return OrderService(session).history(studentId)
