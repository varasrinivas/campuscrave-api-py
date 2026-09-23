"""The canteen's tables, as Python classes."""

from campuscrave_api.models.base import Base
from campuscrave_api.models.canteen_config import CanteenConfig
from campuscrave_api.models.dish import Dish
from campuscrave_api.models.order import Order
from campuscrave_api.models.order_item import OrderItem
from campuscrave_api.models.order_status import OrderStatus
from campuscrave_api.models.student import Student
from campuscrave_api.models.wallet import Wallet

__all__ = ["Base", "CanteenConfig", "Dish", "Order", "OrderItem", "OrderStatus", "Student", "Wallet"]
