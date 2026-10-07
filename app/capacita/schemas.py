from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EmployeeBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "John Doe"})
    age: int = Field(..., gt=18, json_schema_extra={"example": 30})
    department: str = Field(..., json_schema_extra={"example": "Engineering"})
    team: str = Field(..., json_schema_extra={"example": "Backend"})


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(default=None, json_schema_extra={"example": "John Doe"})
    age: Optional[int] = Field(default=None, gt=18, json_schema_extra={"example": 30})
    department: Optional[str] = Field(default=None, json_schema_extra={"example": "Engineering"})
    team: Optional[str] = Field(default=None, json_schema_extra={"example": "Backend"})
