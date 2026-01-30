from app.db.session import SessionLocal
from app.db.models import (
    User,
    Specialist,
    TimeSlot,
    Appointment,
    AppointmentEvent,
)

def inspect_db():
    session = SessionLocal()

    print("\n=== USERS ===")
    for u in session.query(User).all():
        print(f"{u.id} | {u.email} | active={u.is_active}")

    print("\n=== SPECIALISTS ===")
    for s in session.query(Specialist).all():
        print(f"{s.id} | {s.full_name} | {s.service_type}")

    print("\n=== TIME SLOTS ===")
    for ts in session.query(TimeSlot).all():
        print(
            f"{ts.id} | specialist={ts.specialist_id} | "
            f"{ts.start_time} - {ts.end_time} | status={ts.status}"
        )

    print("\n=== APPOINTMENTS ===")
    for a in session.query(Appointment).all():
        print(
            f"{a.id} | user={a.user_id} | slot={a.time_slot_id} | "
            f"status={a.status} | expires={a.expires_at}"
        )

    print("\n=== APPOINTMENT EVENTS ===")
    for e in session.query(AppointmentEvent).all():
        print(
            f"{e.id} | appointment={e.appointment_id} | "
            f"{e.event_type} | {e.created_at}"
        )

    session.close()

if __name__ == "__main__":
    inspect_db()
