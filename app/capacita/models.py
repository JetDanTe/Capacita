from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

name_length = 50

class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(name_length), nullable=False)
    employees: Mapped[list["Employee"]] = relationship(
        back_populates="department",
        cascade="all, delete-orphan",
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(name_length), nullable=False)
    employees: Mapped[list["Employee"]] = relationship(back_populates="project")


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(name_length), nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    team: Mapped[str] = mapped_column(String(name_length), nullable=False)
    capacity_hours: Mapped[int] = mapped_column(default=8, nullable=False)
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False,
    )
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    department: Mapped[Department] = relationship(back_populates="employees")
    project: Mapped[Project | None] = relationship(back_populates="employees")
