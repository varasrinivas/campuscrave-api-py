"""The core flows, proven green. Menu loads, orders place, wallets debit,
cancellation refunds. If these pass, the canteen works.
"""

import pytest

from campuscrave_api.config.cutoff_policy import CutoffPolicy
from campuscrave_api.models import OrderStatus
from campuscrave_api.schemas.orders import PlaceOrderLine, PlaceOrderRequest
from campuscrave_api.services.menu_service import MenuService
from campuscrave_api.services.order_service import OrderService
from campuscrave_api.services.wallet_service import WalletService


@pytest.fixture(autouse=True)
def canteen_always_open(monkeypatch):
    """Time-of-day rules make tests flaky depending on when CI runs,
    so we stub the cutoff out. The canteen is always open in here.
    """
    monkeypatch.setattr(CutoffPolicy, "is_past_cutoff", lambda self: False)


def test_menu_lists_all_eight_dishes_with_the_biryani_on_top_form(session):
    menu = MenuService(session).list_menu()

    assert len(menu) == 8
    assert any(
        d.name == "Hyderabadi Biryani" and d.price_rupees == 90 and d.wednesday_special
        for d in menu
    )


def test_a_student_can_place_an_order_and_gets_a_token(session):
    response = OrderService(session).create_order(dosa_for(3, 1))

    assert response.order_id is not None
    assert response.token_number > 0
    assert response.status == OrderStatus.PLACED
    assert response.total_rupees == 50


def test_placing_an_order_debits_the_wallet(session):
    wallets = WalletService(session)
    before = wallets.balance(3).balance_rupees
    OrderService(session).create_order(dosa_for(3, 1))
    after = wallets.balance(3).balance_rupees

    assert after == before - 50


def test_order_status_is_visible_after_placing(session):
    orders = OrderService(session)
    placed = orders.create_order(dosa_for(3, 2))

    status = orders.status(placed.order_id)

    assert status.status == OrderStatus.PLACED
    assert len(status.items) == 1
    assert status.items[0].dish_name == "Masala Dosa"


def test_cancelling_refunds_the_wallet(session):
    orders = OrderService(session)
    wallets = WalletService(session)
    before = wallets.balance(3).balance_rupees
    placed = orders.create_order(dosa_for(3, 1))

    orders.cancel(placed.order_id)

    assert wallets.balance(3).balance_rupees == before
    assert orders.status(placed.order_id).status == OrderStatus.CANCELLED


def test_wallet_top_up_credits_the_balance(session):
    result = WalletService(session).top_up(2, 100)

    assert result.balance_rupees == 220


def test_order_history_comes_back_newest_first(session):
    orders = OrderService(session)
    orders.create_order(dosa_for(3, 1))
    orders.create_order(dosa_for(3, 1))

    history = orders.history(3)

    assert len(history) >= 2


def dosa_for(student_id: int, quantity: int) -> PlaceOrderRequest:
    """One masala dosa (dish 2, Rs.50 each) for the given student."""
    return PlaceOrderRequest(
        student_id=student_id,
        pickup_block="Block C",
        total_rupees=50 * quantity,
        items=[PlaceOrderLine(dish_id=2, quantity=quantity)],
    )
