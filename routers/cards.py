from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from deps import get_db

router = APIRouter(prefix="/api/v1/cards", tags=["cards"])


@router.post("", response_model=schemas.CardOut)
def create_card(payload: schemas.CardCreate, db: Session = Depends(get_db)):
    return crud.create_card(db, payload)