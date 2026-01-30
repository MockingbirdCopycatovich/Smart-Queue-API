from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.specialist import SpecialistCreate, SpecialistResponse
from app.services.booking_service import create_specialist

router = APIRouter(prefix="/specialists", tags=["specialists"])


@router.post("", response_model=SpecialistResponse)
def create(data: SpecialistCreate, db: Session = Depends(get_db)):
    return create_specialist(db, data.full_name, data.service_type)
