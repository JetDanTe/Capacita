from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Employee
from ..schemas import EmployeeCreate, EmployeeUpdate


def create_employee(session: Session, employee: EmployeeCreate) -> Employee:
    db_employee = Employee(**employee.model_dump())
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee

def get_employee(session: Session, employee_id: int) -> Employee | None:
    return session.get(Employee, employee_id)

def get_employees(session: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
    db_employees = select(Employee)
    db_employees = db_employees.offset(skip).limit(limit)
    return session.scalars(db_employees).all()


def update_employee(session: Session, db_employee: Employee, employee: EmployeeUpdate) -> Employee:
    changes = employee.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(db_employee, field, value)
    session.commit()
    session.refresh(db_employee)
    return db_employee


def delete_employee(session: Session, employee_id: int) -> bool:
    employee = session.get(Employee, employee_id)
    if not employee:
        return False

    session.delete(employee)
    session.commit()
    return True

