from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from deps import get_current_user
from models import Category, CategoryCard
from schemas import CategoryCreate, CategoryOut, CategoryCardCreate, CategoryCardOut

router = APIRouter()


@router.get("", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Category).filter(Category.user_id == current_user.id).all()


@router.post("", response_model=CategoryOut)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_category = Category(
        title=category_data.title,
        user_id=current_user.id,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/{category_id}/cards", response_model=list[CategoryCardOut])
def get_category_cards(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id,
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return db.query(CategoryCard).filter(CategoryCard.category_id == category_id).all()


@router.post("/{category_id}/cards", response_model=CategoryCardOut)
def add_card_to_category(
    category_id: int,
    card_data: CategoryCardCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id,
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_card = CategoryCard(
        category_id=category_id,
        word=card_data.word,
        translation=card_data.translation,
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card