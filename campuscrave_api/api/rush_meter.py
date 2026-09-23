from fastapi import APIRouter

from campuscrave_api.api.deps import SessionDep
from campuscrave_api.schemas.rush import RushMeter
from campuscrave_api.services.rush_meter_service import RushMeterService

router = APIRouter(prefix="/api/rush")


@router.get("")
def current(session: SessionDep) -> RushMeter:
    return RushMeterService(session).current()
