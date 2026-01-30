from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.models import (
    User,
    Specialist,
    TimeSlot,
    Appointment,
    AppointmentEvent,
)
from app.db.models import (
    TimeSlotStatus,
    AppointmentStatus,
    AppointmentPriority,
)
from uuid import uuid4


def create_user(session: Session, email: str) -> User:
    user = User(
        id=uuid4(),
        email=email,
        password_hash="hash",
        role="CLIENT",
    )
    session.add(user)
    session.commit()
    return user

def create_specialist(session: Session, full_name: str, service_type: str) -> Specialist:
    specialist = Specialist(
        id=uuid4(),
        full_name=full_name,
        service_type=service_type,
    )
    session.add(specialist)
    session.commit()
    return specialist

def create_time_slot(
    session: Session,
    specialist_id: str,
    start_time: datetime,
    end_time: datetime,
) -> TimeSlot:
    slot = TimeSlot(
        id=uuid4(),
        specialist_id=specialist_id,
        start_time=start_time,
        end_time=end_time,
    )
    session.add(slot)
    session.commit()
    return slot

def book_time_slot(session: Session, user_id: str, slot_id: str) -> Appointment:
    try:
        slot = (
            session.query(TimeSlot)
            .filter(
                TimeSlot.id == slot_id,
                TimeSlot.status == TimeSlotStatus.AVAILABLE,
            )
            .with_for_update()
            .one_or_none()
        )

        if slot is None:
            raise ValueError("Time slot is not available")

        appointment = Appointment(
            id=uuid4(),
            user_id=user_id,
            specialist_id=slot.specialist_id,
            time_slot_id=slot.id,
            status=AppointmentStatus.HOLD,
            priority=AppointmentPriority.NORMAL,
            expires_at=datetime.utcnow() + timedelta(minutes=5),
        )

        slot.status = TimeSlotStatus.HOLD

        event = AppointmentEvent(
            id=uuid4(),
            appointment_id=appointment.id,
            event_type="CREATED",
        )

        session.add_all([appointment, event])
        session.commit()

        return appointment

    except Exception:
        session.rollback()
        raise

def confirm_appointment(session: Session, appointment_id):
    with session.begin():

        appointment = session.execute(
            select(Appointment)
            .where(Appointment.id == appointment_id)
            .with_for_update()
        ).scalar_one_or_none()

        if not appointment:
            raise ValueError("Appointment not found")

        if appointment.status != AppointmentStatus.HOLD:
            raise ValueError("Appointment is not in HOLD state")

        if appointment.expires_at and appointment.expires_at < datetime.utcnow():
            raise ValueError("Appointment HOLD expired")

        slot = session.execute(
            select(TimeSlot)
            .where(TimeSlot.id == appointment.time_slot_id)
            .with_for_update()
        ).scalar_one()

        if slot.status != TimeSlotStatus.HOLD:
            raise ValueError("Time slot is not in HOLD state")

        appointment.status = AppointmentStatus.CONFIRMED
        slot.status = TimeSlotStatus.BOOKED

        event = AppointmentEvent(
            id=uuid4(),
            appointment_id=appointment.id,
            event_type="CONFIRMED",
        )
        session.add(event)

    return appointment

def cancel_appointment(session: Session, appointment_id):
    with session.begin():

        appointment = session.execute(
            select(Appointment)
            .where(Appointment.id == appointment_id)
            .with_for_update()
        ).scalar_one_or_none()

        if not appointment:
            raise ValueError("Appointment not found")

        if appointment.status in (
            AppointmentStatus.CANCELLED,
            AppointmentStatus.EXPIRED
        ):
            return appointment

        slot = session.execute(
            select(TimeSlot)
            .where(TimeSlot.id == appointment.time_slot_id)
            .with_for_update()
        ).scalar_one()

        appointment.status = AppointmentStatus.CANCELLED
        slot.status = TimeSlotStatus.AVAILABLE

        event = AppointmentEvent(
            id=uuid4(),
            appointment_id=appointment.id,
            event_type="CANCELLED",
        )
        session.add(event)

    return appointment



def expire_holds(session: Session) -> int:

    now = datetime.utcnow()

    appointments = session.execute(
        select(Appointment)
        .where(
            Appointment.status == AppointmentStatus.HOLD,
            Appointment.expires_at < now,
        )
        .with_for_update()
    ).scalars().all()

    count = 0

    for appointment in appointments:
        slot = session.execute(
            select(TimeSlot)
            .where(TimeSlot.id == appointment.time_slot_id)
            .with_for_update()
        ).scalar_one()

        appointment.status = AppointmentStatus.EXPIRED
        slot.status = TimeSlotStatus.AVAILABLE

        event = AppointmentEvent(
            id=uuid4(),
            appointment_id=appointment.id,
            event_type="EXPIRED",
        )
        session.add(event)

        count += 1

    session.commit()
    return count
