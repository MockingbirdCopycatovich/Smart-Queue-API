from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SpecialistCreate(BaseModel):
    full_name: str
    service_type: str


class SpecialistResponse(BaseModel):
    id: UUID
    full_name: str
    service_type: str
    created_at: datetime

    class Config:
        from_attributes = True
