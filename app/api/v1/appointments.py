from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.appointment import AppointmentResponse
from app.services.booking_service import (
    book_time_slot,
    confirm_appointment,
    cancel_appointment,
)

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/book", response_model=AppointmentResponse)
def book(user_id: str, slot_id: str, db: Session = Depends(get_db)):
    return book_time_slot(db, user_id, slot_id)


@router.post("/{appointment_id}/confirm", response_model=AppointmentResponse)
def confirm(appointment_id: str, db: Session = Depends(get_db)):
    return confirm_appointment(db, appointment_id)


@router.post("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel(appointment_id: str, db: Session = Depends(get_db)):
    return cancel_appointment(db, appointment_id)
