from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

from app.models import (
    user,
    specialist,
    timeslot,
    appointment,
    appointment_event,
)

# SQLite in-memory DB
engine = create_engine("sqlite:///:memory:", echo=True)

SessionLocal = sessionmaker(bind=engine)

def main():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully ✅")

if __name__ == "__main__":
    main()
