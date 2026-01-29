from datetime import datetime, timedelta

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.services.booking_service import (
    create_user,
    create_specialist,
    create_time_slot,
    book_time_slot,
    confirm_appointment
)

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    session = SessionLocal()

    user = create_user(session, "demo6@example.com")
    specialist = create_specialist(session, "Dr. House", "Therapist")

    slot = create_time_slot(
        session,
        specialist.id,
        datetime.utcnow(),
        datetime.utcnow() + timedelta(minutes=30),
    )

    appointment = book_time_slot(session, user.id, slot.id)

    print("Appointment ID:", appointment.id)
    
    with SessionLocal() as confirm_session:
        confirmed = confirm_appointment(confirm_session, appointment.id)
        print("CONFIRMED:", confirmed.id)
