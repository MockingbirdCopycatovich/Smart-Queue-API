import enum

class UserRole(str, enum.Enum):
    CLIENT = "CLIENT"
    OPERATOR = "OPERATOR"
    ADMIN = "ADMIN"

class TimeSlotStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    HOLD = "HOLD"
    BOOKED = "BOOKED"

class AppointmentStatus(str, enum.Enum):
    HOLD = "HOLD"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"
    EXPIRED = "EXPIRED"

class AppointmentPriority(str, enum.Enum):
    NORMAL = "NORMAL"
    VIP = "VIP"
    URGENT = "URGENT"
