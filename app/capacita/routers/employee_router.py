from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import session

from ..dependencies import SessionDep
from ..services import employees_service as emp_service
from ..schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate


router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=list[EmployeeResponse])
async def list_employees(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
) -> list[EmployeeResponse]:
    employees = emp_service.get_employees(session, skip=skip, limit=limit)
    return [EmployeeResponse.model_validate(employee) for employee in employees]


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int, session: SessionDep) -> EmployeeResponse:
    employee = emp_service.get_employee(session, employee_id)
    if employee:
        return EmployeeResponse.model_validate(employee)
    raise HTTPException(status_code=404, detail="Employee not found")


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate, session: SessionDep) -> EmployeeResponse:
    return EmployeeResponse.model_validate(emp_service.create_employee(session, employee))


@router.patch("/{employee_id}", response_model=EmployeeResponse)
async def patch_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    session: SessionDep,
) -> EmployeeResponse:
    db_employee = emp_service.get_employee(session, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeResponse.model_validate(emp_service.update_employee(session, db_employee, employee))

@router.delete("/{employee_id}")
async def delete_employee(employee_id: int, session: SessionDep) -> dict[str, str]:
    deleted_employee = emp_service.get_employee(session, employee_id)
    if not deleted_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp_service.delete_employee(session, employee_id)
    return {"message": "Employee deleted successfully"}