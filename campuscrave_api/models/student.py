from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from campuscrave_api.models.base import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)

    roll_number: Mapped[str] = mapped_column(String(20), unique=True)

    name: Mapped[str] = mapped_column(String(120))

    email: Mapped[str] = mapped_column(String(160))

    # Where the order gets collected. Block C is the canteen window.
    hostel_block: Mapped[str | None] = mapped_column(String(20))
