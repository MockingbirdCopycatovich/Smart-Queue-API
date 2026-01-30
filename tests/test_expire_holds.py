from datetime import datetime, timedelta

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.services.booking_service import (
    create_user,
    create_specialist,
    create_time_slot,
    book_time_slot,
    expire_holds,
)
from app.db.models import AppointmentStatus, TimeSlotStatus


def test_expire_hold():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = SessionLocal()

    user = create_user(session, "expire@example.com")
    specialist = create_specialist(session, "Dr. Who", "Time")

    slot = create_time_slot(
        session,
        specialist.id,
        datetime.utcnow(),
        datetime.utcnow() + timedelta(minutes=30),
    )

    appointment = book_time_slot(session, user.id, slot.id)

    appointment.expires_at = datetime.utcnow() - timedelta(minutes=1)
    session.commit()

    expired = expire_holds(session)

    session.refresh(appointment)
    session.refresh(slot)

    assert expired == 1
    assert appointment.status == AppointmentStatus.EXPIRED
    assert slot.status == TimeSlotStatus.AVAILABLE

    session.close()
