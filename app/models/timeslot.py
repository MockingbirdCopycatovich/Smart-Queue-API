import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import TimeSlotStatus

class TimeSlot(Base):
    __tablename__ = "time_slots"

    __table_args__ = (
        CheckConstraint("start_time < end_time", name="chk_time_range"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    specialist_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("specialists.id"),
        nullable=False
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    status: Mapped[TimeSlotStatus] = mapped_column(
        default=TimeSlotStatus.AVAILABLE,
        nullable=False
    )
