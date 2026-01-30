from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.deps import get_db
from app.services.booking_service import (
    book_time_slot,
    confirm_appointment,
    cancel_appointment,
)

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/{slot_id}/book")
def book(slot_id: UUID, user_id: UUID, db: Session = Depends(get_db)):
    try:
        appointment = book_time_slot(db, user_id, slot_id)
        return {"id": appointment.id, "status": appointment.status}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/{appointment_id}/confirm")
def confirm(appointment_id: UUID, db: Session = Depends(get_db)):
    try:
        appointment = confirm_appointment(db, appointment_id)
        return {"id": appointment.id, "status": appointment.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{appointment_id}/cancel")
def cancel(appointment_id: UUID, db: Session = Depends(get_db)):
    try:
        appointment = cancel_appointment(db, appointment_id)
        return {"id": appointment.id, "status": appointment.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
