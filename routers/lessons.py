from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Lesson, Card
from schemas import LessonOut, CardOut

router = APIRouter()


@router.get("", response_model=list[LessonOut])
def get_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).all()


@router.get("/{lesson_id}/cards", response_model=list[CardOut])
def get_lesson_cards(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return db.query(Card).filter(Card.lesson_id == lesson_id).all()