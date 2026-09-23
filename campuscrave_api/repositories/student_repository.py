from sqlalchemy import select
from sqlalchemy.orm import Session

from campuscrave_api.models import Student


class StudentRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, student_id: int) -> Student | None:
        return self.session.get(Student, student_id)

    def find_by_roll_number(self, roll_number: str) -> Student | None:
        query = select(Student).where(Student.roll_number == roll_number)
        return self.session.scalars(query).one_or_none()
