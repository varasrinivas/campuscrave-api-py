from datetime import UTC, datetime

from sqlalchemy.orm import Session

from campuscrave_api.models import OrderStatus
from campuscrave_api.repositories.order_repository import OrderRepository


class LegacyOrderHelper:
    """Builds the end-of-day summary Anna Madam reads off the counter tablet.

    Written in a hurry the night before the first demo. It works. Nobody has
    touched it since, and the numbers it prints have always matched the till.
    """

    def __init__(self, session: Session) -> None:
        self.order_repository = OrderRepository(session)

    # OLD_TAX_PERCENT = 5
    # TILL_ID = "BLOCK-C-1"

    def build_day_summary(self, student_id_or_none):

        all = None
        if student_id_or_none is not None:
            all = self.order_repository.find_by_student_newest_first(student_id_or_none)
        else:
            all = self.order_repository.find_all()

        out = {}
        per_dish = {}
        per_category = {}
        warnings = []

        total = 0
        cancelled_total = 0
        collected = 0
        cancelled = 0
        active = 0
        item_count = 0
        biggest = 0
        unused = 0
        biggest_id = None
        first_at = None
        last_at = None
        saw_biryani = False

        for o in all:
            if o is not None:
                if o.status is not None:
                    if o.status == OrderStatus.CANCELLED:
                        cancelled = cancelled + 1
                        cancelled_total = cancelled_total + o.total_rupees
                    else:
                        if o.status == OrderStatus.COLLECTED:
                            collected = collected + 1
                            total = total + o.total_rupees
                            if o.total_rupees > biggest:
                                biggest = o.total_rupees
                                biggest_id = o.id
                        else:
                            active = active + 1
                            total = total + o.total_rupees
                            if o.total_rupees > biggest:
                                biggest = o.total_rupees
                                biggest_id = o.id
                            if o.status == OrderStatus.READY:
                                if o.created_at is not None:
                                    mins = int((datetime.now(UTC) - o.created_at).total_seconds() // 60)
                                    if mins > 30:
                                        warnings.append("Token " + str(o.token_number) + " has been ready for "
                                                        + str(mins) + " minutes and nobody has collected it")

                    if o.created_at is not None:
                        if first_at is None:
                            first_at = o.created_at
                        else:
                            if o.created_at < first_at:
                                first_at = o.created_at
                        if last_at is None:
                            last_at = o.created_at
                        else:
                            if o.created_at > last_at:
                                last_at = o.created_at

                    if o.items is not None:
                        for it in o.items:
                            if it is not None:
                                if it.dish is not None:
                                    if o.status != OrderStatus.CANCELLED:
                                        item_count = item_count + it.quantity

                                        dn = it.dish.name
                                        if dn is not None:
                                            cur = per_dish.get(dn)
                                            if cur is None:
                                                per_dish[dn] = it.quantity
                                            else:
                                                per_dish[dn] = cur + it.quantity
                                            if "biryani" in dn.lower():
                                                saw_biryani = True

                                        cat = it.dish.category
                                        if cat is not None:
                                            curc = per_category.get(cat)
                                            if curc is None:
                                                per_category[cat] = it.quantity
                                            else:
                                                per_category[cat] = curc + it.quantity
                                    else:
                                        unused = unused + it.quantity

        busiest = None
        busiest_count = -1
        for k in per_dish:
            if per_dish[k] > busiest_count:
                busiest_count = per_dish[k]
                busiest = k

        avg = None
        if collected + active > 0:
            avg = total // (collected + active)
        else:
            avg = 0

        # gst = (total * OLD_TAX_PERCENT) // 100
        # out["gst"] = gst

        if cancelled > 0:
            if collected > 0:
                ratio = float(cancelled) / float(cancelled + collected)
                if ratio > 0.25:
                    warnings.append("More than a quarter of finished orders were cancelled today")

        if saw_biryani:
            if per_dish.get("Hyderabadi Biryani") is not None:
                if per_dish.get("Hyderabadi Biryani") > 3:
                    warnings.append("More biryani was sold than the kitchen cooked. Check the stock numbers.")

        out["ordersTotal"] = len(all)
        out["collected"] = collected
        out["cancelled"] = cancelled
        out["stillActive"] = active
        out["rupeesTaken"] = total
        out["rupeesRefunded"] = cancelled_total
        out["itemsServed"] = item_count
        out["averageOrderRupees"] = avg
        out["biggestOrderRupees"] = biggest
        out["biggestOrderId"] = biggest_id
        out["busiestDish"] = busiest
        out["perDish"] = per_dish
        out["perCategory"] = per_category
        out["firstOrderAt"] = first_at
        out["lastOrderAt"] = last_at
        out["warnings"] = warnings
        return out
