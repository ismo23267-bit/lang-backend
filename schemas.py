from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class LessonOut(BaseModel):
    id: int
    title: str
    level: str
    words_count: int

    class Config:
        from_attributes = True


class CardOut(BaseModel):
    id: int
    word: str
    translation: str

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    title: str


class CategoryOut(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class CategoryCardCreate(BaseModel):
    word: str
    translation: str


class CategoryCardOut(BaseModel):
    id: int
    word: str
    translation: str

    class Config:
        from_attributes = True