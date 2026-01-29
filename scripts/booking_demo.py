from datetime import datetime, timedelta

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.services.booking_service import (
    create_user,
    create_specialist,
    create_time_slot,
    book_time_slot,
)

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    session = SessionLocal()

    user = create_user(session, "demo2@example.com")
    specialist = create_specialist(session, "Dr. House", "Therapist")

    slot = create_time_slot(
        session,
        specialist.id,
        datetime.utcnow(),
        datetime.utcnow() + timedelta(minutes=30),
    )

    appointment = book_time_slot(session, user.id, slot.id)

    print("Appointment ID:", appointment.id)
