from database import SessionLocal
from models import Lesson, Card

db = SessionLocal()

lesson = Lesson(
    title="HSK 1",
    level=1,
    words_count=2,
)
db.add(lesson)
db.commit()
db.refresh(lesson)

cards = [
    Card(word="你好", translation="Привет", lesson_id=lesson.id),
    Card(word="谢谢", translation="Спасибо", lesson_id=lesson.id),
]

db.add_all(cards)
db.commit()
db.close()

print("Seed completed.")