from fastapi import APIRouter

from campuscrave_api.api.deps import SessionDep
from campuscrave_api.schemas.wallet import TopUpRequest, WalletView
from campuscrave_api.services.wallet_service import WalletService

router = APIRouter(prefix="/api/wallet")


@router.get("/{student_id}")
def balance(student_id: int, session: SessionDep) -> WalletView:
    return WalletService(session).balance(student_id)


@router.post("/{student_id}/topup")
def top_up(student_id: int, request: TopUpRequest, session: SessionDep) -> WalletView:
    return WalletService(session).top_up(student_id, request.amount_rupees)
