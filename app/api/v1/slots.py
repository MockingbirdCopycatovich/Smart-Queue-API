from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.time_slot import TimeSlotResponse
from app.services.booking_service import get_slots_by_specialist

router = APIRouter(prefix="/slots", tags=["slots"])


@router.get("", response_model=list[TimeSlotResponse])
def list_slots(
    specialist_id: UUID = Query(...),
    db: Session = Depends(get_db),
):
    return get_slots_by_specialist(db, specialist_id)
