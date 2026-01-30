from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.db.models import TimeSlotStatus


class TimeSlotCreate(BaseModel):
    specialist_id: UUID
    start_time: datetime
    end_time: datetime


class TimeSlotResponse(BaseModel):
    id: UUID
    specialist_id: UUID
    start_time: datetime
    end_time: datetime
    status: TimeSlotStatus

    class Config:
        from_attributes = True
