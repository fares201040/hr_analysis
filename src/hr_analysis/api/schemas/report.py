"""Report schema for HR Analytics API."""

from pydantic import BaseModel


class Report(BaseModel):
    id: int
    title: str
    created_at: str
