from sqlalchemy import select
from sqlalchemy.orm import Session

from campuscrave_api.models import Wallet


class WalletRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_student_id(self, student_id: int) -> Wallet | None:
        query = select(Wallet).where(Wallet.student_id == student_id)
        return self.session.scalars(query).one_or_none()

    def save(self, wallet: Wallet) -> Wallet:
        self.session.add(wallet)
        self.session.commit()
        return wallet
