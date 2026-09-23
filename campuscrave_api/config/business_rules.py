"""The canteen's rules, in one place, with the names everyone uses out loud.

These are the defaults. Anna Madam can override them in the canteen_config
table without waiting for a deploy.
"""

from datetime import time
from typing import Final

# A student may have at most this many orders in flight at once.
MAX_ACTIVE_ORDERS: Final = 3

# No orders after this. IST.
ORDER_CUTOFF: Final = time(14, 30)

# When the queue at the window gets real. IST.
RUSH_WINDOW_START: Final = time(12, 15)
RUSH_WINDOW_END: Final = time(13, 45)

# Minutes added to the quoted wait once the rush is on.
RUSH_WAIT_PENALTY_MINUTES: Final = 6
