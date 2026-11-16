from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DepartmentBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Engineering"})


class DepartmentResponse(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProjectBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Platform Refresh"})


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class EmployeeBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "John Doe"})
    age: int = Field(..., gt=18, json_schema_extra={"example": 30})
    team: str = Field(..., json_schema_extra={"example": "Backend"})
    capacity_hours: int = Field(default=8, ge=1, json_schema_extra={"example": 8})


class EmployeeCreate(EmployeeBase):
    department_id: int = Field(..., json_schema_extra={"example": 1})
    project_id: Optional[int] = Field(default=None, json_schema_extra={"example": 2})


class EmployeeResponse(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    department: DepartmentResponse
    project: Optional[ProjectResponse] = None


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(default=None, json_schema_extra={"example": "John Doe"})
    age: Optional[int] = Field(default=None, gt=18, json_schema_extra={"example": 30})
    team: Optional[str] = Field(default=None, json_schema_extra={"example": "Backend"})
    capacity_hours: Optional[int] = Field(default=None, ge=1, json_schema_extra={"example": 8})
    department_id: Optional[int] = Field(default=None, json_schema_extra={"example": 1})
    project_id: Optional[int] = Field(default=None, json_schema_extra={"example": 2})
