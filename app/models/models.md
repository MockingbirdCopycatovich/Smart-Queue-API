# Database Schema 
## Goals - Prevent double booking - Guarantee data consistency - Handle concurrent access 
## Key Decisions - PostgreSQL as source of truth - ENUM types for states - Row-level locking (SELECT FOR UPDATE) 

## Enums
```
CREATE TYPE user_role AS ENUM (
    'CLIENT',
    'OPERATOR',
    'ADMIN'
);

CREATE TYPE timeslot_status AS ENUM (
    'AVAILABLE',
    'HOLD',
    'BOOKED'
);

CREATE TYPE appointment_status AS ENUM (
    'HOLD',
    'CONFIRMED',
    'CANCELLED',
    'NO_SHOW'
);

CREATE TYPE appointment_priority AS ENUM (
    'NORMAL',
    'VIP',
    'URGENT'
);
```

## Tables

### users
```
CREATE TABLE users (
    id              UUID PRIMARY KEY,
    email           TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    role            user_role NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT now()
);
```

### specialists
```
CREATE TABLE specialists (
    id              UUID PRIMARY KEY,
    full_name       TEXT NOT NULL,
    service_type    TEXT NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT now()
);
```

### time_slots
```
CREATE TABLE time_slots (
    id              UUID PRIMARY KEY,
    specialist_id   UUID NOT NULL REFERENCES specialists(id),
    start_time      TIMESTAMP NOT NULL,
    end_time        TIMESTAMP NOT NULL,
    status          timeslot_status NOT NULL DEFAULT 'AVAILABLE',

    CONSTRAINT chk_time_range CHECK (start_time < end_time)
);
```

Indexes:
```
CREATE INDEX idx_time_slots_specialist_time
ON time_slots (specialist_id, start_time, end_time);

CREATE INDEX idx_time_slots_status
ON time_slots (status);
```

### appointments
```
CREATE TABLE appointments (
    id              UUID PRIMARY KEY,
    user_id         UUID NOT NULL REFERENCES users(id),
    specialist_id   UUID NOT NULL REFERENCES specialists(id),
    time_slot_id    UUID NOT NULL UNIQUE REFERENCES time_slots(id),

    status          appointment_status NOT NULL,
    priority        appointment_priority NOT NULL DEFAULT 'NORMAL',

    expires_at      TIMESTAMP,
    created_at      TIMESTAMP NOT NULL DEFAULT now()
);
```
Unique constraint on time_slot_id ensures that only one appointment can exist per slot.


### appointment_events
```
CREATE TABLE appointment_events (
    id              UUID PRIMARY KEY,
    appointment_id  UUID NOT NULL REFERENCES appointments(id),
    event_type      TEXT NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT now()
);
```

## Race Condition Protection
```
BEGIN;

SELECT *
FROM time_slots
WHERE id = :slot_id
AND status = 'AVAILABLE'
FOR UPDATE;

UPDATE time_slots
SET status = 'HOLD'
WHERE id = :slot_id;

INSERT INTO appointments (
    id, user_id, specialist_id, time_slot_id, status, expires_at
)
VALUES (
    :id, :user_id, :specialist_id, :slot_id,
    'HOLD', now() + interval '5 minutes'
);

COMMIT;
```
Transactions are executed with at least REPEATABLE READ isolation level to ensure consistency under concurrent access.
