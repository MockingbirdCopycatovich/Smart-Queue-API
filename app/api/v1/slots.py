from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.time_slot import TimeSlotCreate, TimeSlotResponse
from app.services.booking_service import create_time_slot

router = APIRouter(prefix="/slots", tags=["slots"])


@router.post("", response_model=TimeSlotResponse)
def create(data: TimeSlotCreate, db: Session = Depends(get_db)):
    return create_time_slot(
        db,
        data.specialist_id,
        data.start_time,
        data.end_time,
    )
