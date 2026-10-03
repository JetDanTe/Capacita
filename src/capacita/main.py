from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from capacita.schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from capacita.settings import settings
from capacita.storage import get_next_id, load_db, save_db


TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"

app = FastAPI(title="Capacita - Backend Capacity Planner API")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.api_route("/health", methods=["GET", "HEAD"])
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


@app.get("/employees/new")
async def add_employee_page(request: Request):
    return templates.TemplateResponse(request=request, name="employee_add.html", context={})


@app.post("/employees/new")
async def add_employee_form(
    name: str = Form(...),
    age: int = Form(...),
    department: str = Form(...),
    team: str = Form(...),
):
    employees = load_db()
    record = EmployeeCreate(
        name=name,
        age=age,
        department=department,
        team=team,
    ).model_dump()
    record["id"] = get_next_id(employees)
    employees.append(record)
    save_db(employees)
    return RedirectResponse(url="/", status_code=303)


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


@app.api_route("/", methods=["GET", "HEAD"])
async def employees_page(request: Request):
    employees = load_db()
    return templates.TemplateResponse(
        request=request,
        name="employees.html",
        context={"employees": employees},
    )


@app.get("/employees/{employee_id}/edit")
async def edit_employee_page(request: Request, employee_id: int):
    employees = load_db()
    for employee in employees:
        if employee.get("id") == employee_id:
            return templates.TemplateResponse(
                request=request,
                name="employee_edit.html",
                context={"employee": employee},
            )
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees/{employee_id}/edit")
async def edit_employee_form(
    employee_id: int,
    name: str = Form(...),
    age: int = Form(...),
    department: str = Form(...),
    team: str = Form(...),
):
    employees = load_db()
    for idx, existing in enumerate(employees):
        if existing.get("id") == employee_id:
            updates = EmployeeUpdate(
                name=name,
                age=age,
                department=department,
                team=team,
            ).model_dump(exclude_unset=True)
            employees[idx] = {**existing, **updates}
            save_db(employees)
            return RedirectResponse(url="/", status_code=303)
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees/{employee_id}/delete")
async def delete_employee_form(employee_id: int):
    employees = load_db()
    for idx, employee in enumerate(employees):
        if employee.get("id") == employee_id:
            del employees[idx]
            save_db(employees)
            return RedirectResponse(url="/", status_code=303)
    raise HTTPException(status_code=404, detail="Employee not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("capacita.main:app", host=settings.host, port=settings.port, reload=False)

