from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from capacita.schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from capacita.storage import get_next_id, load_db, save_db


app = FastAPI(title="Capacita - Backend Capacity Planner API")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/employees/", response_model=list[EmployeeResponse])
async def list_employees(
    skip: int = 0,
    limit: int = 10,
    q: Annotated[str | None, Query(min_length=2, max_length=50)] = None,
    department: Annotated[str | None, Query()] = None,
) -> list[EmployeeResponse]:
    employees = load_db()

    if q:
        query = q.lower()
        employees = [emp for emp in employees if query in emp.get("name", "").lower()]

    if department:
        employees = [emp for emp in employees if emp.get("department") == department]

    return employees[skip : skip + limit]


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int) -> EmployeeResponse:
    employees = load_db()
    for employee in employees:
        if employee.get("id") == employee_id:
            return EmployeeResponse(**employee)
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees/", response_model=EmployeeResponse, status_code=201)
async def create_employee(employee: EmployeeCreate) -> EmployeeResponse:
    employees = load_db()
    record = employee.model_dump()
    record["id"] = get_next_id(employees)
    employees.append(record)
    save_db(employees)
    return EmployeeResponse(**record)


@app.patch("/employees/{employee_id}", response_model=EmployeeResponse)
async def patch_employee(employee_id: int, employee: EmployeeUpdate) -> EmployeeResponse:
    employees = load_db()
    for idx, existing in enumerate(employees):
        if existing.get("id") == employee_id:
            updates = employee.model_dump(exclude_unset=True)
            employees[idx] = {**existing, **updates}
            save_db(employees)
            return EmployeeResponse(**employees[idx])
    raise HTTPException(status_code=404, detail="Employee not found")


@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int) -> dict[str, str]:
    employees = load_db()
    for idx, employee in enumerate(employees):
        if employee.get("id") == employee_id:
            del employees[idx]
            save_db(employees)
            return {"message": "Employee deleted successfully"}
    raise HTTPException(status_code=404, detail="Employee not found")
