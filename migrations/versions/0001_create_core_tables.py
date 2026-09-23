"""CampusCrave core schema.

SQLite in dev, Postgres in prod — everything here is written with Alembic's
portable operations, so the same file builds both.

Revision ID: 0001
Revises:
"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "students",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("roll_number", sa.String(20), nullable=False, unique=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(160), nullable=False),
        sa.Column("hostel_block", sa.String(20)),
    )

    op.create_table(
        "wallets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("students.id"), nullable=False, unique=True),
        sa.Column("balance_rupees", sa.Integer, nullable=False, server_default="0"),
    )

    op.create_table(
        "dishes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("description", sa.String(300)),
        sa.Column("price_rupees", sa.Integer, nullable=False),
        sa.Column("category", sa.String(40), nullable=False),
        sa.Column("vegetarian", sa.Boolean, nullable=False),
        sa.Column("stock", sa.Integer, nullable=False, server_default="0"),
        sa.Column("emoji", sa.String(8)),
        sa.Column("prep_minutes", sa.Integer, nullable=False, server_default="10"),
        sa.Column("wednesday_special", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("active", sa.Boolean, nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("students.id"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("total_rupees", sa.Integer, nullable=False),
        sa.Column("token_number", sa.Integer, nullable=False),
        sa.Column("pickup_block", sa.String(20)),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("dish_id", sa.Integer, sa.ForeignKey("dishes.id"), nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("unit_price_rupees", sa.Integer, nullable=False),
    )

    op.create_table(
        "canteen_config",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=False),
        sa.Column("order_cutoff", sa.Time, nullable=False),
        sa.Column("rush_start", sa.Time, nullable=False),
        sa.Column("rush_end", sa.Time, nullable=False),
        sa.Column("max_active_orders", sa.Integer, nullable=False),
        sa.Column("accepting_orders", sa.Boolean, nullable=False, server_default=sa.true()),
    )

    op.create_index("idx_orders_student", "orders", ["student_id"])
    op.create_index("idx_orders_status", "orders", ["status"])
    op.create_index("idx_order_items_order", "order_items", ["order_id"])
    op.create_index("idx_order_items_dish", "order_items", ["dish_id"])


def downgrade() -> None:
    for table in ("order_items", "orders", "canteen_config", "dishes", "wallets", "students"):
        op.drop_table(table)
