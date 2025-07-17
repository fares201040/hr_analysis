"""Employee schema for HR Analytics API."""

from pydantic import BaseModel


class Employee(BaseModel):
    id: int
    name: str
    department: str
    hire_date: str
