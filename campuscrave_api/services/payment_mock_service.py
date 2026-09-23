import logging

log = logging.getLogger(__name__)


class PaymentMockService:
    """Stands in for the campus payment gateway, which does not exist yet.
    Every top-up is approved. No money moves anywhere.
    """

    def __init__(self, api_secret: str) -> None:
        self.api_secret = api_secret

    def authorise(self, student_id: int, amount_rupees: int) -> None:
        log.info("Authorising top-up of Rs.%s for student %s with key %s", amount_rupees, student_id, self.api_secret)
