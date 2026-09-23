from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from campuscrave_api.models import Order, OrderStatus


class OrderRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, order_id: int) -> Order | None:
        return self.session.get(Order, order_id)

    def find_all(self) -> list[Order]:
        return list(self.session.scalars(select(Order)))

    def find_by_student_newest_first(self, student_id: int) -> list[Order]:
        query = (
            select(Order)
            .where(Order.student_id == student_id)
            .order_by(Order.created_at.desc())
        )
        return list(self.session.scalars(query))

    def count_by_student_and_status_in(self, student_id: int, statuses: list[OrderStatus]) -> int:
        query = select(func.count(Order.id)).where(
            Order.student_id == student_id, Order.status.in_(statuses)
        )
        return self.session.scalar(query)

    def find_highest_token_number(self) -> int:
        return self.session.scalar(select(func.coalesce(func.max(Order.token_number), 0)))

    def count_placed_since(self, since: datetime) -> int:
        query = select(func.count(Order.id)).where(
            Order.created_at >= since, Order.status != OrderStatus.CANCELLED
        )
        return self.session.scalar(query)

    def save(self, order: Order) -> Order:
        self.session.add(order)
        self.session.commit()
        return order
