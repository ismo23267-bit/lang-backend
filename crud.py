from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from models import Lesson, Card, User
from schemas import CardCreate
import models
import schemas
from security import hash_password, verify_password


def list_lessons(db: Session):
    return db.scalars(select(Lesson).order_by(Lesson.level, Lesson.id)).all()


def get_lesson(db: Session, lesson_id: int):
    return db.get(Lesson, lesson_id)


def list_cards(db: Session, lesson_id: int):
    lesson = get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return db.scalars(
        select(Card).where(Card.lesson_id == lesson_id).order_by(Card.id)
    ).all()


def create_card(db: Session, payload: CardCreate):
    lesson = get_lesson(db, payload.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    exists = db.execute(
        select(Card).where(
            Card.lesson_id == payload.lesson_id,
            Card.word.ilike(payload.word),
        )
    ).scalars().first()

    if exists:
        raise HTTPException(status_code=409, detail="Word already exists in this lesson")

    card = Card(
        lesson_id=payload.lesson_id,
        word=payload.word.strip(),
        translation=payload.translation.strip(),
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def get_lessons(db: Session):
    return db.query(models.Lesson).all()


def create_lesson(db: Session, lesson: schemas.LessonCreate):
    exists = db.query(models.Lesson).filter(models.Lesson.title == lesson.title).first()
    if exists:
        raise HTTPException(status_code=409, detail="Lesson already exists")

    db_lesson = models.Lesson(
        title=lesson.title,
        level=lesson.level,
        words_count=lesson.words_count
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


def get_user_by_username(db: Session, username: str):
    return db.execute(select(User).where(User.username == username)).scalars().first()


def create_user(db: Session, payload: schemas.UserCreate):
    existing = get_user_by_username(db, payload.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")

    user = User(
        username=payload.username.strip(),
        password_hash=hash_password(payload.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user