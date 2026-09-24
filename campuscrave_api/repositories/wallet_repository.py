from sqlalchemy import select, update
from sqlalchemy.orm import Session

from campuscrave_api.models import Wallet


class WalletRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_student_id(self, student_id: int) -> Wallet | None:
        query = select(Wallet).where(Wallet.student_id == student_id)
        return self.session.scalars(query).one_or_none()

    def debit(self, student_id: int, rupees: int) -> bool:
        """Take money out in one statement, and only if it is there. False means too low.

        The check and the subtraction happen together in the database, so two orders
        landing at once cannot both read the same balance and each write back their own answer.
        """
        result = self.session.execute(
            update(Wallet)
            .where(Wallet.student_id == student_id, Wallet.balance_rupees >= rupees)
            .values(balance_rupees=Wallet.balance_rupees - rupees)
        )
        self.session.commit()
        return result.rowcount == 1

    def credit(self, student_id: int, rupees: int) -> None:
        """Put money in, in one statement."""
        self.session.execute(
            update(Wallet)
            .where(Wallet.student_id == student_id)
            .values(balance_rupees=Wallet.balance_rupees + rupees)
        )
        self.session.commit()
