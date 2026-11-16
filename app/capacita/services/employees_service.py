from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..models import Employee
from ..schemas import EmployeeCreate, EmployeeUpdate


def _employee_query():
    return select(Employee).options(
        selectinload(Employee.department),
        selectinload(Employee.project),
    )


def create_employee(session: Session, employee: EmployeeCreate) -> Employee:
    db_employee = Employee(**employee.model_dump())
    session.add(db_employee)
    session.commit()
    return get_employee(session, db_employee.id) or db_employee

def get_employee(session: Session, employee_id: int) -> Employee | None:
    stmt = _employee_query().where(Employee.id == employee_id)
    return session.scalars(stmt).first()

def get_employees(session: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
    db_employees = _employee_query()
    db_employees = db_employees.offset(skip).limit(limit)
    return list(session.scalars(db_employees).all())


def update_employee(session: Session, db_employee: Employee, employee: EmployeeUpdate) -> Employee:
    changes = employee.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(db_employee, field, value)
    session.commit()
    return get_employee(session, db_employee.id) or db_employee


def delete_employee(session: Session, employee_id: int) -> bool:
    employee = session.get(Employee, employee_id)
    if not employee:
        return False

    session.delete(employee)
    session.commit()
    return True

