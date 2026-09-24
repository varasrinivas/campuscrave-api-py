from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from campuscrave_api.models.base import Base
from campuscrave_api.models.student import Student


class Wallet(Base):
    """The campus wallet. Parents top it up, students spend it on biryani.
    There is no real money here — see PaymentMockService.
    """

    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True)
    student: Mapped[Student] = relationship()

    # Money moves through WalletRepository.debit / credit — one guarded statement each.
    balance_rupees: Mapped[int] = mapped_column(default=0)
