from datetime import time

from campuscrave_api.schemas import CamelModel


class RushMeter(CamelModel):
    rush_on: bool
    orders_in_last_hour: int
    estimated_wait_minutes: int
    window_start: time
    window_end: time
