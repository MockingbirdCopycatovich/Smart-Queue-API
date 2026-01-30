from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.db.models import AppointmentStatus, AppointmentPriority


class AppointmentCreate(BaseModel):
    user_id: UUID
    time_slot_id: UUID


class AppointmentResponse(BaseModel):
    id: UUID
    user_id: UUID
    specialist_id: UUID
    time_slot_id: UUID
    status: AppointmentStatus
    priority: AppointmentPriority
    expires_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True
