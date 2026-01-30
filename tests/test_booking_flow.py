from datetime import datetime, timedelta

from app.services.booking_service import (
    create_user,
    create_specialist,
    create_time_slot,
    book_time_slot,
    confirm_appointment,
)
from app.db.models import AppointmentStatus, TimeSlotStatus


def test_booking_and_confirm(session):
    user = create_user(session, "test@example.com")
    specialist = create_specialist(session, "Dr Test", "Therapist")

    slot = create_time_slot(
        session,
        specialist.id,
        datetime.utcnow(),
        datetime.utcnow() + timedelta(minutes=30),
    )

    appointment = book_time_slot(session, user.id, slot.id)

    assert appointment.status == AppointmentStatus.HOLD

    confirmed = confirm_appointment(session, appointment.id)

    assert confirmed.status == AppointmentStatus.CONFIRMED
    assert slot.status == TimeSlotStatus.BOOKED

import pytest

def test_double_booking_fails(session):
    user1 = create_user(session, "a@example.com")
    user2 = create_user(session, "b@example.com")
    specialist = create_specialist(session, "Dr X", "Therapist")

    slot = create_time_slot(
        session,
        specialist.id,
        datetime.utcnow(),
        datetime.utcnow() + timedelta(minutes=30),
    )

    book_time_slot(session, user1.id, slot.id)

    with pytest.raises(ValueError):
        book_time_slot(session, user2.id, slot.id)
