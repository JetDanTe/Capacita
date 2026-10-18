from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


name_length = 50



class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(name_length), nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    department: Mapped[str] = mapped_column(String(name_length), nullable=False)
    team: Mapped[str] = mapped_column(String(name_length), nullable=False)
