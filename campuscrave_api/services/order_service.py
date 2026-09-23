import logging

from sqlalchemy.orm import Session

from campuscrave_api.config.cutoff_policy import CutoffPolicy
from campuscrave_api.errors import (
    CanteenClosedError,
    NotFoundError,
    OutOfStockError,
    TooManyActiveOrdersError,
)
from campuscrave_api.models import Order, OrderItem, OrderStatus
from campuscrave_api.repositories.dish_repository import DishRepository
from campuscrave_api.repositories.order_repository import OrderRepository
from campuscrave_api.repositories.student_repository import StudentRepository
from campuscrave_api.schemas.orders import (
    OrderLine,
    OrderResponse,
    OrderStatusView,
    PlaceOrderRequest,
)
from campuscrave_api.services.canteen_config_service import CanteenConfigService
from campuscrave_api.services.wallet_service import WalletService

log = logging.getLogger(__name__)

ACTIVE_STATUSES = [OrderStatus.PLACED, OrderStatus.ACCEPTED, OrderStatus.COOKING, OrderStatus.READY]


class OrderService:
    """Everything that happens between "Place order" and a token number."""

    def __init__(self, session: Session) -> None:
        self.order_repository = OrderRepository(session)
        self.dish_repository = DishRepository(session)
        self.student_repository = StudentRepository(session)
        self.wallet_service = WalletService(session)
        self.canteen_config = CanteenConfigService(session)
        self.cutoff_policy = CutoffPolicy(self.canteen_config)

    def create_order(self, request: PlaceOrderRequest) -> OrderResponse:
        """Place an order and mint a token."""
        student = self.student_repository.find_by_id(request.student_id)
        if student is None:
            raise NotFoundError(f"No student with id {request.student_id}")

        if not self.canteen_config.is_accepting_orders():
            raise CanteenClosedError("The canteen has stopped taking orders")
        if self.cutoff_policy.is_past_cutoff():
            raise CanteenClosedError(f"Orders close at {self.canteen_config.order_cutoff():%H:%M} IST")

        order = Order(student=student, token_number=self._next_token_number(), pickup_block=request.pickup_block)

        for line in request.items:
            dish = self.dish_repository.find_by_id(line.dish_id)
            if dish is None:
                raise NotFoundError(f"No dish with id {line.dish_id}")

            if dish.stock < line.quantity:
                raise OutOfStockError(dish.name)
            order.add_item(OrderItem.of(dish, line.quantity))

        order.total_rupees = request.total_rupees
        self.wallet_service.debit(student.id, request.total_rupees)

        saved = self.order_repository.save(order)

        active = self.order_repository.count_by_student_and_status_in(student.id, ACTIVE_STATUSES)
        if active > self.canteen_config.max_active_orders():
            raise TooManyActiveOrdersError(self.canteen_config.max_active_orders())

        for line in request.items:
            self.dish_repository.decrement_stock(line.dish_id, line.quantity)

        log.info("Order %s placed by student %s — token %s", saved.id, student.id, saved.token_number)

        headline_dish_id = request.items[0].dish_id
        dish = self.dish_repository.find_sellable_by_id(headline_dish_id)
        remaining_stock = dish.stock

        return OrderResponse(
            order_id=saved.id,
            token_number=saved.token_number,
            status=saved.status,
            total_rupees=saved.total_rupees,
            pickup_block=saved.pickup_block,
            remaining_stock=remaining_stock,
        )

    def cancel(self, order_id: int) -> None:
        """Student changed their mind. Money goes back to the wallet."""
        order = self.order_repository.find_by_id(order_id)
        if order is None:
            raise NotFoundError(f"No order with id {order_id}")

        if not order.status.is_cancellable():
            raise CanteenClosedError(f"Order {order_id} is already {order.status}")

        order.status = OrderStatus.CANCELLED
        self.order_repository.save(order)

        self.wallet_service.refund(order.student_id, order.total_rupees)

        log.info("Order %s cancelled, Rs.%s refunded", order_id, order.total_rupees)

    def status(self, order_id: int) -> OrderStatusView:
        order = self.order_repository.find_by_id(order_id)
        if order is None:
            raise NotFoundError(f"No order with id {order_id}")
        return self._to_status_view(order)

    def history(self, student_id: int) -> list[OrderStatusView]:
        return [
            self._to_status_view(order)
            for order in self.order_repository.find_by_student_newest_first(student_id)
        ]

    @staticmethod
    def _to_status_view(order: Order) -> OrderStatusView:
        lines = [
            OrderLine(dish_name=item.dish.name, quantity=item.quantity, unit_price_rupees=item.unit_price_rupees)
            for item in order.items
        ]
        return OrderStatusView(
            order_id=order.id,
            token_number=order.token_number,
            status=order.status,
            total_rupees=order.total_rupees,
            pickup_block=order.pickup_block,
            created_at=order.created_at,
            items=lines,
        )

    def _next_token_number(self) -> int:
        return self.order_repository.find_highest_token_number() + 1
