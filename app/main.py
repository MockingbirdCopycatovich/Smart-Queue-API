from fastapi import FastAPI

from app.api.v1 import users, specialists, slots, appointments

app = FastAPI(title="Smart Queue API")

app.include_router(users.router, prefix="/api/v1")
app.include_router(specialists.router, prefix="/api/v1")
app.include_router(slots.router, prefix="/api/v1")
app.include_router(appointments.router, prefix="/api/v1")
