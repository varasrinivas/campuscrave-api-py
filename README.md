# campuscrave-api (Python)

The brains behind the token. FastAPI / SQLAlchemy 2 / Python 3.12 backend for
**CampusCrave**, the campus canteen ordering app — and the repo you'll live in
for the *Code With AI* course (Python edition).

> This repo ships in its honest Day-1 state: the happy path works, the demo
> went great, and several things are quietly wrong. That's not an accident —
> it's the course material. Don't fix what a lab hasn't asked you to fix yet.

## Run it

You need [uv](https://docs.astral.sh/uv/). It fetches the right Python for you.

```bash
uv sync
uv run campuscrave
```

- Menu: http://localhost:8080/api/menu
- API docs (try every endpoint from the browser): http://localhost:8080/docs
- Database: a SQLite file at `var/campuscrave.db`, rebuilt from the Day-1 menu
  every time the API starts. Peek inside with `sqlite3 var/campuscrave.db`
  or any SQLite browser.
- The React app (`campuscrave-web`) expects this API on port 8080.

## Test it

```bash
uv run pytest
```

All green. Draw your own conclusions about what that proves.

## The map

```
campuscrave_api/
├── api/            HTTP in: menu, orders, wallet, rush meter, admin
├── services/       the rules: order_service.py is where orders become tokens
├── repositories/   every SQL query the API makes
├── models/         Student, Dish, Order, OrderItem, Wallet, CanteenConfig
├── schemas/        shapes crossing the HTTP boundary (camelCase on the wire)
├── config/         business_rules (MAX_ACTIVE_ORDERS = 3, ORDER_CUTOFF 14:30 IST), cutoff_policy
├── db/             session per request, startup bootstrap, data.sql
├── errors.py       ApiError family + the one place failures become responses
└── settings.py     reads config/application.toml
```

Schema lives in Alembic (`migrations/versions`), Day-1 menu in
`campuscrave_api/db/data.sql` (Wednesday special: Hyderabadi Biryani, ₹90, stock 3).

## Folders you'll meet later

- `hints/` — optional per-bug reproduction scripts; open only when a lab says so.
- `incident/` — sealed until Episode 42. No peeking; it's better live.
