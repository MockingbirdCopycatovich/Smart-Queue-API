from fastapi import FastAPI

from app.api.appointments import router as appointments_router
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Queue API")

app.include_router(appointments_router)
