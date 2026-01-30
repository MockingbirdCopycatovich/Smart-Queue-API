from app.services.booking_service import cancel_appointment
from app.db.models import AppointmentStatus, TimeSlotStatus

def test_cancel_confirmed(session):
    user = create_user(session, "cancel@example.com")
    specialist = create_specialist(session, "Dr C", "Therapist")

    slot = create_time_slot(
        session,
        specialist.id,
        datetime.utcnow(),
        datetime.utcnow() + timedelta(minutes=30),
    )

    appointment = book_time_slot(session, user.id, slot.id)
    confirm_appointment(session, appointment.id)

    canceled = cancel_appointment(session, appointment.id)

    assert canceled.status == AppointmentStatus.CANCELED
    assert slot.status == TimeSlotStatus.AVAILABLE
