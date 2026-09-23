from pydantic import Field

from campuscrave_api.schemas import CamelModel


class WalletView(CamelModel):
    student_id: int
    balance_rupees: int


class TopUpRequest(CamelModel):
    amount_rupees: int = Field(ge=1)
