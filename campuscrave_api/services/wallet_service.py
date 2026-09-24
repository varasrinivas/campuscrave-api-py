from sqlalchemy.orm import Session

from campuscrave_api.errors import NotFoundError
from campuscrave_api.models import Wallet
from campuscrave_api.repositories.wallet_repository import WalletRepository
from campuscrave_api.schemas.wallet import WalletView
from campuscrave_api.services.payment_mock_service import PaymentMockService
from campuscrave_api.settings import get_settings


class WalletService:

    def __init__(self, session: Session, payments: PaymentMockService | None = None) -> None:
        self.wallet_repository = WalletRepository(session)
        self.payments = payments or PaymentMockService(get_settings().payments_api_secret)

    def balance(self, student_id: int) -> WalletView:
        wallet = self._load(student_id)
        return WalletView(student_id=student_id, balance_rupees=wallet.balance_rupees)

    def top_up(self, student_id: int, amount_rupees: int) -> WalletView:
        self._load(student_id)
        self.payments.authorise(student_id, amount_rupees)
        self.wallet_repository.credit(student_id, amount_rupees)
        return WalletView(student_id=student_id, balance_rupees=self._load(student_id).balance_rupees)

    def debit(self, student_id: int, amount_rupees: int) -> None:
        self._load(student_id)
        if not self.wallet_repository.debit(student_id, amount_rupees):
            raise ValueError("Wallet balance too low")

    def refund(self, student_id: int, amount_rupees: int) -> None:
        self._load(student_id)
        self.wallet_repository.credit(student_id, amount_rupees)

    def _load(self, student_id: int) -> Wallet:
        wallet = self.wallet_repository.find_by_student_id(student_id)
        if wallet is None:
            raise NotFoundError(f"No wallet for student {student_id}")
        return wallet
